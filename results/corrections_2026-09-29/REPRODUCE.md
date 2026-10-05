# Reproducing the corrected results

All commands run from the repository root. Nothing here needs paid compute: the whole
pipeline takes about 25 minutes on a 16-core machine.

## Environment

Python 3.14.4 with the versions pinned in `simulation/requirements.txt`.

    uv venv --python 3.14 .venv
    uv pip install --python .venv/bin/python -r simulation/requirements.txt tabulate

The data the model reads are not in git (`data/processed/synthetic_population_5000.parquet`,
`data/raw/NIDS_W5`). They are unchanged by the corrections.

## Versions

| What | Git reference |
|---|---|
| State before the corrections (code, thesis, tracked outputs) | tag `pre-correction-2026-09-29` (commit `5694751`) |
| Code that produced the original outputs | commit `e214245` (model logic identical to the tag) |
| Interest and payment accounting | `b483ea1` |
| Instalment timing | `d3352c4` |
| Traditional fallback request | `1415625` |
| Late-fee cap; cap documented and tested | `f40e4bf` |
| Combined bureau-and-screening arm | `c6c8742` (calibration, six suites and Sobol were run at this commit) |
| Alternative checkout assumption; effect suite re-run | `e366631` |
| Alternative checkout assumption removed; one shortfall rule | `4ef473c` |

Commit `e366631` adds a parameter whose default leaves behaviour unchanged. `rerun_effect.py`
confirms this: the baseline suite and the 880 effect runs already stored are reproduced
exactly at that commit. Commit `4ef473c` removes the parameter again, and
`remove_checkout_arm.py` confirms that the baseline suite and the same 880 effect runs are
reproduced exactly. The 40 runs of the removed arm are in `effect_checkout_unfunded.parquet`
in this folder and can be reproduced only from `e366631`.

## Steps

    # 1. tests (128)
    .venv/bin/python -m pytest simulation/tests -q

    # 2. calibration: original grid, targets and objective
    PYTHONPATH=. .venv/bin/python -m simulation.calibrate --reps 20

    # 3. every experiment suite, the Sobol analysis and the summaries
    PYTHONPATH=. .venv/bin/python scratchpad/final_run.py

    # 4. tables, figures, parameter register, and the independent check of the tables
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_tables.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_figures.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/generate_param_register.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py

    # 5. the thesis
    cd thesis && latexmk -pdf main.tex

    # the records in this folder
    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/verify_behaviour.py
    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/diagnostic_summary.py
    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/before_after.py --write
    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/cap_definitions.py
    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/remove_checkout_arm.py

`before_after.py` and `rerun_effect.py` read the removed arm and run at commit `e366631`.

## Configurations and seeds

Every run echoes all of its parameters and its seed into its own row of `results/raw/*.parquet`,
so each run can be reproduced from that row alone. All arms use shock probability 0.016 and
payment friction 0.09, 5,000 households, 52 ticks and a 12-tick burn-in unless the arm varies
them. Twenty replicates per arm, seeds `seed0 + 0..19`, except the scenario suite, which has
one hundred.

| Suite | File | Runs | seed0 | Arms share seeds? |
|---|---|---|---|---|
| calibration | `results/summary/calibration_runs.parquet` | 460 | 1,000 | yes |
| baseline and injection | `rq0.parquet` | 60 | 10,000 | yes |
| platform count | `rq1.parquet` | 600 | 20,000 | yes |
| access, linear rule | `rq2.parquet` | 700 | 30,000 | yes |
| access, threshold rule | `rq2t.parquet` | 1,460 | 60,000; 61,000 for the mean-threshold arms | yes, within each block |
| cooling-off and cap | `rq3.parquet` | 320 | 40,000 benchmark and cooling-off; 43,000 cap | only the cooling-off arms share the benchmark's seeds |
| scenarios: benchmark, bureau, screening, both | `rq3s.parquet` | 800 | 80,000 | yes, 100 replicates per arm |
| sensitivity of the level | `robustness.parquet` | 620 | 50,000 to 59,000, one block per group | within a group |
| sensitivity of the effect | `effect.parquet` | 880 | 70,000 | yes |
| Sobol | `results/summary/sobol_runs.parquet` | 4,096 | see file | 2 replicates per design point |
| step-by-step diagnostic | `results/corrections_2026-09-29/diagnostic/*.parquet` | 160 per step | 10,000 | yes |

The run log of the corrected suite is `results/final_run.log` (copy:
`results/corrections_2026-09-29/final_run_c6c8742.log`); the effect re-run is logged in
`effect_rerun.log`.

## Scenario arms at 100 replicates (2026-10-05)

Until 2026-10-05 the bureau, screening and combined arms were part of `rq3.parquet`, with 20
replicates each on seed blocks 41,000, 42,000 and 44,000. They now form the suite `rq3s`, with
their own benchmark, 100 replicates per arm and one shared seed block.
`python -m simulation.experiments --which all --reps 20` runs it at five times `--reps`. The
retained arms of `rq3.parquet` are reproduced exactly. The earlier file is kept, untracked, in
`results/superseded_2026-10-05_rq3_20_replicates/`. The calibration script has a fourth stage
that checks the fitted shock probability in steps of 0.001 and writes
`fine_grid_90_plus` into `calibration.json`; the 460 calibration runs and the selection are
unchanged.

## Preserved original outputs

`results/superseded_2026-09-29_pre-correction/` holds the original raw runs, summaries, logs,
generated tables, figures and the compiled thesis. This environment reproduces those runs from
the original code: the 60 baseline runs match in every default, arrears and volume figure,
with one platform request in one run and rounding at the sixth decimal as the only differences.
