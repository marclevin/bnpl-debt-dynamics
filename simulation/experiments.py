"""Experiment grids for RQ1, RQ2, RQ3 and the robustness suite.

Design principle inherited from D17: `beta = 0` is the CONTROL ARM, not one row among
many. Every RQ1 and RQ2 result is a surface over the swept parameter and `beta` jointly,
with the `beta = 0` row always present, because that is what makes the RQ2 claim
non-circular. The grids below enforce this by construction: `BETA_GRID` always starts
at 0.

Access rates are expressed as a share of the BANKED subpopulation (83.1% of households),
never of all households (D11).

Usage:
    python -m simulation.experiments --which rq2 --reps 20
    python -m simulation.experiments --which all --reps 20
"""

from __future__ import annotations

import argparse

from .batch import replicate, run_batch, save
from .config import ParamSet

# ---------------------------------------------------------------------------
# The calibrated baseline. Both values are FITTED (calibrate.py):
#   shock_prob      -> the CCMR 90+ band
#   payment_friction -> the CCMR 1-30 band
# Held fixed across every BNPL run, so nothing downstream is re-tuned.
# ---------------------------------------------------------------------------
FITTED_SHOCK_PROB = 0.048
FITTED_PAYMENT_FRICTION = 0.09


def calibrated(**kw) -> ParamSet:
    return ParamSet(
        shock_prob=FITTED_SHOCK_PROB,
        payment_friction=FITTED_PAYMENT_FRICTION,
        **kw,
    )


#: beta = 0 first and always. The control arm.
BETA_GRID = [0.0, 0.5, 1.0, 2.0, 3.0]
ACCESS_GRID = [0.0, 0.15, 0.30, 0.50, 0.70, 0.85, 1.0]
PLATFORM_GRID = [1, 2, 3, 4, 5, 6]


def rq0_baseline(reps: int) -> list[ParamSet]:
    """The BNPL-free 2017 baseline, and the BNPL-on comparison at defaults.

    Pattern 1 (deHaan complementarity) is read off this pair: enabling BNPL must RAISE
    arrears and interest burden on traditional debt. Falling traditional stress would
    contradict the best available causal evidence and falsify the D5 lender-choice rule.
    """
    arms = [
        calibrated(bnpl_enabled=False, label="baseline_no_bnpl"),
        calibrated(bnpl_enabled=True, beta=0.0, label="bnpl_on_beta0"),
        calibrated(bnpl_enabled=True, beta=1.0, label="bnpl_on_beta1"),
    ]
    return [p for a in arms for p in replicate(a, reps, seed0=10_000)]


def rq1_stacking(reps: int) -> list[ParamSet]:
    """RQ1: when does stacking become self-reinforcing?

    Platform count x beta. N=1 isolates single-platform accumulation from genuine
    cross-firm stacking; beta separates the financial loop (borrow to service) from the
    social loop (adopt because peers adopted).
    """
    out: list[ParamSet] = []
    for n in PLATFORM_GRID:
        for b in BETA_GRID:
            out += replicate(
                calibrated(
                    bnpl_enabled=True, n_platforms=n, beta=b, label=f"rq1_n{n}_b{b}"
                ),
                reps,
                seed0=20_000,
            )
    return out


def rq2_surface(reps: int) -> list[ParamSet]:
    """RQ2: does default respond non-linearly to BNPL access?

    THE central surface: access rate x beta, with the beta=0 row explicit. The claim is
    conditional -- "default responds non-linearly to access ONLY where social
    transmission is present" -- so if the beta=0 row is ALSO non-linear that is a more
    interesting result and must not be buried.
    """
    out: list[ParamSet] = []
    for a in ACCESS_GRID:
        for b in BETA_GRID:
            out += replicate(
                calibrated(
                    bnpl_enabled=True,
                    bnpl_access_rate=a,
                    beta=b,
                    label=f"rq2_a{a}_b{b}",
                ),
                reps,
                seed0=30_000,
            )
    return out


