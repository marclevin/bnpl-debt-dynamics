"""How much does the DEFINITION of the hypothetical cap matter?

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/cap_definitions.py

The model implements definition (a), following the decision register. Definitions (b) and
(c) are NOT part of the model: they are patched in here, for this diagnostic only, to show
what the alternative readings of "a cap" would give. Seeds 43,000-43,019, as the cap arms.

  (a) platforms owed, freeze at the cap   the model: at the cap every new draw is refused
  (b) platforms owed, top-ups allowed     at the cap a draw may still use a platform already owed
  (c) agreements                          at most `cap` open agreements, on any platforms
"""
from __future__ import annotations

import math
import warnings

import pandas as pd
from joblib import Parallel, delayed

from simulation.affordability import nca_gate
from simulation.config import MONTHLY_TO_TICK, ParamSet

P, F = 0.016, 0.09


def n_agreements(agent) -> int:
    return sum(len(pl.loans.get(agent.agent_id, ())) for pl in agent.model.platforms)


def make_draw(definition: str):
    def _bnpl_draw(self, amount: float) -> float:
        p = self.model.params
        cap = p.stacking_cap
        if amount <= 0:
            return 0.0
        if definition == "agreements" and n_agreements(self) >= cap:
            return 0.0
        if p.bnpl_affordability_check:
            visible = (self.scheduled_service_tick + self.bnpl_obligations_per_tick()) / MONTHLY_TO_TICK
            if not nca_gate(self.income_monthly, visible, (amount / p.bnpl_instalments) / MONTHLY_TO_TICK):
                return 0.0
        order = list(self.model.platforms)
        self.model.rng.shuffle(order)
        financed = 0.0
        for platform in order:
            if financed >= amount:
                break
            if definition == "platforms_topup":
                if not platform.has_balance(self.agent_id) and self.stacking_depth() >= cap:
                    continue
            elif n_agreements(self) >= cap:
                break
            financed += platform.request(self.agent_id, amount - financed, self.model.tick)
        self.bnpl_volume_tick += financed
        return financed

    return _bnpl_draw


def run(definition: str, params: ParamSet) -> dict:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        from simulation.agents import HouseholdAgent
        from simulation.model import BNPLModel

        original = HouseholdAgent._bnpl_draw
        if definition != "model" and params.stacking_cap is not None:
            HouseholdAgent._bnpl_draw = make_draw(definition)
        try:
            out = BNPLModel(params).run()
        finally:
            HouseholdAgent._bnpl_draw = original
    out["definition"] = definition
    return out


if __name__ == "__main__":
    jobs = []
    for beta in (0.0, 1.0):
        for seed in range(43_000, 43_020):
            base = dict(shock_prob=P, payment_friction=F, bnpl_enabled=True, beta=beta, seed=seed)
            jobs.append(("model", ParamSet(**base, label=f"none_b{beta:g}")))
            for cap in (1, 2, 3):
                for d in ("model", "platforms_topup", "agreements"):
                    jobs.append((d, ParamSet(**base, stacking_cap=cap, label=f"cap{cap}_b{beta:g}")))
    df = pd.DataFrame(Parallel(n_jobs=14)(delayed(run)(d, p) for d, p in jobs))
    names = {"model": "(a) platforms, freeze at cap [the model]", "platforms_topup": "(b) platforms, top-ups allowed",
             "agreements": "(c) agreements"}
    rows = []
    for beta in (0.0, 1.0):
        bench = df[df.label == f"none_b{beta:g}"].set_index("seed")
        for cap in (1, 2, 3):
            for d in ("model", "platforms_topup", "agreements"):
                a = df[(df.label == f"cap{cap}_b{beta:g}") & (df.definition == d)].set_index("seed")
                z = (a.default_rate_final - bench.default_rate_final) * 100
                rows.append({
                    "beta": beta, "cap": cap, "definition": names[d],
                    "default less no cap (pp)": f"{z.mean():+.2f} ± {z.std(ddof=1) / math.sqrt(len(z)):.2f}",
                    "volume vs no cap (%)": f"{(a.bnpl_volume_cumulative.mean() / bench.bnpl_volume_cumulative.mean() - 1) * 100:+.1f}",
                })
    out = pd.DataFrame(rows)
    text = out.to_markdown(index=False)
    print(text)
    from pathlib import Path
    Path(__file__).with_name("cap_definitions.md").write_text(
        "# The hypothetical cap under three definitions\n\n"
        "Diagnostic only. The model implements definition (a). Paired by seed against a no-cap arm "
        "on the same seeds (43,000-43,019), one standard error. Corrected code, fitted parameters.\n\n"
        + text + "\n")
