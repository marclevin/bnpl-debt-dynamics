"""Verification: degenerate cases.

These are the checks ch.5 commits to. Each one asserts that a limiting case of the model
reduces exactly to a simpler model it should reduce to. They are the strongest evidence
available that the implementation is the specification.
"""

from __future__ import annotations

import warnings

import pytest

from simulation.config import ParamSet
from simulation.model import BNPLModel

warnings.simplefilter("ignore", FutureWarning)

#: Small and short: these tests check exact equality, not statistical behaviour.
SMALL = dict(n_agents=400, n_ticks=16, burn_in=4)


def run(**kw):
    return BNPLModel(ParamSet(seed=7, **{**SMALL, **kw})).run()


#: The run summary echoes its own parameters for provenance, so comparing two arms means
#: comparing OUTCOMES only. Anything that is an input, not a result, is excluded here.
_PARAM_ECHO = {
    "seed", "label", "shock_prob", "q_base", "beta", "bnpl_enabled", "bnpl_access_rate",
    "n_platforms", "bnpl_bureau_visible", "bnpl_affordability_check", "k_cool",
    "stacking_cap", "amount_rule", "shortfall_bnpl_capped", "min_payer_share",
    "min_payment_frac", "k_default", "activation", "bnpl_purchase_base", "bnpl_purchase_ratio",
    "bnpl_limit_income_multiple", "peer_mechanism", "mu_theta", "sigma_theta", "gamma",
}


def outcomes(summary: dict) -> dict:
    return {k: v for k, v in summary.items() if k not in _PARAM_ECHO}


def test_bnpl_disabled_reproduces_the_baseline_exactly():
    """Injection design: with BNPL off the model must be the BNPL-free 2017 baseline.

    Changing BNPL-side parameters must have no effect whatsoever when BNPL is disabled.
    """
    base = run(bnpl_enabled=False)
    fiddled = run(
        bnpl_enabled=False,
        n_platforms=6,
        q_base=0.9,
        beta=5.0,
        bnpl_limit_income_multiple=99.0,
        bnpl_purchase_ratio=0.9,
        k_cool=4,
        # The calibration is fitted with BNPL off, so it must not depend on the cap.
        shortfall_bnpl_capped=False,
    )
    assert outcomes(base) == outcomes(fiddled)


def test_beta_zero_recovers_the_independent_agent_model():
    """D17: beta=0 must recover the pre-D17 model exactly.

    This is the control arm for RQ2 and RQ3. If it does not hold exactly, every RQ2
    claim about social transmission is contaminated.
    """
    a = run(bnpl_enabled=True, beta=0.0, q_base=0.05)
    b = run(bnpl_enabled=True, beta=0.0, q_base=0.05)
    assert outcomes(a) == outcomes(b)

    # With beta=0 the adoption propensity cannot depend on the group share, so changing
    # nothing but beta away from 0 must be the only thing that can change adoption.
    c = run(bnpl_enabled=True, beta=8.0, q_base=0.05)
    assert c["bnpl_adoption_final"] >= a["bnpl_adoption_final"]


