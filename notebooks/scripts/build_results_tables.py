"""Generate every results table in Sections 3.5, 4, 5 and Appendix C from results/raw.

    ./env/python.exe notebooks/scripts/build_results_tables.py

Writes thesis/chapters/generated/tab_*.tex (each with a "do not edit" header and a
self-contained \\tabnote) and results/summary/results_numbers.json, the numbers the prose
and the abstract are checked against. No number in the thesis is typed: it is read from a
fragment written here or from a figure written by build_results_figures.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from results_common import (  # noqa: E402
    GEN, Q, ROOT, SUMMARY, SCENARIOS, arm, cell, diff, group_row, load, ms, num, paired_diff,
    pct, pm, rand, rm, table, years,
)
from simulation.config import load_ccmr_target  # noqa: E402

N = {}  # the numbers the prose quotes; dumped to results_numbers.json at the end

REPL = "Means over 20 replicates with unique seeds, replicate standard deviation in brackets"
SE = (
    "differences carry one unpaired standard error, "
    r"$\sqrt{s_a^2/n_a + s_b^2/n_b}$ over the two arms' replicates"
)
SHOCK = (
    "every run uses the calibrated shock probability 0.016 and payment friction 0.09, "
    "four platforms, and access at the banked ceiling unless stated"
)
SHOCK_CAP = SHOCK[0].upper() + SHOCK[1:]  # sentence-initial form


def holders_share(d: pd.DataFrame, col: str = "stacking_2plus_final") -> pd.Series:
    """A share of all households re-expressed as a share of end-of-horizon BNPL holders."""
    return d[col] / d.bnpl_adoption_final.clip(lower=1e-9)


# ============================================================ 4 opening: the three arms
def tab_baseline_arms(rq0: pd.DataFrame) -> None:
    off, b0, b1 = (arm(rq0, l) for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))
    rows_spec = [
        ("Population default rate (\\%)", "default_rate_final", 100, 2),
        ("90+ day arrears, credit-active households (\\%)", "active_90_plus_mean", 100, 2),
        ("Traditional arrears rate, all households (\\%)", "trad_arrears_rate_mean", 100, 2),
        ("Traditional interest charged (R m)", "trad_interest_total", 1e-6, 2),
        ("New traditional lending granted (R m)", "trad_granted_value", 1e-6, 2),
        ("Applications refused at the gate (count)", "trad_refused_gate", 1, 0),
        ("Zero liquid savings (\\% of households)", "zero_savings_rate_mean", 100, 1),
        ("\\ac{BNPL} adoption, end of horizon (\\%)", "bnpl_adoption_final", 100, 2),
        ("Ever held a \\ac{BNPL} balance (\\%)", "ever_adopted", 100, 2),
        ("Two or more facilities, end of horizon (\\% of households)", "stacking_2plus_final", 100, 2),
        ("Ever held two or more facilities (\\% of households)", "ever_stacked_2plus", 100, 2),
        ("Ever held two or more facilities (\\% of ever-adopters)", "ever_stacked_2plus_of_adopters", 100, 1),
        ("Cumulative \\ac{BNPL} volume (R m)", "bnpl_volume_cumulative", 1e-6, 2),
    ]
    rows = []
    for name, col, scale, d in rows_spec:
        rows.append(" & ".join([name] + [cell(x[col], d, scale) for x in (off, b0, b1)]) + r" \\")
    # holders share, computed per replicate
    rows.insert(
        10,
        "Two or more facilities, end of horizon (\\% of holders) & -- & "
        + cell(holders_share(b0), 1) + " & " + cell(holders_share(b1), 1) + r" \\",
    )
    d0, se0 = diff(b0.default_rate_final, off.default_rate_final)
    d1, se1 = diff(b1.default_rate_final, off.default_rate_final)
    N.update(
        baseline_default=ms(off.default_rate_final)[0],
        baseline_default_sd=ms(off.default_rate_final)[1],
        baseline_90plus_active=ms(off.active_90_plus_mean)[0],
        ccmr_90plus=load_ccmr_target()["pct_90_plus"] / 100,
        baseline_credit_active=ms(off.n_credit_active_final)[0] / off.n_agents.iloc[0],
        banked_ceiling=off.n_banked.iloc[0] / off.n_agents.iloc[0],
        injection_beta0=d0, injection_beta0_se=se0,
        injection_beta1=d1, injection_beta1_se=se1,
        adoption_beta0=ms(b0.bnpl_adoption_final)[0],
        adoption_beta1=ms(b1.bnpl_adoption_final)[0],
        ever_adopted_beta0=ms(b0.ever_adopted)[0],
        ever_adopted_beta1=ms(b1.ever_adopted)[0],
        stack2_all_beta0=ms(b0.stacking_2plus_final)[0],
        stack2_all_beta1=ms(b1.stacking_2plus_final)[0],
        stack2_holders_beta0=ms(holders_share(b0))[0],
        stack2_holders_beta1=ms(holders_share(b1))[0],
        ever_stack2_adopters_beta0=ms(b0.ever_stacked_2plus_of_adopters)[0],
        ever_stack2_adopters_beta1=ms(b1.ever_stacked_2plus_of_adopters)[0],
        refused_off=ms(off.trad_refused_gate)[0],
        refused_beta0=ms(b0.trad_refused_gate)[0],
        lending_off=ms(off.trad_granted_value)[0],
        lending_beta0=ms(b0.trad_granted_value)[0],
    )
    table(
        "tab_baseline_arms",
        "The 2017 baseline and the \\ac{BNPL} injection",
        f"The calibrated baseline with \\ac{{BNPL}} disabled, and the same population with "
        f"\\ac{{BNPL}} enabled at four platforms and access at the banked ceiling, without "
        f"($\\beta = 0$) and with ($\\beta = 1$) peer influence. {REPL} (seeds 10{{,}}000--10{{,}}019 "
        f"in each arm). The default rate is the share of all households in default at the final tick; "
        f"the 90+ day share is over credit-active households, averaged over post-burn-in ticks; "
        f"the traditional arrears rate is the share of all households with a traditional instalment "
        f"in arrears, averaged over post-burn-in ticks; interest, lending and volume are sums over "
        f"the post-burn-in horizon in 2017 Rands. ``Holders'' are households with a positive "
        f"\\ac{{BNPL}} balance at the final tick; ``ever'' quantities are over every tick of the run. "
        f"The injection raises default by {pm(d0, se0)}pp at $\\beta = 0$ and {pm(d1, se1)}pp at "
        f"$\\beta = 1$; {SE}.",
        "L{6.4cm}rrr",
        r"\textbf{Outcome} & \textbf{No \ac{BNPL}} & \textbf{\ac{BNPL}, $\beta=0$} & \textbf{\ac{BNPL}, $\beta=1$}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ 4.1 stacking
def tab_stacking(rq1: pd.DataFrame) -> None:
    rows = []
    n1, n6 = {}, {}
    sd_max = 0.0
    for n in range(1, 7):
        cells = [str(n)]
        for b in (0.0, 1.0):
            d = rq1[(rq1.n_platforms == n) & (rq1.beta == b)]
            shares = [d.stacking_2plus_final, holders_share(d), d.ever_stacked_2plus_of_adopters]
            sd_max = max(sd_max, *(ms(s)[1] for s in shares))
            cells += [pct(ms(s)[0], 1) for s in shares] + [
                cell(d.bnpl_volume_cumulative, 2, 1e-6),
                cell(d.default_rate_final, 2),
            ]
            N[f"volume_n{n}_beta{b:g}"] = ms(d.bnpl_volume_cumulative)[0]
            if n == 1:
                n1[b] = d
            if n == 6:
                n6[b] = d
            if n == 4:
                N[f"stack2_all_n4_beta{b:g}"] = ms(d.stacking_2plus_final)[0]
            if n in (2, 6):
                N[f"stack2_all_n{n}_beta{b:g}"] = ms(d.stacking_2plus_final)[0]
        rows.append(" & ".join(cells) + r" \\")
    d0, se0 = diff(n6[0.0].default_rate_final, n1[0.0].default_rate_final)
    d1, se1 = diff(n6[1.0].default_rate_final, n1[1.0].default_rate_final)
    N.update(n6_minus_n1_beta0=d0, n6_minus_n1_beta0_se=se0,
             n6_minus_n1_beta1=d1, n6_minus_n1_beta1_se=se1,
             default_n1_beta0=ms(n1[0.0].default_rate_final)[0])
    table(
        "tab_stacking",
        "Concurrent facilities and default by platform count",
        f"The platform-count sweep of the stacking experiment, at $\\beta = 0$ (no peer influence, "
        f"the control) and $\\beta = 1$; the baseline is four platforms. ``2+'' is the share holding "
        f"a balance on two or more platforms at the final tick, as a share of all households and of "
        f"households holding any \\ac{{BNPL}} balance at that tick; ``ever 2+'' is the share of "
        f"households that ever held a \\ac{{BNPL}} balance and at some tick held two or more, the "
        f"analogue of the \\ac{{CFPB}}'s over-a-year measure. With one platform the share is zero "
        f"by construction. ``Volume'' is cumulative post-burn-in \\ac{{BNPL}} volume in R million. "
        f"{REPL} for volume and default (seeds 20{{,}}000--20{{,}}019 in every cell); the three "
        f"share columns are replicate means in per cent, with replicate standard deviations of at "
        f"most {sd_max * 100:.1f} points. {SHOCK_CAP}. Default at "
        f"six platforms less default at one: {pm(d0, se0)}pp at $\\beta = 0$ and {pm(d1, se1)}pp at "
        f"$\\beta = 1$; {SE}. The other three values of $\\beta$ are in Table~\\ref{{tab:stacking-full}}.",
        "c rrrrr rrrrr",
        r"& \multicolumn{5}{c}{$\beta = 0$} & \multicolumn{5}{c}{$\beta = 1$} \\ \cmidrule(lr){2-6}\cmidrule(lr){7-11}"
        "\n\\textbf{Platforms} & \\textbf{2+} & \\textbf{holders} & \\textbf{ever} & \\textbf{Volume} & \\textbf{Default (\\%)} "
        "& \\textbf{2+} & \\textbf{holders} & \\textbf{ever} & \\textbf{Volume} & \\textbf{Default (\\%)}",
        rows,
        size=r"\scriptsize",
        colsep="3pt",
    )
    # appendix: every beta, two outcomes
    betas = sorted(rq1.beta.unique())
    rows = []
    sd_max, sd_def = 0.0, 0.0
    for n in range(1, 7):
        cells = [str(n)]
        for b in betas:
            d = rq1[(rq1.n_platforms == n) & (rq1.beta == b)]
            m, s, _ = ms(d.stacking_2plus_final)
            sd_max = max(sd_max, s)
            cells.append(pct(m, 1))
        for b in betas:
            d = rq1[(rq1.n_platforms == n) & (rq1.beta == b)]
            m, s, _ = ms(d.default_rate_final)
            sd_def = max(sd_def, s)
            cells.append(pct(m, 2))
        rows.append(" & ".join(cells) + r" \\")
    k = len(betas)
    table(
        "tab_stacking_full",
        "Platform count by peer-influence strength: the full grid",
        f"Every cell of the stacking experiment: the share of all households holding two or more "
        f"facilities at the final tick and the population default rate, both replicate means over "
        f"20 replicates in per cent (standard deviations at most {sd_max * 100:.1f} points for the "
        f"shares and {sd_def * 100:.2f} for default), for $N$ = one to six platforms and every value "
        f"of $\\beta$ swept. {SHOCK_CAP}. Table~\\ref{{tab:stacking}} in the body reports the "
        f"$\\beta = 0$ and $\\beta = 1$ columns with dispersion, the holder and over-the-horizon "
        f"denominators, and cumulative volume.",
        "c " + "r" * k + " " + "r" * k,
        f"& \\multicolumn{{{k}}}{{c}}{{2+ facilities (\\% of households)}} & \\multicolumn{{{k}}}{{c}}{{Default rate (\\%)}} \\\\ "
        f"\\cmidrule(lr){{2-{k + 1}}}\\cmidrule(lr){{{k + 2}-{2 * k + 1}}}\n\\textbf{{$N$}} & "
        + " & ".join(f"$\\beta={b:g}$" for b in betas) + " & "
        + " & ".join(f"$\\beta={b:g}$" for b in betas),
        rows,
        size=r"\footnotesize",
        colsep="3pt",
    )


# ============================================================ 3.5 the unfitted BNPL-on checks
def tab_bnpl_on_checks(rq0: pd.DataFrame) -> None:
    off, b0, b1 = (arm(rq0, l) for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))
    anchors = json.loads((ROOT / "data/config/bnpl_anchors_2017.json").read_text(encoding="utf-8"))["model_target"]
    target = anchors["mean_purchase_2017_rands"]
    lo_band, hi_band = target * 0.65, target * 1.35
    yrs = years(rq0)

    # stacking among holders vs CFPB
    sh0 = ms(holders_share(b0))[0]
    ev0 = ms(b0.ever_stacked_2plus_of_adopters)[0]
    # annual volume per eligible household (lower anchor) and per ever-adopting household (upper)
    v_elig = b0.bnpl_volume_cumulative / b0.n_bnpl_eligible / yrs
    v_adopt = b0.bnpl_volume_cumulative / (b0.ever_adopted * b0.n_agents) / yrs
    lo_vol, hi_vol = anchors["annual_volume_per_signed_up_user_2017_rands"], anchors["annual_volume_per_active_user_2017_rands"]
    # mean purchase
    mp0, mp0_sd, _ = ms(b0.bnpl_purchase_mean_realised)
    mp1 = ms(b1.bnpl_purchase_mean_realised)[0]
    inside0 = int(((b0.bnpl_purchase_mean_realised >= lo_band) & (b0.bnpl_purchase_mean_realised <= hi_band)).sum())
    inside1 = int(((b1.bnpl_purchase_mean_realised >= lo_band) & (b1.bnpl_purchase_mean_realised <= hi_band)).sum())
    gap0 = mp0 / target - 1
    margin = mp0 - lo_band
    # the bracket that explains the gap: Q3-Q5 and Q4-Q5 means, from the by-quintile split
    def restricted(d, qs):
        n = sum(d[f"bnpl_want_purchases_{q}"] for q in qs)
        v = sum(d[f"bnpl_want_purchases_{q}"] * d[f"bnpl_purchase_mean_realised_{q}"] for q in qs)
        return float((v / n).mean())
    br35, br45 = restricted(b0, ["Q3", "Q4", "Q5"]), restricted(b0, ["Q4", "Q5"])
    # pattern 1
    d_arr0, se_arr0 = diff(b0.trad_arrears_rate_mean, off.trad_arrears_rate_mean)
    d_arr1, se_arr1 = diff(b1.trad_arrears_rate_mean, off.trad_arrears_rate_mean)
    r_int0 = ms(b0.trad_interest_total)[0] / ms(off.trad_interest_total)[0] - 1
    r_int1 = ms(b1.trad_interest_total)[0] / ms(off.trad_interest_total)[0] - 1
    # pattern 3
    dti = {q: ms(off[f"dti_{q}"])[0] for q in Q}
    peak = max(dti, key=dti.get)
    second = sorted(dti, key=dti.get)[-2]
    dti_mean = {q: ms(off[f"dti_mean_{q}"])[0] for q in Q}
    peak_mean = max(dti_mean, key=dti_mean.get)
    # pattern 4
    zs_off, zs_b0 = ms(off.zero_savings_rate_mean)[0], ms(b0.zero_savings_rate_mean)[0]

    N.update(
        stack2_holders_check=sh0, ever_stack2_adopters_check=ev0, cfpb_cross_firm=0.32,
        vol_per_eligible_year=ms(v_elig)[0], vol_per_adopter_year=ms(v_adopt)[0],
        vol_band_lo=lo_vol, vol_band_hi=hi_vol,
        mean_purchase_beta0=mp0, mean_purchase_beta0_sd=mp0_sd, mean_purchase_beta1=mp1,
        mean_purchase_target=target, mean_purchase_gap=gap0, mean_purchase_margin=margin,
        mean_purchase_inside_beta0=inside0, mean_purchase_inside_beta1=inside1,
        mean_purchase_q345=br35, mean_purchase_q45=br45,
        p1_arrears_beta0=d_arr0, p1_arrears_beta0_se=se_arr0,
        p1_arrears_beta1=d_arr1, p1_arrears_beta1_se=se_arr1,
        p1_interest_beta0=r_int0, p1_interest_beta1=r_int1,
        p3_peak=peak, p3_peak_value=dti[peak], p3_second=second, p3_second_value=dti[second],
        p3_mean_peak=peak_mean, p4_zero_savings_off=zs_off, p4_zero_savings_beta0=zs_b0,
        p4_target=0.36,
    )
    vol_elig_verdict = "inside" if lo_vol <= N["vol_per_eligible_year"] <= hi_vol else ("below" if N["vol_per_eligible_year"] < lo_vol else "above")
    vol_adopt_verdict = "inside" if lo_vol <= N["vol_per_adopter_year"] <= hi_vol else ("below" if N["vol_per_adopter_year"] < lo_vol else "above")
    rows = [
        group_row("Stacking (Submodel 13)", 4),
        f"Holders with two or more facilities, final tick & {pct(sh0, 1)}\\% & 32\\% of borrowers, across firms, over a year & order of magnitude; ever-stacked share of ever-adopters {pct(ev0, 1)}\\% \\\\",
        group_row("Volume (Submodel 4)", 4),
        f"Annual \\ac{{BNPL}} volume per eligible household & {rand(N['vol_per_eligible_year'])} & {rand(lo_vol)}--{rand(hi_vol)} (per signed-up and per active customer) & {vol_elig_verdict} the band; eligible households compare with the lower bound \\\\",
        f"Annual \\ac{{BNPL}} volume per adopting household & {rand(N['vol_per_adopter_year'])} & as above & {vol_adopt_verdict} the band; adopters compare with the upper bound \\\\",
        f"Mean want-driven purchase, $\\beta = 0$ & {rand(mp0, 2)} & {rand(target, 0)} $\\pm$ 35\\% ({rand(lo_band)}--{rand(hi_band)}) & {-gap0 * 100:.2f}\\% low: inside the band by {rand(margin, 2)}; {inside0} of 20 replicates inside; Q3--Q5 mean {rand(br35)}, Q4--Q5 {rand(br45)} \\\\",
        f"Mean want-driven purchase, $\\beta = 1$ & {rand(mp1, 2)} & as above & {(1 - mp1 / target) * 100:.2f}\\% low: outside; {inside1} of 20 inside \\\\",
        group_row("Registered patterns (Table~\\ref{tab:patterns})", 4),
        f"Pattern 1: traditional arrears rate, on less off & {pm(d_arr0, se_arr0)}pp; {pm(d_arr1, se_arr1)}pp & rise & rises \\\\",
        f"Pattern 1: traditional interest charged, on over off & ${r_int0 * 100:+.1f}\\%$; ${r_int1 * 100:+.1f}\\%$ & rise & falls: mixed \\\\",
        f"Pattern 3: aggregate debt-to-income peak, no \\ac{{BNPL}} & {peak} ({dti[peak]:.2f}); {second} second ({dti[second]:.2f}) & middle-income peak & reproduced on the registered statistic; the mean of ratios peaks in {peak_mean} \\\\",
        f"Pattern 4: zero liquid savings & {pct(zs_off, 1)}\\% (no \\ac{{BNPL}}); {pct(zs_b0, 1)}\\% ($\\beta = 0$) & 36\\% expected to miss a payment & same order \\\\",
    ]
    table(
        "tab_bnpl_on_checks",
        "Unfitted checks on the \\ac{BNPL}-on model",
        f"Every comparison here is against a quantity no parameter was fitted to. Model values are "
        f"{REPL.lower()} from the $\\beta = 0$ arm of Table~\\ref{{tab:baseline-arms}} unless the "
        f"$\\beta = 1$ arm is named; Patterns 3 and 4 use the no-\\ac{{BNPL}} baseline. The "
        f"\\ac{{CFPB}} share counts borrowers with loans at more than one firm at any point in a year "
        f"\\cite{{cfpb2025bnpl}}, so the closer model analogue is the over-the-horizon share. Volumes "
        f"are the post-burn-in cumulative volume divided by the number of eligible (banked) households "
        f"or of households that ever held a balance, annualised over the {yrs:.2f}-year post-burn-in "
        f"horizon; the band is the 2017-Rand provider disclosure whose customer denominator is not "
        f"stated \\cite{{weaver2025iar}}. The mean-purchase comparison population (all adopters), "
        f"statistic, target and tolerance were registered before the run; the Q3--Q5 and Q4--Q5 "
        f"means explain the gap and are not alternative comparison populations. Pattern 1 differences "
        f"carry one unpaired standard error.",
        "L{3.6cm}L{2.9cm}L{3.2cm}L{4.1cm}",
        r"\textbf{Check} & \textbf{Model} & \textbf{Benchmark} & \textbf{Reading}",
        rows,
        size=r"\footnotesize",
        colsep="3pt",
    )


# ============================================================ 5 the scenario panel
def tab_scenarios(rq3: pd.DataFrame) -> None:
    def cellset(b):
        return {key: arm(rq3, f"rq3_{key}_b{b}") for key, _ in SCENARIOS}
    arms = {0.0: cellset(0.0), 1.0: cellset(1.0)}
    outcomes = [
        ("Population default rate (\\%)", "default_rate_final", 100, 2),
        ("90+ day arrears, credit-active (\\%)", "active_90_plus_mean", 100, 2),
        ("Traditional arrears rate (\\%)", "trad_arrears_rate_mean", 100, 2),
        ("\\ac{BNPL} adoption, end of horizon (\\%)", "bnpl_adoption_final", 100, 2),
        ("Cumulative \\ac{BNPL} volume (R m)", "bnpl_volume_cumulative", 1e-6, 2),
        ("Applications refused at the gate", "trad_refused_gate", 1, 0),
    ] + [(f"Default rate, {q} (\\%)", f"default_rate_final_{q}", 100, 2) for q in Q]
    rows = []
    for name, col, scale, d in outcomes:
        cells = [name]
        for b in (0.0, 1.0):
            cells += [cell(arms[b][key][col], d, scale) for key, _ in SCENARIOS]
        rows.append(" & ".join(cells) + r" \\")
    # differences to the benchmark, for the note
    notes = []
    for b in (0.0, 1.0):
        bench = arms[b]["kcool0"]
        parts = []
        for key, name in SCENARIOS[1:]:
            dd, se = diff(arms[b][key].default_rate_final, bench.default_rate_final)
            dv = ms(arms[b][key].bnpl_volume_cumulative)[0] / ms(bench.bnpl_volume_cumulative)[0] - 1
            da, sea = diff(arms[b][key].active_90_plus_mean, bench.active_90_plus_mean)
            N[f"scen_{key}_beta{b:g}_default"] = dd
            N[f"scen_{key}_beta{b:g}_default_se"] = se
            N[f"scen_{key}_beta{b:g}_volume_rel"] = dv
            N[f"scen_{key}_beta{b:g}_90plus"] = da
            N[f"scen_{key}_beta{b:g}_90plus_se"] = sea
            N[f"scen_{key}_beta{b:g}_refused"] = ms(arms[b][key].trad_refused_gate)[0]
            parts.append(f"{name.lower()} {pm(dd, se)}pp on default, {pm(da, sea)}pp on 90+ arrears and ${dv * 100:+.1f}\\%$ on volume")
        N[f"scen_bench_beta{b:g}_default"] = ms(bench.default_rate_final)[0]
        N[f"scen_bench_beta{b:g}_refused"] = ms(bench.trad_refused_gate)[0]
        notes.append(f"at $\\beta = {b:g}$, " + "; ".join(parts))
    table(
        "tab_scenarios",
        "Three scenarios for the lending environment, with and without peer influence",
        f"The benchmark (pre-2026 position: \\ac{{BNPL}} invisible to the bureau and lightly screened), "
        f"bureau visibility (\\ac{{BNPL}} obligations enter the Regulation 23A test of the traditional "
        f"lender: the 2026 reporting requirement through its affordability channel only, the scoring "
        f"channel being outside the model) and mandatory screening (the Regulation 23A test applied to "
        f"\\ac{{BNPL}} originations), each at $\\beta = 0$ and $\\beta = 1$. Outcomes as in "
        f"Table~\\ref{{tab:baseline-arms}}; the by-quintile rows are the default rate within each "
        f"per-capita income quintile of the population. {REPL}; seeds 40{{,}}000--40{{,}}019 "
        f"(benchmark), 41{{,}}000--41{{,}}019 (bureau) and 42{{,}}000--42{{,}}019 (screening); {SHOCK}. "
        f"Scenario less benchmark, {SE}: {'; '.join(notes)}.",
        "L{3.5cm}rrrrrr",
        r"& \multicolumn{3}{c}{$\beta = 0$} & \multicolumn{3}{c}{$\beta = 1$} \\ \cmidrule(lr){2-4}\cmidrule(lr){5-7}"
        "\n\\textbf{Outcome} & \\textbf{Benchmark} & \\textbf{Bureau} & \\textbf{Screening} & \\textbf{Benchmark} & \\textbf{Bureau} & \\textbf{Screening}",
        rows,
        size=r"\scriptsize",
        colsep="2.5pt",
    )


# ============================================================ 4.3 distribution
def tab_distribution(rq0: pd.DataFrame) -> None:
    off, b0, b1 = (arm(rq0, l) for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))
    rows = []
    sd_share, sd_dti, sd_purchase = 0.0, 0.0, 0.0
    sizes: list[str] = []
    for q in Q:
        n_q = int(b0[f"n_agents_{q}"].iloc[0])
        shares = [b0[f"bnpl_adoption_final_{q}"], b0[f"trad_arrears_final_{q}"], b0[f"bnpl_rolling_bind_{q}"]]
        sd_share = max(sd_share, *(ms(s)[1] for s in shares))
        sd_dti = max(sd_dti, ms(off[f"dti_{q}"])[1])
        sd_purchase = max(sd_purchase, ms(b0[f"bnpl_purchase_mean_realised_{q}"])[1])
        sizes.append(num(n_q))
        cells = [
            q,
            cell(off[f"default_rate_final_{q}"], 2),
            cell(b0[f"default_rate_final_{q}"], 2),
            pct(ms(shares[0])[0], 1),
            pct(ms(shares[1])[0], 1),
            f"{ms(off[f'dti_{q}'])[0]:.2f}",
            pct(ms(shares[2])[0], 1),
            num(ms(b0[f"bnpl_purchase_mean_realised_{q}"])[0]),
        ]
        rows.append(" & ".join(cells) + r" \\")
        N[f"default_{q}_off"] = ms(off[f"default_rate_final_{q}"])[0]
        N[f"default_{q}_beta0"] = ms(b0[f"default_rate_final_{q}"])[0]
        N[f"default_{q}_beta1"] = ms(b1[f"default_rate_final_{q}"])[0]
        N[f"adoption_{q}_beta0"] = ms(b0[f"bnpl_adoption_final_{q}"])[0]
        N[f"arrears_{q}_beta0"] = ms(b0[f"trad_arrears_final_{q}"])[0]
        N[f"dti_{q}"] = ms(off[f"dti_{q}"])[0]
        N[f"bind_{q}_beta0"] = ms(b0[f"bnpl_rolling_bind_{q}"])[0]
        N[f"purchase_{q}_beta0"] = ms(b0[f"bnpl_purchase_mean_realised_{q}"])[0]
        d, se = diff(b0[f"default_rate_final_{q}"], off[f"default_rate_final_{q}"])
        N[f"injection_{q}_beta0"], N[f"injection_{q}_beta0_se"] = d, se
    inj = "; ".join(f"{q} {pm(N[f'injection_{q}_beta0'], N[f'injection_{q}_beta0_se'])}pp" for q in Q)
    table(
        "tab_distribution",
        "Outcomes by income quintile",
        f"Each row is one per-capita income quintile of the 5{{,}}000-household population (the "
        f"weighted \\ac{{NIDS}} bounds of Appendix~\\ref{{app:variables}}; quintile sizes "
        f"{', '.join(sizes[:-1])} and {sizes[-1]} households). "
        f"Default is the share of the quintile's households in default at the final tick, in the "
        f"no-\\ac{{BNPL}} baseline and in the $\\beta = 0$ arm of Table~\\ref{{tab:baseline-arms}} "
        f"(the $\\beta = 1$ arm by quintile is in Table~\\ref{{tab:scenarios}}); "
        f"adoption and traditional arrears are final-tick shares of the quintile's households in the "
        f"$\\beta = 0$ arm, in per cent; debt-to-income is the aggregate ratio (total debt over total "
        f"monthly income in the quintile) in the baseline; limit binding is the share of the quintile's "
        f"\\ac{{BNPL}} requests refused by the rolling per-platform limit, in per cent; the mean purchase "
        f"is over the quintile's want-driven originations, in 2017 Rands. The default columns are "
        f"{REPL.lower()}; the five right-hand columns are replicate means, with standard deviations of "
        f"at most {sd_share * 100:.1f} points for the three shares, {sd_dti:.2f} for the ratio and "
        f"R{sd_purchase:.0f} for the purchase. {SHOCK_CAP}. The injection "
        f"($\\beta = 0$ less no-\\ac{{BNPL}}) raises default by {inj}; {SE}.",
        "c rr r r r r r",
        r"& \multicolumn{2}{c}{Default rate (\%)} & & & & & \\ \cmidrule(lr){2-3}"
        "\n\\textbf{Quintile} & \\textbf{No \\ac{BNPL}} & \\textbf{$\\beta=0$} & "
        "\\textbf{Adoption} & \\textbf{Arrears} & \\textbf{Debt/inc.} & \\textbf{Limit binds} & \\textbf{Purchase (R)}",
        rows,
        size=r"\scriptsize",
        colsep="3pt",
    )


# ============================================================ 4.2 access (numbers for the prose)
def tab_access(rq2: pd.DataFrame, rq2t: pd.DataFrame) -> None:
    from simulation.analysis import linear_departure

    rows = [group_row("Linear coupling, Equation~\\ref{eq:peer} ($\\beta$ swept)", 5)]
    rises = {}
    for b in sorted(rq2.beta.unique()):
        g = rq2[rq2.beta == b].groupby("bnpl_access_rate").default_rate_final.mean().sort_index()
        d = linear_departure(g.index, g.values)
        rises[b] = d["rise"]
        lo = rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 0.0)].default_rate_final
        hi = rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 1.0)].default_rate_final
        dd, se = diff(hi, lo)
        tag = " (control)" if b == 0 else ""
        rows.append(f"$\\beta = {b:g}${tag} & {pm(dd, se)} & {d['linear_r2']:.3f} & {d['max_dev_frac'] * 100:.1f}\\% & -- \\\\")
        N[f"access_rise_beta{b:g}"], N[f"access_rise_beta{b:g}_se"], N[f"access_r2_beta{b:g}"] = dd, se, d["linear_r2"]
    N["access_amplification"] = max(rises.values()) / rises[0.0]
    N["access_r2_min"] = min(N[f"access_r2_beta{b:g}"] for b in rq2.beta.unique())

    rows.append(group_row("Heterogeneous thresholds ($\\sigma_\\theta$ swept, $\\gamma = 0.3$; $\\gamma = 0$ is the control)", 5))
    surf = rq2t[rq2t.label.str.startswith("rq2t_a")]
    ctrl = surf[surf.gamma == 0].groupby("bnpl_access_rate")[["default_rate_final", "bnpl_adoption_final"]].mean().sort_index()
    dc = linear_departure(ctrl.index, ctrl.default_rate_final.values)
    ac = linear_departure(ctrl.index, ctrl.bnpl_adoption_final.values)
    rows.append(f"$\\gamma = 0$ (control) & {dc['rise'] * 100:+.2f} & {dc['linear_r2']:.3f} & {dc['max_dev_frac'] * 100:.1f}\\% & {ac['rise'] * 100:+.1f}pp, $R^2$ {ac['linear_r2']:.3f} \\\\")
    N["thr_ctrl_default_rise"], N["thr_ctrl_default_r2"] = dc["rise"], dc["linear_r2"]
    N["thr_ctrl_adoption_rise"] = ac["rise"]
    thr_r2, ad_rises, d_rises = [], [], []
    for s in sorted(surf.sigma_theta.unique()):
        sub = surf[(surf.gamma > 0) & (surf.sigma_theta == s)].groupby("bnpl_access_rate")[["default_rate_final", "bnpl_adoption_final"]].mean().sort_index()
        d = linear_departure(sub.index, sub.default_rate_final.values)
        a = linear_departure(sub.index, sub.bnpl_adoption_final.values)
        thr_r2.append(d["linear_r2"]); ad_rises.append(a["rise"]); d_rises.append(d["rise"])
        rows.append(f"$\\sigma_\\theta = {s:g}$ & {d['rise'] * 100:+.2f} & {d['linear_r2']:.3f} & {d['max_dev_frac'] * 100:.1f}\\% & {a['rise'] * 100:+.1f}pp, $R^2$ {a['linear_r2']:.3f} \\\\")
    N.update(thr_default_r2_min=min(thr_r2), thr_adoption_rise_max=max(ad_rises),
             thr_default_rise_min=min(d_rises), thr_default_rise_max=max(d_rises))
    mu = rq2t[rq2t.label.str.startswith("rq2t_mu")]
    rows.append(group_row("Threshold mean $\\mu_\\theta$ at full access, $\\sigma_\\theta = 0.20$, $\\gamma = 0.3$", 5))
    mus = {}
    for m, sub in mu.groupby("mu_theta"):
        rows.append(f"$\\mu_\\theta = {m:g}$ & \\multicolumn{{3}}{{l}}{{default {cell(sub.default_rate_final, 2)}\\%}} & adoption {cell(sub.bnpl_adoption_final, 1)}\\% \\\\")
        mus[m] = (ms(sub.bnpl_adoption_final)[0], ms(sub.default_rate_final)[0])
    N["mu_adoption_lo"], N["mu_default_lo"] = mus[max(mus)]
    N["mu_adoption_hi"], N["mu_default_hi"] = mus[min(mus)]
    table(
        "tab_access",
        "Linearity of the default and adoption response to \\ac{BNPL} access",
        "Each row fits a straight line to the mean default rate at the seven access rates swept "
        "(0 to 1.0 of the banked subpopulation; the banked ceiling is 82.8\\% of all households) and "
        "reports the total rise from zero access to full access (with one unpaired standard error "
        "over the two end arms' replicates), the $R^2$ of the linear fit, and the largest residual as "
        "a share of the rise; a tipping point would show a low $R^2$ and a large residual. The "
        "threshold rows repeat the diagnostic for adoption. Linear-coupling cells have seeds "
        "30{,}000--30{,}019, threshold cells 60{,}000--60{,}019 and the $\\mu_\\theta$ arms "
        "61{,}000--61{,}019; 20 replicates each; " + SHOCK + ". The $\\gamma = 0$ control is identical "
        "at every $\\sigma_\\theta$ because thresholds are then never consulted.",
        "L{4.1cm}rrrL{3.0cm}",
        r"\textbf{Arm} & \textbf{Default rise (pp)} & \textbf{$R^2$} & \textbf{Max residual} & \textbf{Adoption}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ 4.4 robustness
def tab_robustness(rob: pd.DataFrame) -> None:
    def a(label):
        return arm(rob, label)

    def row(name, label, ref_label=None, paired=False):
        d = a(label)
        if ref_label is None:
            return f"{name} & {cell(d.default_rate_final, 2)} & reference \\\\"
        if paired:
            dd, se = paired_diff(d, a(ref_label), "default_rate_final")
            return f"{name} & {cell(d.default_rate_final, 2)} & {pm(dd, se)[:-1]}^\\dagger$ \\\\"
        dd, se = diff(d.default_rate_final, a(ref_label).default_rate_final)
        return f"{name} & {cell(d.default_rate_final, 2)} & {pm(dd, se)} \\\\"

    rules = [("shortfall", "exact shortfall"), ("shortfall_125", "shortfall $+25\\%$"),
             ("shortfall_plus_committed", "shortfall $+$ one tick of committed spending")]
    rows = [group_row("Borrowing-amount rule (Submodel 4), \\ac{BNPL} share of a shortfall capped", 3)]
    rows.append(row(rules[0][1], "rob_amount_shortfall"))
    for key, name in rules[1:]:
        rows.append(row(name, f"rob_amount_{key}", "rob_amount_shortfall"))
    rows.append(group_row("The same rules with the cap removed (paired with the row above by seed)", 3))
    for key, name in rules:
        rows.append(row(name + ", uncapped", f"rob_amount_{key}_uncapped", f"rob_amount_{key}", paired=True))
    rows.append(group_row("Default horizon $k$ (Submodel 7)", 3))
    rows.append(row("$k = 7$ ticks, 98 days", "rob_k7"))
    rows.append(row("$k = 4$ ticks, 56 days", "rob_k4", "rob_k7"))
    rows.append(group_row("Purchase size $\\kappa$ (Submodel 4)", 3))
    kappas = sorted(float(l.replace("rob_kappa", "")) for l in rob.label.unique() if l.startswith("rob_kappa"))
    mid = kappas[1]
    rows.append(row(f"$\\kappa = {mid:g}$ (IES-derived)", f"rob_kappa{mid}"))
    for k in (kappas[0], kappas[2]):
        rows.append(row(f"$\\kappa = {k:g}$", f"rob_kappa{k}", f"rob_kappa{mid}"))
    rows.append(group_row("Purchase sizing base (Submodel 4)", 3))
    rows.append(row("monthly discretionary budget", "rob_base_discretionary"))
    rows.append(row("monthly income, $\\kappa$ matched", "rob_base_income", "rob_base_discretionary"))

    amount_vals = [ms(a(f"rob_amount_{k}{s}").default_rate_final)[0] for k, _ in rules for s in ("", "_uncapped")]
    N.update(
        rob_amount_min=min(amount_vals), rob_amount_max=max(amount_vals),
        rob_amount_shortfall=ms(a("rob_amount_shortfall").default_rate_final)[0],
        rob_amount_plus_committed=ms(a("rob_amount_shortfall_plus_committed").default_rate_final)[0],
        rob_k4=ms(a("rob_k4").default_rate_final)[0], rob_k7=ms(a("rob_k7").default_rate_final)[0],
        rob_kappa_lo=ms(a(f"rob_kappa{kappas[0]}").default_rate_final)[0],
        rob_kappa_hi=ms(a(f"rob_kappa{kappas[2]}").default_rate_final)[0],
        rob_base_income=ms(a("rob_base_income").default_rate_final)[0],
        rob_base_discretionary=ms(a("rob_base_discretionary").default_rate_final)[0],
    )
    dd, se = diff(a("rob_k4").default_rate_final, a("rob_k7").default_rate_final)
    N["rob_k4_minus_k7"], N["rob_k4_minus_k7_se"] = dd, se
    table(
        "tab_robustness",
        "Sensitivity of the default rate: principal arms",
        f"Population default rate at $\\beta = 1$, four platforms and full access, for the sensitivity "
        f"arms whose range exceeds replicate noise. Each group has its own reference arm at the baseline "
        f"value, run on its own seed set (amount rules 50{{,}}000--50{{,}}019, horizon 54{{,}}000--, "
        f"$\\kappa$ 57{{,}}000--, base 59{{,}}000--), so references differ from one another by seed "
        f"noise only. {REPL}. The difference column is arm less reference with one unpaired standard "
        f"error, except $\\dagger$: the uncapped arms share seeds with their capped twins and the "
        f"difference is paired, uncapped less capped. The shortfall rule and its cap have no literature "
        f"anchor (Section~\\ref{{sec:amount}}). The remaining arms are in "
        f"Table~\\ref{{tab:robustness-appendix}}.",
        "L{7.2cm}rr",
        r"\textbf{Arm} & \textbf{Default (\%)} & \textbf{Difference (pp)}",
        rows,
        size=r"\footnotesize",
    )

    # appendix: the rest
    rows = [group_row("Activation order (Submodel 17)", 3),
            row("random, reseeded each tick", "rob_act_random"),
            row("fixed order, the same every tick", "rob_act_uniform", "rob_act_random"),
            group_row("Population size", 3),
            row("5{,}000 households", "rob_n5000"),
            row("1{,}000 households", "rob_n1000", "rob_n5000"),
            row("10{,}000 households", "rob_n10000", "rob_n5000"),
            group_row("Minimum-payer share (Submodel 6)", 3),
            row("0.29 (transferred United States estimate)", "rob_m0.29")]
    for m in (0.2, 0.25, 0.35, 0.4):
        rows.append(row(f"{m:.2f}", f"rob_m{m}", "rob_m0.29"))
    rows += [group_row("Minimum-payment fraction of balance per month (Submodel 6)", 3),
             row("0.05", "rob_minpay0.05")]
    for f in (0.025, 0.1):
        rows.append(row(f"{f:g}", f"rob_minpay{f}", "rob_minpay0.05"))
    rows += [group_row("Rolling per-platform limit $\\lambda$, months of income (Submodel 12)", 3),
             row("0.10", "rob_limit0.1")]
    for lam in (0.25, 0.5, 1.0):
        rows.append(row(f"{lam:.2f}", f"rob_limit{lam}", "rob_limit0.1"))
    rows += [group_row("Income-shock persistence (Submodel 1)", 3),
             row("persistent until re-employment (baseline rule, seeds 50{,}000--)", "rob_amount_shortfall"),
             row("single-tick shock", "rob_shock_single_tick", "rob_amount_shortfall")]
    N.update(
        rob_act_random=ms(a("rob_act_random").default_rate_final)[0],
        rob_act_uniform=ms(a("rob_act_uniform").default_rate_final)[0],
        rob_n1000=ms(a("rob_n1000").default_rate_final)[0],
        rob_n5000=ms(a("rob_n5000").default_rate_final)[0],
        rob_n10000=ms(a("rob_n10000").default_rate_final)[0],
        rob_m_min=min(ms(a(f"rob_m{m}").default_rate_final)[0] for m in (0.2, 0.25, 0.29, 0.35, 0.4)),
        rob_m_max=max(ms(a(f"rob_m{m}").default_rate_final)[0] for m in (0.2, 0.25, 0.29, 0.35, 0.4)),
        rob_limit_lo=ms(a("rob_limit0.1").default_rate_final)[0],
        rob_limit_hi=ms(a("rob_limit1.0").default_rate_final)[0],
        rob_shock_single=ms(a("rob_shock_single_tick").default_rate_final)[0],
    )
    table(
        "tab_robustness_appendix",
        "Sensitivity of the default rate: remaining arms",
        f"Population default rate at $\\beta = 1$, four platforms and full access, for the remaining "
        f"sensitivity arms, laid out as Table~\\ref{{tab:robustness}}: each group's reference is its "
        f"baseline value on the group's own seed set (activation 53{{,}}000--, population 55{{,}}000--, "
        f"minimum-payer share 51{{,}}000--, minimum payment 52{{,}}000--, limit 56{{,}}000--, "
        f"single-tick shock 58{{,}}000--). {REPL}; differences are arm less reference with one unpaired "
        f"standard error. The single-tick shock arm recovers the original one-tick income-loss rule, "
        f"which no shock probability in range could calibrate to the \\ac{{CCMR}} 90+ band.",
        "L{7.2cm}rr",
        r"\textbf{Arm} & \textbf{Default (\%)} & \textbf{Difference (pp)}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ C: Sobol
def tab_sobol() -> None:
    data = json.loads((SUMMARY / "sobol_indices.json").read_text(encoding="utf-8"))
    names = {
        "q_base": "$q_{\\text{base}}$ (Submodel 11)", "beta": "$\\beta$ (Submodel 11)",
        "min_payment_frac": "minimum-payment fraction (Submodel 6)",
        "bnpl_purchase_ratio": "$\\kappa$ (Submodel 4)",
        "bnpl_limit_income_multiple": "$\\lambda$ (Submodel 12)",
        "shock_prob": "shock probability (Submodel 1, fitted)",
    }
    bounds = dict(zip(data["problem"]["names"], data["problem"]["bounds"]))
    idx = {k: {r["parameter"]: r for r in v} for k, v in data["indices"].items()}
    rows = []

    def z(x: float) -> str:  # a bootstrap estimate that rounds to zero prints without a sign
        return f"{x:.2f}".replace("-0.00", "0.00")

    for p in data["problem"]["names"]:
        d, ad = idx["default_rate_final"][p], idx["bnpl_adoption_final"][p]
        lo, hi = bounds[p]
        rows.append(
            f"{names[p]} & {lo:g}--{hi:g} & ${z(d['S1'])} \\pm {d['S1_conf']:.2f}$ & ${z(d['ST'])} \\pm {d['ST_conf']:.2f}$ "
            f"& ${z(ad['S1'])} \\pm {ad['S1_conf']:.2f}$ & ${z(ad['ST'])} \\pm {ad['ST_conf']:.2f}$ \\\\"
        )
    sh = idx["default_rate_final"]["shock_prob"]
    N.update(sobol_shock_s1=sh["S1"], sobol_shock_s1_conf=sh["S1_conf"],
             sobol_bnpl_st_max=max(r["ST"] for p, r in idx["default_rate_final"].items() if p != "shock_prob"),
             sobol_n=data["n_base_samples"], sobol_runs=data["n_design_points"] * data["replicates"])
    table(
        "tab_sobol",
        "Sobol indices for the population default rate and \\ac{BNPL} adoption",
        f"First-order ($S_1$) and total-order ($S_T$) Sobol indices with 95\\% bootstrap confidence "
        f"half-widths, from a Saltelli design of $N = {data['n_base_samples']}$ base samples over six "
        f"parameters ({num(data['n_design_points'])} design points, {data['replicates']} replicates each; "
        f"{num(N['sobol_runs'])} runs), \\ac{{BNPL}} on at $\\beta$ drawn from its range and every other "
        f"parameter at its calibrated value. The indices decompose the variance of the final-tick "
        f"outcome across the ranges shown; an $S_1$ above one reflects bootstrap noise around a "
        f"single dominant parameter. They describe what moves the \\emph{{level}} of default when "
        f"parameters are uncertain; the \\ac{{BNPL}} \\emph{{effect}}, a difference between arms at "
        f"fixed parameters, is a separate quantity and is not decomposed here.",
        "L{4.0cm}c rr rr",
        r"& & \multicolumn{2}{c}{Default rate} & \multicolumn{2}{c}{Adoption} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-6}"
        "\n\\textbf{Parameter} & \\textbf{Range} & \\textbf{$S_1$} & \\textbf{$S_T$} & \\textbf{$S_1$} & \\textbf{$S_T$}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ C: cooling-off and cap
def lever_table(rq3: pd.DataFrame, name: str, caption: str, arms: list[tuple[str, str]], note_extra: str) -> None:
    rows = []
    sd_adopt = 0.0
    for key, label in arms:
        cells = [label]
        for b in (0.0, 1.0):
            d = arm(rq3, f"rq3_{key}_b{b}")
            bench = arm(rq3, f"rq3_kcool0_b{b}")
            dv = ms(d.bnpl_volume_cumulative)[0] / ms(bench.bnpl_volume_cumulative)[0] - 1
            dd, se = diff(d.default_rate_final, bench.default_rate_final)
            sd_adopt = max(sd_adopt, ms(d.bnpl_adoption_final)[1])
            cells += [cell(d.default_rate_final, 2), pm(dd, se) if key != "kcool0" else "--",
                      pct(ms(d.bnpl_adoption_final)[0], 1), f"{dv * 100:+.1f}" if key != "kcool0" else "--"]
            N[f"lever_{key}_beta{b:g}_default"] = ms(d.default_rate_final)[0]
            N[f"lever_{key}_beta{b:g}_diff"], N[f"lever_{key}_beta{b:g}_diff_se"] = dd, se
            N[f"lever_{key}_beta{b:g}_volume_rel"] = dv
        rows.append(" & ".join(cells) + r" \\")
    table(
        name,
        caption,
        f"Outcomes as in Table~\\ref{{tab:scenarios}}, against the same benchmark arm; the difference "
        f"is lever less benchmark on default with one unpaired standard error, and the volume column "
        f"is the change in cumulative post-burn-in \\ac{{BNPL}} volume relative to the benchmark, the "
        f"defer-versus-desist criterion. Default, in per cent: {REPL.lower()}; adoption at the final "
        f"tick is a replicate mean in per cent with a standard deviation of at most "
        f"{sd_adopt * 100:.1f} points; the volume change is in per cent of the benchmark. "
        f"{SHOCK_CAP}. {note_extra}",
        "L{2.6cm} rrrr rrrr",
        r"& \multicolumn{4}{c}{$\beta = 0$} & \multicolumn{4}{c}{$\beta = 1$} \\ \cmidrule(lr){2-5}\cmidrule(lr){6-9}"
        "\n\\textbf{Arm} & \\textbf{Default} & \\textbf{$\\Delta$ (pp)} & \\textbf{Adopt.} & \\textbf{Vol.} "
        "& \\textbf{Default} & \\textbf{$\\Delta$ (pp)} & \\textbf{Adopt.} & \\textbf{Vol.}",
        rows,
        size=r"\scriptsize",
        colsep="2pt",
    )


def tab_levers(rq3: pd.DataFrame) -> None:
    lever_table(
        rq3, "tab_cooloff", "The cooling-off window",
        [("kcool0", "none (benchmark)")] + [(f"kcool{k}", f"{k} tick{'s' if k > 1 else ''} ({k * 14} days)") for k in (1, 2, 3, 4)],
        "The window blocks want-driven \\ac{BNPL} purchases for $k^{\\text{cool}}$ ticks after an "
        "order; one tick is the fourteen-day right of withdrawal in the United Kingdom's rules "
        "\\cite{fca_ps26_1}. Seeds 40{,}000--40{,}019 in every arm. Where peer influence is present "
        "the window also lowers the adoption share each household observes, which is the one "
        "lever-by-peer interaction in the model.",
    )
    lever_table(
        rq3, "tab_cap", "The concurrent-facility cap (hypothetical)",
        [("kcool0", "none (benchmark)")] + [(f"cap{c}", f"{c} facilit{'y' if c == 1 else 'ies'}") for c in (1, 2, 3)],
        "No jurisdiction imposes a cap on concurrent \\ac{BNPL} facilities; the arm is hypothetical. "
        "The cap refuses any new draw while the household already holds the stated number of open "
        "facilities, on any platform, so a cap of one is a one-agreement-at-a-time rule and is "
        "stricter than a single platform, on which a household may hold several agreements. Seeds "
        "43{,}000--43{,}019 for the cap arms and 40{,}000--40{,}019 for the benchmark.",
    )


# ============================================================ main
# Effect-robustness suite: (setting, display name, off-arm setting). The off arm is the
# setting's own where the setting changes the BNPL-free model, else the reference off arm.
EFFECT_ROWS = [
    ("Reference", [("ref", "all parameters at default values", "ref")]),
    ("Borrowing amount on a shortfall (Submodel 4)", [
        ("amount125", "shortfall $+25\\%$", "amount125"),
        ("amountcommitted", "shortfall $+$ one tick of committed spending", "amountcommitted"),
        ("uncapped", "exact shortfall, \\ac{BNPL} cap removed", "ref"),
        ("amount125_uncapped", "shortfall $+25\\%$, cap removed", "amount125"),
        ("amountcommitted_uncapped", "shortfall $+$ committed, cap removed", "amountcommitted"),
    ]),
    ("Default horizon (Submodel 7)", [("k4", "$k = 4$ ticks, 56 days", "k4")]),
    ("Minimum payments (Submodel 6)", [
        ("minpay0.025", "minimum-payment fraction 0.025", "minpay0.025"),
        ("minpay0.1", "minimum-payment fraction 0.10", "minpay0.1"),
        ("m0.2", "minimum-payer share 0.20", "m0.2"),
        ("m0.4", "minimum-payer share 0.40", "m0.4"),
    ]),
    ("Purchase size and limits (Submodels 4 and 12)", [
        ("kappa0.07", "$\\kappa = 0.07$", "ref"),
        ("kappa0.28", "$\\kappa = 0.28$", "ref"),
        ("base_income", "purchases sized on income", "ref"),
        ("limit0.25", "rolling limit $\\lambda = 0.25$", "ref"),
        ("limit1.0", "rolling limit $\\lambda = 1.0$", "ref"),
    ]),
    ("Income-shock persistence (Submodel 1)", [
        ("shock_single_tick", "single-tick shock", "shock_single_tick"),
    ]),
]


def tab_effect(eff: pd.DataFrame) -> None:
    def a(label: str) -> pd.DataFrame:
        return arm(eff, label)

    rows, effects0, effects1 = [], {}, {}
    for group, items in EFFECT_ROWS:
        rows.append(group_row(group, 4))
        for key, name, off_key in items:
            off = a(f"eff_{off_key}_off")
            d0, s0 = paired_diff(a(f"eff_{key}_b0.0"), off, "default_rate_final")
            d1, s1 = paired_diff(a(f"eff_{key}_b1.0"), off, "default_rate_final")
            effects0[key], effects1[key] = (d0, s0), (d1, s1)
            rows.append(f"{name} & {cell(off.default_rate_final)} & {pm(d0, s0)} & {pm(d1, s1)} \\\\")
    rows.append(group_row("Want-driven path switched off ($q_{\\text{base}} = 0$, $\\beta = 0$)", 4))
    ref_off = a("eff_ref_off")
    dw, sw = paired_diff(a("eff_want_off_b0.0"), ref_off, "default_rate_final")
    rows.append(f"\\ac{{BNPL}} for shortfalls only & {cell(ref_off.default_rate_final)} & {pm(dw, sw)} & -- \\\\")

    for k, (d, s) in effects0.items():
        N[f"eff_{k}_b0"], N[f"eff_{k}_b0_se"] = d, s
    for k, (d, s) in effects1.items():
        N[f"eff_{k}_b1"], N[f"eff_{k}_b1_se"] = d, s
    N["eff_want_off_b0"], N["eff_want_off_b0_se"] = dw, sw
    N["eff_ref_off_default"] = ms(ref_off.default_rate_final)[0]
    b0 = [d for d, _ in effects0.values()]
    b1 = [d for d, _ in effects1.values()]
    N.update(eff_b0_min=min(b0), eff_b0_max=max(b0), eff_b1_min=min(b1), eff_b1_max=max(b1))
    table(
        "tab_effect",
        "The \\ac{BNPL} effect on default under each swept assumption",
        "The effect of enabling \\ac{BNPL} on the population default rate at the final tick, "
        "under each setting of the sensitivity analysis, at $\\beta = 0$ (the control) and "
        "$\\beta = 1$. Each setting is run with \\ac{BNPL} off and on over one seed block "
        "(70{,}000--70{,}019) shared by every arm, so each effect is a same-seed paired difference, "
        "\\ac{BNPL} on less off, with one paired standard error. The no-\\ac{BNPL} column gives the "
        "setting's own \\ac{BNPL}-free default rate where the setting changes that model, and the "
        f"reference arm's otherwise; {REPL.lower()}. {SHOCK_CAP}. The last row switches the "
        "want-driven path off, so \\ac{BNPL} is used only to cover shortfalls.",
        "L{4.8cm}rrr",
        r"\textbf{Setting} & \textbf{No \ac{BNPL} (\%)} & \textbf{Effect, $\beta=0$ (pp)} & "
        r"\textbf{Effect, $\beta=1$ (pp)}",
        rows,
        size=r"\footnotesize",
    )


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (load(n) for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    eff = load("effect")
    for df in (rq0, rq1, rq2, rq2t, rq3, rob, eff):
        assert df.groupby("label").seed.nunique().eq(20).all(), "every arm needs 20 unique seeds"
    tab_baseline_arms(rq0)
    tab_stacking(rq1)
    tab_bnpl_on_checks(rq0)
    tab_scenarios(rq3)
    tab_distribution(rq0)
    tab_access(rq2, rq2t)
    tab_robustness(rob)
    tab_sobol()
    tab_levers(rq3)
    tab_effect(eff)
    out ={k: (round(v, 6) if isinstance(v, float) else v) for k, v in N.items()}
    (SUMMARY / "results_numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote results/summary/results_numbers.json ({len(out)} numbers)")


if __name__ == "__main__":
    main()
