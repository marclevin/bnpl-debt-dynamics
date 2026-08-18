"""Figures for the data chapter: does the 5,000-agent population reproduce its sources?

Two outputs, written to thesis/figures as vector PDF (plus PNG for preview):
  fig_population_fidelity.pdf  - agents (unweighted) vs NIDS source (weighted), six key distributions
  fig_inclusion_fidelity.pdf   - imputed FinScope flags, nationally and by quintile

Palette: categorical slots 1/2/3 of the validated default (blue, orange, aqua),
checked with the dataviz validator on the light surface (all-pairs PASS).
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data/processed"
FIGS = ROOT / "thesis/figures"
FIGS.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
SRC = "#2a78d6"     # slot 1 - weighted survey source
AGT = "#eb6834"     # slot 2 - unweighted 5,000 agents
BENCH = "#1baf7a"   # slot 3 - FinScope 2019 benchmark
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8983"
GRID, RULE, SURF = "#e6e5e2", "#b9b8b3", "#ffffff"

# The figures are drawn at the compiled text width (5.78 in) and included at
# width=\textwidth, so nothing is rescaled and these point sizes are the printed ones.
TW = 5.78

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "font.size": 7.6, "axes.titlesize": 8.4, "axes.labelsize": 7.4,
    "xtick.labelsize": 7.0, "ytick.labelsize": 7.0, "legend.fontsize": 7.4,
    "axes.titleweight": "bold", "axes.titlepad": 5,
    "axes.edgecolor": RULE, "axes.linewidth": 0.7,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
    "text.color": INK, "axes.labelcolor": INK2,
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "savefig.facecolor": SURF, "pdf.fonttype": 42,
})


def dress(ax, ygrid=True):
    """Recessive chrome: hairline solid grid, no top/right spines."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_axisbelow(True)
    if ygrid:
        ax.yaxis.grid(True, color=GRID, linewidth=0.6, linestyle="-")
    ax.tick_params(length=2.5)


