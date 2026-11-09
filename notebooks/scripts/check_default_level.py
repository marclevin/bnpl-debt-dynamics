"""Is the default level plausible? Default against the CCMR and NCR CBM benchmarks (B48).

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_default_level.py

Reruns the rq0 baseline and beta = 0 arms (seeds 10,000-10,019), checks each run against
results/raw/rq0.parquet, and records per-tick flows the summary does not keep:
  * the default hazard per tick among credit-active households, against the CCMR inflow
    into 91+ days implied by the 91-120 band (1.76% of accounts per 30 days);
  * the share of ever-credit-active households with a default by the end, against the NCR
    CBM share of credit-active consumers with impaired records (39.3%, March 2017);
  * the share of credit-active households 91+ days behind at the final tick, against the
    CBM's 21.7% three or more months in arrears.
Writes results/summary/default_level.json.
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from simulation import experiments as ex
from simulation.config import load_ccmr_bands

warnings.simplefilter("ignore")
TICK_DAYS = 14


def one(p):
    from simulation.model import BNPLModel
    from simulation.metrics import summarise_run

    m = BNPLModel(p)
    rule = p.distress_rule == "arrears"

    def active(a):
        if a.d_trad > 0 or a.arrears_trad > 0:
            return True
        return rule and any(pl.loans.get(a.agent_id) for pl in m.platforms)

    agents = list(m.agents)
    ever = {a.agent_id for a in agents if active(a)}
    start_active = len(ever)
    prev_def = {a.agent_id for a in agents if a.defaulted}
    hazards, inflows, active_counts = [], [], []
    for _ in range(p.n_ticks):
        act = {a.agent_id for a in agents if active(a)}
        m.step()
        now_def = {a.agent_id for a in agents if a.defaulted}
        new = now_def - prev_def
        # hazard over households credit-active at the start of the tick and not yet in default
        at_risk = act - prev_def
        hazards.append(len(new & at_risk) / max(len(at_risk), 1))
        # flow into default relative to the whole credit-active book, the CCMR's unit
        inflows.append(len(new & act) / max(len(act), 1))
        active_counts.append(len(act))
        ever |= {a.agent_id for a in agents if active(a)}
        prev_def = now_def
    s = summarise_run(m)
    n = len(agents)
    defaulted = {a.agent_id for a in agents if a.defaulted}
    post = slice(p.burn_in, p.n_ticks)
    return dict(
        label=p.label, seed=p.seed, default_rate_final=s["default_rate_final"],
        new_default_rate_final=s["new_default_rate_final"],
        initial_default_rate=s["initial_default_rate"],
        start_active_share=start_active / n, ever_active_share=len(ever) / n,
        defaulted_of_ever_active=len(defaulted & ever) / len(ever),
        hazard_per_tick_post=float(np.mean(hazards[post])),
        inflow_per_tick_of_book=float(np.mean(inflows[post])),
        active_90_plus_final=s["active_90_plus_final"],
        n_new_defaults=len(defaulted) - m.n_initial_defaults,
        mean_active_post=float(np.mean(active_counts[post])),
        n_ticks=p.n_ticks, burn_in=p.burn_in,
    )


if __name__ == "__main__":
    ps = [p for p in ex.rq0_baseline(20) if p.label in ("baseline_no_bnpl", "bnpl_on_beta0")]
    df = pd.DataFrame(Parallel(n_jobs=-2)(delayed(one)(p) for p in ps))
    raw = pd.read_parquet("results/raw/rq0.parquet")
    chk = df.merge(raw[["label", "seed", "default_rate_final"]], on=["label", "seed"], suffixes=("", "_raw"))
    assert len(chk) == len(df) and (abs(chk.default_rate_final - chk.default_rate_final_raw) < 1e-12).all()
    b = load_ccmr_bands()
    ccmr_inflow_per_tick = b["d91_120"] / 100 * TICK_DAYS / 30
    years = (df.n_ticks.iloc[0]) * TICK_DAYS / 365
    out = {"_note": __doc__.split("\n\n")[0], "n_runs_checked_against_raw": len(chk),
           "ccmr_inflow_91plus_per_tick_of_accounts": ccmr_inflow_per_tick,
           "ccmr_inflow_91plus_per_year_of_accounts": 1 - (1 - ccmr_inflow_per_tick) ** (365 / TICK_DAYS),
           "cbm_impaired_share_credit_active": 0.393, "cbm_3plus_months_share": 0.217,
           "run_years": years}
    for lab, g in df.groupby("label"):
        tag = "off" if lab == "baseline_no_bnpl" else "beta0"
        for c in ["default_rate_final", "new_default_rate_final", "initial_default_rate",
                  "start_active_share", "ever_active_share", "defaulted_of_ever_active",
                  "hazard_per_tick_post", "inflow_per_tick_of_book", "active_90_plus_final", "mean_active_post"]:
            out[f"{tag}_{c}"] = float(g[c].mean())
        h = float(g.hazard_per_tick_post.mean())
        out[f"{tag}_hazard_per_year_post"] = 1 - (1 - h) ** (365 / TICK_DAYS)
        out[f"{tag}_new_defaults_per_year_of_all_households"] = float(g.new_default_rate_final.mean()) / years
    Path("results/summary/default_level.json").write_text(json.dumps(out, indent=2))
    for k, v in out.items():
        print(k, round(v, 4) if isinstance(v, float) else v)
