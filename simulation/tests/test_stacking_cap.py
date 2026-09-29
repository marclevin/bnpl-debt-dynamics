"""Verification: what the hypothetical cap counts and which draws it refuses (D14).

The register specifies "a maximum on concurrent facilities". A facility is a platform on
which the household owes a balance, so the cap counts platforms. Until 2026-09-29 the
thesis described it as a count of agreements, which holds only for a cap of one.
"""

from __future__ import annotations

import pytest

from simulation.tests.lab import household, open_agreements

AMPLE = dict(income_tick=30_000, committed_tick=1_000, bnpl_limit_income_multiple=1.0)


def owe(model, agent, platform_ids):
    for i in platform_ids:
        assert model.platforms[i].request(agent.agent_id, 100.0, model.tick) == 100.0


@pytest.mark.parametrize("cap", [1, 2, 3])
def test_a_household_at_the_cap_is_refused_every_draw(cap):
    model, a = household(**AMPLE, stacking_cap=cap)
    owe(model, a, range(cap))
    assert a.stacking_depth() == cap
    assert a._bnpl_draw(100.0) == 0.0
    assert len(open_agreements(model, a)) == cap


def test_at_the_cap_a_platform_already_in_use_is_refused_too():
    model, a = household(**AMPLE, stacking_cap=2, n_platforms=2)
    owe(model, a, [0, 1])
    # Both platforms are already in use and have headroom; the draw is still refused.
    assert a._bnpl_draw(100.0) == 0.0


def test_a_cap_of_one_is_one_agreement_at_a_time():
    model, a = household(**AMPLE, stacking_cap=1)
    granted = sum(a._bnpl_draw(100.0) > 0 for _ in range(20))
    assert granted == 1
    assert len(open_agreements(model, a)) == 1


def test_the_cap_counts_platforms_not_agreements():
    """Below the cap a household may hold several agreements on one platform."""
    model, a = household(**AMPLE, stacking_cap=2, n_platforms=1)
    granted = sum(a._bnpl_draw(100.0) > 0 for _ in range(5))
    assert granted == 5
    assert a.stacking_depth() == 1
    assert len(open_agreements(model, a)) == 5


def test_under_a_cap_of_two_open_agreements_can_exceed_two():
    most = 0
    for seed in range(40):
        model, a = household(**AMPLE, stacking_cap=2, seed=seed)
        for _ in range(20):
            a._bnpl_draw(100.0)
        assert a.stacking_depth() <= 2
        most = max(most, len(open_agreements(model, a)))
    assert most > 2


@pytest.mark.parametrize("cap", [1, 2, 3])
def test_one_large_order_cannot_open_more_platforms_than_the_cap(cap):
    # Per-platform limit 0.10 x R6,500: a R5,000 order must be split across platforms.
    model, a = household(income_tick=3_000, committed_tick=1_000, stacking_cap=cap)
    a._bnpl_draw(5_000.0)
    assert a.stacking_depth() == cap


def test_without_a_cap_the_same_order_spreads_over_every_platform():
    model, a = household(income_tick=3_000, committed_tick=1_000)
    a._bnpl_draw(5_000.0)
    assert a.stacking_depth() == 4
