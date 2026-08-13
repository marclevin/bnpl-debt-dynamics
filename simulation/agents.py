"""The household agent: the seven-step tick.

Ordering is specified in 04_design.tex and D0, and the order itself is a modelling
decision. Two features carry the mechanism:

  * Committed expenditure is paid BEFORE debt service. Madeira's default condition is
    the failure to finance minimum consumption, which is only coherent if consumption has
    priority; servicing first would make default impossible by construction.
  * Borrowing happens LAST, so a household can borrow in order to service existing debt.
    That is the financial self-reinforcing loop. The social loop enters at step 6.
"""

from __future__ import annotations

import math

from mesa import Agent

from .affordability import nca_max_service, tick_interest_rate
from .config import MONTHLY_TO_TICK
from .lender import NEW_LOAN_APR, NEW_LOAN_TERM_MONTHS
from .population import HouseholdRecord


class HouseholdAgent(Agent):
    """One NIDS Wave 5 household carried into the model with a balance sheet."""

    def __init__(self, model, record: HouseholdRecord, is_min_payer: bool, bnpl_eligible: bool):
        super().__init__(model)
        self.rec = record
        self.agent_id = record.agent_id

        # -- balance sheet (2017 Rands) -----------------------------------------
        self.d_trad = record.d_trad
        self.savings = record.liquid_savings
        self.scheduled_service_tick = record.scheduled_service_tick
        self.arrears_trad = 0.0

        # -- static attributes ---------------------------------------------------
        self.income_monthly = record.income_monthly
        self.is_min_payer = is_min_payer
        self.bnpl_eligible = bnpl_eligible
        self.is_wage_household = record.income_source == "WAGE"
        self.reference_group = record.reference_group

        # -- state ---------------------------------------------------------------
        self.distress_streak = 0
        self.arrears_age_ticks = 0
        self.defaulted = False
        self.cool_off_until = -1
        #: D1: how many of the household's earners are currently out of work.
        self.n_unemployed = 0

        # D17 threshold mechanism: this household's personal tipping point, fixed for
        # life (Granovetter 1978). Drawn ONLY under the threshold mechanism, so the
        # linear arm's random stream is byte-for-byte what it was before this existed.
        # Clamped to [0,1] rather than resampled, and that is faithful rather than lazy:
        # the point mass at 0 is Granovetter's INSTIGATORS, who act with no peers at all
        # and are what seeds a cascade, and the mass at 1 is households social influence
        # can never reach. Resampling would delete both groups.
        # Drawn from `init_rng`, NOT the simulation stream, so that `gamma = 0`
        # reproduces the linear control bitwise and a `sigma_theta` sweep is paired.
        self.theta = 0.0
        if model.params.peer_mechanism == "threshold":
            p = model.params
            self.theta = min(max(model.init_rng.gauss(p.mu_theta, p.sigma_theta), 0.0), 1.0)

        # -- per-tick accumulators, read by the collector -------------------------
        self.interest_charged_tick = 0.0
        self.bnpl_fees_tick = 0.0
        self.bnpl_volume_tick = 0.0
        self.shocked_tick = False

    # ------------------------------------------------------------------ helpers
    @property
    def income_tick(self) -> float:
        return self.rec.income_tick

    @property
    def committed_tick(self) -> float:
        return self.rec.committed_tick

    def bnpl_due_per_tick(self) -> float:
        return sum(p.due(self.agent_id) for p in self.model.platforms)

    def bnpl_outstanding(self) -> float:
        return sum(p.exposure(self.agent_id) for p in self.model.platforms)

    def stacking_depth(self) -> int:
        return sum(1 for p in self.model.platforms if p.has_balance(self.agent_id))

    def total_debt(self) -> float:
        return self.d_trad + self.arrears_trad + self.bnpl_outstanding()

    def minimum_payment_tick(self) -> float:
        """D6 contractual minimum. ASSUMPTION: the register never defined this.

        `max(interest accrued, min_payment_frac of balance)`. The interest floor rules
        out negative amortisation by construction; the fraction is the assumed part.
        """
        p = self.model.params
        interest = self.d_trad * tick_interest_rate(self.rec.apr_annual)
        pct = self.d_trad * p.min_payment_frac * MONTHLY_TO_TICK
        return min(max(interest, pct), self.d_trad + interest)

    # -------------------------------------------------------------------- step
    def step(self) -> None:
        p = self.model.params
        self.interest_charged_tick = 0.0
        self.bnpl_fees_tick = 0.0
        self.bnpl_volume_tick = 0.0
        self.shocked_tick = False

        # --- 1. income arrives, subject to the shock ---------------------------
        # D1: the shock is a separation from employment, so the household loses its
        # WAGE COMPONENT. The magnitude is observed (w5_hhwage), not a parameter.
        # Grant-dependent households are exempt: SA social grants are statutory
        # transfers and do not vary with employment.
        # The hazard applies PER EARNER, so `p` is an individual separation rate directly
        # comparable to the QLFS figure, and a multi-earner household correctly faces a
        # higher chance that someone loses work. Losing one of two earners costs half the
        # wage component, which is what puts households in the mild arrears bands.
        income = self.income_tick
        n_earners = self.rec.n_earners
        if self.is_wage_household and n_earners > 0:
            rng = self.model.rng
            if p.shock_persistent:
                # Re-employment first, at the QLFS unemployed->employed hazard, so an
                # earner who separates this tick cannot also recover in it.
                for _ in range(self.n_unemployed):
                    if rng.random() < p.shock_exit_prob:
                        self.n_unemployed -= 1
                for _ in range(n_earners - self.n_unemployed):
                    if rng.random() < p.shock_prob:
                        self.n_unemployed += 1
                lost = self.n_unemployed
            else:
                # D1 as originally written: a single-tick, non-persistent shock.
                lost = sum(1 for _ in range(n_earners) if rng.random() < p.shock_prob)

            self.shocked_tick = lost > 0
            if lost:
                income -= self.rec.income_wage_tick * (lost / n_earners)
        income = max(income, 0.0)

        cash = self.savings + income

        # --- 2. committed expenditure is paid FIRST ----------------------------
        committed = self.committed_tick
        cash -= committed
        committed_shortfall = -cash if cash < 0 else 0.0
        if cash < 0:
            cash = 0.0

        # --- 3. scheduled debt service is attempted ----------------------------
        # Interest accrues on the traditional balance before servicing.
        interest = self.d_trad * tick_interest_rate(self.rec.apr_annual)
        self.d_trad += interest
        self.interest_charged_tick = interest

        due_trad = (
            self.minimum_payment_tick() if self.is_min_payer else self.scheduled_service_tick
        )
        due_trad = min(due_trad, self.d_trad) + self.arrears_trad
        bnpl_due = self.bnpl_due_per_tick()

        service_shortfall = max(due_trad + bnpl_due - cash, 0.0)

        # --- 5 (first pass). Seek credit when short at step 2 or 3 -------------
        # Borrowing sits at step 5 in the specification but must resolve before the
        # payments it funds are made. The trigger is the realised shortfall from steps
        # 2 and 3, which is exactly what D3 and D4 specify.
        shortfall = committed_shortfall + service_shortfall
        if shortfall > 0 and not self.defaulted:
            cash += self._seek_credit(shortfall)

        # --- D7 distress is assessed HERE, after credit ------------------------
        # "Income plus available credit cannot cover committed expenditure plus
        # scheduled debt service." Assessed before payment friction below, so a household
        # that skips a payment through present bias is NOT counted as cash-flow insolvent.
        # Friction must move arrears without moving default.
        unmet_after_credit = max(due_trad + bnpl_due - cash, 0.0)
        distressed = committed_shortfall > 0 or unmet_after_credit > 0

        # --- pay BNPL, then traditional --------------------------------------
        # BNPL first: its instalments are contractually fixed and the platform debits a
        # card automatically, whereas the traditional lender tolerates arrears.
        for platform in self.model.platforms:
            paid, fees = platform.collect(self.agent_id, cash)
            cash -= paid
            self.bnpl_fees_tick += fees

        # D6 payment friction: present-biased borrowers fail to execute planned paydown
        # (Kuchler & Pagel). Traditional debt only, because BNPL auto-debits a card, so
        # inattention cannot stop a BNPL instalment. This is what generates transient
        # mild delinquency: a household misses one instalment and catches up next tick.
        skipped_payment = self.model.rng.random() < p.payment_friction
        paid_trad = 0.0 if skipped_payment else min(cash, due_trad)
        cash -= paid_trad
        self.arrears_trad = max(due_trad - paid_trad, 0.0)
        principal = max(paid_trad - interest, 0.0)
        self.d_trad = max(self.d_trad - principal, 0.0)

        # --- 4. discretionary consumption is set ------------------------------
        # Compressible to zero (D2): a household compresses discretionary spending fully
        # before missing an instalment, which is why this follows servicing.
        target = self.rec.discretionary_tick
        floor = target * p.discretionary_floor
        cash = max(cash, 0.0)
        # Wants `target`, can afford `cash`, and will not cut below `floor` unless cash
        # is short of it. With the baseline floor of 0 this is simply min(cash, target).
        spend = min(max(floor, min(cash, target)), cash)
        cash -= spend

        # --- 6. want-driven BNPL, using the LAGGED group adoption share --------
        # The cool-off gate is STRICT (`>`), not `>=`. With `>=` a purchase at tick t
        # setting cool_off_until = t + k_cool re-opened the gate at t + k_cool, so
        # k_cool = 1 -- the statutory 14-day arm -- blocked nothing at all, because a
        # household could not purchase twice within one tick anyway (DEFECTS.md B27).
        if (
            p.bnpl_enabled
            and self.bnpl_eligible
            and not self.defaulted
            and self.model.tick > self.cool_off_until
        ):
            s_g = self.model.group_share_lagged.get(self.reference_group, 0.0)
            q = self._appetite(s_g)
            if self.model.rng.random() < q:
                cash -= self._bnpl_purchase(cash)

        # --- 7. state updates --------------------------------------------------
        self.savings = max(cash, 0.0)

        # D7: cash-flow insolvency, computed above before payment friction was applied.
        if distressed:
            self.distress_streak += 1
        else:
            self.distress_streak = 0

        if self.arrears_trad > 0:
            self.arrears_age_ticks += 1
        else:
            self.arrears_age_ticks = 0

        if not self.defaulted and self.distress_streak >= p.k_default:
            self.defaulted = True
            self.model.bureau.record_default(self.agent_id)

    # ------------------------------------------------------------ peer influence
    def _appetite(self, s_g: float) -> float:
        """D17: want-driven BNPL propensity, given the lagged group adoption share.

        Two mechanisms, both with a control arm that recovers the independent-agent
        model exactly, and both reading the SAME lagged share so neither is sensitive to
        activation order.

        **linear** — `q = q_base + beta * s_g`. Every household responds identically and
        smoothly. `beta = 0` switches the channel off.

        **threshold** — Granovetter (1978). The household ignores its peers entirely
        until the group's usage crosses its own fixed tipping point `theta_i`, then
        steps up by `gamma`. `gamma = 0` switches the channel off.

        The two are structurally distinct in the way that matters for RQ2: linear
        coupling cannot produce a tipping point in adoption at any parameter value,
        whereas a spread of thresholds can, because there is always another household
        just above the current level waiting to be triggered.
        """
        p = self.model.params
        if p.peer_mechanism == "threshold":
            q = p.q_base + (p.gamma if s_g >= self.theta else 0.0)
        else:
            q = p.q_base + p.beta * s_g
        return min(max(q, 0.0), 1.0)

    # --------------------------------------------------------------- borrowing
    def _requested_amount(self, shortfall: float) -> float:
        """D4: how much to ask for. ASSUMPTION with no anchor; mandatory sensitivity."""
        rule = self.model.params.amount_rule
        if rule == "shortfall_125":
            return shortfall * 1.25
        if rule == "shortfall_plus_committed":
            return shortfall + self.committed_tick
        return shortfall

    def _seek_credit(self, shortfall: float) -> float:
        """D5: BNPL-first where BNPL exists and the household is eligible.

        Returns the NET cash raised. Traditional credit covers what BNPL cannot, and is
        the only channel in the no-BNPL baseline. Cost-ranking is deliberately not used:
        the evidence attributes the choice to convenience and social norm, not price.
        """
        p = self.model.params
        amount = self._requested_amount(shortfall)
        covered = 0.0  # spending need met, by either channel
        net_cash = 0.0  # cash actually freed up

        if p.bnpl_enabled and self.bnpl_eligible:
            financed = self._bnpl_draw(amount)
            covered += financed
            # BNPL defers 75% of the cost: 25% is debited at checkout (D13), so the net
            # cash relief this tick is three quarters of the amount financed.
            net_cash += financed * (1.0 - 1.0 / p.bnpl_instalments)

        remaining = amount - covered
        if remaining > 0:
            # A traditional loan is drawn down in full as cash.
            net_cash += self.model.lender.apply(self, remaining)

        return net_cash

    def _purchase_scale(self) -> float:
        """The household's own monthly budget that a BNPL purchase is sized against (D4).

        A flat national purchase size was the model's single largest driver of output
        and its worst-sourced input (DEFECTS.md B24). It was also indefensible on its own
        terms: R1,568 imposed uniformly is 127% of the median banked Q1 household's
        monthly discretionary spend and 5.8% of Q5's. A population with a Gini of 0.67
        cannot share one purchase size.
        """
        if self.model.params.bnpl_purchase_base == "income":
            return self.income_monthly
        return self.rec.discretionary_monthly

    def _bnpl_purchase(self, cash: float) -> float:
        """A want-driven discretionary BNPL purchase (D3, D4).

        Returns the checkout payment the household must fund this tick. The purchase is
        consumption, so unlike the shortfall path it frees no cash: it costs 25% now and
        creates an obligation for the remaining 75%.

        The purchase is drawn lognormally about `kappa x` the household's own monthly
        budget, so the MEAN is that product and the whole observed heterogeneity of the
        population is inherited rather than averaged away. `kappa` is derived from IES
        2022/23 (config.BNPL_PURCHASE_SHARE_OF_DISCRETIONARY), so the population mean
        purchase is free to be checked against the SA provider disclosure rather than
        being set by it.

        THE CHECKOUT DEBIT MUST CLEAR. Both SA providers debit a card at checkout and
        decline if it fails, so a household cannot buy what it cannot fund the first
        instalment of. Until DEFECTS.md B28 this was unenforced: the checkout payment was
        subtracted without a balance check and the resulting negative cash was silently
        floored to zero at the state update, so purchases were partly funded by money
        that did not exist -- worst exactly where purchase size was least plausible.
        """
        p = self.model.params
        if cash <= 0.0:
            return 0.0

        scale = self._purchase_scale()
        if scale <= 0.0:
            return 0.0

        sigma = math.sqrt(math.log(1.0 + p.bnpl_purchase_cv**2))
        mu = math.log(p.bnpl_purchase_ratio * scale) - 0.5 * sigma**2
        amount = math.exp(self.model.rng.gauss(mu, sigma))

        # The largest order whose checkout instalment the household can actually pay.
        amount = min(amount, cash * p.bnpl_instalments)

        financed = self._bnpl_draw(amount)
        if financed <= 0:
            return 0.0

        self.model.record_want_purchase(financed)
        if p.k_cool > 0:
            self.cool_off_until = self.model.tick + p.k_cool
        return financed / p.bnpl_instalments

    def _bnpl_draw(self, amount: float) -> float:
        """Route a BNPL request across platforms that cannot see one another (D12).

        Returns the gross amount financed. Cash effects are the caller's business, since
        they differ between the shortfall path and the want-driven path.
        """
        p = self.model.params
        if amount <= 0:
            return 0.0

        if p.stacking_cap is not None and self.stacking_depth() >= p.stacking_cap:
            return 0.0

        # A single purchase can be spread across platforms, so the cap has to constrain
        # the routing as well as the entry: checking depth only on the way in would let
        # one draw open several facilities at once and overshoot the cap.
        headroom = (
            p.stacking_cap - self.stacking_depth() if p.stacking_cap is not None else None
        )

        # Lever 2: apply the D9 residual-income test to BNPL as well. Off by default —
        # its absence is precisely what BNPL routes around.
        if p.bnpl_affordability_check:
            capacity = nca_max_service(self.income_monthly)
            visible = (self.scheduled_service_tick + self.bnpl_due_per_tick()) / MONTHLY_TO_TICK
            new_instalment = (amount / p.bnpl_instalments) / MONTHLY_TO_TICK
            if new_instalment > max(capacity - visible, 0.0):
                return 0.0

        order = list(self.model.platforms)
        self.model.rng.shuffle(order)

        financed = 0.0
        opened = 0
        for platform in order:
            if financed >= amount:
                break
            is_new = not platform.has_balance(self.agent_id)
            if is_new and headroom is not None and opened >= headroom:
                continue
            got = platform.request(self.agent_id, amount - financed)
            if got > 0:
                financed += got
                if is_new:
                    opened += 1

        self.bnpl_volume_tick += financed
        return financed
