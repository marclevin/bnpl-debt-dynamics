"""Calibrate the baseline against the 2017-Q1 CCMR.

Revised 2026-10-12: the separation rate `p` is now DERIVED from the stable-employment
condition (labour flows on) and only payment friction is fitted, to the 1-30 band. The
90+ band is reported unfitted. The earlier text below describes the superseded fit.


D1 makes `p` a calibration target rather than a sourced parameter, which is what makes
the baseline CALIBRATED rather than validated: only the BNPL-on results are genuine
predictions. That has to be stated in the limitations chapter, not buried here.

The fit is to the 90+ band at k=7. The other two bands are reported as UNFITTED
diagnostics, as are patterns 3 and 4, so the checkpoint distinguishes what was fitted
from what was merely observed.

A last stage reruns the fitted band on a grid of 0.001 either side of the selected value.
It is a check on the coarse grid and does not change the selection.

The fitted value is then compared to the QLFS 2017 job-separation band. That comparison
is a plausibility check on the calibration, NOT a second objective: fitting to both would
over-determine the baseline.

Usage:
    python -m simulation.calibrate --reps 20
"""

from __future__ import annotations

import argparse
import json

import pandas as pd

from .batch import replicate, run_batch
from .population import stationary_separation_rate
from .config import (
    RESULTS_SUMMARY,
    ParamSet,
    load_ccmr_bands,
    load_ccmr_target,
    load_qlfs_band,
)

#: The band the fit targets. Credit-active denominator: the CCMR counts accounts held by
#: credit-active consumers, and 56% of this population holds no traditional debt at all.
OBJECTIVE_COLUMN = "active_90_plus_mean"

#: Columns printed for the two shock-probability stages.
P_COLS = ["shock_prob", "objective_mean", "active_d30", "active_current", "abs_error"]


def baseline(**overrides) -> ParamSet:
    """The no-BNPL 2017 baseline with labour flows. BNPL is off by construction."""
    return ParamSet(bnpl_enabled=False, labour_flows=True, **overrides)


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


def show(table: pd.DataFrame, cols: list[str]) -> None:
    print(table[cols].to_string(index=False, float_format=lambda v: f"{v:.4f}"))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reps", type=int, default=20, help="replicates per grid point")
    ap.add_argument("--jobs", type=int, default=-2, help="joblib n_jobs")
    args = ap.parse_args()

    ccmr = load_ccmr_target()
    qlfs = load_qlfs_band()
    target = ccmr["pct_90_plus"] / 100.0
    bands = load_ccmr_bands()
    d30_target = bands["d30"] / 100.0

    # --- the separation rate is DERIVED, not fitted (2026-10-12) ---------------
    # Labour flows on: employed members separate at p, unemployed members (including the
    # strictly unemployed on the NIDS roster) find work at the QLFS rate. p is the value
    # at which expected employment is constant, as in the stable 2017 labour market.
    exit_prob = ParamSet().shock_exit_prob
    p = round(stationary_separation_rate(exit_prob), 5)
    print("=" * 78)
    print("CALIBRATION (labour flows on)")
    print("=" * 78)
    print(f"separation rate p : {p:.5f} per tick, DERIVED (re-employment {exit_prob:.5f} x "
          "jobseekers / earners)")
    print(f"QLFS 2017 band    : {qlfs['p_tick_lower']:.5f} to {qlfs['p_tick_upper']:.5f} per tick")

    # --- fit friction to the 1-30 band at the derived p -----------------------
    friction_grid = [0.0, 0.02, 0.04, 0.06, 0.08, 0.09, 0.10, 0.12, 0.16]
    print(f"\n--- friction grid at p={p:.5f}: {friction_grid}")
    df = evaluate([p], args.reps, args.jobs, friction_grid=friction_grid)
    fr = summarise(df, target, by=["payment_friction"])
    fr["d30_error"] = (fr["active_d30"] - d30_target).abs()
    show(fr, ["payment_friction", "active_d30", "objective_mean", "active_current", "d30_error"])
    best_row = fr.loc[fr["d30_error"].idxmin()]
    f_hat = float(best_row["payment_friction"])

    print()
    print("=" * 78)
    print("RESULT")
    print("=" * 78)
    print(f"derived p                    : {p:.5f} per tick")
    print(f"fitted payment friction      : {f_hat:.5f} per tick   [FITTED to 1-30]")
    print(f"  1-30 (credit-active)       : {best_row['active_d30']:.2%}  target {d30_target:.2%}   [FITTED]")
    print(f"  90+  (credit-active)       : {best_row['objective_mean']:.2%}  CCMR {target:.2%}   [UNFITTED]")
    print(f"  population default rate    : {best_row['default_rate']:.2%}")

    RESULTS_SUMMARY.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RESULTS_SUMMARY / "calibration_runs.parquet", index=False)
    fr.to_csv(RESULTS_SUMMARY / "calibration_grid.csv", index=False)
    payload = {
        "derived_shock_prob": p,
        "shock_exit_prob": exit_prob,
        "labour_flows": True,
        "fitted_payment_friction": f_hat,
        "objective_column": OBJECTIVE_COLUMN,
        "objective_value": float(best_row["objective_mean"]),
        "objective_sd": float(best_row["objective_sd"]),
        "target_90_plus": target,
        "target_d30": d30_target,
        "fitted_d30": float(best_row["active_d30"]),
        "unfitted": {
            "active_90_plus": float(best_row["objective_mean"]),
            "active_d31_60": float(best_row["active_d31_60"]),
            "active_d61_90": float(best_row["active_d61_90"]),
            "active_60_plus": float(best_row["active_60_plus"]),
            "active_current": float(best_row["active_current"]),
            "all_households_90_plus": float(best_row["all_90_plus"]),
            "default_rate": float(best_row["default_rate"]),
            "zero_savings_rate": float(best_row["zero_savings"]),
        },
        "qlfs_band": {"lower": qlfs["p_tick_lower"], "upper": qlfs["p_tick_upper"]},
        "replicates": args.reps,
        "earlier_fit": {
            "note": "Before 2026-10-12 p was fitted to the 90+ band without labour flows: 0.016.",
            "shock_prob": 0.016,
        },
    }
    (RESULTS_SUMMARY / "calibration.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {RESULTS_SUMMARY / 'calibration.json'}")


if __name__ == "__main__":
    main()
