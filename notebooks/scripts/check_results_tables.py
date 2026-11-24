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
#: Prose expectations that are not met, listed together at the end (QA 2026-11-10) so that a
#: revision that changes several numbers sees every sentence it has to change in one run.
missing: list[str] = []


def frag(name: str) -> str:
    return (GEN / f"{name}.tex").read_text(encoding="utf-8")


def expect(name: str, text: str, needle: str, prose: bool = False) -> None:
    """Assert that `needle` appears in `text`. A generated fragment must match at once; a prose
    expectation that fails is recorded and reported with the others at the end."""
    global checked
    # A difference beyond two standard errors is printed bold, so match it without its
    # math delimiters too (core).
    ok = needle in text or (needle.startswith("$") and core(needle) in text)
    if not ok and prose:
        missing.append(f"{name}: expected {needle!r}")
        return
    assert ok, f"{name}: expected {needle!r} in the fragment"
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
    expect("stacking", t, "1 & -- & -- & -- & -- &")
    expect("stacking_full", frag("tab_stacking_full"), "1 & -- & -- & -- & -- &")

    t = frag("tab_stacking_full")
    n3b2 = rq1[(rq1.n_platforms == 3) & (rq1.beta == 0.2)]
    expect("stacking_full", t, f"& {n3b2.stacking_2plus_final.mean() * 100:.1f} &")
    expect("stacking_full", t, f"& {n3b2.default_rate_final.mean() * 100:.2f} &")
    expect("stacking_full", t, f"& {rq1[(rq1.n_platforms == 6) & (rq1.beta == 0.1)].default_rate_final.mean() * 100:.2f} &")

    t = frag("tab_bnpl_on_checks")
    mp = b0.bnpl_purchase_mean_realised.mean()
    expect("bnpl_on_checks", t, "R" + f"{mp:,.0f}".replace(",", "{,}") + " &")
    pop = pd.read_parquet(ROOT / "data" / "processed" / "synthetic_population_5000.parquet")
    q4 = pop[pop.income_quintile == "Q4"]
    expect("bnpl_on_checks", t, f"(start: Q4 {q4.D_trad.sum() / q4.w5_hhincome.sum():.2f};")
    assert "Pattern~4" not in t and "Patterns 3 and 4" not in t, "Pattern 4 was dropped (#29)"
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
    k4n = rob[rob.label == "rob_k4"].set_index("seed").new_default_rate_final
    k7n = rob[rob.label == "rob_k7"].set_index("seed").new_default_rate_final
    dn = (k4n - k7n.reindex(k4n.index)) * 100
    expect("robustness", t, f"rises by ${dn.mean():.2f} \\pm {dn.std(ddof=1) / math.sqrt(len(dn)):.2f}$")

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
    # Food and rent left unpaid (QA 2026-11-10), changes at three decimals.
    t = frag("tab_scenarios_distress")
    expect("scenarios_distress", t, f"& {sben0.consumption_distress_mean.mean() * 100:.2f} &")
    expect("scenarios_distress", t, core(pmp(bur0, sben0, "consumption_distress_mean", 3)))
    expect("scenarios_distress", t, core(pmp(both0, sben0, "ever_consumption_distress_final", 3)))
    assert "not Rand amounts" in t

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

    check_effect_split(rq0)
    print(f"OK: {checked} numbers re-derived from results/raw match the generated fragments")
    check_prose()