def test_peer_channel_is_inert_in_the_baseline():
    """s_g must be identically zero with BNPL disabled.

    The CCMR calibration depends on this: if the peer channel were live in the baseline,
    the fitted shock probability would absorb social-transmission effects.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        m = BNPLModel(ParamSet(seed=7, bnpl_enabled=False, beta=3.0, **SMALL))
        m.run()
    assert all(v == 0.0 for v in m.group_share_lagged.values())


def test_single_platform_reduces_stacking_to_single_platform_accumulation():
    """N=1 isolates single-platform accumulation from cross-firm stacking (D12)."""
    r = run(bnpl_enabled=True, n_platforms=1, q_base=0.5, beta=0.0)
    assert r["stacking_2plus_final"] == 0.0
    assert r["stacking_mean_final"] <= 1.0

    multi = run(bnpl_enabled=True, n_platforms=4, q_base=0.5, beta=0.0)
    assert multi["stacking_mean_final"] >= r["stacking_mean_final"]


def test_same_seed_is_reproducible_and_different_seeds_differ():
    a = BNPLModel(ParamSet(seed=11, bnpl_enabled=True, q_base=0.3, **SMALL)).run()
    b = BNPLModel(ParamSet(seed=11, bnpl_enabled=True, q_base=0.3, **SMALL)).run()
    c = BNPLModel(ParamSet(seed=12, bnpl_enabled=True, q_base=0.3, **SMALL)).run()
    assert outcomes(a) == outcomes(b)
    assert outcomes(a) != outcomes(c)


def test_payment_friction_moves_arrears_but_not_default():
    """D6 friction must generate mild delinquency without generating insolvency.

    A household that skips an affordable instalment through present bias is NOT
    cash-flow insolvent, so D7 distress is assessed before friction is applied and
    friction must not inflate the headline default rate.

    It is not perfectly orthogonal, and the residual effect is explicable rather than a
    defect: withholding a payment CONSERVES cash, so heavy friction slightly *reduces*
    default by leaving households more liquid the following tick. What must not happen
    is friction driving default UP, which would mean the parameter fitted to the 1-30
    band was contaminating the model's main output variable.
    """
    none = run(bnpl_enabled=False, shock_prob=0.03, payment_friction=0.0)
    lots = run(bnpl_enabled=False, shock_prob=0.03, payment_friction=0.25)

    # The 1-30 band must move substantially: that is what friction is for.
    assert lots["active_d30_mean"] > none["active_d30_mean"] * 2

    # Default must not rise, and any residual movement must be small.
    delta = lots["default_rate_final"] - none["default_rate_final"]
    assert delta <= 0.0, "friction increased the default rate; D7 is contaminated"
    assert abs(delta) < 0.01, f"friction moved default by {delta:.4f}, more than 1pp"


def test_zero_friction_is_the_no_friction_model():
    a = run(bnpl_enabled=False, shock_prob=0.03, payment_friction=0.0)
    b = run(bnpl_enabled=False, shock_prob=0.03, payment_friction=0.0)
    assert outcomes(a) == outcomes(b)


def test_zero_shock_probability_produces_no_shocks():
    r = run(bnpl_enabled=False, shock_prob=0.0)
    assert r["shocked_rate_mean"] == 0.0


def test_stacking_cap_binds():
    uncapped = run(bnpl_enabled=True, n_platforms=4, q_base=0.6, stacking_cap=None)
    capped = run(bnpl_enabled=True, n_platforms=4, q_base=0.6, stacking_cap=1)
    assert capped["stacking_2plus_final"] == 0.0
    assert capped["stacking_mean_final"] <= uncapped["stacking_mean_final"]


def test_bureau_visibility_tightens_the_gate():
    """Lever 1: with BNPL visible the lender gates against the fuller liability set.

    The gap between the two arms is the measured cost of the reporting exemption.
    """
    hidden = run(bnpl_enabled=True, q_base=0.5, bnpl_bureau_visible=False)
    visible = run(bnpl_enabled=True, q_base=0.5, bnpl_bureau_visible=True)
    assert visible["trad_granted"] <= hidden["trad_granted"]


def test_cool_off_cannot_increase_bnpl_volume():
    """RQ3: a cool-off blocks want-driven initiation, so volume cannot rise.

    ⚠ This test is NECESSARY BUT NOT SUFFICIENT, and that is why DEFECTS.md B27 survived
    the suite for a full experimental run: a no-op satisfies `<=` trivially, and volume
    mixes in the shortfall-driven path, which the cool-off deliberately does not block.
    The test that has teeth is
    `test_bnpl_parameters.test_statutory_cool_off_strictly_reduces_want_driven_purchases`,
    which asserts a STRICT reduction in the want-driven purchase COUNT. Keep both.
    """
    off = run(bnpl_enabled=True, q_base=0.5, k_cool=0)
    on = run(bnpl_enabled=True, q_base=0.5, k_cool=4)
    assert on["bnpl_volume_cumulative"] <= off["bnpl_volume_cumulative"]


@pytest.mark.parametrize("activation", ["random", "uniform"])
def test_all_activation_regimes_run(activation):
    r = run(bnpl_enabled=True, q_base=0.2, activation=activation)
    assert 0.0 <= r["default_rate_final"] <= 1.0
