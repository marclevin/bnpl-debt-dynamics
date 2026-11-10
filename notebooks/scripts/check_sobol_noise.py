"""How much of each total-order Sobol index is replicate noise (QA 2026-11-10, A1 item 6).

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_sobol_noise.py

Reads results/summary/sobol_runs.parquet (the 16,384 runs behind sobol_indices.json; nothing is
simulated) and writes results/summary/sobol_noise_check.json.

Each design point is the mean of `reps` replicates, so it carries independent noise of variance
s2_k / reps, where s2_k is the replicate variance at point k. The Jansen total-order estimator
SALib uses, S_T,i = mean((f(A) - f(AB_i))^2) / (2 Var Y), adds the noise of both points to the
numerator, so in expectation every S_T is raised by the noise share of Var Y, whether or not the
parameter matters. The first-order estimator, mean(f(B) (f(AB_i) - f(A))) / Var Y, has no such
bias: the noise only widens it.

This script reproduces SALib's S_T, then subtracts each pair's own noise from the numerator
(an unbiased correction) and reports the corrected S_T on two scales: as a share of Var Y
(comparable with the table) and as a share of the noise-free variance Var Y - noise. Intervals are
95% percentile intervals from a bootstrap over the 256 base samples, so the uncertainty of the
noise estimate is included.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "results" / "summary" / "sobol_runs.parquet"
IDX = ROOT / "results" / "summary" / "sobol_indices.json"
OUT = ROOT / "results" / "summary" / "sobol_noise_check.json"
B = 2000


def main() -> None:
    meta = json.loads(IDX.read_text(encoding="utf-8"))
    names = meta["problem"]["names"]
    D, N, reps = len(names), meta["n_base_samples"], meta["replicates"]
    df = pd.read_parquet(RUNS)
    g = df.groupby("design")["default_rate_final"]
    y = g.mean().reindex(range(N * (D + 2))).to_numpy()
    nv = (g.var(ddof=1) / reps).reindex(range(N * (D + 2))).to_numpy()  # noise variance of each mean
    # SALib's layout without second order: for base sample j, rows A_j, AB_1j..AB_Dj, B_j.
    step = D + 2
    A, Bm = y[0::step], y[step - 1::step]
    AB = np.stack([y[i + 1::step] for i in range(D)], axis=1)
    nA, nB = nv[0::step], nv[step - 1::step]
    nAB = np.stack([nv[i + 1::step] for i in range(D)], axis=1)

    def indices(ix: np.ndarray) -> dict:
        a, b, ab, na, nab = A[ix], Bm[ix], AB[ix], nA[ix], nAB[ix]
        var_y = np.var(np.r_[a, b])  # SALib's denominator
        noise = np.mean(np.r_[na, nB[ix]])
        st = 0.5 * np.mean((a[:, None] - ab) ** 2, axis=0) / var_y
        st_num_c = 0.5 * np.mean((a[:, None] - ab) ** 2 - (na[:, None] + nab), axis=0)
        s1 = np.mean(b[:, None] * (ab - a[:, None]), axis=0) / var_y
        return dict(st=st, st_c=st_num_c / var_y, st_c_clean=st_num_c / (var_y - noise),
                    s1_clean=s1 * var_y / (var_y - noise), noise_share=noise / var_y)

    full = indices(np.arange(N))
    rng = np.random.default_rng(20261110)
    boots = [indices(rng.integers(0, N, N)) for _ in range(B)]

    def ci(key: str) -> np.ndarray:
        arr = np.array([bt[key] for bt in boots])
        return np.percentile(arr, [2.5, 97.5], axis=0)

    salib = {r["parameter"]: r for r in meta["indices"]["default_rate_final"]}
    rows = []
    lo_c, hi_c = ci("st_c")
    lo_cc, hi_cc = ci("st_c_clean")
    for i, p in enumerate(names):
        rows.append(dict(
            parameter=p,
            ST_salib=salib[p]["ST"], ST_salib_conf=salib[p]["ST_conf"], ST_reproduced=float(full["st"][i]),
            ST_noise_corrected=float(full["st_c"][i]),
            ST_noise_corrected_ci=[float(lo_c[i]), float(hi_c[i])],
            ST_noise_corrected_of_noise_free_var=float(full["st_c_clean"][i]),
            ST_noise_corrected_of_noise_free_var_ci=[float(lo_cc[i]), float(hi_cc[i])],
            S1_salib=salib[p]["S1"], S1_salib_conf=salib[p]["S1_conf"],
        ))
    nlo, nhi = ci("noise_share")
    out = {
        "_note": "Noise correction of the total-order indices for default_rate_final; see the script "
                 "docstring (notebooks/scripts/check_sobol_noise.py). Shares are fractions.",
        "noise_share": float(full["noise_share"]), "noise_share_ci": [float(nlo), float(nhi)],
        "noise_share_in_sobol_indices_json": meta["replicate_noise_share"]["default_rate_final"],
        "bootstrap_draws": B,
        "rows": rows,
    }
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"noise share {out['noise_share']:.3f} [{nlo:.3f}, {nhi:.3f}]")
    for r in rows:
        print(f"{r['parameter']:28s} ST salib {r['ST_salib']:.3f}+-{r['ST_salib_conf']:.3f} "
              f"repro {r['ST_reproduced']:.3f}  corrected {r['ST_noise_corrected']:+.3f} "
              f"[{r['ST_noise_corrected_ci'][0]:+.3f}, {r['ST_noise_corrected_ci'][1]:+.3f}]  "
              f"of noise-free var {r['ST_noise_corrected_of_noise_free_var']:+.3f} "
              f"[{r['ST_noise_corrected_of_noise_free_var_ci'][0]:+.3f}, "
              f"{r['ST_noise_corrected_of_noise_free_var_ci'][1]:+.3f}]")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
