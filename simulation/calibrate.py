"""Calibrate the income-shock probability `p` against the 2017-Q1 CCMR.

D1 makes `p` a calibration target rather than a sourced parameter, which is what makes
the baseline CALIBRATED rather than validated: only the BNPL-on results are genuine
predictions. That has to be stated in the limitations chapter, not buried here.

The fit is to the 90+ band at k=7. The other two bands are reported as UNFITTED
diagnostics, as are patterns 3 and 4, so the checkpoint distinguishes what was fitted
from what was merely observed.

The fitted value is then compared to the QLFS 2017 job-separation band. That comparison
is a plausibility check on the calibration, NOT a second objective: fitting to both would
over-determine the baseline.

Usage:
    python -m simulation.calibrate --reps 20
"""

from __future__ import annotations

import argparse
import json
import statistics as st

import pandas as pd

from .batch import replicate, run_batch
from .config import (
    RESULTS_SUMMARY,
    ParamSet,
    load_ccmr_target,
    load_qlfs_band,
)

#: The band the fit targets. Credit-active denominator: the CCMR counts accounts held by
#: credit-active consumers, and 56% of this population holds no traditional debt at all.
OBJECTIVE_COLUMN = "active_90_plus_mean"


def baseline(**overrides) -> ParamSet:
    """The no-BNPL 2017 baseline. BNPL is off by construction (the injection design)."""
    return ParamSet(bnpl_enabled=False, **overrides)


def evaluate(
    p_grid: list[float],
    reps: int,
    n_jobs: int = -2,
    friction_grid: list[float] | None = None,
) -> pd.DataFrame:
    """Grid over the shock probability and, optionally, the payment-friction rate.

    Two parameters against two DIFFERENT bands: `p` drives the 90+ tail through
    unemployment spells, friction drives the 1-30 band through missed-but-affordable
    instalments. They are near-orthogonal, which is what makes the pair identifiable
    rather than over-determined; the 31-60 and 61-90 bands stay unfitted.
    """
    runs: list[ParamSet] = []
    for p in p_grid:
        for f in friction_grid or [0.0]:
            runs.extend(
                replicate(
                    baseline(shock_prob=p, payment_friction=f, label=f"p={p:.4f},f={f:.3f}"),
                    reps,
                    seed0=1000,
                )
            )
    return run_batch(runs, n_jobs=n_jobs)


def summarise(df: pd.DataFrame, target: float, by: list[str] | None = None) -> pd.DataFrame:
    g = df.groupby(by or ["shock_prob"], as_index=False).agg(
        objective_mean=(OBJECTIVE_COLUMN, "mean"),
        objective_sd=(OBJECTIVE_COLUMN, "std"),
        active_60_plus=("active_60_plus_mean", "mean"),
        active_current=("active_current_mean", "mean"),
        active_d30=("active_d30_mean", "mean"),
        active_d31_60=("active_d31_60_mean", "mean"),
        active_d61_90=("active_d61_90_mean", "mean"),
        all_90_plus=("pct_90_plus_mean", "mean"),
        default_rate=("default_rate_mean", "mean"),
        zero_savings=("zero_savings_rate_mean", "mean"),
        shocked_rate=("shocked_rate_mean", "mean"),
        n_runs=("seed", "count"),
    )
    g["abs_error"] = (g["objective_mean"] - target).abs()
    return g.sort_values(by or ["shock_prob"]).reset_index(drop=True)


