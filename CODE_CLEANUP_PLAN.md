# Code cleanup plan — simulation, notebooks, scripts

Drafted 2026-09-21 from the over-engineering review of the same date, plus the two implementation
qualifications in [THESIS_REVIEW_2026-09-21.md](THESIS_REVIEW_2026-09-21.md). Status: **executed
2026-09-21.** A blocking defect found on the way (B34) was fixed the same day, so the final-run
gate (1.7) is clear.

## Execution log

**Blocker found: DEFECTS B34.** Granted traditional loans added cash but were never added to
`d_trad` or to scheduled service. One calibrated baseline run granted R9.96m (20.7% of the opening
debt book) that was never repaid; 1,084 households were granted five or more times.

**Update, later on 2026-09-21: fixed, on Marc's decision, and re-fitted** (shock 0.040 → 0.016,
friction 0.09 unchanged). Decision C was made the same day (all adopters, within 35%) and is
pre-registered in `DECISIONS.md` D4. **Step 1.7's gate is therefore clear: nothing now blocks the
final run.** See `scratchpad/DEFECTS.md` B34 for what was booked and what it changed. The golden
file was deleted with the fix, since the fix moves outputs on purpose.

| Step | Outcome |
| --- | --- |
| 0.1, 0.2 | Done. Golden run: 4 arms, full population, 372 values, 23 s, deterministic. |
| 1.1 SALib pin | Done. `scipy` pin **kept**: SALib requires it. |
| 1.2 Decision A | **A1 applied.** `synchronous` arm removed; thesis, Appendix B and tests updated; thesis builds clean. |
| 1.3 Decision B | **B1 only.** The D7 comment now states the implemented rule, and `DECISIONS.md` D7 records the gap. **B2 was not built**: assessing distress after credit is meaningless while that credit is free (B34). |
| 1.4 Purchases by quintile | Done. Counts and means reconcile with the overall figures. |
| 1.5 Echo all parameters | Done. 37 parameters echoed; both test modules derive the echo set from `ParamSet`. |
| 1.6 All six band means | Done. Direct 91–120 band equals the old reconstruction to 7e-18. `fig_arrears_profile` now needs a post-cleanup `rq0.parquet`; the stale one lacks the column. |
| 1.7 Gate and run | Gate clear after the B34 fix and decision C. **The run itself has not been started**; it is Marc's to launch. |
| 2.1 Dead code | Done, with two deliberate keeps: `BNPLLoan.principal` (Appendix G opens a facility with it) and the `PURCHASE_RATIO` alias (inlining a 37-character name twice reads worse). |
| 2.2 One gate | Done. `nca_gate` floors headroom at zero, as Appendix G does, so it equals both former call sites in every case. |
| 2.3 Sourced targets | Done, via a new `load_ccmr_bands()` that `analysis.py` also uses. |
| 2.4 Shrinks | Done, except `environment.yml → -r requirements.txt`: it cannot be tested without building an environment, and the reproducibility record is the wrong place for an untested change. |
| 2.5 `rolling_limit` fallback | Skipped, as the plan allowed. Churn in twelve test lines for eight lines saved. |
| 3.1–3.6 | Done by an Opus sub-agent and reviewed diff by diff. `quick.py`, `filter_vars.py`, `to_md.py` left alone. P2's per-row `floored` count became an assert plus zero (no product term is below the floor). |
| 4 | Done: OVERVIEW status table and changelog, DEFECTS B34/B35/D6, DECISIONS D7/D16. |

Verification after every step: tests green and golden run identical. The suite ends at 91 passed /
1 xfailed, the same count as the baseline: one parametrised activation case was removed and one
test was added (the by-quintile purchases must partition the overall figures). Analysis refactors: all eight
summary CSVs and the printed report byte-identical against the existing `results/raw/`. Phase 3:
`p4_validation_summary.json`, `data_figure_numbers.json` and `data/config/` unchanged; population
parquet SHA-256 hashes unchanged.

Two things to know for later. In-place notebook execution on this machine needs `PYTHONUTF8=1`, or
non-ASCII characters are double-encoded (it happened once to P4 and was repaired). The golden-run
scaffolding (`scratchpad/golden.py`, `golden.json`) was never committed and has been deleted.

---

The original plan follows, unedited.

The plan is built around one constraint: **the final run (OVERVIEW step 4) has not happened yet.**
Anything that changes what the run does, how large it is, or what columns it writes must land before
it. Everything else must provably not move a single output.

