"""QA 2026-11-10 (B47): describe the households whose surveyed income is below food and rent.

The group is `income_tick < committed_tick`: NIDS W5 derived monthly household income
(`w5_hhincome`, with imputations) below monthly food plus rent paid (`w5_expf + w5_rentexpend`).
This script reads the population file, the NIDS household-derived file and
results/summary/defaulter_credit.json, and builds the model at tick 0 only (no tick is run) on
the rq0 seeds to count group members placed in default at the start. It writes
results/summary/short_group.json, the source of the Section 3.5 numbers:

- the group's size and the number of NIDS households it is drawn from;
- its make-up (quintile, renting, no employed member, no liquid savings, traditional debt);
- how many start in default (all members holding traditional debt, on every rq0 seed);
- default during the run as a share of all members and of those not in default at the start;
- the household one-shot income question (`w5_hhq_incb`): for how many respondents it covers
  food and rent.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_short_group.py
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import pandas as pd

warnings.simplefilter("ignore")
from simulation.experiments import calibrated  # noqa: E402
from simulation.population import load_population_frame  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "results" / "summary"
SEEDS = range(10_000, 10_020)  # rq0 seeds, as in defaulter_credit.json


def start_in_default(seed: int) -> tuple[int, int, int]:
    """(group members, of them in default at tick 0, of those holding traditional debt)."""
    from simulation.model import BNPLModel

    m = BNPLModel(calibrated(bnpl_enabled=False, label="short_group").replace(seed=seed))
    grp = [a for a in m.agents if a.income_tick < a.committed_tick]
    with_debt = [a for a in grp if a.rec.d_trad > 0]
    return len(grp), sum(bool(a.defaulted) for a in grp), sum(bool(a.defaulted) for a in with_debt)


def main() -> None:
    pop = load_population_frame()
    g = pop.w5_hhincome < pop.expenditure_committed
    G = pop[g]
    hh = pd.read_csv(ROOT / "data" / "raw" / "NIDS_W5" / "hhderived.csv", low_memory=False,
                     usecols=["w5_hhid", "w5_hhq_incb", "w5_rentexpend"])
    one = G.merge(hh, left_on="source_w5_hhid", right_on="w5_hhid", how="left")
    answered = one.w5_hhq_incb.notna()
    covers = (one.w5_hhq_incb >= one.expenditure_committed) & answered

    starts = [start_in_default(s) for s in SEEDS]
    n = int(g.sum())
    n_debt = int((G.D_trad > 0).sum())
    assert all(s[0] == n for s in starts), "group size differs from the population file"
    assert all(s[1] == s[2] == n_debt for s in starts), \
        "not every group member with traditional debt starts in default on every seed"
    at_risk = n - n_debt

    dc = json.loads((SUMMARY / "defaulter_credit.json").read_text())
    out = {
        "n_agents": n,
        "share_of_agents": n / len(pop),
        "n_source_households": int(G.source_w5_hhid.nunique()),
        "share_q1": float((G.income_quintile == "Q1").mean()),
        "share_paying_rent": float((one.w5_rentexpend.fillna(0) > 0).mean()),
        "share_no_employed_member": float((G.n_earners == 0).mean()),
        "share_no_liquid_savings": float((G.liquid_savings <= 0).mean()),
        "n_with_traditional_debt": n_debt,
        "n_in_default_at_start_every_seed": n_debt,
        "n_at_risk": at_risk,
        "seeds": [min(SEEDS), max(SEEDS)],
        "zero_or_missing_income": int((G.w5_hhincome.isna() | (G.w5_hhincome <= 0)).sum()),
        "one_shot_answered": int(answered.sum()),
        "one_shot_covers_food_rent": int(covers.sum()),
        "one_shot_covers_share_of_answered": float(covers.sum() / answered.sum()),
    }
    for arm, key in (("no BNPL", "no_bnpl"), ("BNPL beta=0", "bnpl_beta0")):
        share_all = dc[arm]["income_below_committed_who_default"]
        out[f"default_during_run_{key}_of_all"] = share_all
        # The starting defaulters cannot default again, so the same count over those at risk.
        out[f"default_during_run_{key}_of_at_risk"] = share_all * n / at_risk
    (SUMMARY / "short_group.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
