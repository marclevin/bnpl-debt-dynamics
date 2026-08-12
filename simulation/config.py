"""Parameter register: the single source of truth for every model parameter.

Thesis chapter 5 (Parameter Register) is generated FROM this module rather than typed,
so the table, the ODD submodel specification and the code cannot drift apart.

Every field carries `source` metadata naming the decision rule it implements and where
its value comes from. Three provenance levels are distinguished, and the distinction is
the point of the register:

    SOURCED     a citation fixes the value
    DERIVED     the value is computed from the data, not chosen
    ASSUMPTION  no anchor exists; mandatory sensitivity analysis

Decision rules: ../scratchpad/decision_rules.md
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

Provenance = Literal["SOURCED", "DERIVED", "ASSUMPTION"]

AmountRule = Literal["shortfall", "shortfall_125", "shortfall_plus_committed"]
Activation = Literal["random", "uniform", "synchronous"]


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
        source="24-month horizon at a 14-day tick (04_design.tex)",
    )
    burn_in: int = _p(
        12,
        rule="ODD",
        provenance="SOURCED",
        source="First 12 ticks discarded (04_design.tex)",
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
            "single-tick shock, which cannot carry the calibration (see issues.md B17)."
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
        sweep="RQ2 access sweep",
    )
    beta: float = _p(
        0.0,
        rule="D17",
        provenance="ASSUMPTION",
        source=(
            "Peer imitation strength. NOT SOURCED. beta=0 is the CONTROL ARM and "
            "recovers the independent-agent model exactly."
        ),
        sweep="RQ1/RQ2 primary experimental axis; the beta=0 row is always reported",
    )

    # -- D4 borrowing amount ----------------------------------------------------
    amount_rule: AmountRule = _p(
        "shortfall",
        rule="D4",
        provenance="ASSUMPTION",
        source="No anchor found in the literature sweep. The model's first uncited rule.",
        sweep="MANDATORY: shortfall / +25% / plus one tick of committed expenditure",
    )
    bnpl_purchase_mean: float = _p(
        1568.0,
        rule="D4/D11",
        provenance="ASSUMPTION",
        source=(
            "SA average BNPL basket ~R1,568 (trade press, % VERIFY, current vintage). "
            "Cross-checked against CFPB $135/loan. Weakest source in the thesis."
        ),
        sweep="0.5x to 2x",
    )
    bnpl_purchase_cv: float = _p(
        0.6,
        rule="D4",
        provenance="ASSUMPTION",
        source="Dispersion of BNPL purchase size. No source; lognormal.",
        sweep="with bnpl_purchase_mean",
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
            "alone leaves nearly empty (issues.md B21)."
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
            "The model's SECOND uncited rule (issues.md B15)."
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
            "Share of the BANKED subpopulation that is BNPL-eligible. Banked = 83.1% of "
            "households by observed data, so access_rate=1.0 means 83.1% of all households."
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
        15000.0,
        rule="D11",
        provenance="SOURCED",
        source="Payflex per-order cap of R15,000 (current vintage).",
        sweep="verify it binds rarely at LMI incomes",
    )
    bnpl_platform_limit: float = _p(
        5000.0,
        rule="D11",
        provenance="ASSUMPTION",
        source=(
            "Rolling available balance per platform. SEARCHED AND NOT PUBLISHED by "
            "either major SA provider (issues.md B16). Demoted to a BINDING-CHECK "
            "quantity: measure how often it blocks a transaction rather than tuning it."
        ),
        sweep="MANDATORY, with the binding rate reported",
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
        190.0,
        rule="D13",
        provenance="SOURCED",
        source="Payflex late fee R95 per week = R190 per 14-day tick.",
    )
    bnpl_late_fee_cap: float = _p(
        285.0,
        rule="D13",
        provenance="SOURCED",
        source="Payflex caps the late fee at three weeks: 3 x R95 = R285 per missed instalment.",
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
            "Lever 3. Baseline 0 = lever OFF. k_cool=1 tick = 14 days = the CCA s.66A "
            "statutory right of withdrawal, which lands exactly on a tick boundary."
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
        source="Random asynchronous, reseeded every tick (Comer & Loerch; Alizadeh).",
        sweep="MANDATORY: uniform and synchronous robustness runs",
    )

    # -- bookkeeping -------------------------------------------------------------
    label: str = _p("", rule="--", provenance="DERIVED", source="Experiment arm label")

    def replace(self, **kwargs: Any) -> "ParamSet":
        """Return a copy with fields overridden."""
        from dataclasses import replace as _replace

        return _replace(self, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        return {f.name: getattr(self, f.name) for f in fields(self)}


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
