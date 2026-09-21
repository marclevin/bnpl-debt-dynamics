"""Extract 2017 labour-market transition rates from Stats SA Labour Market Dynamics.

Source: Statistics South Africa, *Labour Market Dynamics in South Africa, 2022*,
Report 02-11-02. The 2022 edition reports the QLFS panel for 2017-2022, so it carries a
**vintage-matched 2017 figure** for the NIDS W5 population.

Two tables are read and required to agree:
  * Table 2.1a (p.15)  headline, Q3:2017 -> Q4:2017, with counts in thousands.
  * Table A.1  (p.149) appendix panel, same transition, percentages only.

Two of the report's own prose statements are asserted so the extraction cannot silently
drift, mirroring the discipline used for `ccmr_2017_baseline.json`.

Feeds D1 (income shock). The model's shock is the loss of a household's wage component,
following Madeira (2018), whose labour shock is a flow into unemployment rather than an
abstract fractional income cut. This file supplies the *plausibility band* against which
the fitted shock probability `p` is reported. `p` itself remains a calibration target.

Usage:
    python notebooks/scripts/extract_qlfs_lmd.py [pdf] [out_json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF = Path("data/raw/QLFS_LMD_2022/Labour Market Dynamics SA 2022.pdf")
DEFAULT_OUT = Path("data/config/qlfs_2017_labour_flows.json")

# Model clock. 14-day tick; quarter length is the mean Julian quarter.
TICK_DAYS = 14.0
QUARTER_DAYS = 365.25 / 4.0
TICKS_PER_QUARTER = QUARTER_DAYS / TICK_DAYS


def page_text(pdf: Path, printed_page: int) -> str:
    """Text of a page, addressed by the page number printed in the report header.

    In this PDF the 0-based index happens to coincide with the printed page number
    (there is no unnumbered cover offset), which the header assertion below confirms.
    """
    from pypdf import PdfReader

    text = PdfReader(str(pdf)).pages[printed_page].extract_text() or ""
    assert f"STATISTICS SOUTH AFRICA {printed_page}" in _squash(text), (
        f"page index {printed_page} is not printed page {printed_page}; "
        "the PDF pagination has changed"
    )
    return text


def _squash(text: str) -> str:
    """Collapse runs of whitespace so assertions survive PDF spacing quirks."""
    return " ".join(text.split())


def quarterly_to_tick_hazard(q_rate: float) -> float:
    """Convert a per-quarter transition probability to a per-tick hazard.

    Constant-hazard conversion: 1 - (1 - q) ** (1 / ticks_per_quarter).
    """
    return 1.0 - (1.0 - q_rate) ** (1.0 / TICKS_PER_QUARTER)


def extract(pdf: Path) -> dict:
    # ---- Table 2.1a, p.15: counts in thousands, Q3:2017 -> Q4:2017 ------------
    # Employed row: Employed / Unemployed / NEA / Total
    p15 = _squash(page_text(pdf, 15))
    assert "Retention and transition rates by labour market status, 2017" in p15, (
        "Table 2.1a not found on p.15 - the report layout has changed"
    )
    assert "15 081 572 538 16 192" in p15, (
        "Table 2.1a employed-row counts not found; re-check the extraction"
    )

    employed_t0 = 16_192  # thousands, Q3:2017
    to_employed = 15_081
    to_unemployed = 572
    to_nea = 538
    # Cells are published rounded to thousands independently, so the row sums to
    # 16 191 against a printed total of 16 192. Allow the rounding, not more.
    assert abs(to_employed + to_unemployed + to_nea - employed_t0) <= 2, (
        "Table 2.1a employed row does not sum to its total within rounding"
    )

    # ---- Table A.1, p.149: appendix panel, same transition, percentages -------
    p149 = _squash(page_text(pdf, 149))
    assert "Table A.1: Quarterly transition rates" in p149
    assert "Q3 2017 Q4 2017 93,1 3,5 1,3 2,0 100,0" in p149, (
        "Table A.1 Q3->Q4 2017 employed row not found"
    )
    # A.1 splits NEA into Discouraged (1,3) + Other NEA (2,0) = 3,3, matching 2.1a.

    # ---- Cross-checks against the report's own prose -------------------------
    # 1. Retention among the employed fell 1,9 pp between 2017 and 2022: 93,1 - 91,2.
    assert "decreased by 1,9" in p15, "prose cross-check 1 (retention delta) failed"
    # 2. Unemployment -> employment "from 11,6 % in 2017", matching Table 2.1a.
    assert "11,6 % in 2017 to 9,9 % in 2022" in p15, (
        "prose cross-check 2 (unemployment->employment) failed"
    )

    pct_retained = round(100 * to_employed / employed_t0, 2)
    pct_to_unemployed = round(100 * to_unemployed / employed_t0, 2)
    pct_to_nea = round(100 * to_nea / employed_t0, 2)
    pct_out_of_employment = round(100 * (to_unemployed + to_nea) / employed_t0, 2)

    # Table A.1 also carries the two neighbouring 2017 transitions, giving a range.
    assert "Q2 2017 Q3 2017 93,1 3,6 1,2 2,1 100,0" in p149
    assert "Q4 2017 Q1 2018 92,6 4,0 1,5 1,9 100,0" in p149
    narrow_2017 = [3.6, 3.5, 4.0]  # employed -> unemployed, t in 2017
    broad_2017 = [6.9, 6.8, 7.4]  # employed -> not employed (100 - retention)

    return {
        "source": (
            "Statistics South Africa, Labour Market Dynamics in South Africa, 2022, "
            "Report 02-11-02, Table 2.1a (p.15) and Table A.1 (p.149)"
        ),
        "basis": (
            "INDIVIDUALS aged 15-64 in the QLFS panel, not households. Quarterly "
            "transition between labour market states."
        ),
        "reference_transition": "Q3:2017 -> Q4:2017",
        "why_this_vintage": (
            "The 2022 edition reports the QLFS panel for 2017-2022, so a 2017 figure is "
            "available that is vintage-matched to the NIDS W5 population."
        ),
        "employed_at_t0_thousands": employed_t0,
        "counts_thousands": {
            "to_employed": to_employed,
            "to_unemployed": to_unemployed,
            "to_nea": to_nea,
        },
        "pct": {
            "retained_employed": pct_retained,
            "to_unemployed": pct_to_unemployed,
            "to_nea": pct_to_nea,
            "out_of_employment": pct_out_of_employment,
        },
        "range_2017": {
            "note": "All three transitions in Table A.1 whose t quarter falls in 2017.",
            "narrow_employed_to_unemployed_pct": narrow_2017,
            "broad_employed_to_not_employed_pct": broad_2017,
        },
        "model_target": {
            "note": (
                "D1 plausibility band for the fitted income-shock probability p. The "
                "model shock is the loss of the household wage component for one tick, "
                "so the analogue is a separation from employment. The NARROW measure "
                "(employed -> unemployed) is the lower bound; the BROAD measure "
                "(employed -> not employed, i.e. including discouraged and other NEA) "
                "is the upper bound. p is FITTED to CCMR arrears, then reported "
                "against this band. It is not fitted to this band."
            ),
            "ticks_per_quarter": round(TICKS_PER_QUARTER, 4),
            "tick_days": TICK_DAYS,
            "p_tick_lower": round(quarterly_to_tick_hazard(min(narrow_2017) / 100), 6),
            "p_tick_upper": round(quarterly_to_tick_hazard(max(broad_2017) / 100), 6),
            "p_tick_central_narrow": round(
                quarterly_to_tick_hazard(pct_to_unemployed / 100), 6
            ),
            "p_tick_central_broad": round(
                quarterly_to_tick_hazard(pct_out_of_employment / 100), 6
            ),
        },
        "caveats": [
            (
                "UNIT MISMATCH. These are INDIVIDUAL transition rates; the model shocks a "
                "HOUSEHOLD. A household with several earners faces a higher probability "
                "that at least one earner separates, so the household-level hazard is at "
                "or above the individual rate. Treat as an order-of-magnitude band, in "
                "the same way as the account-versus-household mismatch on the CCMR target."
            ),
            (
                "The band is a PLAUSIBILITY CHECK on a fitted parameter, not a second "
                "calibration target. p is fitted to CCMR arrears; fitting it to both "
                "would over-determine the baseline."
            ),
            (
                "The model shock is non-persistent (one tick), whereas a QLFS separation "
                "may persist for several quarters. The band therefore bounds the rate of "
                "shock ONSET, not the stock of unemployed households."
            ),
            (
                "Q1:2017 -> Q2:2017 is not in Table A.1; the 2017 range is taken over the "
                "three transitions whose t quarter falls in 2017."
            ),
        ],
    }


def main() -> None:
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / DEFAULT_PDF
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / DEFAULT_OUT

    if not pdf.is_file():
        sys.exit(f"Error: source PDF not found: {pdf}")

    payload = extract(pdf)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    mt = payload["model_target"]
    print(f"wrote {out}")
    print(f"  Q3:2017 -> Q4:2017 employment retention : {payload['pct']['retained_employed']}%")
    print(f"  employed -> unemployed                  : {payload['pct']['to_unemployed']}%")
    print(f"  employed -> not employed                : {payload['pct']['out_of_employment']}%")
    print(
        f"  implied per-tick hazard band for p      : "
        f"{mt['p_tick_lower']:.4%} to {mt['p_tick_upper']:.4%}"
    )


if __name__ == "__main__":
    main()
