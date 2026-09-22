# Results integration plan

Drafted 2026-09-22 after the final run of 2026-09-21 (commit `be45867`, `results/final_run.log`
ends `FINAL RUN COMPLETE`). Status: **draft, nothing executed.** It carries out OVERVIEW steps 6
and 7, and follows steps 5 to 11 of the rewrite sequence in
[SOL_PLAN_REFORMAT.md](SOL_PLAN_REFORMAT.md).

## Does the experiment align with the documents?

**In design, yes.** Every grid the three unwritten sections call for was run, at the replicate
count the drafting notes specify, with the controls the claim-control checklist requires:

| Document requirement | Delivered |
| --- | --- |
| RQ2 stacking half: platforms 1–6, each against beta, one-platform case showing zero cross-platform stacking (`04_results.tex` notes; SOL 4.1) | `rq1`, 600 runs; 2+ share is 0.0% at N=1 in both beta arms |
| RQ2 access half: access x beta with the beta=0 row, linear and Granovetter together, gamma=0 control (SOL 4.2) | `rq2` 700 runs, `rq2t` 1,460 runs, controls present |
| RQ3: benchmark x bureau x screening, crossed with beta 0/1, the 2x3 panel (SOL section 5; `05_policy.tex`) | `rq3`: all six cells, 20 replicates each |
| Cooling-off and cap runs for Appendix C only | `rq3`: k_cool 1–4 and cap 1–3, both betas |
| Robustness: three amount rules capped and uncapped on matched seeds, activation order, k, population size, min-payer share, kappa, lambda, purchase base | `robustness`, 620 runs, 31 arms; the amount-rule pairs share `seed0=50_000` |
| Sobol at N >= 256 | 4,096 runs at N=256 |
| 20 replicates, seeds reproducible, no BNPL-side re-tuning | every arm 20 x unique seeds; shock 0.016 and friction 0.09 in every run |

**In output, one gap, and it matters.** The introduction promises results "by income quintile",
SOL 4.3 asks where debt service and default concentrate by quintile, and the scenario panel asks
for "quintile breakdowns" in every cell. The run summary carries by-quintile debt-to-income,
rolling-limit binding and purchase size, but **not default, adoption or arrears by quintile**. It
also has no "ever stacked over the horizon" measure, which the stacking section needs for a
denominator matched to the CFPB comparison. Phase 0 closes this; it is cheap because the model is
deterministic from its seed.

**In expectation, two things the plan assumed did not happen, and the drafting notes already say
not to assume them.** Both are findings to write, not problems to fix:

1. **Default does not rise with platform count.** SOL section 5 grounds the policy argument on
   "default rising with platform count". It does not: six platforms less one gives −0.04pp ± 0.09
   (beta 0) and +0.18pp ± 0.10 (beta 1). Stacking is emergent and large (45% of holders at four
   platforms, 83% with peers), but default responds to the injection itself (+1.22pp ± 0.11 without
   peers, +2.07pp ± 0.10 with) and not to how many firms it is spread across. The RQ2 answer is
   therefore "yes, and no", and the policy argument needs rewording (decision B below).
2. **Bureau visibility is not a near-null at beta 0.** It is +0.26pp ± 0.11 (2.4 s.e.), the wrong
   direction for a protective instrument: the gate refuses more traditional applications (1,160
   against 1,033) and the refused households do worse. At beta 1 it is a null (+0.04pp ± 0.12).
   The checklist line "the bureau-visibility near-null result is reported without being reframed
   as model failure" still applies to the beta 1 cell; the beta 0 cell is a small adverse effect
   and is written as one.

Smaller discrepancies, each handled in the phase that touches it: Pattern 1 is mixed (arrears up,
interest paid down); the Conclusion budget is 650 words in SOL and 800 in the `06_conclusion.tex`
note; the scenario figure must show body scenarios only; the Appendix C notes quote working-run
magnitudes; the CFPB 32% and the model's 45% use different denominators; and the projected total is
about 9,570 words against the 9,500 ceiling.

## Decisions needed from Marc

