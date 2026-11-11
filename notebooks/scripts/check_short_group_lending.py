"""Audit 2026-11-11: which of the households short of food and rent does the lender lend to?

The group is `income_tick < committed_tick` (Section 3.5; check_short_group.py). Its members not
in default at the start (120 of 182) are split by whether the traditional lender's Regulation 23A
gate grants them any loan during the baseline run without BNPL. The script runs the rq0 seeds with
BNPL off and with BNPL on at beta = 0 and counts default during the run in each part. It writes
results/summary/short_group_lending.json, the source of the split reported in Sections 3.5 and 4.1.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_short_group_lending.py
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path
from statistics import mean, stdev

warnings.simplefilter("ignore")
from simulation.experiments import calibrated  # noqa: E402
from simulation.lender import TraditionalLender  # noqa: E402
from simulation.model import BNPLModel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SEEDS = range(10_000, 10_020)  # rq0 seeds
TICKS = 52


def run(seed: int, bnpl: bool) -> dict:
    m = BNPLModel(calibrated(bnpl_enabled=bnpl, beta=0.0, label="short_lending").replace(seed=seed))
    at_risk = {a.agent_id for a in m.agents if a.income_tick < a.committed_tick and not a.defaulted}
    granted: set[int] = set()
    counts = {"applications": 0, "grants": 0, "refusals": 0}
    original = TraditionalLender.apply

    def apply(self, agent, amount):
        got = original(self, agent, amount)
        if agent.agent_id in at_risk and amount > 0:
            counts["applications"] += 1
            if got > 0:
                counts["grants"] += 1
                granted.add(agent.agent_id)
            else:
                counts["refusals"] += 1
        return got

    TraditionalLender.apply = apply
    try:
        for _ in range(TICKS):
            m.step()
    finally:
        TraditionalLender.apply = original
    defaulted = {a.agent_id for a in m.agents if a.agent_id in at_risk and a.defaulted}
    return {"at_risk": at_risk, "granted": granted, "defaulted": defaulted, **counts,
            "refusals_all": m.lender.n_refused_gate if hasattr(m, "lender") else None}


def main() -> None:
    rows = []
    for seed in SEEDS:
        off, on = run(seed, False), run(seed, True)
        assert off["at_risk"] == on["at_risk"]
        lent = off["granted"]                 # the split: lent to in the baseline without BNPL
        never = off["at_risk"] - lent
        rows.append({
            "seed": seed,
            "at_risk": len(off["at_risk"]),
            "lent_to": len(lent),
            "never_lent_to": len(never),
            "lent_to_default_off": len(off["defaulted"] & lent),
            "lent_to_default_on": len(on["defaulted"] & lent),
            "never_default_off": len(off["defaulted"] & never),
            "never_default_on": len(on["defaulted"] & never),
            "never_granted_in_bnpl_arm": len(on["granted"] & never),
            "group_refusals_off": off["refusals"],
            "group_refusals_on": on["refusals"],
            "all_refusals_off": off["refusals_all"],
            "all_refusals_on": on["refusals_all"],
            "lent_set": sorted(lent),
        })
    same_split = all(r["lent_set"] == rows[0]["lent_set"] for r in rows)
    keys = [k for k in rows[0] if k not in ("seed", "lent_set")]
    summary = {k: {"mean": mean(r[k] for r in rows), "sd": stdev(r[k] for r in rows),
                   "min": min(r[k] for r in rows), "max": max(r[k] for r in rows)}
               for k in keys if rows[0][k] is not None}
    n = 5000
    out = {
        "seeds": [SEEDS.start, SEEDS.stop - 1],
        "beta": 0.0,
        "same_split_on_every_seed": same_split,
        "summary": summary,
        "never_lent_to_effect_points": 100 * (summary["never_default_on"]["mean"] - summary["never_default_off"]["mean"]) / n,
        "lent_to_effect_points": 100 * (summary["lent_to_default_on"]["mean"] - summary["lent_to_default_off"]["mean"]) / n,
        "per_seed": [{k: v for k, v in r.items() if k != "lent_set"} for r in rows],
    }
    path = ROOT / "results" / "summary" / "short_group_lending.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "per_seed"}, indent=1))


if __name__ == "__main__":
    main()
