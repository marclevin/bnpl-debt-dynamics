"""Verification: the three effect-robustness switches added on 2026-10-06.

Each switch defaults to the behaviour of every stored run. These tests pin what each does
when it is turned on:

  * `platform_routing="loyal"` sends a request to a platform already owed before any other;
  * `shortfall_bnpl=False` sends a shortfall to the traditional lender only;
  * `committed_shortfall_funded=True` spends credit raised in a tick with a committed
    shortfall on that shortfall first.
"""

from __future__ import annotations

import pytest

from simulation.tests.lab import household, open_agreements

#: Large limits, so the first platform tried can always finance the whole request.
ROOMY = dict(income_tick=20000, committed_tick=0, bnpl_limit_income_multiple=1.0)


def _platforms_used(model, agent) -> set[int]:
    return {id(p) for p in model.platforms if p.has_balance(agent.agent_id)}


def test_loyal_routing_returns_to_the_platform_already_owed():
    for seed in range(20):
        model, a = household(**ROOMY, seed=seed, platform_routing="loyal")
        a._bnpl_draw(100.0)
        a._bnpl_draw(100.0)
        assert len(open_agreements(model, a)) == 2
        assert len(_platforms_used(model, a)) == 1


def test_random_routing_spreads_a_second_request_across_platforms():
    spread = 0
    for seed in range(20):
        model, a = household(**ROOMY, seed=seed)
        a._bnpl_draw(100.0)
        a._bnpl_draw(100.0)
        spread += len(_platforms_used(model, a)) == 2
    # A second request reaches a different platform first with probability 3/4.
    assert 8 <= spread <= 20


def test_loyal_routing_spills_over_only_when_the_limit_binds():
    model, a = household(income_tick=3000 * 12 / 26, committed_tick=0,
                         platform_routing="loyal")  # limit 0.10 x R3,000 = R300 a platform
    a._bnpl_draw(380.0)  # receivable R285 of the R300 limit
    a._bnpl_draw(100.0)  # room for an order of R20 on the first platform; the rest moves on
    assert len(_platforms_used(model, a)) == 2


SHORT = dict(
    income_tick=3000, committed_tick=3000, discretionary_tick=2000, d_trad=4000,
    service_tick=200, apr=0.0,
)


def test_without_shortfall_bnpl_the_lender_is_asked_for_the_whole_shortfall():
    model, a = household(**SHORT, shortfall_bnpl=False)
    model.step()
    assert open_agreements(model, a) == []
    assert model.lender.value_granted == pytest.approx(200.0)
    assert a.paid_trad_tick == pytest.approx(200.0)


#: Income R1,000 against R1,200 of committed spending: a R200 committed shortfall and no
#: debt service, so the whole request is the committed shortfall.
FOOD_SHORT = dict(income_tick=1000, committed_tick=1200, discretionary_tick=0, d_trad=0)


def test_by_default_credit_raised_against_a_committed_shortfall_is_saved():
    model, a = household(**FOOD_SHORT, bnpl_enabled=False)
    model.step()
    assert model.lender.value_granted == pytest.approx(200.0)
    assert a.savings == pytest.approx(200.0)
    assert a.distress_streak == 1


def test_funded_committed_shortfall_spends_the_loan_on_it():
    model, a = household(**FOOD_SHORT, bnpl_enabled=False, committed_shortfall_funded=True)
    model.step()
    assert model.lender.value_granted == pytest.approx(200.0)
    assert a.savings == pytest.approx(0.0)
    assert a.distress_streak == 1  # the shortfall is still distress
