"""Lead-editor check (2026-10-07): can any shock probability on the calibration grid fit the
CCMR 90+ band under the single-tick (non-persistent) income shock?

Section 4.5 claimed it cannot, but no stored run tested it. Runs the calibration grid of
simulation/calibrate.py (0.008 to 0.064, friction at its fitted 0.09, BNPL off) on the
calibration seeds 1,000-1,019 and reports the post-burn-in mean 90+ share of credit-active
households. Writes results/summary/single_tick_calibration.json (Section 4.5 of the thesis).

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_single_tick_calibration.py
"""
import json
import warnings
from pathlib import Path

from joblib import Parallel, delayed

warnings.simplefilter("ignore")
from simulation.batch import run_one  # noqa: E402
from simulation.config import ParamSet  # noqa: E402

GRID = [0.008, 0.016, 0.024, 0.032, 0.040, 0.048, 0.056, 0.064]
TARGET = 0.1421

if __name__ == "__main__":
    sets = [
        ParamSet(shock_prob=p, payment_friction=0.09, bnpl_enabled=False,
                 shock_persistent=False, seed=1_000 + i, label=f"single_{p}")
        for p in GRID for i in range(20)
    ]
    rows = Parallel(n_jobs=-2)(delayed(run_one)(s) for s in sets)
    out = {}
    for p in GRID:
        vals = [r["active_90_plus_mean"] for r, s in zip(rows, sets) if s.shock_prob == p]
        m = sum(vals) / len(vals)
        out[f"{p:.3f}"] = m
        print(f"p={p:.3f}: 90+ share (credit-active, post-burn-in mean) {m:.4f}  target {TARGET}")
    dest = Path("results/summary/single_tick_calibration.json")
    dest.write_text(json.dumps({"friction": 0.09, "target": TARGET, "active_90_plus_mean": out}, indent=2))
    print(f"wrote {dest}")
