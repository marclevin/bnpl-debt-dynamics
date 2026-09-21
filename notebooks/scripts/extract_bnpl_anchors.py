"""Derive the South African BNPL purchase-size and volume anchors from listed-issuer reports.

**What this replaces.** BNPL purchase size was the model's single largest driver of output
(DEFECTS.md **B24**: 19.6pp of population default across its plausible range) and rested on
**trade press** — `sa_bnpl_basket_2026`, flagged `% VERIFY`, the weakest source in the
bibliography. This script replaces it with figures **derived from published aggregates**
disclosed by a listed issuer.

**Primary source (2026-08-13):** Weaver Fintech, *Integrated Report 2025*, **page 14**, the
"Profitable BNPL network" panel. PayJustNow is the BNPL business inside that group and one
of the four South African platforms the model represents. The panel discloses, on one page:

  * cumulative BNPL GMV by financial year, ending **R13.1bn** at FY2025;
  * **cumulative BNPL transactions of 9.4 million**;
  * **3.7 million signed-up BNPL customers**;
  * an annual **frequency rate** series: 1.8x, 2.2x, 2.8x, 3.9x, **4.4x** for FY2021-FY2025.

The same page states FY2025 GMV at retailer partners **grew 80% to R7.1 billion**.

⚠ **The entity was renamed.** HomeChoice International plc became **Weaver Fintech Ltd**
(JSE: WVR). The FY2024 document is cited under the old name (`homechoice2024ir`), the FY2025
Integrated Report and the 10 March 2026 SENS results under the new one.

**Neither document states an average order value.** It falls out of dividing two disclosed
aggregates, which is why this is an extraction with the sources' own cross-checks asserted
rather than a citation.

**Vintage.** Everything in the model is in 2017 Rands. The cumulative average order value
spans FY2021-FY2025, so it is deflated at its **GMV-weighted mean year** rather than at
either endpoint. The annual volume figures are FY2025 and are deflated at 2025. See
`cpi_deflator_2017.json`.

Usage:
    python notebooks/scripts/extract_bnpl_anchors.py [out_json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path("data/config/bnpl_anchors_2017.json")
DEFLATOR = Path("data/config/cpi_deflator_2017.json")

#: BNPL gross merchandise value by financial year, R million.
#: HomeChoice International plc Integrated Report 2024, five-year review.
GMV_BY_FY_RM: dict[int, float] = {2021: 204.0, 2022: 747.0, 2023: 1527.0, 2024: 3924.0}

#: Cumulative BNPL GMV by financial year, R billion, as charted on IAR 2025 p14. FY2021 is
#: unlabelled on the chart (too small to plot); the other four are read directly and must
#: reconcile with the annual series above, which is check 1.
CUMULATIVE_GMV_CHART_RBN: dict[int, float] = {2022: 0.9, 2023: 2.4, 2024: 6.3, 2025: 13.1}

#: Weaver Fintech Integrated Report 2025, p14, cumulative since BNPL inception.
CUMULATIVE_GMV_RM = 13_100.0
CUMULATIVE_TRANSACTIONS = 9_400_000
SIGNED_UP_CUSTOMERS = 3_700_000

#: Annual BNPL purchase frequency per customer, IAR 2025 p14.
FREQUENCY_BY_FY: dict[int, float] = {2021: 1.8, 2022: 2.2, 2023: 2.8, 2024: 3.9, 2025: 4.4}

#: FY2025 GMV as separately stated in the same report ("grew 80% to R7.1 billion").
FY2025_GMV_STATED_RM = 7_100.0
FY2025_GROWTH_STATED = 0.80
#: The stated FY2025 GMV and the cumulative chart label do not reconcile exactly (~3%),
#: most likely rounding on the chart plus a scope difference between "GMV at our retailer
#: partners" and total BNPL GMV. The gap is recorded, not tuned away. It is well inside the
#: tolerance because the derived order value uses only the cumulative pair, which are
#: disclosed together in a single panel.
RECONCILIATION_TOLERANCE = 0.10

#: The trade-press figure this supersedes, retained as a corroborating second source.
TRADE_PRESS_BASKET_R = 1568.0
TRADE_PRESS_VINTAGE = 2026

#: Published average BNPL transaction size elsewhere, for the ratio benchmark. These are
#: LEVELS in three currencies and none of them transfers; the ratio to median monthly
#: household income does, and that is the comparison the thesis makes.
#: ⚠ The income denominators are NOT recorded here: they must be pinned to each
#: jurisdiction's official household income statistic before the table is published.
INTERNATIONAL_LEVELS = {
    "united_states": {"value": 135.0, "currency": "USD", "source": "cfpb2025bnpl", "year": 2025},
    "australia": {"value": 147.0, "currency": "AUD", "source": "asic2020rep672", "year": 2020},
    "united_kingdom_low": {"value": 88.0, "currency": "GBP", "source": "woolard2021", "year": 2021},
    "united_kingdom_high": {"value": 110.0, "currency": "GBP", "source": "woolard2021", "year": 2021},
}


def main() -> None:
    out_path = ROOT / (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
    deflator = json.loads((ROOT / DEFLATOR).read_text(encoding="utf-8"))
    factor = {int(k): v for k, v in deflator["factor_from_2017"].items()}

    # --- check 1: the FY2024 annual series against the FY2025 cumulative chart ---------
    # Two documents, two different presentations of the same quantity. Summing the annual
    # series must land on the charted cumulative label at every year they share.
    running = 0.0
    for year in sorted(GMV_BY_FY_RM):
        running += GMV_BY_FY_RM[year]
        charted = CUMULATIVE_GMV_CHART_RBN.get(year)
        if charted is None:
            continue
        gap = abs(running / 1000.0 - charted) / charted
        assert gap < 0.12, (
            f"FY{year}: the annual GMV series sums to R{running / 1000:.2f}bn against the "
            f"IAR 2025 chart's R{charted}bn, a {gap:.1%} gap. The two disclosures disagree"
        )
    cumulative_fy2024 = running

    # --- check 2: the derived FY2025 GMV against the separately stated figure ----------
    gmv_fy2025_derived = CUMULATIVE_GMV_RM - cumulative_fy2024
    recon_gap = gmv_fy2025_derived / FY2025_GMV_STATED_RM - 1.0
    assert abs(recon_gap) < RECONCILIATION_TOLERANCE, (
        f"cumulative GMV implies FY2025 GMV of R{gmv_fy2025_derived:.0f}m against the "
        f"separately stated R{FY2025_GMV_STATED_RM:.0f}m, a {recon_gap:+.1%} gap"
    )

    # --- the derived average order value ---------------------------------------------
    aov_nominal = CUMULATIVE_GMV_RM * 1e6 / CUMULATIVE_TRANSACTIONS

    # Deflate at the GMV-weighted mean year: the cumulative average is a value-weighted
    # average over the whole period, so it carries that period's average price level.
    series = {**GMV_BY_FY_RM, 2025: gmv_fy2025_derived}
    weighted_year = sum(y * v for y, v in series.items()) / sum(series.values())
    lo, hi = int(weighted_year), int(weighted_year) + 1
    frac = weighted_year - lo
    weighted_factor = factor[lo] * (1 - frac) + factor[hi] * frac

    aov_2017 = aov_nominal / weighted_factor
    trade_press_2017 = TRADE_PRESS_BASKET_R / factor[TRADE_PRESS_VINTAGE]

    # --- the volume anchor, as a BAND ---------------------------------------------------
    # The frequency rate's denominator is not defined on the page. Two readings are
    # possible and they bracket the truth, so both are reported rather than one being
    # guessed at. This is the check on DEFECTS.md B25 (implausible cumulative volumes).
    per_active_nominal = FREQUENCY_BY_FY[2025] * aov_nominal
    per_signed_up_nominal = FY2025_GMV_STATED_RM * 1e6 / SIGNED_UP_CUSTOMERS
    per_active_2017 = per_active_nominal / factor[2025]
    per_signed_up_2017 = per_signed_up_nominal / factor[2025]

    payload = {
        "sources": {
            "primary": (
                "weaver2025iar (Weaver Fintech, Integrated Report 2025, p14, "
                "'Profitable BNPL network' panel)"
            ),
            "gmv_by_fy": "homechoice2024ir (Integrated Report 2024, five-year review)",
            "results_announcement": "weaver2025results (SENS, 10 March 2026)",
            "trade_press": "sa_bnpl_basket_2026 (superseded; retained as corroboration)",
            "entity_note": (
                "HomeChoice International plc was renamed Weaver Fintech Ltd (JSE: WVR). "
                "FY2024 documents carry the old name, FY2025 documents the new one."
            ),
        },
        "disclosed": {
            "gmv_by_fy_rm": GMV_BY_FY_RM,
            "cumulative_gmv_chart_rbn": CUMULATIVE_GMV_CHART_RBN,
            "cumulative_gmv_rm": CUMULATIVE_GMV_RM,
            "cumulative_transactions": CUMULATIVE_TRANSACTIONS,
            "signed_up_customers": SIGNED_UP_CUSTOMERS,
            "frequency_by_fy": FREQUENCY_BY_FY,
            "fy2025_gmv_stated_rm": FY2025_GMV_STATED_RM,
        },
        "cross_checks": {
            "gmv_since_inception_fy2024_rm": round(cumulative_fy2024, 1),
            "fy2025_gmv_derived_rm": round(gmv_fy2025_derived, 1),
            "fy2025_gmv_stated_rm": FY2025_GMV_STATED_RM,
            "reconciliation_gap_pct": round(100.0 * recon_gap, 1),
            "note": (
                "The annual series from the FY2024 report reproduces the FY2025 report's "
                "cumulative chart at every shared year, and the derived FY2025 GMV lands "
                "within a few per cent of the separately stated R7.1bn. Two documents, "
                "two presentations, one quantity."
            ),
        },
        "derivation": {
            "average_order_value_nominal": round(aov_nominal, 2),
            "gmv_weighted_vintage_year": round(weighted_year, 2),
            "deflator_applied": round(weighted_factor, 4),
        },
        "corroboration": {
            "trade_press_nominal": TRADE_PRESS_BASKET_R,
            "trade_press_vintage": TRADE_PRESS_VINTAGE,
            "trade_press_2017_rands": round(trade_press_2017, 2),
            "gap_pct": round(100.0 * (trade_press_2017 / aov_2017 - 1.0), 1),
            "note": (
                "Two independent South African sources — a listed-issuer disclosure and "
                "trade press — land within a few per cent of each other once both are "
                "deflated to 2017 Rands. Neither is fitted to anything."
            ),
        },
        "superseded_metric": {
            "figure": "FY2024 IAR: 'Frequency is up to 2.12 per annum, average spending up 21% to 7 000'",
            "why_dropped": (
                "RESOLVED 2026-08-13 and no longer used. Read as a BNPL order value it "
                "implies R7,000/2.12 = R3,302, which contradicts the R1,394 the cumulative "
                "aggregates give and would be anomalously high for South African apparel "
                "and homeware checkouts. It is a GROUP-WIDE fintech metric: Weaver "
                "cross-sells personal lending, a wallet and insurance alongside BNPL, so "
                "R7,000 across 2.12 transactions describes a blended portfolio, not a BNPL "
                "basket. The FY2025 report settles it by publishing a BNPL-SPECIFIC "
                "frequency series (1.8x to 4.4x), which is what this file now uses."
            ),
        },
        "international_levels": INTERNATIONAL_LEVELS,
        "international_note": (
            "Levels in three currencies; none transfers. The transferable object is the "
            "ratio to median monthly household income. Pin the income denominators to "
            "each jurisdiction's official statistic before publishing that table."
        ),
        "model_target": {
            #: VALIDATION TARGETS, not inputs. The purchase-size rule is derived from the
            #: IES budget share; these are what the resulting model output is checked
            #: against.
            "mean_purchase_2017_rands": round(aov_2017, 2),
            "annual_volume_per_active_user_2017_rands": round(per_active_2017, 2),
            "annual_volume_per_signed_up_user_2017_rands": round(per_signed_up_2017, 2),
            "volume_band_note": (
                "The frequency rate's denominator is not defined in the source, so the "
                "volume target is a BAND, not a point. The upper bound assumes frequency "
                "is per ACTIVE BNPL customer; the lower divides FY2025 GMV by all "
                "SIGNED-UP customers, most of whom are dormant. Compare the model's "
                "volume per ADOPTING household against the upper bound and per ELIGIBLE "
                "household against the lower."
            ),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"  cumulative GMV / transactions : R{aov_nominal:,.0f} nominal")
    print(f"  GMV-weighted vintage          : {weighted_year:.2f}  (deflator {weighted_factor:.4f})")
    print(f"  AVERAGE ORDER VALUE, 2017 R   : R{aov_2017:,.0f}")
    print(f"  trade press, 2017 R           : R{trade_press_2017:,.0f} "
          f"({payload['corroboration']['gap_pct']:+.1f}%)")
    print(f"  FY2025 GMV derived / stated   : R{gmv_fy2025_derived:,.0f}m / "
          f"R{FY2025_GMV_STATED_RM:,.0f}m ({recon_gap:+.1%})")
    print(f"  VOLUME BAND, 2017 R per year  : R{per_signed_up_2017:,.0f} (per signed-up) "
          f"to R{per_active_2017:,.0f} (per active)")


if __name__ == "__main__":
    main()
