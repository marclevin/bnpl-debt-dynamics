"""Parallel batch runner.

One row of output per run. Raw run-level output lands in `results/raw/`; summarised
output in `results/summary/` (thesis ch.5, Reproducibility).
"""

from __future__ import annotations

import warnings
from collections.abc import Iterable

import pandas as pd
from joblib import Parallel, delayed

from .config import RESULTS_RAW, ParamSet


def run_one(params: ParamSet) -> dict:
    """Run a single parameterisation. Top-level so joblib can pickle it."""
    # Mesa 3.5.1 warns that Model(seed=...) is deprecated in favour of rng=. Seeding is
    # explicit via ParamSet.seed and the model's own Random, so the warning is noise.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        from .model import BNPLModel

        return BNPLModel(params).run()


def run_batch(
    param_sets: Iterable[ParamSet],
    n_jobs: int = -2,
    verbose: int = 5,
) -> pd.DataFrame:
    """Run many parameterisations in parallel.

    `n_jobs=-2` leaves one core free so the machine stays usable during long sweeps.
    """
    param_sets = list(param_sets)
    results = Parallel(n_jobs=n_jobs, verbose=verbose)(
        delayed(run_one)(p) for p in param_sets
    )
    return pd.DataFrame(results)


def replicate(base: ParamSet, n_reps: int, seed0: int = 0) -> list[ParamSet]:
    """Replicates of one arm, with a deterministic seed scheme.

    Seeds are `seed0 + i` so any single run can be reproduced from its reported seed
    without re-running the batch.
    """
    return [base.replace(seed=seed0 + i) for i in range(n_reps)]


def save(df: pd.DataFrame, name: str) -> None:
    RESULTS_RAW.mkdir(parents=True, exist_ok=True)
    out = RESULTS_RAW / f"{name}.parquet"
    df.to_parquet(out, index=False)
    print(f"wrote {out}  ({len(df)} runs)")