def check_effect_split(rq0: pd.DataFrame) -> None:
    """D19 (2026-11-24): tab:effect-split and its keys in results_numbers.json.

    The all-households column is re-derived from results/raw (rq0, screen, redraw); the two group
    columns from the per-run rows of effect_split.json, which check_effect_split.py checked
    against results/raw run by run. Every cell, and each key the prose may quote, is compared.
    """
    global checked
    t = frag("tab_effect_split")
    num = json.loads((SUMMARY / "results_numbers.json").read_text())
    es = json.loads((SUMMARY / "effect_split.json").read_text())
    runs = pd.DataFrame(es["per_run"])
    screen = pd.read_parquet(RAW / "screen.parquet")
    redraw = pd.read_parquet(RAW / "redraw.parquet")
    off = rq0[rq0.label == "baseline_no_bnpl"]
    assert len(screen) == 20 and sorted(screen.seed) == sorted(off.seed), "the screen pairs with rq0"
    assert (redraw.groupby("label").seed.nunique() == 100).all()
    raw = {"bench": (rq0[rq0.label == "bnpl_on_beta0"], off), "screen": (screen, off),
           "redraw": (redraw[redraw.label == "redraw_b0.0"], redraw[redraw.label == "redraw_off"])}
    labels = {"bench": ("bnpl_on_beta0", "baseline_no_bnpl"), "screen": ("screen_b0.0", "baseline_no_bnpl"),
              "redraw": ("redraw_b0.0", "redraw_off")}
    names = {"bench": "Benchmark", "screen": "Wage-income screen", "redraw": "Redrawn population"}

    def numbers(a: pd.DataFrame, b: pd.DataFrame, col: str) -> tuple[float, float]:
        x = a.set_index("seed")[col]
        y = b.set_index("seed")[col]
        assert sorted(x.index) == sorted(y.index), "arms do not share seeds"
        z = x - y.reindex(x.index)
        return z.mean(), z.std(ddof=1) / math.sqrt(len(z))

    for key in ("bench", "screen", "redraw"):
        cells = [core(pmp(*raw[key], "new_default_rate_final"))]
        d, se = numbers(*raw[key], "new_default_rate_final")
        # results_numbers.json rounds to six decimals, so agreement is to within half of 1e-6.
        assert abs(num[f"split_{key}_all"] - d) < 1e-6 and abs(num[f"split_{key}_all_se"] - se) < 1e-6, key
        on, of = (runs[runs.label == lab] for lab in labels[key])
        for g in ("short", "other"):
            cells.append(core(pmp(on, of, f"new_default_{g}")))
            d, se = numbers(on, of, f"new_default_{g}")
            assert abs(num[f"split_{key}_{g}"] - d) < 1e-6, (key, g)
            assert abs(num[f"split_{key}_{g}_se"] - se) < 1e-6, (key, g)
        # The row as a whole, so a cell in the wrong column fails; bold cells match via core().
        row = " & ".join([names[key]] + cells)
        flat = t.replace("\\boldsymbol{", "").replace("}$", "$").replace("$", "")
        expect("effect_split", flat, row)
    # The group columns sum to the first: default during the run is over all households.
    assert np.allclose(runs.new_default_short + runs.new_default_other, runs.new_default_rate_final, atol=1e-12)
    # The rerun rows are the stored runs.
    for key, (a, b) in raw.items():
        for frame, lab in zip((a, b), labels[key]):
            r = runs[runs.label == lab].set_index("seed").new_default_rate_final
            assert (frame.set_index("seed").new_default_rate_final.reindex(r.index) == r).all(), lab
    # The screen less the benchmark, in the note, paired by seed.
    expect("effect_split", t, pmp(screen, rq0[rq0.label == "bnpl_on_beta0"], "new_default_rate_final") + " points")
    # The redrawn populations: separation rate re-derived per draw, short group sizes in the note.
    ro = redraw[redraw.label == "redraw_off"]
    assert ro.shock_prob.nunique() > 1 and (ro.population_seed == ro.seed).all()
    assert abs(num["split_redraw_separation_rate_mean"] - ro.shock_prob.mean()) < 1e-6
    expect("effect_split", t, f"{int(runs[runs.label == 'redraw_off'].n_short.min())} to "
           f"{int(runs[runs.label == 'redraw_off'].n_short.max())} in the draws")
    expect("effect_split", t, f"{num['split_short_n']} households in the benchmark population")
    assert num["split_short_n"] == 182 and num["split_short_at_risk"] == 120
    assert num["split_eligible_screen"] == screen.n_bnpl_eligible.mean()
    checked += 3


