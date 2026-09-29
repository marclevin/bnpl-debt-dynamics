"""One household with a hand-set balance sheet, for deterministic accounting tests.

The household sits inside an ordinary `BNPLModel`, so every rule it meets is the rule the
experiments run. Income shocks, payment friction and want-driven purchases are switched
off unless a test switches them on, which leaves platform routing as the only random
draw.
"""

from __future__ import annotations

import warnings
from dataclasses import replace

from simulation.config import MONTHLY_TO_TICK, ParamSet
from simulation.model import BNPLModel

warnings.simplefilter("ignore", FutureWarning)


def household(
    *,
    income_tick: float,
    committed_tick: float,
    discretionary_tick: float = 0.0,
    d_trad: float = 0.0,
    service_tick: float = 0.0,
    apr: float = 0.26,
    savings: float = 0.0,
    min_payer: bool = False,
    seed: int = 1,
    **params,
):
    """Return `(model, agent)` for a single household with the given finances."""
    base = dict(
        seed=seed,
        n_agents=1,
        n_ticks=8,
        burn_in=0,
        shock_prob=0.0,
        payment_friction=0.0,
        q_base=0.0,
        beta=0.0,
        bnpl_enabled=True,
        n_platforms=4,
    )
    base.update(params)
    model = BNPLModel(ParamSet(**base))
    agent = next(iter(model.agents))
    agent.rec = replace(
        agent.rec,
        income_source="GRANT",  # exempt from the income shock
        n_earners=0,
        income_tick=income_tick,
        income_wage_tick=0.0,
        committed_tick=committed_tick,
        discretionary_tick=discretionary_tick,
        discretionary_monthly=discretionary_tick / MONTHLY_TO_TICK,
        income_monthly=income_tick / MONTHLY_TO_TICK,
        banked=True,
    )
    agent.is_wage_household = False
    agent.income_monthly = income_tick / MONTHLY_TO_TICK
    agent.bnpl_eligible = base["bnpl_enabled"]
    agent.is_min_payer = min_payer
    agent.d_trad = d_trad
    agent.scheduled_service_tick = service_tick
    agent.apr_annual = apr
    agent.savings = savings
    limit = base.get("bnpl_limit_income_multiple", 0.10) * agent.income_monthly
    for platform in model.platforms:
        platform.rolling_limits[agent.agent_id] = limit
    return model, agent


def open_agreements(model, agent) -> list:
    """Every live BNPL agreement the household holds, across platforms."""
    return [
        loan for platform in model.platforms for loan in platform.loans.get(agent.agent_id, [])
    ]
