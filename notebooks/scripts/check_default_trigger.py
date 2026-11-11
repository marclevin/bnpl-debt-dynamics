"""Fix pass 2026-11-11: which facility triggers the extra defaults when BNPL is enabled?

For each rq0 seed the script runs the baseline without BNPL and the BNPL arm at beta = 0 and, at
the tick each household defaults, records whether its oldest unpaid BNPL instalment had reached
the threshold (k_default ticks), and whether its traditional arrears had. The rise in default
during the run is split into households in default on BNPL alone (bnpl_only_pp) and the
remainder (remainder_pp), the change in defaults that involve traditional arrears.
bnpl_triggered_pp also counts households past the threshold on both facilities. It writes results/summary/default_trigger.json, the source of the
split in Section 4.1.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_default_trigger.py
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path
from statistics import mean, stdev

warnings.simplefilter("ignore")
from simulation.experiments import calibrated  # noqa: E402
from simulation.model import BNPLModel  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SEEDS = range(10_000, 10_020)  # rq0 seeds
TICKS = 52


def run(seed: int, bnpl: bool) -> tuple[int, int, int, int]:
    """(households, new defaults, those with BNPL arrears at the threshold, of them BNPL only)."""
    m = BNPLModel(calibrated(bnpl_enabled=bnpl, beta=0.0, label="default_trigger").replace(seed=seed))
    k = m.params.k_default
    known = {a.agent_id for a in m.agents if a.defaulted}
    new = by_bnpl = bnpl_only = 0
    for _ in range(TICKS):
        m.step()
        for a in m.agents:
            if a.defaulted and a.agent_id not in known:
                known.add(a.agent_id)
                new += 1
                # The age the household's default was decided on is arrears_age_max; find the tick
                # index that reproduces it, then read the BNPL age at that tick.
                for t in (m.tick, m.tick - 1):
                    trad = t - a.trad_unpaid[0][0] + 1 if a.trad_unpaid and a.arrears_trad > 0 else 0
                    b = max((pl.arrears_age(a.agent_id, t) for pl in m.platforms), default=0)
                    if max(trad, b) == a.arrears_age_max:
                        break
                else:
                    raise AssertionError("could not reproduce the arrears age at default")
                by_bnpl += b >= k
                bnpl_only += b >= k and trad < k
    return len(m.agents), new, by_bnpl, bnpl_only


def se(xs: list[float]) -> float:
    return stdev(xs) / len(xs) ** 0.5


def main() -> None:
    rows = []
    for seed in SEEDS:
        n, off_new, off_b, _ = run(seed, False)
        _, on_new, on_b, on_only = run(seed, True)
        assert off_b == 0
        rows.append({"seed": seed,
                     "effect_pp": 100 * (on_new - off_new) / n,
                     "bnpl_triggered_pp": 100 * on_b / n,
                     "bnpl_only_pp": 100 * on_only / n,
                     "remainder_pp": 100 * (on_new - on_only - off_new) / n,
                     "traditional_pp": 100 * (on_new - on_b - off_new) / n})
    out = {"seeds": [SEEDS.start, SEEDS.stop - 1], "beta": 0.0}
    for key in ("effect_pp", "bnpl_triggered_pp", "bnpl_only_pp", "remainder_pp", "traditional_pp"):
        xs = [r[key] for r in rows]
        out[key] = mean(xs)
        out[key + "_se"] = se(xs)
    out["per_seed"] = rows
    (ROOT / "results" / "summary" / "default_trigger.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "per_seed"}, indent=1))


if __name__ == "__main__":
    main()
