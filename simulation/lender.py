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

from .affordability import DEFAULT_PRODUCT, amortised_instalment, load_rate_table, nca_gate
from .config import MONTHLY_TO_TICK

#: New traditional credit is priced as an unsecured credit transaction, READ from the same
#: sourced table that prices opening debt (the `other_default` row of
#: credit_rate_table.csv) so the two cannot drift apart: the NCA statutory maximum of
#: repo + 21% at the 2017 repo rate of 7.00%, over the CCMR 2017-Q1 stock-flow implied life
#: of the unsecured book (24.8 months, rounded to 25).
_NEW_LOAN_TERMS = load_rate_table().loc[DEFAULT_PRODUCT]
NEW_LOAN_APR = float(_NEW_LOAN_TERMS["apr_annual"])
NEW_LOAN_TERM_MONTHS = float(_NEW_LOAN_TERMS["term_months"])


def new_loan_instalment(amount: float) -> float:
    """Level MONTHLY instalment on a new traditional loan of `amount`, at the terms above.

    One function for the two places that need it: the gate tests this instalment against
    residual income, and the household books the same instalment when the loan is granted.
    """
    return amortised_instalment(amount, NEW_LOAN_APR, NEW_LOAN_TERM_MONTHS)


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

    __slots__ = ("bureau", "n_applications", "n_granted", "n_refused_gate", "value_granted")

    def __init__(self, bureau: CreditBureau) -> None:
        self.bureau = bureau
        self.n_applications = 0
        self.n_granted = 0
        self.n_refused_gate = 0
        self.value_granted = 0.0

    def apply(self, agent, amount: float) -> float:
        """Assess an application. Returns the amount granted (0.0 if refused).

        Credit is all-or-nothing: the household asks for what it needs (D4) and the
        residual-income test either accommodates the resulting instalment or does not.
        The lender only decides. The household books what it is granted
        (`HouseholdAgent._book_trad_loan`), which raises the scheduled service the bureau
        shows this lender at the next application (D10).
        """
        if amount <= 0:
            return 0.0

        self.n_applications += 1

        # A defaulted household is cut off: the bureau shows the default (D7/D10).
        if self.bureau.is_defaulted(agent.agent_id):
            return 0.0

        visible = self.bureau.visible_monthly_service(agent)

        if not nca_gate(agent.income_monthly, visible, new_loan_instalment(amount)):
            self.n_refused_gate += 1
            return 0.0

        self.n_granted += 1
        self.value_granted += amount
        return amount
