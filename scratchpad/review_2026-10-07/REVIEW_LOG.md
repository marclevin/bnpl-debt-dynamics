# Lead-editor review log, 2026-10-07

Baseline for this revision: commit `ad20b65` (last night's uncommitted edits, checkpointed
unchanged). The full reviewer reports are in this folder:
`01_experimental_audit.md`, `02_correctness_review.md`, `03_structure_review.md`,
`04_language_edit.md`, `05_coherence_review.md`, `06_revision_verification.md`.

Body prose: 9,803 → 9,879 words (cap 10,000; `scratchpad/wc_prose.py`). The thesis compiles to
117 pages with no undefined references or overfull boxes. `check_results_tables.py` passes
(43 numbers).

Only substantive items are logged here. Line edits for simplicity are not listed.

## 1. Experiment/paper discrepancies (fixed)

| # | Thesis said | Artefacts show | Fix |
|---|---|---|---|
| 1 | Lending, refusals and applications are post-burn-in sums (3.1, `tab:baseline-arms` note, Alg. 5) | Lender counters cover all 52 ticks (`lender.py:99-112`, `metrics.py:272-275`); so do purchase means, binding rates and "ever" measures | 3.1, the table note (build script) and Alg. 5 now state the right window for each measure |
| 2 | Arrears "track unpaid debt obligations" | Only traditional arrears are aged into CCMR bands; BNPL arrears are not | Section 2.3 corrected |
| 3 | Bureau and screening tests see "instalments and arrears" (no detail) | BNPL arrears enter both tests ×26/12, i.e. as if recurring monthly; traditional arrears enter neither (`lender.py:65`, `bnpl.py:152`, `agents.py:493`) | Stated in Section 2.2 |
| 4 | Calibration "fitted" on a grid (procedure not given) | Sequential three-stage fit plus a fine-grid check (`calibrate.py:121-164`) | One sentence added to 3.4 |
| 5 | Submodel 12: order-cap binding rate "reported by quintile" | Aggregate only | Corrected |
| 6 | Submodel 11: β = 0 control "reported in all comparisons" | Level-sensitivity arms run at β = 1 only | Corrected (also Appendix B) |
| 7 | 4.5: every sensitivity arm compared "on the same seeds" | Population-size and single-tick arms are unpaired | Corrected |
| 8 | Appendix C compared stacking shares across seed blocks (52.0→36.6, 85.1→22.0) | Same-seed figures are 52.6→36.6 and 85.2→22.0 | Corrected |
| 9 | `tab:effect` single-tick row printed ±0.02 ± 0.01 (looks like exactly 2 SE) | 1.1 and 1.2 SE | Build script prints this row to three decimals |
| 10 | Pseudocode: "Discard the first T₀ ticks; summarise the run" | Contradicts default counted from tick 1; Appendix F says the algorithms govern | Alg. 5 corrected |

## 2. Factual claims verified or newly evidenced

- **Single-tick shock cannot be calibrated** (4.5, `tab:robustness-appendix` note). No stored
  run supported this. Checked with `notebooks/scripts/check_single_tick_calibration.py` (output `results/summary/single_tick_calibration.json`; friction held at 0.09): the 90+ share stays at
  7.3–7.6% across the whole calibration grid (0.008–0.064, seeds 1,000–1,019), about half the
  14.21% target. The claim now cites this evidence.
- **Who defaults.** Default includes households with no debt (a food or rent shortfall alone
  counts as distress). Checked with `notebooks/scripts/check_defaulter_credit.py` (output `results/summary/defaulter_credit.json`): 90.5% of baseline defaulters
  owe traditional debt when they default, and 98.4% owe traditional debt or BNPL with BNPL on at
  β = 0. Added to Section 2.3 and the limitations index.
- **Agreements-cap diagnostic** (Appendix C). It predated the October code changes. Rerunning
  `results/corrections_2026-09-29/cap_definitions.md` on the current code reproduced it byte for
  byte.
- **β = 1 BNPL volume.** About R10,400 per eligible household per year (derived from
  `results_numbers.json`: R1,010 × 65.88/6.42), well above the provider band's upper end of
  R4,261. β = 0 is below the band, so the two settings bracket observed volume.
