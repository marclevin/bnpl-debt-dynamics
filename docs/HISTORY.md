# Project history

Dated record of the changes that altered the model, its results or the thesis's claims. The
current position is always the thesis text, `results/summary/results_numbers.json` and
[`DEFECTS.md`](DEFECTS.md) (open items). Detail not kept here is in git history; the commit
that removed each source file is noted under its entry. Design choices and their reasons are in
[`DECISIONS.md`](DECISIONS.md).

Earlier history (model build, 2026-08-05 to 2026-09-28) is in the closed rows of
`DEFECTS.md` and in the full defect log at `git show 3b79e3c:scratchpad/DEFECTS.md`.

---

## 2026-09-29: implementation defects corrected and every suite rerun

State before: tag `pre-correction-2026-09-29` (commit `5694751`). Six implementation defects
were fixed, the model recalibrated (the fitted values did not change) and every suite rerun.
Defect 5 accounted for almost all of the BNPL effect previously reported: at fixed parameters
the beta = 0 effect fell from +1.22 to +0.03 points. Full record, scripts, the before-and-after
table and the step-by-step diagnostic outputs: `git show ca9ae96:results/corrections_2026-09-29/`
(`CORRECTIONS.md`, `BEFORE_AFTER.md`, `REPRODUCE.md`). The superseded outputs were moved to the
system trash on 2026-10-07; they can be regenerated from the tag.

### Confirmed implementation defects, corrected

| # | Defect | Evidence on the original code | Correction | Commit | Tests |
|---|---|---|---|---|---|
| 1 | **Traditional interest was charged twice.** Interest was added to the balance at accrual, and the payment then reduced the balance by the payment less interest. | R1,000 at 1% a tick with R100 paid left R920, where 1000 + 10 − 100 = 910. A loan amortised over 12 ticks took 15 to clear and cost R1,144 against a contract total of R1,066. | The whole payment comes off the balance. | `b483ea1` | `test_debt_accounting.py` |
| 2 | **Arrears were counted twice in total debt.** An unpaid instalment stays inside the balance, and `total_debt()` added arrears to it again. Affects the debt-to-income statistics only. | Balance R1,010 with R100 in arrears reported R1,110. | Arrears are no longer added. The amount due is also capped at the balance. | `b483ea1` | `test_debt_accounting.py` |
| 3 | **A cleared debt kept its instalment.** `scheduled_service_tick` was never reset, so the bureau went on showing the lender the service of a loan that no longer existed, and the gate refused credit on it. | After the 12-tick loan cleared the gate was still shown R88.85 a tick. | Scheduled service and arrears return to zero when the balance clears. | `b483ea1` | `test_debt_accounting.py` |
| 4 | **The next BNPL instalment was collected in the tick an agreement was opened**, on the shortfall path only, because that path borrows before it pays. Half the purchase was paid at once. The contract is 25% at checkout and 25% at each of the next three ticks. | A shortfall agreement of R200 ended its opening tick with two instalments remaining; a want-driven purchase ended it with three. | Agreements record the tick they were opened in and collection skips them until the next tick. | `d3352c4` | `test_shortfall_path.py` |
| 5 | **The checkout quarter of a shortfall agreement was requested from neither lender.** BNPL relieves a shortfall by three quarters of the amount financed, because a quarter is paid at checkout (DECISIONS.md, D5). The traditional lender was asked for the request less the *whole* amount financed. A household that used BNPL for a shortfall therefore stayed short, and was recorded as distressed, whatever either lender was willing to grant. | Shortfall R200: with traditional credit alone the household borrowed R200 and was not distressed. With BNPL enabled it financed R200, received R150, made no traditional application, paid R100 of the R200 due and was recorded as distressed. | The traditional lender is asked for the request less the cash BNPL freed. A refusal still leaves the shortfall unpaid and the tick distressed. | `1415625` | `test_shortfall_path.py` |
| 6 | **Late fees could exceed the purchase price.** Payflex caps late fees at "the lower of R285.00 (including VAT) or 50% of the Purchase Price" (terms and conditions, read 2026-09-29). The model applied the Rand cap only. | A R200 purchase could accrue R285 (nominal) in fees. | The cap is the lower of the two. The share is a sourced parameter, `bnpl_late_fee_cap_share`. | `f40e4bf` | `test_bnpl_schedule.py` |

