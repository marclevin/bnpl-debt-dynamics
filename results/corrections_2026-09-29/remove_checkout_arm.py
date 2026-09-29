"""Remove the alternative checkout arm from the stored effect runs, and confirm that
removing the switch from the code changed no result.

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/remove_checkout_arm.py

The 40 runs of `eff_checkout_unfunded` are moved to `effect_checkout_unfunded.parquet` in
this folder, together with the parameter column that only they varied. They were produced
at commit `e366631` and cannot be reproduced from later code, which has one shortfall rule.
The baseline suite and the remaining effect arms are then run again at the current commit
and compared with the stored runs in every numeric column.
"""
import subprocess
from pathlib import Path

import pandas as pd

from simulation.batch import run_batch, save
from simulation.config import RESULTS_RAW
from simulation.experiments import effect_robustness, rq0_baseline

HERE = Path(__file__).resolve().parent
ARM = "eff_checkout_unfunded"
SWITCH = "shortfall_checkout_financed"
KEY = ["label", "seed"]


def largest_gap(old: pd.DataFrame, new: pd.DataFrame) -> float:
    old = old.sort_values(KEY).reset_index(drop=True)
    new = new.sort_values(KEY).reset_index(drop=True)
    assert old[KEY].equals(new[KEY]), "the two sets of runs differ in label or seed"
    assert set(old.columns) == set(new.columns), set(old.columns) ^ set(new.columns)
    cols = [c for c in old.columns if pd.api.types.is_numeric_dtype(old[c]) and old[c].dtype != bool]
    other = [c for c in old.columns if c not in cols]
    for c in other:
        assert (old[c].map(repr) == new[c].map(repr)).all(), c
    return float((new[cols].astype(float) - old[cols].astype(float)).abs().max().max())


print("commit", subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip())

eff = pd.read_parquet(RESULTS_RAW / "effect.parquet")
dropped = eff[eff.label.str.startswith(ARM)]
if len(dropped):
    assert len(dropped) == 40 and not dropped[SWITCH].any()
    dropped.to_parquet(HERE / "effect_checkout_unfunded.parquet")
    eff = eff[~eff.label.str.startswith(ARM)]
    assert eff[SWITCH].all()
    eff = eff.drop(columns=SWITCH).reset_index(drop=True)
    print(f"moved {len(dropped)} runs of {ARM} out of effect.parquet; {len(eff)} remain")
else:
    print(f"effect.parquet holds no runs of {ARM}; {len(eff)} runs")

gap = largest_gap(pd.read_parquet(RESULTS_RAW / "rq0.parquet"), run_batch(rq0_baseline(20), n_jobs=14, verbose=0))
print("baseline suite at this commit against the stored rq0: largest absolute difference", gap)
assert gap == 0.0

gap = largest_gap(eff, run_batch(effect_robustness(20), n_jobs=14, verbose=0))
print("effect suite at this commit against the stored runs: largest absolute difference", gap,
      "over", len(eff), "runs")
assert gap == 0.0
save(eff, "effect")