- All headline numbers in the abstract and Sections 3–6 were confirmed by the auditor against
  the generated tables, `results_numbers.json` or a recalculation from `results/raw`. The β = 1
  effect appears as 0.61 ± 0.11, 0.60 ± 0.11, 0.60 ± 0.12 and 0.60 ± 0.07. All four are correct,
  each for its own seed block or the pool.

## 3. Claims materially weakened

- "Default does not depend on routing / platform count" (4 places) → "does not change
  detectably", with the effect sizes the design cannot exclude (about 0.2 and 0.25 points).
- "Neither rule shows a tipping point" → there is no adoption cascade in holding, but the absence
  of a tipping point in default is not established.
- Pattern 1: the post hoc "the lender-choice hierarchy stands" is removed. The arrears rise
  partly follows from paying BNPL instalments before traditional debt, so Pattern 1 does not
  test the lender-choice rule. The ever-stacked share is no longer counted as corroborating
  evidence, because the routing assumption sets it.
- The bureau effect (0.22) was described as "more than" the BNPL effect (0.12). The difference,
  0.10 ± 0.06, is not detectable, so the text now says "comparable".
- "Mostly in the lowest quintile" → "largest in the lowest quintile". Q1 accounts for about
  55–60% of the rise.
- The bureau-visibility result: a new paragraph in Section 5 says the model's rules favour a
  rise. The lender refinances the whole shortfall over 25 months on surveyed income, refused
  households have no fallback, and loan costs partly fall after the run. It also says the switch
  was not run under the alternative borrowing rules.
- The fitted shock rate: "illness, unexpected bills or family changes" was dropped, because the
  shock only reaches wage-dominant households. The text now says the fit depends on the
  measurement window (everyone starts current; nothing is written off).
- RQ2 premise: the thesis now says no arm gives platforms a shared view of exposure. The effect
  of platforms not seeing one another is therefore not isolated, and the nearest comparison is
  mandatory screening.
- The abstract and RQ1 answer now report the misses (intermediate arrears bands, debt-to-income
  profile, purchase size) and the unvalidated level of default. They no longer summarise RQ1 more
  favourably than Section 3.5 does.

## 4. Claims strengthened or reframed

- **β = 0 against β = 1.** The old reason (β = 1 stacks more than CFPB) rested on a share the
  routing assumption sets. The new reason uses volume: the two settings bracket the provider's
  volume, β = 0 is closer on both measures, and because the effect grows with borrowing, the
  β = 0 effect probably understates the effect at market volume.
- The conclusion now answers the main question in its own words and states the pattern across
  the results: default follows borrowing volume and refusals by the traditional lender, not the
  number of platforms owed. It reports the quintile finding for the BNPL effect (Q2–Q4, not Q1),
  which was previously dropped, and gives a short, conditional implication for the reporting
  arrangements.

## 5. Structural changes

- **Section 3.1 is now "Simulation Protocol".** It collects measurement windows, replication and
  seeds, and the detectability convention, which was moved from the Results opening. A new
  `tab:experiments` lists every experiment with its factors, β values, replicates, seed block and
  results table, and defines the access rate.
- **One definition of the outcome** (default, plus the 90+ share) now sits in Section 1.2. The
  introduction also gains a short preview of findings, as in the supervisor's paper.
- **Section 5.** The switches are defined once (Section 2.2), and Submodel 15 and the Section 5
  opening point to that definition. The first finding now comes before the floats. The levers
  paragraph is cut to two sentences; the agreements-cap diagnostic now lives only in Appendix C.
- **Appendix E.** The construction-fidelity floats (`tab:imputation_errors`,
  `fig:inclusion-fidelity`, `fig:pop-fidelity`) moved here (new E.5). The body keeps their
  sentences and references.
- **Limitations index (Appendix C).** It now has twelve central rows. "Default is a model
  construct" is new. "Income at the gate" moved up, because it bounds RQ3. The window dependence
  of the fit and the untested switches were added.
- Section 4.2 is retitled "Stacking Across Platforms". "Invisible credit" had conflated the
  bureau gap with platforms not seeing one another.
- Terminology now holds throughout: **random/loyal routing**, **mandatory screening**,
  **default threshold** (the word "horizon" is kept for the run length only).

**Considered and not done.** These were recommended by the structure or coherence reviewer. Each
is reasonable, but each is a larger reorganisation than the gain justifies this close to
submission:
- moving the BNPL-on checks out of RQ1 into Results;
- reordering Results to follow RQ2's wording;
- removing the parameter column from the submodel table;
- moving `tab:stacking`, `tab:access` and `tab:robustness` to the appendix;
- a separate Discussion chapter.

