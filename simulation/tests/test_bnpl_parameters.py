"""Verification: the 2026-08-12 BNPL parameter and defect fixes.

Every test here is written so that the defect it covers WOULD HAVE FAILED IT. That is the
point: the 65-test suite missed all four of these, and in one case (B27) missed it because
the existing test asserted the wrong direction on the wrong quantity.

Covers:
  * B27  the cool-off off-by-one, which made the statutory 14-day arm a silent no-op
  * B28  want-driven purchases partly funded by cash the household did not have
  * B29  current-vintage nominal BNPL figures used unadjusted in a 2017-Rand model
  * B30  flat purchase size and flat platform limit replaced by household-relative rules
"""

from __future__ import annotations

import warnings

import pytest

from simulation import config
from simulation.bnpl import BNPLPlatform
from simulation.config import ParamSet
from simulation.model import BNPLModel

warnings.simplefilter("ignore", FutureWarning)

SMALL = dict(n_agents=400, n_ticks=16, burn_in=4)


def run(**kw):
    return BNPLModel(ParamSet(seed=7, **{**SMALL, **kw})).run()


def build(**kw) -> BNPLModel:
    return BNPLModel(ParamSet(seed=7, **{**SMALL, **kw}))


# ---------------------------------------------------------------------------
# B27: the cool-off off-by-one
# ---------------------------------------------------------------------------


def test_statutory_cool_off_strictly_reduces_want_driven_purchases():
    """k_cool=1 must BLOCK something. This is the test the suite did not have.

    `test_cool_off_cannot_increase_bnpl_volume` asserted only that volume does not rise,
    which a no-op satisfies trivially, and it asserted on VOLUME, which is confounded by
    the shortfall-driven path the cool-off deliberately does not block. The count of
    want-driven purchases is the quantity the lever actually acts on.
    """
    off = build(bnpl_enabled=True, q_base=0.5, k_cool=0)
    off.run()
    on = build(bnpl_enabled=True, q_base=0.5, k_cool=1)
    on.run()

    assert off.want_purchase_count > 0, "the arm under test must actually buy something"
    assert on.want_purchase_count < off.want_purchase_count, (
        "k_cool=1 is the CCA s.66A statutory 14-day arm and must block purchases; "
        "if it does not, the gate is off by one again (DEFECTS.md B27)"
    )


def test_cool_off_blocks_for_exactly_k_ticks():
    """k_cool=n blocks the next n ticks, so a longer cool-off cannot buy more."""
    counts = []
    for k in (0, 1, 2, 4):
        m = build(bnpl_enabled=True, q_base=0.5, k_cool=k)
        m.run()
        counts.append(m.want_purchase_count)
    assert counts == sorted(counts, reverse=True), (
        f"want-driven purchase count must be monotonically non-increasing in k_cool: {counts}"
    )


# ---------------------------------------------------------------------------
# B28: the checkout debit must clear
# ---------------------------------------------------------------------------


def test_a_household_with_no_cash_cannot_make_a_want_driven_purchase():
    """Both SA providers debit a card at checkout and decline if it fails.

    Before the fix the checkout instalment was subtracted without a balance check and the
    resulting negative cash was floored to zero at the state update, so a household with
    R0 could buy and 'pay' the 25% out of nothing.
    """
    m = build(bnpl_enabled=True, q_base=1.0, beta=0.0)
    agent = next(iter(m.agents))
    assert agent._bnpl_purchase(0.0) == 0.0
    assert agent._bnpl_purchase(-50.0) == 0.0


def test_checkout_payment_never_exceeds_available_cash():
    """The returned checkout payment is what the household is about to spend."""
    m = build(bnpl_enabled=True, q_base=1.0, beta=0.0)
    eligible = [a for a in m.agents if a.bnpl_eligible]
    assert eligible, "the arm under test must have eligible households"
    for agent in eligible[:50]:
        for cash in (1.0, 25.0, 400.0):
            paid = agent._bnpl_purchase(cash)
            assert paid <= cash + 1e-9, (
                f"checkout payment {paid} exceeds available cash {cash}: the household "
                "is spending money it does not have (DEFECTS.md B28)"
            )


def test_savings_are_never_driven_negative_by_a_purchase():
    """The guard, at population scale and through a full run.

    `savings` is floored at zero in the state update, so a leak cannot be seen there.
    This checks the invariant the floor was hiding: cash after the purchase step is
    already non-negative.
    """
    m = build(bnpl_enabled=True, q_base=0.8, beta=2.0)
    m.run()
    assert all(a.savings >= 0.0 for a in m.agents)


