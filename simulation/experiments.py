"""Experiment grids for the research questions and the robustness suite.

NUMBERING. The grid keys below (`rq1`, `rq2`, `rq2t`, `rq3`) are the ORIGINAL scheme and
are deliberately frozen: they are baked into every label in `results/raw/`, into the
`load()` keys in analysis.py, and into figure filenames cited by the thesis. Renaming
them would orphan the existing runs for no gain. Map them to the thesis as:
  * `rq1_stacking`   -> thesis RQ2, the stacking half
  * `rq2_surface`    -> thesis RQ2, the access-and-default half
  * `rq2_threshold`  -> thesis RQ2, pre-registered structural alternative
  * `rq3_*`          -> thesis RQ3, unchanged
Thesis RQ1 (does the population reproduce behaviour it was not fitted to) has no grid
here: it is answered by the data layer and the calibrated baseline, not by a sweep.

Design principle inherited from D17: `beta = 0` is the CONTROL ARM, not one row among
many. Every thesis-RQ2 result is a surface over the swept parameter and `beta` jointly,
with the `beta = 0` row always present, because that is what makes the RQ2 claim
non-circular. The grids below enforce this by construction: `BETA_GRID` always starts
at 0.

Access rates are expressed as a share of the BANKED subpopulation (82.8% of households),
never of all households (D11).

Usage:
    python -m simulation.experiments --which rq2 --reps 20
    python -m simulation.experiments --which all --reps 20
"""

from __future__ import annotations

import argparse

from .batch import replicate, run_batch, save
from .config import BNPL_PURCHASE_SHARE_OF_DISCRETIONARY, ParamSet

# ---------------------------------------------------------------------------
# The calibrated baseline. Both values are FITTED (calibrate.py):
#   shock_prob      -> the CCMR 90+ band
#   payment_friction -> the CCMR 1-30 band
# Held fixed across every BNPL run, so nothing downstream is re-tuned.
#
# NOTE: neither is disturbed by BNPL-side parameter work. Both are fitted with
# `bnpl_enabled=False`, and the peer channel is inert in that arm. They DO depend on the
# population: re-fitted 2026-09-21 (results/summary/calibration.json, 20 replicates) after
# P0 stopped counting imputed rent as discretionary spending (DEFECTS.md B32). A smaller
# compressible buffer absorbs less, so the shock rate fell from 0.048 to 0.040; friction
# did not move.
# ---------------------------------------------------------------------------
FITTED_SHOCK_PROB = 0.040
FITTED_PAYMENT_FRICTION = 0.09

#: kappa as derived from IES 2022/23. Held here so the robustness grid centres on the
#: derived value rather than on a number typed twice.
PURCHASE_RATIO = BNPL_PURCHASE_SHARE_OF_DISCRETIONARY


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
    """Thesis RQ2, stacking half: do households accumulate facilities no lender sees?

    Grid key `rq1` is frozen -- see the numbering note at the top of this module.

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


#: Threshold dispersion, the primary axis of the Granovetter arm. 0.0 is near-homogeneous
#: (everyone tips at the same point, so either nobody starts or everyone goes at once) and
#: 0.40 is highly dispersed (someone stands at every level, so adoption can ratchet).
SIGMA_THETA_GRID = [0.05, 0.10, 0.20, 0.30, 0.40]
#: The threshold arm's control. gamma=0 recovers the independent-agent model exactly.
GAMMA_GRID = [0.0, 0.3]


def rq2_threshold(reps: int) -> list[ParamSet]:
    """RQ2 under Granovetter heterogeneous thresholds, the PRE-REGISTERED alternative.

    D17 registered this as the structural robustness check should linear coupling produce
    only a smooth response, which is exactly what happened (DEFECTS.md B22). A linear rule
    producing a linear response is close to tautological, so the negative result needs a
    structurally different mechanism before it can be believed.

    **`sigma_theta` is the axis, not `mu_theta`.** Granovetter's claim is about the
    VARIANCE of thresholds: a distribution with someone standing at every level cascades,
    a tightly clustered one does not, at identical means. `mu_theta` gets a small separate
    sensitivity rather than a full cross, which keeps this arm at the same run count as the
    linear surface it is compared against.

    **What this arm is really for.** Not "one more attempt to find a threshold". It
    separates ADOPTION tipping from DISTRESS tipping. The model has peer feedback in its
    input and none in its output, so if this arm produces a sharp adoption cascade and
    default still responds linearly to access, that is a much stronger answer to RQ2 than
    the linear arm can give: the cascade mechanism demonstrably works and still does not
    move the outcome.
    """
    out: list[ParamSet] = []
    for a in ACCESS_GRID:
        for s in SIGMA_THETA_GRID:
            for g in GAMMA_GRID:
                out += replicate(
                    calibrated(
                        bnpl_enabled=True,
                        bnpl_access_rate=a,
                        peer_mechanism="threshold",
                        sigma_theta=s,
                        gamma=g,
                        label=f"rq2t_a{a}_s{s}_g{g}",
                    ),
                    reps,
                    seed0=60_000,
                )
    # mu_theta sensitivity, at full access and the mid dispersion only.
    for m in (0.15, 0.30, 0.45):
        out += replicate(
            calibrated(
                bnpl_enabled=True,
                peer_mechanism="threshold",
                sigma_theta=0.20,
                gamma=0.3,
                mu_theta=m,
                label=f"rq2t_mu{m}",
            ),
            reps,
            seed0=61_000,
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
        # The same three rules with the shortfall path UNCAPPED, as it was in the working
        # run, so the thesis can say whether the cap narrows this sensitivity. Same seeds
        # as the capped arms above: a paired comparison.
        out += replicate(
            calibrated(
                **base,
                amount_rule=rule,
                shortfall_bnpl_capped=False,
                label=f"rob_amount_{rule}_uncapped",
            ),
            reps,
            seed0=50_000,
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

    # D11 rolling limit -- MANDATORY. No SA provider publishes one, so the range is set
    # from the external band: ~0.1 months of income per provider implied by Woolard, and
    # ~0.26 by Afterpay's published maximum. 1.0 is deliberately outside it, to show what
    # the old flat R5,000 constant was really assuming (DEFECTS.md B30).
    for lam in (0.1, 0.25, 0.5, 1.0):
        out += replicate(
            calibrated(**base, bnpl_limit_income_multiple=lam, label=f"rob_limit{lam}"),
            reps,
            seed0=56_000,
        )

    # D4 BNPL purchase size -- MANDATORY. Half to double the IES-derived budget share.
    for ratio in (0.07, PURCHASE_RATIO, 0.28):
        out += replicate(
            calibrated(**base, bnpl_purchase_ratio=ratio, label=f"rob_kappa{ratio}"),
            reps,
            seed0=57_000,
        )

    # D4 purchase BASE -- MANDATORY. Discretionary is the primary rule; income is the
    # base the international regulator ratios are expressed against, so it is the arm
    # that answers "does the anchor choice drive the result?".
    for basis in ("discretionary", "income"):
        out += replicate(
            calibrated(
                **base,
                bnpl_purchase_base=basis,
                # Sized so the two bases produce a comparable population mean purchase,
                # otherwise the arm would confound the base with the level.
                bnpl_purchase_ratio=PURCHASE_RATIO if basis == "discretionary" else 0.073,
                label=f"rob_base_{basis}",
            ),
            reps,
            seed0=59_000,
        )

    # D1 shock persistence -- recovers the ORIGINAL single-tick rule (DEFECTS.md B17).
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
    "rq2t": rq2_threshold,
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