def check_prose() -> None:
    """Typed numbers in the results prose (#95, #100): each must match its JSON source, as printed.

    Covers the headline numbers that are typed rather than \\input from a fragment. A number is
    formatted from the JSON exactly as the text prints it and must appear in the named chapter.
    """
    global checked
    start = checked

    def expect_p(name: str, text: str, needle: str) -> None:
        expect(name, text, needle, prose=True)

    num = json.loads((SUMMARY / "results_numbers.json").read_text())
    sweep = json.loads((SUMMARY / "beta_sweep.json").read_text())
    cont = json.loads((SUMMARY / "contestable_default.json").read_text())
    dc = json.loads((SUMMARY / "defaulter_credit.json").read_text())
    # Whitespace is collapsed (QA 2026-11-10) so that a needle matches across a line break.
    ch = {n: " ".join((ROOT / "thesis" / "chapters" / f"{n}.tex").read_text(encoding="utf-8").split())
          for n in ("01_introduction", "03_calibration","04_results", "05_policy", "06_conclusion", "appendix_c_supplementary")}

    def pmj(d: dict, key: str, dp: int = 2) -> str:
        return f"{d[key] * 100:+.{dp}f} \\pm {d[key + '_se'] * 100:.{dp}f}"

    def unsigned(s: str) -> str:
        return s.lstrip("+")

    # Section 3.4: the fit.
    for key, txt in (("fit_friction", "0.0575"), ("fit_persistence", "0.72"), ("derived_write_off", "0.0707")):
        assert f"{num[key]:g}" == txt, key
        expect_p("ch3 fit", ch["03_calibration"], txt)
    expect_p("ch3 fit", ch["03_calibration"], f"{num['fit_90plus'] * 100:.2f}\\%")
    expect_p("ch3 fit", ch["03_calibration"], f"{num['fit_90plus_final'] * 100:.2f}\\%")
    expect_p("ch3 book", ch["03_calibration"], f"{num['baseline_credit_active'] * 5000:,.0f}".replace(",", "{,}"))
    # Section 3.5: default and the households short from the start.
    expect_p("ch3 default", ch["03_calibration"], f"{num['baseline_default'] * 100:.2f}\\%")
    expect_p("ch3 default", ch["03_calibration"], f"{dc['no BNPL']['default_rate'] * 100:.2f}\\%")
    # Section 3.1 (QA 2026-11-10): the two default measures and their denominators.
    expect_p("ch3 measures", ch["03_calibration"], f"{num['baseline_new_default'] * 100:.2f}\\% without \\ac{{BNPL}}, or "
             f"{num['baseline_new_default_of_not_initially_defaulted'] * 100:.2f}\\% of those not in default")
    expect_p("ch3 measures", ch["03_calibration"], f"adds the {num['baseline_initial_default'] * 100:.2f}\\% placed")
    # Section 3.5 (QA 2026-11-10, B47): the group short from the start (short_group.json).
    sg = json.loads((SUMMARY / "short_group.json").read_text())
    assert sg["n_agents"] == 182 and sg["zero_or_missing_income"] == 0
    c3 = ch["03_calibration"]
    expect_p("ch3 short", c3, f"Its {sg['n_agents']} households are drawn from {sg['n_source_households']} \\ac{{NIDS}} records")
    assert round(sg["share_q1"] * 3) == 2 and round(sg["share_paying_rent"] * 3) == 2, "two-thirds"
    expect_p("ch3 short", c3, f"{sg['share_no_employed_member'] * 100:.0f}\\% have no employed member")
    expect_p("ch3 short", c3, f"{sg['share_no_liquid_savings'] * 100:.0f}\\% have no liquid savings")
    expect_p("ch3 short", c3, f"for {sg['one_shot_covers_share_of_answered'] * 100:.0f}\\% of the group's respondents")
    expect_p("ch3 short", c3, f"The {sg['n_in_default_at_start_every_seed']} of the {sg['n_agents']} that hold traditional debt")
    expect_p("ch3 short", c3, f"only the other {sg['n_at_risk']} can default during the run")
    # Style pass 2026-11-16: the effect among the other households moved from Section 3.5 to 4.1,
    # and the 3.5 preview of the group's default shares was cut (Section 4.1 decomposes the effect).
    # Anchored on the 4.1 wording: bare figures also match the RQ2 answer's copy (ultrareview).
    expect_p("ch4 others", ch["04_results"], f"(three at $\\beta=0.3$), the effect is ${pmj(cont, 'beta0_effect_pooled_contestable')}$ "
             f"points at $\\beta=0$, not detectable, and ${pmj(cont, 'peer_effect_pooled_contestable')}$ at $\\beta=0.3$, which is.")
    # QA 2026-11-10 (E2): beta = 0 not detectable, beta = 0.3 detectable; both in the RQ2 answer.
    assert abs(cont["beta0_effect_pooled_contestable"]) < 2 * cont["beta0_effect_pooled_contestable_se"]
    assert abs(cont["peer_effect_pooled_contestable"]) > 2 * cont["peer_effect_pooled_contestable_se"]
    expect_p("ch4 RQ2 others", ch["04_results"], f"it is ${pmj(cont, 'beta0_effect_pooled_contestable')}$ points at $\\beta=0$, not detectable, "
             f"and ${pmj(cont, 'peer_effect_pooled_contestable')}$ at $\\beta=0.3$, which is")
    # Fix pass 2026-11-11: the bureau-visibility figure for the other households moved from
    # Section 3.5 to Section 5 (examiner audit, L6).
    expect_p("ch5 others", ch["05_policy"], unsigned(pmj(cont, "rq3s_bureau_diff_contestable_b0")))
    # Fix pass 2026-11-11: the split of the effect by the facility in default (Section 4.1).
    trig = json.loads((SUMMARY / "default_trigger.json").read_text(encoding="utf-8"))
    expect_p("ch4 trigger", ch["04_results"], f"${trig['bnpl_only_pp']:.2f} \\pm {trig['bnpl_only_pp_se']:.2f}$ of the "
             f"{trig['effect_pp']:.2f}")
    expect_p("ch4 trigger", ch["04_results"], f"{trig['remainder_pp']:.2f} \\pm {trig['remainder_pp_se']:.2f}")
    assert abs(trig["remainder_pp"]) < 2 * trig["remainder_pp_se"], "text says the remainder is not detectable"
    # Section 3.5: the default level against the bureau figures (check_default_level.py).
    lvl = json.loads((SUMMARY / "default_level.json").read_text())
    expect_p("ch3 level", ch["03_calibration"], f"{lvl['off_new_default_rate_final'] * 100:.2f}\\%")
    expect_p("ch3 level", ch["03_calibration"], f"{lvl['off_new_defaults_per_year_of_all_households'] * 100:.1f}\\%")
    expect_p("ch3 level", ch["03_calibration"], f"{lvl['off_inflow_per_tick_of_book'] * 100:.2f}\\%")
    expect_p("ch3 level", ch["03_calibration"], f"{lvl['ccmr_inflow_91plus_per_tick_of_accounts'] * 100:.2f}\\%")
    expect_p("ch3 level", ch["03_calibration"], f"{lvl['off_defaulted_of_ever_active'] * 100:.1f}\\%")
    # QA 2026-11-10 (E8): the share of the stock placed in default at the start, in points of the
    # households that ever held credit; (E4): the final-tick 90+ share on the same seeds.
    expect_p("ch3 level", ch["03_calibration"],
             f"{lvl['off_initial_default_rate'] / lvl['off_ever_active_share'] * 100:.1f} points of it from the starting stock")
    expect_p("ch3 level", ch["03_calibration"],
             f"arrears at the final tick, when {lvl['off_active_90_plus_final'] * 100:.2f}\\% of credit-active households")
    # QA 2026-11-10 (E3): households holding traditional debt at the start, from the population.
    pop = pd.read_parquet(ROOT / "data" / "processed" / "synthetic_population_5000.parquet", columns=["D_trad"])
    n_start = int((pop.D_trad > 0).sum())
    assert n_start == round(lvl["off_start_active_share"] * len(pop)), "start book against default_level.json"
    start_txt = f"{n_start:,}".replace(",", "{,}")
    # Style pass 2026-11-16: Appendix C's limitations index points to Section 3.4 for the book.
    expect_p("ch3 book", ch["03_calibration"], f"fall from {start_txt} at the start")
    expect_p("ch4 level", ch["04_results"], f"{num['baseline_default'] * 100:.2f}\\%")
    sobj = json.loads((SUMMARY / "sobol_indices.json").read_text(encoding="utf-8"))
    shd = next(r for r in sobj["indices"]["default_rate_final"] if r["parameter"] == "shock_prob")
    others = [r["ST"] for r in sobj["indices"]["default_rate_final"] if r["parameter"] != "shock_prob"]
    fifths = sobj["new_default_by_shock_prob_fifth"]
    noise = sobj["replicate_noise_share"]["default_rate_final"]
    # Style pass 2026-11-16: Section 4.6 points to Appendix C for the replicate-noise argument.
    expect_p("appC sobol", ch["appendix_c_supplementary"], f"{noise * 100:.0f}\\% of the")
    expect_p("appC sobol", ch["appendix_c_supplementary"], f"{min(others):.2f} to {max(others):.2f}")
    # A1 (2026-11-10): S1_conf is a 95% bootstrap half-width, not one standard error.
    expect_p("ch4 sobol", ch["04_results"],
             f"{shd['S1']:.2f}, with a 95\\% bootstrap interval of $\\pm {shd['S1_conf']:.2f}$")
    snc = json.loads((SUMMARY / "sobol_noise_check.json").read_text(encoding="utf-8"))
    ub = max(r["ST_noise_corrected_ci"][1] for r in snc["rows"] if r["parameter"] != "shock_prob")
    expect_p("ch4 sobol noise", ch["04_results"], f"within {math.ceil(ub * 100) / 100:.2f} of zero")
    expect_p("ch4 sobol", ch["04_results"], f"is {fifths[0] * 100:.1f}\\% in the lowest fifth")
    expect_p("ch4 sobol", ch["04_results"], f"and {fifths[-1] * 100:.1f}\\% in the highest")
    expect_p("ch3 sobol", ch["03_calibration"], f"Saltelli design & 0--0.3 & {sobj['replicates']} &")
    # Section 4.1 and the RQ2 answer: the pooled effect.
    for c in ("04_results", "06_conclusion"):
        expect_p(f"{c} pooled", ch[c], unsigned(pmj(num, "beta0_effect_pooled")))
    expect_p("ch4 pooled", ch["04_results"], unsigned(pmj(num, "peer_effect_pooled")))
    expect_p("ch4 shortfall", ch["04_results"], pmj(num, "eff_no_shortfall_bnpl_b0"))
    # Section 4.2: the beta sweep.
    h = sweep["headline_linear"]
    expect_p("ch4 beta", ch["04_results"], f"{h['beta0_effect_pp']:+.2f} \\pm {h['beta0_effect_se']:.2f}")
    # Fix pass 2026-11-11: the replicate SD is in Table tab:beta only.
    slope = f"{h['slope_pp_per_0.1_beta']:+.3f} \\pm {h['slope_se_per_0.1_beta']:.3f}"
    # 2026-11-24: the conclusion states the slope's result without the number (Section 4.2 has it).
    expect_p("04_results slope", ch["04_results"], slope)
    assert sweep["verdict"] == "linear"
    # QA 2026-11-10 (E6): Section 4.1's side measures from the sweep's beta = 0 arm (post-burn-in
    # mean of the 90+ share of all households; ever short of food and rent), seeds 90,000-90,249.
    s0 = next(r for r in sweep["table"] if r["beta"] == 0.0)
    s3 = next(r for r in sweep["table"] if abs(r["beta"] - BP) < 1e-9)
    assert sweep["table"][0]["n"] == 250
    expect_p("ch4 side", ch["04_results"], f"rises by ${s0['effect_90plus_all_pp']:.2f} \\pm {s0['effect_90plus_all_se']:.2f}$ points at $\\beta=0$")
    expect_p("ch4 side", ch["04_results"], f"short of food and rent by ${s0['effect_consumption_ever_pp']:.2f} \\pm {s0['effect_consumption_ever_se']:.2f}$")
    # QA 2026-11-10 (E10a): stacking among ever-holders across the sweep.
    expect_p("ch4 stack", ch["04_results"], f"who stack from {s0['stacking_ever_holders'] * 100:.0f}\\% to {s3['stacking_ever_holders'] * 100:.0f}\\%")
    # A1 (2026-11-10): the detectable difference between two values of beta, with the no-BNPL
    # arm cancelling seed by seed (between_beta_difference_detected_half_the_time_pp).
    expect_p("ch4 beta power", ch["04_results"],
             f"difference of {sweep['between_beta_difference_detected_half_the_time_pp']:.2f} points between two values")
    # Section 4.4 (QA 2026-11-10): steps along the access sweep, replacing "no step is followed by
    # a level".
    assert num["access_step_dev_beyond_2se_all"] == 1, "text says only one of the 24 steps"
    c4 = ch["04_results"]
    # Fix pass 2026-11-11: the range of steps was cut from the prose; the 24-step count stays.
    expect_p("ch4 access", c4, unsigned(pmj(num, "access_rise_30_70_beta0.3")))
    expect_p("ch4 access", c4, unsigned(pmj(num, "access_rise_70_100_beta0.3")))
    # Section 4.6 (QA 2026-11-10): the 56-day threshold split into stock and default in the run.
    expect_p("ch4 k4", c4, f"{num['rob_k4_initial_minus_k7'] * 100:.2f} points come from households placed")
    expect_p("ch4 k4", c4, unsigned(pmj(num, "rob_k4_new_minus_k7")))
    # Section 5 (QA 2026-11-10): food and rent left unpaid (tab:scenarios-distress).
    def pm3(key: str) -> str:
        return f"{num[key] * 100:.3f} \\pm {num[key + '_se'] * 100:.3f}"
    c5 = ch["05_policy"]
    for key in ("scen_bureau_beta0_cdist_tick_diff", "scen_bureau_beta0_cdist_ever_diff",
                "scen_afford_beta0_cdist_tick_diff", "scen_afford_beta0_cdist_ever_diff"):
        expect_p("ch5 distress", c5, pm3(key))
    for key in ("scen_afford_beta0.3_cdist_tick_diff", "scen_afford_beta0.3_cdist_ever_diff"):
        assert abs(num[key]) < 2 * num[key + "_se"], f"{key}: text says not detectable"
    # QA 2026-11-10 (E1): the RQ3 answer, with standard errors; at beta = 0.3 only visibility.
    # Fix pass 2026-11-11: the RQ3 answer states the direction; the figures are in the body above.
    expect_p("ch5 distress", c5, "and at $\\beta=0.3$ only visibility does")
    for key in ("scen_bureau_beta0_cdist_tick_diff", "scen_afford_beta0_cdist_tick_diff",
                "scen_bureau_beta0.3_cdist_tick_diff", "scen_bureau_beta0.3_cdist_ever_diff"):
        assert abs(num[key]) > 2 * num[key + "_se"], f"{key}: text says detectable"
    # Section 5: the switches at beta = 0.
    expect_p("ch5 bureau", ch["05_policy"], unsigned(pmj(num, "lever_bureau_beta0_diff")))
    expect_p("ch5 screening", ch["05_policy"], f"{-num['lever_afford_beta0_diff'] * 100:.2f} \\pm "
           f"{num['lever_afford_beta0_diff_se'] * 100:.2f}")
    # Style pass 2026-11-16: the introduction now gives the body's figures exactly (ultrareview).
    c1 = ch["01_introduction"]
    expect_p("ch1 effect", c1, f"${unsigned(pmj(num, 'beta0_effect_pooled'))}$ points without peer influence, "
             f"from {num['baseline_new_default'] * 100:.2f}\\%")
    expect_p("ch1 shortfall", c1, f"${pmj(num, 'eff_no_shortfall_bnpl_b0')}$ points")
    for c in ("01_introduction", "06_conclusion"):
        expect_p(f"{c} bureau", ch[c], f"${unsigned(pmj(num, 'lever_bureau_beta0_diff'))}$ points without peer influence")
    expect_p("ch1 screening", c1, f"lowers default by {-num['lever_afford_beta0_diff'] * 100:.2f} to "
             f"{-num['lever_afford_beta0.3_diff'] * 100:.2f} points")
    expect_p("ch1 volume", c1, f"from R{s0['volume_per_eligible_year']:,.0f} to R{s3['volume_per_eligible_year']:,.0f} a year"
             .replace(",", "{,}"))
    expect_p("ch1 stack", c1, f"Under the assumed routing, {s0['stacking_ever_holders'] * 100:.0f}\\% of")
    # ------------------------------------------------------------------------------------------
    # D19 (2026-11-24): PROSE CHECKS FOR tab:effect-split GO HERE (to be added by the lead once
    # the sentences on the wage-income screen and the redrawn population are written). Format
    # each needle from results_numbers.json (keys split_*) or effect_split.json, e.g.
    #   expect_p("ch4 screen", ch["04_results"], unsigned(pmj(num, "split_screen_all")))
    # ------------------------------------------------------------------------------------------
    c3 = ch["03_calibration"]
    es = json.loads((SUMMARY / "effect_split.json").read_text())
    drop = unsigned(pmj({k: -v if not k.endswith("_se") else v for k, v in num.items()
                         if k.startswith("split_screen_less_bench_all")}, "split_screen_less_bench_all"))
    # Section 4.1: the wage-income screen.
    expect_p("ch4 screen", c4, f"The arm lowers the effect by ${drop}$ points, to")
    expect_p("ch4 screen", c4, f"${pmj(num, 'split_screen_all')}$ (Table~\\ref{{tab:effect-split}}), so about half")
    assert es["never_lent_every_seed"] == 55 and round(es["never_lent_default_bench"]) == 46
    expect_p("ch4 screen", c4, f"Of the {es['never_lent_every_seed']} the lender never lends to, "
             f"{es['never_lent_default_screen']:.0f}")
    expect_p("ch4 screen", c4, f"still default, all among the {es['never_lent_every_seed_wage']} with wage income")
    # "all among": a household without wage income is refused by the screen, holds no debt and
    # cannot default, so every default among the 55 under the screen is one of the 19.
    assert es["never_lent_default_screen"] <= es["never_lent_every_seed_wage"]
    # "About half": the fall and what remains, as shares of the benchmark effect on the same seeds.
    assert abs(-num["split_screen_less_bench_all"] / num["split_bench_all"] - 0.5) < 0.05
    assert abs(num["split_screen_all"] / num["split_bench_all"] - 0.5) < 0.05
    # Section 4.1: the redrawn population.
    expect_p("ch4 redraw", c4, f"In the redrawn population the effect is ${pmj(num, 'split_redraw_all')}$ points, "
             f"of which ${pmj(num, 'split_redraw_short')}$ are")
    # "does not differ detectably from the pooled" estimate, and the baseline level over the draws.
    gap_all = num["split_redraw_all"] - num["beta0_effect_pooled"]
    assert abs(gap_all) < 2 * math.hypot(num["split_redraw_all_se"], num["beta0_effect_pooled_se"])
    expect_p("ch4 redraw", c4, f"from the pooled ${unsigned(pmj(num, 'beta0_effect_pooled'))}$, and without")
    level = f"{num['split_redraw_baseline_new_default_mean'] * 100:.2f}"
    assert level == f"{num['baseline_default_during'] * 100:.2f}" if "baseline_default_during" in num else True
    expect_p("ch4 redraw", c4, f"default during the run averages {level}\\%")
    expect_p("ch4 redraw", c4, f"The redrawn population's ${pmj(num, 'split_redraw_other')}$ at $\\beta=0$ is detectable")
    assert num["split_redraw_other"] > 2 * num["split_redraw_other_se"]
    gap = num["split_redraw_other"] - cont["beta0_effect_pooled_contestable"]
    gap_se = math.hypot(num["split_redraw_other_se"], cont["beta0_effect_pooled_contestable_se"])
    assert abs(gap) < 2 * gap_se, "redrawn and pooled estimates for the other households differ detectably"
    # Answer to RQ2.
    expect_p("ch4 answer", c4, f"${pmj(num, 'split_redraw_all')}$ points, and the wage-income screen lowers the "
             f"benchmark's {num['split_bench_all'] * 100:.2f} points by")
    expect_p("ch4 answer", c4, f"${drop}$ (Section~\\ref{{sec:results-injection}})")
    # tab:experiments (Section 3.1): the two rows, their replicates and first seeds.
    screen_seeds = [r["seed"] for r in es["per_run"] if r["label"] == "screen_b0.0"]
    assert es["screen_n"] == len(screen_seeds) == 20 and min(screen_seeds) == 10000
    expect_p("ch3 experiments", c3, "Wage-income screen & platforms lend only to households with wage income & 0 & "
             f"{es['screen_n']} & 10{{,}}000 & \\ref{{tab:effect-split}}")
    first_seed = f"{num['split_redraw_seed_min']:,}".replace(",", "{,}")
    expect_p("ch3 experiments", c3, "Redrawn population & \\ac{BNPL} off and on, one population draw per replicate & 0 & "
             + f"{num['split_redraw_reps']} & {first_seed} & \\ref{{tab:effect-split}}")
    if missing:
        print(f"{checked - start} typed prose numbers match; {len(missing)} do not. Each needle is "
              "formatted from results/ and must appear in the named chapter:")
        for m in missing:
            print("  MISSING", m)
        raise SystemExit(1)
    print(f"OK: {checked - start} typed prose numbers match results/summary")


if __name__ == "__main__":
    main()