Defect 5 is the one that matters for the thesis. At fixed parameters and on the same seeds it
accounts for almost all of the effect of BNPL on default that the thesis reported
(`diagnostic_summary.md`). It is classified as a defect, and not as a modelling assumption,
for two reasons. The decision register defines what BNPL covers: the household "pays only 25%
at checkout, and the other 75% stays in its pocket", and "traditional credit is approached for
shortfalls BNPL cannot cover". And Submodel 4 has the household request its shortfall; under
the old arithmetic its two requests together always fell short of it.

Because the classification decides the headline result, the earlier behaviour is kept as an
explicit alternative assumption, `shortfall_checkout_financed = False`, and run as one arm of
the effect suite. The thesis reports both.

**Diagnostic at fixed parameters** (shock probability 0.016, friction 0.09; seeds 10,000-10,019,
paired, one SE):

Seeds 10,000-10,019 in every arm and at every step; differences are paired by seed, with one standard error. Default is the share of all households in default at the final tick.

|                                            | original code   | + interest and payment accounting   | + instalment timing   | + traditional fallback request   | + late-fee cap (all corrections)   |
|:-------------------------------------------|:----------------|:------------------------------------|:----------------------|:---------------------------------|:-----------------------------------|
| commit                                     | 5694751         | b483ea1                             | d3352c4               | 1415625                          | f40e4bf                            |
| default, no BNPL (%)                       | 13.40           | 13.31                               | 13.31                 | 13.31                            | 13.31                              |
| 90+ credit-active, no BNPL (%)             | 13.68           | 14.20                               | 14.20                 | 14.20                            | 14.20                              |
| BNPL effect, beta=0 (pp)                   | +1.22 ± 0.13    | +1.15 ± 0.11                        | +1.11 ± 0.09          | +0.06 ± 0.09                     | +0.03 ± 0.09                       |
| BNPL effect, beta=1 (pp)                   | +2.07 ± 0.10    | +1.99 ± 0.12                        | +2.09 ± 0.09          | +0.47 ± 0.13                     | +0.61 ± 0.11                       |
| shortfall path only (pp)                   | +1.20 ± 0.10    | +1.16 ± 0.12                        | +1.20 ± 0.09          | +0.07 ± 0.08                     | +0.07 ± 0.08                       |
| bureau less benchmark (pp)                 | +0.03 ± 0.08    | +0.12 ± 0.07                        | +0.15 ± 0.07          | +0.20 ± 0.11                     | +0.20 ± 0.10                       |
| screening less benchmark (pp)              | -0.06 ± 0.11    | -0.04 ± 0.10                        | +0.02 ± 0.11          | -0.01 ± 0.09                     | +0.02 ± 0.09                       |
| cap 1 less benchmark (pp)                  | -1.26 ± 0.11    | -1.14 ± 0.13                        | -1.01 ± 0.10          | -0.01 ± 0.10                     | +0.12 ± 0.10                       |
| cap 2 less benchmark (pp)                  | -1.18 ± 0.10    | -1.07 ± 0.09                        | -1.08 ± 0.09          | +0.02 ± 0.12                     | +0.04 ± 0.11                       |
| new traditional lending, BNPL beta=0 (R m) | 3.48            | 3.28                                | 3.43                  | 5.42                             | 5.43                               |
| BNPL volume, beta=0 (R m)                  | 5.47            | 5.45                                | 5.34                  | 6.42                             | 6.42                               |

### Inaccurate descriptions, corrected in the text (no change in behaviour)

