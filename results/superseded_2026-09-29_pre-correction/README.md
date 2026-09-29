# Outputs preserved before the accounting corrections (2026-09-29)

Snapshot of every output of the model as it stood at git tag `pre-correction-2026-09-29`
(commit 5694751). The simulation code that produced `raw/` was commit e214245 (see
`final_run.log`); the model logic did not change between that commit and the tag.

- `raw/`      per-run results, 20 replicates per arm (rq0, rq1, rq2, rq2t, rq3, robustness, effect)
- `summary/`  calibration, Sobol and summary tables
- `*.log`     the original run logs, with seeds and timings
- `thesis/`   the generated tables, figures and compiled PDF built from these outputs

Nothing in this directory is read by the current pipeline. Corrected outputs are written to
`results/raw` and `results/summary`.
