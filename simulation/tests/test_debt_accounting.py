"""Verification: interest, payments and arrears on traditional debt.

Until the corrections of 2026-09-29 interest was added to the balance at accrual and
then deducted from the payment before the payment was taken off the balance, so every
paying household was charged its interest twice. These tests fix the identity

    closing balance = opening balance + interest + new loans - payments

for a single household by hand and for a whole population tick by tick.
"""

from __future__ import annotations

import warnings

import pytest

from simulation.config import ParamSet
from simulation.model import BNPLModel
from simulation.tests.lab import household

warnings.simplefilter("ignore", FutureWarning)


def level_instalment(balance: float, rate: float, n: int) -> float:
    return balance * rate / (1.0 - (1.0 + rate) ** (-n))


def test_a_payment_comes_off_the_balance_in_full():
    """R1,000 at 1% a tick with R100 paid: 1000 + 10 - 100 = 910."""
    model, a = household(
        income_tick=5000, committed_tick=1000, d_trad=1000, service_tick=100, bnpl_enabled=False
    )
    model.step()
    assert a.interest_charged_tick == pytest.approx(10.0)
    assert a.paid_trad_tick == pytest.approx(100.0)
    assert a.d_trad == pytest.approx(910.0)


def test_a_loan_amortises_on_its_contract_schedule():
    """A level instalment over 12 ticks clears the balance in 12 ticks, not 15."""
    instalment = level_instalment(1000.0, 0.01, 12)
    model, a = household(
        income_tick=5000,
        committed_tick=1000,
        d_trad=1000,
        service_tick=instalment,
        bnpl_enabled=False,
        n_ticks=20,
    )
    paid = 0.0
    for tick in range(12):
        assert a.d_trad > 0, f"cleared early, at tick {tick}"
        model.step()
        paid += a.paid_trad_tick
    assert a.d_trad == 0.0
    assert paid == pytest.approx(12 * instalment)


def test_a_cleared_debt_shows_the_lender_no_service():
    instalment = level_instalment(1000.0, 0.01, 4)
    model, a = household(
        income_tick=5000,
        committed_tick=1000,
        d_trad=1000,
        service_tick=instalment,
        bnpl_enabled=False,
    )
    for _ in range(5):
        model.step()
    assert a.d_trad == 0.0
    assert a.scheduled_service_tick == 0.0
    assert model.bureau.visible_monthly_service(a) == 0.0
    # and nothing further is collected
    model.step()
    assert a.paid_trad_tick == 0.0


def test_a_minimum_payer_pays_the_larger_of_interest_and_the_fraction():
    # 5% of the balance a month is 2.3% a tick, which exceeds 1% interest.
    model, a = household(
        income_tick=5000,
        committed_tick=1000,
        d_trad=1000,
        min_payer=True,
        bnpl_enabled=False,
    )
    model.step()
    expected = 1010.0 * model.params.min_payment_frac * 12 / 26
    assert a.paid_trad_tick == pytest.approx(expected)
    assert a.d_trad == pytest.approx(1010.0 - expected)


def test_a_minimum_payer_never_amortises_negatively():
    # 60% a year is 2.31% a tick, above the 2.3% fraction: the interest floor binds.
    model, a = household(
        income_tick=5000,
        committed_tick=1000,
        d_trad=1000,
        apr=0.60,
        min_payer=True,
        min_payment_frac=0.025,
        bnpl_enabled=False,
    )
    model.step()
    assert a.paid_trad_tick == pytest.approx(a.interest_charged_tick)
    assert a.d_trad == pytest.approx(1000.0)


def test_an_unpaid_instalment_is_arrears_inside_the_balance():
    """Arrears are part of what is owed, not an addition to it."""
    model, a = household(
        income_tick=1000, committed_tick=1000, d_trad=1000, service_tick=100, bnpl_enabled=False
    )
    a.defaulted = True  # no borrowing, so the instalment simply goes unpaid
    model.step()
    assert a.paid_trad_tick == 0.0
    assert a.arrears_trad == pytest.approx(100.0)
    assert a.d_trad == pytest.approx(1010.0)
    assert a.total_debt() == pytest.approx(1010.0)


def test_the_amount_due_never_exceeds_the_balance():
    """Arrears and the instalment together are capped at what is owed."""
    model, a = household(
        income_tick=1000, committed_tick=1000, d_trad=150, service_tick=100, apr=0.0,
        bnpl_enabled=False,
    )
    a.defaulted = True
    model.step()  # R100 unpaid
    model.step()  # R100 + R100 arrears would be R200; only R150 is owed
    assert a.arrears_trad == pytest.approx(150.0)
    a.rec.income_tick = 5000.0
    model.step()
    assert a.paid_trad_tick == pytest.approx(150.0)
    assert a.d_trad == 0.0


@pytest.mark.parametrize("bnpl", [False, True])
def test_the_balance_identity_holds_for_every_household_every_tick(bnpl):
    """closing = opening + interest + borrowed - paid, across a full population."""
    model = BNPLModel(
        ParamSet(
            seed=11,
            n_agents=600,
            n_ticks=30,
            burn_in=0,
            shock_prob=0.05,
            payment_friction=0.09,
            bnpl_enabled=bnpl,
            beta=1.0,
        )
    )
    agents = list(model.agents)
    checked = 0
    for _ in range(30):
        opening = {a.agent_id: a.d_trad for a in agents}
        model.step()
        for a in agents:
            expected = (
                opening[a.agent_id]
                + a.interest_charged_tick
                + a.borrowed_trad_tick
                - a.paid_trad_tick
            )
            assert a.d_trad == pytest.approx(max(expected, 0.0), abs=2e-3)
            assert a.arrears_trad <= a.d_trad + 1e-9
            checked += a.d_trad > 0
    assert checked > 1000, "too few indebted household-ticks to exercise the identity"