# ---------------------------------------------------------------------------
# B29: 2017 Rands
# ---------------------------------------------------------------------------


def test_bnpl_money_parameters_are_denominated_in_2017_rands():
    """The Payflex figures are published at current vintage; the model is 2017.

    Using them unadjusted denominated the BNPL side of the model ~1.4x too high against
    the NIDS backbone, the Reg 23A table and the CCMR targets.
    """
    p = ParamSet()
    factor = config.load_cpi_factors()[config.PAYFLEX_TERMS_VINTAGE]
    assert factor > 1.0, "the deflator must actually deflate"

    assert p.bnpl_order_cap == pytest.approx(
        config.PAYFLEX_ORDER_CAP_NOMINAL / factor, rel=1e-3
    )
    assert p.bnpl_late_fee_per_tick == pytest.approx(
        config.PAYFLEX_LATE_FEE_PER_TICK_NOMINAL / factor, rel=1e-3
    )
    assert p.bnpl_late_fee_cap == pytest.approx(
        config.PAYFLEX_LATE_FEE_CAP_NOMINAL / factor, rel=1e-3
    )
    # The relationship the product terms specify -- three weeks at R95 -- must survive
    # deflation, or the cap and the per-tick fee have drifted apart.
    assert p.bnpl_late_fee_cap == pytest.approx(p.bnpl_late_fee_per_tick * 1.5, rel=1e-3)


def test_deflator_round_trips():
    factors = config.load_cpi_factors()
    assert factors[2017] == pytest.approx(1.0)
    for year in (2024, 2025, 2026):
        assert config.to_2017_rands(1000.0 * factors[year], year) == pytest.approx(1000.0)
    # Monotone: prices rose in every year of the window.
    years = sorted(factors)
    assert all(factors[a] < factors[b] for a, b in zip(years, years[1:]))


# ---------------------------------------------------------------------------
# B30: household-relative purchase size and platform limit
# ---------------------------------------------------------------------------


def test_purchase_size_is_proportional_to_the_household_budget():
    """The mean draw must be kappa x the household's OWN monthly budget.

    Limits and caps are opened wide so the draw is what is being measured rather than the
    truncation. The draw is lognormal, so this asserts on the mean of many draws.
    """
    m = build(
        bnpl_enabled=True,
        bnpl_limit_income_multiple=1e6,
        bnpl_order_cap=1e12,
        n_agents=400,
    )
    ratio = m.params.bnpl_purchase_ratio
    assert ratio == pytest.approx(config.BNPL_PURCHASE_SHARE_OF_DISCRETIONARY)

    # Two households with materially different budgets, to check proportionality and not
    # merely the level.
    eligible = sorted(
        (a for a in m.agents if a.bnpl_eligible and a.rec.discretionary_monthly > 0),
        key=lambda a: a.rec.discretionary_monthly,
    )
    lean, rich = eligible[len(eligible) // 10], eligible[-len(eligible) // 10]
    assert rich.rec.discretionary_monthly > 2 * lean.rec.discretionary_monthly

    for agent in (lean, rich):
        assert agent._purchase_scale() == pytest.approx(agent.rec.discretionary_monthly)
        before_n, before_v = m.want_purchase_count, m.want_purchase_value
        for _ in range(3000):
            # Cash far above any plausible draw, so the checkout guard cannot truncate.
            agent._bnpl_purchase(1e9)
        drawn = (m.want_purchase_value - before_v) / (m.want_purchase_count - before_n)
        expected = ratio * agent.rec.discretionary_monthly
        assert drawn == pytest.approx(expected, rel=0.08), (
            f"mean draw R{drawn:,.0f} against kappa x budget R{expected:,.0f}"
        )


def test_purchase_base_switches_the_budget_the_purchase_is_sized_against():
    m_disc = build(bnpl_enabled=True, bnpl_purchase_base="discretionary")
    m_inc = build(bnpl_enabled=True, bnpl_purchase_base="income")
    a_disc = next(iter(m_disc.agents))
    a_inc = next(iter(m_inc.agents))
    assert a_disc._purchase_scale() == pytest.approx(a_disc.rec.discretionary_monthly)
    assert a_inc._purchase_scale() == pytest.approx(a_inc.income_monthly)


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Realised R629 against the R992 anchor since P0 stopped counting imputed rentals "
        "as discretionary spending (2026-08-18). The two means are taken over different "
        "populations: R992 is a provider's own customers, which kappa puts at about "
        "R7,151 monthly discretionary -- the Q4/Q5 boundary, and above 80% of banked "
        "agents -- while the model averages over adopters in every quintile. Banked Q4 "
        "alone gives R613 and Q5 R2,186. Resolving it means choosing the comparison "
        "population, which is a design decision, not a tolerance. DELETE this marker when "
        "that is settled -- strict=True fails the suite if it starts passing regardless."
    ),
)
def test_realised_mean_purchase_lands_near_the_sa_provider_anchor():
    """THE validation check the new rule buys.

    kappa comes from Stats SA IES 2022/23 expenditure microdata. The target comes from a
    listed issuer's disclosed cumulative BNPL GMV and transaction count, deflated to 2017
    Rands. The two are wholly independent, and nothing is fitted to anything: if they
    disagree, the rule is wrong.
    """
    m = build(bnpl_enabled=True, q_base=0.3, beta=0.0, n_agents=2000, n_ticks=20)
    m.run()
    anchor = config.load_bnpl_anchors()["model_target"]["mean_purchase_2017_rands"]
    realised = m.want_purchase_value / m.want_purchase_count

    assert m.want_purchase_count > 500
    assert realised == pytest.approx(anchor, rel=0.35), (
        f"realised mean purchase R{realised:,.0f} against the SA provider anchor of "
        f"R{anchor:,.0f}. This check is UNFITTED; a failure means the IES budget share "
        "and the provider disclosure disagree, which is a finding, not a nuisance."
    )