The coherence problems these would solve were instead handled with cross-references and
de-duplication.

## 5b. Fixes after the independent verification of this revision (`06_revision_verification.md`)

The verifier confirmed every new number. It also found three overclaims and one contradiction
that this revision had introduced, all now fixed:
- **Pattern 1.** The new text said it "does not test" the lender-choice rule, while
  `tab:patterns` treats it as a test. It now says that, as specified, the interest measure
  falsifies the rule, and that neither measure discriminates well.
- **"Default follows how much households borrow."** Borrowing more on a shortfall *lowers*
  default, and larger purchases at β = 0 leave the effect unchanged. This is now limited to
  peer-driven BNPL borrowing.
- **"The β = 0 effect probably understates the effect."** Now "may understate, if the missing
  volume comes from more frequent borrowing".
- **Quintile result.** Now attributed to `tab:distribution`, not the access sweep.
- **Smaller fixes:**
  - "May favour" in Section 5, and "a stricter counterpart of" the FCA check.
  - The deleted lever caveat is restored in Appendix C.
  - The friction scope of the single-tick check is now stated.
  - The check scripts moved to `notebooks/scripts/`.
  - Section 3.1 is renamed "Runs, Replications and Inference" so it no longer clashes with 3.4.
  - The Appendix E references are tidied.

## 5c. Final simplicity pass

I read every body chapter once more for simplicity only. These were line edits, with no change to any claim or number:
- I split long sentences in 1.4, 2.2, 3.1 and 3.3.
- I removed a repeated "no adoption cascade" sentence (4.3) and a repeated bureau-refusal clause in the conclusion's opening paragraph.
- I untangled the β = 0 volume paragraph in 4.1.
- I replaced "mutual blindness" with "platforms not seeing one another" (4.7), matching the conclusion.

I spot-checked the conclusion's 0.37–1.27 range against `tab_effect`. The thesis builds with no undefined references, and `check_results_tables.py` still passes.

## 6. Unresolved: needs your input

1. **RQ1 wording.** "Benchmarks not used in fitting" became "external comparisons not used in
   fitting", because "benchmark" also names a model arm. The RQs were approved by your supervisor
   on 2026-09-09, so confirm this is acceptable or revert it.
2. **Abstract length** grew from about 225 to about 265 words to carry the validation misses, the
   definition of default and the volume bracket. Check the departmental limit.
3. **Experiments the examiner may ask for.** None were run, because each changes results rather
   than text:
   - (a) the bureau switch under the "+25%" and "credit pays committed shortfall first" rules,
     or over 104 ticks;
   - (b) following refused against granted households;
   - (c) a four-platform arm with a shared aggregate limit, to isolate platforms not seeing one
     another from capacity;
   - (d) refitting the shock rate on another window (e.g. final-tick 90+), and the effects at the
     QLFS upper bound.

   (a) and (c) are the most likely viva questions (`02_correctness_review.md`, M3 and M4).
4. **Default level has no benchmark.** If you know a usable figure (e.g. the NCR Credit Bureau
   Monitor's impaired-record share), a one-line comparison would strengthen Section 3.5.
5. **Novelty claim** ("We found no comparable South African study"). There is still no record of
   the search (DEFECTS B9).

## 7. Could not be verified from stored artefacts

- The fine-grid calibration runs (1.5% → 13.93%) exist only as a summary in `calibration.json`;
  `calibrate.py` does not save stage-4 runs.
- "Specified before the run" claims (threshold rule, Pattern 3 statistic, mean-purchase
  comparison) can be traced only back to 2026-08-13, where git history starts.
- Data-layer figures 12.6% (median non-food share of credit payments) and 11.2% (Appendix C) are
  not in any `data/processed` JSON; presumably they are in `notebooks/p4_validation.ipynb`.
- Several correct prose numbers are typed rather than generated: the threshold-minus-control
  rises, want-off refusals and lending, effect-block refusals, the single-tick no-BNPL default,
  and R10,400. (90.5%, 98.4% and 7.3–7.6% now come from the two new JSON files.) Adding them to `results_numbers.json` would let
  `check_results_tables.py` cover them.
