"""Verification: the NCA Reg 23A gate and the debt pricing.

Verification is "did I build the model I specified", as distinct from validation,
"does the model behave like the world". These are verification tests only.
"""

from __future__ import annotations

import pytest

from simulation.affordability import (
    NCA_WORKED_EXAMPLES,
    amortised_instalment,
    nca_gate,
    nca_max_service,
    nca_necessary_expenses,
)


@pytest.mark.parametrize("income,expected", NCA_WORKED_EXAMPLES)
def test_reg23a_reproduces_published_worked_examples(income, expected):
    """GN R202 GG 38557 publishes two worked examples; both must reproduce exactly.

    R2,000 -> R881.00 and R10,000 -> R1,505.38. Asserted in P2 as well, so this test
    also protects the population construction from silent drift.
    """
    assert round(nca_necessary_expenses(income), 2) == expected


def test_reg23a_ceiling_is_income_varying_not_a_flat_dsti():
    """The NCA prescribes no DSTI ratio; the implied ceiling must vary with income.

    Documented values at the quintile bounds: 10.4% of income at R900, 83.2% at R7,712.
    A flat cap would be wildly over-permissive at the bottom of the distribution.
    """
    low = nca_max_service(900) / 900
    high = nca_max_service(7712) / 7712
    assert round(low, 3) == pytest.approx(0.104, abs=0.001)
    assert round(high, 3) == pytest.approx(0.832, abs=0.001)
    assert low < high


def test_reg23a_zero_and_negative_income():
    assert nca_necessary_expenses(0) == 0.0
    assert nca_necessary_expenses(-100) == 0.0
    assert nca_max_service(0) == 0.0


def test_gate_refuses_when_instalment_exceeds_residual_income():
    income = 3400.0
    capacity = nca_max_service(income)
    assert nca_gate(income, 0.0, capacity - 1)
    assert not nca_gate(income, 0.0, capacity + 1)


def test_gate_counts_existing_visible_obligations():
    """Existing visible debt consumes capacity — this is the D10 mechanism's hinge."""
    income = 7712.0
    capacity = nca_max_service(income)
    assert nca_gate(income, 0.0, capacity * 0.9)
    # The same application, once existing obligations are visible, must be refused.
    assert not nca_gate(income, capacity * 0.5, capacity * 0.9)


def test_amortisation_matches_closed_form():
    """R10,000 at 28% over 24 months."""
    pmt = amortised_instalment(10_000, 0.28, 24)
    r = 0.28 / 12
    expected = 10_000 * r / (1 - (1 + r) ** -24)
    assert pmt == pytest.approx(expected)
    # Total repaid must exceed principal at a positive rate.
    assert pmt * 24 > 10_000


def test_amortisation_degenerate_cases():
    assert amortised_instalment(0, 0.28, 24) == 0.0
    assert amortised_instalment(-5, 0.28, 24) == 0.0
    assert amortised_instalment(1200, 0.0, 12) == pytest.approx(100.0)
