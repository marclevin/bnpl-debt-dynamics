"""Verification: the Pay-in-4 schedule and the late-fee cap (D13).

Both are taken from published Payflex terms, so these tests check the implementation
against a real product rather than against a modelling choice.
"""

from __future__ import annotations

import pytest

from simulation.bnpl import BNPLPlatform


def make_platform(**kw) -> BNPLPlatform:
    defaults = dict(
        platform_id=0,
        order_cap=15_000.0,
        rolling_limit=5_000.0,
        late_fee_per_tick=190.0,
        late_fee_cap=285.0,
        n_instalments=4,
    )
    defaults.update(kw)
    return BNPLPlatform(**defaults)


def test_pay_in_four_splits_into_quarters_with_three_remaining():
    """25% at checkout then 25% at each of the next three ticks."""
    p = make_platform()
    financed = p.request(1, 1000.0)
    assert financed == 1000.0
    loan = p.loans[1][0]
    assert loan.instalment == pytest.approx(250.0)
    # Checkout takes the first quarter, so three instalments remain to be collected.
    assert loan.remaining == 3


def test_instalments_land_exactly_on_tick_boundaries():
    """Three further instalments, one per tick, then the facility is settled.

    This is the property that retroactively validated the 14-day tick: Payflex
    instalments fall exactly on tick boundaries, so no discretisation error enters.
    """
    p = make_platform()
    p.request(1, 1000.0)
    for tick in range(3):
        assert p.due(1) == pytest.approx(250.0), f"tick {tick}"
        paid, fees = p.collect(1, 250.0)
        assert paid == pytest.approx(250.0)
        assert fees == 0.0
    # Settled after exactly three post-checkout ticks.
    assert not p.has_balance(1)
    assert p.due(1) == 0.0


def test_late_fee_is_190_per_tick_and_caps_at_285():
    """R95 per week = R190 per 14-day tick, capped at three weeks = R285."""
    p = make_platform()
    p.request(1, 1000.0)

    _, fees1 = p.collect(1, 0.0)
    assert fees1 == pytest.approx(190.0)

    # Second miss can only take the fee to the cap, not 190 again.
    _, fees2 = p.collect(1, 0.0)
    assert fees2 == pytest.approx(95.0)
    assert p.loans[1][0].fee_accrued == pytest.approx(285.0)

    # Third miss charges nothing further.
    _, fees3 = p.collect(1, 0.0)
    assert fees3 == 0.0
    assert p.loans[1][0].fee_accrued == pytest.approx(285.0)


def test_household_is_cut_off_once_the_fee_cap_is_exhausted():
    p = make_platform()
    p.request(1, 1000.0)
    p.collect(1, 0.0)
    p.collect(1, 0.0)
    assert 1 in p.cut_off
    # Cut off from THIS platform only; platforms are blind to each other (D12).
    assert p.request(1, 500.0) == 0.0
    assert p.request(2, 500.0) == 500.0


def test_exposure_excludes_the_checkout_instalment():
    """The platform's receivable is the three deferred instalments, not the full order.

    25% is taken at checkout, so financing R800 leaves the platform owed R600.
    """
    p = make_platform()
    p.request(1, 800.0)
    assert p.exposure(1) == pytest.approx(600.0)


def test_order_cap_truncates_the_request_and_is_counted():
    p = make_platform(order_cap=800.0, rolling_limit=100_000.0)
    assert p.request(1, 5_000.0) == pytest.approx(800.0)
    assert p.n_blocked_order_cap == 1
    # A request inside the cap is untouched.
    assert p.request(1, 500.0) == pytest.approx(500.0)
    assert p.n_blocked_order_cap == 1


def test_rolling_limit_is_measured_against_the_outstanding_receivable():
    """Available balance frees up as instalments are repaid, as a real facility does.

    Because 25% is taken at checkout, financing X raises the receivable by 0.75X, so
    the headroom a draw consumes is less than the amount financed.
    """
    p = make_platform(order_cap=15_000.0, rolling_limit=600.0)

    # Financing R800 leaves exactly R600 outstanding, which exhausts the limit.
    assert p.request(1, 800.0) == pytest.approx(800.0)
    assert p.exposure(1) == pytest.approx(600.0)
    assert p.available(1) == 0.0

    # Fully drawn, so the next request is refused outright.
    assert p.request(1, 100.0) == 0.0
    assert p.n_blocked_rolling_limit == 1

    # Repaying an instalment frees headroom again.
    p.collect(1, 200.0)
    assert p.available(1) == pytest.approx(200.0)
    # R200 of receivable headroom supports an order of 200 / 0.75.
    assert p.request(1, 1_000.0) == pytest.approx(200.0 / 0.75)


def test_rolling_limit_partially_fills_an_oversized_request():
    p = make_platform(order_cap=15_000.0, rolling_limit=600.0)
    p.request(1, 400.0)  # receivable 300, so 300 of headroom remains
    assert p.available(1) == pytest.approx(300.0)
    assert p.request(1, 10_000.0) == pytest.approx(400.0)  # 300 / 0.75
    assert p.n_blocked_rolling_limit == 1
    assert p.exposure(1) == pytest.approx(600.0)


def test_bnpl_charges_no_interest():
    """Zero interest is the product, and the basis on which it sits outside the NCA."""
    p = make_platform()
    p.request(1, 1000.0)
    total_paid = 0.0
    for _ in range(3):
        paid, _ = p.collect(1, 250.0)
        total_paid += paid
    # 250 at checkout is handled by the agent; the platform collects the other 750.
    assert total_paid == pytest.approx(750.0)


def test_partial_payment_rolls_shortfall_plus_fee_into_arrears():
    p = make_platform()
    p.request(1, 1000.0)
    paid, fees = p.collect(1, 100.0)
    assert paid == pytest.approx(100.0)
    assert fees == pytest.approx(190.0)
    # Owed 250, paid 100 -> 150 short, plus the R190 fee.
    assert p.loans[1][0].arrears == pytest.approx(340.0)
