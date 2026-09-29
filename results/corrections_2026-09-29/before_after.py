"""Headline results before and after the corrections.

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/before_after.py

Reads the preserved outputs (results/superseded_2026-09-29_pre-correction/raw) and the
corrected outputs (results/raw). Differences between arms that share seeds are paired by
seed; others are unpaired. One standard error throughout.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / "results" / "superseded_2026-09-29_pre-correction" / "raw"
NEW = ROOT / "results" / "raw"


def arm(df, label):
    out = df[df.label == label]
    assert len(out) == 20, (label, len(out))
    return out


def d(a, b, col="default_rate_final", scale=100.0):
    if set(a.seed) == set(b.seed) and set(a.n_agents) == set(b.n_agents):
        z = (a.set_index("seed")[col] - b.set_index("seed")[col]) * scale
        return z.mean(), z.std(ddof=1) / math.sqrt(len(z)), "paired"
    m = (a[col].mean() - b[col].mean()) * scale
    se = math.sqrt(a[col].var(ddof=1) / len(a) + b[col].var(ddof=1) / len(b)) * scale
    return m, se, "unpaired"


def f(x):
    star = "*" if abs(x[0]) > 2 * x[1] else ""
    return f"{x[0]:+.2f} ± {x[1]:.2f}{star}"


def level(a, col="default_rate_final", scale=100.0, dp=2):
    return f"{a[col].mean() * scale:.{dp}f}"


rows = []


def add(name, fn):
    out = []
    for raw in (OLD, NEW):
        try:
            out.append(fn(lambda n: pd.read_parquet(raw / f"{n}.parquet")))
        except (AssertionError, KeyError, FileNotFoundError):
            out.append("not run")
    rows.append((name, *out))


add("Baseline default, no BNPL (%)", lambda L: level(arm(L("rq0"), "baseline_no_bnpl")))
add("Baseline 90+ arrears, credit-active (%); target 14.21", lambda L: level(arm(L("rq0"), "baseline_no_bnpl"), "active_90_plus_mean"))
add("Baseline 1-30 day arrears (%); target 8.24", lambda L: level(arm(L("rq0"), "baseline_no_bnpl"), "active_d30_mean"))
add("Baseline 31-60 day arrears (%); CCMR 3.59", lambda L: level(arm(L("rq0"), "baseline_no_bnpl"), "active_d31_60_mean"))
add("Baseline 61-90 day arrears (%); CCMR 2.32", lambda L: level(arm(L("rq0"), "baseline_no_bnpl"), "active_d61_90_mean"))
add("BNPL effect on default, beta=0 (pp)", lambda L: f(d(arm(L("rq0"), "bnpl_on_beta0"), arm(L("rq0"), "baseline_no_bnpl"))))
add("BNPL effect on default, beta=1 (pp)", lambda L: f(d(arm(L("rq0"), "bnpl_on_beta1"), arm(L("rq0"), "baseline_no_bnpl"))))
add("BNPL effect on traditional arrears rate, beta=0 (pp)", lambda L: f(d(arm(L("rq0"), "bnpl_on_beta0"), arm(L("rq0"), "baseline_no_bnpl"), "trad_arrears_rate_mean")))
add("BNPL effect on traditional arrears rate, beta=1 (pp)", lambda L: f(d(arm(L("rq0"), "bnpl_on_beta1"), arm(L("rq0"), "baseline_no_bnpl"), "trad_arrears_rate_mean")))
add("BNPL effect on traditional interest, beta=0 (R m)", lambda L: f(d(arm(L("rq0"), "bnpl_on_beta0"), arm(L("rq0"), "baseline_no_bnpl"), "trad_interest_total", 1e-6)))
add("New traditional lending, no BNPL / beta=0 (R m)", lambda L: level(arm(L("rq0"), "baseline_no_bnpl"), "trad_granted_value", 1e-6) + " / " + level(arm(L("rq0"), "bnpl_on_beta0"), "trad_granted_value", 1e-6))
add("BNPL volume, beta=0 / beta=1 (R m)", lambda L: level(arm(L("rq0"), "bnpl_on_beta0"), "bnpl_volume_cumulative", 1e-6) + " / " + level(arm(L("rq0"), "bnpl_on_beta1"), "bnpl_volume_cumulative", 1e-6))
add("Holding BNPL at final tick, beta=0 / beta=1 (%)", lambda L: level(arm(L("rq0"), "bnpl_on_beta0"), "bnpl_adoption_final") + " / " + level(arm(L("rq0"), "bnpl_on_beta1"), "bnpl_adoption_final"))
add("Holders on 2+ platforms, final tick, beta=0 / beta=1 (%)", lambda L: "{:.1f} / {:.1f}".format(
    *(100 * (arm(L("rq0"), l).stacking_2plus_final / arm(L("rq0"), l).bnpl_adoption_final).mean() for l in ("bnpl_on_beta0", "bnpl_on_beta1"))))
add("Ever on 2+ platforms, of ever-adopters, beta=0 / beta=1 (%)", lambda L: level(arm(L("rq0"), "bnpl_on_beta0"), "ever_stacked_2plus_of_adopters", dp=1) + " / " + level(arm(L("rq0"), "bnpl_on_beta1"), "ever_stacked_2plus_of_adopters", dp=1))
add("Mean want-driven purchase, beta=0 (R); band 645-1339", lambda L: level(arm(L("rq0"), "bnpl_on_beta0"), "bnpl_purchase_mean_realised", 1.0))
for b in (0.0, 1.0, 2.0, 3.0):
    add(f"Default, six platforms less one, beta={b:g} (pp)", lambda L, b=b: f(d(arm(L("rq1"), f"rq1_n6_b{b}"), arm(L("rq1"), f"rq1_n1_b{b}"))))
for b in (0.0, 1.0, 3.0):
    add(f"Default, full access less none, beta={b:g} (pp)", lambda L, b=b: f(d(arm(L("rq2"), f"rq2_a1.0_b{b}"), arm(L("rq2"), f"rq2_a0.0_b{b}"))))
for key, name in (("bureau", "Bureau visibility"), ("afford", "Screening"), ("both", "Both switches"), ("cap1", "Cap of one platform"), ("cap2", "Cap of two platforms"), ("cap3", "Cap of three platforms"), ("kcool1", "Cooling-off, one tick"), ("kcool4", "Cooling-off, four ticks")):
    for b in (0.0, 1.0):
        add(f"{name} less benchmark, default, beta={b:g} (pp)", lambda L, key=key, b=b: f(d(arm(L("rq3"), f"rq3_{key}_b{b}"), arm(L("rq3"), f"rq3_kcool0_b{b}"))))
for key, name in (("amount125", "shortfall +25%"), ("amountcommitted", "shortfall + committed"), ("uncapped", "BNPL share uncapped"), ("shock_single_tick", "single-tick shock")):
    off = "ref" if key == "uncapped" else key
    add(f"BNPL effect under {name}, beta=0 (pp)", lambda L, key=key, off=off: f(d(arm(L("effect"), f"eff_{key}_b0.0"), arm(L("effect"), f"eff_{off}_off"))))
add("BNPL effect, shortfall path only, beta=0 (pp)", lambda L: f(d(arm(L("effect"), "eff_want_off_b0.0"), arm(L("effect"), "eff_ref_off"))))
add("BNPL effect, checkout quarter not requested, beta=0 (pp)", lambda L: f(d(arm(L("effect"), "eff_checkout_unfunded_b0.0"), arm(L("effect"), "eff_ref_off"))))
add("BNPL effect, checkout quarter not requested, beta=1 (pp)", lambda L: f(d(arm(L("effect"), "eff_checkout_unfunded_b1.0"), arm(L("effect"), "eff_ref_off"))))
add("Sensitivity: shortfall + committed less exact, default at beta=1 (pp)", lambda L: f(d(arm(L("robustness"), "rob_amount_shortfall_plus_committed"), arm(L("robustness"), "rob_amount_shortfall"))))
add("Sensitivity: default horizon 56 days less 98, beta=1 (pp)", lambda L: f(d(arm(L("robustness"), "rob_k4"), arm(L("robustness"), "rob_k7"))))
add("Sensitivity: single-tick shock, default at beta=1 (%)", lambda L: level(arm(L("robustness"), "rob_shock_single_tick")))

out = pd.DataFrame(rows, columns=["Result", "Before", "After"]).set_index("Result")
text = out.to_markdown()
print(text)
if "--write" in sys.argv:
    (Path(__file__).parent / "BEFORE_AFTER.md").write_text(
        "# Headline results before and after the corrections\n\n"
        "Before: code at tag `pre-correction-2026-09-29`, outputs preserved in "
        "`results/superseded_2026-09-29_pre-correction/raw`. After: corrected code, outputs in "
        "`results/raw`. Both use shock probability 0.016 and payment friction 0.09, which the "
        "recalibration confirmed. Twenty replicates per arm. Differences carry one standard error, "
        "paired by seed where the two arms share seeds and unpaired otherwise. An asterisk marks a "
        "difference beyond two standard errors.\n\n" + text + "\n"
    )
