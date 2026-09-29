"""Re-run the effect suite, and confirm that rq0 is unchanged by the new parameter.

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/rerun_effect.py
"""
import subprocess

import pandas as pd

from simulation.batch import run_batch, save
from simulation.config import RESULTS_RAW
from simulation.experiments import effect_robustness, rq0_baseline

print("commit", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
old = pd.read_parquet(RESULTS_RAW / "rq0.parquet").sort_values(["label", "seed"]).reset_index(drop=True)
new = run_batch(rq0_baseline(20), n_jobs=14, verbose=0).sort_values(["label", "seed"]).reset_index(drop=True)
cols = [c for c in old.columns if pd.api.types.is_numeric_dtype(old[c]) and old[c].dtype != bool]
gap = (new[cols].astype(float) - old[cols].astype(float)).abs().max().max()
print("rq0 at this commit against the stored rq0: largest absolute difference", gap)
assert gap == 0.0
old_eff = pd.read_parquet(RESULTS_RAW / "effect.parquet")
eff = run_batch(effect_robustness(20), n_jobs=14, verbose=0)
m = old_eff.merge(eff, on=["label", "seed"], suffixes=("_a", "_b"))
gap = (m.default_rate_final_a - m.default_rate_final_b).abs().max()
print("effect arms already stored, against this run: largest difference in default", gap, "over", len(m), "runs")
assert gap == 0.0
save(eff, "effect")
