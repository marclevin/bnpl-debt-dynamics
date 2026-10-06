"""Re-run the effect suite with the three switches added on 2026-10-06.

    PYTHONPATH=. .venv/bin/python results/variants_2026-10-06/run_variants.py

Every arm already stored in results/raw/effect.parquet must come out identical, so the
new switches change nothing at their defaults. The new arms are then saved with the rest.
"""
import subprocess

import pandas as pd

from simulation.batch import run_batch, save
from simulation.config import RESULTS_RAW
from simulation.experiments import effect_robustness

print("commit", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())
old = pd.read_parquet(RESULTS_RAW / "effect.parquet")
new = run_batch(effect_robustness(20), n_jobs=14, verbose=0)
m = old.merge(new, on=["label", "seed"], suffixes=("_a", "_b"))
assert len(m) == len(old), (len(m), len(old))
cols = [c for c in old.columns
        if c not in ("label", "seed") and pd.api.types.is_numeric_dtype(old[c]) and old[c].dtype != bool]
gap = max((m[f"{c}_a"].astype(float) - m[f"{c}_b"].astype(float)).abs().max() for c in cols)
print(f"stored arms reproduced: {len(m)} runs, largest absolute difference over {len(cols)} columns: {gap}")
assert gap == 0.0
added = sorted(set(new.label) - set(old.label))
print("new arms:", added, "runs:", len(new) - len(old))
save(new, "effect")
