"""Traditional lender and credit bureau.

D9: the credit-granting gate is the NCA Reg 23A residual-income test — the same function
that built `monthly_trad_repayment` in P2, not a re-implementation.

D10: the bureau holds TRADITIONAL debt only. It cannot see BNPL obligations (which sit
outside the NCA and carry no reporting duty) or informal debt. The lender is therefore
applying the regulation correctly to an incomplete liability set, which is the thesis
mechanism rather than a modelling shortcut.

The lender does not adapt (ODD: Adaptation). It is a non-adaptive stub by design.
"""

from __future__ import annotations

from .affordability import (
    amortised_instalment,
    nca_max_service,
)
from .config import MONTHLY_TO_TICK

#: New traditional credit is priced as an unsecured credit transaction: the NCA statutory
#: maximum of repo + 21% at the 2017 repo rate of 7.00%, over 24 months. Matches the
#: `other_default` row of credit_rate_table.csv.
NEW_LOAN_APR = 0.28
NEW_LOAN_TERM_MONTHS = 24.0


class CreditBureau:
    """The in-model credit record. Traditional debt only (D10).

    What the lender sees through this object, and what it does not, IS the mechanism.
    `bnpl_visible` is the D14 lever-1 switch; with it off (the South African status quo)
    BNPL obligations are invisible to the affordability test.
    """

    __slots__ = ("bnpl_visible", "_defaulted")

    def __init__(self, bnpl_visible: bool = False) -> None:
        self.bnpl_visible = bnpl_visible
        self._defaulted: set[int] = set()

    def record_default(self, agent_id: int) -> None:
        self._defaulted.add(agent_id)

    def is_defaulted(self, agent_id: int) -> bool:
        return agent_id in self._defaulted

    def visible_monthly_service(self, agent) -> float:
        """Monthly obligations the lender can observe for this household.

        Always the traditional scheduled instalment. BNPL is added only when the
        reporting gap is closed by lever 1 — the gap between the two settings is the
        measured cost of the reporting exemption.
        """
        visible = agent.scheduled_service_tick / MONTHLY_TO_TICK
        if self.bnpl_visible:
            visible += agent.bnpl_due_per_tick() / MONTHLY_TO_TICK
        return visible


class TraditionalLender:
    """Single non-adaptive lender operating the NCA Reg 23A gate (D9).

    Multi-lender competition on the traditional side is explicitly out of scope
    (OVERVIEW section 6); the BNPL side does have multiple platforms.
    """

    __slots__ = ("bureau", "n_applications", "n_granted", "n_refused_gate", "n_refused_default")

    def __init__(self, bureau: CreditBureau) -> None:
        self.bureau = bureau
        self.n_applications = 0
        self.n_granted = 0
        self.n_refused_gate = 0
        self.n_refused_default = 0

    def apply(self, agent, amount: float) -> float:
        """Assess an application. Returns the amount granted (0.0 if refused).

        Credit is all-or-nothing: the household asks for what it needs (D4) and the
        residual-income test either accommodates the resulting instalment or does not.
        """
        if amount <= 0:
            return 0.0

        self.n_applications += 1

        # A defaulted household is cut off: the bureau shows the default (D7/D10).
        if self.bureau.is_defaulted(agent.agent_id):
            self.n_refused_default += 1
            return 0.0

        new_instalment = amortised_instalment(amount, NEW_LOAN_APR, NEW_LOAN_TERM_MONTHS)
        capacity = nca_max_service(agent.income_monthly)
        visible = self.bureau.visible_monthly_service(agent)

        if new_instalment > max(capacity - visible, 0.0):
            self.n_refused_gate += 1
            return 0.0

        self.n_granted += 1
        return amount