def grouped(ax, cats, series, colors, width=0.38, gap=0.02):
    """Grouped bars, separated by a surface-coloured gap rather than a border."""
    x = np.arange(len(cats))
    k = len(series)
    for i, ((label, vals), colour) in enumerate(zip(series.items(), colors)):
        off = (i - (k - 1) / 2) * (width + gap)
        ax.bar(x + off, vals, width, label=label, color=colour,
               edgecolor=SURF, linewidth=0.8, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    return x


def wgini(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    o = np.argsort(x)
    x, w = x[o], w[o]
    cw, cxw = np.cumsum(w), np.cumsum(x * w)
    return 1 - np.sum((cxw[1:] + cxw[:-1]) * np.diff(cw)) / (cxw[-1] * cw[-1])


# ---------------------------------------------------------------- data
QORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]
FLAGS = ["banked", "credit_access_formal", "savings_product", "informal_finance"]
FLAG_LABEL = {"banked": "Banked", "credit_access_formal": "Formal credit",
              "savings_product": "Savings product", "informal_finance": "Informal finance"}
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
fig, axes = plt.subplots(2, 3, figsize=(TW, 4.55))
(ax_a, ax_b, ax_c), (ax_d, ax_e, ax_f) = axes

# (a) per-capita income ECDF -------------------------------------------------
o = np.argsort(src.income_pc.values)
xs, ws = src.income_pc.values[o], W[o]
Fs = np.cumsum(ws) / ws.sum()
xa = np.sort(agt.income_pc.values)
Fa = np.arange(1, len(xa) + 1) / len(xa)
grid_x = np.union1d(xs, xa)
gaps = np.abs(np.interp(grid_x, xs, Fs) - np.interp(grid_x, xa, Fa))
ks, ks_at = gaps.max(), grid_x[gaps.argmax()]

ax_a.plot(xs, Fs, color=SRC, lw=2.6, alpha=0.85, solid_capstyle="round", label=SRC_LBL)
ax_a.plot(xa, Fa, color=AGT, lw=1.0, label=AGT_LBL)
y0, y1 = np.interp(ks_at, xs, Fs), np.interp(ks_at, xa, Fa)
ax_a.vlines(ks_at, min(y0, y1), max(y0, y1), color=INK, lw=1.0, zorder=5)
ax_a.annotate(f"KS gap {ks:.3f}", xy=(ks_at, (y0 + y1) / 2), xytext=(8, -22),
              textcoords="offset points", fontsize=6.9, color=INK2,
              arrowprops=dict(arrowstyle="-", lw=0.6, color=INK3))
ax_a.set_xscale("log")
ax_a.set_xlim(max(xs.min(), 50), xs.max())
ax_a.set_ylim(0, 1.02)
ax_a.set_xlabel("Per-capita income (2017 ZAR, log)")
ax_a.set_ylabel("Cumulative share of households")
ax_a.set_title("(a) Per-capita income")
dress(ax_a)

# (b) Lorenz curve -----------------------------------------------------------
cum_p, cum_i = np.cumsum(ws) / ws.sum(), np.cumsum(xs * ws) / (xs * ws).sum()
cum_pa, cum_ia = np.arange(1, len(xa) + 1) / len(xa), np.cumsum(xa) / xa.sum()
g_src, g_agt = wgini(src.income_pc, W), wgini(agt.income_pc, np.ones(len(agt)))
ax_b.plot([0, 1], [0, 1], color=INK3, lw=0.8)
ax_b.text(0.52, 0.555, "line of equality", fontsize=6.4, color=INK3, rotation=41,
          rotation_mode="anchor", ha="center", va="bottom")
ax_b.plot(np.r_[0, cum_p], np.r_[0, cum_i], color=SRC, lw=2.6, alpha=0.85, label=SRC_LBL)
ax_b.plot(np.r_[0, cum_pa], np.r_[0, cum_ia], color=AGT, lw=1.0, label=AGT_LBL)
ax_b.text(0.04, 0.97, f"Gini\nsource {g_src:.3f}\nagents {g_agt:.3f}",
          fontsize=6.9, color=INK2, va="top", linespacing=1.5)
ax_b.set_xlim(0, 1)
ax_b.set_ylim(0, 1)
ax_b.set_xlabel("Cumulative share of households")
ax_b.set_ylabel("Cumulative share of income")
ax_b.set_title("(b) Income concentration")
dress(ax_b)

# (c) quintile shares --------------------------------------------------------
q_s, q_a = wshare(src, W, "income_quintile", QORDER), ushare(agt, "income_quintile", QORDER)
grouped(ax_c, QORDER, {SRC_LBL: q_s, AGT_LBL: q_a}, [SRC, AGT])
ax_c.axhline(20, color=INK3, lw=0.8, zorder=4)
ax_c.text(4.45, 20.9, "20%", fontsize=6.4, color=INK3, ha="right")
ax_c.set_ylim(0, 26)
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
ax_d.set_ylim(0, max(s_s.max(), s_a.max()) * 1.18)
ax_d.set_xlabel("Household members")
ax_d.set_ylabel("Share of households (%)")
ax_d.set_title("(d) Household size")
dress(ax_d)

# (e) province ---------------------------------------------------------------
p_s, p_a = wshare(src, W, "prov", PROV_ORDER), ushare(agt, "prov", PROV_ORDER)
grouped(ax_e, PROV_ORDER, {SRC_LBL: p_s, AGT_LBL: p_a}, [SRC, AGT], width=0.40)
ax_e.set_ylim(0, max(p_s.max(), p_a.max()) * 1.20)
ax_e.set_ylabel("Share of households (%)")
ax_e.set_title("(e) Province")
ax_e.tick_params(axis="x", labelsize=6.4, pad=2)
for t in ax_e.get_xticklabels():
    t.set_rotation(90)
    t.set_va("top")
dress(ax_e)

# (f) dominant income source -------------------------------------------------
ISRC = ["WAGE", "GRANT", "OTHER"]
ISRCL = ["Wage", "Grant", "Other"]
i_s, i_a = wshare(src, W, "income_source", ISRC), ushare(agt, "income_source", ISRC)
grouped(ax_f, ISRCL, {SRC_LBL: i_s, AGT_LBL: i_a}, [SRC, AGT], width=0.34)
ax_f.set_ylim(0, max(i_s.max(), i_a.max()) * 1.20)
ax_f.set_ylabel("Share of households (%)")
ax_f.set_title("(f) Income source")
dress(ax_f)

handles = [Patch(facecolor=SRC, edgecolor="none", label=SRC_LBL),
           Patch(facecolor=AGT, edgecolor="none", label=AGT_LBL)]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
           bbox_to_anchor=(0.5, 0.002), handlelength=1.9, columnspacing=2.2)
fig.tight_layout(rect=(0, 0.055, 1, 1), w_pad=1.5, h_pad=1.9)
fig.savefig(FIGS / "fig_population_fidelity.pdf")
fig.savefig(FIGS / "fig_population_fidelity.png", dpi=300)
plt.close(fig)

# =================================================================== figure 2
fs = pd.read_csv(ROOT / "data/raw/FINMARK_2019/Finscope South Africa 2019.csv",
                 usecols=["HH_WEIGHT16", "Number_in_HH", "M13_MHI_Imputed",
                          "F1", "G5", "K7", "G10", "G11", "G12", "G13", "G14"])
fs = fs[fs.HH_WEIGHT16 > 0].copy()
MID = {"No Income": 0, "R1 - R999": 500, "R1 000 - R2 999": 2000, "R3 000 - R7 999": 5500,
       "R8 000 - R11 999": 10000, "R12 000 - R29 999": 21000, "R30 000 or more": 40000}
