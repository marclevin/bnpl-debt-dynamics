"""Reproduce two figures the reference audit (docs/REFERENCE_AUDIT.md, R9 and R20) put in the thesis.

    .venv/bin/python notebooks/scripts/check_reference_audit_figures.py

R9: NIDS financial debt (w5_f_deb, the model's D_trad) includes informal loans. Adult-file
balances from friends (g21), mashonisas (g22) and family (g20) are summed by household and
compared with weighted w5_f_deb.
R20: the per-capita income Gini weighted by household (as in Table pop-external) and by
person (household weight times household size, as Stats SA and Hundenborn et al. compute it).
Writes results/summary/reference_audit_checks.json.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
NIDS = ROOT / "data/raw/NIDS_W5"
BAL = {"bnk": "w5_a_dtbnk_b", "mic": "w5_a_dtmic_b", "stubnk": "w5_a_dtstubnk_b", "stuo": "w5_a_dtstuo_b",
       "cre": "w5_a_dtcre_b", "str": "w5_a_dtstr_b", "hp": "w5_a_dthp_b", "fam": "w5_a_dtflloan_b",
       "fr": "w5_a_dtfrloanbal", "msh": "w5_a_dtmsh_b", "emp": "w5_a_dtemploan_b",
       "oth1": "w5_a_dtoth1_b", "oth2": "w5_a_dtoth2_b"}


def wgini(x, w) -> float:
    o = np.argsort(x)
    x, w = np.asarray(x, float)[o], np.asarray(w, float)[o]
    p = np.r_[0, np.cumsum(w) / w.sum()]
    lor = np.r_[0, np.cumsum(x * w) / (x * w).sum()]
    return float(1 - np.sum((p[1:] - p[:-1]) * (lor[1:] + lor[:-1])))


def informal_debt() -> dict:
    a = pd.read_stata(NIDS / "Adult_W5_Anon_V1.0.0.dta", columns=["w5_hhid", *BAL.values()],
                      convert_categoricals=False)
    for k, v in BAL.items():
        a[k] = pd.to_numeric(a[v], errors="coerce")
        a.loc[a[k] < 0, k] = np.nan  # negative codes are missing or refused
        a[k] = a[k].fillna(0)
    h = a.groupby("w5_hhid")[list(BAL)].sum()
    d = pd.read_stata(NIDS / "hhderived_W5_Anon_V1.0.0.dta", columns=["w5_hhid", "w5_wgt", "w5_f_deb"],
                      convert_categoricals=False).set_index("w5_hhid")
    m = d.join(h, how="left").fillna({c: 0 for c in BAL})
    w = pd.to_numeric(m.w5_wgt, errors="coerce").fillna(0)
    f_deb = pd.to_numeric(m.w5_f_deb, errors="coerce").fillna(0)
    total = (w * f_deb).sum()
    out = {f"households_with_{lab}_debt_weighted": float((w * (m[c] > 0)).sum() / w.sum())
           for c, lab in (("msh", "mashonisa"), ("fr", "friend"), ("fam", "family"))}
    out["friend_mashonisa_share_of_f_deb_weighted"] = float((w * (m.fr + m.msh)).sum() / total)
    out["friend_mashonisa_family_share_of_f_deb_weighted"] = float((w * (m.fr + m.msh + m.fam)).sum() / total)
    return out


def gini() -> dict:
    d = pd.read_stata(NIDS / "hhderived_W5_Anon_V1.0.0.dta", columns=["w5_hhincome", "w5_hhsizer", "w5_wgt"],
                      convert_categoricals=False).dropna()
    d = d[(d.w5_hhincome > 0) & (d.w5_wgt > 0) & (d.w5_hhsizer > 0)]
    pc = d.w5_hhincome / d.w5_hhsizer
    return {"n_households": int(len(d)), "gini_household_weighted": wgini(pc, d.w5_wgt),
            "gini_person_weighted": wgini(pc, d.w5_wgt * d.w5_hhsizer)}


if __name__ == "__main__":
    out = {"R9_informal_debt": informal_debt(), "R20_gini": gini()}
    dest = ROOT / "results/summary/reference_audit_checks.json"
    dest.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