| Subject | What the code does | What the text said |
|---|---|---|
| **The hypothetical cap** | Counts platforms on which the household owes a balance. A household at the cap is refused every new draw, including a draw on a platform it already uses. Below the cap it may open further agreements on a platform in use, so under a cap of two or three it can hold more agreements than the cap. A cap of one is one agreement at a time. | "A cap on concurrent agreements"; "a count of open agreements on any platform, not of platforms". |
| **Platform routing** | Every request goes to the platforms in a random order, redrawn for the request, and what one platform does not finance passes to the next. With four platforms a second request reaches a different platform first three times in four, although the first has headroom. | "Stacking arises from borrowing requests and the available platform headroom"; "emerges although no rule assigns households to several providers". |
| **Screening gate** | Is shown the household's traditional service and its BNPL instalments on every platform, whether or not the bureau switch is on. | "The same affordability gate applied to BNPL originations", with no statement of what it is shown. |
| **Switches "crossed"** | Each switch was crossed with peer influence only. No arm ran both switches. | "Crossed". An arm with both switches has been added (`rq3_both`, seeds 44,000–44,019). |
| **Default** | Absorbing, counted from tick 0, over all 5,000 households. The final-tick rate is the share that defaulted at any tick, burn-in included. | "In default at the final tick", which is correct but does not say the measure is cumulative. |
| **Income at the gates** | Both gates use income at initialisation. An unemployment spell does not reduce it. | "Declared gross income". |
| **Committed shortfall** | A committed-expenditure shortfall is recorded as distress and is not carried forward. Cash borrowed against it is spent on debt service, then discretionary spending, and the rest is saved. | "Remains recorded as distress even if later borrowing supplies enough cash to cover it", which implies the loan pays for the expenditure. |
| **Debt service in the distress test** | The amount due: the instalment or minimum payment plus arrears, and the BNPL instalments due. | "Scheduled debt service". |
| **Rolling limit** | The count is of platform requests that the limit truncates or refuses, over every platform a request reaches. | "Requests refused by the limit". |
| **Late-fee cap** | Per agreement, over its life. | The parameter register said "per missed instalment". |
| **Seed blocks** | The sensitivity groups, the scenario arms, the cap arms and the threshold-mean arms each have their own block. | "Arms within a suite share seeds, except in the scenario suite". |
| **Imputed product flags** | BNPL eligibility uses the banked flag only. The five product flags price opening traditional debt. Stacking follows from routing. | "The joint structure that cross-platform stacking depends on". |
| **Initial vulnerability** | Of the 5,000 agents, 45.2% start with no liquid savings, 3.6% with income below committed expenditure and 5.1% with income below committed expenditure plus service. | 44.3%, 3.9% and 5.2%, which are the figures of the validation summary and not of the agents. |
| **Parameter register** | Runs use the fitted shock probability 0.016 and payment friction 0.09. | The register printed the code defaults 0.01 and 0.0, decision numbers in place of submodel numbers, and development notes. |

The cap follows the register ("a maximum on concurrent facilities"; a facility is a platform
relationship with a balance) and the code was written to it, so the code is unchanged and the
text is corrected.

### Marc's decisions of 2026-09-29, and what was done

Where this subsection differs from those above, it is the position adopted.

**The corrected shortfall rule is the only one.** Marc confirmed that defect 5 was a defect:
a household is distressed only if the lender refuses. The alternative assumption
`shortfall_checkout_financed = False` is removed from the code (commit `4ef473c`): the
parameter, the branch in `_seek_credit`, the arm `eff_checkout_unfunded`, its test, and its
entries in the table builder, the check script and the register generator. The thesis no
longer reports the arm (commit `c29300a`). The original record's statement that "the thesis reports both" describes the position before
this decision.

- The 40 runs of the arm were moved from `results/raw/effect.parquet` to
  `effect_checkout_unfunded.parquet` in the corrections folder (moved to the system trash 2026-10-07), together with the parameter column that
  only they varied. The file is not tracked, like the other raw runs. The arm can be
  reproduced from commit `e366631`, and from no later commit.
- `remove_checkout_arm.py` reran the baseline suite (60 runs) and the remaining effect suite
  (880 runs) at commit `4ef473c` and compared every numeric column with the stored runs. The
  largest absolute difference is 0.0 in both (`remove_checkout_arm.log`).
