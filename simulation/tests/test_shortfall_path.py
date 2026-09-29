"""Verification: a shortfall financed by BNPL, by the traditional lender, or by both.

The contract (D13) takes 25% at checkout and 25% at each of the next three ticks. The
borrowing rules (D4, D5) have the household request its shortfall, use BNPL first and
send what BNPL cannot cover to the traditional lender. Two defects were corrected on
2026-09-29 and are pinned here:

  * the traditional lender was asked for the request less the whole amount BNPL financed,
    although BNPL relieves only three quarters of it, so the household stayed a quarter
    short whatever the lenders were willing to grant;
  * the instalment after checkout was collected in the tick the agreement was opened.

A shortfall is NOT removed by construction. When the traditional lender refuses, the
household stays short and is recorded as distressed.
"""

from __future__ import annotations

import pytest

from simulation.tests.lab import household, open_agreements

#: Income equals committed expenditure, so the R200 instalment is a R200 shortfall. The
#: discretionary budget is large enough that the BNPL share of the request is not capped.
SHORT = dict(
    income_tick=3000, committed_tick=3000, discretionary_tick=2000, d_trad=4000,
    service_tick=200, apr=0.0,
)


def test_traditional_credit_alone_covers_the_shortfall():
    model, a = household(**SHORT, bnpl_enabled=False)
    model.step()
    assert model.lender.value_granted == pytest.approx(200.0)
    assert a.paid_trad_tick == pytest.approx(200.0)
    assert a.distress_streak == 0


def test_bnpl_relieves_three_quarters_and_the_lender_is_asked_for_the_rest():
    model, a = household(**SHORT)
    model.step()
    (loan,) = open_agreements(model, a)
    assert loan.principal == pytest.approx(200.0)
    # 200 financed frees 150; the remaining 50 is requested from the traditional lender.
    assert model.lender.n_applications == 1
    assert model.lender.value_granted == pytest.approx(50.0)
    assert a.paid_trad_tick == pytest.approx(200.0)
    assert a.arrears_trad == 0.0
    assert a.distress_streak == 0


def test_a_refusal_leaves_the_shortfall_unpaid_and_recorded():
    model, a = household(**SHORT)
    a.income_monthly = 500.0  # below the Reg 23A expense norm: no room for any instalment
    model.step()
    assert model.lender.n_applications == 1
    assert model.lender.n_refused_gate == 1
    assert model.lender.value_granted == 0.0
    # BNPL still freed 150 of the 200 due; 50 goes unpaid and the tick counts as distress.
    assert a.paid_trad_tick == pytest.approx(150.0)
    assert a.arrears_trad == pytest.approx(50.0)
    assert a.distress_streak == 1


def test_a_household_without_bnpl_access_uses_the_lender_for_everything():
    model, a = household(**SHORT)
    a.bnpl_eligible = False
    model.step()
    assert open_agreements(model, a) == []
    assert model.lender.value_granted == pytest.approx(200.0)
    assert a.distress_streak == 0


def test_the_bnpl_share_of_a_shortfall_is_capped_at_kappa_times_the_budget():
    # Discretionary budget R100 a tick = R216.67 a month; kappa x budget = R30.05.
    kw = {**SHORT, "discretionary_tick": 100}
    model, a = household(**kw)
    model.step()
    (loan,) = open_agreements(model, a)
    cap = model.params.bnpl_purchase_ratio * a.rec.discretionary_monthly
    assert loan.principal == pytest.approx(cap)
    assert model.lender.value_granted == pytest.approx(200.0 - 0.75 * cap)
    assert a.distress_streak == 0


def test_cash_is_conserved_in_the_tick_a_shortfall_is_financed():
    """opening cash + income + credit raised = committed + payments + closing savings."""
    model, a = household(**{**SHORT, "savings": 40.0})
    model.step()
    (loan,) = open_agreements(model, a)
    raised = 0.75 * loan.principal + a.borrowed_trad_tick
    uses = 3000.0 + a.paid_trad_tick + a.savings  # no BNPL instalment falls due this tick
    assert 40.0 + 3000.0 + raised == pytest.approx(uses)


# ------------------------------------------------------------------ instalment timing
def test_nothing_is_collected_in_the_tick_a_shortfall_agreement_is_opened():
    model, a = household(**SHORT)
    model.step()
    (loan,) = open_agreements(model, a)
    assert loan.remaining == 3
    assert loan.arrears == 0.0


def test_a_shortfall_agreement_is_repaid_over_the_next_three_ticks():
    model, a = household(**SHORT)
    model.step()
    (loan,) = open_agreements(model, a)
    # Remove the shortfall so that no further agreement is opened.
    a.rec.income_tick = 6000.0
    remaining = []
    for _ in range(3):
        due = a.bnpl_due_per_tick()
        assert due == pytest.approx(50.0)
        model.step()
        remaining.append(loan.remaining)
    assert remaining == [2, 1, 0]
    assert open_agreements(model, a) == []


def test_a_want_driven_purchase_follows_the_same_schedule():
    model, a = household(
        income_tick=3000, committed_tick=1000, discretionary_tick=500, q_base=1.0,
        bnpl_purchase_cv=0.0001,
    )
    model.step()
    (loan,) = open_agreements(model, a)
    assert loan.remaining == 3
    paid_at_checkout = loan.principal / 4
    assert a.savings == pytest.approx(3000 - 1000 - 500 - paid_at_checkout)
    object.__setattr__(model, "params", model.params.replace(q_base=0.0))
    for expected in (2, 1, 0):
        model.step()
        assert loan.remaining == expected


def test_both_gates_see_an_agreement_opened_in_the_same_tick():
    """Timing changed what is COLLECTED in the opening tick, not what a gate is shown."""
    model, a = household(income_tick=3000, committed_tick=1000, bnpl_limit_income_multiple=1.0)
    model.platforms[0].request(a.agent_id, 400.0, model.tick)
    assert a.bnpl_due_per_tick() == 0.0
    assert a.bnpl_obligations_per_tick() == pytest.approx(100.0)
    model.bureau.bnpl_visible = True
    assert model.bureau.visible_monthly_service(a) == pytest.approx(100.0 * 26 / 12)