def rq3_interventions(reps: int) -> list[ParamSet]:
    """RQ3: do cool-off interventions change outcomes or merely defer them?

    Defer-versus-desist is measured as CUMULATIVE BNPL VOLUME over the horizon, not the
    timing of purchases. Unchanged volume with shifted timing means agents defer; lower
    cumulative volume means they desist.
    """
    out: list[ParamSet] = []
    for b in (0.0, 1.0):
        # Lever 3: cool-off length. k_cool=1 is the CCA s.66A statutory 14 days.
        for k in (0, 1, 2, 3, 4):
            out += replicate(
                calibrated(bnpl_enabled=True, beta=b, k_cool=k, label=f"rq3_kcool{k}_b{b}"),
                reps,
                seed0=40_000,
            )
        # Lever 1: bureau visibility. The comparison the model was built to make.
        out += replicate(
            calibrated(
                bnpl_enabled=True, beta=b, bnpl_bureau_visible=True, label=f"rq3_bureau_b{b}"
            ),
            reps,
            seed0=41_000,
        )
        # Lever 2: mandatory Reg 23A affordability check on BNPL (FCA PS26/1).
        out += replicate(
            calibrated(
                bnpl_enabled=True,
                beta=b,
                bnpl_affordability_check=True,
                label=f"rq3_afford_b{b}",
            ),
            reps,
            seed0=42_000,
        )
        # Lever 4: concurrent-facility cap. HYPOTHETICAL -- no jurisdiction imposes one.
        for cap in (1, 2, 3):
            out += replicate(
                calibrated(
                    bnpl_enabled=True, beta=b, stacking_cap=cap, label=f"rq3_cap{cap}_b{b}"
                ),
                reps,
                seed0=43_000,
            )
    return out


def robustness(reps: int) -> list[ParamSet]:
    """The mandatory sensitivity arms.

    Several of these are flagged MANDATORY in the decision register rather than optional:
    the D4 amount rule, the D6 minimum-payment formula, and the D16 activation order.
    """
    out: list[ParamSet] = []
    base = dict(bnpl_enabled=True, beta=1.0)

    # D4 amount rule -- MANDATORY. The model's first uncited rule.
    for rule in ("shortfall", "shortfall_125", "shortfall_plus_committed"):
        out += replicate(
            calibrated(**base, amount_rule=rule, label=f"rob_amount_{rule}"), reps, seed0=50_000
        )

    # D6 minimum-payer share -- brackets the transferred US point estimate of 0.29.
    for m in (0.20, 0.25, 0.29, 0.35, 0.40):
        out += replicate(
            calibrated(**base, min_payer_share=m, label=f"rob_m{m}"), reps, seed0=51_000
        )

    # D6 minimum-payment formula -- MANDATORY. The model's second uncited rule.
    for f in (0.025, 0.05, 0.10):
        out += replicate(
            calibrated(**base, min_payment_frac=f, label=f"rob_minpay{f}"), reps, seed0=52_000
        )

    # D16 activation order -- MANDATORY. The peer channel should be insensitive by
    # construction (it reads a lagged share); confirm it empirically.
    for act in ("random", "uniform", "synchronous"):
        out += replicate(
            calibrated(**base, activation=act, label=f"rob_act_{act}"), reps, seed0=53_000
        )

    # D7 default horizon -- k=4 targets the 60+ band instead of 90+.
    for k in (4, 7):
        out += replicate(calibrated(**base, k_default=k, label=f"rob_k{k}"), reps, seed0=54_000)

    # Population-size stability.
    for n in (1000, 5000, 10000):
        out += replicate(calibrated(**base, n_agents=n, label=f"rob_n{n}"), reps, seed0=55_000)

    # D11 rolling limit -- the binding-check parameter (no published figure exists).
    for lim in (1000.0, 5000.0, 15000.0):
        out += replicate(
            calibrated(**base, bnpl_platform_limit=lim, label=f"rob_limit{lim}"),
            reps,
            seed0=56_000,
        )

    # D4 BNPL purchase size -- rests on a trade-press figure.
    for amt in (784.0, 1568.0, 3136.0):
        out += replicate(
            calibrated(**base, bnpl_purchase_mean=amt, label=f"rob_basket{amt}"),
            reps,
            seed0=57_000,
        )

    # D1 shock persistence -- recovers the ORIGINAL single-tick rule (issues.md B17).
    out += replicate(
        calibrated(**base, shock_persistent=False, label="rob_shock_single_tick"),
        reps,
        seed0=58_000,
    )
    return out


SUITES = {
    "rq0": rq0_baseline,
    "rq1": rq1_stacking,
    "rq2": rq2_surface,
    "rq3": rq3_interventions,
    "robustness": robustness,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--which", default="all", choices=[*SUITES, "all"])
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--jobs", type=int, default=-2)
    args = ap.parse_args()

    names = list(SUITES) if args.which == "all" else [args.which]
    total = sum(len(SUITES[n](args.reps)) for n in names)
    print(f"suites: {names}  |  replicates: {args.reps}  |  total runs: {total}")

    for name in names:
        sets = SUITES[name](args.reps)
        print(f"\n=== {name}: {len(sets)} runs ===")
        df = run_batch(sets, n_jobs=args.jobs)
        save(df, name)


if __name__ == "__main__":
    main()