- `rerun_effect.py` and `before_after.py` read the removed arm. They belong to the record and
  run at commit `e366631`, not at the current one.
- Two conclusions rested on the comparison and were removed with it: that the size of the
  effect depends on the checkout assumption more than on any other setting, and that it
  depends more on how households finance a shortfall than on what lenders can see. No
  remaining experiment compares those two things. The limits in the conclusion are now three.

**Committed shortfalls stay as they are.** Marc considered carrying an unpaid committed
shortfall forward and kept the existing rule (credit raised against a committed shortfall pays debt service first). No code or text changed.

**RQ2 is reworded** (commit `03bf1ab`): "When BNPL platforms cannot observe one another's
exposures, how often do households owe several platforms at once, and how do enabling BNPL,
platform count, access and peer adoption affect population default?" The restatements in
Sections 1, 3, 4 and 4.6 follow it. Nothing in the thesis describes stacking as emergent.

**Four figures were checked against their sources** (commit `7eb36b8`). No parameter and no
validation tolerance changed.

| Figure | Source read on 2026-09-29 | Result |
|---|---|---|
| Order cap, R15,000 | Payflex terms and conditions; the pages in the payflex.co.za sitemap and archived copies of the terms, 2019 to 2026 (scanned by a search agent); Payflex's archived FAQ "What's the maximum I can spend with Payflex?" | **Not sourced.** No Payflex page states a maximum order value. Clause 4.4 of the terms reserves the right to amend a customer's spend limit, and the FAQ says the limit depends on an individual assessment. Third-party pages give R10,000 (loanrating.co.za) and "e.g., R20,000" (Peach Payments). The cap is now recorded as an assumption. It binds on 0.3% of platform requests at beta = 0. |
| UK median income behind the 37% | ONS, "Average household income, UK: financial year ending 2020", released 21 January 2021, corrected 22 March 2022 | Median equivalised household disposable income, 30,500 pounds a year. 1,000 pounds is **39.3%** of a month's income. The text now says 39%. The earlier 37% matches the median for the year to March 2022, published after the Woolard Review. |
| Australian median income behind 0.26 | ABS, "Household Income and Wealth, Australia, 2019-20", released 28 April 2022; ASIC REP 672, Table 2 | Afterpay's maximum of A$2,000 is **25.8%** of median gross household income (A$1,786 a week), so 0.26 stands on that measure. On median equivalised disposable income (A$959 a week), the measure used for the UK, it is 48.1%. The text names the measure and gives both. |
| Gini bounds, 0.63 and 0.70 | World Bank API, archive vintages of February and April 2026 and the live series; Stats SA Report 03-10-19, Table B3; Hundenborn, Leibbrandt and Woolard, WIDER Working Paper 2018/162, Table 1 | The World Bank citation is accurate: 63.0 for 2014 in the February vintage, 59.6 and 54.1 (2022) in the April vintage, consumption-based. The upper bound matches Stats SA's per-capita income Gini for 2009, 0.70. Income comparisons added: 0.67 (Stats SA, 2015) and 0.66 (NIDS 2014). No published income Gini computed from NIDS Wave 5 was found. |

One bibliography entry was wrong and is corrected: `payflex_limits` pointed at
support.myboost.co, the help centre of Boost PayFlex, a Malaysian product.

## 2026-10-05: scenario arms rerun at 100 replicates

The bureau, screening and combined arms had 20 replicates on separate seed blocks (41,000,
42,000, 44,000), so their differences were unpaired and too noisy to rank. They became suite
`rq3s` with their own benchmark, 100 replicates per arm and one shared block (80,000). The
retained arms of `rq3.parquet` reproduced exactly. With the extra precision bureau visibility
raises default (+0.22 and +0.15 points); before, the effect was not detectable (DEFECTS B23).
The calibration script also gained a fine-grid check of the shock probability in steps of 0.001
(`fine_grid_90_plus` in `calibration.json`; the 460 stage-4 runs are not saved).

## 2026-10-06: routing and shortfall-path robustness arms