def test_shortfall_path_puts_no_more_on_bnpl_than_the_financeable_budget():
    """D5: BNPL finances retail goods, so it relieves a shortfall only up to kappa x budget.

    The uncapped arm is the working-run behaviour and must still exceed the cap, or the
    robustness comparison in experiments.py compares a rule with itself.
    """
    drawn = {}
    for capped in (True, False):
        m = build(bnpl_enabled=True, shortfall_bnpl_capped=capped)
        a = next(x for x in m.agents if x.bnpl_eligible and x._purchase_scale() > 0)
        cap = m.params.bnpl_purchase_ratio * a._purchase_scale()
        a._seek_credit(cap * 50)
        drawn[capped] = a.bnpl_volume_tick
    assert 0 < drawn[True] <= cap + 1e-9
    assert drawn[False] > cap


def test_rolling_limit_is_per_household_and_proportional_to_income():
    m = build(bnpl_enabled=True, bnpl_limit_income_multiple=0.25)
    platform = m.platforms[0]
    for agent in list(m.agents)[:25]:
        assert platform.limit_for(agent.agent_id) == pytest.approx(
            0.25 * agent.income_monthly
        )
    # Every platform sees the same household limit: they are blind to each other (D12),
    # not differently informed about the customer.
    other = m.platforms[-1]
    a = next(iter(m.agents))
    assert platform.limit_for(a.agent_id) == other.limit_for(a.agent_id)


def test_a_flat_limit_is_no_longer_imposed_on_unequal_households():
    """The defect in one line: the old constant was 217% of Q1 median monthly income."""
    m = build(bnpl_enabled=True)
    platform = m.platforms[0]
    limits = {a.agent_id: platform.limit_for(a.agent_id) for a in m.agents}
    assert len(set(round(v, 2) for v in limits.values())) > 100, (
        "the rolling limit must vary across households; a near-constant limit means the "
        "per-household wiring is not reaching the platform"
    )


def test_rolling_limit_binds_harder_at_the_bottom_of_the_distribution():
    """A limit that scales with income must bite where income is lowest.

    Reported by quintile precisely because an aggregate binding rate can read as inert
    while the constraint is binding hard on Q1.
    """
    summary = run(bnpl_enabled=True, q_base=0.5, beta=1.0, n_agents=2000, n_ticks=24)
    q1 = summary["bnpl_rolling_bind_Q1"]
    q5 = summary["bnpl_rolling_bind_Q5"]
    assert q1 > q5, f"expected the rolling limit to bind harder on Q1 than Q5: {q1} vs {q5}"


def test_platform_falls_back_to_its_default_limit_when_no_household_limit_is_set():
    """Unit-level construction must stay well defined; the model always sets limits."""
    p = BNPLPlatform(
        platform_id=0,
        order_cap=10_000.0,
        rolling_limit=600.0,
        late_fee_per_tick=130.0,
        late_fee_cap=195.0,
        n_instalments=4,
    )
    assert p.limit_for(99) == 600.0
    p.rolling_limits[99] = 1_200.0
    assert p.limit_for(99) == 1_200.0
