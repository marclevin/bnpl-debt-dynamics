"""Figures for the data chapter: does the 5,000-agent population reproduce its sources?

Two outputs, written to thesis/figures as vector PDF (plus PNG for preview):
  fig_population_fidelity.pdf  - agents (unweighted) vs NIDS source (weighted), six key distributions
  fig_inclusion_fidelity.pdf   - imputed FinScope flags, nationally and by quintile

Style: the shared figure style of results_common.py. The weighted source is dark blue, the
unweighted agents light orange and the FinScope benchmark hatched, so the series separate in
greyscale as well as in colour.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.ticker import LogLocator, NullLocator
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PROC = ROOT / "data/processed"
FIGS = ROOT / "thesis/figures"

from notebooks.scripts.survey_common import load_finscope, wgini  # noqa: E402

# ---------------------------------------------------------------- style
# The shared figure style of results_common (Computer Modern, 8 pt ticks, 9 pt labels), drawn at
# the compiled text width and included at width=\textwidth, so these point sizes are the printed
# ones. Series separate in greyscale as well as colour: the survey source is dark blue, the
# agents light orange, and the external FinScope benchmark is hatched.
from notebooks.scripts.results_common import (  # noqa: E402
    DKBLUE as SRC, INK, INK2, LTORANGE as AGT, RC, RED, SURF, TW, dress, minus, save,
)

plt.rcParams.update(RC)
BENCH_STYLE = dict(color=SURF, edgecolor=INK, hatch="////", linewidth=0.6)


def grouped(ax, cats, series, styles, width=0.38, gap=0.02, horizontal=False):
    """Grouped bars; each style is a colour (filled bar) or a dict of bar keywords."""
    x = np.arange(len(cats))
    k = len(series)
    for i, ((label, vals), style) in enumerate(zip(series.items(), styles)):
        off = (i - (k - 1) / 2) * (width + gap)
        kw = style if isinstance(style, dict) else dict(color=style, edgecolor=SURF, linewidth=0.5)
        (ax.barh if horizontal else ax.bar)(x + off, vals, width, label=label, zorder=3, **kw)
    if horizontal:
        ax.set_yticks(x)
        ax.set_yticklabels(cats)
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(cats)
    return x


# ---------------------------------------------------------------- data
QORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]
FLAGS = ["banked", "G10", "G11", "G12", "G13", "G14"]
FLAG_LABEL = {"banked": "Banked", "G10": "Store card", "G11": "Revolving credit",
              "G12": "Hire purchase", "G13": "Short-term loan", "G14": "Personal loan"}
PROV_ABBR = {"Western Cape": "WC", "Eastern Cape": "EC", "Northern Cape": "NC",
             "Free State": "FS", "KwaZulu-Natal": "KZN", "North West": "NW",
             "Gauteng": "GP", "Mpumalanga": "MP", "Limpopo": "LP"}
PROV_ORDER = ["WC", "EC", "NC", "FS", "KZN", "NW", "GP", "MP", "LP"]
SRC_LBL = "NIDS source (weighted)"
AGT_LBL = "Agent population (unweighted)"

src = pd.read_parquet(PROC / "synthetic_population_matched.parquet")
agt = pd.read_parquet(PROC / "synthetic_population_5000.parquet")
for frame in (src, agt):
    frame["income_quintile"] = pd.Categorical(frame["income_quintile"], QORDER, ordered=True)
    frame["prov"] = frame["province"].map(PROV_ABBR)
    for flag in FLAGS:
        frame[flag] = frame[flag].astype(int)
W = src.w5_wgt.values
seed = json.loads((PROC / "p3_resample_summary.json").read_text())["seed"]


def wshare(frame, w, col, cats):
    tot = w.sum()
    return np.array([w[(frame[col] == c).values].sum() / tot * 100 for c in cats])


def ushare(frame, col, cats):
    return np.array([(frame[col] == c).mean() * 100 for c in cats])


# =================================================================== figure 1
fig, axes = plt.subplots(2, 3, figsize=(TW, 5.0))
(ax_a, ax_b, ax_c), (ax_d, ax_e, ax_f) = axes
UNIT = [0, 0.25, 0.5, 0.75, 1.0]
UNIT_LBL = ["0", "", "0.5", "", "1"]

# (a) per-capita income ECDF -------------------------------------------------
# The source is drawn as a thick dark band and the agents as a thin light line inside it, so the
# two read apart by width as well as colour.
o = np.argsort(src.income_pc.values)
xs, ws = src.income_pc.values[o], W[o]
Fs = np.cumsum(ws) / ws.sum()
xa = np.sort(agt.income_pc.values)
Fa = np.arange(1, len(xa) + 1) / len(xa)
grid_x = np.union1d(xs, xa)
gaps = np.abs(np.interp(grid_x, xs, Fs) - np.interp(grid_x, xa, Fa))
ks, ks_at = gaps.max(), grid_x[gaps.argmax()]

ax_a.plot(xs, Fs, color=SRC, lw=2.8, solid_capstyle="round", label=SRC_LBL)
ax_a.plot(xa, Fa, color=AGT, lw=1.0, label=AGT_LBL)
y0, y1 = np.interp(ks_at, xs, Fs), np.interp(ks_at, xa, Fa)
ax_a.vlines(ks_at, min(y0, y1), max(y0, y1), color=INK, lw=1.0, zorder=5)
ax_a.annotate(f"KS gap {ks:.3f}", xy=(ks_at, (y0 + y1) / 2), xytext=(9, -24),
              textcoords="offset points", fontsize=8,
              arrowprops=dict(arrowstyle="-", lw=0.6, color=INK2))
ax_a.set_xscale("log")
ax_a.xaxis.set_major_locator(LogLocator(base=10, numticks=10))
ax_a.xaxis.set_minor_locator(NullLocator())
ax_a.set_xlim(max(xs.min(), 50), xs.max())
ax_a.set_ylim(0, 1.02)
ax_a.set_yticks(UNIT, UNIT_LBL)
ax_a.set_xlabel("Per-capita income\n(2017 ZAR, log scale)")
ax_a.set_ylabel("Cumulative share\nof households")
ax_a.set_title("(a) Per-capita income")
dress(ax_a)

# (b) Lorenz curve -----------------------------------------------------------
cum_p, cum_i = np.cumsum(ws) / ws.sum(), np.cumsum(xs * ws) / (xs * ws).sum()
cum_pa, cum_ia = np.arange(1, len(xa) + 1) / len(xa), np.cumsum(xa) / xa.sum()
g_src, g_agt = wgini(src.income_pc, W), wgini(agt.income_pc, np.ones(len(agt)))
ax_b.plot([0, 1], [0, 1], color=INK2, lw=0.6)
ax_b.text(0.56, 0.585, "line of equality", fontsize=8, color=INK2, rotation=45,
          rotation_mode="anchor", ha="center", va="bottom", transform_rotates_text=True)
ax_b.plot(np.r_[0, cum_p], np.r_[0, cum_i], color=SRC, lw=2.8, label=SRC_LBL)
ax_b.plot(np.r_[0, cum_pa], np.r_[0, cum_ia], color=AGT, lw=1.0, label=AGT_LBL)
ax_b.text(0.04, 0.97, f"Gini\nsource {g_src:.3f}\nagents {g_agt:.3f}",
          fontsize=8, va="top", linespacing=1.3)
ax_b.set_xlim(0, 1)
ax_b.set_ylim(0, 1)
ax_b.set_xticks(UNIT, UNIT_LBL)
ax_b.set_yticks(UNIT, UNIT_LBL)
ax_b.set_xlabel("Cumulative share\nof households")
ax_b.set_ylabel("Cumulative share of income")
ax_b.set_title("(b) Income concentration")
dress(ax_b)

# (c) quintile shares --------------------------------------------------------
q_s, q_a = wshare(src, W, "income_quintile", QORDER), ushare(agt, "income_quintile", QORDER)
grouped(ax_c, QORDER, {SRC_LBL: q_s, AGT_LBL: q_a}, [SRC, AGT])
ax_c.axhline(20, color=INK, lw=0.6, ls="--", zorder=4)
ax_c.text(4.6, 20.6, "20%", fontsize=8, ha="right", va="bottom")
ax_c.set_ylim(0, max(q_s.max(), q_a.max()) * 1.18)
ax_c.set_ylabel("Share of households (%)")
ax_c.set_title("(c) Income quintiles")
dress(ax_c)

# (d) household size ---------------------------------------------------------
src["hsz"] = np.where(src.w5_hhsizer.values >= 7, 7, src.w5_hhsizer.values).astype(int)
agt["hsz"] = np.where(agt.w5_hhsizer.values >= 7, 7, agt.w5_hhsizer.values).astype(int)
SZ = [1, 2, 3, 4, 5, 6, 7]
SZL = ["1", "2", "3", "4", "5", "6", "7+"]
s_s, s_a = wshare(src, W, "hsz", SZ), ushare(agt, "hsz", SZ)
grouped(ax_d, SZL, {SRC_LBL: s_s, AGT_LBL: s_a}, [SRC, AGT], width=0.40)
ax_d.set_ylim(0, max(s_s.max(), s_a.max()) * 1.12)
ax_d.set_xlabel("Household members")
ax_d.set_ylabel("Share of households (%)")
ax_d.set_title("(d) Household size")
dress(ax_d)

# (e) province ---------------------------------------------------------------
p_s, p_a = wshare(src, W, "prov", PROV_ORDER), ushare(agt, "prov", PROV_ORDER)
grouped(ax_e, PROV_ORDER, {SRC_LBL: p_s, AGT_LBL: p_a}, [SRC, AGT], width=0.40)
ax_e.set_ylim(0, max(p_s.max(), p_a.max()) * 1.12)
ax_e.set_ylabel("Share of households (%)")
ax_e.set_title("(e) Province")
ax_e.tick_params(axis="x", rotation=90)
dress(ax_e)

# (f) dominant income source -------------------------------------------------
ISRC = ["WAGE", "GRANT", "OTHER"]
ISRCL = ["Wage", "Grant", "Other"]
i_s, i_a = wshare(src, W, "income_source", ISRC), ushare(agt, "income_source", ISRC)
grouped(ax_f, ISRCL, {SRC_LBL: i_s, AGT_LBL: i_a}, [SRC, AGT], width=0.34)
ax_f.set_ylim(0, max(i_s.max(), i_a.max()) * 1.12)
ax_f.set_ylabel("Share of households (%)")
ax_f.set_title("(f) Income source")
dress(ax_f)

handles = [Patch(facecolor=SRC, edgecolor="none", label=SRC_LBL),
           Patch(facecolor=AGT, edgecolor="none", label=AGT_LBL)]
fig.legend(handles=handles, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.045, 1, 1), w_pad=0.8, h_pad=1.2)
save(fig, "fig_population_fidelity")
plt.close(fig)

# =================================================================== figure 2
# Cut at the backbone's own quintile bounds, so the benchmark and the population it is
# compared against are split at exactly the same per-capita income.
bounds = json.loads((PROC / "nids_backbone_summary.json").read_text())["pc_income_quintile_bounds"]
fs = load_finscope(ROOT, bounds)
FW = fs.HH_WEIGHT16.values

# Panel (a) is drawn as horizontal bars so that its rows line up with the heatmap's in (b) and
# the indicator names read horizontally, once, on the left.
fig2, (ax_g, ax_h) = plt.subplots(1, 2, figsize=(TW, 3.0), sharey=True,
                                  gridspec_kw={"width_ratios": [1.0, 1.0]})

nat_fs = np.array([np.average(fs[f], weights=FW) * 100 for f in FLAGS])
nat_src = np.array([np.average(src[f], weights=W) * 100 for f in FLAGS])
nat_agt = np.array([agt[f].mean() * 100 for f in FLAGS])
labels = [FLAG_LABEL[f] for f in FLAGS]
grouped(ax_g, labels, {"FinScope 2019 (benchmark)": nat_fs, SRC_LBL: nat_src, AGT_LBL: nat_agt},
        [BENCH_STYLE, SRC, AGT], width=0.26, gap=0.02, horizontal=True)
ax_g.set_ylim(len(FLAGS) - 0.5, -0.5)
ax_g.set_xlim(0, 100)
ax_g.set_xlabel("Share of households (%)")
ax_g.set_title("(a) National rates")
dress(ax_g, ygrid=False, xgrid=True)
ax_g.tick_params(axis="y", length=0)

dev = np.zeros((len(FLAGS), len(QORDER)))
for i, flag in enumerate(FLAGS):
    for j, q in enumerate(QORDER):
        m1 = (src.income_quintile == q).values
        m2 = (fs.income_quintile == q).values
        dev[i, j] = (np.average(src[flag][m1], weights=W[m1]) * 100
                     - np.average(fs[flag][m2], weights=FW[m2]) * 100)

# Vector cells (pcolormesh, not imshow), so the heatmap prints sharp; white rules between cells.
cmap = LinearSegmentedColormap.from_list("dev", [SRC, "#f0efec", RED])
im = ax_h.pcolormesh(np.arange(len(QORDER) + 1) - 0.5, np.arange(len(FLAGS) + 1) - 0.5, dev,
                     cmap=cmap, norm=TwoSlopeNorm(vmin=-5, vcenter=0, vmax=5),
                     edgecolors=SURF, linewidth=1.5)
for i in range(dev.shape[0]):
    for j in range(dev.shape[1]):
        ax_h.text(j, i, minus(dev[i, j]), ha="center", va="center", fontsize=8,
                  color=INK if abs(dev[i, j]) < 3.2 else SURF)
ax_h.set_xticks(range(len(QORDER)))
ax_h.set_xticklabels(QORDER)
ax_h.set_xlim(-0.5, len(QORDER) - 0.5)
for sp in ax_h.spines.values():
    sp.set_visible(False)
ax_h.tick_params(length=0)
ax_h.set_title("(b) Deviation from FinScope, by quintile")
cb = fig2.colorbar(im, ax=ax_h, fraction=0.06, pad=0.04, shrink=0.82, ticks=[-5, -2.5, 0, 2.5, 5])
cb.set_label("Synthetic minus FinScope\n(percentage points)")
cb.ax.tick_params(length=2)
cb.outline.set_visible(False)
cb.solids.set_rasterized(False)
cb.solids.set_edgecolor("face")
fig2.legend(*ax_g.get_legend_handles_labels(), loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.0),
            handlelength=1.2, columnspacing=1.0)
fig2.tight_layout(rect=(0, 0.07, 1, 1), w_pad=2.2)
save(fig2, "fig_inclusion_fidelity")
plt.close(fig2)

# ---------------------------------------------------------------- numbers
out = {
    "resample_seed": int(seed),
    "ks_gap": round(float(ks), 3),
    "gini_source_weighted": round(float(g_src), 3),
    "gini_agents_unweighted": round(float(g_agt), 3),
    "max_quintile_share_gap_pp": round(float(np.abs(q_a - q_s).max()), 2),
    "max_province_share_gap_pp": round(float(np.abs(p_a - p_s).max()), 2),
    "max_hhsize_share_gap_pp": round(float(np.abs(s_a - s_s).max()), 2),
    "max_income_source_gap_pp": round(float(np.abs(i_a - i_s).max()), 2),
    "mean_hh_size_source": round(float(np.average(src.w5_hhsizer, weights=W)), 2),
    "mean_hh_size_agents": round(float(agt.w5_hhsizer.mean()), 2),
    "national_flags_pct": {FLAG_LABEL[f]: {"finscope": round(float(nat_fs[i]), 1),
                                           "source": round(float(nat_src[i]), 1),
                                           "agents": round(float(nat_agt[i]), 1)}
                           for i, f in enumerate(FLAGS)},
    "max_abs_quintile_deviation_pp": round(float(np.abs(dev).max()), 1),
    "max_abs_agent_flag_gap_pp": round(float(np.abs(nat_agt - nat_src).max()), 2),
}
(PROC / "data_figure_numbers.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
print("\nwrote: " + ", ".join(sorted(p.name for p in FIGS.iterdir())))
