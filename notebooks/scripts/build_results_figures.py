"""The results figures for Sections 4 and 5 and Appendix C, from results/raw.

    ./env/python.exe notebooks/scripts/build_results_figures.py

Writes to thesis/figures as vector PDF (plus PNG for preview), drawn at the compiled text
width so nothing is rescaled:
  fig_baseline_arrears   baseline arrears profile against the CCMR bands, fitted bands marked
  fig_stacking           2+ facility shares (final tick; ever, the CFPB analogue) and default
  fig_access_default     default against access: linear coupling, and thresholds (adoption, default)
  fig_scenarios          the three body scenarios at both betas, default and volume
  fig_tornado            each sensitivity arm's change from its reference, with 95% intervals
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
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from results_common import (  # noqa: E402
    GRID, INK, INK2, INK3, RAMP, RC, RED, SCENARIOS, SRC, SURF, TW, arm, dress, load, save,
)
from simulation.config import load_ccmr_bands  # noqa: E402

plt.rcParams.update(RC)
CTRL_LBL = r"$\beta = 0$ (control)"
BETA1_LBL = r"$\beta = 1$"


def half_ci(x: pd.Series) -> float:
    """Half-width of the 95% confidence interval of the mean of x."""
    n = x.count()
    return float(stats.t.ppf(0.975, n - 1) * x.std(ddof=1) / np.sqrt(n))


def agg(df: pd.DataFrame, by: str, col: str) -> pd.DataFrame:
    """Mean and 95% CI half-width per group."""
    g = df.groupby(by)[col]
    return pd.DataFrame({"mean": g.mean(), "ci": g.apply(half_ci)}).sort_index()


# =================================================================== baseline arrears
def fig_baseline_arrears(rq0: pd.DataFrame) -> None:
    off = arm(rq0, "baseline_no_bnpl")
    pct = load_ccmr_bands()
    bands = ["current", "d30", "d31_60", "d61_90", "d91_120", "d120_plus"]
    labels = ["Current", "1–30 d", "31–60 d", "61–90 d", "91–120 d", "120+ d"]
    # The 1-30 day band is fitted on its own; 91-120 and 120+ are fitted only as their sum (90+).
    fitted = {"d30", "d91_120", "d120_plus"}
    status = {"d30": "fitted", "d91_120": "in fitted 90+", "d120_plus": "in fitted 90+"}
    model = np.array([off[f"active_{b}_mean"].mean() * 100 for b in bands])
    sd = np.array([half_ci(off[f"active_{b}_mean"]) * 100 for b in bands])
    target = np.array([pct[b] for b in bands])

    fig, ax = plt.subplots(figsize=(TW, 2.55))
    x = np.arange(len(bands))
    w = 0.38
    ax.bar(x - w / 2 - 0.01, target, w, color=INK3, edgecolor=SURF, linewidth=0.8, zorder=3,
           label="NCR CCMR 2017-Q1 (accounts)")
    ax.bar(x + w / 2 + 0.01, model, w, yerr=sd, color=SRC, edgecolor=SURF, linewidth=0.8, zorder=3,
           error_kw=dict(elinewidth=0.7, capsize=2, ecolor=INK2), label="Model, no BNPL (credit-active households)")
    for i, b in enumerate(bands):
        ax.text(x[i] - w / 2 - 0.01, target[i] + 0.4, f"{target[i]:.1f}", ha="center", va="bottom", fontsize=6.0, color=INK2)
        ax.text(x[i] + w / 2 + 0.01, model[i] + sd[i] + 0.4, f"{model[i]:.1f}", ha="center", va="bottom", fontsize=6.0, color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{l}\n{status.get(b, 'unfitted')}" for l, b in zip(labels, bands)])
    for t, b in zip(ax.get_xticklabels(), bands):
        t.set_color(INK if b in fitted else INK2)
    ax.set_ylim(0, 86)
    ax.set_ylabel("Share of accounts or households (%)")
    ax.set_xlabel("Days in arrears on traditional credit")
    ax.legend(loc="upper right", handlelength=1.2)
    dress(ax)
    fig.tight_layout()
    save(fig, "fig_baseline_arrears")
    plt.close(fig)


# =================================================================== stacking
def fig_stacking(rq1: pd.DataFrame) -> None:
    # Panels (a) and (b) start at two platforms: with one platform no household can hold
    # facilities on two platforms, so the share is zero by construction and is not a result.
    fig, axes = plt.subplots(1, 3, figsize=(TW, 2.45))
    series = [(0.0, INK, CTRL_LBL, "s"), (1.0, SRC, BETA1_LBL, "o")]
    cols = ("stacking_2plus_final", "ever_stacked_2plus_of_adopters", "default_rate_final")
    for b, colour, label, marker in series:
        sub = rq1[rq1.beta == b]
        for ax, col in zip(axes, cols):
            g = agg(sub if col == "default_rate_final" else sub[sub.n_platforms >= 2], "n_platforms", col)
            ax.errorbar(g.index, g["mean"] * 100, yerr=g["ci"] * 100, color=colour, marker=marker,
                        ms=3.2, lw=1.4, capsize=2, elinewidth=0.7, label=label, zorder=4 if b == 0 else 3)
    axes[1].axhline(32, ls="--", lw=0.9, color=RED, zorder=2)
    axes[1].text(6.15, 29.5, "CFPB 32%\n(US, cross-firm,\nover a year)", ha="right", va="top",
                 fontsize=6.0, color=RED, linespacing=1.25)
    axes[0].set_title("(a) 2+ platforms, final tick")
    axes[1].set_title("(b) 2+ platforms, ever")
    axes[2].set_title("(c) Default rate")
    axes[0].set_ylabel("Share of all households (%)")
    axes[1].set_ylabel("Share of ever-adopters (%)")
    axes[2].set_ylabel("Share of all households (%)")
    for ax in axes:
        ax.set_xlabel("Number of BNPL platforms")
        ax.set_xticks(range(1, 7))
        ax.set_xlim(0.6, 6.4)
        dress(ax)
    axes[0].set_ylim(0, 65)
    axes[1].set_ylim(0, 105)
    axes[2].set_ylim(13.5, 16.5)
    axes[0].legend(loc="center right", handlelength=1.6)
    fig.tight_layout(w_pad=1.4)
    save(fig, "fig_stacking")
    plt.close(fig)


# =================================================================== access and default
def fig_access_default(rq2: pd.DataFrame, rq2t: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(TW, 2.5))
    ax_a, ax_b, ax_c = axes

    betas = sorted(rq2.beta.unique())
    for i, b in enumerate(betas):
        g = agg(rq2[rq2.beta == b], "bnpl_access_rate", "default_rate_final")
        ctrl = b == 0
        ax_a.errorbar(g.index, g["mean"] * 100, yerr=g["ci"] * 100,
                      color=INK if ctrl else RAMP[i], marker="s" if ctrl else "o", ms=3.0,
                      lw=1.6 if ctrl else 1.2, capsize=2, elinewidth=0.6, zorder=5 if ctrl else 3,
                      label=CTRL_LBL if ctrl else rf"$\beta = {b:g}$")
    ax_a.set_title("(a) Linear rule")
    ax_a.set_ylabel("Population default rate (%)")
    ax_a.legend(loc="upper left", handlelength=1.4, ncol=1)

    surf = rq2t[rq2t.label.str.startswith("rq2t_a")]
    ctrl = surf[surf.gamma == 0]
    live = surf[surf.gamma > 0]
    sigmas = sorted(live.sigma_theta.unique())
    for ax, col, scale in ((ax_b, "bnpl_adoption_final", 100), (ax_c, "default_rate_final", 100)):
        for i, s in enumerate(sigmas):
            g = agg(live[live.sigma_theta == s], "bnpl_access_rate", col)
            ax.errorbar(g.index, g["mean"] * scale, yerr=g["ci"] * scale, color=RAMP[i], marker="o",
                        ms=2.8, lw=1.1, capsize=1.5, elinewidth=0.5, label=rf"$\sigma_\theta = {s:g}$", zorder=3)
        g = agg(ctrl, "bnpl_access_rate", col)
        ax.errorbar(g.index, g["mean"] * scale, yerr=g["ci"] * scale, color=INK, marker="s", ms=3.0,
                    lw=1.6, capsize=2, elinewidth=0.6, label=r"$\gamma = 0$ (control)", zorder=5)
    ax_b.set_title("(b) Threshold rule")
    ax_b.set_ylabel("Households holding BNPL, final tick (%)")
    ax_c.set_title("(c) Threshold rule")
    ax_c.set_ylabel("Population default rate (%)")
    ax_b.legend(loc="upper left", handlelength=1.2, fontsize=6.0, ncol=2, columnspacing=0.8)
    for ax in axes:
        ax.set_xlabel("Access (share of banked)")
        ax.set_xlim(-0.03, 1.03)
        dress(ax)
    ax_a.set_ylim(13, 17)
    ax_b.set_ylim(0, 75)
    ax_c.set_ylim(13, 17)
    fig.tight_layout(w_pad=1.3)
    save(fig, "fig_access_default")
    plt.close(fig)


# =================================================================== scenarios (body)
def fig_scenarios(rq3: pd.DataFrame) -> None:
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(TW, 2.5))
    x = np.arange(len(SCENARIOS))
    w = 0.36
    for j, (b, colour, label) in enumerate([(0.0, INK3, CTRL_LBL), (1.0, SRC, BETA1_LBL)]):
        means, sds, vols = [], [], []
        bench = arm(rq3, f"rq3_kcool0_b{b}").bnpl_volume_cumulative.mean()
        for key, _ in SCENARIOS:
            d = arm(rq3, f"rq3_{key}_b{b}")
            means.append(d.default_rate_final.mean() * 100)
            sds.append(half_ci(d.default_rate_final) * 100)
            vols.append((d.bnpl_volume_cumulative.mean() / bench - 1) * 100)
        off = (j - 0.5) * (w + 0.02)
        ax_a.errorbar(x + off, means, yerr=sds, fmt="o" if b else "s", color=colour, ms=4.5,
                      capsize=3, elinewidth=0.8, label=label, zorder=3)
        ax_b.bar(x + off, vols, w, color=colour, edgecolor=SURF, linewidth=0.8, zorder=3, label=label)
        for xi, v in zip(x + off, vols):
            if abs(v) < 0.05:
                continue
            ax_b.text(xi, v + (0.15 if v >= 0 else -0.15), f"{v:+.1f}", ha="center",
                      va="bottom" if v >= 0 else "top", fontsize=6.2, color=INK2)
    names = [n for _, n in SCENARIOS]
    for ax in (ax_a, ax_b):
        ax.set_xticks(x)
        ax.set_xticklabels(names)
        dress(ax)
    ax_a.set_ylim(12.5, 16.5)
    ax_a.set_ylabel("Population default rate (%)")
    ax_a.set_title("(a) Default at the final tick")
    ax_a.legend(loc="upper left", handlelength=1.2)
    ax_b.axhline(0, color=INK3, lw=0.8)
    ax_b.set_ylim(-3.2, 3.2)
    ax_b.set_ylabel("Cumulative BNPL volume vs benchmark (%)")
    ax_b.set_title("(b) Volume: defer or desist?")
    fig.tight_layout(w_pad=1.6)
    save(fig, "fig_scenarios")
    plt.close(fig)


# =================================================================== tornado
# Each group: display name, reference label, [(arm name, arm label)], swept (no source fixes
# the value: the "Swept" class of Table 3.1). Arms are matched by exact label; a prefix match
# once pooled the default-horizon arms with the kappa arms ("rob_k" is a prefix of "rob_kappa").
# Population size and activation order are numerical checks, not model assumptions, and the
# single-tick shock arm (-9.8pp) is off any shared scale; all three stay in the appendix table.
TORNADO_GROUPS = [
    ("Borrowing amount on a shortfall (exact)", "rob_amount_shortfall", [
        ("+25%", "rob_amount_shortfall_125"),
        ("+ one tick of committed spending", "rob_amount_shortfall_plus_committed"),
        ("exact, BNPL cap removed", "rob_amount_shortfall_uncapped"),
        ("+25%, BNPL cap removed", "rob_amount_shortfall_125_uncapped"),
        ("+ committed, BNPL cap removed", "rob_amount_shortfall_plus_committed_uncapped"),
    ], True),
    ("Default horizon (98 days)", "rob_k7", [("56 days", "rob_k4")], False),
    ("Purchase size κ (0.139)", "rob_kappa0.1387", [("0.07", "rob_kappa0.07"), ("0.28", "rob_kappa0.28")], False),
    ("Purchase sizing base (discretionary)", "rob_base_discretionary", [("income", "rob_base_income")], False),
    ("Minimum-payment fraction (0.05)", "rob_minpay0.05",
     [("0.025", "rob_minpay0.025"), ("0.10", "rob_minpay0.1")], True),
    ("Rolling limit λ (0.10)", "rob_limit0.1",
     [("0.25", "rob_limit0.25"), ("0.50", "rob_limit0.5"), ("1.00", "rob_limit1.0")], True),
    ("Minimum-payer share (0.29)", "rob_m0.29",
     [("0.20", "rob_m0.2"), ("0.25", "rob_m0.25"), ("0.35", "rob_m0.35"), ("0.40", "rob_m0.4")], False),
]


def fig_tornado(rob: pd.DataFrame) -> None:
    def x(label: str) -> pd.Series:
        return arm(rob, label).default_rate_final * 100

    blocks = []
    for name, ref, arms_, swept in TORNADO_GROUPS:
        r = x(ref)
        rows = []
        for arm_name, label in arms_:
            a = x(label)
            d = a.mean() - r.mean()
            se = np.sqrt(a.var(ddof=1) / a.count() + r.var(ddof=1) / r.count())
            rows.append((arm_name, d, stats.t.ppf(0.975, a.count() + r.count() - 2) * se))
        blocks.append((name, swept, rows, max(abs(d) for _, d, _ in rows)))
    blocks.sort(key=lambda b: -b[3])

    ticks, names, headers = [], [], []
    y = 0
    fig, ax = plt.subplots(figsize=(TW, 3.9))
    for name, swept, rows, _ in blocks:
        ticks.append(y)
        names.append(name)
        headers.append(True)
        y += 1
        for arm_name, d, h in rows:
            face = SURF if swept else SRC
            ax.errorbar(d, y, xerr=h, fmt="o", ms=3.6, mfc=face, mec=SRC, mew=1.0, color=SRC,
                        capsize=2, elinewidth=0.8, zorder=3)
            ticks.append(y)
            names.append(arm_name)
            headers.append(False)
            y += 1
        y += 0.4
    ax.axvline(0, color=INK3, lw=0.8, zorder=2)
    ax.set_yticks(ticks)
    ax.set_yticklabels(names)
    for t, head in zip(ax.get_yticklabels(), headers):
        t.set_fontweight("bold" if head else "normal")
        t.set_color(INK if head else INK2)
    ax.invert_yaxis()
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Change in population default rate from the reference value (pp)")
    fig.legend(handles=[
        Line2D([0], [0], marker="o", lw=0, ms=4, mfc=SRC, mec=SRC,
               label="reference value observed, constructed, imported or fitted"),
        Line2D([0], [0], marker="o", lw=0, ms=4, mfc=SURF, mec=SRC,
               label="no empirical estimate exists: range swept"),
    ], loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0), handlelength=1.0)
    dress(ax, ygrid=False, xgrid=True)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    save(fig, "fig_tornado")
    plt.close(fig)


# =================================================================== scenarios (appendix)
def fig_scenarios_appendix(rq3: pd.DataFrame) -> None:
    arms = [("bureau", "Bureau visibility"), ("afford", "Screening")] + \
           [(f"kcool{k}", f"Cooling-off {k} tick{'s' if k > 1 else ''}") for k in (1, 2, 3, 4)] + \
           [(f"cap{c}", f"Cap: {c} facilit{'y' if c == 1 else 'ies'} (hypothetical)") for c in (1, 2, 3)]
    fig, axes = plt.subplots(1, 2, figsize=(TW, 2.9), sharey=True)
    y = np.arange(len(arms))
    for ax, b in zip(axes, (0.0, 1.0)):
        bench = arm(rq3, f"rq3_kcool0_b{b}").default_rate_final
        means = [arm(rq3, f"rq3_{k}_b{b}").default_rate_final.mean() * 100 for k, _ in arms]
        sds = [half_ci(arm(rq3, f"rq3_{k}_b{b}").default_rate_final) * 100 for k, _ in arms]
        for yi, m, s, (k, _) in zip(y, means, sds, arms):
            hyp = k.startswith("cap")
            ax.errorbar(m, yi, xerr=s, fmt="D" if hyp else "o", color=RED if hyp else SRC, ms=4.2,
                        capsize=2.5, elinewidth=0.8, zorder=3)
        ax.axvline(bench.mean() * 100, color=INK, lw=1.0, ls="--", zorder=2)
        ax.set_title(rf"$\beta = {b:g}$")
        ax.set_xlim(12.5, 16.5)
        ax.set_xlabel("Population default rate (%)")
        dress(ax, ygrid=False, xgrid=True)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([n for _, n in arms])
    axes[0].invert_yaxis()
    fig.legend(handles=[Line2D([0], [0], color=SRC, marker="o", lw=0, ms=4.2, label="implemented or proposed instrument"),
                        Line2D([0], [0], color=RED, marker="D", lw=0, ms=4.2, label="hypothetical: no jurisdiction imposes it"),
                        Line2D([0], [0], color=INK, ls="--", lw=1.0, label="benchmark mean")],
               loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0), handlelength=1.2)
    fig.tight_layout(rect=(0, 0.08, 1, 1), w_pad=1.0)
    save(fig, "fig_scenarios_appendix")
    plt.close(fig)


def main() -> None:
    rq0, rq1, rq2, rq2t, rq3, rob = (load(n) for n in ("rq0", "rq1", "rq2", "rq2t", "rq3", "robustness"))
    fig_baseline_arrears(rq0)
    fig_stacking(rq1)
    fig_access_default(rq2, rq2t)
    fig_scenarios(rq3)
    fig_tornado(rob)
    fig_scenarios_appendix(rq3)


if __name__ == "__main__":
    main()
