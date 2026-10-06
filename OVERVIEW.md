# Project overview

**Thesis:** *Buy Now, Pay Later and Household Credit Distress in South Africa: An Agent-Based
Model* (Masters mini-dissertation, University of Cape Town). Last updated **2026-10-06**.

This file says where the project stands and where everything lives. The thesis text
(`thesis/chapters/*.tex`) is the authority for what the thesis claims; the generated tables
(`thesis/chapters/generated/`) and `results/summary/results_numbers.json` are the authority for
its numbers. Earlier plans, changelogs and superseded results are in git history (the last
version of this file before the rewrite is in commit `1d1067f`).

## Where we are

The model, every experiment and the thesis are complete. What remains before submission:

- **Front matter** (`thesis/main.tex`): the UCT declaration wording and title page are
  provisional until the departmental template is confirmed, and `\date{\today}` must be fixed.
- **Open items** in [`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md).

Body prose is **9,739 words** against the 10,000-word cap (abstract, appendices, tables,
figures, algorithm floats and bibliography excluded); count with `python3 scratchpad/wc_prose.py`.
The abstract is 218 words. The thesis compiles to 115 pages with no undefined references.

## The research questions

Approved by the supervisor on 2026-09-09; RQ2 reworded on 2026-09-29. The thesis introduction
(Section 1.2) is authoritative.

- **Main question.** In a model of South African households already exposed to credit
  distress, how does adding a BNPL channel change that distress, and how do bureau visibility
  and affordability screening affect the outcome? The model has no credit score, so it tests
  reporting only through the traditional lender's affordability assessment.
- **RQ1.** How well does a synthetic population built from South African survey microdata
  reproduce the selected baseline arrears bands, and how does it perform against benchmarks not
  used in fitting or construction?
- **RQ2.** When BNPL platforms cannot observe one another's exposures, how often do households
  owe several platforms at once, and how do enabling BNPL, platform count, access and peer
  adoption affect population default?
- **RQ3.** How do bureau visibility and mandatory affordability screening change simulated
  borrowing and distress, with and without peer influence on adoption?

Experiment keys and figure filenames keep an older numbering (`rq0` is the baseline suite,
`rq1` the platform sweep); see the note at the top of `simulation/experiments.py`.

## Design in brief

A counterfactual, not a historical fit. The household population is built from **NIDS Wave 5
(2017)**, with financial-inclusion flags imputed from **FinScope 2019** by a cell-donor match on
per-capita income quintile and province, and resampled to 5,000 agents. Everything is in 2017
Rands. Two parameters are fitted with BNPL disabled to the **2017-Q1 NCR CCMR** arrears profile
(income-shock probability 0.016 per tick to the 90+ band, payment friction 0.09 to the 1-30 day
band). BNPL is then enabled in the same environment: four platforms that cannot see one another,
a bureau that does not record BNPL, and a traditional lender applying the Regulation 23A
residual-income test. Ticks are 14 days; runs are 52 ticks with a 12-tick burn-in.

The seventeen submodels, their sources and parameters are in Section 2 and Appendix B of the
thesis; the reasoning and rejected alternatives are in
[`scratchpad/DECISIONS.md`](scratchpad/DECISIONS.md) and Appendix A.

## Headline results

Differences carry one standard error; "detectable" means beyond two.

- **RQ1.** The fitted bands are matched (90+ share 14.20% against 14.21%), but the 90+ share
  keeps rising within a run (14.48% post-burn-in mean, 19.9% at the final tick) because no
  account is written off. Three broad external population checks pass; the intermediate arrears
  bands, the servicing share, BNPL purchase size and volume, the interest measure of Pattern 1
  and Pattern 3 fail.
- **RQ2.** With four platforms and no peer influence, 52.0% of final-tick BNPL holders owe two or
  more platforms under random routing and 36.6% when households return to platforms they
  already owe; default does not change detectably with the routing rule or the platform count.
  Enabling BNPL raises default by +0.12 ± 0.05pp without peer influence (pooled over four seed
  blocks) and +0.61 ± 0.11pp at the illustrative `beta = 1`, where volume is ten times higher.
  The effect is detectable under 19 of 20 robustness settings at `beta = 1` and 5 of 20 at
  `beta = 0`. At `beta = 1` traditional lending does not fall because applications rise
  (+801 ± 65) while the mean loan shrinks.
- **RQ3** (100 replicates per arm). Bureau visibility raises default by +0.22 ± 0.04pp
  (`beta = 0`) and +0.15 ± 0.04pp (`beta = 1`) through more refusals by the traditional lender,
  mostly in Q1; in the model a refused household has no other source of credit. Screening alone
  changes default by +0.02 ± 0.05 and +0.02 ± 0.06; added to bureau visibility at `beta = 0` it
  roughly halves the visibility effect.

## Where things live

| What | Where |
| --- | --- |
| Thesis source | `thesis/main.tex`, `thesis/chapters/*.tex`, `thesis/main.bib` |
| Generated tables and numbers | `thesis/chapters/generated/`, `results/summary/results_numbers.json` (from `notebooks/scripts/build_results_tables.py`; checked by `check_results_tables.py`) |
| Figures | `thesis/figures/` (from `notebooks/scripts/build_results_figures.py`, `build_data_figures.py`) |
| Parameter register (Appendix B) | generated from `simulation/config.py` by `notebooks/scripts/generate_param_register.py` |
| Model | `simulation/` (Mesa); tests in `simulation/tests/` |
| Data pipeline | `notebooks/p0_backbone.ipynb` to `p4_validation.ipynb`; outputs in `data/processed/` |
| Calibration targets and sources | `data/config/` (see its README) |
| Raw experiment output | `results/raw/*.parquet` (not in git; reproduce with the commands below) |
| Corrections of 2026-09-29 | `results/corrections_2026-09-29/` (`CORRECTIONS.md`, `BEFORE_AFTER.md`, `REPRODUCE.md`) |
| Robustness arms of 2026-10-06 | `results/variants_2026-10-06/README.md` |
| Superseded outputs | `results/superseded_*` (do not quote); tag `pre-correction-2026-09-29` |
| Design decisions | [`scratchpad/DECISIONS.md`](scratchpad/DECISIONS.md) |
| Open and closed defects | [`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md) |
| Data-to-agent mapping | [`household_agent.md`](household_agent.md) |

## Reproducing everything

About 25 minutes on a 16-core machine. Full commands, seeds and versions are in
[`results/corrections_2026-09-29/REPRODUCE.md`](results/corrections_2026-09-29/REPRODUCE.md).

    .venv/bin/python -m pytest simulation/tests -q
    PYTHONPATH=. .venv/bin/python -m simulation.calibrate --reps 20
    PYTHONPATH=. .venv/bin/python scratchpad/final_run.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_tables.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/build_results_figures.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/generate_param_register.py
    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py
    cd thesis && latexmk -pdf main.tex