def refine(coarse: pd.DataFrame, width_frac: float = 0.6, n: int = 7) -> list[float]:
    """A finer grid bracketing the best coarse point."""
    best = float(coarse.loc[coarse["abs_error"].idxmin(), "shock_prob"])
    lo, hi = best * (1 - width_frac), best * (1 + width_frac)
    step = (hi - lo) / (n - 1)
    return [round(lo + i * step, 5) for i in range(n)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reps", type=int, default=20, help="replicates per grid point")
    ap.add_argument("--jobs", type=int, default=-2, help="joblib n_jobs")
    ap.add_argument("--quick", action="store_true", help="coarse grid only")
    args = ap.parse_args()

    ccmr = load_ccmr_target()
    qlfs = load_qlfs_band()
    target = ccmr["pct_90_plus"] / 100.0

    print("=" * 78)
    print("CALIBRATION OF THE INCOME-SHOCK PROBABILITY p  (D1)")
    print("=" * 78)
    print(f"target        : CCMR 2017-Q1 90+ = {target:.2%} (account basis)")
    print(f"objective     : {OBJECTIVE_COLUMN} (credit-active denominator)")
    print(f"replicates    : {args.reps} per grid point")
    print()

    d30_target = ccmr["pct_d30"] / 100.0 if "pct_d30" in ccmr else 0.0824

    # --- stage 1: fit p to the 90+ tail with friction off ---------------------
    coarse_grid = [0.016, 0.024, 0.032, 0.040, 0.048, 0.056, 0.064]
    print(f"--- stage 1, p grid (friction off): {coarse_grid}")
    df = evaluate(coarse_grid, args.reps, args.jobs)
    coarse = summarise(df, target)
    print(
        coarse[
            ["shock_prob", "objective_mean", "active_d30", "active_current", "abs_error"]
        ].to_string(index=False, float_format=lambda v: f"{v:.4f}")
    )
    p_hat = float(coarse.loc[coarse["abs_error"].idxmin(), "shock_prob"])
    print(f"    -> p = {p_hat:.4f}")

    # --- stage 2: fit friction to the 1-30 band, holding p ---------------------
    friction_grid = [0.0, 0.02, 0.04, 0.06, 0.09, 0.12, 0.16]
    print(f"\n--- stage 2, friction grid at p={p_hat:.4f}: {friction_grid}")
    df2 = evaluate([p_hat], args.reps, args.jobs, friction_grid=friction_grid)
    fr = summarise(df2, target, by=["payment_friction"])
    fr["d30_error"] = (fr["active_d30"] - d30_target).abs()
    print(
        fr[
            ["payment_friction", "active_d30", "objective_mean", "active_current", "d30_error"]
        ].to_string(index=False, float_format=lambda v: f"{v:.4f}")
    )
    f_hat = float(fr.loc[fr["d30_error"].idxmin(), "payment_friction"])
    print(f"    -> friction = {f_hat:.4f}  (1-30 target {d30_target:.2%})")

    # --- stage 3: re-fit p with friction on (they are not perfectly orthogonal) -
    print(f"\n--- stage 3, re-fit p at friction={f_hat:.4f}")
    df3 = evaluate(coarse_grid, args.reps, args.jobs, friction_grid=[f_hat])
    final_tbl = summarise(df3, target)
    print(
        final_tbl[
            ["shock_prob", "objective_mean", "active_d30", "active_current", "abs_error"]
        ].to_string(index=False, float_format=lambda v: f"{v:.4f}")
    )

    all_runs = pd.concat([df, df2, df3], ignore_index=True)
    best_table = final_tbl
    best_row = best_table.loc[best_table["abs_error"].idxmin()]
    p_hat = float(best_row["shock_prob"])

    # --- the QLFS plausibility check ------------------------------------------
    lo, hi = qlfs["p_tick_lower"], qlfs["p_tick_upper"]
    inside = lo <= p_hat <= hi

    print()
    print("=" * 78)
    print("RESULT")
    print("=" * 78)
    print(f"fitted p                     : {p_hat:.5f} per tick   [FITTED to 90+]")
    print(f"fitted payment friction      : {f_hat:.5f} per tick   [FITTED to 1-30]")
    print()
    print(f"  90+  (credit-active)       : {best_row['objective_mean']:.2%}  "
          f"target {target:.2%}   [FITTED]")
    print(f"  1-30 (credit-active)       : {best_row['active_d30']:.2%}  "
          f"target {d30_target:.2%}   [FITTED]")
    print(f"  31-60 (credit-active)      : {best_row['active_d31_60']:.2%}  "
          f"CCMR 3.59%   [UNFITTED]")
    print(f"  61-90 (credit-active)      : {best_row['active_d61_90']:.2%}  "
          f"CCMR 2.32%   [UNFITTED]")
    print(f"  current (credit-active)    : {best_row['active_current']:.2%}  "
          f"CCMR {ccmr['pct_current']:.2f}%   [UNFITTED]")
    print(f"  60+  (credit-active)       : {best_row['active_60_plus']:.2%}  "
          f"CCMR {ccmr['pct_60_plus']:.2f}%   [UNFITTED]")
    print(f"  90+  (all households)      : {best_row['all_90_plus']:.2%}   [different denominator]")
    print(f"  population default rate    : {best_row['default_rate']:.2%}")
    print()
    print(f"QLFS 2017 job-separation band: {lo:.5f} to {hi:.5f} per tick")
    print(f"  fitted p inside the band?  : {'YES' if inside else 'NO'}"
          f"  (ratio to upper bound {p_hat / hi:.2f}x)")
    print("  NOTE: this comparison is now LIKE-FOR-LIKE. Since the shock hazard applies")
    print("  per EARNER (each employed member separates independently), `p` is an")
    print("  individual separation rate, directly comparable to the QLFS individual")
    print("  transition rate. The earlier household-vs-individual caveat no longer")
    print("  applies and cannot be used to explain away the gap.")

    RESULTS_SUMMARY.mkdir(parents=True, exist_ok=True)
    all_runs.to_parquet(RESULTS_SUMMARY / "calibration_runs.parquet", index=False)
    best_table.to_csv(RESULTS_SUMMARY / "calibration_grid.csv", index=False)
    payload = {
        "fitted_shock_prob": p_hat,
        "fitted_payment_friction": f_hat,
        "objective_column": OBJECTIVE_COLUMN,
        "objective_value": float(best_row["objective_mean"]),
        "objective_sd": float(best_row["objective_sd"]),
        "target_90_plus": target,
        "target_d30": d30_target,
        "fitted_d30": float(best_row["active_d30"]),
        "unfitted": {
            "active_d31_60": float(best_row["active_d31_60"]),
            "active_d61_90": float(best_row["active_d61_90"]),
            "active_60_plus": float(best_row["active_60_plus"]),
            "active_current": float(best_row["active_current"]),
            "all_households_90_plus": float(best_row["all_90_plus"]),
            "default_rate": float(best_row["default_rate"]),
            "zero_savings_rate": float(best_row["zero_savings"]),
        },
        "qlfs_band": {"lower": lo, "upper": hi, "fitted_inside": bool(inside)},
        "replicates": args.reps,
    }
    (RESULTS_SUMMARY / "calibration.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print(f"\nwrote {RESULTS_SUMMARY / 'calibration.json'}")


if __name__ == "__main__":
    main()
