"""Summarise the step-by-step diagnostic: what each correction does at fixed parameters.

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/diagnostic_summary.py

All arms share seeds 10,000-10,019, so every difference is taken seed by seed and carries
the standard error of the mean of the twenty paired differences.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STEPS = [
    ("0_original", "original code"),
    ("1_interest", "+ interest and payment accounting"),
    ("2_timing", "+ instalment timing"),
    ("3_fallback", "+ traditional fallback request"),
    ("4_latefee", "+ late-fee cap (all corrections)"),
]


def arm(df, label, col):
    return df[df.label == label].set_index("seed")[col].sort_index()


def paired(a, b, scale=100.0):
    d = (a - b) * scale
    return d.mean(), d.std(ddof=1) / np.sqrt(len(d))


def pm(x):
    return f"{x[0]:+.2f} ± {x[1]:.2f}"


rows = []
data = {k: pd.read_parquet(HERE / "diagnostic" / f"{k}.parquet") for k, _ in STEPS}
for key, name in STEPS:
    d = data[key]
    c = "default_rate_final"
    rows.append(
        {
            "step": name,
            "commit": d["commit"].iloc[0],
            "default, no BNPL (%)": f"{100 * arm(d, 'no_bnpl', c).mean():.2f}",
            "90+ credit-active, no BNPL (%)": f"{100 * arm(d, 'no_bnpl', 'active_90_plus_mean').mean():.2f}",
            "BNPL effect, beta=0 (pp)": pm(paired(arm(d, "bnpl_b0", c), arm(d, "no_bnpl", c))),
            "BNPL effect, beta=1 (pp)": pm(paired(arm(d, "bnpl_b1", c), arm(d, "no_bnpl", c))),
            "shortfall path only (pp)": pm(paired(arm(d, "bnpl_shortfall_only", c), arm(d, "no_bnpl", c))),
            "bureau less benchmark (pp)": pm(paired(arm(d, "bureau_b0", c), arm(d, "bnpl_b0", c))),
            "screening less benchmark (pp)": pm(paired(arm(d, "screening_b0", c), arm(d, "bnpl_b0", c))),
            "cap 1 less benchmark (pp)": pm(paired(arm(d, "cap1_b0", c), arm(d, "bnpl_b0", c))),
            "cap 2 less benchmark (pp)": pm(paired(arm(d, "cap2_b0", c), arm(d, "bnpl_b0", c))),
            "new traditional lending, BNPL beta=0 (R m)": f"{arm(d, 'bnpl_b0', 'trad_granted_value').mean() / 1e6:.2f}",
            "BNPL volume, beta=0 (R m)": f"{arm(d, 'bnpl_b0', 'bnpl_volume_cumulative').mean() / 1e6:.2f}",
        }
    )
out = pd.DataFrame(rows).set_index("step").T
print(out.to_markdown())
(HERE / "diagnostic_summary.md").write_text(
    "# Diagnostic at fixed parameters (shock probability 0.016, friction 0.09)\n\n"
    "Seeds 10,000-10,019 in every arm and at every step; differences are paired by seed, "
    "with one standard error. Default is the share of all households in default at the final tick.\n\n"
    + out.to_markdown() + "\n"
)
