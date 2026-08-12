"""BNPL platform: the injected entity (D11-D13).

D11 eligibility is banked-only, because both major South African providers debit a bank
card at checkout. The screen is deliberately NOT the Reg 23A test — that asymmetry with
D9 is the mechanism, not an oversight.

D12: platforms cannot see one another. This FOLLOWS FROM D10 rather than being a fresh
assumption: with BNPL outside the NCA there is no shared reporting infrastructure through
which one platform could observe another's exposure. Stacking depth is therefore emergent.

D13: Pay in 4 on the Payflex schedule — 25% at checkout then 25% at each of the next
three ticks, which lands exactly on tick boundaries. Interest zero. Late fee R95/week
capped at three weeks (R190 per tick to a maximum of R285 per missed instalment).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BNPLLoan:
    """One Pay-in-4 facility on one platform."""

    principal: float
    instalment: float
    #: Instalments still to be collected after the checkout payment.
    remaining: int
    #: The single payable carried forward: unpaid instalments PLUS any fees charged.
    arrears: float = 0.0
    #: Cumulative late fees charged on this loan. Tracked only to enforce the D13 cap;
    #: it is not separately payable, having already been rolled into `arrears`.
    fee_accrued: float = 0.0

    @property
    def outstanding(self) -> float:
        return self.remaining * self.instalment + self.arrears

    @property
    def settled(self) -> bool:
        return self.remaining <= 0 and self.arrears <= 0


@dataclass(slots=True)
class BNPLPlatform:
    """One provider. Blind to every other platform (D12)."""

    platform_id: int
    order_cap: float
    rolling_limit: float
    late_fee_per_tick: float
    late_fee_cap: float
    n_instalments: int

    #: agent_id -> live loans on this platform.
    loans: dict[int, list[BNPLLoan]] = field(default_factory=dict)
    #: Households cut off after exhausting the fee cap. Still eligible elsewhere (D12).
    cut_off: set[int] = field(default_factory=set)

    # -- diagnostics for the D11 binding check --------------------------------
    n_requests: int = 0
    n_blocked_order_cap: int = 0
    n_blocked_rolling_limit: int = 0
    n_blocked_cut_off: int = 0
    n_originated: int = 0

    def exposure(self, agent_id: int) -> float:
        """Outstanding receivable: what the household still owes this platform."""
        return sum(loan.outstanding for loan in self.loans.get(agent_id, ()))

    def available(self, agent_id: int) -> float:
        """Headroom in RECEIVABLE terms, which is what the limit caps."""
        return max(self.rolling_limit - self.exposure(agent_id), 0.0)

    def max_order(self, agent_id: int) -> float:
        """Largest order whose receivable still fits the rolling limit.

        The checkout instalment is paid immediately and so never becomes a receivable:
        an order of X raises exposure by only X*(n-1)/n. Truncating the order directly
        against receivable headroom would mix the two units and under-lend.
        """
        deferred_share = (self.n_instalments - 1) / self.n_instalments
        if deferred_share <= 0:  # pragma: no cover - pay-in-1 is not a BNPL product
            return float("inf")
        return self.available(agent_id) / deferred_share

    def request(self, agent_id: int, amount: float) -> float:
        """Attempt to originate a purchase. Returns the amount financed (0.0 if refused).

        The screen is light by design (D11): a per-order cap and a rolling available
        balance. No residual-income test unless lever 2 is active, and that check is
        applied by the household before it gets here, not by the platform.
        """
        self.n_requests += 1

        if agent_id in self.cut_off:
            self.n_blocked_cut_off += 1
            return 0.0
        if amount > self.order_cap:
            self.n_blocked_order_cap += 1
            amount = self.order_cap
        ceiling = self.max_order(agent_id)
        if amount > ceiling:
            self.n_blocked_rolling_limit += 1
            amount = ceiling
        if amount <= 0:
            return 0.0

        instalment = amount / self.n_instalments
        self.loans.setdefault(agent_id, []).append(
            BNPLLoan(
                principal=amount,
                instalment=instalment,
                # 25% is paid at checkout, so three instalments remain.
                remaining=self.n_instalments - 1,
            )
        )
        self.n_originated += 1
        return amount

    def due(self, agent_id: int) -> float:
        """Amount falling due this tick: one instalment per live loan, plus arrears."""
        total = 0.0
        for loan in self.loans.get(agent_id, ()):
            if loan.remaining > 0:
                total += loan.instalment
            total += loan.arrears
        return total

    def collect(self, agent_id: int, available_cash: float) -> tuple[float, float]:
        """Collect what the household can pay this tick.

        Returns (paid, fees_charged). An unpaid instalment accrues the Payflex late fee
        at R190 per tick to a cap of R285 per loan; once the cap is exhausted the
        household is cut off from THIS platform while remaining eligible at the others,
        since platforms are blind to each other (D12).
        """
        loans = self.loans.get(agent_id)
        if not loans:
            return 0.0, 0.0

        paid = 0.0
        fees = 0.0
        cash = max(available_cash, 0.0)

        for loan in loans:
            owed = loan.arrears + (loan.instalment if loan.remaining > 0 else 0.0)
            if owed <= 0:
                continue

            # The instalment falls due whether or not it is met; what is unpaid becomes
            # arrears. Decrementing here (not only on payment) is what makes the
            # Pay-in-4 schedule land on tick boundaries regardless of payment success.
            if loan.remaining > 0:
                loan.remaining -= 1

            if cash >= owed:
                cash -= owed
                paid += owed
                loan.arrears = 0.0
            else:
                part = cash
                cash = 0.0
                paid += part
                shortfall = owed - part

                headroom = max(self.late_fee_cap - loan.fee_accrued, 0.0)
                fee = min(self.late_fee_per_tick, headroom)
                loan.fee_accrued += fee
                fees += fee

                # Fees roll into the single payable rather than being tracked separately.
                loan.arrears = shortfall + fee

                if loan.fee_accrued >= self.late_fee_cap:
                    self.cut_off.add(agent_id)

        # Drop settled loans so stacking depth counts live facilities only.
        live = [loan for loan in loans if not loan.settled]
        if live:
            self.loans[agent_id] = live
        else:
            del self.loans[agent_id]

        return paid, fees

    def has_balance(self, agent_id: int) -> bool:
        return self.exposure(agent_id) > 0
