"""Verification: the D17 peer channel, both mechanisms.

Covers the two changes of 2026-08-13:

  * **B31 / Option A** — `s_g` is normalised onto the BNPL-ELIGIBLE subpopulation, not the
    whole reference group, so the signal can reach 1.0 and its ceiling no longer moves
    with `bnpl_access_rate` (which is RQ2's own x-axis).
  * **The Granovetter threshold arm** — D17's pre-registered structural alternative to
    linear coupling, with `gamma = 0` as its control arm.

The control-arm tests are the important ones. If `beta = 0` or `gamma = 0` fails to
reproduce the independent-agent model exactly, every RQ1 and RQ2 claim about social
transmission is contaminated.
"""

from __future__ import annotations

import warnings

import pytest

from simulation.config import ParamSet
from simulation.model import BNPLModel

warnings.simplefilter("ignore", FutureWarning)

SMALL = dict(n_agents=400, n_ticks=16, burn_in=4)


def build(**kw) -> BNPLModel:
    return BNPLModel(ParamSet(seed=7, **{**SMALL, **kw}))


def run(**kw):
    return build(**kw).run()


_PARAM_ECHO = {
    "seed", "label", "shock_prob", "q_base", "beta", "bnpl_enabled", "bnpl_access_rate",
    "n_platforms", "bnpl_bureau_visible", "bnpl_affordability_check", "k_cool",
    "stacking_cap", "amount_rule", "min_payer_share", "min_payment_frac", "k_default",
    "activation", "bnpl_purchase_base", "bnpl_purchase_ratio",
    "bnpl_limit_income_multiple", "peer_mechanism", "mu_theta", "sigma_theta", "gamma",
}


#: Observations ABOUT the mechanism, not outcomes OF it. `threshold_triggered` counts the
#: households whose personal tipping point the signal has crossed, which is well defined
#: and informative even when `gamma = 0` holds the channel shut — it measures how much
#: cascading WOULD have occurred. It therefore varies with `sigma_theta` in arms whose
#: behaviour is byte-identical, and comparing it would make the control-arm tests assert
#: something they do not mean. Excluded deliberately, and only these two fields are:
#: `peer_share_*` stays in, because it is a real behavioural observable.
_MECHANISM_DIAGNOSTICS = {"threshold_triggered_final", "threshold_triggered_mean"}


def outcomes(summary: dict) -> dict:
    return {
        k: v
        for k, v in summary.items()
        if k not in _PARAM_ECHO and k not in _MECHANISM_DIAGNOSTICS
    }


# ---------------------------------------------------------------------------
# B31: the s_g denominator
# ---------------------------------------------------------------------------


def test_peer_share_is_measured_against_the_eligible_subpopulation():
    """The denominator is who COULD use BNPL, not everyone in the group."""
    m = build(bnpl_enabled=True, q_base=0.6, beta=1.0, bnpl_access_rate=0.5)
    m.run()
    for g, members in m.groups.items():
        assert m.group_eligible[g] <= len(members)
        holders = sum(
            1
            for a in m.agents
            if a.reference_group == g and a.bnpl_outstanding() > 0
        )
        expected = holders / m.group_eligible[g] if m.group_eligible[g] else 0.0
        assert m.group_share_lagged[g] == pytest.approx(expected)


def test_peer_signal_can_reach_high_values_at_low_access():
    """The point of the fix: the ceiling no longer moves with the access rate.

    Before Option A, `s_g` was capped at the group's eligible share, which is
    proportional to `bnpl_access_rate`. At 15% access nothing above ~0.125 could be
    reached ANYWHERE, so a Granovetter threshold drawn on [0,1] would have been compared
    against a signal whose maximum was being swept alongside the axis under test.
    """
    low = build(bnpl_enabled=True, q_base=0.8, beta=0.0, bnpl_access_rate=0.15)
    low.run()
    peak_low = max(r["peer_share_max"] for r in low.history)

    high = build(bnpl_enabled=True, q_base=0.8, beta=0.0, bnpl_access_rate=1.0)
    high.run()
    peak_high = max(r["peer_share_max"] for r in high.history)

    assert peak_low > 0.5, (
        f"peak s_g at 15% access is only {peak_low:.3f}; the signal is still being "
        "diluted by ineligible households (DEFECTS.md B31)"
    )
    # Both regimes must be able to reach a comparable signal, since the quantity is now
    # 'share OF THE ELIGIBLE who are using it' in both.
    assert abs(peak_high - peak_low) < 0.4


