"""P5: turn the validated population parquet into agent initialisation records.

Loads `synthetic_population_5000.parquet` (P3 output, 14/14 checks passed in P4), joins
the wage component needed for the D1 shock, recomputes each household's product-mix APR,
and builds the D17 reference groups.

Nothing here re-derives the population. P1-P3 are not re-run: the wage column is joined
onto the existing parquet on `source_w5_hhid`, so the validated resample is untouched.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import pandas as pd

from .affordability import (
    amortised_instalment,
    load_rate_table,
    nca_max_service,
    weighted_apr_and_term,
)
from .config import (
    MONTHLY_TO_TICK,
    NIDS_HHDERIVED,
    NIDS_INDDERIVED,
    POPULATION_PARQUET,
)

PRODUCT_COLS = ["G10", "G11", "G12", "G13", "G14"]


@dataclass(slots=True)
class HouseholdRecord:
    """Immutable initialisation data for one household agent. All money in 2017 Rands."""

    agent_id: int
    # -- tags -------------------------------------------------------------------
    province: str
    income_quintile: str
    income_source: str
    household_size: float
    # -- flows, PER TICK (monthly survey values scaled by 12/26) -----------------
    income_tick: float
    income_wage_tick: float
    #: Employed members on the NIDS roster. A separation costs one earner's share.
    n_earners: int
    committed_tick: float
    discretionary_tick: float
    scheduled_service_tick: float
    # -- flows, monthly (the Reg 23A test is specified on monthly income) --------
    income_monthly: float
    nca_capacity_monthly: float
    # -- stocks ------------------------------------------------------------------
    d_trad: float
    liquid_savings: float
    # -- debt pricing -------------------------------------------------------------
    apr_annual: float
    term_months: float
    # -- FinScope flags -----------------------------------------------------------
    banked: bool
    credit_access_formal: bool
    # -- D17 --------------------------------------------------------------------
    reference_group: tuple[str, str]

    @property
    def wage_share(self) -> float:
        if self.income_tick <= 0:
            return 0.0
        return self.income_wage_tick / self.income_tick


@lru_cache(maxsize=1)
def load_population_frame() -> pd.DataFrame:
    """The 5,000-agent population with the wage column joined and APRs recomputed.

    Cached: the parquet is read once per process, which matters because the batch runner
    instantiates thousands of models.
    """
    pop = pd.read_parquet(POPULATION_PARQUET)

    # --- D1: join the wage component -----------------------------------------
    # Following Madeira, the income shock is a separation from employment, so its
    # magnitude is the household's observed wage income rather than a chosen fraction.
    wage = pd.read_csv(
        NIDS_HHDERIVED, usecols=["w5_hhid", "w5_hhincome", "w5_hhwage"]
    ).rename(columns={"w5_hhincome": "_income_check"})
    merged = pop.merge(wage, left_on="source_w5_hhid", right_on="w5_hhid", how="left")

    if len(merged) != len(pop):
        raise ValueError("wage join changed row count; source_w5_hhid is not unique in NIDS")
    if merged["w5_hhid"].isna().any():
        raise ValueError("wage join left unmatched households")
    if not np.allclose(
        merged["w5_hhincome"], merged["_income_check"], rtol=1e-6, equal_nan=True
    ):
        raise ValueError("joined NIDS income disagrees with the backbone; wrong join key")

    # Nulls are households with no wage income. Verified: no WAGE-dominant household has
    # a null or zero wage, so filling with 0 cannot silently exempt a household that
    # ought to be shocked.
    merged["w5_hhwage"] = merged["w5_hhwage"].fillna(0.0).clip(lower=0.0)
    over = merged["w5_hhwage"] > merged["w5_hhincome"]
    if over.any():
        merged.loc[over, "w5_hhwage"] = merged.loc[over, "w5_hhincome"]

    merged = merged.drop(columns=["w5_hhid", "_income_check"])

    # --- D1: join the earner count -------------------------------------------
    # A separation costs the household ONE earner's wage, not all of it. Without this
    # a two-earner household loses everything at once, which leaves the mild CCMR
    # arrears bands empty (issues.md B21). It also makes `p` a per-EARNER hazard,
    # directly comparable to the QLFS individual transition rate.
    ind = pd.read_stata(NIDS_INDDERIVED, columns=["w5_hhid", "w5_empl_stat"])
    earners = (
        ind.assign(_emp=(ind["w5_empl_stat"] == "Employed").astype(int))
        .groupby("w5_hhid", as_index=False)["_emp"]
        .sum()
        .rename(columns={"_emp": "n_earners"})
    )
    merged = merged.merge(
        earners, left_on="source_w5_hhid", right_on="w5_hhid", how="left"
    ).drop(columns=["w5_hhid"])
    merged["n_earners"] = merged["n_earners"].fillna(0).astype(int)

    # Consistency check: a WAGE-dominant household must have at least one earner on the
    # roster. Verified to hold for all 2,892 of them; if it ever fails the income-source
    # classification and the employment roster have diverged.
    wage_no_earner = ((merged["income_source"] == "WAGE") & (merged["n_earners"] < 1)).sum()
    if wage_no_earner:
        raise ValueError(
            f"{wage_no_earner} WAGE-dominant households have no employed member on the "
            "NIDS roster; income_source and w5_empl_stat disagree"
        )

    # --- recompute the product-mix APR and term -------------------------------
    # The parquet stores repay_uncapped but not the rate behind it, and per-tick
    # interest accrual needs it.
    rate_table = load_rate_table()
    aprs, terms = [], []
    for _, row in merged[PRODUCT_COLS].iterrows():
        apr, term = weighted_apr_and_term(row, rate_table)
        aprs.append(apr)
        terms.append(term)
    merged["apr_annual"] = aprs
    merged["term_months"] = terms

    return merged


def build_records(
    n_agents: int | None = None, seed: int = 0
) -> tuple[list[HouseholdRecord], dict[tuple[str, str], list[int]]]:
    """Build agent records and the D17 reference-group index.

    `n_agents` None uses the full 5,000. A smaller value samples without replacement and
    a larger one resamples with replacement, for the population-stability check.
    """
    df = load_population_frame()

    if n_agents is not None and n_agents != len(df):
        rng = np.random.default_rng(seed)
        replace = n_agents > len(df)
        idx = rng.choice(len(df), size=n_agents, replace=replace)
        df = df.iloc[idx].reset_index(drop=True)

    records: list[HouseholdRecord] = []
    groups: dict[tuple[str, str], list[int]] = {}

    for i, row in enumerate(df.itertuples(index=False)):
        quintile = str(row.income_quintile)
        province = str(row.province)
        group = (quintile, province)

        income_monthly = float(row.w5_hhincome)
        # The instalment is recomputed rather than read from the parquet so that a
        # sensitivity run altering the rate table flows through consistently. It
        # reproduces `monthly_trad_repayment` under baseline settings.
        uncapped = amortised_instalment(
            float(row.D_trad), float(row.apr_annual), float(row.term_months)
        )
        capacity_monthly = nca_max_service(income_monthly)
        scheduled_monthly = min(uncapped, capacity_monthly)

        records.append(
            HouseholdRecord(
                agent_id=i,
                province=province,
                income_quintile=quintile,
                income_source=str(row.income_source),
                household_size=float(row.w5_hhsizer),
                income_tick=income_monthly * MONTHLY_TO_TICK,
                income_wage_tick=float(row.w5_hhwage) * MONTHLY_TO_TICK,
                n_earners=int(row.n_earners),
                committed_tick=float(row.expenditure_committed) * MONTHLY_TO_TICK,
                discretionary_tick=float(row.expenditure_discretionary) * MONTHLY_TO_TICK,
                scheduled_service_tick=scheduled_monthly * MONTHLY_TO_TICK,
                income_monthly=income_monthly,
                nca_capacity_monthly=capacity_monthly,
                d_trad=float(row.D_trad),
                liquid_savings=float(row.liquid_savings),
                apr_annual=float(row.apr_annual),
                term_months=float(row.term_months),
                banked=bool(row.banked),
                credit_access_formal=bool(row.credit_access_formal),
                reference_group=group,
            )
        )
        groups.setdefault(group, []).append(i)

    return records, groups


def zero_capacity_debtors(records: list[HouseholdRecord]) -> list[int]:
    """Households holding debt that no NCA-compliant lender could have granted.

    P2 found 53 of these and the decision was to report them, not cap them away. They
    have `D_trad > 0` but zero Reg 23A capacity, so their scheduled service is zero: they
    can never miss an instalment while their balance compounds. Tracked as a named
    diagnostic so they cannot quietly distort the arrears denominator.
    """
    return [r.agent_id for r in records if r.d_trad > 0 and r.nca_capacity_monthly <= 0]