## How to read this

| Phase | What | When | Moves outputs? |
| --- | --- | --- | --- |
| 0 | Safety net: commit the open thesis edits, save a golden run | first | no |
| 1 | Three decisions (yours), then the changes that follow from them | **before the final run** | yes, deliberately |
| 2 | Dead code and duplication inside `simulation/` | before the run if there is time, otherwise after | no, and checked |
| 3 | Notebooks and helper scripts | any time; independent of results | no |
| 4 | Bookkeeping: OVERVIEW, DEFECTS, DECISIONS | last | no |

If it gets late, do phases 0 and 1 only and start the run. Do not do part of phase 2.

Baseline measured today: `./env/python.exe -m pytest simulation/tests -q` gives **91 passed,
1 xfailed, 25 s**. Every step below ends with that command and the golden check.

---

## Phase 0 — safety net

**0.1 Commit the working tree first.** Thirteen thesis files and `OVERVIEW.md` carry uncommitted
edits from the writing review. Commit them on `six-section-restructure` before touching code, so
the cleanup diffs are separable and a clobbered edit is recoverable. Re-read any file immediately
before editing it; edits have silently reverted between sessions before.

**0.2 Save a golden run.** One throwaway script, `scratchpad/golden.py`. It runs four fixed arms on
the full population and compares every value in the run summary. It compares only keys that
existed when the golden file was saved, so steps that add columns still pass.

```python
"""Golden-run check: outcomes must not move. Usage: golden.py save | check"""
import json, sys, warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
warnings.simplefilter("ignore", FutureWarning)
from simulation.experiments import calibrated
from simulation.model import BNPLModel

OUT = Path(__file__).with_name("golden.json")
ARMS = {
    "off": dict(bnpl_enabled=False),
    "linear": dict(bnpl_enabled=True, beta=1.0),
    "threshold": dict(bnpl_enabled=True, peer_mechanism="threshold", gamma=0.3),
    # exercises both Reg 23A call sites, the facility cap and the fixed-order scheduler
    "levers": dict(bnpl_enabled=True, beta=1.0, bnpl_affordability_check=True,
                   stacking_cap=2, activation="uniform"),
}
now = {a: BNPLModel(calibrated(seed=11, n_ticks=26, **kw)).run() for a, kw in ARMS.items()}
now = json.loads(json.dumps(now, default=str))
if sys.argv[1] == "save":
    OUT.write_text(json.dumps(now, indent=1))
else:
    old = json.loads(OUT.read_text())
    bad = [(a, k, old[a][k], now[a][k]) for a in old for k in old[a] if now[a][k] != old[a][k]]
    assert not bad, bad
    print("golden: identical on", sum(map(len, old.values())), "values")
```

Run `save` once on the untouched code. Run `check` after every numbered step in phases 1 and 2.
Steps 1.2 and 1.3 change behaviour on purpose; for those, `check` must still pass, because the
golden arms use the default path. Delete the script and `golden.json` when the cleanup is merged.

---

## Phase 1 — before the final run

### Decisions needed from you

**Decision A — the activation arms.** `"uniform"` and `"synchronous"` are the same schedule: agents
are created in `agent_id` order, so sorting by id and iterating in insertion order are identical.
`rob_act_uniform` and `rob_act_synchronous` match on every seed in `results/raw/robustness.parquet`.
The thesis reports them as two checks.

- **A1, recommended.** Drop `"synchronous"`. Keep `"random"` (baseline) and `"uniform"` (fixed
  order). Saves 20 runs tonight. The thesis then claims one fixed-order check, which is what exists.
- A2. Implement real synchronous updating: every household decides on start-of-tick state, then all
  commit. The tick has inline lender and platform decisions, so this is a redesign of the step, not
  a scheduler flag. Not before tonight.

