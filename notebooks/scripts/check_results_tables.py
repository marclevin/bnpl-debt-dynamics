"""Re-derive three numbers per generated table straight from results/raw and assert that each
appears, formatted, in the fragment build_results_tables.py wrote.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py

Deliberately uses plain pandas and none of results_common's helpers, so a wrong helper
cannot agree with itself. Fails loudly on the first mismatch.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

#: Milestone 2 (#98): the peer-influence arm beside beta = 0. Table text prints it as 0.3.
from simulation.experiments import BETA_PEER as BP  # noqa: E402
assert BP == 0.30, "table text prints the peer arm as beta = 0.3; update it with BETA_PEER"


ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw"
GEN = ROOT / "thesis" / "chapters" / "generated"
SUMMARY = ROOT / "results" / "summary"

checked = 0


def frag(name: str) -> str:
    return (GEN / f"{name}.tex").read_text(encoding="utf-8")


def expect(name: str, text: str, needle: str) -> None:
    global checked
    # A difference beyond two standard errors is printed bold, so match it without its
    # math delimiters too (core).
    assert needle in text or (needle.startswith("$") and core(needle) in text), (
        f"{name}: expected {needle!r} in the fragment"
    )
    checked += 1


def cell(x: pd.Series, d: int = 2, scale: float = 100.0) -> str:
    return f"{x.mean() * scale:.{d}f} ({x.std(ddof=1) * scale:.{d}f})"


def core(x: str) -> str:
    """A difference without its math delimiters, so bold and plain cells both match."""
    return x.strip("$")


def pm(a: pd.Series, b: pd.Series, d: int = 2) -> str:
    diff = (a.mean() - b.mean()) * 100
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)) * 100
    return f"${diff:+.{d}f} \\pm {se:.{d}f}$"


def pmp(a: pd.DataFrame, b: pd.DataFrame, col: str, d: int = 2) -> str:
    """The same difference for two arms that share seeds: taken seed by seed."""
    x = a.set_index("seed")[col]
    y = b.set_index("seed")[col]
    assert sorted(x.index) == sorted(y.index), "arms do not share seeds"
    z = (x - y.reindex(x.index)) * 100
    return f"${z.mean():+.{d}f} \\pm {z.std(ddof=1) / math.sqrt(len(z)):.{d}f}$"


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (pd.read_parquet(RAW / f"{n}.parquet") for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    off, b0, b1 = (rq0[rq0.label == l] for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_peer"))

    t = frag("tab_baseline_arms")
    expect("baseline_arms", t, cell(off.default_rate_final))
    expect("baseline_arms", t, cell(b1.bnpl_adoption_final))
    expect("baseline_arms", t, pmp(b0, off, "default_rate_final"))

    t = frag("tab_stacking")
    n4b0 = rq1[(rq1.n_platforms == 4) & (rq1.beta == 0.0)]
    n1b1 = rq1[(rq1.n_platforms == 1) & (rq1.beta == BP)]
    n6b1 = rq1[(rq1.n_platforms == 6) & (rq1.beta == BP)]
    expect("stacking", t, f"4 & {(n4b0.stacking_2plus_final / n4b0.bnpl_adoption_final).mean() * 100:.1f} &")
    expect("stacking", t, f"& {n1b1.default_rate_final.mean() * 100:.2f} \\\\")
    expect("stacking", t, pmp(n6b1, n1b1, "default_rate_final"))

    t = frag("tab_stacking_full")
    n3b2 = rq1[(rq1.n_platforms == 3) & (rq1.beta == 0.2)]
    expect("stacking_full", t, f"& {n3b2.stacking_2plus_final.mean() * 100:.1f} &")
    expect("stacking_full", t, f"& {n3b2.default_rate_final.mean() * 100:.2f} &")
    expect("stacking_full", t, f"& {rq1[(rq1.n_platforms == 6) & (rq1.beta == 0.1)].default_rate_final.mean() * 100:.2f} &")

    t = frag("tab_bnpl_on_checks")
    mp = b0.bnpl_purchase_mean_realised.mean()
    expect("bnpl_on_checks", t, "R" + f"{mp:,.0f}".replace(",", "{,}") + " &")
    expect("bnpl_on_checks", t, f"{off.zero_savings_rate_mean.mean() * 100:.1f}\\%")
    expect("bnpl_on_checks", t, core(pmp(b0, off, "trad_arrears_rate_mean")))

    t = frag("tab_scenarios")
    rq3s = pd.read_parquet(RAW / "rq3s.parquet")
    bur0 = rq3s[rq3s.label == "rq3s_bureau_b0.0"]
    sben0 = rq3s[rq3s.label == "rq3s_bench_b0.0"]
    aff1 = rq3s[rq3s.label == f"rq3s_afford_b{BP}"]
    ben0 = rq3[rq3.label == "rq3_kcool0_b0.0"]
    assert len(bur0) == len(sben0) == len(aff1) == 100, "scenario arms need 100 replicates"
    expect("scenarios", t, f"& {sben0.default_rate_final.mean() * 100:.2f} &")
    expect("scenarios", t, core(pmp(bur0, sben0, "default_rate_final")))
    expect("scenarios", t, core(pmp(aff1, rq3s[rq3s.label == f"rq3s_bench_b{BP}"], "default_rate_final_Q1")))

    t = frag("tab_distribution")
    expect("distribution", t, core(pmp(rq0[rq0.label == "bnpl_on_peer"], off, "default_rate_final_Q4")))
    expect("distribution", t, f"& {b0.bnpl_rolling_bind_Q5.mean() * 100:.1f} &")
    expect("distribution", t, f"& {b0.bnpl_purchase_mean_realised_Q3.mean():.0f} \\\\")

    t = frag("tab_access")
    lo = rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 0.0)].default_rate_final
    hi = rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 1.0)].default_rate_final
    expect("access", t, pmp(rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 1.0)],
                            rq2[(rq2.beta == 0.0) & (rq2.bnpl_access_rate == 0.0)], "default_rate_final"))
    # the linear fit is printed only where the end-to-end change exceeds two standard errors
    z = (rq2[(rq2.beta == BP) & (rq2.bnpl_access_rate == 1.0)].set_index("seed").default_rate_final
         - rq2[(rq2.beta == BP) & (rq2.bnpl_access_rate == 0.0)].set_index("seed").default_rate_final)
    if abs(z.mean()) > 2 * z.std(ddof=1) / math.sqrt(len(z)):
        g = rq2[rq2.beta == BP].groupby("bnpl_access_rate").default_rate_final.mean().sort_index()
        xs = np.asarray(g.index, dtype=float)
        slope, icpt = np.polyfit(xs, g.values, 1)
        r2 = 1 - ((g.values - (slope * xs + icpt)) ** 2).sum() / ((g.values - g.values.mean()) ** 2).sum()
        expect("access", t, f"& {r2:.2f} \\\\")
    h = rq2[rq2.beta == BP].groupby("bnpl_access_rate").bnpl_adoption_final.mean().sort_index()
    expect("access", t, f"& {(h.iloc[-1] - h.iloc[0]) * 100:+.1f} &")

    t = frag("tab_robustness")
    expect("robustness", t, cell(rob[rob.label == "rob_k4"].default_rate_final))
    expect("robustness", t, cell(rob[rob.label == "rob_amount_shortfall_plus_committed"].default_rate_final))
    cap = rob[rob.label == "rob_amount_shortfall"].set_index("seed").default_rate_final
    unc = rob[rob.label == "rob_amount_shortfall_uncapped"].set_index("seed").default_rate_final
    d = (unc - cap.reindex(unc.index)) * 100
    expect("robustness", t, f"{d.mean():+.2f} \\pm {d.std(ddof=1) / math.sqrt(len(d)):.2f}")

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
    k4 = rq3[rq3.label == f"rq3_kcool4_b{BP}"]
    ben1 = rq3[rq3.label == f"rq3_kcool0_b{BP}"]
    expect("cooloff", t, cell(k4.default_rate_final))
    expect("cooloff", t, f"{(k4.bnpl_volume_cumulative.mean() / ben1.bnpl_volume_cumulative.mean() - 1) * 100:+.1f}")
    expect("cooloff", t, core(pmp(k4, ben1, "default_rate_final")))

    t = frag("tab_cap")
    c1 = rq3[rq3.label == "rq3_cap1_b0.0"]
    expect("cap", t, cell(c1.default_rate_final))
    expect("cap", t, core(pm(c1.default_rate_final, ben0.default_rate_final)))
    expect("cap", t, f"& {c1.bnpl_adoption_final.mean() * 100:.1f} &")

    t = frag("tab_scenarios")
    both0 = rq3s[rq3s.label == "rq3s_both_b0.0"]
    expect("scenarios", t, core(pmp(both0, sben0, "default_rate_final")))
    expect("scenarios", t, core(pmp(both0, sben0, "active_90_plus_mean")))

    t = frag("tab_effect")
    eff = pd.read_parquet(RAW / "effect.parquet")

    def paired(on_label: str, off_label: str) -> str:
        on = eff[eff.label == on_label].set_index("seed").default_rate_final
        off_ = eff[eff.label == off_label].set_index("seed").default_rate_final
        d = (on - off_.reindex(on.index)) * 100
        return f"{d.mean():+.2f} \\pm {d.std(ddof=1) / math.sqrt(len(d)):.2f}"

    expect("effect", t, f"& {eff[eff.label == 'eff_ref_off'].default_rate_final.mean() * 100:.2f} &")
    expect("effect", t, paired("eff_amountcommitted_b0.0", "eff_amountcommitted_off"))
    expect("effect", t, paired("eff_want_off_b0.0", "eff_ref_off"))

    print(f"OK: {checked} numbers re-derived from results/raw match the generated fragments")
    check_prose()


def check_prose() -> None:
    """Typed numbers in the results prose (#95, #100): each must match its JSON source, as printed.

    Covers the headline numbers that are typed rather than \\input from a fragment. A number is
    formatted from the JSON exactly as the text prints it and must appear in the named chapter.
    """
    global checked
    start = checked
    num = json.loads((SUMMARY / "results_numbers.json").read_text())
    sweep = json.loads((SUMMARY / "beta_sweep.json").read_text())
    cont = json.loads((SUMMARY / "contestable_default.json").read_text())
    dc = json.loads((SUMMARY / "defaulter_credit.json").read_text())
    ch = {n: (ROOT / "thesis" / "chapters" / f"{n}.tex").read_text(encoding="utf-8")
          for n in ("03_calibration", "04_results", "05_policy", "06_conclusion")}

    def pmj(d: dict, key: str, dp: int = 2) -> str:
        return f"{d[key] * 100:+.{dp}f} \\pm {d[key + '_se'] * 100:.{dp}f}"

    def unsigned(s: str) -> str:
        return s.lstrip("+")

    # Section 3.4: the fit.
    for key, txt in (("fit_friction", "0.0575"), ("fit_persistence", "0.72"), ("derived_write_off", "0.0707")):
        assert f"{num[key]:g}" == txt, key
        expect("ch3 fit", ch["03_calibration"], txt)
    expect("ch3 fit", ch["03_calibration"], f"{num['fit_90plus'] * 100:.2f}\\%")
    expect("ch3 fit", ch["03_calibration"], f"{num['fit_90plus_final'] * 100:.2f}\\%")
    expect("ch3 book", ch["03_calibration"], f"{num['baseline_credit_active'] * 5000:,.0f}".replace(",", "{,}"))
    # Section 3.5: default and the households short from the start.
    expect("ch3 default", ch["03_calibration"], f"{num['baseline_default'] * 100:.2f}\\%")
    expect("ch3 default", ch["03_calibration"], f"{dc['no BNPL']['default_rate'] * 100:.2f}\\%")
    expect("ch3 short", ch["03_calibration"], f"{dc['no BNPL']['income_below_committed_who_default'] * 100:.0f}\\%")
    expect("ch3 short", ch["03_calibration"], f"{dc['BNPL beta=0']['income_below_committed_who_default'] * 100:.0f}\\%")
    expect("ch3 short", ch["03_calibration"], pmj(cont, "beta0_effect_pooled_contestable"))
    expect("ch3 short", ch["03_calibration"], pmj(cont, "peer_effect_pooled_contestable"))
    expect("ch3 short", ch["03_calibration"], unsigned(pmj(cont, "rq3s_bureau_diff_contestable_b0")))
    # Section 3.5: the default level against the bureau figures (check_default_level.py).
    lvl = json.loads((SUMMARY / "default_level.json").read_text())
    expect("ch3 level", ch["03_calibration"], f"{lvl['off_new_default_rate_final'] * 100:.2f}\\%")
    expect("ch3 level", ch["03_calibration"], f"{lvl['off_new_defaults_per_year_of_all_households'] * 100:.1f}\\%")
    expect("ch3 level", ch["03_calibration"], f"{lvl['off_inflow_per_tick_of_book'] * 100:.2f}\\%")
    expect("ch3 level", ch["03_calibration"], f"{lvl['ccmr_inflow_91plus_per_tick_of_accounts'] * 100:.2f}\\%")
    expect("ch3 level", ch["03_calibration"], f"about {lvl['ccmr_inflow_91plus_per_year_of_accounts'] * 100:.0f}\\%")
    expect("ch3 level", ch["03_calibration"], f"{lvl['off_defaulted_of_ever_active'] * 100:.1f}\\%")
    expect("ch4 level", ch["04_results"], f"{num['baseline_default'] * 100:.2f}\\%")
    # Section 4.1 and the RQ2 answer: the pooled effect.
    for c in ("04_results", "06_conclusion"):
        expect(f"{c} pooled", ch[c], unsigned(pmj(num, "beta0_effect_pooled")))
    expect("ch4 pooled", ch["04_results"], unsigned(pmj(num, "peer_effect_pooled")))
    expect("ch4 shortfall", ch["04_results"], pmj(num, "eff_no_shortfall_bnpl_b0"))
    # Section 4.2: the beta sweep.
    h = sweep["headline_linear"]
    expect("ch4 beta", ch["04_results"], f"{h['beta0_effect_pp']:+.2f} \\pm {h['beta0_effect_se']:.2f}")
    expect("ch4 beta", ch["04_results"], f"{h['beta0_effect_sd']:.2f}")
    slope = f"{h['slope_pp_per_0.1_beta']:+.3f} \\pm {h['slope_se_per_0.1_beta']:.3f}"
    for c in ("04_results", "06_conclusion"):
        expect(f"{c} slope", ch[c], slope)
    assert sweep["verdict"] == "linear"
    # Section 5: the switches at beta = 0.
    expect("ch5 bureau", ch["05_policy"], unsigned(pmj(num, "lever_bureau_beta0_diff")))
    expect("ch5 screening", ch["05_policy"], f"{-num['lever_afford_beta0_diff'] * 100:.2f} \\pm "
           f"{num['lever_afford_beta0_diff_se'] * 100:.2f}")
    print(f"OK: {checked - start} typed prose numbers match results/summary")


if __name__ == "__main__":
    main()
