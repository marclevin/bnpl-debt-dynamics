"""Milestone 2 (#97 to #99): the BNPL effect over beta, and the pre-registered linearity verdict.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/beta_sweep_analysis.py

Reads results/raw/rqb.parquet (suite `rqb`, 250 replicates per arm, seeds 90,000 onwards)
and writes results/summary/beta_sweep.json.

The test was fixed before the sweep ran (issue #97, signed off 2026-11-09):
  * outcome: the BNPL effect on default, default with BNPL at each beta less default without
    it, paired by seed (default during the run; the initial stock is common to both arms);
  * fits: weighted least squares, weights 1 / SE^2, of the effect on beta: linear, quadratic,
    and piecewise linear with one hinge at beta = 0.10;
  * standard errors of the fits (QA 2026-11-10): the eight effects share one no-BNPL arm and one
    seed block, so they are correlated (about 0.5). The weights stay as fixed, but every standard
    error, of the coefficients, the fitted values and the non-linear less linear differences, uses
    the full covariance of the eight mean effects estimated across seeds (a sandwich, equivalent
    to clustering on the seed). Until 2026-11-10 they assumed the eight were independent, which
    put the shared arm's noise into the slope (0.014 per 0.1 against 0.010) and shrank the extra
    terms' t-values (quadratic 0.81 against 1.23, hinge 0.23 against 0.34); the verdict is unchanged;
  * "non-linear" only if (1) the quadratic or hinge term is more than 2 SE from zero AND
    (2) at some grid point the non-linear and linear fits differ by more than 2 SE of that
    difference and by enough to change a conclusion (detectable against not, or the sign);
  * otherwise "linear": the headline is the beta = 0 effect with its SD and SE, and beta > 0
    gets a slope +/- SE per 0.1 of beta;
  * X is the largest grid beta at which annual volume per eligible household is at or below
    the top of the provider range (R4,261), capped at 0.30.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw" / "rqb.parquet"
OUT = ROOT / "results" / "summary" / "beta_sweep.json"
VOLUME_TOP = 4261.0
VOLUME_BOTTOM = 1333.0
CFPB_STACKING = (0.32, 0.33)
Q_BASE = 0.05
HINGE = 0.10


def paired(on: pd.DataFrame, off: pd.DataFrame, col: str) -> tuple[float, float, float]:
    """Mean, SE and SD of the seed-paired difference, in percentage points."""
    z = (on.set_index("seed")[col] - off.set_index("seed")[col]).dropna() * 100
    return float(z.mean()), float(z.std(ddof=1) / np.sqrt(len(z))), float(z.std(ddof=1))


def wls(X: np.ndarray, y: np.ndarray, var: np.ndarray, C: np.ndarray):
    """WLS with weights 1/var, and the covariance of the estimate under the true covariance C of y.

    Returns coefficients, their sandwich covariance A C A', the same under independence (the
    pre-2026-11-10 standard errors, kept for the record), and the hat map.
    """
    W = np.diag(1.0 / var)
    bread = np.linalg.inv(X.T @ W @ X)
    A = bread @ X.T @ W
    return A @ y, A @ C @ A.T, bread, X @ A


TABLE = ROOT / "thesis" / "chapters" / "generated" / "tab_beta.tex"


def write_table(t: pd.DataFrame, res: dict, verdicts: dict, payload: dict) -> None:
    """Table `tab:beta` (#100): the effect at each beta, and the pre-registered verdict."""
    def money(x: float) -> str:
        return f"{x:,.0f}".replace(",", "{,}")

    lin = payload["headline_linear"]
    rows = []
    for r in t.itertuples():
        bold = abs(r.effect_pp) > 2 * r.effect_se
        cell = f"{r.effect_pp:+.2f} \\pm {r.effect_se:.2f}"
        cell = f"$\\boldsymbol{{{cell}}}$" if bold else f"${cell}$"
        rows.append(
            f"{r.beta:g} & {cell} & {r.effect_sd:.2f} & {r.default_rate * 100:.2f} & "
            f"{money(r.volume_per_eligible_year)} & {r.stacking_ever_holders * 100:.1f} & "
            f"{r.adoption_final * 100:.1f} \\\\"
        )
    note = (
        "Effect: default with \\ac{BNPL} less default without, paired by seed, 250 replicates per "
        "value of $\\beta$ against one no-\\ac{BNPL} arm (seeds 90{,}000--90{,}249); SD: its replicate "
        "standard deviation. Default: with \\ac{BNPL}, including households in default at the start. "
        "Volume: annual \\ac{BNPL} volume per eligible household, in 2017 Rands, against a provider "
        "range of R1{,}333--R4{,}261 (Table~\\ref{tab:bnpl-on-checks}). Stacking: ever-holders who owed "
        "two or more platforms at some tick (\\ac{CFPB}: 32--33\\%). Holding: at the final tick. "
        f"Weighted least squares of the effect on $\\beta$: slope ${lin['slope_pp_per_0.1_beta']:+.3f} "
        f"\\pm {lin['slope_se_per_0.1_beta']:.3f}$ points per 0.1 of $\\beta$, with standard errors that "
        "allow for the shared seeds and no-\\ac{BNPL} arm; the quadratic and hinge "
        f"($\\beta = 0.1$) terms are {verdicts['quadratic']['extra_term_t']:.2f} and "
        f"{verdicts['hinge']['extra_term_t']:.2f} standard errors from zero, so the effect is "
        f"{payload['verdict']} under the test fixed before the sweep (Section~\\ref{{sec:results-beta}})."
    )
    lines = [
        "% GENERATED by notebooks/scripts/beta_sweep_analysis.py from results/raw/rqb.parquet --",
        "% do not edit by hand; re-run the script instead.",
        r"\begin{table}[!htb]",  # floats like the other body tables (issue #89)
        r"\centering",
        r"\caption{The \ac{BNPL} effect on default across $\beta$}",
        r"\label{tab:beta}",
        r"\tabnote{" + note + "}",
        r"\begingroup\setlength{\tabcolsep}{4pt}\footnotesize",
        r"\begin{tabular}{c R{2.6cm} rrrrr}",
        r"\toprule",
        r"$\beta$ & \textbf{Effect (pp)} & \textbf{SD} & \textbf{Default (\%)} & \textbf{Volume (R)} "
        r"& \textbf{Stacking (\%)} & \textbf{Holding (\%)} \\",
        r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\endgroup",
        r"\end{table}",
        "",
    ]
    TABLE.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {TABLE}")


def main() -> None:
    df = pd.read_parquet(RAW)
    off = df[df.label == "rqb_off"]
    betas = sorted(df[df.label != "rqb_off"].beta.unique())
    years = float((df.n_ticks - df.burn_in).iloc[0]) * 14 / 365.0

    rows, per_seed = [], {}
    off_s = off.set_index("seed").default_rate_final
    for b in betas:
        on = df[(df.label != "rqb_off") & (df.beta == b)]
        eff, se, sd = paired(on, off, "default_rate_final")
        per_seed[float(b)] = (on.set_index("seed").default_rate_final - off_s) * 100
        e90, se90, _ = paired(on, off, "pct_90_plus_mean")
        econ, secon, _ = paired(on, off, "ever_consumption_distress_final")
        s_g = float((on.bnpl_adoption_final * on.n_agents / on.n_bnpl_eligible).mean())
        rows.append(dict(
            beta=float(b), n=len(on), effect_pp=eff, effect_se=se, effect_sd=sd,
            effect_90plus_all_pp=e90, effect_90plus_all_se=se90,
            effect_consumption_ever_pp=econ, effect_consumption_ever_se=secon,
            default_rate=float(on.default_rate_final.mean()),
            volume_per_eligible_year=float((on.bnpl_volume_cumulative / on.n_bnpl_eligible / years).mean()),
            stacking_ever_holders=float(on.ever_stacked_2plus_of_adopters.mean()),
            adoption_final=float(on.bnpl_adoption_final.mean()),
            ever_adopted=float(on.ever_adopted.mean()),
            s_g_final=s_g, appetite_multiplier=(Q_BASE + b * s_g) / Q_BASE,
            mean_purchase=float(on.bnpl_purchase_mean_realised.mean()),
        ))
    t = pd.DataFrame(rows)
    x, y, v = t.beta.to_numpy(), t.effect_pp.to_numpy(), t.effect_se.to_numpy() ** 2
    # Covariance of the eight mean effects across seeds: they share the no-BNPL arm and the seeds.
    E = pd.DataFrame(per_seed).dropna()
    C = E.cov().to_numpy() / len(E)
    assert np.allclose(np.diag(C), v)
    # Two values of beta compared directly: the no-BNPL arm cancels seed by seed.
    pair_se = [float((E[b2] - E[b1]).std(ddof=1) / np.sqrt(len(E)))
               for i, b1 in enumerate(E.columns) for b2 in E.columns[i + 1:]]
    one = np.ones_like(x)
    X_lin = np.column_stack([one, x])
    fits = {
        "linear": X_lin,
        "quadratic": np.column_stack([one, x, x ** 2]),
        "hinge": np.column_stack([one, x, np.maximum(x - HINGE, 0.0)]),
    }
    res, hats = {}, {}
    for name, X in fits.items():
        coef, cov, cov_indep, H = wls(X, y, v, C)
        hats[name] = H
        pred = X @ coef
        pred_se = np.sqrt(np.diag(H @ C @ H.T))
        res[name] = dict(
            coef=coef.tolist(), se=np.sqrt(np.diag(cov)).tolist(),
            se_if_independent=np.sqrt(np.diag(cov_indep)).tolist(),
            chi2=float(((y - pred) ** 2 / v).sum()), pred=pred.tolist(), pred_se=pred_se.tolist(),
        )

    verdicts = {}
    for name in ("quadratic", "hinge"):
        extra_t = res[name]["coef"][2] / res[name]["se"][2]
        D = hats[name] - hats["linear"]
        diff = D @ y
        diff_se = np.sqrt(np.maximum(np.diag(D @ C @ D.T), 1e-30))
        lin_p, lin_s = np.array(res["linear"]["pred"]), np.array(res["linear"]["pred_se"])
        nl_p, nl_s = np.array(res[name]["pred"]), np.array(res[name]["pred_se"])
        changes = [
            bool((abs(diff[i]) > 2 * diff_se[i])
                 and ((abs(lin_p[i]) > 2 * lin_s[i]) != (abs(nl_p[i]) > 2 * nl_s[i])
                      or np.sign(lin_p[i]) != np.sign(nl_p[i])))
            for i in range(len(x))
        ]
        verdicts[name] = dict(
            extra_term_t=float(extra_t), condition1=bool(abs(extra_t) > 2),
            extra_term_t_if_independent=float(res[name]["coef"][2] / res[name]["se_if_independent"][2]),
            max_diff_over_se=float(np.max(np.abs(diff) / diff_se)),
            condition2_points=[float(x[i]) for i, c in enumerate(changes) if c],
            condition2=bool(any(changes)),
        )
    nonlinear = any(d["condition1"] and d["condition2"] for d in verdicts.values())

    within = t[t.volume_per_eligible_year <= VOLUME_TOP]
    x_rule = float(min(within.beta.max(), 0.30)) if len(within) else 0.0
    b0 = t[t.beta == 0].iloc[0]
    slope, slope_se = res["linear"]["coef"][1], res["linear"]["se"][1]
    payload = {
        "_note": "Milestone 2 beta sweep; test pre-registered in issue #97. Effects in percentage "
                 "points of default during the run, paired by seed against rqb_off (seeds 90,000+).",
        "verdict": "non-linear" if nonlinear else "linear",
        "tests": verdicts,
        "fits": res,
        "x_rule": {"x": x_rule, "volume_top": VOLUME_TOP,
                   "beta_in_provider_volume_range": t[(t.volume_per_eligible_year >= VOLUME_BOTTOM)
                                                      & (t.volume_per_eligible_year <= VOLUME_TOP)].beta.tolist()},
        "headline_linear": {
            "beta0_effect_pp": float(b0.effect_pp), "beta0_effect_se": float(b0.effect_se),
            "beta0_effect_sd": float(b0.effect_sd),
            "slope_pp_per_0.1_beta": slope / 10, "slope_se_per_0.1_beta": slope_se / 10,
            "slope_se_per_0.1_beta_if_independent": res["linear"]["se_if_independent"][1] / 10,
        },
        "_se_note": "Standard errors use the covariance of the eight mean effects across seeds "
                    "(shared no-BNPL arm and seeds); *_if_independent: the pre-2026-11-10 values.",
        "effect_correlation_across_beta": {
            "min": float(np.min(E.corr().to_numpy()[np.triu_indices(len(betas), 1)])),
            "max": float(np.max(E.corr().to_numpy()[np.triu_indices(len(betas), 1)]))},
        "between_beta_difference_se": {"min": min(pair_se), "median": float(np.median(pair_se)),
                                       "max": max(pair_se)},
        # A true difference equal to two standard errors is detected about half the time.
        "between_beta_difference_detected_half_the_time_pp": 2 * float(np.median(pair_se)),
        "baseline_default_no_bnpl": float(off.default_rate_final.mean()),
        "replicates_per_arm": int(t.n.min()),
        "table": t.to_dict(orient="records"),
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_table(t, res, verdicts, payload)
    pd.set_option("display.width", 220)
    print(t[["beta", "effect_pp", "effect_se", "effect_sd", "effect_90plus_all_pp", "volume_per_eligible_year",
             "stacking_ever_holders", "adoption_final", "appetite_multiplier", "mean_purchase"]]
          .round(3).to_string(index=False))
    print(json.dumps({"verdict": payload["verdict"], "tests": verdicts, "x_rule": payload["x_rule"],
                      "headline_linear": payload["headline_linear"]}, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
