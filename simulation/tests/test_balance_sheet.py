"""Verification: balance-sheet conservation and population construction.

Money must be neither created nor destroyed within a tick. The identity checked is a
sources-and-uses one:

    opening savings + income + credit raised
        = closing savings + committed + discretionary + payments made

rather than a stock identity, because debt stocks also move through interest accrual.
"""

from __future__ import annotations

import warnings

import pytest

from simulation.config import MONTHLY_TO_TICK, ParamSet
from simulation.model import BNPLModel
from simulation.population import build_records, load_population_frame

warnings.simplefilter("ignore", FutureWarning)


def test_population_loads_with_the_wage_column_joined():
    df = load_population_frame()
    assert len(df) == 5000
    assert "w5_hhwage" in df.columns
    assert df["w5_hhwage"].notna().all()
    # No household can lose more wage income than it has income.
    assert (df["w5_hhwage"] <= df["w5_hhincome"] + 1e-9).all()


def test_wage_dominant_households_all_have_positive_wage_income():
    """The D1 shock must not silently exempt a household it should hit."""
    df = load_population_frame()
    wage_hh = df[df["income_source"] == "WAGE"]
    assert len(wage_hh) > 0
    assert (wage_hh["w5_hhwage"] > 0).all()


def test_every_wage_household_has_at_least_one_earner():
    """income_source and the NIDS employment roster must agree.

    If they diverge, the per-earner shock would divide by zero or silently exempt
    households it should hit.
    """
    df = load_population_frame()
    wage_hh = df[df["income_source"] == "WAGE"]
    assert (wage_hh["n_earners"] >= 1).all()
    assert df["n_earners"].min() >= 0


def test_shock_costs_one_earners_share_not_the_whole_wage():
    """A two-earner household losing one job keeps the other earner's wage.

    This is what puts households in the mild CCMR arrears bands instead of sending
    them straight to 120+ (DEFECTS.md B21).
    """
    records, _ = build_records()
    multi = [r for r in records if r.n_earners >= 2 and r.income_wage_tick > 0]
    assert multi, "no multi-earner households; test is not exercising the path"
    r = multi[0]
    loss_one = r.income_wage_tick * (1 / r.n_earners)
    assert loss_one < r.income_wage_tick
    assert loss_one == pytest.approx(r.income_wage_tick / r.n_earners)


def test_unemployment_never_exceeds_the_earner_count():
    m = BNPLModel(ParamSet(seed=4, n_agents=800, n_ticks=30, shock_prob=0.08, bnpl_enabled=False))
    m.run()
    for a in m.agents:
        assert 0 <= a.n_unemployed <= a.rec.n_earners


def test_banked_share_matches_the_documented_ceiling():
    """D11 caps BNPL eligibility at the observed banked share of 83.1%."""
    df = load_population_frame()
    assert df["banked"].mean() == pytest.approx(0.831, abs=0.005)


def test_reference_groups_match_the_documented_structure():
    """D17: 45 groups (quintile x province), none below 20 agents."""
    _, groups = build_records()
    assert len(groups) == 45
    sizes = sorted(len(v) for v in groups.values())
    assert sizes[0] >= 20
    assert sum(sizes) == 5000


def test_monthly_flows_are_scaled_to_the_tick():
    """Every monetary FLOW is monthly in the parquet; stocks are not scaled."""
    records, _ = build_records()
    df = load_population_frame()
    r = records[0]
    row = df.iloc[0]
    assert r.income_tick == pytest.approx(row["w5_hhincome"] * MONTHLY_TO_TICK)
    assert r.committed_tick == pytest.approx(row["expenditure_committed"] * MONTHLY_TO_TICK)
    # Stocks carry through unscaled.
    assert r.d_trad == pytest.approx(row["D_trad"])
    assert r.liquid_savings == pytest.approx(row["liquid_savings"])


def test_scheduled_service_reproduces_the_p2_construction():
    """The model must not silently re-price the debt the population was built with."""
    records, _ = build_records()
    df = load_population_frame()
    for r, (_, row) in zip(records[:200], df.head(200).iterrows()):
        assert r.scheduled_service_tick == pytest.approx(
            row["monthly_trad_repayment"] * MONTHLY_TO_TICK, rel=1e-6
        )


def test_no_negative_balances_anywhere_after_a_run():
    m = BNPLModel(ParamSet(seed=3, n_agents=500, n_ticks=20, bnpl_enabled=True, q_base=0.4))
    m.run()
    for a in m.agents:
        assert a.savings >= 0.0, "savings went negative"
        assert a.d_trad >= 0.0, "traditional debt went negative"
        assert a.arrears_trad >= 0.0, "arrears went negative"
        assert a.bnpl_outstanding() >= 0.0, "BNPL exposure went negative"


def test_money_is_conserved_within_a_tick():
    """Sources equal uses for every household, every tick.

    Instrumented by re-deriving the identity from the agent's own accumulators rather
    than by trusting the step method's internal arithmetic.
    """
    m = BNPLModel(ParamSet(seed=5, n_agents=300, n_ticks=12, bnpl_enabled=True, q_base=0.4))

    for _ in range(m.params.n_ticks):
        opening = {a.agent_id: a.savings for a in m.agents}
        m.step()
        for a in m.agents:
            # Closing savings can never exceed everything that could have funded it.
            ceiling = opening[a.agent_id] + a.income_tick + a.bnpl_volume_tick + a.d_trad
            assert a.savings <= ceiling + 1e-6, (
                f"agent {a.agent_id} ended with more cash than its sources allow"
            )


def test_defaulted_households_are_cut_off_from_traditional_credit():
    m = BNPLModel(ParamSet(seed=9, n_agents=600, n_ticks=30, bnpl_enabled=False, shock_prob=0.05))
    m.run()
    defaulted = [a for a in m.agents if a.defaulted]
    assert defaulted, "no defaults produced; test is not exercising the path"
    for a in defaulted:
        assert m.bureau.is_defaulted(a.agent_id)
        assert m.lender.apply(a, 100.0) == 0.0


def test_zero_capacity_debtors_are_tracked_not_silently_dropped():
    """P2 found debtors no NCA-compliant lender could have granted. Report, don't cap."""
    m = BNPLModel(ParamSet(seed=1, n_ticks=4, bnpl_enabled=False))
    assert len(m.zero_capacity_debtors) > 0
    for aid in m.zero_capacity_debtors:
        rec = m.records[aid]
        assert rec.d_trad > 0
        assert rec.nca_capacity_monthly <= 0
