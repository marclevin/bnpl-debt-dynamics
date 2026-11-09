"""Verification: the arrears-based distress rule (D18, issues #91 and #92).

A household is in default once its oldest unpaid instalment on any facility, traditional
or BNPL, is `k_default` ticks old (91+ days at k = 7). Payment friction is set to 1 or 0 to
make missing a payment deterministic.
"""

from __future__ import annotations

import warnings

import pytest

from simulation.bnpl import _age_unpaid
from simulation.config import ARREARS_RULE, CCMR_BANDS, load_ccmr_bands
from simulation.tests.lab import household

ARREARS = dict(distress_rule="arrears", bnpl_enabled=False)
#: A household that can always pay: ample income, one traditional loan.
ABLE = dict(income_tick=5000, committed_tick=1000, d_trad=10_000, service_tick=200, apr=0.0)


def _run(model, agent, friction_by_tick):
    """Step the model, setting payment friction tick by tick. Returns per-tick ages."""
    ages, defaulted = [], []
    for f in friction_by_tick:
        model.params = model.params.replace(payment_friction=f)
        model.step()
        ages.append(agent.arrears_age_max)
        defaulted.append(agent.defaulted)
    return ages, defaulted


def test_two_months_behind_then_catching_up_is_never_distressed():
    """The supervisor's example: four ticks (two months) in arrears, cured in month 3."""
    model, a = household(**ABLE, **ARREARS, n_ticks=10)
    ages, defaulted = _run(model, a, [1.0] * 4 + [0.0] * 4)
    assert ages[:4] == [1, 2, 3, 4]
    assert ages[4] == 0 and a.arrears_trad == 0
    assert not any(defaulted)


@pytest.mark.parametrize("k", [4, 7])
def test_default_falls_on_exactly_the_kth_tick_in_arrears(k):
    model, a = household(**ABLE, **ARREARS, k_default=k, n_ticks=12)
    ages, defaulted = _run(model, a, [1.0] * 10)
    assert defaulted.index(True) == k - 1  # the k-th tick in arrears, not the (k-1)-th
    assert ages[k - 1] == k


def test_a_friction_skip_followed_by_a_payment_is_never_distressed():
    model, a = household(**ABLE, **ARREARS)
    ages, defaulted = _run(model, a, [1.0, 0.0, 0.0])
    assert ages == [1, 0, 0]
    assert not any(defaulted)


def test_partial_payments_clear_the_oldest_arrears_first():
    unpaid = [[0, 100.0], [1, 100.0], [2, 100.0]]
    _age_unpaid(unpaid, paid=150.0, arrears_now=150.0 + 100.0, tick=3)
    # Tick 0 is cleared, half of tick 1 is left, and tick 3's instalment opens a bucket.
    assert unpaid == [[1, 50.0], [2, 100.0], [3, 100.0]]
    assert sum(x for _, x in unpaid) == pytest.approx(250.0)


def test_a_capped_amount_due_trims_the_newest_arrears():
    unpaid = [[0, 100.0], [1, 100.0]]
    _age_unpaid(unpaid, paid=0.0, arrears_now=150.0, tick=2)
    assert unpaid == [[0, 100.0], [1, 50.0]]


def test_unpaid_bnpl_alone_reaches_default_on_the_kth_tick(monkeypatch):
    """A household with no traditional debt still defaults on BNPL arrears (C1)."""
    model, a = household(income_tick=1000, committed_tick=1000, distress_rule="arrears",
                         shortfall_bnpl=False, n_ticks=10)
    monkeypatch.setattr(type(model.lender), "apply", lambda self, agent, amount: 0.0)
    model.platforms[0].request(a.agent_id, 400.0)  # no cash: every instalment goes unpaid
    defaulted = []
    for _ in range(8):
        model.step()
        defaulted.append(a.defaulted)
    assert a.d_trad == 0
    assert defaulted.index(True) == 6  # the oldest unpaid instalment is 7 ticks old


def test_bnpl_paid_late_within_the_threshold_is_not_default(monkeypatch):
    model, a = household(income_tick=1000, committed_tick=1000, distress_rule="arrears",
                         shortfall_bnpl=False, n_ticks=10)
    monkeypatch.setattr(type(model.lender), "apply", lambda self, agent, amount: 0.0)
    model.platforms[0].request(a.agent_id, 400.0)
    for _ in range(3):
        model.step()
    assert a.arrears_age_max == 3
    a.savings = 5_000.0  # the household catches up in the fourth tick
    model.step()
    assert a.arrears_age_max == 0 and not a.defaulted


def test_the_streak_rule_ignores_arrears_age():
    model, a = household(**ABLE, bnpl_enabled=False, distress_rule="streak", n_ticks=12)
    _, defaulted = _run(model, a, [1.0] * 10)
    # A friction skip is never distress under the old rule, however long it lasts.
    assert not any(defaulted)


def test_a_defaulted_account_is_non_performing_and_ages():
    model, a = household(**ABLE, **ARREARS, n_ticks=14)
    _run(model, a, [1.0] * 7)
    assert a.defaulted
    owed, balance = a.arrears_trad, a.d_trad
    _run(model, a, [0.0] * 3)  # the household could pay, but the account is handed over
    assert a.arrears_trad == owed and a.d_trad == balance
    assert a.arrears_age_max == 10


def test_write_off_removes_the_debt_and_keeps_the_default():
    model, a = household(**ABLE, **ARREARS, write_off_rate=1.0, n_ticks=10)
    _run(model, a, [1.0] * 7)
    assert a.defaulted and a.d_trad > 0  # written off from the next tick, not this one
    _run(model, a, [1.0])
    assert a.defaulted and a.d_trad == 0 and a.arrears_trad == 0 and a.arrears_age_max == 0


def test_arrears_persistence_one_keeps_a_household_behind():
    model, a = household(**ABLE, **ARREARS, arrears_persistence=1.0, n_ticks=10)
    ages, _ = _run(model, a, [1.0] + [0.0] * 3)
    assert ages == [1, 2, 3, 4]


def test_initial_arrears_reproduce_the_ccmr_profile_at_tick_zero():
    from simulation.model import BNPLModel
    from simulation.config import ParamSet
    from simulation.metrics import ccmr_band
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = BNPLModel(ParamSet(seed=3, bnpl_enabled=False, labour_flows=True, **ARREARS_RULE))
    active = [a for a in model.agents if a.d_trad > 0]
    shares = load_ccmr_bands()
    for label, _, _ in CCMR_BANDS:
        if label == "current":
            continue
        got = sum(ccmr_band(a.arrears_age_max) == label for a in active) / len(active)
        assert got == pytest.approx(shares[label] / 100, abs=0.001), label
    in_default = sum(a.arrears_age_max >= 7 for a in active)
    assert model.n_initial_defaults == in_default
    assert all(a.arrears_trad <= a.d_trad + 1e-9 for a in active)
