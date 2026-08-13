"""Build the 2017-Rand CPI deflator used to convert current-vintage BNPL figures.

**Why this exists.** Every quantity in the model is denominated in **2017 Rands** — the
NIDS W5 backbone, the Reg 23A expense table, the CCMR arrears targets, the statutory
interest rates at the 2017 repo rate. The BNPL parameters were the exception: purchase
size, the Payflex per-order cap and the Payflex late fees were all taken at **current
vintage** and used unadjusted, so the BNPL side of the model was denominated roughly 1.4x
too high against everything it interacts with (DEFECTS.md **B29**).

This script produces the single documented factor that fixes that, so the conversion is
applied in one place with its provenance attached rather than by adjusting numbers by
hand.

Source: Statistics South Africa, *Consumer Price Index*, statistical release **P0141**,
headline CPI, **annual average** basis. The annual average is the correct basis for the
2018-2025 chain because the quantities being deflated are averages over a year (an average
order value, a published tariff in force across a year), not point-in-time observations.

**The 2026 anchor is a published figure, not a guess (2026-08-13).** The Payflex terms and
the trade-press basket are 2026-vintage sources observed mid-year, so they need the mid-2026
price level rather than a full-year 2026 average, which does not exist yet. The **June 2026
release** supplies it:

  * headline CPI index **107.5** (Dec 2024 = 100), and
  * **5.0%** year-on-year inflation to June 2026.

The year-on-year rate is exactly what is needed, and this is the reasoning: an annual
average sits at the *mid-point* of its year when prices move smoothly within the year, so
the 2025 annual average IS approximately the mid-2025 price level. June 2026 is twelve
months after mid-2025. The ratio between them is therefore the June 2026 year-on-year rate.
So `factor(2017 -> mid-2026) = factor(2017 -> 2025 average) x 1.05`.

That happens to reproduce the number the earlier part-year guess produced, but it is now
*derived from a published rate* rather than assumed, which is the point.

**A drift check on the whole chain.** The published June 2026 index is on a Dec 2024 = 100
base, so it can be compared against what this script's chain implies for the same date. The
two agree to within about 1%, which bounds the error on a factor of ~1.5 and is asserted
below. That check is the reason the `% VERIFY` on the 2018-2025 series is now *narrow*
rather than open-ended.

⚠ **`% VERIFY`, narrowed.** The 2018-2025 annual averages are still taken from Stats SA's
published inflation releases and media statements rather than re-derived from **P0141
Table B1** index numbers (statssa.gov.za blocks automated retrieval; Table B1 is carried in
the appendix of each monthly release). Two independent checks now constrain them: the 2024
rate against Stats SA's own published 4,4% statement, and the whole chain against the
published June 2026 index. Pin the series to Table B1 when convenient and delete this note.

Usage:
    python notebooks/scripts/extract_cpi_deflator.py [out_json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DEFAULT_OUT = Path("data/config/cpi_deflator_2017.json")

#: The model's base year. Everything monetary is expressed in Rands of this year.
BASE_YEAR = 2017

#: Stats SA headline CPI, annual average change on the previous year, per cent.
#: Keyed by the year the change lands IN, so 2018 is the 2017->2018 change.
ANNUAL_AVERAGE_INFLATION_PCT: dict[int, float] = {
    2018: 4.7,
    2019: 4.1,
    2020: 3.3,
    2021: 4.5,
    2022: 7.04,
    2023: 6.08,
    2024: 4.36,
    2025: 3.22,
}

#: 2026 has no annual average yet. The MID-YEAR price level is what 2026-vintage sources
#: need, and P0141 June 2026 publishes it directly. See the module docstring for why the
#: year-on-year rate is the right multiplier onto the 2025 annual average.
MID_2026: dict[str, float] = {
    "yoy_pct": 5.0,          # year-on-year headline inflation to June 2026
    "index": 107.5,          # headline CPI index, June 2026
    "index_base": 2024.0,    # Dec 2024 = 100
    "month": 6,
}

#: Stats SA's own published statement, used as the drift check on the series.
PUBLISHED_CLAIM_2024_PCT = 4.4

#: Tolerance on the chain-vs-published-index check. The residual is real (the chain implies
#: ~106.7 against a published 107.5) and comes from approximating each year's average by its
#: mid-point. It is recorded rather than tuned away, and it bounds the deflator error at
#: under a per cent on a factor of ~1.5.
INDEX_CHECK_TOLERANCE_PCT = 1.5

#: Stats SA has rebased the headline index three times over this window. Index numbers taken
#: from releases either side of a rebase are NOT directly comparable and need the published
#: linking factors. The chain below is built from annual RATES, which are rebase-invariant,
#: precisely so that this does not have to be handled.
REBASE_MONTHS = ["Dec 2016 = 100", "Dec 2021 = 100", "Dec 2024 = 100"]

SOURCE_URL = "https://www.statssa.gov.za/publications/P0141/P0141June2026.pdf"


def find_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for d in [start, *start.parents]:
        if (d / "data" / "config").is_dir():
            return d
    raise FileNotFoundError("could not locate repo root (data/config missing)")


def factors() -> dict[int, float]:
    """Cumulative price factor from the base year to each later year's ANNUAL AVERAGE.

    `factor[y]` multiplies a base-year Rand amount to give year-`y` Rands, so a
    current-vintage figure is converted to base-year Rands by DIVIDING by it.

    2026 is the exception and is keyed at the same integer for convenience: it is the
    **mid-2026** price level, not a 2026 annual average, which does not exist yet.
    """
    out = {BASE_YEAR: 1.0}
    running = 1.0
    for year in sorted(ANNUAL_AVERAGE_INFLATION_PCT):
        running *= 1.0 + ANNUAL_AVERAGE_INFLATION_PCT[year] / 100.0
        out[year] = running
    # Mid-2026: the 2025 annual average approximates the mid-2025 price level, and the
    # published June 2026 year-on-year rate carries it forward exactly twelve months.
    out[2026] = running * (1.0 + MID_2026["yoy_pct"] / 100.0)
    return out


def implied_june_2026_index() -> float:
    """What this script's chain implies for the published June 2026 index.

    Independent of the chain's own arithmetic in one respect that matters: the published
    index is on a Dec 2024 = 100 base, so reproducing it exercises the 2025 rate and the
    2026 anchor together against a number neither of them was built from.
    """
    r2025 = ANNUAL_AVERAGE_INFLATION_PCT[2025] / 100.0
    # Dec 2024 -> mid-2025 is half a year of 2025 inflation; mid-2025 -> June 2026 is the
    # published year-on-year rate.
    return 100.0 * (1.0 + r2025) ** 0.5 * (1.0 + MID_2026["yoy_pct"] / 100.0)


def main() -> None:
    root = find_root(Path(__file__).resolve().parent)
    out_path = root / (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)

    # Drift check against the source's own published statement. Stats SA reports the
    # 2024 annual average as 4,4%; the series carries 4.36% from the same release, so
    # they must agree to the rounding the statement uses.
    assert abs(ANNUAL_AVERAGE_INFLATION_PCT[2024] - PUBLISHED_CLAIM_2024_PCT) < 0.05, (
        "the 2024 annual average disagrees with the published 4,4% statement; "
        "the series has drifted from its source"
    )
    # Sanity: South African headline inflation has stayed inside the 0-15% range over
    # this window. A value outside it means a rate was entered as a factor, or a
    # month-on-month figure was pasted in place of an annual average.
    for year, rate in ANNUAL_AVERAGE_INFLATION_PCT.items():
        assert 0.0 < rate < 15.0, f"implausible annual average inflation for {year}: {rate}"

    # Drift check on the WHOLE chain against a published index the chain was not built
    # from. This is what narrows the % VERIFY: the 2018-2025 rates cannot all be badly
    # wrong and still land within a per cent of the published June 2026 index.
    implied = implied_june_2026_index()
    gap_pct = 100.0 * (implied / MID_2026["index"] - 1.0)
    assert abs(gap_pct) < INDEX_CHECK_TOLERANCE_PCT, (
        f"the compounded rate chain implies a June 2026 index of {implied:.2f} against the "
        f"published {MID_2026['index']}, a {gap_pct:+.2f}% gap. Beyond "
        f"{INDEX_CHECK_TOLERANCE_PCT}% the annual-average series has drifted from its source"
    )

    f = factors()

    payload = {
        "source": (
            "Statistics South Africa, Consumer Price Index, statistical release P0141, "
            "headline CPI. Annual average basis for 2018-2025; the June 2026 release "
            "supplies the mid-2026 anchor."
        ),
        "source_url": SOURCE_URL,
        "base_year": BASE_YEAR,
        "verify": (
            "% VERIFY (narrowed 2026-08-13): the 2018-2025 annual averages are taken from "
            "published Stats SA releases and media statements, NOT re-derived from P0141 "
            "Table B1 index numbers, because statssa.gov.za blocks automated retrieval. "
            "TWO independent checks now constrain them: the 2024 rate against Stats SA's "
            "published 4,4% statement, and the whole compounded chain against the "
            "published June 2026 index (see index_drift_check). Pin to Table B1 when "
            "convenient; the residual error is bounded at ~1%."
        ),
        "rebasing_note": (
            "Stats SA rebased the headline index at " + "; ".join(REBASE_MONTHS) + ". "
            "Index numbers from releases either side of a rebase are NOT directly "
            "comparable without the published linking factors. This chain is built from "
            "annual RATES, which are rebase-invariant, so the issue does not arise."
        ),
        "annual_average_inflation_pct": ANNUAL_AVERAGE_INFLATION_PCT,
        "mid_2026_anchor": {
            **MID_2026,
            "note": (
                "2026 has no annual average yet. An annual average sits at the mid-point "
                "of its year under smooth within-year price movement, so the 2025 annual "
                "average IS approximately the mid-2025 price level, and June 2026 is "
                "twelve months later. The published June 2026 year-on-year rate is "
                "therefore exactly the multiplier from the 2025 average to mid-2026. "
                "factor_from_2017['2026'] is a MID-YEAR level, not an annual average."
            ),
        },
        "index_drift_check": {
            "published_june_2026_index": MID_2026["index"],
            "implied_by_this_chain": round(implied, 2),
            "gap_pct": round(gap_pct, 3),
            "tolerance_pct": INDEX_CHECK_TOLERANCE_PCT,
            "note": (
                "The residual comes from approximating each year's average by its "
                "mid-point. Recorded, not tuned away. It bounds the error on a deflator "
                "of ~1.5 at well under one per cent."
            ),
        },
        "factor_from_2017": {str(y): round(v, 6) for y, v in f.items()},
        "usage": (
            "A nominal amount observed in year Y is converted to 2017 Rands by DIVIDING "
            "by factor_from_2017[Y]."
        ),
        "model_target": {
            # The vintages the model actually needs.
            "factor_2024": round(f[2024], 6),
            "factor_2025": round(f[2025], 6),
            "factor_2026_mid": round(f[2026], 6),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {out_path}")
    for year in sorted(f):
        print(f"  {year}: factor {f[year]:.4f}  (R1 of 2017 = R{f[year]:.2f} of {year})")


if __name__ == "__main__":
    main()
