"""The model: environment, scheduler and observation.

Scheduling (D16) is synchronous at the level of the tick. Within a tick households act in
random asynchronous order reseeded each tick, then the lender processes, then state
updates and observation occur.

The peer channel (D17) is activation-order independent BY CONSTRUCTION, and that is a
payoff of the one-tick lag rather than an accident: `group_share_lagged` is computed once
per tick from end-of-previous-tick balances and is never written during the tick, so
every household sees the same already-settled share regardless of when it acts.
"""

from __future__ import annotations

import random

from mesa import Model

from .agents import HouseholdAgent
from .bnpl import BNPLPlatform
from .config import ParamSet
from .lender import CreditBureau, TraditionalLender
from .metrics import collect_tick, summarise_run
from .population import build_records, zero_capacity_debtors


class BNPLModel(Model):
    """A population of household agents, one traditional lender, and N BNPL platforms."""

    def __init__(self, params: ParamSet):
        super().__init__(seed=params.seed)
        self.params = params
        self.tick = 0

        # Mesa seeds `self.random`; use one explicit generator for every stochastic
        # draw so a run is reproducible from its seed alone.
        self.rng = random.Random(params.seed)

        records, groups = build_records(params.n_agents, seed=params.seed)
        self.records = records
        self.groups = groups
        self.zero_capacity_debtors = set(zero_capacity_debtors(records))

        # --- D11 eligibility: banked-only, then the access rate within that group ---
        banked = [r.agent_id for r in records if r.banked]
        n_eligible = int(round(params.bnpl_access_rate * len(banked)))
        eligible = set(self.rng.sample(banked, n_eligible)) if n_eligible else set()
        self.n_banked = len(banked)
        self.n_bnpl_eligible = len(eligible)

        # --- D6: the minimum-payer arm --------------------------------------------
        n_min = int(round(params.min_payer_share * len(records)))
        min_payers = set(self.rng.sample(range(len(records)), n_min)) if n_min else set()

        # --- entities ---------------------------------------------------------------
        self.bureau = CreditBureau(bnpl_visible=params.bnpl_bureau_visible)
        self.lender = TraditionalLender(self.bureau)
        self.platforms: list[BNPLPlatform] = [
            BNPLPlatform(
                platform_id=i,
                order_cap=params.bnpl_order_cap,
                rolling_limit=params.bnpl_platform_limit,
                late_fee_per_tick=params.bnpl_late_fee_per_tick,
                late_fee_cap=params.bnpl_late_fee_cap,
                n_instalments=params.bnpl_instalments,
            )
            for i in range(params.n_platforms if params.bnpl_enabled else 0)
        ]

        for rec in records:
            HouseholdAgent(
                self,
                rec,
                is_min_payer=rec.agent_id in min_payers,
                bnpl_eligible=rec.agent_id in eligible,
            )

        # D17: zero at t=0 everywhere, which is why q_base > 0 is structurally required.
        self.group_share_lagged: dict[tuple[str, str], float] = {g: 0.0 for g in groups}

        self.history: list[dict] = []

    # ------------------------------------------------------------------ scheduling
    def _activate(self) -> None:
        p = self.params
        if p.activation == "random":
            # Reseeded every tick, so no household holds a persistent first claim on
            # credit, which is rationed by the D9 gate and the per-platform limits.
            self.agents.shuffle_do("step")
        elif p.activation == "uniform":
            # Fixed order every tick — the artefact D16 warns about, kept as the
            # mandated robustness arm.
            for agent in sorted(self.agents, key=lambda a: a.agent_id):
                agent.step()
        elif p.activation == "synchronous":
            # Order still has to be serialised in a single-threaded model; what makes
            # this arm distinct is that it is deterministic and unshuffled.
            self.agents.do("step")
        else:  # pragma: no cover
            raise ValueError(f"unknown activation regime: {p.activation}")

    def step(self) -> None:
        self._activate()

        # State updates and observation occur after every household has acted.
        self.history.append(collect_tick(self))

        # Recompute the group adoption shares FOR THE NEXT TICK. This write happens
        # once, after the tick, which is what makes the peer channel independent of
        # activation order (D16/D17).
        self._recompute_group_shares()
        self.tick += 1

    def _recompute_group_shares(self) -> None:
        if not self.params.bnpl_enabled:
            # s_g is identically zero with BNPL disabled, so the peer channel is inert
            # in the baseline and the CCMR calibration is untouched.
            return
        holders = {g: 0 for g in self.groups}
        for agent in self.agents:
            if agent.bnpl_outstanding() > 0:
                holders[agent.reference_group] += 1
        self.group_share_lagged = {
            g: holders[g] / len(members) for g, members in self.groups.items()
        }

    # ----------------------------------------------------------------------- run
    def run(self) -> dict:
        """Run the full horizon and return the summarised result."""
        for _ in range(self.params.n_ticks):
            self.step()
        return summarise_run(self)