fs["pc"] = fs.M13_MHI_Imputed.map(MID) / pd.to_numeric(fs.Number_in_HH, errors="coerce").replace(0, np.nan)
fs = fs.dropna(subset=["pc"])
BOUNDS = [900.0, 1801.42, 3400.0, 7712.14]
fs["income_quintile"] = pd.cut(fs.pc, [-np.inf] + BOUNDS + [np.inf], labels=QORDER, include_lowest=True)
FORMAL = ["Bank", "Retail store (e.g. Woolworths, Edgars etc)",
          "Micro finance institution e.g. Wonga", "Insurance company"]
fs["banked"] = (fs.F1 == "Yes").astype(int)
fs["credit_access_formal"] = (fs.G5.isin(FORMAL)
                              | (fs[["G10", "G11", "G12", "G13", "G14"]] == "Yes").any(axis=1)).astype(int)
fs["savings_product"] = fs.K7.astype(str).str.strip().str.startswith("R").astype(int)
fs["informal_finance"] = fs.G5.isin([
    "Mashonisa or loan shark",
    "Stokvel society, burial society, umgalelo or savings club",
    "Friends or family or household member", "Colleagues or neighbours",
    "Employer including getting an advance on your salary"]).astype(int)
FW = fs.HH_WEIGHT16.values

fig2, (ax_g, ax_h) = plt.subplots(1, 2, figsize=(TW, 2.75),
                                  gridspec_kw={"width_ratios": [1.10, 1.0]})

nat_fs = np.array([np.average(fs[f], weights=FW) * 100 for f in FLAGS])
nat_src = np.array([np.average(src[f], weights=W) * 100 for f in FLAGS])
nat_agt = np.array([agt[f].mean() * 100 for f in FLAGS])
labels = [FLAG_LABEL[f] for f in FLAGS]
wrapped = ["Banked", "Formal\ncredit", "Savings\nproduct", "Informal\nfinance"]
grouped(ax_g, wrapped, {"FinScope 2019 (benchmark)": nat_fs, SRC_LBL: nat_src, AGT_LBL: nat_agt},
        [BENCH, SRC, AGT], width=0.26, gap=0.015)
ax_g.set_ylim(0, 104)
ax_g.set_ylabel("Share of households (%)")
ax_g.set_title("(a) National inclusion rates")
dress(ax_g)
ax_g.legend(frameon=False, fontsize=6.4, loc="upper right", handlelength=1.2,
            borderpad=0.1, labelspacing=0.35, handletextpad=0.5)

dev = np.zeros((len(FLAGS), len(QORDER)))
for i, flag in enumerate(FLAGS):
    for j, q in enumerate(QORDER):
        m1 = (src.income_quintile == q).values
        m2 = (fs.income_quintile == q).values
        dev[i, j] = (np.average(src[flag][m1], weights=W[m1]) * 100
                     - np.average(fs[flag][m2], weights=FW[m2]) * 100)

cmap = LinearSegmentedColormap.from_list("dev", [SRC, "#f0efec", "#e34948"])
im = ax_h.imshow(dev, cmap=cmap, norm=TwoSlopeNorm(vmin=-5, vcenter=0, vmax=5), aspect="auto")
for i in range(dev.shape[0]):
    for j in range(dev.shape[1]):
        ax_h.text(j, i, f"{dev[i, j]:+.1f}", ha="center", va="center", fontsize=6.6,
                  color=INK if abs(dev[i, j]) < 3.2 else SURF)
ax_h.set_xticks(range(len(QORDER)))
ax_h.set_xticklabels(QORDER)
ax_h.set_yticks(range(len(FLAGS)))
ax_h.set_yticklabels(labels)
ax_h.set_xticks(np.arange(-0.5, len(QORDER), 1), minor=True)
ax_h.set_yticks(np.arange(-0.5, len(FLAGS), 1), minor=True)
ax_h.grid(which="minor", color=SURF, linewidth=1.6)
ax_h.tick_params(which="minor", length=0)
for s in ax_h.spines.values():
    s.set_visible(False)
ax_h.tick_params(length=0)
ax_h.set_title("(b) Deviation from FinScope, by quintile")
cb = fig2.colorbar(im, ax=ax_h, fraction=0.045, pad=0.03, ticks=[-5, -2.5, 0, 2.5, 5])
cb.set_label("Percentage points (synthetic minus FinScope)", fontsize=6.4)
cb.ax.tick_params(labelsize=6.2, length=2)
cb.outline.set_visible(False)
fig2.tight_layout(w_pad=1.8)
fig2.savefig(FIGS / "fig_inclusion_fidelity.pdf")
fig2.savefig(FIGS / "fig_inclusion_fidelity.png", dpi=300)
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
