"""Derive the BNPL-financeable share of household discretionary expenditure from IES 2022/23.

**What this replaces.** `bnpl_purchase_mean` was a single flat constant taken from trade
press (R1,568) and applied to every household, which put the poorest banked households in
the model making single BNPL purchases worth more than their entire monthly discretionary
budget (DEFECTS.md **B30**). This script supplies the quantity that lets purchase size be
**household-relative and data-derived** instead: the share of a household's discretionary
budget that goes on the categories BNPL actually finances.

Source: Statistics South Africa, *Income and Expenditure Survey 2022/2023*, household
microdata (DataFirst `zaf-statssa-ies-2022-2023-v1`), COICOP 2018 coded, annualised and
adjusted values. 19,940 households, weighted to ~21.3m.

**Vintage is handled the same way FinScope 2019 is handled.** Only a *ratio* is taken from
this survey, never a money amount, so the 2022/23 vintage cannot contaminate a 2017-Rand
model. That is the identical argument already made and accepted for the FinScope
categorical flags in P2.

**Category mapping.** BNPL in South Africa finances semi-durable and durable goods —
apparel, homeware and appliances, consumer electronics, sporting goods — which is what
both major providers' merchant networks sell. Mapped onto COICOP 2018:

    03      Clothing and footwear                       (all)
    05.1-.5 Furniture, textiles, appliances, utensils, tools
    08.1    Information and communication equipment     (devices, not airtime or data)
    09.1-.2 Recreational durables and other recreational goods

Excluded deliberately: 05.6 (routine household maintenance goods and services), 08.2-.3
(software and communication services), and every service group in 09. The result is
insensitive to the division 09 groups either way, which the script reports.

**Denominator.** The model's `expenditure_discretionary` is NIDS non-food expenditure less
rent, so the matching IES denominator is total consumption less food (division 01) and
less actual rentals (04.1). Imputed rentals (04.2) are removed from BOTH sides, since
NIDS non-food expenditure does not carry an imputed rent for owner-occupiers.

The script asserts Stats SA's own published headline for this survey — clothing and
footwear at 5.0% of total household consumption expenditure — so the extraction cannot
silently drift. Same discipline as `ccmr_2017_baseline.json` and `qlfs_2017_labour_flows.json`.

Usage:
    python notebooks/scripts/extract_ies_bnpl_share.py [ies_csv] [out_json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DEFAULT_CSV = Path("data/raw/IES_2022/ies_22_23.csv")
DEFAULT_OUT = Path("data/config/ies_2022_bnpl_share.json")

#: COICOP 2018 groups treated as BNPL-financeable, as (division, groups or None for all).
BNPL_GROUPS: dict[int, tuple[int, ...] | None] = {
    3: None,                       # clothing and footwear, in full
    5: (51, 52, 53, 54, 55),       # furniture, textiles, appliances, utensils, tools
    8: (81,),                      # ICT equipment: devices only
    9: (91, 92),                   # recreational durables and other recreational goods
}

FOOD_DIVISION = 1                 # division 01, food and non-alcoholic beverages
ACTUAL_RENT_GROUP = 41            # 04.1 actual rentals for housing
IMPUTED_RENT_GROUP = 42           # 04.2 imputed rentals, removed from both sides

#: Stats SA's published headline for IES 2022/23, used as the drift check.
PUBLISHED_CLOTHING_FOOTWEAR_PCT = 5.0
CLOTHING_TOLERANCE_PCT = 0.5


def find_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for d in [start, *start.parents]:
        if (d / "data" / "config").is_dir():
            return d
    raise FileNotFoundError("could not locate repo root (data/config missing)")


def load_consumption(csv: Path) -> pd.DataFrame:
    """Household x (division, group) consumption, with the survey weight recovered.

    The file carries both the raw annualised value and the weighted value, so the
    household weight is their ratio. Recovering it this way rather than joining a
    separate weights file means the weight can never be mismatched to the record.
    """
    df = pd.read_csv(
        csv,
        usecols=[
            "UQNO",
            "coicoptype",
            "division",
            "group",
            "valueannualized_adj",
            "valueannualized_adj_wgt",
        ],
    )
    df = df[df["coicoptype"] == "Consumption"].copy()
    df["weight"] = np.where(
        df["valueannualized_adj"].abs() > 1e-9,
        df["valueannualized_adj_wgt"] / df["valueannualized_adj"],
        np.nan,
    )
    return df


def main() -> None:
    root = find_root(Path(__file__).resolve().parent)
    csv = root / (sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV)
    out_path = root / (sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT)

    df = load_consumption(csv)
    weight = df.groupby("UQNO")["weight"].median()

    def wsum(mask: pd.Series) -> float:
        """Weighted total spending over the rows selected by `mask`."""
        sub = df[mask]
        w = weight.reindex(sub["UQNO"]).to_numpy()
        return float((sub["valueannualized_adj"].to_numpy() * w).sum())

    imputed_rent = df["group"] == IMPUTED_RENT_GROUP
    total_all = wsum(pd.Series(True, index=df.index))
    total = wsum(~imputed_rent)                      # the comparable total
    food = wsum(df["division"] == FOOD_DIVISION)
    rent = wsum(df["group"] == ACTUAL_RENT_GROUP)
    discretionary = total - food - rent

    bnpl_mask = pd.Series(False, index=df.index)
    for division, groups in BNPL_GROUPS.items():
        in_div = df["division"] == division
        bnpl_mask |= in_div if groups is None else (in_div & df["group"].isin(groups))
    bnpl = wsum(bnpl_mask)

    # Robustness: division 09 contributes very little, so the mapping's one genuinely
    # arguable inclusion should be shown not to matter.
    no_div9 = bnpl_mask & (df["division"] != 9)
    bnpl_excl_9 = wsum(no_div9)

    clothing_pct = 100.0 * wsum(df["division"] == 3) / total_all
    assert abs(clothing_pct - PUBLISHED_CLOTHING_FOOTWEAR_PCT) < CLOTHING_TOLERANCE_PCT, (
        f"clothing and footwear extracted at {clothing_pct:.2f}% of consumption against "
        f"Stats SA's published {PUBLISHED_CLOTHING_FOOTWEAR_PCT}%; the extraction has "
        "drifted from its source"
    )

    share = bnpl / discretionary
    share_excl_9 = bnpl_excl_9 / discretionary

    # Does one national ratio do violence to the distribution? Reported by expenditure
    # quintile so the thesis can say whether a single kappa is defensible.
    hh_total = df[~imputed_rent].groupby("UQNO")["valueannualized_adj"].sum()
    hh_bnpl = df[bnpl_mask].groupby("UQNO")["valueannualized_adj"].sum().reindex(
        hh_total.index, fill_value=0.0
    )
    hh_food = df[df["division"] == FOOD_DIVISION].groupby("UQNO")[
        "valueannualized_adj"
    ].sum().reindex(hh_total.index, fill_value=0.0)
    hh_rent = df[df["group"] == ACTUAL_RENT_GROUP].groupby("UQNO")[
        "valueannualized_adj"
    ].sum().reindex(hh_total.index, fill_value=0.0)
    hh_disc = hh_total - hh_food - hh_rent
    hh_w = weight.reindex(hh_total.index)

    quintile = pd.qcut(hh_total, 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])
    by_quintile = {}
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        sel = quintile == q
        num = float((hh_bnpl[sel] * hh_w[sel]).sum())
        den = float((hh_disc[sel] * hh_w[sel]).sum())
        by_quintile[q] = round(num / den, 6) if den > 0 else 0.0

    payload = {
        "source": (
            "Statistics South Africa, Income and Expenditure Survey 2022/2023 household "
            "microdata (DataFirst zaf-statssa-ies-2022-2023-v1), COICOP 2018."
        ),
        "n_households": int(df["UQNO"].nunique()),
        "weighted_households": round(float(weight.sum())),
        "vintage_note": (
            "Only a RATIO is taken from this survey, never a money amount, so the "
            "2022/23 vintage cannot contaminate the 2017-Rand model. Identical "
            "treatment to the FinScope 2019 categorical flags in P2."
        ),
        "category_mapping": {
            "included": {str(d): (list(g) if g else "all") for d, g in BNPL_GROUPS.items()},
            "excluded_note": (
                "05.6 routine household maintenance, 08.2-08.3 software and "
                "communication services, and all service groups in 09."
            ),
        },
        "drift_check": {
            "clothing_footwear_pct_of_consumption": round(clothing_pct, 3),
            "statssa_published_pct": PUBLISHED_CLOTHING_FOOTWEAR_PCT,
        },
        "aggregates_pct_of_comparable_total": {
            "food": round(100.0 * food / total, 3),
            "actual_rent": round(100.0 * rent / total, 3),
            "discretionary": round(100.0 * discretionary / total, 3),
            "bnpl_financeable": round(100.0 * bnpl / total, 3),
        },
        "by_expenditure_quintile": by_quintile,
        "robustness": {
            "share_excluding_division_09": round(share_excl_9, 6),
            "note": "Division 09 moves the share by well under a percentage point.",
        },
        "model_target": {
            #: kappa in `bnpl_purchase_ratio`: a BNPL purchase is the scale of one
            #: month of the household's own spending in BNPL-financeable categories.
            "bnpl_financeable_share_of_discretionary": round(share, 6),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"  clothing and footwear    : {clothing_pct:.2f}% of consumption "
          f"(published {PUBLISHED_CLOTHING_FOOTWEAR_PCT}%)")
    print(f"  BNPL-financeable         : {100 * bnpl / total:.2f}% of comparable total")
    print(f"  discretionary            : {100 * discretionary / total:.2f}% of comparable total")
    print(f"  SHARE OF DISCRETIONARY   : {share:.4f}  (excl. div 09: {share_excl_9:.4f})")
    print(f"  by expenditure quintile  : {by_quintile}")


if __name__ == "__main__":
    main()
