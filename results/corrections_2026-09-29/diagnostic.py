"""Diagnostic comparison at FIXED parameters, run once after each correction.

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/diagnostic.py <step-label>

Eight arms on ONE seed block (10,000-10,019) at the original fitted values (shock
probability 0.016, payment friction 0.09), so that a change between two steps is the
effect of the code correction alone and not of recalibration. Output:
results/corrections_2026-09-29/diagnostic/<step-label>.parquet
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from simulation.batch import replicate, run_batch
from simulation.config import ParamSet

HERE = Path(__file__).resolve().parent
P, F = 0.016, 0.09


def arm(**kw) -> ParamSet:
    return ParamSet(shock_prob=P, payment_friction=F, **kw)


ARMS = [
    arm(bnpl_enabled=False, label="no_bnpl"),
    arm(bnpl_enabled=True, beta=0.0, label="bnpl_b0"),
    arm(bnpl_enabled=True, beta=1.0, label="bnpl_b1"),
    arm(bnpl_enabled=True, beta=0.0, q_base=0.0, label="bnpl_shortfall_only"),
    arm(bnpl_enabled=True, beta=0.0, bnpl_bureau_visible=True, label="bureau_b0"),
    arm(bnpl_enabled=True, beta=0.0, bnpl_affordability_check=True, label="screening_b0"),
    arm(bnpl_enabled=True, beta=0.0, stacking_cap=1, label="cap1_b0"),
    arm(bnpl_enabled=True, beta=0.0, stacking_cap=2, label="cap2_b0"),
]

if __name__ == "__main__":
    step = sys.argv[1]
    runs = [p for a in ARMS for p in replicate(a, 20, seed0=10_000)]
    df = run_batch(runs, n_jobs=14, verbose=0)
    df["step"] = step
    df["commit"] = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    out = HERE / "diagnostic" / f"{step}.parquet"
    out.parent.mkdir(exist_ok=True)
    df.to_parquet(out, index=False)
    cols = ["default_rate_final", "active_90_plus_mean", "active_d30_mean", "trad_granted_value",
            "bnpl_volume_cumulative", "n_credit_active_final"]
    print(df.groupby("label", sort=False)[cols].mean().round(4).to_string())