**A. Re-run scope for the missing columns.** Adding columns to `summarise_run` cannot change any
existing column, and re-running a suite with the same seeds reproduces it bitwise (proved by the
golden checks during the cleanup). Recommended: **re-run all six experiment suites** (67 minutes)
so every reported number comes from one commit, and keep the Sobol output, which decomposes five
outputs that are unchanged. The alternative, re-running only `rq0`, `rq1` and `rq3` (about 20
minutes), leaves the results split across two commits for no saving that matters.

**B. How the policy argument is grounded now.** SOL said: stacking evidence, including default
rising with platform count, corroborates the null policy results. Recommended rewording: the
mechanism produces stacking; stacking does not translate into more default per platform; the two
real instruments act on the individual agreement and do not move default either; what moves
default is the injection itself, and the only lever that reverses it is the hypothetical cap,
which works by blocking any new draw while a balance is open (see the note in Phase 2). This is a
weaker policy story than planned and an honest one.

**C. Conclusion budget: 650 or 800 words.** Recommended 650, the SOL figure, because the projected
total is already about 70 words over the ceiling.

**D. Ever-stacked measure.** Recommended yes, added in Phase 0 since the re-run happens anyway:
the share of households that held two or more facilities at any tick, and the same share among
households that ever adopted. It is the closest the model can get to the CFPB's "borrowers with
loans at multiple firms" over a period.

## Phase 0: close the output gap and re-run (about 1.5 hours, mostly compute)

1. In `simulation/metrics.py` `summarise_run`, add per quintile: `default_rate_final_{Q}`,
   `bnpl_adoption_final_{Q}` and `trad_arrears_final_{Q}` (share of the quintile's households
   with traditional arrears at the final tick). In `simulation/model.py` keep a set of households
   that have held two or more facilities at any tick, updated in `collect_tick`, and emit
   `ever_stacked_2plus` (share of all households) and `ever_stacked_2plus_of_adopters` (share of
   households that ever held a BNPL balance, which needs a second set). About 20 lines.
2. One test: the by-quintile defaults weighted by quintile size reconcile with `default_rate_final`,
   as `test_purchases_by_quintile_reconcile_with_the_overall_figures` does for purchases.
3. Re-run per decision A: `./env/python.exe -m simulation.experiments --which all --reps 20`,
   then `-m simulation.analysis`. Do not re-run Sobol. Before overwriting, copy the current
   `results/raw/*.parquet` to the scratchpad; after, assert every one of the 115 existing columns
   is equal to the copy, row for row. If any differs, stop: the model changed and the run is not
   the run.
4. Commit the code, the regenerated figures and the updated `results/final_run.log` note. Record
   the new commit in OVERVIEW step 4 as "re-run for the by-quintile columns; existing columns
   bitwise identical".

## Phase 1: build the evidence blocks (tables and figures) before any prose

The rule from SOL: every result in the Abstract and Conclusion traces to one final table or figure,
and each RQ has one clearly identified evidence block. Numbers must never be typed into prose or
captions; they are generated. Two scripts, both in `notebooks/scripts/`, in the style of
`build_data_figures.py` (its colours, text width `TW = 5.78`, PDF output to `thesis/figures/`) and
`generate_param_register.py` (generated `.tex` with a "do not edit" header):

**`build_results_figures.py`** writes the five body figures SOL expects, plus one for the appendix:

| Figure | Source | Notes |
| --- | --- | --- |
| `fig_baseline_arrears.pdf` | `rq0` baseline arm, `load_ccmr_bands()` | replaces the PNG; mark fitted bands |
| `fig_stacking.pdf` | `rq1_stacking.csv` | 2+ share by platform count, both betas, CFPB 32% as a dashed order-of-magnitude line with its denominator named in the note |
| `fig_access_default.pdf` | `rq2_surface.csv`, `rq2_threshold_surface.csv` | two panels: linear arm (beta rows, control in black) and threshold arm (adoption and default side by side) |
| `fig_scenarios.pdf` | `rq3` raw | **body scenarios only** (benchmark, bureau, screening) at both betas with error bars; the cooling-off and cap arms are excluded |
| `fig_tornado.pdf` | `robustness.csv` | provenance colouring as now; uncited rules in red |
| `fig_scenarios_appendix.pdf` | `rq3` raw | all levers, both betas, cap marked hypothetical |

**`build_results_tables.py`** writes generated `.tex` fragments under `thesis/chapters/generated/`:

