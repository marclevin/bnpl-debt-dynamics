# Buy Now, Pay Later and Household Credit Distress in South Africa: An Agent-Based Model

Masters mini-dissertation, University of Cape Town.

## Sources of truth

Each kind of information has one home. Nothing else should restate it.

| Question | Authority |
| --- | --- |
| What the thesis claims, the research questions, the design | `thesis/chapters/*.tex` |
| Every number in the thesis | `thesis/chapters/generated/` and `results/summary/results_numbers.json`, built from `results/raw/` by `notebooks/scripts/build_results_tables.py` and checked by `check_results_tables.py` |
| Parameter values and their provenance | `simulation/config.py` (Appendix B is generated from it) |
| What the model does | `simulation/` (the thesis describes it; the code decides) |
| Calibration targets and external anchors, with sources | `data/config/` and its README |
| Why each design choice was made, and what was rejected | [`docs/DECISIONS.md`](docs/DECISIONS.md) (design history; code comments cite its D-numbers) |
| What is still open, and how past defects were closed | [`docs/DEFECTS.md`](docs/DEFECTS.md) (code comments cite its B-numbers) |
| What changed when, and why results moved | [`docs/HISTORY.md`](docs/HISTORY.md) |

## Layout

| Path | Contents |
| --- | --- |
| `thesis/` | `main.tex`, `chapters/`, `main.bib`, `figures/` (generated) |
| `simulation/` | the Mesa model; tests in `simulation/tests/` |
| `notebooks/` | data pipeline P0 to P4 (below); `scripts/` holds every build, run and check script |
| `data/raw/` | survey and administrative source files (not in git) |
| `data/config/` | hand-curated targets and anchors, each with its source |
| `data/processed/` | outputs of the data pipeline; the model reads `synthetic_population_5000.parquet` (not in git) |
| `results/raw/` | one row per simulation run, with every parameter and seed (not in git) |
| `results/summary/` | calibration, Sobol, summary tables, `results_numbers.json`, and the outputs of the check scripts |
| `references/` | supervisor's reference paper and source PDFs (not in git) |

## Data pipeline

| Step | What it does | Where |
| --- | --- | --- |
| P0 backbone | NIDS Wave 5 filtered to 10,841 households; income, expenditure, savings and debt derived | `notebooks/p0_backbone.ipynb` |
| P2 match | one FinScope 2019 donor per household within its quintile-by-province cell; all six flags copied together | `notebooks/p2_finscope_match.ipynb` |
| P3 resample | 5,000 households drawn with replacement in proportion to weight | `notebooks/p3_resample.ipynb` |
| P4 validate | construction, imputation and resampling checks (`tab:validation`) | `notebooks/p4_validation.ipynb` |
| P5 instantiate | each row becomes a household agent | `simulation/population.py` |

## Reproducing everything

About 25 minutes on a 16-core machine. Python 3.14 with the versions in
`simulation/requirements.txt`:

    uv venv --python 3.14 .venv
    uv pip install --python .venv/bin/python -r simulation/requirements.txt tabulate

Then, from the repository root:

    .venv/bin/python -m pytest simulation/tests -q
    PYTHONPATH=. .venv/bin/python -m simulation.calibrate --reps 20
    PYTHONPATH=. .venv/bin/python notebooks/scripts/final_run.py        # every suite, Sobol, summaries; log in results/final_run.log
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_tables.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_figures.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/generate_param_register.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_defaulter_credit.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_single_tick_calibration.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_cap_definitions.py
    cd thesis && latexmk -pdf main.tex

Word count of the body (cap 10,000): `python3 notebooks/scripts/wc_prose.py`.

Seeds, replicates and factors for each experiment are in the thesis (`tab:experiments`). The
raw files map to suites as follows; experiment keys keep an older numbering (`rq0` is the
baseline suite, `rq1` the platform sweep; see the top of `simulation/experiments.py`).

| Suite | File | Runs |
| --- | --- | --- |
| calibration | `results/summary/calibration_runs.parquet` | 460 |
| baseline and injection | `results/raw/rq0.parquet` | 60 |
| platform count | `results/raw/rq1.parquet` | 600 |
| access, linear rule | `results/raw/rq2.parquet` | 700 |
| access, threshold rule | `results/raw/rq2t.parquet` | 1,460 |
| cooling-off and cap | `results/raw/rq3.parquet` | 320 |
| scenarios | `results/raw/rq3s.parquet` | 800 |
| sensitivity of the level | `results/raw/robustness.parquet` | 620 |
| sensitivity of the effect | `results/raw/effect.parquet` | 1,020 |
| Sobol | `results/summary/sobol_runs.parquet` | 4,096 |

Outputs from before the corrections of 2026-09-29 can be regenerated from tag
`pre-correction-2026-09-29` ([`docs/HISTORY.md`](docs/HISTORY.md)).
