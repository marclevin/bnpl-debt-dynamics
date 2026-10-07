"""Generate every results table in Sections 3.5, 4, 5 and Appendix C from results/raw.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_tables.py

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
    GEN, Q, ROOT, SUMMARY, SCENARIOS, arm, cell, delta, detectable, diff, group_row, load, ms,
    num, paired_diff, pct, pm, pmb, rand, ratio_change, rm, shares_seeds, table, years,
)
from simulation.config import load_ccmr_target  # noqa: E402

N = {}  # the numbers the prose quotes; dumped to results_numbers.json at the end

# Section 3.1 states the shared conventions once (20 replicates, standard deviation in brackets,
# paired differences with one standard error, bold beyond two standard errors, the fitted
# parameters, four platforms, access for every banked household), so a note states only what
# differs or what a column means.
SEEDS_S = "seeds 80{,}000--80{,}099"
SE_P = "paired by seed"
SE_U = "unpaired, on different seed blocks"


def se_note(a: pd.DataFrame, b: pd.DataFrame) -> str:
    return SE_P if shares_seeds(a, b) else SE_U


def verb(d: float, se: float, up: str = "raises", down: str = "lowers") -> str:
    """The verb a difference supports under the two-standard-error convention."""
    if not detectable(d, se):
        return "does not detectably change"
    return up if d > 0 else down


def holders_share(d: pd.DataFrame, col: str = "stacking_2plus_final") -> pd.Series:
    """A share of all households re-expressed as a share of end-of-horizon BNPL holders."""
    return d[col] / d.bnpl_adoption_final.clip(lower=1e-9)


# ============================================================ 4 opening: the three arms
def tab_baseline_arms(rq0: pd.DataFrame) -> None:
    off, b0, b1 = (arm(rq0, l) for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))
    rows_spec = [
        ("Distress", None, 0, 0),
        ("Default rate (\\%)", "default_rate_final", 100, 2),
        ("90+ day arrears, credit-active (\\%)", "active_90_plus_mean", 100, 2),
        ("Traditional arrears, all households (\\%)", "trad_arrears_rate_mean", 100, 2),
        ("No liquid savings (\\% of households)", "zero_savings_rate_mean", 100, 1),
        ("Traditional credit", None, 0, 0),
        ("Interest charged (R m)", "trad_interest_total", 1e-6, 2),
        ("New lending (R m)", "trad_granted_value", 1e-6, 2),
        ("Refused applications", "trad_refused_gate", 1, 0),
        ("\\ac{BNPL} use", None, 0, 0),
        ("Holding at the final tick (\\%)", "bnpl_adoption_final", 100, 2),
        ("Ever held (\\%)", "ever_adopted", 100, 2),
        ("Volume (R m)", "bnpl_volume_cumulative", 1e-6, 2),
        ("Owing two or more platforms at once", None, 0, 0),
        ("Ever-holders, at any tick (\\%)", "ever_stacked_2plus_of_adopters", 100, 1),
    ]
    rows = []
    for name, col, scale, d in rows_spec:
        if col is None:
            rows.append(group_row(name, 4))
            continue
        rows.append(" & ".join([name] + [cell(x[col], d, scale) for x in (off, b0, b1)]) + r" \\")
    # holders share, computed per replicate, before the ever row
    rows.insert(
        len(rows) - 1,
        "Holders at the final tick (\\%) & -- & "
        + cell(holders_share(b0), 1) + " & " + cell(holders_share(b1), 1) + r" \\",
    )
    d0, se0 = delta(b0, off, "default_rate_final")
    d1, se1 = delta(b1, off, "default_rate_final")
    d10, se10 = delta(b1, b0, "default_rate_final")
    N.update(
        injection_beta1_less_beta0=d10, injection_beta1_less_beta0_se=se10,
        lending_beta1=ms(b1.trad_granted_value)[0],
        refused_beta1=ms(b1.trad_refused_gate)[0],
        volume_beta0=ms(b0.bnpl_volume_cumulative)[0],
        volume_beta1=ms(b1.bnpl_volume_cumulative)[0],
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
    rows += [
        "\\midrule",
        f"Default, change from no \\ac{{BNPL}} (pp) & -- & {pmb(d0, se0)} & {pmb(d1, se1)} \\\\",
    ]
    table(
        "tab_baseline_arms",
        "The baseline and the \\ac{BNPL} injection",
        "Seeds 10{,}000--10{,}019 in every arm. Holders: households owing a \\ac{BNPL} balance at "
        "the final tick. Ever: at any tick of the two-year run. Arrears, interest, savings and "
        "volume cover the post-burn-in ticks; default, lending and refusals cover the whole run.",
        "L{5.6cm}rrr",
        r"\textbf{Outcome} & \textbf{No \ac{BNPL}} & \textbf{\ac{BNPL}, $\beta=0$} & \textbf{\ac{BNPL}, $\beta=1$}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ 3.5 the calibration fit
def tab_arrears_fit() -> None:
    """The fitted baseline against the CCMR bands, from the calibration run itself."""
    from simulation.config import load_ccmr_bands

    cal = json.loads((SUMMARY / "calibration.json").read_text(encoding="utf-8"))
    runs = pd.read_parquet(SUMMARY / "calibration_runs.parquet")
    p, f = cal["fitted_shock_prob"], cal["fitted_payment_friction"]
    fit = runs[(runs.shock_prob == p) & (runs.payment_friction == f)].drop_duplicates("seed")
    assert len(fit) == 20, len(fit)
    ccmr = load_ccmr_bands()
    target = load_ccmr_target()
    model = {
        "current": ms(fit.active_current_mean)[0], "d30": ms(fit.active_d30_mean)[0],
        "d31_60": ms(fit.active_d31_60_mean)[0], "d61_90": ms(fit.active_d61_90_mean)[0],
        "d91_120": ms(fit.active_d91_120_mean)[0], "d120_plus": ms(fit.active_d120_plus_mean)[0],
        "90": ms(fit.active_90_plus_mean)[0], "60": ms(fit.active_60_plus_mean)[0],
    }
    assert abs(model["90"] - cal["objective_value"]) < 1e-9
    rows = [
        f"Current & {ccmr['current']:.2f} & {pct(model['current'])} & \\\\",
        f"1--30 days & {ccmr['d30']:.2f} & {pct(model['d30'])} & fitted \\\\",
        f"31--60 days & {ccmr['d31_60']:.2f} & {pct(model['d31_60'])} & \\\\",
        f"61--90 days & {ccmr['d61_90']:.2f} & {pct(model['d61_90'])} & \\\\",
        f"91--120 days & {ccmr['d91_120']:.2f} & {pct(model['d91_120'])} & \\\\",
        f"120+ days & {ccmr['d120_plus']:.2f} & {pct(model['d120_plus'])} & \\\\",
        "\\midrule",
        f"90+ days & {target['pct_90_plus']:.2f} & {pct(model['90'])} & fitted \\\\",
        f"60+ days & {target['pct_60_plus']:.2f} & {pct(model['60'])} & \\\\",
    ]
    grid = sorted(runs.shock_prob.unique())
    step = min(b - a for a, b in zip(grid[:-1], grid[1:]))
    stage3 = runs[runs.payment_friction == f].drop_duplicates(["shock_prob", "seed"])
    by_p = stage3.groupby("shock_prob").active_90_plus_mean.mean()
    lo_p = max(x for x in grid if x < p)
    hi_p = min(x for x in grid if x > p)
    qlfs = cal["qlfs_band"]
    fine = {float(k): v for k, v in cal["fine_grid_90_plus"].items()}
    fine_lo = max(x for x in fine if x < p)
    assert abs(fine[p] - model["90"]) < 1e-9
    N.update(
        fit_fine_step=round(p - fine_lo, 6), fit_fine_below=fine_lo, fit_90plus_fine_below=fine[fine_lo],
        fit_90plus_fine_above=fine[min(x for x in fine if x > p)],
        fit_shock_prob=p, fit_friction=f, fit_90plus=model["90"], fit_90plus_sd=ms(fit.active_90_plus_mean)[1],
        fit_d30=model["d30"], fit_d31_60=model["d31_60"], fit_d61_90=model["d61_90"],
        fit_current=model["current"], fit_60plus=model["60"],
        ccmr_d31_60=ccmr["d31_60"] / 100, ccmr_d61_90=ccmr["d61_90"] / 100,
        ccmr_60plus=target["pct_60_plus"] / 100, ccmr_d30=ccmr["d30"] / 100, ccmr_current=ccmr["current"] / 100,
        fit_grid_step=step, fit_grid_below=lo_p, fit_grid_above=hi_p,
        fit_90plus_below=float(by_p[lo_p]), fit_90plus_above=float(by_p[hi_p]),
        fit_ratio_to_qlfs_upper=p / qlfs["upper"], qlfs_lower=qlfs["lower"], qlfs_upper=qlfs["upper"],
        fit_seed_min=int(fit.seed.min()), fit_seed_max=int(fit.seed.max()),
    )
    table(
        "tab_arrears_fit",
        "Baseline arrears profile: model and \\ac{CCMR}",
        "\\ac{CCMR}: share of unsecured and credit-facility accounts by days in arrears, first "
        "quarter of 2017 \\cite{ncr_ccmr_2017}. Model: share of credit-active households (those "
        "owing traditional debt or arrears), \\ac{BNPL} disabled, averaged over the post-burn-in "
        f"ticks; seeds {num(fit.seed.min())}--{num(fit.seed.max())}. Fitted: the two bands that the "
        "income-shock probability and payment friction were chosen to match, so agreement there "
        "is by construction. The other bands were not targeted.",
        "lrrl",
        r"\textbf{Days in arrears} & \textbf{\ac{CCMR} (\%)} & \textbf{Model (\%)} & ",
        rows,
        size=r"\small",
    )


# ============================================================ 4.1 stacking
def tab_stacking(rq1: pd.DataFrame) -> None:
    rows = []
    n1, n6 = {}, {}
    sd_def = 0.0
    for n in range(1, 7):
        sub = {b: rq1[(rq1.n_platforms == n) & (rq1.beta == b)] for b in (0.0, 1.0)}
        cells = [str(n)]
        # grouped by outcome, so each pair compares beta = 0 with beta = 1 side by side
        cells += [pct(ms(holders_share(sub[b]))[0], 1) for b in (0.0, 1.0)]
        cells += [pct(ms(sub[b].ever_stacked_2plus_of_adopters)[0], 1) for b in (0.0, 1.0)]
        cells += [rm(ms(sub[b].bnpl_volume_cumulative)[0], 2) for b in (0.0, 1.0)]
        cells += [pct(ms(sub[b].default_rate_final)[0], 2) for b in (0.0, 1.0)]
        for b in (0.0, 1.0):
            d = sub[b]
            sd_def = max(sd_def, ms(d.default_rate_final)[1])
            N[f"volume_n{n}_beta{b:g}"] = ms(d.bnpl_volume_cumulative)[0]
            if n == 1:
                n1[b] = d
            if n == 6:
                n6[b] = d
            if n in (2, 4, 6):
                N[f"stack2_all_n{n}_beta{b:g}"] = ms(d.stacking_2plus_final)[0]
        rows.append(" & ".join(cells) + r" \\")
    d0, se0 = delta(n6[0.0], n1[0.0], "default_rate_final")
    d1, se1 = delta(n6[1.0], n1[1.0], "default_rate_final")
    N.update(n6_minus_n1_beta0=d0, n6_minus_n1_beta0_se=se0,
             n6_minus_n1_beta1=d1, n6_minus_n1_beta1_se=se1,
             default_n1_beta0=ms(n1[0.0].default_rate_final)[0])
    table(
        "tab_stacking",
        "Stacking, volume and default by number of platforms",
        "Seeds 20{,}000--20{,}019. Holders: share of households holding \\ac{BNPL} at the final "
        "tick that owe two or more platforms. Ever-holders: share of households that ever held "
        "\\ac{BNPL} that owed two or more platforms at some tick; the \\ac{CFPB} reports 32 to 33\\% "
        "of United States borrowers with loans at two or more firms in a year \\cite{cfpb2025bnpl}. "
        "Volume: cumulative post-burn-in \\ac{BNPL} lending. Replicate standard deviations of default "
        f"are at most {sd_def * 100:.2f} points. Default with six platforms less one: "
        f"{pm(d0, se0)} points at $\\beta = 0$ and {pm(d1, se1)} at $\\beta = 1$.",
        "c rr rr rr rr",
        r"& \multicolumn{2}{c}{\textbf{Holders (\%)}} & \multicolumn{2}{c}{\textbf{Ever-holders (\%)}} "
        r"& \multicolumn{2}{c}{\textbf{Volume (R m)}} & \multicolumn{2}{c}{\textbf{Default (\%)}} \\ "
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}\cmidrule(lr){6-7}\cmidrule(lr){8-9}"
        "\n\\textbf{Platforms} & $\\beta=0$ & $\\beta=1$ & $\\beta=0$ & $\\beta=1$ & $\\beta=0$ & $\\beta=1$ "
        "& $\\beta=0$ & $\\beta=1$",
        rows,
        size=r"\small",
        colsep="4pt",
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
    contrasts = []
    for b in betas:
        one = rq1[(rq1.n_platforms == 1) & (rq1.beta == b)]
        six = rq1[(rq1.n_platforms == 6) & (rq1.beta == b)]
        dd, se = delta(six, one, "default_rate_final")
        N[f"n6_minus_n1_beta{b:g}"], N[f"n6_minus_n1_beta{b:g}_se"] = dd, se
        contrasts.append(f"{pm(dd, se)}pp at $\\beta = {b:g}$")
        # the largest contrast with one platform, over two to six
        best = max(
            (delta(rq1[(rq1.n_platforms == n) & (rq1.beta == b)], one, "default_rate_final") + (n,)
             for n in range(2, 7)),
            key=lambda t: abs(t[0]) / t[1],
        )
        N[f"nmax_minus_n1_beta{b:g}"], N[f"nmax_minus_n1_beta{b:g}_se"], N[f"nmax_n_beta{b:g}"] = best
    table(
        "tab_stacking_full",
        "Platform count by peer-influence strength: the full grid",
        f"Seeds 20{{,}}000--20{{,}}019. 2+ platforms: share of all households owing two or more "
        f"platforms at the final tick. Replicate standard deviations are at most {sd_max * 100:.1f} "
        f"points for that share and {sd_def * 100:.2f} for default. Default with six platforms less "
        f"one: {', '.join(contrasts)}.",
        "c " + "r" * k + " " + "r" * k,
        f"& \\multicolumn{{{k}}}{{c}}{{2+ platforms (\\% of households)}} & \\multicolumn{{{k}}}{{c}}{{Default rate (\\%)}} \\\\ "
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
    d_arr0, se_arr0 = delta(b0, off, "trad_arrears_rate_mean")
    d_arr1, se_arr1 = delta(b1, off, "trad_arrears_rate_mean")
    r_int0, r_int0_se = ratio_change(b0, off, "trad_interest_total")
    r_int1, r_int1_se = ratio_change(b1, off, "trad_interest_total")

    def reading(pairs, what):
        """What a pair of (difference, se) supports, under the two-standard-error rule."""
        words = []
        for d, se in pairs:
            words.append("no detectable change" if not detectable(d, se) else ("rises" if d > 0 else "falls"))
        if words[0] == words[1]:
            text = words[0]
        else:
            text = f"{words[0]} at $\\beta = 0$, {words[1]} at $\\beta = 1$"
        ok = all(w == "rises" for w in words)
        return text if ok else f"{text}: the pattern is not reproduced on {what}"
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
        p1_interest_beta0_se=r_int0_se, p1_interest_beta1_se=r_int1_se,
        p1_arrears_reproduced=bool(all(detectable(d, e) and d > 0 for d, e in ((d_arr0, se_arr0), (d_arr1, se_arr1)))),
        p1_interest_reproduced=bool(all(detectable(d, e) and d > 0 for d, e in ((r_int0, r_int0_se), (r_int1, r_int1_se)))),
        p3_middle_peak=bool(peak in ("Q2", "Q3", "Q4") and second in ("Q2", "Q3", "Q4")),
        p3_peak=peak, p3_peak_value=dti[peak], p3_second=second, p3_second_value=dti[second],
        p3_mean_peak=peak_mean, p4_zero_savings_off=zs_off, p4_zero_savings_beta0=zs_b0,
        p4_target=0.36,
    )
    def verdict(pairs):
        """The direction each (difference, se) supports, under the two-standard-error rule."""
        words = ["no change" if not detectable(d, se) else ("rises" if d > 0 else "falls")
                 for d, se in pairs]
        return words[0].capitalize() if words[0] == words[1] else \
            f"{words[0].capitalize()} ($\\beta=0$); {words[1]} ($\\beta=1$)"

    def band(v):
        return "inside" if lo_vol <= v <= hi_vol else ("below" if v < lo_vol else "above")

    p3_reading = ("Reproduced" if N["p3_middle_peak"] else
                  f"Not reproduced: peak in {peak}, {second} second")
    rows = [
        group_row("Behavioural patterns", 4),
        f"1. Traditional arrears rise \\cite{{dehaan2024bnpl}} & Rise & {pmb(d_arr0, se_arr0)}; "
        f"{pmb(d_arr1, se_arr1)} pp & {verdict(((d_arr0, se_arr0), (d_arr1, se_arr1)))} \\\\",
        f"1. Traditional interest rises \\cite{{dehaan2024bnpl}} & Rise & "
        f"{pmb(r_int0, r_int0_se, 1)}; {pmb(r_int1, r_int1_se, 1)}\\% & "
        f"{verdict(((r_int0, r_int0_se), (r_int1, r_int1_se)))} \\\\",
        f"3. Debt-to-income peaks mid-distribution \\cite{{hamill2023creditcard}} & Peak in Q2--Q4 & "
        f"{peak} {dti[peak]:.2f}; {second} {dti[second]:.2f} & {p3_reading} \\\\",
        f"4. Households without savings \\cite{{transunion_cps_sa_2025}} & 36\\% expect to miss a payment & "
        f"{pct(zs_off, 1)}\\% & Same order \\\\",
        group_row("\\ac{BNPL} market", 4),
        f"Owing two or more providers \\cite{{cfpb2025bnpl}} & 32--33\\% of borrowers & "
        f"{pct(ev0, 1)}\\% of ever-holders & Close; different market \\\\",
        f"Annual volume per eligible household \\cite{{weaver2025iar}} & {rand(lo_vol)}--{rand(hi_vol)} & "
        f"{rand(N['vol_per_eligible_year'])} & {band(N['vol_per_eligible_year']).capitalize()} \\\\",
        f"Annual volume per ever-holder \\cite{{weaver2025iar}} & {rand(lo_vol)}--{rand(hi_vol)} & "
        f"{rand(N['vol_per_adopter_year'])} & {band(N['vol_per_adopter_year']).capitalize()} \\\\",
        f"Mean purchase \\cite{{weaver2025iar}} & {rand(target)} ($\\pm$35\\%) & {rand(mp0)} & "
        f"{'Inside' if lo_band <= mp0 <= hi_band else 'Below'}: {-gap0 * 100:.0f}\\% low \\\\",
    ]
    table(
        "tab_bnpl_on_checks",
        "Comparisons with external evidence",
        "No parameter was fitted to these quantities. Model values are from the $\\beta = 0$ arm of "
        "Table~\\ref{tab:baseline-arms}; Pattern~1 shows the change from the no-\\ac{BNPL} arm at "
        "$\\beta = 0$ and $\\beta = 1$, and Patterns 3 and 4 use the no-\\ac{BNPL} arm. Debt-to-income "
        "is total debt over total monthly income in each quintile. The volume band runs from the "
        "provider's volume per signed-up customer to its volume per active customer, in 2017 Rands; "
        "the purchase target divides its gross merchandise value by its transaction count. Pattern~2, "
        "the calibration target, is in Table~\\ref{tab:arrears-fit}.",
        "L{4.6cm}L{2.7cm}L{3.0cm}L{3.3cm}",
        r"\textbf{Comparison} & \textbf{Expected} & \textbf{Model} & \textbf{Result}",
        rows,
        size=r"\footnotesize",
        colsep="3pt",
    )


# ============================================================ 5 the scenario panel
def tab_scenarios(rq3s: pd.DataFrame) -> None:
    """One table for RQ3: the benchmark level and each arm's change from it, at both betas."""
    keys = [("bench", "Benchmark"), ("bureau", "Bureau visibility"), ("afford", "Screening"),
            ("both", "Both")]
    arms = {b: {k: arm(rq3s, f"rq3s_{k}_b{b}") for k, _ in keys} for b in (0.0, 1.0)}
    # (label, column, kind, scale, decimals): kind 'pp' is a difference in points, 'rel' a
    # relative change in per cent, 'abs' a difference in the column's own unit
    outcomes = [
        ("Default rate (\\%)", "default_rate_final", "pp", 100, 2),
        ("90+ day arrears (\\%)", "active_90_plus_mean", "pp", 100, 2),
        ("Refused applications", "trad_refused_gate", "abs", 1, 0),
        ("Traditional lending (R m)", "trad_granted_value", "abs", 1e-6, 2),
        ("\\ac{BNPL} holding (\\%)", "bnpl_adoption_final", "pp", 100, 2),
        ("\\ac{BNPL} volume (R m)", "bnpl_volume_cumulative", "rel", 1e-6, 2),
    ] + [(f"Default rate, {q} (\\%)", f"default_rate_final_{q}", "pp", 100, 2) for q in Q]  # noqa
    rows = []
    for b in (0.0, 1.0):
        rows.append(group_row("No peer influence ($\\beta = 0$)" if b == 0 else
                              "Peer influence ($\\beta = 1$)", 5))
        bench = arms[b]["bench"]
        for name, col, kind, scale, dd in outcomes:
            cells = [name, f"{ms(bench[col])[0] * scale:.{dd}f}"]
            for k, _ in keys[1:]:
                assert shares_seeds(arms[b][k], bench)
                if kind == "rel":
                    x, se = ratio_change(arms[b][k], bench, col)
                    cells.append(pmb(x, se, 1))
                else:
                    x, se = delta(arms[b][k], bench, col)
                    cells.append(pmb(x, se, dd, scale))
            rows.append(" & ".join(cells) + r" \\")
        for k, _ in keys[1:]:
            dd_, se = delta(arms[b][k], bench, "default_rate_final")
            dv, dv_se = ratio_change(arms[b][k], bench, "bnpl_volume_cumulative")
            da, sea = delta(arms[b][k], bench, "active_90_plus_mean")
            dl, dl_se = delta(arms[b][k], bench, "trad_granted_value")
            dr, dr_se = delta(arms[b][k], bench, "trad_refused_gate")
            dad, dad_se = delta(arms[b][k], bench, "bnpl_adoption_final")
            N[f"scen_{k}_beta{b:g}_volume_rel_se"] = dv_se
            N[f"scen_{k}_beta{b:g}_lending"] = ms(arms[b][k].trad_granted_value)[0]
            N[f"scen_{k}_beta{b:g}_lending_diff"], N[f"scen_{k}_beta{b:g}_lending_diff_se"] = dl, dl_se
            N[f"scen_{k}_beta{b:g}_refused_diff"], N[f"scen_{k}_beta{b:g}_refused_diff_se"] = dr, dr_se
            N[f"scen_{k}_beta{b:g}_adoption"] = ms(arms[b][k].bnpl_adoption_final)[0]
            N[f"scen_{k}_beta{b:g}_adoption_diff"], N[f"scen_{k}_beta{b:g}_adoption_diff_se"] = dad, dad_se
            N[f"scen_{k}_beta{b:g}_volume"] = ms(arms[b][k].bnpl_volume_cumulative)[0]
            N[f"scen_{k}_beta{b:g}_default"], N[f"scen_{k}_beta{b:g}_default_se"] = dd_, se
            N[f"scen_{k}_beta{b:g}_volume_rel"] = dv
            N[f"scen_{k}_beta{b:g}_90plus"], N[f"scen_{k}_beta{b:g}_90plus_se"] = da, sea
            N[f"scen_{k}_beta{b:g}_refused"] = ms(arms[b][k].trad_refused_gate)[0]
        for col, tag in (("default_rate_final", "default"), ("trad_refused_gate", "refused"),
                         ("trad_granted_value", "lending"), ("bnpl_adoption_final", "adoption"),
                         ("bnpl_volume_cumulative", "volume")):
            N[f"scen_bench_beta{b:g}_{tag}"] = ms(bench[col])[0]
    table(
        "tab_scenarios",
        "Bureau visibility and mandatory screening",
        f"One hundred replicates per arm, {SEEDS_S}. The first column is the benchmark's mean; the "
        "others are each arm's change from it, paired by seed, in the row's unit except for "
        "\\ac{BNPL} volume, whose change is in per cent. 90+ day arrears: share of credit-active "
        "households. Refused applications and lending: the traditional lender's. Holding: at the "
        "final tick. Quintiles are of per-capita income.",
        "L{3.5cm}R{1.9cm}R{2.4cm}R{2.3cm}R{2.3cm}",
        r"& & \multicolumn{3}{c}{\textbf{Change from benchmark}} \\ \cmidrule(lr){3-5}"
        "\n\\textbf{Outcome} & \\textbf{Benchmark} & \\textbf{Bureau visibility} & "
        "\\textbf{Screening} & \\textbf{Both}",
        rows,
        size=r"\footnotesize",
        colsep="4pt",
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
        e0 = delta(b0, off, f"default_rate_final_{q}")
        e1 = delta(b1, off, f"default_rate_final_{q}")
        cells = [
            q,
            pct(ms(off[f"default_rate_final_{q}"])[0], 2),
            pmb(*e0),
            pmb(*e1),
            pct(ms(shares[0])[0], 1),
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
        d, se = delta(b0, off, f"default_rate_final_{q}")
        N[f"injection_{q}_beta0"], N[f"injection_{q}_beta0_se"] = d, se
        d, se = delta(b1, off, f"default_rate_final_{q}")
        N[f"injection_{q}_beta1"], N[f"injection_{q}_beta1_se"] = d, se
    N["order_cap_bind_beta0"] = ms(b0.bnpl_order_cap_bind_rate)[0]
    N["order_cap_bind_beta1"] = ms(b1.bnpl_order_cap_bind_rate)[0]
    N["injection_quintiles_detectable_beta0"] = [
        q for q in Q if detectable(N[f"injection_{q}_beta0"], N[f"injection_{q}_beta0_se"])]
    N["injection_quintiles_detectable_beta1"] = [
        q for q in Q if detectable(N[f"injection_{q}_beta1"], N[f"injection_{q}_beta1_se"])]
    table(
        "tab_distribution",
        "Outcomes by income quintile",
        f"Per-capita income quintiles of {', '.join(sizes[:-1])} and {sizes[-1]} households; seeds "
        "10{,}000--10{,}019. Change: default with \\ac{BNPL} less default without. Holding: share "
        "holding \\ac{BNPL} at the final tick. Debt/income: the quintile's total debt over its total "
        "monthly income. Limit binds: share of the quintile's platform requests that a platform's "
        "limit for that household reduced or refused. Purchase: mean want-driven purchase, in 2017 "
        "Rands.",
        "c R{1.4cm} R{2.3cm} R{2.3cm} R{1.4cm} R{1.3cm} R{1.4cm} R{1.4cm}",
        r"& \textbf{Default (\%)} & \multicolumn{2}{c}{\textbf{Change in default (pp)}} & "
        r"\textbf{Holding (\%)} & \textbf{Debt/ income} & \textbf{Limit binds (\%)} & \textbf{Purchase (R)} \\ \cmidrule(lr){3-4}"
        "\n\\textbf{Quintile} & No \\ac{BNPL} & $\\beta=0$ & $\\beta=1$ & $\\beta=0$ & No \\ac{BNPL} & $\\beta=0$ & $\\beta=0$",
        rows,
        size=r"\footnotesize",
        colsep="3pt",
    )


# ============================================================ 4.2 access (numbers for the prose)
def tab_access(rq2: pd.DataFrame, rq2t: pd.DataFrame) -> None:
    from simulation.analysis import linear_departure

    rows = [group_row("Linear peer rule, Equation~\\ref{eq:peer}", 4)]
    rises = {}
    for b in sorted(rq2.beta.unique()):
        g = rq2[rq2.beta == b].groupby("bnpl_access_rate").default_rate_final.mean().sort_index()
        d = linear_departure(g.index, g.values)
        rises[b] = d["rise"]
        lo = rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 0.0)]
        hi = rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 1.0)]
        dd, se = delta(hi, lo, "default_rate_final")
        tag = " (control)" if b == 0 else ""
        # A straight line through a rise that is itself within noise has no meaning, so the
        # fit is reported only where the end-to-end rise is detectable.
        hold = rq2[rq2.beta == b].groupby("bnpl_access_rate").bnpl_adoption_final.mean().sort_index()
        hold_rise = float(hold.iloc[-1] - hold.iloc[0])
        N[f"access_holding_rise_beta{b:g}"] = hold_rise
        fit = f"{d['linear_r2']:.2f}" if detectable(dd, se) else "--"
        N[f"access_rise_beta{b:g}_detectable"] = bool(detectable(dd, se))
        N[f"access_maxdev_beta{b:g}"] = d["max_dev_frac"]
        rows.append(f"$\\beta = {b:g}${tag} & {hold_rise * 100:+.1f} & {pmb(dd, se)} & {fit} \\\\")
        N[f"access_rise_beta{b:g}"], N[f"access_rise_beta{b:g}_se"], N[f"access_r2_beta{b:g}"] = dd, se, d["linear_r2"]
    fitted = [b for b in rq2.beta.unique() if N[f"access_rise_beta{b:g}_detectable"]]
    N["access_fitted_betas"] = sorted(float(b) for b in fitted)
    N["access_r2_min"] = min((N[f"access_r2_beta{b:g}"] for b in fitted), default=float("nan"))
    N["access_maxdev_max"] = max((N[f"access_maxdev_beta{b:g}"] for b in fitted), default=float("nan"))

    rows.append(group_row("Threshold rule, $\\gamma = 0.3$, by threshold dispersion $\\sigma_\\theta$", 4))
    surf = rq2t[rq2t.label.str.startswith("rq2t_a")]
    ctrl = surf[surf.gamma == 0].groupby("bnpl_access_rate")[["default_rate_final", "bnpl_adoption_final"]].mean().sort_index()
    dc = linear_departure(ctrl.index, ctrl.default_rate_final.values)
    ac = linear_departure(ctrl.index, ctrl.bnpl_adoption_final.values)
    def ends(sub_df):
        lo = sub_df[sub_df.bnpl_access_rate == 0.0]
        hi = sub_df[sub_df.bnpl_access_rate == 1.0]
        return delta(hi, lo, "default_rate_final")

    def fit_cells(dd, se, d):
        return f"{d['linear_r2']:.2f}" if detectable(dd, se) else "--"

    ctrl_runs = surf[(surf.gamma == 0) & (surf.sigma_theta == surf.sigma_theta.min())]
    cd, cse = ends(ctrl_runs)
    N["thr_ctrl_default_rise_se"] = cse
    N["thr_ctrl_default_detectable"] = bool(detectable(cd, cse))
    rows.append(f"$\\gamma = 0$ (control) & {ac['rise'] * 100:+.1f} & {pmb(cd, cse)} & {fit_cells(cd, cse, dc)} \\\\")
    N["thr_ctrl_default_rise"], N["thr_ctrl_default_r2"] = dc["rise"], dc["linear_r2"]
    N["thr_ctrl_adoption_rise"] = ac["rise"]
    thr_r2, ad_rises, d_rises = [], [], []
    for s in sorted(surf.sigma_theta.unique()):
        sub = surf[(surf.gamma > 0) & (surf.sigma_theta == s)].groupby("bnpl_access_rate")[["default_rate_final", "bnpl_adoption_final"]].mean().sort_index()
        d = linear_departure(sub.index, sub.default_rate_final.values)
        a = linear_departure(sub.index, sub.bnpl_adoption_final.values)
        dd, se = ends(surf[(surf.gamma > 0) & (surf.sigma_theta == s)])
        N[f"thr_default_rise_s{s:g}"], N[f"thr_default_rise_s{s:g}_se"] = dd, se
        N[f"thr_adoption_rise_s{s:g}"] = a["rise"]
        N[f"thr_adoption_r2_s{s:g}"] = a["linear_r2"]
        N[f"thr_adoption_maxdev_s{s:g}"] = a["max_dev_frac"]
        if detectable(dd, se):
            thr_r2.append(d["linear_r2"])
        ad_rises.append(a["rise"]); d_rises.append(d["rise"])
        rows.append(f"$\\sigma_\\theta = {s:g}$ & {a['rise'] * 100:+.1f} & {pmb(dd, se)} & {fit_cells(dd, se, d)} \\\\")
    N.update(thr_default_r2_min=min(thr_r2, default=float("nan")), thr_adoption_rise_max=max(ad_rises),
             thr_adoption_rise_min=min(ad_rises),
             thr_adoption_r2_min=min(N[f"thr_adoption_r2_s{s:g}"] for s in surf.sigma_theta.unique()),
             thr_default_rise_min=min(d_rises), thr_default_rise_max=max(d_rises),
             thr_default_n_detectable=len(thr_r2))
    mu = rq2t[rq2t.label.str.startswith("rq2t_mu")]
    mus = {}
    for m, sub in mu.groupby("mu_theta"):
        mus[m] = (ms(sub.bnpl_adoption_final)[0], ms(sub.default_rate_final)[0])
    N["mu_adoption_lo"], N["mu_default_lo"] = mus[max(mus)]
    N["mu_adoption_hi"], N["mu_default_hi"] = mus[min(mus)]
    N["mu_default_diff"], N["mu_default_diff_se"] = delta(
        mu[mu.mu_theta == max(mus)], mu[mu.mu_theta == min(mus)], "default_rate_final")
    table(
        "tab_access",
        "Holding and default from zero to full \\ac{BNPL} access",
        "Each row compares full access (every banked household eligible) with zero access, over "
        "seven access levels; seeds 30{,}000--30{,}019 for the linear rule and 60{,}000--60{,}019 "
        "for the threshold rule. Holding: change in the share holding \\ac{BNPL} at the final tick. "
        "$R^2$: fit of a straight line to default at the seven access levels, given only where the "
        "change in default is detectable.",
        "L{4.4cm}rrr",
        r"\textbf{Arm} & \textbf{Holding (pp)} & \textbf{Default (pp)} & \textbf{$R^2$}",
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
        dd, se = delta(d, a(ref_label), "default_rate_final")
        N[f"{label}_diff"], N[f"{label}_diff_se"] = dd, se
        mark = "" if shares_seeds(d, a(ref_label)) else "^\\ddagger"
        return f"{name} & {cell(d.default_rate_final, 2)} & {pm(dd, se)[:-1]}{mark}$ \\\\"

    rules = [("shortfall", "exact shortfall"), ("shortfall_125", "shortfall $+25\\%$"),
             ("shortfall_plus_committed", "shortfall $+$ one tick of committed spending")]
    rows = [group_row("Borrowing-amount rule (Submodel 4), \\ac{BNPL} share of a shortfall capped", 3)]
    rows.append(row(rules[0][1], "rob_amount_shortfall"))
    for key, name in rules[1:]:
        rows.append(row(name, f"rob_amount_{key}", "rob_amount_shortfall"))
    rows.append(group_row("The same rules with the cap removed (paired with the row above by seed)", 3))
    for key, name in rules:
        rows.append(row(name + ", uncapped", f"rob_amount_{key}_uncapped", f"rob_amount_{key}", paired=True))
    rows.append(group_row("Default threshold $k$ (Submodel 7)", 3))
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
    dd, se = delta(a("rob_k4"), a("rob_k7"), "default_rate_final")
    N["rob_k4_minus_k7"], N["rob_k4_minus_k7_se"] = dd, se
    for key, _ in rules:
        du, su = paired_diff(a(f"rob_amount_{key}_uncapped"), a(f"rob_amount_{key}"), "default_rate_final")
        N[f"rob_amount_{key}_uncapped_diff"], N[f"rob_amount_{key}_uncapped_diff_se"] = du, su
    table(
        "tab_robustness",
        "Sensitivity of the default rate: principal arms",
        "Default rate at $\\beta = 1$. Each group has its own reference arm and seed block "
        "(50{,}000, 54{,}000, 57{,}000 and 59{,}000), so references differ by seed noise. "
        "Difference: arm less its group's reference. $\\dagger$: arm less the same rule with the "
        "cap. Remaining arms: Table~\\ref{tab:robustness-appendix}.",
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
             row("persistent until re-employment (default rule, seeds 50{,}000--)", "rob_amount_shortfall"),
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
        "Default rate at $\\beta = 1$, laid out as Table~\\ref{tab:robustness}; seed blocks "
        "53{,}000 (activation), 55{,}000 (population), 51{,}000 (minimum-payer share), 52{,}000 "
        "(minimum payment), 56{,}000 (limit) and 58{,}000 (single-tick shock, against the "
        "exact-shortfall reference on 50{,}000). $\\ddagger$: unpaired, because seeds or population "
        "size differ. Under the single-tick shock the baseline 90+ share stays between 7.3\\% and "
        "7.6\\% at every shock probability on the calibration grid, about half the \\ac{CCMR} target.",
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
        "Sobol indices for the population default rate and \\ac{BNPL} holding",
        f"First-order ($S_1$) and total-order ($S_T$) indices with 95\\% bootstrap half-widths; "
        f"Saltelli design, $N = {data['n_base_samples']}$ base samples, {num(N['sobol_runs'])} runs, "
        f"\\ac{{BNPL}} enabled. The indices apportion the variance of the \\emph{{level}} of each outcome "
        f"across the ranges shown; they do not decompose the \\ac{{BNPL}} effect. Values outside "
        f"zero to one are bootstrap noise.",
        "L{4.0cm}c rr rr",
        r"& & \multicolumn{2}{c}{Default rate} & \multicolumn{2}{c}{Holding} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-6}"
        "\n\\textbf{Parameter} & \\textbf{Range} & \\textbf{$S_1$} & \\textbf{$S_T$} & \\textbf{$S_1$} & \\textbf{$S_T$}",
        rows,
        size=r"\footnotesize",
    )


# ============================================================ C: cooling-off and cap
def lever_table(rq3: pd.DataFrame, name: str, caption: str, arms: list[tuple[str, str]], note_extra: str,
                prefix: str = "rq3", bench_key: str = "kcool0", write: bool = True) -> None:
    rows = []
    sd_adopt = 0.0
    paired_any, unpaired_any = False, False
    for key, label in arms:
        cells = [label]
        for b in (0.0, 1.0):
            d = arm(rq3, f"{prefix}_{key}_b{b}")
            bench = arm(rq3, f"{prefix}_{bench_key}_b{b}")
            dv, dv_se = ratio_change(d, bench, "bnpl_volume_cumulative")
            dd, se = delta(d, bench, "default_rate_final")
            dl, dl_se = delta(d, bench, "trad_granted_value")
            sd_adopt = max(sd_adopt, ms(d.bnpl_adoption_final)[1])
            if key != bench_key:
                paired_any |= shares_seeds(d, bench)
                unpaired_any |= not shares_seeds(d, bench)
            cells += [cell(d.default_rate_final, 2), pm(dd, se) if key != bench_key else "--",
                      pct(ms(d.bnpl_adoption_final)[0], 1), f"{dv * 100:+.1f}" if key != bench_key else "--",
                      rm(ms(d.trad_granted_value)[0])]
            N[f"lever_{key}_beta{b:g}_default"] = ms(d.default_rate_final)[0]
            N[f"lever_{key}_beta{b:g}_diff"], N[f"lever_{key}_beta{b:g}_diff_se"] = dd, se
            N[f"lever_{key}_beta{b:g}_volume_rel"] = dv
            N[f"lever_{key}_beta{b:g}_volume_rel_se"] = dv_se
            N[f"lever_{key}_beta{b:g}_adoption"] = ms(d.bnpl_adoption_final)[0]
            N[f"lever_{key}_beta{b:g}_lending"] = ms(d.trad_granted_value)[0]
            N[f"lever_{key}_beta{b:g}_lending_diff"], N[f"lever_{key}_beta{b:g}_lending_diff_se"] = dl, dl_se
        rows.append(" & ".join(cells) + r" \\")
    if paired_any and not unpaired_any:
        se_text = "paired by seed"
    elif unpaired_any and not paired_any:
        se_text = "unpaired, because the arms and the benchmark use different seed blocks"
    else:
        raise AssertionError("a lever table must not mix paired and unpaired differences")
    if not write:
        return
    table(
        name,
        caption,
        f"$\\Delta$: default less the benchmark's, {se_text}. Hold.: share holding \\ac{{BNPL}} at "
        f"the final tick (\\%). Vol.: change in cumulative post-burn-in \\ac{{BNPL}} volume (\\%). "
        f"Trad.: new traditional lending (R m). {note_extra}",
        "L{1.9cm} rrrrr rrrrr",
        r"& \multicolumn{5}{c}{$\beta = 0$} & \multicolumn{5}{c}{$\beta = 1$} \\ \cmidrule(lr){2-6}\cmidrule(lr){7-11}"
        "\n\\textbf{Arm} & \\textbf{Default} & \\textbf{$\\Delta$ (pp)} & \\textbf{Hold.} & \\textbf{Vol.} & \\textbf{Trad.} "
        "& \\textbf{Default} & \\textbf{$\\Delta$ (pp)} & \\textbf{Hold.} & \\textbf{Vol.} & \\textbf{Trad.}",
        rows,
        size=r"\scriptsize",
        colsep="1.5pt",
    )


def tab_levers(rq3: pd.DataFrame, rq3s: pd.DataFrame) -> None:
    # The switches are tabulated in tab_scenarios; this records their numbers only.
    lever_table(
        rq3s, "tab_switches", "",
        [("bench", "benchmark"), ("bureau", "bureau visibility"), ("afford", "screening"),
         ("both", "both switches")],
        "", prefix="rq3s", bench_key="bench", write=False,
    )
    lever_table(
        rq3, "tab_cooloff", "The cooling-off window",
        [("kcool0", "benchmark")] + [(f"kcool{k}", f"{k} tick{'s' if k > 1 else ''} ({k * 14} days)") for k in (1, 2, 3, 4)],
        "Seeds 40{,}000--40{,}019. The window blocks want-driven \\ac{BNPL} purchases for "
        "$k^{\\text{cool}}$ ticks after one; borrowing for a shortfall is not blocked.",
    )
    lever_table(
        rq3, "tab_cap", "The cap on platforms owed (hypothetical)",
        [("kcool0", "benchmark")] + [(f"cap{c}", f"cap of {c}") for c in (1, 2, 3)],
        "Seeds 43{,}000--43{,}019 for the caps, 40{,}000--40{,}019 for the benchmark. A household "
        "owing the stated number of platforms is refused every new agreement until a balance clears "
        "(Appendix~\\ref{app:levers}).",
    )


# ============================================================ main
# Effect-robustness suite: (setting, display name, off-arm setting). The off arm is the
# setting's own where the setting changes the BNPL-free model, else the reference off arm.
EFFECT_ROWS = [
    ("Reference", [("ref", "reference settings", "ref")]),
    ("Purchase size (Submodel 4)", [
        ("kappa0.07", "$\\kappa = 0.07$ (half)", "ref"),
        ("kappa0.28", "$\\kappa = 0.28$ (double)", "ref"),
        ("base_income", "sized on income", "ref"),
    ]),
    ("Borrowing amount on a shortfall (Submodel 4)", [
        ("amount125", "shortfall $+25\\%$", "amount125"),
        ("amountcommitted", "shortfall $+$ committed spending", "amountcommitted"),
        ("uncapped", "exact shortfall, no cap", "ref"),
        ("amount125_uncapped", "shortfall $+25\\%$, no cap", "amount125"),
        ("amountcommitted_uncapped", "shortfall $+$ committed, no cap", "amountcommitted"),
    ]),
    ("Routing and the shortfall path (Submodels 5, 7 and 13)", [
        ("routing_loyal", "loyal routing", "ref"),
        ("no_shortfall_bnpl", "no \\ac{BNPL} for shortfalls", "ref"),
        ("committed_funded", "credit pays food and rent first", "committed_funded"),
    ]),
    ("Other assumptions (Submodels 1, 6, 7 and 12)", [
        ("shock_single_tick", "single-tick income shock", "shock_single_tick"),
        ("k4", "default after 56 days", "k4"),
        ("minpay0.025", "minimum payment 2.5\\% a month", "minpay0.025"),
        ("minpay0.1", "minimum payment 10\\% a month", "minpay0.1"),
        ("m0.2", "minimum-payer share 0.20", "m0.2"),
        ("m0.4", "minimum-payer share 0.40", "m0.4"),
        ("limit0.25", "platform limit $\\lambda = 0.25$", "ref"),
        ("limit1.0", "platform limit $\\lambda = 1.0$", "ref"),
    ]),
]


def tab_effect(eff: pd.DataFrame) -> None:
    def a(label: str) -> pd.DataFrame:
        return arm(eff, label)

    rows, effects0, effects1 = [], {}, {}
    for group, items in EFFECT_ROWS:
        rows.append(group_row(group, 5))
        for key, name, off_key in items:
            off = a(f"eff_{off_key}_off")
            d0, s0 = paired_diff(a(f"eff_{key}_b0.0"), off, "default_rate_final")
            d1, s1 = paired_diff(a(f"eff_{key}_b1.0"), off, "default_rate_final")
            effects0[key], effects1[key] = (d0, s0), (d1, s1)
            # Three decimals where two would round a 1.1-SE effect to an apparent 2 SE.
            dd = 3 if key == "shock_single_tick" else 2
            purchase = ms(a(f"eff_{key}_b1.0").bnpl_purchase_mean_realised)[0]
            N[f"eff_{key}_purchase_b1"] = purchase
            N[f"eff_{key}_purchase_b0"] = ms(a(f"eff_{key}_b0.0").bnpl_purchase_mean_realised)[0]
            name_ = f"\\textbf{{{name}}}" if key == "ref" else name
            rows.append(f"{name_} & {pct(ms(off.default_rate_final)[0])} & {num(purchase)} & "
                        f"{pmb(d0, s0, dd)} & {pmb(d1, s1, dd)} \\\\")
    rows.append(group_row("Want-driven path switched off ($q_{\\text{base}} = 0$, $\\beta = 0$)", 5))
    ref_off = a("eff_ref_off")
    dw, sw = paired_diff(a("eff_want_off_b0.0"), ref_off, "default_rate_final")
    rows.append(f"\\ac{{BNPL}} for shortfalls only & {pct(ms(ref_off.default_rate_final)[0])} & -- & {pmb(dw, sw)} & -- \\\\")

    for k, (d, s) in effects0.items():
        N[f"eff_{k}_b0"], N[f"eff_{k}_b0_se"] = d, s
    for k, (d, s) in effects1.items():
        N[f"eff_{k}_b1"], N[f"eff_{k}_b1_se"] = d, s
    N["eff_want_off_b0"], N["eff_want_off_b0_se"] = dw, sw
    N["eff_ref_off_default"] = ms(ref_off.default_rate_final)[0]
    b0 = [d for d, _ in effects0.values()]
    b1 = [d for d, _ in effects1.values()]
    N.update(eff_b0_min=min(b0), eff_b0_max=max(b0), eff_b1_min=min(b1), eff_b1_max=max(b1))
    N["eff_b0_detectable"] = sorted(k for k, (d, s) in effects0.items() if detectable(d, s))
    N["eff_b1_detectable"] = sorted(k for k, (d, s) in effects1.items() if detectable(d, s))
    N["eff_b0_n"], N["eff_b1_n"] = len(effects0), len(effects1)
    N["eff_b0_negative_detectable"] = sorted(k for k, (d, s) in effects0.items() if detectable(d, s) and d < 0)
    N["eff_b1_negative_detectable"] = sorted(k for k, (d, s) in effects1.items() if detectable(d, s) and d < 0)
    N["eff_want_off_detectable"] = bool(detectable(dw, sw))
    table(
        "tab_effect",
        "The \\ac{BNPL} effect on default under alternative assumptions",
        "Effect: default with \\ac{BNPL} less default without, paired by seed over one block "
        "(70{,}000--70{,}019). No \\ac{BNPL}: the setting's default rate without \\ac{BNPL}. "
        "Purchase: mean want-driven purchase at $\\beta = 1$, in 2017 Rands, against a "
        "provider-based figure of R992 (Table~\\ref{tab:bnpl-on-checks}).",
        "L{4.4cm}R{1.5cm}R{1.5cm}rr",
        r"& & & \multicolumn{2}{c}{\textbf{Effect (pp)}} \\ \cmidrule(lr){4-5}"
        "\n\\textbf{Setting} & \\textbf{No \\ac{BNPL} (\\%)} & \\textbf{Purchase (R)} & "
        "$\\beta=0$ & $\\beta=1$",
        rows,
        size=r"\footnotesize",
    )


def derived_numbers(rq0, rq2, rq2t, rq3, eff) -> None:
    """Quantities the prose quotes that no single table cell holds."""
    # --- the effect of BNPL at beta = 0, estimated on four independent seed blocks -------
    surf = rq2t[rq2t.label.str.startswith("rq2t_a")]
    ctrl = surf[(surf.gamma == 0) & (surf.sigma_theta == surf.sigma_theta.min())]
    blocks = {
        "rq0": delta(arm(rq0, "bnpl_on_beta0"), arm(rq0, "baseline_no_bnpl"), "default_rate_final"),
        "access": delta(rq2[(rq2.beta == 0) & (rq2.bnpl_access_rate == 1.0)],
                        rq2[(rq2.beta == 0) & (rq2.bnpl_access_rate == 0.0)], "default_rate_final"),
        "threshold_control": delta(ctrl[ctrl.bnpl_access_rate == 1.0], ctrl[ctrl.bnpl_access_rate == 0.0],
                                   "default_rate_final"),
        "effect": paired_diff(arm(eff, "eff_ref_b0.0"), arm(eff, "eff_ref_off"), "default_rate_final"),
    }
    w = {k: 1.0 / se**2 for k, (_, se) in blocks.items()}
    pooled = sum(w[k] * blocks[k][0] for k in blocks) / sum(w.values())
    pooled_se = (1.0 / sum(w.values())) ** 0.5
    for k, (d, se) in blocks.items():
        N[f"beta0_effect_{k}"], N[f"beta0_effect_{k}_se"] = d, se
    N["beta0_effect_min"] = min(d for d, _ in blocks.values())
    N["beta0_effect_max"] = max(d for d, _ in blocks.values())
    N["beta0_effect_n_detectable"] = sum(detectable(d, se) for d, se in blocks.values())
    N["beta0_effect_pooled"], N["beta0_effect_pooled_se"] = pooled, pooled_se
    N["beta0_effect_pooled_detectable"] = bool(detectable(pooled, pooled_se))
    # the same at beta = 1, three blocks
    blocks1 = {
        "rq0": delta(arm(rq0, "bnpl_on_beta1"), arm(rq0, "baseline_no_bnpl"), "default_rate_final"),
        "access": delta(rq2[(rq2.beta == 1) & (rq2.bnpl_access_rate == 1.0)],
                        rq2[(rq2.beta == 1) & (rq2.bnpl_access_rate == 0.0)], "default_rate_final"),
        "effect": paired_diff(arm(eff, "eff_ref_b1.0"), arm(eff, "eff_ref_off"), "default_rate_final"),
    }
    w1 = {k: 1.0 / se**2 for k, (_, se) in blocks1.items()}
    N["beta1_effect_pooled"] = sum(w1[k] * blocks1[k][0] for k in blocks1) / sum(w1.values())
    N["beta1_effect_pooled_se"] = (1.0 / sum(w1.values())) ** 0.5
    N["beta1_effect_min"] = min(d for d, _ in blocks1.values())
    N["beta1_effect_max"] = max(d for d, _ in blocks1.values())

    # --- the access response step by step: is any single step a jump? -------------------
    levels = sorted(rq2.bnpl_access_rate.unique())
    for b in sorted(rq2.beta.unique()):
        steps = []
        for lo, hi in zip(levels[:-1], levels[1:]):
            d, se = delta(rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == hi)],
                          rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == lo)], "default_rate_final")
            steps.append((d, se, lo, hi))
        big = max(steps, key=lambda t: t[0])
        N[f"access_max_step_beta{b:g}"], N[f"access_max_step_beta{b:g}_se"] = big[0], big[1]
        N[f"access_max_step_beta{b:g}_from"], N[f"access_max_step_beta{b:g}_to"] = big[2], big[3]
        N[f"access_steps_detectable_beta{b:g}"] = sum(detectable(d, se) for d, se, _, _ in steps)
    N["access_max_step_all"] = max(N[f"access_max_step_beta{b:g}"] for b in rq2.beta.unique())

    # --- volume and saving beside the effect ---------------------------------------------
    off, b0, b1 = (arm(rq0, l) for l in ("baseline_no_bnpl", "bnpl_on_beta0", "bnpl_on_beta1"))
    N["volume_ratio_beta1_over_beta0"] = ms(b1.bnpl_volume_cumulative)[0] / ms(b0.bnpl_volume_cumulative)[0]
    for name, d_ in (("beta0", b0), ("beta1", b1)):
        x, se = delta(d_, off, "zero_savings_rate_mean")
        N[f"zero_savings_change_{name}"], N[f"zero_savings_change_{name}_se"] = x, se
        x, se = delta(d_, off, "trad_granted_value")
        N[f"lending_change_{name}"], N[f"lending_change_{name}_se"] = x, se
        x, se = delta(d_, off, "trad_refused_gate")
        N[f"refused_change_{name}"], N[f"refused_change_{name}_se"] = x, se
        x, se = delta(d_, off, "active_90_plus_mean")
        N[f"arrears90_change_{name}"], N[f"arrears90_change_{name}_se"] = x, se
    N["zero_savings_beta1"] = ms(b1.zero_savings_rate_mean)[0]
    # Why lending falls at beta=0 but not at beta=1: applications against the mean loan.
    for name, d_ in (("beta0", b0), ("beta1", b1)):
        x, se = delta(d_, off, "trad_applications")
        N[f"applications_change_{name}"], N[f"applications_change_{name}_se"] = x, se
        x, se = delta(d_, off, lambda d: d.trad_granted_value / d.trad_granted.clip(lower=1))
        N[f"mean_grant_change_{name}"], N[f"mean_grant_change_{name}_se"] = x, se
    # Stacking under the two routing rules, on the effect suite's seeds (added 2026-10-06).
    for rule, key in (("random", "ref"), ("loyal", "routing_loyal")):
        for b in (0.0, 1.0):
            d_ = arm(eff, f"eff_{key}_b{b}")
            N[f"stack_holders_{rule}_beta{b:g}"] = ms(holders_share(d_))[0]
            N[f"stack_ever_{rule}_beta{b:g}"] = ms(d_.ever_stacked_2plus_of_adopters)[0]
            N[f"volume_{rule}_beta{b:g}"] = ms(d_.bnpl_volume_cumulative)[0]
    for b in (0.0, 1.0):
        x, se = paired_diff(arm(eff, f"eff_routing_loyal_b{b}"), arm(eff, f"eff_ref_b{b}"), "default_rate_final")
        N[f"routing_default_diff_beta{b:g}"], N[f"routing_default_diff_beta{b:g}_se"] = x, se
    N["volume_want_off"] = ms(arm(eff, "eff_want_off_b0.0").bnpl_volume_cumulative)[0]
    N["volume_eff_ref_b0"] = ms(arm(eff, "eff_ref_b0.0").bnpl_volume_cumulative)[0]
    N["lending_eff_ref_b0"] = ms(arm(eff, "eff_ref_b0.0").trad_granted_value)[0]

    # --- how often holders borrow: want-driven purchases per household that ever held BNPL --
    for name, d_ in (("beta0", b0), ("beta1", b1)):
        N[f"want_per_everholder_{name}"] = ms(d_.bnpl_want_purchases / (d_.ever_adopted * d_.n_agents))[0]
    # --- volume under the threshold rule against its control, at full access -------------
    full = surf[surf.bnpl_access_rate == 1.0]
    ctrl_vol = full[full.gamma == 0].bnpl_volume_cumulative.mean()
    thr_vol = full[full.gamma > 0].groupby("sigma_theta").bnpl_volume_cumulative.mean() / ctrl_vol
    N["thr_volume_ratio_min"], N["thr_volume_ratio_max"] = float(thr_vol.min()), float(thr_vol.max())
    lin_full = rq2[rq2.bnpl_access_rate == 1.0].groupby("beta").bnpl_volume_cumulative.mean()
    N["access_volume_ratio_beta0.5"] = float(lin_full[0.5] / lin_full[0.0])

    # --- does the effect differ between quintiles? the largest against the smallest ------
    for name, d_ in (("beta0", b0), ("beta1", b1)):
        eff_q = {q: (d_.set_index("seed")[f"default_rate_final_{q}"]
                     - off.set_index("seed")[f"default_rate_final_{q}"]) for q in Q}
        hi_q = max(Q, key=lambda q: eff_q[q].mean())
        lo_q = min(Q, key=lambda q: eff_q[q].mean())
        gap = eff_q[hi_q] - eff_q[lo_q]
        N[f"injection_gap_{name}_hi"], N[f"injection_gap_{name}_lo"] = hi_q, lo_q
        N[f"injection_gap_{name}"] = float(gap.mean())
        N[f"injection_gap_{name}_se"] = float(gap.std(ddof=1) / len(gap) ** 0.5)

    # --- the smallest change each scenario comparison could have detected ----------------
    ses = [N[f"lever_{k}_beta{b:g}_diff_se"] for k in ("bureau", "afford", "both") for b in (0.0, 1.0)]
    N["switch_se_max"] = max(ses)
    N["switch_detectable_min"] = 2 * max(ses)
    N["switch_n_detectable"] = sum(
        detectable(N[f"lever_{k}_beta{b:g}_diff"], N[f"lever_{k}_beta{b:g}_diff_se"])
        for k in ("bureau", "afford", "both") for b in (0.0, 1.0))
    # --- what the prose of Section 5 quotes beyond the two tables ------------------------
    for b in (0.0, 1.0):
        arms = {k: arm(rq3, f"rq3s_{k}_b{b}") for k in ("bench", "bureau", "afford", "both")}
        for k in ("bureau", "afford", "both"):
            for col, tag in (("active_90_plus_mean", "90plus"), ("trad_refused_gate", "refused"),
                             ("trad_granted_value", "lending"), ("bnpl_adoption_final", "adoption")):
                N[f"switch_{k}_beta{b:g}_{tag}_diff"], N[f"switch_{k}_beta{b:g}_{tag}_diff_se"] = delta(arms[k], arms["bench"], col)
            for q in Q:
                N[f"switch_{k}_beta{b:g}_default_{q}_diff"], N[f"switch_{k}_beta{b:g}_default_{q}_diff_se"] = \
                    delta(arms[k], arms["bench"], f"default_rate_final_{q}")
        for a, c in (("both", "afford"), ("both", "bureau"), ("bureau", "afford")):
            N[f"switch_{a}_less_{c}_beta{b:g}"], N[f"switch_{a}_less_{c}_beta{b:g}_se"] = delta(arms[a], arms[c], "default_rate_final")
            N[f"switch_{a}_less_{c}_beta{b:g}_refused"], _ = delta(arms[a], arms[c], "trad_refused_gate")
            N[f"switch_{a}_less_{c}_beta{b:g}_lending"], _ = delta(arms[a], arms[c], "trad_granted_value")
        # peer influence and the switches: the beta = 1 less beta = 0 gap in each arm
    for k in ("bench", "bureau", "afford", "both"):
        N[f"switch_{k}_beta_gap"], N[f"switch_{k}_beta_gap_se"] = delta(
            arm(rq3, f"rq3s_{k}_b1.0"), arm(rq3, f"rq3s_{k}_b0.0"), "default_rate_final")
    for k in ("bureau", "afford", "both"):
        x = (arm(rq3, f"rq3s_{k}_b1.0").set_index("seed").default_rate_final - arm(rq3, "rq3s_bench_b1.0").set_index("seed").default_rate_final) \
            - (arm(rq3, f"rq3s_{k}_b0.0").set_index("seed").default_rate_final - arm(rq3, "rq3s_bench_b0.0").set_index("seed").default_rate_final)
        N[f"switch_{k}_interaction"], N[f"switch_{k}_interaction_se"] = float(x.mean()), float(x.std(ddof=1) / len(x) ** 0.5)


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (load(n) for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    eff = load("effect")
    rq3s = load("rq3s")
    for df in (rq0, rq1, rq2, rq2t, rq3, rob, eff):
        assert df.groupby("label").seed.nunique().eq(20).all(), "every arm needs 20 unique seeds"
    assert rq3s.groupby("label").seed.nunique().eq(100).all(), "every scenario arm needs 100 unique seeds"
    tab_arrears_fit()
    tab_baseline_arms(rq0)
    tab_stacking(rq1)
    tab_bnpl_on_checks(rq0)
    tab_scenarios(rq3s)
    tab_distribution(rq0)
    tab_access(rq2, rq2t)
    tab_robustness(rob)
    tab_sobol()
    tab_levers(rq3, rq3s)
    tab_effect(eff)
    derived_numbers(rq0, rq2, rq2t, rq3s, eff)
    out = {k: (round(float(v), 6) if isinstance(v, (float, np.floating)) else
               (int(v) if isinstance(v, np.integer) else v)) for k, v in N.items()}
    (SUMMARY / "results_numbers.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"wrote results/summary/results_numbers.json ({len(out)} numbers)")


if __name__ == "__main__":
    main()