| Table | Content | Section |
| --- | --- | --- |
| `tab_baseline_arms.tex` | `baseline_no_bnpl`, `bnpl_on_beta0`, `bnpl_on_beta1`: default, 90+ credit-active, traditional arrears rate, traditional interest, new traditional lending, adoption, 2+ share, ever-stacked; mean and sd over 20 replicates | 4 opening |
| `tab_stacking.tex` | platforms 1–6 x beta: 2+ share of all households, of end holders, ever-stacked of adopters, default | 4.1 (endpoints in body, full in Appendix C) |
| `tab_bnpl_on_checks.tex` | the unfitted BNPL-on checks: 2+ share vs CFPB 32%; volume per eligible household R1,321 vs the R1,333–R4,261 band; mean purchase R645.60 vs R992 (pass by R0.74, 8/20 inside); Pattern 1 direction; Pattern 3 peak; Pattern 4 25.9% vs 36% | 3 (the 250-word RQ1 close) |
| `tab_scenarios.tex` | the 2x3 panel: each cell default, 90+ arrears, adoption, cumulative volume, plus the by-quintile default from Phase 0; differences to the benchmark with one s.e. in the note, not as a delta column | 5 |
| `tab_distribution.tex` | by quintile: default, adoption, arrears, aggregate DTI, rolling-limit binding (Q1 25.7% to Q5 7.3%), mean purchase | 4.3 |
| `tab_robustness.tex` | the arms that move the answer: amount rule (13.30% to 15.54%, capped and uncapped, paired seeds), k (16.79% vs 15.45%), kappa, purchase base; the rest in Appendix C | 4.4 |
| `tab_sobol.tex`, `tab_activation.tex`, `tab_popsize.tex`, `tab_minpayer.tex`, `tab_cooloff.tex`, `tab_cap.tex` | Appendix C required content | C |

Every generated table carries a `\tabnote` written in the script with: outcome definitions,
denominator (all households / credit-active / banked-eligible / holders), replicates and seed
scheme, the uncertainty convention (one unpaired s.e. on differences; paired only for the
amount-rule arms), and the control arm. This is the float-note requirement in every drafting note,
done once in code.

Verification for the phase: the thesis compiles with every fragment included and no float
overflows the text width; a script re-derives three numbers per table directly from `results/raw`
and asserts they match the fragment.

## Phase 2: write the prose, in SOL order

Budgets are prose only; captions and tables are free. Written so far: 5,024 words.

**2.1 Results (`04_results.tex`, 2,100 words).** Opening 100: baseline 13.40% default, 90+ 13.68%
vs 14.21%, 20 replicates, replicate sd about 0.35pp, one s.e. on a difference about 0.10pp, the
banked ceiling 82.8%, credit-active 44.6%. Then:

- *4.1 Stacking (550).* Emergent, not coded: zero at one platform, 6.4% of all households at two,
  7.6% at four, 8.0% at six (beta 0); 43.7% to 57.0% with peers. Among end-of-horizon holders 45%
  and 83%, against the CFPB's 32%, with the denominator difference stated (point-in-time holders
  here; borrowers with loans at multiple firms over a period there); the ever-stacked figure from
  Phase 0 is the closer analogue. Then the negative: default does not rise with platform count.
- *4.2 Access and peers (750).* The bold lead: default rises smoothly with access under both
  mechanisms; no threshold. Linear R² 0.98 to 0.99 in every arm including beta 0; amplification
  1.7x (+1.41pp to +2.36pp across the access range). Granovetter: adoption rises up to 49.8pp
  across the range and default 1.3 to 1.7pp, both near-linear; mu_theta moves adoption (50% to
  26%) and not default (14.9% to 14.8%). The structural reason from `sec:no-cascade`. Pattern 1
  here, written as mixed: arrears rate up (+0.64pp, +1.14pp), traditional interest paid down
  (−2.1%, −1.7%) because BNPL-first diverts borrowing (new traditional lending R6.57m to R3.48m).
- *4.3 Distribution (350).* From `tab_distribution`. The limit binds hardest at the bottom (Q1
  25.7% of requests) and barely changes default (lambda 0.1 to 1.0: 15.60% to 15.54%) because it
  trims purchase size; aggregate DTI peaks in Q4 (1.49) with Q1 second (1.32), the mean of ratios
  peaks in Q1. Report by-quintile default from Phase 0 before saying where harm concentrates.
