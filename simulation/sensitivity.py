"""Global sensitivity analysis (Sobol variance decomposition).

The sweeps in `experiments.py` are one-factor-at-a-time around the baseline. OFAT tells
you whether a result moves when one knob moves; it cannot tell you how the model's output
variance is APPORTIONED across the uncalibrated parameters, and it misses interactions
entirely. For a model carrying three admittedly uncalibrated parameters plus a fitted
shock rate known to sit above observed labour-market flows, that gap matters.

Sobol indices close it:
  * S1 (first order)  - variance explained by a parameter on its own.
  * ST (total order)  - including every interaction it takes part in.
  * ST - S1 large     - the parameter matters mainly THROUGH interactions.

Usage:
    python -m simulation.sensitivity --samples 128
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from SALib.analyze import sobol as sobol_analyze
from SALib.sample import sobol as sobol_sample

from .batch import run_batch
from .config import RESULTS_SUMMARY, ParamSet

#: The uncalibrated and fitted parameters, with the ranges each is defensible over.
#: `beta` and `q_base` are the two admitted uncalibratable parameters (issues.md B8);
#: min_payment_frac is the model's second uncited rule (B15); bnpl_platform_limit is
#: unsourceable (B16); bnpl_purchase_mean rests on trade press; shock_prob is fitted but
#: sits 4x above the QLFS band (B20), so its uncertainty belongs here too.
PROBLEM = {
    "num_vars": 6,
    "names": [
        "q_base",
        "beta",
        "min_payment_frac",
        "bnpl_purchase_mean",
        "bnpl_platform_limit",
        "shock_prob",
    ],
    "bounds": [
        [0.01, 0.30],      # spontaneous want-driven BNPL propensity
        [0.0, 3.0],        # peer imitation strength; 0 is the control arm
        [0.025, 0.10],     # contractual minimum payment (mandatory sweep)
        [800.0, 3200.0],   # ~0.5x to 2x the SA average basket of R1,568
        [1000.0, 20000.0], # rolling limit; no published figure exists
        [0.012, 0.064],    # shock probability, bracketing the fitted 0.048
    ],
}

#: Outputs to decompose. The first is the thesis headline.
OUTPUTS = [
    "default_rate_final",
    "active_90_plus_mean",
    "bnpl_adoption_final",
    "stacking_mean_final",
    "trad_arrears_rate_mean",
]


def build_param_sets(sample: np.ndarray, reps: int, base: ParamSet) -> list[ParamSet]:
    sets: list[ParamSet] = []
    for i, row in enumerate(sample):
        kwargs = dict(zip(PROBLEM["names"], (float(v) for v in row)))
        kwargs["min_payment_frac"] = float(kwargs["min_payment_frac"])
        for r in range(reps):
            sets.append(base.replace(seed=100_000 + i * reps + r, label=f"sobol_{i}", **kwargs))
    return sets


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--samples",
        type=int,
        default=128,
        help="Saltelli base sample size (power of 2). Total runs = N*(2D+2)*reps.",
    )
    ap.add_argument("--reps", type=int, default=2, help="replicates per design point")
    ap.add_argument("--jobs", type=int, default=-2)
    ap.add_argument("--ticks", type=int, default=52)
    args = ap.parse_args()

    sample = sobol_sample.sample(PROBLEM, args.samples, calc_second_order=False)
    n_design = len(sample)
    print(f"Sobol design points : {n_design}  (N={args.samples}, D={PROBLEM['num_vars']})")
    print(f"replicates          : {args.reps}")
    print(f"total runs          : {n_design * args.reps}")

    base = ParamSet(bnpl_enabled=True, n_ticks=args.ticks)
    param_sets = build_param_sets(sample, args.reps, base)
    df = run_batch(param_sets, n_jobs=args.jobs)

    # Average replicates within each design point so Sobol sees the expected response
    # rather than the seed noise, which is not part of the parameter variance.
    df["design"] = [i for i in range(n_design) for _ in range(args.reps)]
    agg = df.groupby("design")[OUTPUTS].mean().reindex(range(n_design))

    results = {}
    print()
    for out in OUTPUTS:
        y = agg[out].to_numpy(dtype=float)
        if not np.isfinite(y).all() or np.allclose(y, y[0]):
            print(f"--- {out}: constant or non-finite, skipped")
            continue
        si = sobol_analyze.analyze(PROBLEM, y, calc_second_order=False, print_to_console=False)
        table = pd.DataFrame(
            {
                "parameter": PROBLEM["names"],
                "S1": si["S1"],
                "S1_conf": si["S1_conf"],
                "ST": si["ST"],
                "ST_conf": si["ST_conf"],
            }
        ).sort_values("ST", ascending=False)
        table["interaction"] = table["ST"] - table["S1"]
        print(f"--- {out}")
        print(table.to_string(index=False, float_format=lambda v: f"{v:7.4f}"))
        print()
        results[out] = table.to_dict(orient="records")

    RESULTS_SUMMARY.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RESULTS_SUMMARY / "sobol_runs.parquet", index=False)
    (RESULTS_SUMMARY / "sobol_indices.json").write_text(
        json.dumps(
            {
                "problem": PROBLEM,
                "n_base_samples": args.samples,
                "n_design_points": n_design,
                "replicates": args.reps,
                "indices": results,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"wrote {RESULTS_SUMMARY / 'sobol_indices.json'}")


if __name__ == "__main__":
    main()
