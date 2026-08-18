"""Turn raw run output into the summary tables and figures Chapter 6 requires.

Reporting rules enforced here rather than left to the writing-up:

  * Every RQ1/RQ2 result is a surface over the swept parameter AND beta, with the
    beta = 0 row always shown. That is what makes the RQ2 claim non-circular.
  * Access rates are labelled as a share of the BANKED subpopulation (82.8% ceiling),
    so they cannot be misread as a share of all households.
  * The concurrent-facility cap is labelled HYPOTHETICAL wherever it appears.
  * Dispersion is shown, not just means.

Usage:
    python -m simulation.analysis
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .config import RESULTS_RAW, RESULTS_SUMMARY, load_ccmr_target

FIGDIR = RESULTS_SUMMARY / "figures"

#: Stated wherever an access rate is reported (D11).
BANKED_CEILING = 0.828


def load(name: str) -> pd.DataFrame | None:
    path = RESULTS_RAW / f"{name}.parquet"
    if not path.exists():
        print(f"  (skipping {name}: not found)")
        return None
    return pd.read_parquet(path)


def agg(df: pd.DataFrame, by: list[str], cols: list[str]) -> pd.DataFrame:
    out = df.groupby(by, as_index=False)[cols].agg(["mean", "std"])
    out.columns = ["_".join(c).rstrip("_") for c in out.columns.to_flat_index()]
    return out.reset_index() if out.index.name else out


# ---------------------------------------------------------------------------
def baseline_and_pattern1() -> None:
    """Baseline calibration and the deHaan complementarity test (pattern 1)."""
    df = load("rq0")
    if df is None:
        return
    ccmr = load_ccmr_target()

    cols = [
        "active_current_mean",
        "active_d30_mean",
        "active_60_plus_mean",
        "active_90_plus_mean",
        "default_rate_final",
        "trad_arrears_rate_mean",
        "trad_interest_total",
        "bnpl_adoption_final",
        "zero_savings_rate_mean",
    ]
    t = df.groupby("label")[cols].agg(["mean", "std"])
    t.to_csv(RESULTS_SUMMARY / "rq0_baseline.csv")

    off = df[df.label == "baseline_no_bnpl"]
    print("\n=== BASELINE vs CCMR 2017 (credit-active denominator) ===")
    print(f"  current : {off.active_current_mean.mean():.2%}   CCMR {ccmr['pct_current']:.2f}%")
    print(f"  60+     : {off.active_60_plus_mean.mean():.2%}   CCMR {ccmr['pct_60_plus']:.2f}%  [UNFITTED]")
    print(f"  90+     : {off.active_90_plus_mean.mean():.2%}   CCMR {ccmr['pct_90_plus']:.2f}%  [FITTED]")

    print("\n=== PATTERN 1 (deHaan): enabling BNPL must RAISE traditional stress ===")
    print("  Direction is partly designed in via the want-driven trigger; the MAGNITUDE is not.")
    for arm in ("bnpl_on_beta0", "bnpl_on_beta1"):
        on = df[df.label == arm]
        if on.empty:
            continue
        d_arr = on.trad_arrears_rate_mean.mean() - off.trad_arrears_rate_mean.mean()
        d_int = on.trad_interest_total.mean() / max(off.trad_interest_total.mean(), 1e-9) - 1
        verdict = "COMPLEMENTARITY (consistent)" if d_arr > 0 else "SUBSTITUTION (falsifies D5)"
        print(
            f"  {arm:16} arrears {d_arr:+.2%}pp | interest {d_int:+.2%} | {verdict}"
        )

    print("\n=== PATTERN 3 (Hamill): aggregate debt/income by quintile ===")
    print("  PRE-REGISTERED primary statistic: total debt / total income per quintile.")
    for pref, name in (("dti_", "aggregate (PRIMARY)"), ("dti_mean_", "mean (secondary)")):
        v = {q: off[f"{pref}{q}"].mean() for q in ("Q1", "Q2", "Q3", "Q4", "Q5")}
        peak = max(v, key=v.get)
        held = "MIDDLE-INCOME PEAK" if peak in ("Q2", "Q3", "Q4") else f"peak {peak}"
        print(f"  {name:22} " + "  ".join(f"{k} {x:5.3f}" for k, x in v.items()) + f"  -> {held}")

    print("\n=== PATTERN 4 (TransUnion 36%): savings exhaustion ===")
    print(f"  zero liquid savings: {off.zero_savings_rate_mean.mean():.1%}  [UNFITTED]")


def linear_departure(x, y) -> dict:
    """How far a response departs from a straight line over the swept range.

    `linear_r2` near 1 and a small `max_dev_frac` mean the response is smooth; a genuine
    tipping point shows a low R^2 and a large residual relative to the total rise. Shared
    by the linear and threshold arms so the two are judged on identical terms, which is
    the whole point of running both.
    """
    import numpy as np

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    rise = float(y[-1] - y[0])
    slope, intercept = np.polyfit(x, y, 1)
    resid = y - (slope * x + intercept)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((resid**2).sum()) / ss_tot if ss_tot > 0 else 1.0
    max_dev = float(abs(resid).max() / abs(rise)) if abs(rise) > 1e-12 else 0.0
    return {"rise": rise, "linear_r2": r2, "max_dev_frac": max_dev}


def rq2_threshold_figure() -> None:
    """RQ2 under Granovetter thresholds: does ADOPTION tip while DEFAULT does not?

    This is the arm's real purpose. The model carries peer feedback in its input
    (adoption) and none in its output (default), so the interesting comparison is not
    "did we find a threshold" but "does the cascade mechanism visibly work, and does the
    outcome move when it does". Both responses are therefore measured on the same
    linear-departure diagnostic and plotted on one figure.
    """
    df = load("rq2t")
    if df is None:
        return
    surf = df[df.label.str.startswith("rq2t_a")]
    if surf.empty:
        return
    g = agg(
        surf,
        ["bnpl_access_rate", "sigma_theta", "gamma"],
        ["default_rate_final", "bnpl_adoption_final", "threshold_triggered_final"],
    )
    g.to_csv(RESULTS_SUMMARY / "rq2_threshold_surface.csv", index=False)

    live = g[g.gamma > 0]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), sharex=True)
    for s, sub in live.groupby("sigma_theta"):
        sub = sub.sort_values("bnpl_access_rate")
        axes[0].plot(sub.bnpl_access_rate, sub.bnpl_adoption_final_mean, marker="o",
                     label=f"sigma = {s:g}")
        axes[1].plot(sub.bnpl_access_rate, sub.default_rate_final_mean, marker="o",
                     label=f"sigma = {s:g}")
    ctrl = g[g.gamma == 0].groupby("bnpl_access_rate", as_index=False).mean(numeric_only=True)
    if not ctrl.empty:
        ctrl = ctrl.sort_values("bnpl_access_rate")
        for ax, col in zip(axes, ("bnpl_adoption_final_mean", "default_rate_final_mean")):
            ax.plot(ctrl.bnpl_access_rate, ctrl[col], color="black", lw=2.5, marker="s",
                    zorder=5, label="gamma = 0  (control arm)")
    axes[0].set_title("ADOPTION: does the cascade fire?")
    axes[0].set_ylabel("BNPL adoption rate")
    axes[1].set_title("DEFAULT: does the outcome follow?")
    axes[1].set_ylabel("Population default rate")
    for ax in axes:
        ax.set_xlabel("BNPL access rate (share of the banked subpopulation)")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle(
        "RQ2, Granovetter heterogeneous thresholds: adoption tipping vs distress tipping",
        fontsize=11,
    )
    fig.tight_layout()
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGDIR / "rq2_threshold_adoption_vs_default.png", dpi=200)
    plt.close(fig)

    print("\n=== RQ2 THRESHOLD ARM (pre-registered D17 alternative) ===")
    print("  Granovetter's claim is about the VARIANCE of thresholds, so sigma is the axis.")
    print("  Both responses get the SAME diagnostic, because the question is whether")
    print("  adoption and default behave differently, not whether either is non-linear.")
    rows = []
    for (s, gam), sub in g.groupby(["sigma_theta", "gamma"]):
        sub = sub.sort_values("bnpl_access_rate")
        d = linear_departure(sub.bnpl_access_rate, sub.default_rate_final_mean)
        a = linear_departure(sub.bnpl_access_rate, sub.bnpl_adoption_final_mean)
        rows.append({"sigma_theta": s, "gamma": gam,
                     **{f"default_{k}": v for k, v in d.items()},
                     **{f"adoption_{k}": v for k, v in a.items()}})
        tag = "  <- CONTROL" if gam == 0 else ""
        print(f"  sigma={s:<5g} gamma={gam:<4g} | adoption rise {a['rise']:+.2%} "
              f"R^2 {a['linear_r2']:.4f} | default rise {d['rise']:+.2%} "
              f"R^2 {d['linear_r2']:.4f}{tag}")
    pd.DataFrame(rows).to_csv(RESULTS_SUMMARY / "rq2_threshold_nonlinearity.csv", index=False)

    mu = df[df.label.str.startswith("rq2t_mu")]
    if not mu.empty:
        m = agg(mu, ["mu_theta"], ["bnpl_adoption_final", "default_rate_final"])
        print("\n  mu_theta sensitivity (secondary axis, full access, sigma=0.20):")
        for _, r in m.sort_values("mu_theta").iterrows():
            print(f"    mu={r.mu_theta:<5g} adoption {r.bnpl_adoption_final_mean:.1%}  "
                  f"default {r.default_rate_final_mean:.1%}")


def rq2_surface_figure() -> None:
    df = load("rq2")
    if df is None:
        return
    g = agg(df, ["bnpl_access_rate", "beta"], ["default_rate_final"])
    g.to_csv(RESULTS_SUMMARY / "rq2_surface.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for b, sub in g.groupby("beta"):
        sub = sub.sort_values("bnpl_access_rate")
        control = b == 0.0
        ax.errorbar(
            sub.bnpl_access_rate,
            sub.default_rate_final_mean,
            yerr=sub.default_rate_final_std,
            marker="o",
            capsize=3,
            lw=2.5 if control else 1.4,
            color="black" if control else None,
            zorder=5 if control else 2,
            label=f"beta = {b:g}" + ("  (control arm)" if control else ""),
        )
    ax.set_xlabel(
        f"BNPL access rate, as a share of the BANKED subpopulation "
        f"(ceiling {BANKED_CEILING:.1%} of all households)"
    )
    ax.set_ylabel("Population default rate")
    ax.set_title("RQ2: population default over BNPL access x peer-influence strength")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGDIR / "rq2_default_surface.png", dpi=200)
    plt.close(fig)

    print("\n=== RQ2: is the response non-linear, and only when beta > 0? ===")
    print("  Non-linearity is measured as departure from a straight line fitted over the")
    print("  access range: R^2 of the linear fit, and the largest residual expressed as a")
    print("  share of the total rise. A sharp threshold would show low R^2 and a large")
    print("  max residual. AMPLIFICATION (how far default moves) is a separate question")
    print("  from NON-LINEARITY (whether it moves smoothly), and they must not be conflated.")
    import numpy as np

    rows = []
    for b, sub in g.groupby("beta"):
        sub = sub.sort_values("bnpl_access_rate")
        x = sub.bnpl_access_rate.to_numpy(dtype=float)
        y = sub.default_rate_final_mean.to_numpy(dtype=float)
        rise = y[-1] - y[0]
        slope, intercept = np.polyfit(x, y, 1)
        resid = y - (slope * x + intercept)
        ss_res = float((resid**2).sum())
        ss_tot = float(((y - y.mean()) ** 2).sum())
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        max_dev = float(np.abs(resid).max() / abs(rise)) if abs(rise) > 1e-12 else 0.0
        rows.append(
            {"beta": b, "rise": rise, "linear_r2": r2, "max_dev_frac": max_dev}
        )
        tag = "   <- CONTROL ARM" if b == 0.0 else ""
        print(
            f"  beta={b:<4g} rise {rise:+.2%}  linear R^2 {r2:.4f}  "
            f"max deviation {max_dev:.1%} of rise{tag}"
        )
    pd.DataFrame(rows).to_csv(RESULTS_SUMMARY / "rq2_nonlinearity.csv", index=False)

    ctrl = next(r for r in rows if r["beta"] == 0.0)
    amp = max(r["rise"] for r in rows) / ctrl["rise"] if ctrl["rise"] else float("nan")
    print(f"\n  AMPLIFICATION: peer influence multiplies the access response by {amp:.1f}x")
    if all(r["linear_r2"] > 0.95 for r in rows):
        print("  NON-LINEARITY: every arm is near-linear (R^2 > 0.95), INCLUDING beta = 0.")
        print("  The conditional claim 'non-linear ONLY where social transmission is present'")
        print("  is therefore NOT supported. Report the amplification result instead, and run")
        print("  the Granovetter heterogeneous-threshold variant pre-registered in D17 as the")
        print("  structural robustness check before concluding no threshold exists.")


def rq1_stacking_figure() -> None:
    df = load("rq1")
    if df is None:
        return
    g = agg(
        df,
        ["n_platforms", "beta"],
        ["stacking_mean_final", "stacking_2plus_final", "default_rate_final",
         "trad_arrears_rate_mean"],
    )
    g.to_csv(RESULTS_SUMMARY / "rq1_stacking.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for b, sub in g.groupby("beta"):
        sub = sub.sort_values("n_platforms")
        control = b == 0.0
        ax.errorbar(
            sub.n_platforms,
            sub.stacking_2plus_final_mean,
            yerr=sub.stacking_2plus_final_std,
            marker="s",
            capsize=3,
            lw=2.5 if control else 1.4,
            color="black" if control else None,
            label=f"beta = {b:g}" + ("  (control arm)" if control else ""),
        )
    # CFPB order-of-magnitude check: 32% of BNPL borrowers held loans across firms.
    ax.axhline(0.32, ls="--", c="crimson", lw=1)
    ax.text(1.05, 0.325, "CFPB 32% cross-firm (US, order-of-magnitude)", fontsize=7, c="crimson")
    ax.set_xlabel("Number of BNPL platforms (N=1 isolates single-platform accumulation)")
    ax.set_ylabel("Share of households holding 2+ concurrent facilities")
    ax.set_title("RQ1: emergent cross-platform stacking")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGDIR / "rq1_stacking.png", dpi=200)
    plt.close(fig)


def rq3_interventions_table() -> None:
    df = load("rq3")
    if df is None:
        return
    cols = ["default_rate_final", "bnpl_volume_cumulative", "trad_arrears_rate_mean"]
    g = agg(df, ["label", "beta"], cols)
    g.to_csv(RESULTS_SUMMARY / "rq3_interventions.csv", index=False)

    print("\n=== RQ3: defer vs desist, measured as CUMULATIVE BNPL VOLUME ===")
    base = g[g.label.str.startswith("rq3_kcool0")]
    for b in sorted(df.beta.unique()):
        ref = base[base.beta == b]
        if ref.empty:
            continue
        v0 = ref.bnpl_volume_cumulative_mean.iloc[0]
        print(f"  beta = {b:g}   (no-lever cumulative volume = R{v0:,.0f})")
        sub = g[(g.beta == b) & (g.label != f"rq3_kcool0_b{b}")].sort_values(
            "default_rate_final_mean"
        )
        for _, r in sub.iterrows():
            dv = r.bnpl_volume_cumulative_mean / v0 - 1 if v0 else 0.0
            verdict = "DESIST" if dv < -0.05 else "DEFER (volume ~unchanged)"
            hyp = "  [HYPOTHETICAL LEVER]" if "cap" in r.label else ""
            print(
                f"    {r.label:22} default {r.default_rate_final_mean:.2%}"
                f"  volume {dv:+.1%}  {verdict}{hyp}"
            )


def robustness_table() -> None:
    df = load("robustness")
    if df is None:
        return
    g = agg(df, ["label"], ["default_rate_final", "active_90_plus_mean", "bnpl_adoption_final"])
    g.to_csv(RESULTS_SUMMARY / "robustness.csv", index=False)
    print("\n=== ROBUSTNESS (default rate; mandatory arms marked) ===")
    mandatory = ("rob_amount", "rob_minpay", "rob_act")
    for _, r in g.sort_values("label").iterrows():
        flag = "  [MANDATORY]" if r.label.startswith(mandatory) else ""
        print(
            f"  {r.label:28} {r.default_rate_final_mean:.2%} "
            f"(sd {r.default_rate_final_std:.4f}){flag}"
        )


def fig_arrears_profile() -> None:
    """Model arrears profile against the CCMR 2017 age analysis, band by band."""
    df = load("rq0")
    if df is None:
        return
    import json

    from .config import CCMR_BASELINE

    ccmr = json.loads(CCMR_BASELINE.read_text(encoding="utf-8"))
    pct = ccmr["combined_unsecured_and_facilities"]["pct"]

    off = df[df.label == "baseline_no_bnpl"]
    bands = ["current", "d30", "d31_60", "d61_90", "d91_120", "d120_plus"]
    labels = ["current", "1-30 d", "31-60 d", "61-90 d", "91-120 d", "120+ d"]
    model = [
        off["active_current_mean"].mean() * 100,
        off["active_d30_mean"].mean() * 100,
        off["active_d31_60_mean"].mean() * 100,
        off["active_d61_90_mean"].mean() * 100,
        off["active_90_plus_mean"].mean() * 100 - off["active_d120_plus_mean"].mean() * 100,
        off["active_d120_plus_mean"].mean() * 100,
    ]
    target = [pct[b] for b in bands]

    x = range(len(bands))
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar([i - 0.2 for i in x], model, width=0.4, label="Model (credit-active)")
    ax.bar([i + 0.2 for i in x], target, width=0.4, label="NCR CCMR 2017-Q1 (accounts)")
    # Mark which bands were fitted; the rest are independent checks.
    for i, b in enumerate(bands):
        if b in ("d30",) or b in ("d91_120", "d120_plus"):
            ax.text(i, max(model[i], target[i]) + 1.5, "FITTED", ha="center", fontsize=7,
                    color="crimson")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Share of accounts / credit-active households (%)")
    ax.set_title("Baseline arrears profile vs CCMR 2017 (unit mismatch: accounts vs households)")
    ax.legend()
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(FIGDIR / "baseline_arrears_profile.png", dpi=200)
    plt.close(fig)


def fig_pattern3() -> None:
    """Pattern 3 under all three statistics, showing the verdict is statistic-dependent."""
    df = load("rq0")
    if df is None:
        return
    off = df[df.label == "baseline_no_bnpl"]
    Q = ["Q1", "Q2", "Q3", "Q4", "Q5"]

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    specs = [
        ("dti_", "AGGREGATE (pre-registered primary)", "tab:blue"),
        ("dti_mean_", "mean of ratios (secondary)", "tab:orange"),
        ("dti_median_", "median, debtors (secondary)", "tab:green"),
    ]
    for ax, (pref, title, c) in zip(axes, specs):
        vals = [off[f"{pref}{q}"].mean() for q in Q]
        peak = Q[vals.index(max(vals))]
        ax.bar(Q, vals, color=c)
        ax.set_title(f"{title}\npeak {peak}", fontsize=9)
        ax.set_ylabel("debt / monthly income")
        ax.grid(alpha=0.3, axis="y")
    fig.suptitle(
        "Pattern 3 (Hamill): the verdict depends on the statistic. "
        "Aggregate gives a middle-income peak; a mean of ratios does not.",
        fontsize=10,
    )
    fig.tight_layout()
    fig.savefig(FIGDIR / "pattern3_dti_by_quintile.png", dpi=200)
    plt.close(fig)


def fig_rq3_interventions() -> None:
    """Intervention ranking, and the defer-vs-desist volume test."""
    df = load("rq3")
    if df is None:
        return
    for beta in sorted(df.beta.unique()):
        sub = df[df.beta == beta]
        g = sub.groupby("label", as_index=False).agg(
            d=("default_rate_final", "mean"),
            dsd=("default_rate_final", "std"),
            v=("bnpl_volume_cumulative", "mean"),
        )
        ref = g[g.label == f"rq3_kcool0_b{beta}"]
        if ref.empty:
            continue
        v0 = ref.v.iloc[0]
        g = g[g.label != f"rq3_kcool0_b{beta}"].sort_values("d")
        g["dv"] = g.v / v0 - 1

        fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6))
        colors = ["crimson" if "cap" in l else "tab:blue" for l in g.label]
        a1.barh(g.label, g.d * 100, xerr=g.dsd * 100, color=colors)
        a1.axvline(ref.d.iloc[0] * 100, ls="--", c="k", lw=1)
        a1.text(ref.d.iloc[0] * 100, -0.6, " no lever", fontsize=7)
        a1.set_xlabel("Population default rate (%)")
        a1.set_title(f"Intervention ranking, beta = {beta:g}\nred = HYPOTHETICAL lever", fontsize=9)
        a1.grid(alpha=0.3, axis="x")

        a2.barh(g.label, g.dv * 100, color=colors)
        a2.axvline(-5, ls=":", c="grey", lw=1)
        a2.set_xlabel("Change in cumulative BNPL volume (%)")
        a2.set_title("Defer vs desist: volume over the full horizon\n"
                     "(left of the dotted line = desist)", fontsize=9)
        a2.grid(alpha=0.3, axis="x")
        fig.tight_layout()
        fig.savefig(FIGDIR / f"rq3_interventions_beta{beta:g}.png", dpi=200)
        plt.close(fig)


def fig_robustness_tornado() -> None:
    """Which parameters actually move the answer, ranked."""
    df = load("robustness")
    if df is None:
        return
    g = df.groupby("label", as_index=False)["default_rate_final"].mean()

    # Labels carry the PROVENANCE, because the point of this figure is which parameters
    # move the answer AND how well each is grounded. Both BNPL parameters changed
    # character on 2026-08-12: they were a flat trade-press purchase size and a flat
    # unsourceable platform limit, and they are now ratios applied to household
    # characteristics (DEFECTS.md B30). Whether they still top the ranking is an open
    # question this figure answers.
    groups = {
        "BNPL purchase size, kappa (IES-derived)": "rob_kappa",
        "BNPL purchase base (discretionary vs income)": "rob_base",
        "Rolling limit, lambda (band-reported)": "rob_limit",
        "Amount rule (uncited, D4)": "rob_amount",
        "Default horizon k": "rob_k",
        "Population size": "rob_n",
        "Min-payer share (D6)": "rob_m0",
        "Min-payment formula (uncited)": "rob_minpay",
        "Activation order (D16)": "rob_act",
    }
    rows = []
    for name, prefix in groups.items():
        sub = g[g.label.str.startswith(prefix)]
        if len(sub) < 2:
            continue
        rows.append((name, (sub.default_rate_final.max() - sub.default_rate_final.min()) * 100))
    rows.sort(key=lambda r: r[1])

    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    colors = ["crimson" if "uncited" in n else "tab:blue" for n, _ in rows]
    ax.barh([r[0] for r in rows], [r[1] for r in rows], color=colors)
    ax.set_xlabel("Range of population default rate across the swept values (pp)")
    ax.set_title("Robustness: what actually moves the answer\n"
                 "red = the rule has no citation", fontsize=10)
    ax.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(FIGDIR / "robustness_tornado.png", dpi=200)
    plt.close(fig)


def fig_sobol() -> None:
    """Sobol total-order indices, with the interaction share separated."""
    path = RESULTS_SUMMARY / "sobol_indices.json"
    if not path.exists():
        print("  (skipping sobol figure: not found)")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    idx = data["indices"].get("default_rate_final")
    if not idx:
        return
    t = pd.DataFrame(idx).sort_values("ST")

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.barh(t.parameter, t.S1.clip(lower=0), label="S1 (on its own)")
    ax.barh(
        t.parameter,
        (t.ST - t.S1).clip(lower=0),
        left=t.S1.clip(lower=0),
        label="interaction (ST - S1)",
    )
    ax.set_xlabel("Share of variance in the population default rate")
    ax.set_title(
        f"Sobol decomposition (N={data['n_base_samples']}, "
        f"{data['n_design_points']} design points)\n"
        "wide CIs at this sample size - re-run at N>=256 before quoting",
        fontsize=10,
    )
    ax.legend()
    ax.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(FIGDIR / "sobol_default_rate.png", dpi=200)
    plt.close(fig)


def main() -> None:
    RESULTS_SUMMARY.mkdir(parents=True, exist_ok=True)
    FIGDIR.mkdir(parents=True, exist_ok=True)
    baseline_and_pattern1()
    rq1_stacking_figure()
    rq2_surface_figure()
    rq2_threshold_figure()
    rq3_interventions_table()
    robustness_table()
    # Figures for Chapter 6.
    fig_arrears_profile()
    fig_pattern3()
    fig_rq3_interventions()
    fig_robustness_tornado()
    fig_sobol()
    print(f"\nfigures -> {FIGDIR}")
    for p in sorted(FIGDIR.glob("*.png")):
        print(f"  {p.name}")


if __name__ == "__main__":
    main()