- *4.4 Robustness (350).* Amount rule first (uncited; 2.2pp range; the plus-committed rule lowers
  default because it over-borrows into savings, say so); k; kappa; purchase base. One sentence
  each for activation order (15.42% vs 15.47%), population size (15.05 / 15.42 / 15.49%), min-payer
  share (flat), Sobol (shock probability carries the variance in the *level* of default, S1 1.02 ±
  0.15; every BNPL parameter ST <= 0.02; this says nothing about the BNPL *effect*, which is a
  difference between arms). The single-tick shock arm (5.66%) explains why persistence is needed.

**2.2 Scenarios (`05_policy.tex`, 1,150 words, definitions already written and counted).** The
panel from `tab_scenarios`. Bureau visibility: +0.26pp ± 0.11 at beta 0 with the mechanism (more
refusals at the gate) and the affordability-only scope in the same sentence; +0.04pp ± 0.12 at beta
1. Screening: +0.02pp ± 0.10 and −0.05pp ± 0.10. Volume: both instruments leave cumulative volume
within 2%, so neither defers nor deters. Interpretation per decision B. Close with the RQ3 answer:
neither instrument changes distress in the affordability channel, with or without peer adoption;
the scoring channel is outside the model. The cap and cooling-off go to Appendix C with one
sentence pointing there. Note for the appendix text: **cap = 1 is stricter than a single
platform.** With one platform a household can hold several loans on it; the cap blocks any new
draw while any balance is open. That is why cap = 1 (13.36%) sits below the one-platform arm
(14.56%) and near the no-BNPL baseline (13.40%): it is a one-agreement-at-a-time rule, and it
should be described as such rather than as a facility count.

**2.3 The RQ1 close (`03_calibration.tex`, the 250-word block).** From `tab_bnpl_on_checks`. Close
RQ1 in one sentence naming every failure: the intermediate arrears bands (0.94% and 0.96% against
3.59% and 2.32%), the servicing-share check, the mean purchase at the edge of its band. Section 3
is at 1,839 against a 2,000 budget, so this block is 150 words or the section is trimmed by 90.

**2.4 Conclusion (`06_conclusion.tex`, 650 per decision C).** Four paragraphs per SOL. The RQ
answers: RQ1 partly (calibrated on two bands, three of four external checks, named failures); RQ2
yes then no (stacking emerges; default does not scale with platform count; the response to access
is smooth under both mechanisms); RQ3 neither instrument moves default in the affordability
channel, peer adoption doubles the injection's effect but changes no policy conclusion. Future
work compresses from 330 to about 160 words.

**2.5 Introduction preview and Abstract.** Preview of about 120 words at the marked comment;
abstract 250, every number traced to a Phase 1 table. Both written last.

**2.6 Superseded text.** Remove the working-run magnitudes from the Appendix C comments (−33%,
−54% to −63%), the "default rising with platform count" sentence in SOL section 5, and the stale
"Final simulation outputs do not exist" in SOL step 1.

## Phase 3: verification and bookkeeping

- Compile clean: no undefined references, no overfull boxes, no missing figures.
- `./env/python.exe scratchpad/wc_prose.py` under 9,500 (projected 9,570 before the compression
  pass; step 11 of SOL removes the difference).
- Walk the claim-control checklist in SOL line by line; the two lines that need care are the
  bureau near-null (true at beta 1 only) and "default rising with platform count" (false; the
  policy argument must not rest on it).
- Terminology and duplication audits per SOL's completion criteria.
- `tab:further-caveats` still points at the right sections after the new prose.
- OVERVIEW: step 6 done, step 7 (compression) next; DEFECTS B32 closed with the final number;
  DECISIONS D4 gets the outcome line. Memory: update `final-run-2026-09-21`.

## What this plan does not do

It does not change the model, the calibration or any experiment grid. Phase 0 adds output columns
only, and proves it. It does not revisit the pre-registered tolerance for the mean-purchase check.
It does not write the results for the cooling-off window or the cap into the body.

## Rough effort

Phase 0: 20 minutes of code, 67 minutes of compute, 10 minutes of verification. Phase 1: half a
day; the scripts are the work, the figures are then free. Phase 2: two days of writing at the
budgets above. Phase 3: half a day.
