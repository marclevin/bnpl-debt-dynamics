"""NCA Regulation 23A residual-income test and product-mix amortisation.

The Reg 23A function here is the SAME function that constructed `monthly_trad_repayment`
in `notebooks/p2_finscope_match.ipynb` (cell 14). That is deliberate: D9 specifies the
credit-granting gate as the residual-income test *already implemented in P2*, so the gate
and the servicing construction must be one implementation, not two that agree by luck.

The APR/term recomputation exists because the population parquet stores `repay_uncapped`
but not the APR that produced it, and per-tick interest accrual needs the rate.

Rules: D6 (repayment), D9 (credit gate), D14 lever 2 (the same test applied to BNPL).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import RATE_TABLE, TICKS_PER_YEAR

# ---------------------------------------------------------------------------
# NCA Regulation 23A(9) minimum expense norms.
# Source: National Credit Regulations including Affordability Assessment Regulations,
# GN R202, Government Gazette 38557, 13 March 2015.
# (band lower bound, minimum monthly fixed factor, % of income above the band lower bound)
# ---------------------------------------------------------------------------
NCA_EXPENSE_NORMS: tuple[tuple[float, float, float], ...] = (
    (0.00, 0.00, 1.0000),
    (800.01, 800.00, 0.0675),
    (6250.01, 1167.88, 0.0900),
    (25000.01, 2855.38, 0.0820),
    (50000.01, 4905.38, 0.0675),
)

#: The regulation's two published worked examples. Asserted at import so the table
#: cannot silently drift, exactly as the P2 notebook does.
NCA_WORKED_EXAMPLES: tuple[tuple[float, float], ...] = ((2000.0, 881.00), (10000.0, 1505.38))

#: Numerical guard only: keeps a zero or negative term out of the amortisation formula.
#: This was 6 months, an unsourced assumption inherited from P2. It never bound, because
#: the shortest term in the rate table was itself 6. Now that the terms are sourced, a
#: 6-month floor WOULD bind, silently overriding the 1-month short_term_loan term for
#: 1.1% of donors. The affordability guard is the Reg 23A residual-income ceiling below.
MIN_TERM_MONTHS = 1.0

PRODUCT_MAP = {
    "G10": "store_card",
    "G11": "revolving_credit",
    "G12": "hire_purchase",
    "G13": "short_term_loan",
    "G14": "personal_loan",
}
#: Fallback when D_trad > 0 but the FinScope donor flags no specific product.
DEFAULT_PRODUCT = "other_default"


def nca_necessary_expenses(gross_income: float) -> float:
    """Reg 23A(9) minimum monthly necessary expenses for a gross monthly income."""
    if gross_income is None or not np.isfinite(gross_income) or gross_income <= 0:
        return 0.0
    for lower, fixed, pct in reversed(NCA_EXPENSE_NORMS):
        if gross_income >= lower:
            return fixed + pct * (gross_income - lower)
    return 0.0


def nca_max_service(gross_income: float) -> float:
    """Monthly debt service the Reg 23A residual-income test permits.

    This is the D9 gate. Note it is income-varying and far tighter at the bottom of the
    distribution than the flat DSTI cap it replaced: 10.4% of income at R900/month
    against 83.2% at R7,712/month.
    """
    return max(gross_income - nca_necessary_expenses(gross_income), 0.0)


def nca_gate(
    gross_income: float,
    existing_visible_service: float,
    new_instalment: float,
) -> bool:
    """D9: grant only if the new instalment fits in residual income.

    `existing_visible_service` is what the lender can SEE (D10) — traditional debt via
    the bureau, never BNPL unless `bnpl_bureau_visible` is on. Passing a liability set
    the lender cannot observe is the whole mechanism, so callers decide what goes in
    here; this function does not.
    """
    capacity = nca_max_service(gross_income) - existing_visible_service
    return new_instalment <= capacity


# --- self-check at import, mirroring the P2 notebook -------------------------
for _income, _expected in NCA_WORKED_EXAMPLES:
    _got = round(nca_necessary_expenses(_income), 2)
    if _got != _expected:  # pragma: no cover
        raise AssertionError(
            f"Reg 23A table mis-specified: R{_income:,.0f} -> R{_got}, expected R{_expected}"
        )


def load_rate_table() -> pd.DataFrame:
    """NCA statutory maximum prescribed rates by product class (2017 repo 7.00%)."""
    return pd.read_csv(RATE_TABLE).set_index("product_class")


def weighted_apr_and_term(
    product_flags: dict[str, str] | pd.Series,
    rate_table: pd.DataFrame,
) -> tuple[float, float]:
    """APR and term for a household's traditional debt.

    NIDS records one consolidated balance, so neither can be weighted by product. Both are
    an unweighted mean over the classes the matched donor holds, falling back to unsecured
    when none is held. Reproduces the P2 `servicing()` construction.
    """
    held = [PRODUCT_MAP[c] for c in PRODUCT_MAP if bool(product_flags.get(c))]
    if not held:
        held = [DEFAULT_PRODUCT]
    apr = float(np.mean([rate_table.at[c, "apr_annual"] for c in held]))
    term_raw = float(np.mean([rate_table.at[c, "term_months"] for c in held]))
    return apr, max(term_raw, MIN_TERM_MONTHS)


def amortised_instalment(balance: float, apr_annual: float, term_months: float) -> float:
    """Level monthly instalment amortising `balance` over `term_months`."""
    if balance <= 0 or term_months <= 0:
        return 0.0
    r = apr_annual / 12.0
    if r <= 0:
        return balance / term_months
    return balance * r / (1.0 - (1.0 + r) ** (-term_months))


def tick_interest_rate(apr_annual: float) -> float:
    """Per-tick interest rate from an annual rate.

    Simple division by ticks-per-year, matching the P2 amortisation convention (which
    divides the APR by 12 for a monthly rate) rather than compounding it.
    """
    return apr_annual / TICKS_PER_YEAR
