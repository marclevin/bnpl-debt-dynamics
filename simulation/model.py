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

        # A SEPARATE stream for fixed agent endowments drawn at initialisation, so that
        # drawing them cannot shift the simulation's own stream. Two payoffs:
        #   * `gamma = 0` under the threshold mechanism reproduces the linear `beta = 0`
        #     control BITWISE, rather than merely in distribution;
        #   * sweeping `sigma_theta` changes only the thresholds, leaving every shock,
        #     purchase and friction draw identical, which makes the D17 dispersion sweep
        #     a PAIRED comparison instead of a noisy one.
        # Offset by a fixed prime so it cannot coincide with the main stream.
        self.init_rng = random.Random(params.seed + 999_983)

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

        # D17 denominator: how many members of each reference group COULD use BNPL.
        # See `_recompute_group_shares` for why this, and not group size, is the
        # denominator (DEFECTS.md B31).
        self.group_eligible: dict[tuple[str, str], int] = {
            g: sum(1 for i in members if i in eligible) for g, members in groups.items()
        }

        # --- D6: the minimum-payer arm --------------------------------------------
        n_min = int(round(params.min_payer_share * len(records)))
        min_payers = set(self.rng.sample(range(len(records)), n_min)) if n_min else set()

        # --- entities ---------------------------------------------------------------
        self.bureau = CreditBureau(bnpl_visible=params.bnpl_bureau_visible)
        self.lender = TraditionalLender(self.bureau)

        # D11: the rolling available balance is set PER HOUSEHOLD from monthly income,
        # which is what a light automated screen can infer from card activity. It is
        # deliberately NOT the Reg 23A capacity: that asymmetry with D9 is the mechanism
        # the thesis exists to study, and setting BNPL limits from statutory capacity
        # would quietly dissolve it.
        limits = {
            rec.agent_id: max(params.bnpl_limit_income_multiple * rec.income_monthly, 0.0)
            for rec in records
        }
        self.platforms: list[BNPLPlatform] = [
            BNPLPlatform(
                platform_id=i,
                order_cap=params.bnpl_order_cap,
                # Every household carries an explicit limit, so the fallback is unused
                # in a normal run; it exists so a platform is still well defined when
                # constructed directly in a unit test.
                rolling_limit=0.0,
                rolling_limits=dict(limits),
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

        # --- want-driven purchase counters ------------------------------------------
        # Two jobs. (1) The realised mean purchase is the VALIDATION quantity for the
        # new household-relative purchase rule: it is checked against the SA provider
        # disclosure rather than being set by it (bnpl_anchors_2017.json). (2) The
        # cool-off regression test needs a purchase COUNT, because cumulative volume is
        # confounded by the shortfall-driven path, which the cool-off deliberately does
        # not block -- asserting on volume is what let DEFECTS.md B27 through the suite.
        self.want_purchase_count = 0
        self.want_purchase_value = 0.0

        self.history: list[dict] = []

    def record_want_purchase(self, financed: float) -> None:
        """Record one want-driven BNPL origination (D3)."""
        self.want_purchase_count += 1
        self.want_purchase_value += financed

    # ------------------------------------------------------------------ scheduling
    def _activate(self) -> None:
        p = self.params
        if p.activation == "random":
            # Reseeded every tick, so no household holds a persistent first claim on
            # credit, which is rationed by the D9 gate and the per-platform limits.
            self.agents.shuffle_do("step")
        elif p.activation == "uniform":
            # Fixed order every tick — the artefact D16 warns about, kept as the
            # mandated robustness arm. A separate "synchronous" arm was removed: agents
            # are created in `agent_id` order, so an unshuffled sweep was this same
            # schedule and the two arms were bitwise identical.
            for agent in sorted(self.agents, key=lambda a: a.agent_id):
                agent.step()
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
        """The D17 peer signal: what share of my reference group is using BNPL.

        The denominator is the group's **BNPL-ELIGIBLE** members, not all its members
        (DEFECTS.md B31, resolved 2026-08-13 as Option A). Counting the unbanked and the
        ineligible in the denominator capped `s_g` at each group's eligible share, and
        that ceiling is proportional to `bnpl_access_rate` -- which is RQ2's own x-axis.
        Under linear coupling the effect is absorbed into `beta` and is harmless, but a
        Granovetter threshold is a fixed number compared against this signal: at 15%
        access nothing above `theta_i ~ 0.125` could ever fire, so sweeping access would
        also sweep the maximum attainable signal and produce a threshold-shaped response
        that is partly an artefact.

        Normalising also gives the quantity a cleaner reading -- "what share of the
        people who *could* use BNPL are using it" is closer to what a household observes
        than a share diluted by neighbours who have no bank card.

        ⚠ This changes the meaning of `beta`, so linear-arm results are not comparable
        across the change. Everything BNPL-on is being re-run regardless.
        """
        if not self.params.bnpl_enabled:
            # s_g is identically zero with BNPL disabled, so the peer channel is inert
            # in the baseline and the CCMR calibration is untouched.
            return
        holders = {g: 0 for g in self.groups}
        for agent in self.agents:
            if agent.bnpl_outstanding() > 0:
                holders[agent.reference_group] += 1
        # A group with no eligible members emits no signal. It cannot: nobody in it can
        # hold BNPL, so the numerator is zero too.
        self.group_share_lagged = {
            g: (holders[g] / n_elig) if (n_elig := self.group_eligible[g]) else 0.0
            for g in self.groups
        }

    # ----------------------------------------------------------------------- run
    def run(self) -> dict:
        """Run the full horizon and return the summarised result."""
        for _ in range(self.params.n_ticks):
            self.step()
        return summarise_run(self)