Three switches were added to `simulation/config.py`, each defaulting to the behaviour of every
stored run: `platform_routing="loyal"`, `shortfall_bnpl=False` and
`committed_shortfall_funded=True`. The effect suite gained 140 runs on seeds 70,000-70,019; the
880 stored runs reproduced exactly (largest absolute difference 0.0 over 127 columns). Results
are in `tab:effect` and Section 4.2 (DEFECTS B37). Driver: `git show
ca9ae96:results/variants_2026-10-06/run_variants.py`; the arms now run as part of
`simulation.experiments --which all`.

## 2026-10-07: lead-editor review

Five independent reviews (experimental audit, examiner-style correctness, structure against the
supervisor's paper, language, coherence), a verification of the revision, and a final
simplicity pass. Reviewer reports: `git show ca9ae96:scratchpad/review_2026-10-07/`. Body prose
9,803 to 9,879 words. Questions left open by the review are in `DEFECTS.md`.

### Experiment/paper discrepancies (fixed)

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

### Factual claims verified or newly evidenced

- **Single-tick shock cannot be calibrated** (4.5, `tab:robustness-appendix` note). No stored
  run supported this. Checked with `notebooks/scripts/check_single_tick_calibration.py` (output `results/summary/single_tick_calibration.json`; friction held at 0.09): the 90+ share stays at
  7.3–7.6% across the whole calibration grid (0.008–0.064, seeds 1,000–1,019), about half the
  14.21% target. The claim now cites this evidence.
- **Who defaults.** Default includes households with no debt (a food or rent shortfall alone
  counts as distress). Checked with `notebooks/scripts/check_defaulter_credit.py` (output `results/summary/defaulter_credit.json`): 90.5% of baseline defaulters
  owe traditional debt when they default, and 98.4% owe traditional debt or BNPL with BNPL on at
  β = 0. Added to Section 2.3 and the limitations index.
- **Agreements-cap diagnostic** (Appendix C). It predated the October code changes. Rerunning
  the agreements-cap diagnostic (now `notebooks/scripts/check_cap_definitions.py`, output `results/summary/cap_definitions.md`) on the current code reproduced it byte for
  byte.
- **β = 1 BNPL volume.** About R10,400 per eligible household per year (derived from
  `results_numbers.json`: R1,010 × 65.88/6.42), well above the provider band's upper end of
  R4,261. β = 0 is below the band, so the two settings bracket observed volume.
- All headline numbers in the abstract and Sections 3–6 were confirmed by the auditor against
  the generated tables, `results_numbers.json` or a recalculation from `results/raw`. The β = 1
  effect appears as 0.61 ± 0.11, 0.60 ± 0.11, 0.60 ± 0.12 and 0.60 ± 0.07. All four are correct,
  each for its own seed block or the pool.

### Claims materially weakened

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

### Claims strengthened or reframed

- **β = 0 against β = 1.** The old reason (β = 1 stacks more than CFPB) rested on a share the
  routing assumption sets. The new reason uses volume: the two settings bracket the provider's
  volume, β = 0 is closer on both measures, and because the effect grows with borrowing, the
  β = 0 effect probably understates the effect at market volume.
- The conclusion now answers the main question in its own words and states the pattern across
  the results: default follows borrowing volume and refusals by the traditional lender, not the
  number of platforms owed. It reports the quintile finding for the BNPL effect (Q2–Q4, not Q1),
  which was previously dropped, and gives a short, conditional implication for the reporting
  arrangements.

### Structural changes

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

### Fixes after the independent verification of this revision 

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

### Final simplicity pass

I read every body chapter once more for simplicity only. These were line edits, with no change to any claim or number:
- I split long sentences in 1.4, 2.2, 3.1 and 3.3.
- I removed a repeated "no adoption cascade" sentence (4.3) and a repeated bureau-refusal clause in the conclusion's opening paragraph.
- I untangled the β = 0 volume paragraph in 4.1.
- I replaced "mutual blindness" with "platforms not seeing one another" (4.7), matching the conclusion.

I spot-checked the conclusion's 0.37–1.27 range against `tab_effect`. The thesis builds with no undefined references, and `check_results_tables.py` still passes.
