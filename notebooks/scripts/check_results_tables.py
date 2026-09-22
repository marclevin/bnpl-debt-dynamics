"""Re-derive three numbers per generated table straight from results/raw and assert that each
appears, formatted, in the fragment build_results_tables.py wrote.

    ./env/python.exe notebooks/scripts/check_results_tables.py

Deliberately uses plain pandas and none of results_common's helpers, so a wrong helper
cannot agree with itself. Fails loudly on the first mismatch.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw"
GEN = ROOT / "thesis" / "chapters" / "generated"
SUMMARY = ROOT / "results" / "summary"

checked = 0


def frag(name: str) -> str:
    return (GEN / f"{name}.tex").read_text(encoding="utf-8")


def expect(name: str, text: str, needle: str) -> None:
    global checked
    assert needle in text, f"{name}: expected {needle!r} in the fragment"
    checked += 1


def cell(x: pd.Series, d: int = 2, scale: float = 100.0) -> str:
    return f"{x.mean() * scale:.{d}f} ({x.std(ddof=1) * scale:.{d}f})"


def pm(a: pd.Series, b: pd.Series, d: int = 2) -> str:
    diff = (a.mean() - b.mean()) * 100
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)) * 100
    return f"${diff:+.{d}f} \\pm {se:.{d}f}$"


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (pd.read_parquet(RAW / f"{n}.parquet") for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    off, b0, b1 = (rq0[rq0.label == l] for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))

    t = frag("tab_baseline_arms")
    expect("baseline_arms", t, cell(off.default_rate_final))
    expect("baseline_arms", t, cell(b1.bnpl_adoption_final))
    expect("baseline_arms", t, pm(b0.default_rate_final, off.default_rate_final))

    t = frag("tab_stacking")
    n4b0 = rq1[(rq1.n_platforms == 4) & (rq1.beta == 0.0)]
    n1b1 = rq1[(rq1.n_platforms == 1) & (rq1.beta == 1.0)]
    n6b1 = rq1[(rq1.n_platforms == 6) & (rq1.beta == 1.0)]
    expect("stacking", t, f"4 & {n4b0.stacking_2plus_final.mean() * 100:.1f} &")
    expect("stacking", t, cell(n1b1.default_rate_final))
    expect("stacking", t, pm(n6b1.default_rate_final, n1b1.default_rate_final))

    t = frag("tab_stacking_full")
    n3b2 = rq1[(rq1.n_platforms == 3) & (rq1.beta == 2.0)]
    expect("stacking_full", t, f"& {n3b2.stacking_2plus_final.mean() * 100:.1f} &")
    expect("stacking_full", t, f"& {n3b2.default_rate_final.mean() * 100:.2f} &")
    expect("stacking_full", t, f"& {rq1[(rq1.n_platforms == 6) & (rq1.beta == 0.5)].default_rate_final.mean() * 100:.2f} &")

    t = frag("tab_bnpl_on_checks")
    mp = b0.bnpl_purchase_mean_realised.mean()
    expect("bnpl_on_checks", t, "R" + f"{mp:,.2f}".replace(",", "{,}"))
    expect("bnpl_on_checks", t, f"{off.zero_savings_rate_mean.mean() * 100:.1f}\\%")
    expect("bnpl_on_checks", t, pm(b0.trad_arrears_rate_mean, off.trad_arrears_rate_mean))

    t = frag("tab_scenarios")
    bur0 = rq3[rq3.label == "rq3_bureau_b0.0"]
    ben0 = rq3[rq3.label == "rq3_kcool0_b0.0"]
    aff1 = rq3[rq3.label == "rq3_afford_b1.0"]
    expect("scenarios", t, cell(bur0.default_rate_final))
    expect("scenarios", t, cell(aff1.bnpl_volume_cumulative, 2, 1e-6))
    expect("scenarios", t, pm(bur0.default_rate_final, ben0.default_rate_final))
    expect("scenarios", t, cell(aff1.default_rate_final_Q1))

    t = frag("tab_distribution")
    expect("distribution", t, cell(b0.default_rate_final_Q1))
    expect("distribution", t, f"& {b0.bnpl_rolling_bind_Q5.mean() * 100:.1f} &")
    expect("distribution", t, f"& {b0.bnpl_purchase_mean_realised_Q3.mean():.0f} \\\\")

    t = frag("tab_access")
    lo = rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 0.0)].default_rate_final
    hi = rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 1.0)].default_rate_final
    expect("access", t, pm(hi, lo))
    g = rq2[rq2.beta == 3.0].groupby("bnpl_access_rate").default_rate_final.mean().sort_index()
    xs = np.asarray(g.index, dtype=float)
    slope, icpt = np.polyfit(xs, g.values, 1)
    r2 = 1 - ((g.values - (slope * xs + icpt)) ** 2).sum() / ((g.values - g.values.mean()) ** 2).sum()
    expect("access", t, f"{r2:.3f}")
    mu = rq2t[rq2t.label == "rq2t_mu0.45"]
    expect("access", t, cell(mu.bnpl_adoption_final, 1))

    t = frag("tab_robustness")
    expect("robustness", t, cell(rob[rob.label == "rob_k4"].default_rate_final))
    expect("robustness", t, cell(rob[rob.label == "rob_amount_shortfall_plus_committed"].default_rate_final))
    cap = rob[rob.label == "rob_amount_shortfall"].set_index("seed").default_rate_final
    unc = rob[rob.label == "rob_amount_shortfall_uncapped"].set_index("seed").default_rate_final
    d = (unc - cap.reindex(unc.index)) * 100
    expect("robustness", t, f"${d.mean():+.2f} \\pm {d.std(ddof=1) / math.sqrt(len(d)):.2f}^\\dagger$")

    t = frag("tab_robustness_appendix")
    expect("robustness_appendix", t, cell(rob[rob.label == "rob_n1000"].default_rate_final))
    expect("robustness_appendix", t, cell(rob[rob.label == "rob_m0.2"].default_rate_final))
    expect("robustness_appendix", t, cell(rob[rob.label == "rob_shock_single_tick"].default_rate_final))

    t = frag("tab_sobol")
    sob = json.loads((SUMMARY / "sobol_indices.json").read_text(encoding="utf-8"))["indices"]
    sh = next(r for r in sob["default_rate_final"] if r["parameter"] == "shock_prob")
    qb = next(r for r in sob["bnpl_adoption_final"] if r["parameter"] == "q_base")
    expect("sobol", t, f"${sh['S1']:.2f} \\pm {sh['S1_conf']:.2f}$")
    expect("sobol", t, f"${sh['ST']:.2f} \\pm {sh['ST_conf']:.2f}$")
    expect("sobol", t, f"${qb['S1']:.2f} \\pm {qb['S1_conf']:.2f}$")

    t = frag("tab_cooloff")
    k4 = rq3[rq3.label == "rq3_kcool4_b1.0"]
    ben1 = rq3[rq3.label == "rq3_kcool0_b1.0"]
    expect("cooloff", t, cell(k4.default_rate_final))
    expect("cooloff", t, f"{(k4.bnpl_volume_cumulative.mean() / ben1.bnpl_volume_cumulative.mean() - 1) * 100:+.1f}")
    expect("cooloff", t, pm(k4.default_rate_final, ben1.default_rate_final))

    t = frag("tab_cap")
    c1 = rq3[rq3.label == "rq3_cap1_b0.0"]
    expect("cap", t, cell(c1.default_rate_final))
    expect("cap", t, pm(c1.default_rate_final, ben0.default_rate_final))
    expect("cap", t, f"& {c1.bnpl_adoption_final.mean() * 100:.1f} &")

    print(f"OK: {checked} numbers re-derived from results/raw match the generated fragments")


if __name__ == "__main__":
    main()