def test_peer_share_never_exceeds_one():
    m = build(bnpl_enabled=True, q_base=0.9, beta=3.0)
    m.run()
    assert all(0.0 <= v <= 1.0 for v in m.group_share_lagged.values())
    assert all(0.0 <= r["peer_share_max"] <= 1.0 for r in m.history)


def test_peer_channel_is_inert_with_bnpl_disabled():
    """The baseline calibration must be untouchable by anything in D17."""
    m = build(bnpl_enabled=False, beta=3.0, peer_mechanism="threshold", gamma=0.9)
    m.run()
    assert all(v == 0.0 for v in m.group_share_lagged.values())


# ---------------------------------------------------------------------------
# The Granovetter threshold mechanism
# ---------------------------------------------------------------------------


def test_gamma_zero_recovers_the_independent_agent_model():
    """The threshold arm's CONTROL. Must hold exactly, as beta=0 does for linear."""
    control = run(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.0, q_base=0.05)
    independent = run(bnpl_enabled=True, peer_mechanism="linear", beta=0.0, q_base=0.05)
    assert outcomes(control) == outcomes(independent), (
        "gamma=0 must reproduce the independent-agent model exactly; if it does not, "
        "the threshold arm cannot serve as a control for RQ2"
    )


def test_threshold_dispersion_does_nothing_when_the_channel_is_off():
    """With gamma=0 the thresholds are drawn but cannot act, so sigma cannot matter."""
    a = run(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.0, sigma_theta=0.05)
    b = run(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.0, sigma_theta=0.40)
    assert outcomes(a) == outcomes(b)


def test_thresholds_are_fixed_for_life_and_bounded():
    m = build(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.3)
    before = {a.agent_id: a.theta for a in m.agents}
    assert all(0.0 <= t <= 1.0 for t in before.values())
    assert len(set(round(t, 6) for t in before.values())) > 50, "thresholds must be heterogeneous"
    m.run()
    assert {a.agent_id: a.theta for a in m.agents} == before


def test_linear_arm_draws_no_thresholds():
    """Determinism guard: adding the threshold arm must not perturb the linear one.

    The draw is conditional on the mechanism, so the linear arm's random stream is
    untouched. If this fails, every previously recorded linear result has shifted for a
    reason that has nothing to do with the model.
    """
    m = build(bnpl_enabled=True, peer_mechanism="linear", beta=1.0)
    assert all(a.theta == 0.0 for a in m.agents)


def test_dispersion_changes_adoption_when_the_channel_is_on():
    """Granovetter's actual claim: the VARIANCE of thresholds decides what happens.

    Same mean, different spread, different outcome. If this did not hold, sweeping
    sigma_theta would be pointless and the citation would be decorative.
    """
    tight = run(
        bnpl_enabled=True, peer_mechanism="threshold", gamma=0.4,
        sigma_theta=0.02, mu_theta=0.3, q_base=0.02,
    )
    spread = run(
        bnpl_enabled=True, peer_mechanism="threshold", gamma=0.4,
        sigma_theta=0.40, mu_theta=0.3, q_base=0.02,
    )
    assert tight["bnpl_adoption_final"] != spread["bnpl_adoption_final"]


def test_triggered_share_is_reported_only_for_the_threshold_arm():
    thresholded = run(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.3, q_base=0.3)
    linear = run(bnpl_enabled=True, peer_mechanism="linear", beta=1.0, q_base=0.3)
    assert 0.0 <= thresholded["threshold_triggered_final"] <= 1.0
    assert linear["threshold_triggered_final"] == 0.0


def test_a_household_below_its_threshold_uses_only_the_base_appetite():
    m = build(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.5, q_base=0.07)
    agent = next(a for a in m.agents if a.theta > 0.5)
    assert agent._appetite(0.0) == pytest.approx(0.07)
    assert agent._appetite(1.0) == pytest.approx(0.57)
    # And the step is at the threshold itself, not one side of it.
    assert agent._appetite(agent.theta) == pytest.approx(0.57)


def test_appetite_is_clipped_to_a_probability():
    m = build(bnpl_enabled=True, peer_mechanism="threshold", gamma=5.0, q_base=0.5)
    agent = next(iter(m.agents))
    assert agent._appetite(1.0) == 1.0
    m2 = build(bnpl_enabled=True, peer_mechanism="linear", beta=-99.0, q_base=0.5)
    assert next(iter(m2.agents))._appetite(1.0) == 0.0
