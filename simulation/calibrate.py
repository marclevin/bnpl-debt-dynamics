"""Calibrate the baseline against the 2017-Q1 CCMR.

Revised 2026-11-09 (D18, issue #93), under the arrears distress rule. The run starts from
the CCMR age profile (`initial_arrears`), defaulted accounts are written off at a rate
DERIVED from the CCMR stock-flow balance, and the separation rate `p` is DERIVED from the
stable-employment condition. Two parameters are FITTED jointly:

  * payment friction, the entry into arrears;
  * arrears persistence, the chance a household already behind pays nothing again.

They are fitted by simulated minimum distance to the five CCMR arrears bands (1-30, 31-60,
61-90, 91-120, 120+): the grid point with the smallest root sum of squared deviations, in
points. Five moments for two parameters, so the fit is over-identified and its band-by-band
error is reported. A first attempt fitted friction to 1-30 and persistence to 31-60 alone;
one persistence parameter cannot reproduce the CCMR's rising roll rates, and every band
above 60 days then fell short (90+ at 9.9%), so all five bands are targeted. UNFITTED: the
90+ share at the final tick against its post-burn-in mean (whether the profile is
stationary), default against the NCR Credit Bureau Monitor, and the BNPL-off patterns of
Section 3.5. Every share is over credit-active households, the closest analogue to the
CCMR's accounts (B5). The fit is with BNPL off.

The earlier calibrations (friction alone to 1-30, 2026-10-12; the shock rate to 90+, before
that) are in calibration history; their outputs are kept in results/summary/pre_arrears_rule.

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
    ARREARS_RULE,
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
    return ParamSet(**{"bnpl_enabled": False, "labour_flows": True, **ARREARS_RULE, **overrides})


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


#: The five target bands and the grid. Persistence sets the shape of the profile; friction
#: sets the level of entry into arrears.
TARGETS = ("d30", "d31_60", "d61_90", "d91_120", "d120_plus")
FRICTION_GRID = [0.05, 0.0525, 0.055, 0.0575, 0.06]
PERSISTENCE_GRID = [0.70, 0.71, 0.72, 0.73, 0.74]
BAND_COLS = ["current", "d30", "d31_60", "d61_90", "d91_120", "d120_plus"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reps", type=int, default=20, help="replicates per grid point")
    ap.add_argument("--jobs", type=int, default=-2, help="joblib n_jobs")
    args = ap.parse_args()

    ccmr = load_ccmr_target()
    qlfs = load_qlfs_band()
    bands = {k: v / 100.0 for k, v in load_ccmr_bands().items()}
    target_90 = ccmr["pct_90_plus"] / 100.0

    exit_prob = ParamSet().shock_exit_prob
    p = round(stationary_separation_rate(exit_prob), 5)
    print("=" * 78)
    print("CALIBRATION (arrears rule, CCMR initial arrears, labour flows)")
    print("=" * 78)
    print(f"separation rate p : {p:.5f} per tick, DERIVED")
    print(f"write-off rate    : {ARREARS_RULE['write_off_rate']:.4f} per tick, DERIVED from the CCMR")

    runs: list[ParamSet] = []
    for f in FRICTION_GRID:
        for pi in PERSISTENCE_GRID:
            runs += replicate(
                baseline(shock_prob=p, payment_friction=f, arrears_persistence=pi,
                         label=f"f={f:.3f},pi={pi:.2f}"),
                args.reps, seed0=1000,
            )
    df = run_batch(runs, n_jobs=args.jobs)
    keys = ["payment_friction", "arrears_persistence"]
    agg = {f"active_{b}": (f"active_{b}_mean", "mean") for b in BAND_COLS}
    agg.update(
        active_90_plus=("active_90_plus_mean", "mean"),
        active_90_plus_sd=("active_90_plus_mean", "std"),
        active_90_plus_final=("active_90_plus_final", "mean"),
        default_rate=("default_rate_final", "mean"),
        new_default_rate=("new_default_rate_final", "mean"),
        initial_default_rate=("initial_default_rate", "mean"),
        consumption_distress=("consumption_distress_mean", "mean"),
        n_credit_active=("n_credit_active_final", "mean"),
        n_runs=("seed", "count"),
    )
    fr = df.groupby(keys, as_index=False).agg(**agg)
    fr["fit_error"] = sum((fr[f"active_{b}"] - bands[b]) ** 2 for b in TARGETS) ** 0.5 * 100
    best = fr.loc[fr["fit_error"].idxmin()]
    f_hat, pi_hat = float(best["payment_friction"]), float(best["arrears_persistence"])
    print(fr.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    print()
    print("=" * 78)
    print("RESULT")
    print("=" * 78)
    print(f"fitted payment friction   : {f_hat:.4f}   [FITTED, five bands]")
    print(f"fitted arrears persistence: {pi_hat:.2f}   [FITTED, five bands]")
    for b in BAND_COLS:
        tag = "FITTED" if b in TARGETS else "UNFITTED"
        print(f"  {b:10s}: {best[f'active_{b}']:.2%}  CCMR {bands[b]:.2%}   [{tag}]")
    print(f"  90+       : {best['active_90_plus']:.2%}  CCMR {target_90:.2%}   [sum of two fitted bands]")
    print(f"  90+ final : {best['active_90_plus_final']:.2%}   [UNFITTED: stationarity]")

    RESULTS_SUMMARY.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RESULTS_SUMMARY / "calibration_runs.parquet", index=False)
    fr.to_csv(RESULTS_SUMMARY / "calibration_grid.csv", index=False)
    payload = {
        "rule": "arrears (D18, 2026-11-09)",
        "derived_shock_prob": p,
        "shock_exit_prob": exit_prob,
        "derived_write_off_rate": ARREARS_RULE["write_off_rate"],
        "labour_flows": True,
        "fitted_payment_friction": f_hat,
        "fitted_arrears_persistence": pi_hat,
        "targets": list(TARGETS),
        "fit_error_points": float(best["fit_error"]),
        "ccmr_bands": bands,
        "target_90_plus": target_90,
        "model_bands": {b: float(best[f"active_{b}"]) for b in BAND_COLS},
        "objective_value": float(best["active_90_plus"]),
        "objective_sd": float(best["active_90_plus_sd"]),
        "fitted_d30": float(best["active_d30"]),
        "unfitted": {
            "active_90_plus": float(best["active_90_plus"]),
            "active_90_plus_final": float(best["active_90_plus_final"]),
            "active_d61_90": float(best["active_d61_90"]),
            "active_d91_120": float(best["active_d91_120"]),
            "active_d120_plus": float(best["active_d120_plus"]),
            "active_current": float(best["active_current"]),
            "default_rate": float(best["default_rate"]),
            "new_default_rate": float(best["new_default_rate"]),
            "initial_default_rate": float(best["initial_default_rate"]),
            "consumption_distress": float(best["consumption_distress"]),
        },
        "qlfs_band": {"lower": qlfs["p_tick_lower"], "upper": qlfs["p_tick_upper"]},
        "replicates": args.reps,
        "earlier_fit": {
            "note": "Streak rule, all households current at t=0: friction 0.09 fitted to 1-30 (2026-10-12); before that p fitted to 90+ (0.016).",
            "payment_friction": 0.09,
            "shock_prob": 0.016,
        },
    }
    (RESULTS_SUMMARY / "calibration.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nwrote {RESULTS_SUMMARY / 'calibration.json'}")


if __name__ == "__main__":
    main()
