"""Survey helpers shared by the data-layer notebooks and the figure script.

Two things that were copy-pasted three and four times over: the weighted Gini behind the
inequality checks, and the FinScope 2019 donor load (income midpoints, per-capita quintile
cut, flag recode). Put the repo root on sys.path once, then:

    from notebooks.scripts.survey_common import load_finscope, wgini

Self-check:  ./env/python.exe notebooks/scripts/survey_common.py
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike

FINSCOPE_CSV = "data/raw/FINMARK_2019/Finscope South Africa 2019.csv"

#: FinScope M13_MHI_Imputed band -> monthly household income midpoint. Only the RANKING
#: this produces is used (the quintile cut), never the amounts, so the survey's vintage
#: cannot leak into the 2017-Rand model.
_INCOME_MIDPOINTS = {
    "No Income": 0, "R1 - R999": 500, "R1 000 - R2 999": 2000, "R3 000 - R7 999": 5500,
    "R8 000 - R11 999": 10000, "R12 000 - R29 999": 21000, "R30 000 or more": 40000,
}

#: The six imputed flags: F1 (banked) plus the five credit products the model carries.
_PRODUCT_COLS = ["G10", "G11", "G12", "G13", "G14"]


def wgini(x: ArrayLike, w: ArrayLike) -> float:
    """Weighted Gini coefficient: one minus twice the area under the Lorenz curve."""
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    o = np.argsort(x)
    x, w = x[o], w[o]
    cw, cxw = np.cumsum(w), np.cumsum(x * w)
    return 1 - np.sum((cxw[1:] + cxw[:-1]) * np.diff(cw)) / (cxw[-1] * cw[-1])


def load_finscope(root: Path, bounds: Sequence[float]) -> pd.DataFrame:
    """FinScope 2019 donors with per-capita income, income quintile and the six flags.

    Positive-weight households only. Per-capita income is the M13 band midpoint over
    `Number_in_HH` (a household of zero is missing, not a household of one), and `bounds`
    are the NIDS backbone's per-capita quintile cut-points. `F1` and `G10`-`G14` are
    recoded to booleans as `banked` and the five product flags.
    """
    fs = pd.read_csv(root / FINSCOPE_CSV, usecols=[
        "HH_WEIGHT16", "Province", "Number_in_HH", "M13_MHI_Imputed", "F1", *_PRODUCT_COLS])
    fs = fs[fs.HH_WEIGHT16 > 0].copy()
    hhsize = pd.to_numeric(fs.Number_in_HH, errors="coerce").replace(0, np.nan)
    fs["income_pc"] = fs.M13_MHI_Imputed.map(_INCOME_MIDPOINTS) / hhsize
    fs = fs.dropna(subset=["income_pc"])
    fs["income_quintile"] = pd.cut(fs.income_pc, [-np.inf, *bounds, np.inf],
                                   labels=[f"Q{i}" for i in range(1, 6)], include_lowest=True)
    fs["banked"] = fs.F1 == "Yes"
    for c in _PRODUCT_COLS:
        fs[c] = fs[c] == "Yes"
    return fs


if __name__ == "__main__":
    # The estimator omits the Lorenz segment from the origin, so perfect equality lands
    # at 1/n^2 rather than exactly zero. Tolerances below allow for that, nothing more.
    assert wgini([1.0] * 1000, [1.0] * 1000) < 1e-5, "equal incomes must give a Gini of 0"
    assert wgini([0.0] * 999 + [1.0], [1.0] * 1000) > 0.99, "one holder must give a Gini of 1"
    print("survey_common: wgini self-check passed")
