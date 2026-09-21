"""Parameter register: the single source of truth for every model parameter.

Thesis chapter 5 (Parameter Register) is generated FROM this module rather than typed,
so the table, the ODD submodel specification and the code cannot drift apart.

Every field carries `source` metadata naming the decision rule it implements and where
its value comes from. Three provenance levels are distinguished, and the distinction is
the point of the register:

    SOURCED     a citation fixes the value
    DERIVED     the value is computed from the data, not chosen
    ASSUMPTION  no anchor exists; mandatory sensitivity analysis

Decision rules: ../scratchpad/DECISIONS.md
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, Literal

# ---------------------------------------------------------------------------
# Clock. 14-day tick (D15/decision.md Set 1), retroactively confirmed by D13:
# Payflex Pay-in-4 instalments fall exactly on tick boundaries.
# ---------------------------------------------------------------------------
TICK_DAYS = 14
MONTHS_PER_YEAR = 12
TICKS_PER_YEAR = 26
#: Monthly survey flows -> per-tick flows. Every monetary column in the population
#: parquet is monthly; stocks (D_trad, liquid_savings) are NOT scaled.
MONTHLY_TO_TICK = MONTHS_PER_YEAR / TICKS_PER_YEAR

#: CCMR age-analysis bands, as (label, min_ticks_in_arrears, max_ticks_inclusive).
#: At 14 days a tick the mapping onto the published day buckets is exact:
#: 1-2 ticks = 1-30d, 3-4 = 31-60d, 5-6 = 61-90d, 7-8 = 91-120d, 9+ = 120+d.
CCMR_BANDS: tuple[tuple[str, int, int | None], ...] = (
    ("current", 0, 0),
    ("d30", 1, 2),
    ("d31_60", 3, 4),
    ("d61_90", 5, 6),
    ("d91_120", 7, 8),
    ("d120_plus", 9, None),
)


def _root(start: Path | None = None) -> Path:
    start = start or Path(__file__).resolve().parent
    for d in [start, *start.parents]:
        if (d / "data" / "config").is_dir() and (d / "data" / "processed").is_dir():
            return d
    raise FileNotFoundError("could not locate repo root")


ROOT = _root()
DATA_CONFIG = ROOT / "data" / "config"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_RAW = ROOT / "data" / "raw"
RESULTS_RAW = ROOT / "results" / "raw"
RESULTS_SUMMARY = ROOT / "results" / "summary"

POPULATION_PARQUET = DATA_PROCESSED / "synthetic_population_5000.parquet"
NIDS_HHDERIVED = DATA_RAW / "NIDS_W5" / "hhderived.csv"
NIDS_INDDERIVED = DATA_RAW / "NIDS_W5" / "indderived_W5_Anon_V1.0.0.dta"
RATE_TABLE = DATA_CONFIG / "credit_rate_table.csv"
CCMR_BASELINE = DATA_CONFIG / "ccmr_2017_baseline.json"
QLFS_FLOWS = DATA_CONFIG / "qlfs_2017_labour_flows.json"
CPI_DEFLATOR = DATA_CONFIG / "cpi_deflator_2017.json"
BNPL_ANCHORS = DATA_CONFIG / "bnpl_anchors_2017.json"
IES_BNPL_SHARE = DATA_CONFIG / "ies_2022_bnpl_share.json"

Provenance = Literal["SOURCED", "DERIVED", "ASSUMPTION"]

AmountRule = Literal["shortfall", "shortfall_125", "shortfall_plus_committed"]
Activation = Literal["random", "uniform"]
PurchaseBase = Literal["discretionary", "income"]
PeerMechanism = Literal["linear", "threshold"]

# ---------------------------------------------------------------------------
# 2017 Rands. EVERY monetary quantity in this model is denominated in 2017 Rands:
# the NIDS W5 backbone, the Reg 23A expense table, the CCMR targets, the statutory
# rates at the 2017 repo rate. The BNPL parameters were the exception until
# DEFECTS.md B29 -- purchase size, the per-order cap and the late fees were all taken
# at CURRENT vintage and used unadjusted, denominating the BNPL side of the model
# roughly 1.4x too high against everything it interacts with.
#
# The conversion now happens HERE, once, from a sourced deflator, so a published
# nominal figure and the 2017-Rand value the model uses can never drift apart.
# ---------------------------------------------------------------------------


def load_cpi_factors() -> dict[int, float]:
    """Cumulative price factors from 2017, keyed by year (see cpi_deflator_2017.json)."""
    raw = json.loads(CPI_DEFLATOR.read_text(encoding="utf-8"))["factor_from_2017"]
    return {int(y): float(v) for y, v in raw.items()}


def to_2017_rands(nominal: float, vintage_year: int) -> float:
    """Convert a nominal amount observed in `vintage_year` into 2017 Rands."""
    factors = load_cpi_factors()
    if vintage_year not in factors:
        raise KeyError(
            f"no CPI factor for {vintage_year}; extend "
            "notebooks/scripts/extract_cpi_deflator.py"
        )
    return nominal / factors[vintage_year]


def load_bnpl_anchors() -> dict[str, Any]:
    """SA BNPL purchase-size and volume VALIDATION TARGETS (not inputs)."""
    return json.loads(BNPL_ANCHORS.read_text(encoding="utf-8"))


def load_ies_bnpl_share() -> float:
    """BNPL-financeable share of discretionary expenditure, derived from IES 2022/23."""
    payload = json.loads(IES_BNPL_SHARE.read_text(encoding="utf-8"))
    return float(payload["model_target"]["bnpl_financeable_share_of_discretionary"])


#: Vintage of the published Payflex terms the model takes its product mechanics from.
PAYFLEX_TERMS_VINTAGE = 2026

#: Payflex figures as published (nominal), and as the model uses them (2017 Rands).
PAYFLEX_ORDER_CAP_NOMINAL = 15_000.0
PAYFLEX_LATE_FEE_PER_TICK_NOMINAL = 190.0   # R95 per week x 2 weeks
PAYFLEX_LATE_FEE_CAP_NOMINAL = 285.0        # 3 weeks x R95

BNPL_ORDER_CAP_2017 = round(
    to_2017_rands(PAYFLEX_ORDER_CAP_NOMINAL, PAYFLEX_TERMS_VINTAGE), 2
)
BNPL_LATE_FEE_PER_TICK_2017 = round(
    to_2017_rands(PAYFLEX_LATE_FEE_PER_TICK_NOMINAL, PAYFLEX_TERMS_VINTAGE), 2
)
BNPL_LATE_FEE_CAP_2017 = round(
    to_2017_rands(PAYFLEX_LATE_FEE_CAP_NOMINAL, PAYFLEX_TERMS_VINTAGE), 2
)

#: kappa: a BNPL purchase is the scale of one month of the household's own spending in
#: the categories BNPL finances. DERIVED from IES 2022/23, not chosen.
BNPL_PURCHASE_SHARE_OF_DISCRETIONARY = round(load_ies_bnpl_share(), 4)


def _p(
    default: Any,
    *,
    rule: str,
    provenance: Provenance,
    source: str,
    sweep: str = "",
) -> Any:
    """Declare a parameter with its provenance metadata."""
    return field(
        default=default,
        metadata={
            "rule": rule,
            "provenance": provenance,
            "source": source,
            "sweep": sweep,
        },
    )


@dataclass(frozen=True, slots=True)
class ParamSet:
    """One fully specified model configuration.

    Frozen so a running model cannot mutate its own parameters, and so a ParamSet can be
    hashed into a run identifier.
    """

    # -- run control ------------------------------------------------------------
    seed: int = _p(0, rule="--", provenance="DERIVED", source="Run replicate seed")
    n_ticks: int = _p(
        52,
        rule="ODD",
        provenance="SOURCED",
        source="24-month horizon at a 14-day tick (03_calibration.tex)",
    )
    burn_in: int = _p(
        12,
        rule="ODD",
        provenance="SOURCED",
        source="First 12 ticks discarded (03_calibration.tex)",
    )
    n_agents: int | None = _p(
        None,
        rule="P3",
        provenance="DERIVED",
        source="None = use the full 5,000-agent resample",
        sweep="1000 / 5000 / 10000 population-stability check",
    )

    # -- D1 income and shock ----------------------------------------------------
    shock_prob: float = _p(
        0.01,
        rule="D1",
        provenance="ASSUMPTION",
        source=(
            "CALIBRATION TARGET, fitted to CCMR baseline arrears. Reported against the "
            "QLFS 2017 job-separation band (0.54%-1.17% per tick), NOT fitted to it."
        ),
        sweep="calibration grid",
    )
    # NOTE: there is deliberately no shock_magnitude parameter. Following Madeira, the
    # shock is a separation from employment, so the magnitude is the household's observed
    # wage component (w5_hhwage). See D1 and population.py.
    shock_persistent: bool = _p(
        True,
        rule="D1",
        provenance="SOURCED",
        source=(
            "An unemployment spell persists until re-employment. Madeira models FLOWS "
            "into and out of unemployment, and QLFS 2017 shows 68.4% of the unemployed "
            "remain unemployed the next quarter. False recovers D1's original "
            "single-tick shock, which cannot carry the calibration (see DEFECTS.md B17)."
        ),
        sweep="False = the original non-persistent rule, reported as a robustness arm",
    )
    shock_exit_prob: float = _p(
        0.018724,
        rule="D1",
        provenance="SOURCED",
        source=(
            "Per-tick re-employment hazard. QLFS 2017 Q3->Q4: 11.6% of the unemployed "
            "moved into employment per quarter -> 1.87% per 14-day tick."
        ),
        sweep="with the QLFS band",
    )

    # -- D2 consumption ---------------------------------------------------------
    discretionary_floor: float = _p(
        0.0,
        rule="D2",
        provenance="SOURCED",
        source="Discretionary spend fully compressible in the baseline (D2)",
        sweep="0.25 / 0.50 habit-persistence floors",
    )

    # -- D3 borrowing trigger / D17 peer influence -------------------------------
    q_base: float = _p(
        0.05,
        rule="D3/D17",
        provenance="ASSUMPTION",
        source="Spontaneous want-driven BNPL propensity. NOT SOURCED; swept.",
        sweep="RQ2 adoption sweep; sets the level that beta then amplifies",
    )
    beta: float = _p(
        0.0,
        rule="D17",
        provenance="ASSUMPTION",
        source=(
            "Peer imitation strength under the LINEAR mechanism. NOT SOURCED. beta=0 is "
            "the CONTROL ARM and recovers the independent-agent model exactly. Note that "
            "beta's scale changed on 2026-08-13 when s_g was renormalised onto the "
            "eligible subpopulation (DEFECTS.md B31), so values are not comparable with "
            "pre-2026-08-13 runs."
        ),
        sweep=(
            "RQ2 primary experimental axis -- it is what makes peer effects in BNPL "
            "adoption visible -- and toggled on/off for RQ3, whose cool-off lever only "
            "bites where beta > 0. The beta=0 row is always reported."
        ),
    )

    # -- D17 peer mechanism: the pre-registered structural robustness check -------
    # Linear coupling produced a linear response in every arm (DEFECTS.md B22), which is
    # close to tautological. D17 pre-registered Granovetter's heterogeneous-threshold
    # formulation as the alternative to try before concluding no threshold exists. Both
    # mechanisms remain runnable so they can be compared on identical access grids.
    peer_mechanism: PeerMechanism = _p(
        "linear",
        rule="D17",
        provenance="SOURCED",
        source=(
            "Which social-transmission rule is active. 'linear' is q = q_base + beta*s_g. "
            "'threshold' is Granovetter (1978): each household carries a fixed personal "
            "tipping point and ignores its peers until the group crosses it. "
            "MANDATORY comparison -- RQ2's negative result under linear coupling is weak "
            "evidence on its own, since a linear rule producing a linear response is "
            "nearly tautological."
        ),
        sweep="RQ2: both mechanisms on identical access grids",
    )
    mu_theta: float = _p(
        0.3,
        rule="D17",
        provenance="ASSUMPTION",
        source=(
            "Mean adoption threshold: the share of a household's reference group that "
            "must already be using BNPL before it responds. NOT SOURCED. Held fixed as "
            "the SECONDARY axis -- see sigma_theta for why."
        ),
        sweep="3-point sensitivity at one access level, not a full cross",
    )
    sigma_theta: float = _p(
        0.2,
        rule="D17",
        provenance="SOURCED",
        source=(
            "Dispersion of adoption thresholds, truncated to [0,1]. THE PRIMARY "
            "EXPERIMENTAL AXIS of the threshold arm, because Granovetter's actual claim "
            "is that the VARIANCE of thresholds, not their mean, decides whether a "
            "cascade occurs: a chain of thresholds with someone standing at every level "
            "propagates, a tightly clustered one does not. Sweeping mu_theta alone would "
            "test the wrong quantity and misrepresent the citation."
        ),
        sweep="MANDATORY: 0.05-0.40",
    )
    gamma: float = _p(
        0.0,
        rule="D17",
        provenance="ASSUMPTION",
        source=(
            "Appetite increment once a household's threshold is crossed. NOT SOURCED. "
            "gamma=0 is the CONTROL ARM of the threshold mechanism and recovers the "
            "independent-agent model exactly, exactly as beta=0 does for the linear one."
        ),
        sweep="RQ2 threshold arm; the gamma=0 row is always reported",
    )

    # -- D4 borrowing amount ----------------------------------------------------
    amount_rule: AmountRule = _p(
        "shortfall",
        rule="D4",
        provenance="ASSUMPTION",
        source="No anchor found in the literature sweep. The model's first uncited rule.",
        sweep="MANDATORY: shortfall / +25% / plus one tick of committed expenditure",
    )
    shortfall_bnpl_capped: bool = _p(
        True,
        rule="D5",
        provenance="ASSUMPTION",
        source=(
            "Caps the BNPL share of a SHORTFALL request at kappa x the household's own "
            "monthly budget -- the same quantity that sizes a want-driven purchase. BNPL "
            "finances retail goods in particular categories, so the most it can relieve "
            "is what the household spends in them; the uncapped path let it stand in for "
            "general-purpose cash. Whatever the cap excludes goes to the traditional "
            "lender and faces the D9 gate. Added 2026-09-21 after the working run ranked "
            "the D4 amount rule, which acts through this path, as the largest sensitivity."
        ),
        sweep="Robustness: uncapped, crossed with the three D4 amount rules",
    )
    bnpl_purchase_base: PurchaseBase = _p(
        "discretionary",
        rule="D4/D11",
        provenance="SOURCED",
        source=(
            "What a BNPL purchase is sized AGAINST. BNPL finances discretionary "
            "consumption, so the household's own discretionary budget is the observed "
            "scale at which it makes discretionary purchases. 'income' is the "
            "robustness arm, and is the base the international regulator ratios are "
            "expressed against."
        ),
        sweep="MANDATORY: discretionary / income",
    )
    bnpl_purchase_ratio: float = _p(
        BNPL_PURCHASE_SHARE_OF_DISCRETIONARY,
        rule="D4/D11",
        provenance="DERIVED",
        source=(
            "kappa. Share of a household's discretionary budget spent on the categories "
            "BNPL finances (clothing and footwear, furniture and appliances, ICT "
            "devices, recreational durables), DERIVED from Stats SA IES 2022/23 COICOP "
            "microdata -- see ies_2022_bnpl_share.json. A ratio, never a money amount, "
            "so the 2022/23 vintage cannot contaminate the 2017-Rand model. "
            "REPLACES the flat R1,568 trade-press constant (DEFECTS.md B24/B30)."
        ),
        sweep="MANDATORY: 0.07-0.28 (half to double the derived share)",
    )
    bnpl_purchase_cv: float = _p(
        0.6,
        rule="D4",
        provenance="ASSUMPTION",
        source="Dispersion of BNPL purchase size around its household-relative mean. No source; lognormal.",
        sweep="with bnpl_purchase_ratio",
    )

    # -- D6 repayment and arrears -----------------------------------------------
    min_payer_share: float = _p(
        0.29,
        rule="D6",
        provenance="SOURCED",
        source="Keys & Wang (2019): 29% of accounts pay at or near the minimum. US transfer.",
        sweep="0.20-0.40 (brackets the transferred US point estimate)",
    )
    payment_friction: float = _p(
        0.0,
        rule="D6",
        provenance="SOURCED",
        source=(
            "Per-tick probability of missing a traditional instalment DESPITE having the "
            "cash. Kuchler & Pagel (2021): present-biased borrowers fail to execute "
            "planned paydown. Applies to traditional debt only, since BNPL auto-debits a "
            "card. CALIBRATED to the CCMR 1-30 day band, which the unemployment channel "
            "alone leaves nearly empty (DEFECTS.md B21)."
        ),
        sweep="calibration grid; second fitted parameter",
    )
    min_payment_frac: float = _p(
        0.05,
        rule="D6",
        provenance="ASSUMPTION",
        source=(
            "The contractual minimum itself. D6 fixes the SHARE of minimum-payers but "
            "never defined the minimum; the NCA prescribes no formula either. "
            "The model's SECOND uncited rule (DEFECTS.md B15)."
        ),
        sweep="MANDATORY: 0.025-0.10",
    )

    # -- D7 distress and default -------------------------------------------------
    k_default: int = _p(
        7,
        rule="D7",
        provenance="SOURCED",
        source=(
            "7 ticks = 98 days, inside the CCMR 91-120 band, so it maps onto the 90+ "
            "impairment convention. Revised from 6 once the 2017 CCMR was in hand."
        ),
        sweep="k=4 (56 days -> the 60+ band, target 16.54%)",
    )

    # -- D10 information asymmetry / D14 lever 1 ---------------------------------
    bnpl_bureau_visible: bool = _p(
        False,
        rule="D10/D14",
        provenance="SOURCED",
        source=(
            "BNPL sits outside the NCA: no bureau reporting obligation "
            "(Norton Rose; TransUnion). Default False IS the SA status quo."
        ),
        sweep="RQ3 lever 1 - the comparison the model was built to make",
    )

    # -- D11 BNPL eligibility and limits -----------------------------------------
    bnpl_enabled: bool = _p(
        False,
        rule="OVERVIEW 1a",
        provenance="SOURCED",
        source="Injection design: the 2017 baseline is BNPL-free by construction.",
        sweep="the injection itself",
    )
    bnpl_access_rate: float = _p(
        1.0,
        rule="D11",
        provenance="DERIVED",
        source=(
            "Share of the BANKED subpopulation that is BNPL-eligible. Banked = 82.8% of "
            "households by observed data, so access_rate=1.0 means 82.8% of all households."
        ),
        sweep="RQ2 axis 1, 0.0-1.0 within the banked subpopulation",
    )
    n_platforms: int = _p(
        4,
        rule="D12",
        provenance="SOURCED",
        source="PayJustNow, Payflex, Mobicred, TymeBank all active in South Africa.",
        sweep="1-6; N=1 isolates single-platform accumulation from cross-firm stacking",
    )
    bnpl_order_cap: float = _p(
        BNPL_ORDER_CAP_2017,
        rule="D11",
        provenance="SOURCED",
        source=(
            f"Payflex per-order cap of R{PAYFLEX_ORDER_CAP_NOMINAL:,.0f} as published "
            f"({PAYFLEX_TERMS_VINTAGE} vintage), DEFLATED to 2017 Rands "
            "(cpi_deflator_2017.json). Every other quantity in the model is 2017 Rands; "
            "using the nominal figure denominated the BNPL side ~1.4x too high "
            "(DEFECTS.md B29)."
        ),
        sweep="verify it binds rarely at LMI incomes",
    )
    bnpl_limit_income_multiple: float = _p(
        0.10,
        rule="D11",
        provenance="ASSUMPTION",
        source=(
            "lambda. Rolling available balance per platform, as a multiple of the "
            "household's MONTHLY income, applied independently at each of n_platforms. "
            "No SA provider publishes a rolling limit (DEFECTS.md B16), but both state "
            "the limit is set per customer from credit profile and repayment behaviour, "
            "and the group's audited credit-risk disclosure describes a 'low and grow' "
            "policy -- which licenses a FUNCTION of household characteristics rather "
            "than a flat constant. REPLACES the flat R5,000, which was 217% of the "
            "median banked Q1 household's monthly income (DEFECTS.md B30). "
            "VALUE CHOSEN 2026-08-13 to make the model's STACKED total match the only "
            "measurement of that quantity: Woolard found it 'relatively easy' to accrue "
            "~GBP1,000 of bureau-invisible BNPL debt, ~37% of UK median monthly "
            "household income ACROSS ALL PROVIDERS, so ~0.09 each across four. "
            "lambda=0.10 x 4 platforms reproduces that; the earlier 0.25 gave a stacked "
            "total of 1.0x monthly income, ~2.7x what Woolard called easy to accrue. "
            "Cross-check: Afterpay's published initial and maximum limits are ~8% and "
            "~26% of AU median monthly income, so 0.10 sits at the initial-limit end. "
            "Reported against that band, NOT fitted to it -- the same treatment "
            "shock_prob receives against the QLFS band. The income denominators are the "
            "author's arithmetic and must be pinned before the band is published."
        ),
        sweep="MANDATORY: 0.1-1.0, with the binding rate reported BY QUINTILE",
    )

    # -- D13 BNPL repayment and penalties ----------------------------------------
    bnpl_instalments: int = _p(
        4,
        rule="D13",
        provenance="SOURCED",
        source="Payflex Pay in 4: 25% at checkout then 25% at each of the next three ticks.",
        sweep="Pay in 3 monthly (PayJustNow) as the structural alternative",
    )
    bnpl_late_fee_per_tick: float = _p(
        BNPL_LATE_FEE_PER_TICK_2017,
        rule="D13",
        provenance="SOURCED",
        source=(
            "Payflex late fee R95 per week = R190 per 14-day tick as published "
            f"({PAYFLEX_TERMS_VINTAGE} vintage), DEFLATED to 2017 Rands (DEFECTS.md B29)."
        ),
    )
    bnpl_late_fee_cap: float = _p(
        BNPL_LATE_FEE_CAP_2017,
        rule="D13",
        provenance="SOURCED",
        source=(
            "Payflex caps the late fee at three weeks: 3 x R95 = R285 per missed "
            f"instalment as published ({PAYFLEX_TERMS_VINTAGE} vintage), DEFLATED to "
            "2017 Rands (DEFECTS.md B29)."
        ),
    )

    # -- D14 intervention levers (RQ3) -------------------------------------------
    bnpl_affordability_check: bool = _p(
        False,
        rule="D14",
        provenance="SOURCED",
        source=(
            "Lever 2. Applies the D9 Reg 23A residual-income test to BNPL. "
            "The FCA PS26/1 'proportionate affordability check' in SA statutory terms."
        ),
        sweep="RQ3 lever 2, on/off",
    )
    k_cool: int = _p(
        0,
        rule="D14",
        provenance="SOURCED",
        source=(
            "Lever 3. Baseline 0 = lever OFF. k_cool=1 tick = 14 days = the UK CCA "
            "s.66A statutory right of withdrawal, which lands exactly on a tick "
            "boundary. SEMANTICS: k_cool=n blocks want-driven initiation for the next n "
            "ticks. Until DEFECTS.md B27 was fixed the gate was off by one and k_cool=1 "
            "blocked nothing, so the statutory arm reported precisely zero effect."
        ),
        sweep="RQ3 lever 3, 0-4 ticks",
    )
    stacking_cap: int | None = _p(
        None,
        rule="D14",
        provenance="ASSUMPTION",
        source=(
            "Lever 4. Max concurrent facilities. HYPOTHETICAL: no jurisdiction imposes "
            "one. Must be labelled as such wherever it is reported."
        ),
        sweep="RQ3 lever 4, 1-4 or None",
    )

    # -- D16 scheduling ----------------------------------------------------------
    activation: Activation = _p(
        "random",
        rule="D16",
        provenance="SOURCED",
        source="Random asynchronous order, re-drawn every tick (Comer & Loerch; Alizadeh).",
        sweep="MANDATORY: fixed-order (uniform) robustness run",
    )

    # -- bookkeeping -------------------------------------------------------------
    label: str = _p("", rule="--", provenance="DERIVED", source="Experiment arm label")

    def replace(self, **kwargs: Any) -> "ParamSet":
        """Return a copy with fields overridden."""
        from dataclasses import replace as _replace

        return _replace(self, **kwargs)


def parameter_register() -> list[dict[str, str]]:
    """The register as rows, for the thesis parameter table.

    Chapter 5's table is generated from this so it cannot drift from the code.
    """
    default = ParamSet()
    rows = []
    for f in fields(ParamSet):
        meta = f.metadata
        if meta.get("rule") == "--":
            continue
        rows.append(
            {
                "parameter": f.name,
                "rule": meta.get("rule", ""),
                "baseline": str(getattr(default, f.name)),
                "provenance": meta.get("provenance", ""),
                "source": meta.get("source", ""),
                "sweep": meta.get("sweep", ""),
            }
        )
    return rows


def load_ccmr_target() -> dict[str, float]:
    """The 2017-Q1 CCMR baseline arrears target (account basis)."""
    return json.loads(CCMR_BASELINE.read_text(encoding="utf-8"))["model_target"]


def load_qlfs_band() -> dict[str, float]:
    """The QLFS 2017 per-tick job-separation band for the fitted shock probability."""
    return json.loads(QLFS_FLOWS.read_text(encoding="utf-8"))["model_target"]


if __name__ == "__main__":  # pragma: no cover
    import csv
    import sys

    w = csv.DictWriter(
        sys.stdout,
        fieldnames=["parameter", "rule", "baseline", "provenance", "source", "sweep"],
    )
    w.writeheader()
    w.writerows(parameter_register())