**Decision B — the distress rule** (review qualification 1). `committed_shortfall` is recorded
before borrowing, and `distressed` stays true even when credit is granted. One more fact from the
code that bears on the choice: at [agents.py:150-153](simulation/agents.py#L150-L153) cash is floored
at zero, and the cash raised at [L175](simulation/agents.py#L175) is never applied to the committed
shortfall. It goes to debt service, then discretionary spending, then savings. So under the current
rule, access to credit can never lift a household out of committed-expenditure distress. With BNPL
on, that pushes the sign of the BNPL effect on default in one direction by construction.

- B1. Keep the rule. Zero code change, today's calibration stands, and the thesis already describes
  it. Fix the comment at [agents.py:177-181](simulation/agents.py#L177-L181), which quotes the other
  definition, and record the choice in `DECISIONS.md` under D7.
- **B2, recommended if an hour is available.** B1, plus the alternative as a robustness arm: a
  `distress_after_credit: bool = False` parameter, about four lines in `step()` that apply raised
  cash to the committed shortfall before testing what remains unmet, one `rob_distress_after_credit`
  arm, one test. Default off, so the golden check and the calibration are untouched. The thesis can
  then report whether the definition drives the result instead of only disclosing it.
- B3. Switch the baseline to the after-credit rule. Requires re-running `simulation.calibrate
  --reps 20` (420 baseline runs), updating `FITTED_*` in `experiments.py`, and only then the final
  run. Costs one night.

**Decision C — the mean-purchase comparator** (B32, R629 against R992). The standing recommendation
in `DEFECTS.md` is to keep all adopters as the comparison population and report a named miss with
the quintile bracket as its explanation. Whatever you choose, write the comparator and the tolerance
into `DECISIONS.md` **before** the run starts. Step 1.4 makes every candidate comparator computable
from tonight's output, so the decision cannot force a re-run.

**Review qualification 2 (the gate omits tax and statutory deductions) needs no code.** Appendix C
discloses it. The only action is in phase 2: step 2.2 edits the gate's call sites, and its
docstring must not be reworded into a claim of full regulatory coverage.

### Steps

**1.1 Pin SALib.** `sensitivity.py` imports it; neither manifest lists it. Installed version is
1.5.2. Add `SALib==1.5.2` to [requirements.txt](simulation/requirements.txt) and to the pip block of
[environment.yml](simulation/environment.yml). Keep the `scipy` pin: nothing in the repo imports
scipy, but SALib requires it (checked with `pip show SALib`), so add a comment saying so. This
withdraws the review's suggestion to drop it.

**1.2 Apply decision A (assuming A1).**
- [config.py:76](simulation/config.py#L76): `Activation = Literal["random", "uniform"]`. Update the
  `activation` field's `sweep` text at [L572](simulation/config.py#L572) to "MANDATORY: fixed-order
  robustness run".
- [model.py:141-144](simulation/model.py#L141-L144): delete the `synchronous` branch.
- [experiments.py:282](simulation/experiments.py#L282): loop over `("random", "uniform")`.
- [test_degenerate.py:177](simulation/tests/test_degenerate.py#L177): drop `"synchronous"` from the
  parametrize list.
- Regenerate Appendix B: `./env/python.exe notebooks/scripts/generate_param_register.py`.
- Hand-edit the three prose sites: [02_model.tex:209](thesis/chapters/02_model.tex#L209),
  [appendix_c_supplementary.tex:35](thesis/chapters/appendix_c_supplementary.tex#L35) and the
  drafting comment at L163. Wording: one re-run under a fixed activation order.
- [analysis.py:501](simulation/analysis.py#L501): the `"rob_act"` tornado row still works with two
  arms; no change.

**1.3 Apply decision B.** B1: comment and `DECISIONS.md` only. B2: as described above; add
`"distress_after_credit"` handling before step 1.5 so it is echoed automatically.

**1.4 Emit want-driven purchases by quintile.** Today only the overall mean reaches the summary, so
the B32 bracket table came from an ad hoc calculation. Change
[model.py:124-127](simulation/model.py#L124-L127) to take the agent's quintile and keep two
`Counter`s; emit `bnpl_want_purchases_{Q}` and `bnpl_purchase_mean_realised_{Q}` from
`summarise_run`. About eight lines. After the decision, replace the `xfail(strict=True)` at
[test_bnpl_parameters.py:209](simulation/tests/test_bnpl_parameters.py#L209) with a test that pins
the reported numbers for the chosen comparator.

**1.5 Echo every parameter in the run summary.** Replace the 24 hand-listed names at
[metrics.py:220-249](simulation/metrics.py#L220-L249) with `**dataclasses.asdict(p)`. This shortens
the code and also fixes a real gap: `shock_persistent`, `n_agents`, `bnpl_purchase_cv`,
`discretionary_floor` and `bnpl_instalments` are swept or sweepable but are identifiable in the
output only through the label. Two details:
- `n_agents` is both a parameter and an output. The output assignment comes later in the dict and
  wins, as it should. Leave it that way and say so in a one-line comment.
- Both test modules keep a hand-typed `_PARAM_ECHO` set
  ([test_degenerate.py:29](simulation/tests/test_degenerate.py#L29),
  [test_peer_channel.py:38](simulation/tests/test_peer_channel.py#L38)). Replace each with
  `set(ParamSet.__dataclass_fields__)`, or the control-arm equality tests will start comparing
  inputs.

This changes the parquet schema, which is why it sits in phase 1. It is this step or never.

**1.6 Emit all six credit-active band means.** In `summarise_run`, replace
[metrics.py:264-269](simulation/metrics.py#L264-L269) with
`**{f"active_{l}_mean": mean(f"active_{l}") for l, _, _ in CCMR_BANDS}`. Then
[analysis.py:379-386](simulation/analysis.py#L379-L386) becomes a loop over `bands` and stops
reconstructing 91–120 days as `90_plus − d120_plus`. Adds one column, `active_d91_120_mean`.

**1.7 Gate, then run.** Tests green, golden `check` green, commit, and record the commit hash next
to the run command in OVERVIEW step 4. Then start the final run.

---

## Phase 2 — behaviour-neutral cleanup inside `simulation/`

One commit per numbered step. Each must leave the golden check identical. About 120 lines removed.

**2.1 Delete what nothing reads.**
- [agents.py:21](simulation/agents.py#L21): unused `NEW_LOAN_APR, NEW_LOAN_TERM_MONTHS` import.
- [affordability.py:146-148](simulation/affordability.py#L146-L148): `monthly_to_tick()`.
- [population.py:70-74](simulation/population.py#L70-L74): `wage_share`. Also the `household_size`
  and `term_months` record fields and their two assignments in `build_records`.
- [config.py:584-585](simulation/config.py#L584-L585): `ParamSet.to_dict` (superseded by 1.5).
- [bnpl.py:25](simulation/bnpl.py#L25) `principal`; [bnpl.py:70-71](simulation/bnpl.py#L70-L71)
  `n_blocked_cut_off`, `n_originated` and their increments; `n_refused_default` in
  [lender.py](simulation/lender.py#L70). Grep the tests for each name before deleting.
- [calibrate.py](simulation/calibrate.py): the unused `statistics` import (L23), `refine()` (L90-95),
  the `--quick` flag (L102), the `best_table` alias (L157).
- [sensitivity.py:79](simulation/sensitivity.py#L79): the redundant `float()`.
- [experiments.py:51-53](simulation/experiments.py#L51-L53): the `PURCHASE_RATIO` alias; use the
  imported constant.
- [metrics.py:73](simulation/metrics.py#L73): the `"active_current"` key that the comprehension on
  the next lines overwrites.

**2.2 One Reg 23A gate, not three.** Call `nca_gate()` from
[lender.py:95-101](simulation/lender.py#L95-L101) and
[agents.py:399-404](simulation/agents.py#L399-L404) in place of the two inlined comparisons. They are
equivalent whenever the instalment is positive, and both callers guarantee that with an early
return. The golden `levers` arm exercises both sites. Leave the docstring's scope as it is.

**2.3 Sourced numbers from the sourced file.** [calibrate.py:117](simulation/calibrate.py#L117): the
`if "pct_d30" in ccmr` branch never fires, so the fitted 1–30 target is the literal `0.0824`. Read
it, and the `3.59` and `2.32` printed at L177-179, from
`ccmr_2017_baseline.json → combined_unsecured_and_facilities.pct`, as `analysis.py` already does.
Numerically identical today (8.24). No refit needed.

**2.4 Shrink, same logic.**
- [config.py:48-56](simulation/config.py#L48-L56): `ROOT = Path(__file__).resolve().parents[1]`.
- [affordability.py:141](simulation/affordability.py#L141): move the local import to the top.
- [population.py:32](simulation/population.py#L32): `PRODUCT_COLS = list(PRODUCT_MAP)`.
  [L144-150](simulation/population.py#L144-L150): one comprehension over `to_dict("records")`.
- [metrics.py:66-88](simulation/metrics.py#L66-L88): one `share(counter, labels, denom)` helper for
  the four band sums. [L198-208](simulation/metrics.py#L198-L208): two `Counter`s.
- [analysis.py:245-261](simulation/analysis.py#L245-L261): call `linear_departure()`, defined at
  L103. Hoist the three function-local imports. Drop the two repeated `FIGDIR.mkdir` calls.
- [calibrate.py](simulation/calibrate.py): one helper for the three identical table prints.
- [environment.yml](simulation/environment.yml): replace the pip pins with `- -r requirements.txt`.

**2.5 Optional, lowest value.** Remove the `rolling_limit` fallback and `limit_for()` from
[bnpl.py](simulation/bnpl.py#L50); tests pass `rolling_limits=defaultdict(lambda: 5000.0)`. Touches
12 test lines for 8 lines saved. Skip unless everything else is done.

Analysis-only edits (`analysis.py`, `calibrate.py` prints) cannot affect the golden run. Check them
by running `./env/python.exe -m simulation.analysis` against the existing `results/raw/` and
diffing `results/summary/*.csv` before and after.

---

## Phase 3 — notebooks and scripts

None of this touches model outputs. **Never overwrite `synthetic_population_5000.parquet` or
`synthetic_population_matched.parquet` in this phase.** The final run depends on them byte for byte.

**3.1 P2 imports the gate instead of retyping it.** In `p2_finscope_match.ipynb` cell 14, replace
the local Reg 23A table, `nca_necessary_expenses`, product map, `MIN_TERM_MONTHS` and amortisation
formula with imports from `simulation.affordability`, using the same two-line `sys.path` insert as
`generate_param_register.py`. Verify without re-drawing donors: load the existing matched parquet,
recompute `monthly_trad_repayment` with the imported functions, and assert it equals the stored
column. Do not re-execute the donor-draw cell.

**3.2 Delete the two stale notebooks.** `00_showcase.ipynb` and `p1p2_visualizer.ipynb` read three
columns no parquet has any more and fail at cell 2. `build_data_figures.py` is the thesis figure
source. Before deleting, confirm nothing in `thesis/` includes `quintile_archetypes.csv` or a figure
only they produce. Then update the two mentions in `OVERVIEW.md` and DEFECTS D6.

**3.3 Script root-finding.** In the four `extract_*.py` scripts replace `find_root()` with
`ROOT = Path(__file__).resolve().parents[2]`, as the other two scripts already do. Verify by
re-running each and confirming `git diff data/config/` is empty. `extract_qlfs_lmd.py` needs the
source PDF; if it is not on disk, skip that one.

**3.4 One copy of the shared notebook helpers.** `wgini` exists four times; the FinScope income
midpoints, quintile cut and flag recode exist three times. Put them in one module under
`notebooks/scripts/` and import. In the same pass, make `p4_validation.ipynb` and
[build_data_figures.py:226](notebooks/scripts/build_data_figures.py#L226) read the quintile bounds
from `nids_backbone_summary.json`, as P2 does, instead of retyping four numbers. Verify:
`p4_validation_summary.json` and `data_figure_numbers.json` unchanged after a re-run.

**3.5 Small deletions.** P4 cell 2: unused `FORMAL`, unused `G5`/`K7` columns, the dead
`if "dsti" not in df` guard, the repeated imports in cell 16. P2 cell 4: four unused columns.
`generate_param_register.py`: the `fmt_baseline` alias.

**3.6 One-off scripts.** `data/raw/IES_2022/convert.py` cannot run (a `StataReader` has no
`to_csv`) and nothing references it: delete. `quick.py`, `filter_vars.py` and `to_md.py` are
unreferenced one-offs; delete them if you no longer use them, otherwise leave them. Your call.

---

## Phase 4 — bookkeeping

- `OVERVIEW.md`: add this plan to the status table, tick decisions A–C as they are made, remove the
  two notebook references after 3.2.
- `DECISIONS.md`: D16 (one fixed-order arm), D7 (distress rule as decided), D4 (comparator and
  tolerance, dated before the run).
- `DEFECTS.md`: close or update B32 per decision C; add an entry for the identical activation arms
  and mark it fixed.
- `simulation/requirements.txt` header already says it is the reproducibility record; after 1.1 it is
  true.

## Deliberately left alone

The import-time Reg 23A self-check. The long `source=` strings in `config.py`, which generate
Appendix B. The separate `init_rng` stream. The nested-loop experiment grids and the frozen
`rq1`/`rq2`/`rq2t`/`rq3` keys. The test suite, apart from the three edits named above. Per-notebook
`find_root()` cells: a notebook's working directory is not fixed, so the walk earns its place there.

## Rough effort

Phase 0: 15 minutes, mostly the golden run. Phase 1 with A1, B1 and C unchanged: about an hour.
B2 adds an hour. Phase 2: two hours. Phase 3: two to three hours, mostly re-running P4 and the
figure script to verify.
