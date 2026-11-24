"""The results figures for Sections 4 and 5 and Appendix C, from results/raw.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_figures.py

Writes to thesis/figures as vector PDF (plus PNG for preview), drawn at the compiled text
width so nothing is rescaled:
  fig_baseline_arrears   baseline arrears profile against the CCMR bands, fitted bands marked
  fig_stacking           2+ platform shares (final tick; ever, the CFPB analogue) and default
  fig_access_default     default against access: linear coupling, and thresholds (adoption, default)
  fig_scenarios          the three body scenarios at both betas, default and volume
  fig_tornado            each behavioural sensitivity arm's change from its reference, with 95%
                         intervals (the 56-day default threshold is tabulated, not drawn)
  fig_scenarios_appendix every lever at both betas, the cap marked hypothetical

Palette: categorical slots 1 and 8 of the validated default (blue, red) plus black for the
control arm; ordered series use the blue ordinal ramp. Error bars are 95% confidence intervals
of the replicate mean (t with n - 1 degrees of freedom); every difference the prose quotes
comes from the tables.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FormatStrFormatter, MaxNLocator, MultipleLocator
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from results_common import (  # noqa: E402
    DKBLUE, ERR, INK, INK2, MARKERS, RAMP, RC, RED, SCENARIOS, SRC, SURF, TW, arm, delta, dress, load, minus,
    param, save,
)
from simulation.config import load_ccmr_bands  # noqa: E402

#: Milestone 2 (#98): the peer-influence arm beside beta = 0. Table text prints it as 0.3.
from simulation.experiments import BETA_PEER as BP  # noqa: E402
assert BP == 0.30, "table text prints the peer arm as beta = 0.3; update it with BETA_PEER"


plt.rcParams.update(RC)
CTRL_LBL = r"$\beta\,=\,0$ (control)"
BETA1_LBL = r"$\beta\,=\,0.3$"


def half_ci(x: pd.Series) -> float:
    """Half-width of the 95% confidence interval of the mean of x."""
    n = x.count()
    return float(stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n))


def agg(df: pd.DataFrame, by: str, col: str) -> pd.DataFrame:
    """Mean and 95% CI half-width per group."""
    g = df.groupby(by)[col]
    return pd.DataFrame({"mean": g.mean(), "ci": g.apply(half_ci)}).sort_index()


# =================================================================== helpers
def one_decimal(ax, axis: str = "y", nbins: int = 5) -> None:
    """Default-rate axes: steps of 0.1, 0.2 or 0.5 points, printed to one decimal in every figure."""
    a = ax.yaxis if axis == "y" else ax.xaxis
    a.set_major_locator(MaxNLocator(nbins, steps=[1, 2, 5, 10]))
    a.set_major_formatter(FormatStrFormatter("%.1f"))


def legend_below(fig, handles, labels, ncol: int | None = None, y: float = 0.0, **kw) -> None:
    """One figure-level legend row under the panels, shared by all of them."""
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, y),
               ncol=ncol or len(handles), **kw)


# =================================================================== baseline arrears
def fig_baseline_arrears(rq0: pd.DataFrame) -> None:
    off = arm(rq0, "baseline_no_bnpl")
    pct = load_ccmr_bands()
    bands = ["current", "d30", "d31_60", "d61_90", "d91_120", "d120_plus"]
    labels = ["Current", "1$–$30 d", "31$–$60 d", "61$–$90 d", "91$–$120 d", "120+ d"]
    # The 1-30 day band is fitted on its own; 91-120 and 120+ are fitted only as their sum (90+).
    fitted = {"d30", "d91_120", "d120_plus"}
    status = {"d30": "fitted", "d91_120": "", "d120_plus": ""}
    model = np.array([off[f"active_{b}_mean"].mean() * 100 for b in bands])
    sd = np.array([half_ci(off[f"active_{b}_mean"]) * 100 for b in bands])
    target = np.array([pct[b] for b in bands])

    fig, ax = plt.subplots(figsize=(TW, 2.9))
    x = np.arange(len(bands))
    w = 0.38
    # The external benchmark is hatched, as in the data figures.
    ax.bar(x - w / 2 - 0.01, target, w, color=SURF, edgecolor=INK, hatch="////", linewidth=0.6, zorder=3,
           label="NCR CCMR 2017-Q1 (accounts)")
    ax.bar(x + w / 2 + 0.01, model, w, yerr=sd, color=SRC, edgecolor=SURF, linewidth=0.6, zorder=3,
           error_kw=dict(ecolor=INK, **ERR), label="Model, no BNPL (credit-active households)")
    for i, b in enumerate(bands):
        ax.text(x[i] - w / 2 - 0.01, target[i] + 0.6, f"{target[i]:.1f}", ha="center", va="bottom", fontsize=8)
        ax.text(x[i] + w / 2 + 0.01, model[i] + sd[i] + 0.6, f"{model[i]:.1f}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}\n{status.get(b, 'unfitted')}" for l, b in zip(labels, bands)])
    for t, b in zip(ax.get_xticklabels(), bands):
        t.set_color(INK if b in fitted else INK2)
    ax.set_ylim(0, max(target.max(), (model + sd).max()) * 1.18)
    ax.set_ylabel("Share of accounts or households (%)")
    ax.set_xlabel("Days in arrears on traditional credit")
    ax.legend(loc="upper right")
    dress(ax)
    fig.tight_layout()
    save(fig, "fig_baseline_arrears")
    plt.close(fig)


# =================================================================== stacking
def fig_stacking(rq1: pd.DataFrame) -> None:
    # Panels (a) and (b) start at two platforms: with one platform no household can hold
    # facilities on two platforms, so the share is zero by construction and is not a result.
    fig, axes = plt.subplots(1, 3, figsize=(TW, 2.55))
    series = [(0.0, INK, CTRL_LBL, "s"), (BP, SRC, BETA1_LBL, "o")]
    cols = ("stacking_2plus_final", "ever_stacked_2plus_of_adopters", "default_rate_final")
    top_a = 0.0
    for j, (b, colour, label, marker) in enumerate(series):
        sub = rq1[rq1.beta == b]
        dx = (j - 0.5) * 0.16  # dodge, so the two arms' error bars do not overlap
        for ax, col in zip(axes, cols):
            g = agg(sub if col == "default_rate_final" else sub[sub.n_platforms >= 2], "n_platforms", col)
            ax.errorbar(g.index + dx, g["mean"] * 100, yerr=g["ci"] * 100, color=colour, marker=marker,
                        label=label, zorder=4 if b == 0 else 3, **ERR)
            if col == cols[0]:
                top_a = max(top_a, float(((g["mean"] + g["ci"]) * 100).max()))
    axes[1].axhline(32, ls="--", lw=0.9, color=RED, zorder=2)
    # Above the line at the left, where there are no data (both shares start at two platforms).
    axes[1].text(0.72, 34, "CFPB 32% (US, cross-firm,\nover a year)", ha="left", va="bottom",
                 fontsize=8, color=RED, linespacing=1.1)
    axes[0].set_title("(a) 2+ platforms, final tick")
    axes[1].set_title("(b) 2+ platforms, ever")
    axes[2].set_title("(c) Default rate")
    axes[0].set_ylabel("Share of all households (%)")
    axes[1].set_ylabel("Share of households that\never held BNPL (%)")
    axes[2].set_ylabel("Population default rate (%)")
    for ax in axes:
        ax.set_xlabel("Number of BNPL platforms")
        ax.set_xticks(range(1, 7))
        ax.set_xlim(0.6, 6.4)
        dress(ax)
    axes[0].set_ylim(0, top_a * 1.6)  # data-driven; a fixed 70 went stale after a rerun
    axes[1].set_ylim(0, 100)          # a share of ever-holders, so the whole range
    axes[2].margins(y=0.15)
    one_decimal(axes[2])
    legend_below(fig, *axes[0].get_legend_handles_labels())
    fig.tight_layout(w_pad=1.0, rect=(0, 0.08, 1, 1))
    save(fig, "fig_stacking")
    plt.close(fig)


# =================================================================== access and default
def fig_access_default(rq2: pd.DataFrame, rq2t: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(TW, 3.2))
    ax_a, ax_b, ax_c = axes

    def dodge(i: int, n: int) -> float:
        return (i - (n - 1) / 2) * 0.012

    betas = sorted(rq2.beta.unique())
    for i, b in enumerate(betas):
        g = agg(rq2[rq2.beta == b], "bnpl_access_rate", "default_rate_final")
        ctrl = b == 0
        ax_a.errorbar(g.index + dodge(i, len(betas)), g["mean"] * 100, yerr=g["ci"] * 100,
                      color=INK if ctrl else RAMP[i], marker="s" if ctrl else MARKERS[i - 1],
                      lw=1.4 if ctrl else 1.0, zorder=5 if ctrl else 3,
                      label=CTRL_LBL if ctrl else rf"$\beta\,=\,{b:g}$", **ERR)
    ax_a.set_title("(a) Linear rule")
    ax_a.set_ylabel("Population default rate (%)")

    surf = rq2t[rq2t.label.str.startswith("rq2t_a")]
    ctrl = surf[surf.gamma == 0]
    live = surf[surf.gamma > 0]
    sigmas = sorted(live.sigma_theta.unique())
    n = len(sigmas) + 1
    top_b = 0.0
    for ax, col in ((ax_b, "bnpl_adoption_final"), (ax_c, "default_rate_final")):
        for i, s in enumerate(sigmas):
            g = agg(live[live.sigma_theta == s], "bnpl_access_rate", col)
            ax.errorbar(g.index + dodge(i + 1, n), g["mean"] * 100, yerr=g["ci"] * 100, color=RAMP[i],
                        marker=MARKERS[i], lw=1.0, label=rf"$\sigma_\theta\,=\,{param(s)}$", zorder=3, **ERR)
            if ax is ax_b:
                top_b = max(top_b, float(((g["mean"] + g["ci"]) * 100).max()))
        g = agg(ctrl, "bnpl_access_rate", col)
        ax.errorbar(g.index + dodge(0, n), g["mean"] * 100, yerr=g["ci"] * 100, color=INK, marker="s",
                    lw=1.4, label=r"$\gamma\,=\,0$ (control)", zorder=5, **ERR)
    ax_b.set_title("(b) Threshold rule")
    ax_b.set_ylabel("Households holding BNPL,\nfinal tick (%)")
    ax_c.set_title("(c) Threshold rule")
    ax_c.set_ylabel("Population default rate (%)")
    for ax in axes:
        ax.set_xlabel("Access (share of banked)")
        ax.set_xlim(-0.04, 1.04)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_xticklabels(["0", "", "0.5", "", "1"])
        dress(ax)
    ax_b.set_ylim(0, top_b * 1.12)
    # Panels (a) and (c) share a data-driven default scale (fixed limits went stale on 2026-10-12).
    for ax in (ax_a, ax_c):
        ax.margins(y=0.08)
        ax.autoscale_view()
    lo = min(ax_a.get_ylim()[0], ax_c.get_ylim()[0]); hi = max(ax_a.get_ylim()[1], ax_c.get_ylim()[1])
    for ax in (ax_a, ax_c):
        ax.set_ylim(lo, hi)
        one_decimal(ax)
    fig.tight_layout(w_pad=1.0, rect=(0, 0.17, 1, 1))
    # Two legends under the panels they belong to: (a) on the left, (b) and (c) on the right.
    h, l = ax_a.get_legend_handles_labels()
    fig.legend(h, l, title="(a) Linear rule", ncol=2, loc="lower left", alignment="left",
               bbox_to_anchor=(ax_a.get_position().x0 - 0.06, 0.0), title_fontsize=9)
    h, l = ax_b.get_legend_handles_labels()
    fig.legend(h, l, title=r"(b), (c) Threshold rule, $\gamma\,=\,0.3$", ncol=3, loc="lower right",
               alignment="left", bbox_to_anchor=(ax_c.get_position().x1 + 0.01, 0.0), title_fontsize=9)
    save(fig, "fig_access_default")
    plt.close(fig)


# =================================================================== scenarios (body)
def fig_scenarios(rq3s: pd.DataFrame) -> None:
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(TW, 2.75))
    x = np.arange(len(SCENARIOS))
    w = 0.36
    allvols = []
    for j, (b, colour, label, marker) in enumerate([(0.0, INK, CTRL_LBL, "s"), (BP, SRC, BETA1_LBL, "o")]):
        means, sds, vols = [], [], []
        bench = arm(rq3s, f"rq3s_bench_b{b}").bnpl_volume_cumulative.mean()
        for key, _ in SCENARIOS:
            d = arm(rq3s, f"rq3s_{key}_b{b}")
            means.append(d.default_rate_final.mean() * 100)
            sds.append(half_ci(d.default_rate_final) * 100)
            vols.append((d.bnpl_volume_cumulative.mean() / bench - 1) * 100)
        allvols += vols
        off = (j - 0.5) * (w + 0.02)
        ax_a.errorbar(x + off, means, yerr=sds, fmt=marker, color=colour, ms=4.5, label=label, zorder=3, **ERR)
        for xi, v in zip(x + off, vols):
            if abs(v) < 0.05:  # the benchmark against itself: zero by construction, no bar
                continue
            ax_b.bar(xi, v, w, color=colour, edgecolor=SURF, linewidth=0.6, zorder=3)
            ax_b.text(xi, v - 0.12 if v < 0 else v + 0.12, minus(v), ha="center",
                      va="top" if v < 0 else "bottom", fontsize=8)
    names = [n.replace(" ", "\n") for _, n in SCENARIOS]  # "Bureau\nvisibility": no collision
    for ax in (ax_a, ax_b):
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        ax.set_xlim(-0.6, len(SCENARIOS) - 0.4)
        dress(ax)
    ax_a.margins(y=0.12)
    one_decimal(ax_a)
    ax_a.set_ylabel("Population default rate (%)")
    ax_a.set_title("(a) Default at the final tick")
    ax_b.axhline(0, color=INK2, lw=0.6, zorder=4)
    lo, hi = min(allvols), max(allvols)
    ax_b.set_ylim(min(lo, 0) * 1.3 - 0.2, max(hi, 0) * 1.3 + 0.3)  # data-driven, with room for the labels
    ax_b.set_ylabel("Cumulative BNPL volume\nvs benchmark (%)")
    ax_b.set_title("(b) Cumulative volume")
    legend_below(fig, *ax_a.get_legend_handles_labels())
    fig.tight_layout(w_pad=1.6, rect=(0, 0.08, 1, 1))
    save(fig, "fig_scenarios")
    plt.close(fig)


# =================================================================== tornado
# Each group: display name, reference label, [(arm name, arm label)], swept (no source fixes
# the value: the "Swept" class of Table 3.1). Arms are matched by exact label; a prefix match
# once pooled the default-horizon arms with the kappa arms ("rob_k" is a prefix of "rob_kappa").
# Population size and activation order are numerical checks, not model assumptions, and the
# single-tick shock arm changes the shock process itself; all three stay in the appendix table.
# The 56-day default threshold (rob_k4 against rob_k7) was taken out on 2026-11-10: it changes
# the definition and the timing of default (freezing, cut-off from credit, write-off), not a
# behavioural assumption, and its +13 points compressed every other arm. It stays in
# Table tab:robustness.
TORNADO_GROUPS = [
    ("Borrowing amount on a shortfall (exact)", "rob_amount_shortfall", [
        ("shortfall +25%", "rob_amount_shortfall_125"),
        ("shortfall + one tick of committed expenditure", "rob_amount_shortfall_plus_committed"),
        ("exact shortfall, uncapped", "rob_amount_shortfall_uncapped"),
        ("shortfall +25%, uncapped", "rob_amount_shortfall_125_uncapped"),
        ("shortfall + one tick of committed expenditure, uncapped", "rob_amount_shortfall_plus_committed_uncapped"),
    ], True),
    (r"Purchase size $\kappa$ (0.139)", "rob_kappa0.1387", [("0.07", "rob_kappa0.07"), ("0.28", "rob_kappa0.28")], False),
    ("Purchase sizing base (discretionary)", "rob_base_discretionary", [("sized on income", "rob_base_income")], False),
    ("Minimum-payment fraction (0.05)", "rob_minpay0.05",
     [("0.025", "rob_minpay0.025"), ("0.10", "rob_minpay0.1")], True),
    (r"Rolling limit $\lambda$ (0.10)", "rob_limit0.1",
     [("0.25", "rob_limit0.25"), ("0.50", "rob_limit0.5"), ("1.00", "rob_limit1.0")], True),
    ("Minimum-payer share (0.29)", "rob_m0.29",
     [("0.20", "rob_m0.2"), ("0.25", "rob_m0.25"), ("0.35", "rob_m0.35"), ("0.40", "rob_m0.4")], False),
]


def fig_tornado(rob: pd.DataFrame) -> None:
    def x(label: str) -> pd.Series:
        return arm(rob, label).set_index("seed").default_rate_final * 100

    blocks = []
    for name, ref, arms_, swept in TORNADO_GROUPS:
        r = x(ref)
        rows = []
        for arm_name, label in arms_:
            a = x(label)
            # Every group shares seeds and population with its reference, so the interval is
            # that of the paired difference, as in the tables.
            assert sorted(a.index) == sorted(r.index), f"{label} does not share seeds with {ref}"
            z = a - r.reindex(a.index)
            se = z.std(ddof=1) / np.sqrt(z.count())
            rows.append((arm_name, z.mean(), stats.t.ppf(0.975, z.count() - 1) * se))
        blocks.append((name, swept, rows, max(abs(d) for _, d, _ in rows)))
    blocks.sort(key=lambda b: -b[3])

    ticks, names, headers = [], [], []
    y = 0
    fig, ax = plt.subplots(figsize=(TW, 4.5))
    for name, swept, rows, _ in blocks:
        ticks.append(y)
        names.append(name)
        headers.append(True)
        y += 1
        for arm_name, d, h in rows:
            face = SURF if swept else SRC
            ax.errorbar(d, y, xerr=h, fmt="o", mfc=face, mec=SRC, color=SRC, zorder=3, **ERR)
            ticks.append(y)
            names.append(arm_name)
            headers.append(False)
            y += 1
        y += 0.4
    ax.axvline(0, color=INK2, lw=0.6, zorder=2)
    ax.set_yticks(ticks)
    ax.set_yticklabels(names)
    for t, head in zip(ax.get_yticklabels(), headers):
        if head:  # group headings in Computer Modern bold; arms in roman
            t.set_fontfamily("cmb10")
    ax.invert_yaxis()
    ax.set_ylim(y - 0.4 - 0.5, -0.6)
    ax.set_xlabel("Change in default rate from the reference value (pp)")
    dress(ax, ygrid=False, xgrid=True)
    ax.tick_params(axis="y", length=0)
    legend_below(fig, [
        Line2D([0], [0], marker="o", lw=0, mfc=SRC, mec=SRC),
        Line2D([0], [0], marker="o", lw=0, mfc=SURF, mec=SRC),
    ], ["reference value observed, constructed, imported or fitted",
        "no empirical estimate exists: range swept"], ncol=1, handlelength=1.0)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "fig_tornado")
    plt.close(fig)


# =================================================================== scenarios (appendix)
def fig_scenarios_appendix(rq3: pd.DataFrame, rq3s: pd.DataFrame) -> None:
    """Each lever's change in default against its own benchmark.

    The switches (100 replicates) and the levers (20) have different benchmark arms, so the
    figure plots differences and not levels.
    """
    arms = [("rq3s", "bureau", "Bureau visibility"), ("rq3s", "afford", "Screening"), ("rq3s", "both", "Both switches")] + \
           [("rq3", f"kcool{k}", f"Cooling-off {k} tick{'s' if k > 1 else ''}") for k in (1, 2, 3, 4)] + \
           [("rq3", f"cap{c}", f"Cap: {c} platform{'' if c == 1 else 's'} owed (hypothetical)") for c in (1, 2, 3)]
    frames = {"rq3": (rq3, "kcool0"), "rq3s": (rq3s, "bench")}
    fig, axes = plt.subplots(1, 2, figsize=(TW, 3.35), sharey=True, sharex=True)
    y = np.arange(len(arms))
    lo, hi = 0.0, 0.0
    for i, (ax, b) in enumerate(zip(axes, (0.0, BP))):
        for yi, (suite, k, _) in zip(y, arms):
            df, bench_key = frames[suite]
            d = arm(df, f"{suite}_{k}_b{b}")
            dd, se = delta(d, arm(df, f"{suite}_{bench_key}_b{b}"), "default_rate_final")
            half = stats.t.ppf(0.975, len(d) - 1) * se
            lo, hi = min(lo, (dd - half) * 100), max(hi, (dd + half) * 100)
            hyp = k.startswith("cap")
            ax.errorbar(dd * 100, yi, xerr=half * 100, fmt="D" if hyp else "o", color=RED if hyp else DKBLUE,
                        ms=4.2 if hyp else 4.5, zorder=3, **ERR)
        ax.axvline(0, color=INK, lw=0.8, ls="--", zorder=2)
        ax.set_title(rf"({'ab'[i]}) $\beta\,=\,{b:g}$")
        dress(ax, ygrid=False, xgrid=True)
    # Limits from the data: a fixed (-0.75, 0.5) once hid the screening rows (about -1 point).
    pad = 0.1
    axes[0].set_xlim(lo - pad, hi + pad)
    axes[0].xaxis.set_major_locator(MultipleLocator(0.5))
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([n for _, _, n in arms])
    axes[0].set_ylim(len(arms) - 0.5, -0.5)
    axes[1].tick_params(axis="y", length=0)
    legend_below(fig, [Line2D([0], [0], color=DKBLUE, marker="o", lw=0, ms=4.5),
                       Line2D([0], [0], color=RED, marker="D", lw=0, ms=4.2),
                       Line2D([0], [0], color=INK, ls="--", lw=0.8)],
                 ["implemented or proposed instrument", "hypothetical: no jurisdiction found that imposes it",
                  "no change"], ncol=2, handlelength=1.4, columnspacing=1.0)
    fig.tight_layout(rect=(0, 0.165, 1, 1), w_pad=1.2)
    # One x-axis label for both panels, just under the tick labels and above the legend.
    r = fig.canvas.get_renderer()
    y_ticks = min(ax.xaxis.get_tightbbox(r).y0 for ax in axes) / fig.bbox.height
    x_mid = (axes[0].get_position().x0 + axes[1].get_position().x1) / 2
    # The legend is centred on the two panels, as the axis label is, not on the whole figure,
    # as far as the figure's right edge allows (it is about as wide as the two panels).
    legend = fig.legends[-1]
    half = legend.get_window_extent(r).width / fig.bbox.width / 2
    legend.set_bbox_to_anchor((min(x_mid, 1 - half), 0.0), transform=fig.transFigure)
    fig.text(x_mid, y_ticks - 0.01, "Change in default against the benchmark (percentage points)", ha="center",
             va="top", fontsize=plt.rcParams["axes.labelsize"])
    save(fig, "fig_scenarios_appendix")
    plt.close(fig)


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (load(n) for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    fig_baseline_arrears(rq0)
    fig_stacking(rq1)
    fig_access_default(rq2, rq2t)
    rq3s = load("rq3s")
    fig_scenarios(rq3s)
    fig_tornado(rob)
    fig_scenarios_appendix(rq3, rq3s)


if __name__ == "__main__":
    main()
