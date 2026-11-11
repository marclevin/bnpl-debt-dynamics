# Audit B: model description vs code and data

Scope: thesis/chapters/02_model.tex, 03_calibration.tex, appendix_a_rationale.tex, appendix_b_register.tex,
appendix_b_specification.tex, appendix_d_variables.tex, appendix_e_matching.tex, appendix_f_pseudo_init.tex,
appendix_g_pseudo_main.tex, generated tab_arrears_fit.tex and tab_bnpl_on_checks.tex (plus tab_baseline_arms.tex
for the figures Ch3 quotes from it), and the model sentences of the Abstract (main.tex l.108-111).
Read-only. Checks used: code reading; pandas on data/processed and results/summary; model *initialisation only*
(no ticks run) to compare starting states across arms; the unit suite (171 passed).

## Coverage

About 300 items checked: all 45 register parameters (value and provenance against `experiments.calibrated()`,
programmatically, 45/45 match), about 20 sweep ranges and seed blocks (all match experiments.py, sensitivity.py,
calibrate.py), about 150 numbers in Ch2, Ch3, App D, App E and the abstract (against results/summary/*.json,
data/processed/*.json, the population parquet and the code), and about 70 statements about mechanics and
pseudocode lines (against agents.py, bnpl.py, lender.py, affordability.py, model.py, metrics.py,
population.py). Everything not listed below matched. 1 HIGH, 4 MED and 11 LOW findings.

---

## HIGH

### H1. The labour-market and income-path figures in Section 3.4 come from the run before the arrears rule
- **Thesis** 03_calibration.tex:269-275: "After two years employment is within 0.1\% of its starting level,
  although 13.5\% of the members employed at the start are out of work at the final tick ... By the final tick
  household income is 15.2\% above its start in Q1 and 6.1\% below it in Q4, and 3.9\% lower in total."
  The source comment (l.276-278) cites results/summary/defaulter_credit.json.
- **Data** results/summary/defaulter_credit.json, regenerated in 504b668 (2026-11-09):
  `employment_rel_t52_all` = -0.00223 (`employment_index_t52` 0.99777), so employment is 0.22\% below its start,
  not within 0.1\%; `earners_out_of_work_t52` = 0.1361 (13.6\%); `income_rel_t52_Q1` = +0.1487 (14.9\%);
  `income_rel_t52_Q4` = -0.0531 (5.3\%); `income_rel_t52_all` = -0.0392 (3.9\%, the only one that still matches).
  The printed values are those in the 2b9b033 version of the file (+0.1519, -0.0607, -0.0006, 0.1351), i.e. the
  streak-rule run of 2026-10-13. The hire-wage and lost-wage comparison in the same paragraph (above in Q1-Q2,
  below in Q3-Q5) still holds.
- **Known?** DEFECTS.md H2 (and HISTORY.md l.515, l.533) records the old numbers as done; that they went stale
  in the rerun is not recorded. The same stale numbers are in appendix_c_supplementary.tex:114 (outside this
  scope).
- **Fix**: "After two years employment is within 0.3\% of its starting level, although 13.6\% of the members
  employed at the start are out of work at the final tick ... household income is 14.9\% above its start in Q1
  and 5.3\% below it in Q4, and 3.9\% lower in total." Make the same change in Appendix C l.114, and in any
  prose that rests on "within 0.1\%".

---

## MED

### M1. The starting stock and the early draws are not the same in every arm of a seed block
- **Thesis** 03_calibration.tex:48-50: "Within a seed block the starting stock is the same households in every
  arm, except under the 56-day default threshold ... so it cancels from differences between arms." And l.59-60:
  "Arms in a block share seeds, so a replicate starts from the same draws in every arm".
- **Code** model.py:56-71: BNPL eligibility is drawn with `self.rng.sample(banked, n_eligible)` *before* the
  minimum-payer draw on the same stream, and only when `n_eligible > 0`. Changing `bnpl_access_rate` changes how
  many numbers that sample consumes, so it changes which households are minimum-payers. Through `due_tick` that
  changes the initial-arrears ranking (model.py:160-165) and so who starts in default. `min_payment_frac` and
  `min_payer_share` change the ranking directly. I checked at initialisation only, seed 30,000, against access
  1.0: access 0.5 and access 0.0 each swap 7 of the 318 households starting in default (24 of the households
  in arrears differ); `min_payment_frac` 0.10 swaps 24; `min_payer_share` 0.20 swaps 4. BNPL off against on at
  access 1.0 gives identical sets, so the claim holds for rq0 and rq3s (the arms the source comment says were
  checked) and for tab_baseline_arms and tab_scenarios. It does not hold for the access surface (rq2, rq2t,
  block 30,000 and 60,000) or for the minimum-payment, minimum-payer and population-size arms. The *count* of
  initial defaults is the same (318 = round(14.21\% of 2,237)), so the 6.36\% level still cancels; who those
  households are does not.
- **Known?** Not recorded.
- **Fix**: "Within a seed block the starting stock is the same share of households in every arm, and the same
  households in every arm at full access; under the 56-day threshold its size also changes." Also qualify
  l.59-60: "... a replicate starts from the same draws in every arm that keeps full access and the default
  repayment parameters." A code alternative is to draw eligibility and archetypes on `init_rng`.

### M2. The CCMR 91-120 band is converted into a per-tick flow in two ways within Section 3
- **Thesis** 03_calibration.tex:286-288 (and register `write_off_rate`, appendix_b_register.tex:87): "Accounts
  enter the 120+ band at half the 91--120 share per tick ... $(1.76/2)/12.45 = 0.0707$", which is an inflow of
  0.88\% a tick (the band is two ticks, 28 days, wide). 03_calibration.tex:343-344: "Each tick 0.83\% of the
  credit-active book reaches 91 days, against the 0.82\% implied by the \ac{CCMR} 91--120 day band, which holds
  1.76\% of accounts for 30 days" (default_level.json `ccmr_inflow_91plus_per_tick_of_accounts` =
  0.0176 x 14/30 = 0.00821; check_default_level.py:86).
- So the same band implies 0.88\% a tick for the write-off and 0.82\% a tick for the consistency check. Under the
  write-off's own convention the model's 0.83\% sits about 6\% below the derived inflow, not just above it.
  With the 30-day convention the write-off rate would be 0.82/12.45 = 0.0660.
- **Known?** Not recorded.
- **Fix**: use one convention. Either keep 0.0707 and say "against the 0.88\% a tick the write-off derivation
  assumes (1.76\% over two ticks); on a 30-day band it is 0.82\%", or state why the two differ.

### M3. A defaulted household's frozen BNPL balance still counts as holding BNPL
- **Thesis** 02_model.tex:293-295: "$s_g(t-1)$ [is] the share of eligible households in reference group $g$
  holding an active \ac{BNPL} balance at the previous tick." 02_model.tex:199-202 says a defaulted household's
  accounts are non-performing until written off.
- **Code** agents.py:225, 285: a defaulted (frozen) household's BNPL agreements are never collected, so they
  stay in `platform.loans` with their remaining instalments, arrears and fees until write-off (a mean of about
  14 ticks at 0.0707). model.py:246-248 counts any household with `bnpl_outstanding() > 0` as a holder in $s_g$;
  metrics.py:74-84 counts them in BNPL holding, `stacking_depth` (owing two or more platforms), `ever_holders`
  and `ever_stacked`, and metrics.py:52-56 keeps them credit-active. So non-performing households feed the peer
  signal and the holding and stacking measures until write-off. App G Alg. peer (l.282) shows this formula, so
  the pseudocode matches the code; the prose word "active" does not.
- **Size**: not measured (would need a run). DEFECTS.md H1 records that 99.9\% of BNPL arrears are held by
  households that have already defaulted, which suggests these frozen balances are a material part of the BNPL
  stock at any tick.
- **Known?** Not recorded as such.
- **Fix**: say so in Submodel 11 and the stacking measures: "holding a \ac{BNPL} balance, including the
  non-performing balance of a defaulted household until it is written off". Or exclude defaulted households from
  the numerator and from the holding and stacking measures, and rerun.

### M4. Under the arrears rule, friction plus persistence can default a household that has the cash (analytic estimate)
- **Thesis** 02_model.tex:264 and 03_calibration.tex:289-292 describe friction ("skipping an affordable
  traditional instalment") and persistence ("pays nothing again"), and l.292 says persistence stops "households
  with spare income" clearing arrears. Nothing says what this implies for default. 03_calibration.tex:357-358
  reports that 12.5\% of defaulters have an earner out of work.
- **Code** agents.py:294-306: once a household is in traditional arrears it skips the whole payment with
  probability $1-(1-0.72)(1-0.0575) = 0.736$ each tick, whatever its cash. Default comes at age 7
  (agents.py:388). A household with ample cash that skips once at random therefore reaches default with
  probability about $0.736^6 \approx 0.16$. For a current debtor that is a per-tick hazard of about
  $0.0575 \times 0.16 \approx 0.009$. The measured post-burn-in hazard among credit-active households not yet in
  default is 0.0097 a tick (default_level.json `off_hazard_per_tick_post`). So the random skip chain could
  account for most of default during the run. This is **an analytic estimate, not simulated**: it ignores
  households with zero service due, and households whose cash is short.
- The code's own design note no longer holds under the baseline. agents.py:267-269 says "Friction must move
  arrears without moving default", and simulation/tests/test_degenerate.py:104
  (`test_payment_friction_moves_arrears_but_not_default`) tests that property only under bare `ParamSet`
  defaults, which are the streak rule.
- **Known?** Not recorded in DEFECTS, DECISIONS or ARREARS_RULE.
- **Fix**: measure it (default during the run with persistence or friction set to 0, or the share of defaulters
  with cash to cover the amount due at their first missed tick) and state it in 3.5 "Default". For example:
  "Under the arrears rule a household that misses one instalment at random reaches default with probability
  about 0.16, whatever its income, so [x]\% of default during the run follows a missed payment the household
  could have made."

---

## LOW

### L1. Arrears persistence is placed in two different submodels
- **Thesis** appendix_b_register.tex:85 (generated): `arrears_persistence` & 7. Also `initial_arrears` and
  `write_off_rate` are in 7. Against this, 02_model.tex:185 and :264 (Table submodels, row 6) and
  appendix_b_specification.tex:59-60 and :66 put persistence in "Submodel~6".
- **Code** notebooks/scripts/generate_param_register.py SUBMODEL maps "D18" to "7".
- **Fix**: give `arrears_persistence` its own rule key, or override it to "6" in the generator.

### L2. In the pseudocode the single-tick arm is gated on the wrong switch
- **Thesis** appendix_g_pseudo_main.tex:43 "If $\mathbb{1}^{\text{flow}}$" for the labour-flows branch;
  l.48 "ElsIf not $\mathbb{1}^{\text{pers}}$"; l.33-34 and appendix_f_pseudo_init.tex:100: $\mathbb{1}^{\text{pers}}$
  and $\mathbb{1}^{\text{flow}}$ are "off together in the single-tick arm".
- **Code** agents.py:168 tests `p.labour_flows and p.shock_persistent`. The single-tick arm
  (experiments.py `rob_shock_single_tick` and effect `shock_single_tick`) is `calibrated(shock_persistent=False)`,
  so `labour_flows` stays True and is ignored. As written, the pseudocode would run labour flows in that arm. The
  persistent-without-flows branch (agents.py:193-202) is not in the pseudocode either; no reported arm uses it.
- **Fix**: "If $\mathbb{1}^{\text{flow}}$ and $\mathbb{1}^{\text{pers}}$"; notation: "the single-tick arm sets
  $\mathbb{1}^{\text{pers}}$ off, which also disables labour flows".

### L3. Friction is applied whether or not the instalment is affordable
- **Thesis** 02_model.tex:264 "Payment friction skips an affordable traditional instalment at random";
  03_calibration.tex:290 "the chance of skipping an affordable traditional instalment"; appendix_f_pseudo_init.tex:87.
- **Code** agents.py:294, 306: the skip is drawn for every household and sets `paid_trad = 0` even when
  `cash < due_trad`. So it also cancels the partial payment of a household that is short of cash. A partial
  payment would clear the oldest arrears and could lower the arrears age.
- **Fix**: "skips a traditional instalment at random, whether or not the household could pay it" (or condition
  the draw on `cash >= due_trad`, and refit).

### L4. Write-off also acts on defaulted accounts still at 91-120 days
- **Thesis** 03_calibration.tex:286-288 and the register derive the rate as the outflow that keeps the 120+ stock
  stationary.
- **Code** agents.py:374-383: any defaulted household with a balance is written off at 0.0707 a tick, from the
  tick after default, including at ages 7-8 (91-120 days). So some accounts leave before they reach 120+, and the
  stock-flow identity behind 0.0707 is not the one the code implements. Agreement on the bands is fitted, so the
  effect on the reported fit is small.
- **Fix**: add "applied from default, so a small share of accounts is written off before 120 days".

### L5. The data-to-agent table lists fields the agent does not carry
- **Thesis** 02_model.tex:37-58 (tab:agent-mapping, "The state initialised for each agent") lists
  `household_size` and `term_months`.
- **Code** population.py:33-71: `HouseholdRecord` has neither. It does carry `n_jobseekers`, `hire_wage_tick`
  and `discretionary_monthly`, which the agent uses and the table omits. appendix_d_variables.tex:255-257 lists
  the per-tick flows scaled by 12/26 but omits the hire wage (population.py:230).
- **Fix**: drop the two rows, or mark them "data layer only"; add `n_jobseekers` and `hire_wage_tick`; add the
  hire wage to App D's tick-scaling list.

### L6. "Every run uses the same 5,000 households" and "one random stream"
- **Thesis** 03_calibration.tex:58-59: "Every run uses the same 5{,}000 households". l.61: "Each run takes
  every later draw from one random stream".
- **Code** experiments.py `rob_n1000` and `rob_n10000` resample the population (population.py:185-189).
  Activation order uses Mesa's own generator (model.py:198, `shuffle_do`), and the thresholds use `init_rng`.
  appendix_f_pseudo_init.tex:13-15 says both correctly.
- **Fix**: "Every run except the population-size check uses ..."; "... every later draw except the activation
  order from one random stream".

### L7. Tick indexing in the pseudocode
- appendix_g_pseudo_main.tex:12 runs $t = 1,\dots,T$, while Alg. seed (appendix_f_pseudo_init.tex:251) dates the
  initial unpaid instalments $-a,\dots,-1$. Under the pseudocode's own age (Table notation: "counting its own
  tick"), the first tick then gives age $a+2$. The code starts at tick 0 and gives $a+1$ (model.py:34, 175;
  agents.py:370).
- **Fix**: run $t = 0,\dots,T-1$, or date the initial instalments $1-a,\dots,0$.

### L8. Symbols with two meanings are not flagged
- $c_i(t)$ is consumption distress (App F l.74), while $c(i)$ and $c$ are the matching cell (l.42; App E).
  $d_i$ is default, while $d$ is a donor (Alg. match). $b$ is BNPL due in Alg. tick, while $b$ is an arrears
  band in Alg. seed. $a$ is an age in Alg. seed, while $a_i$ is savings. The notation table flags the $q$ and
  $p$ overloads only.
- **Fix**: rename the band and age in Alg. seed (for example $\ell_b$ and $\tilde a$), and note the $c$ and
  $d$ overloads in the notation table.

### L9. Pattern 3 criterion as written is met at the start
- **Thesis** tab_bnpl_on_checks.tex row 3: "Expected: Peak in Q2--Q4"; "Not counted: absent at the start".
  03_calibration.tex:427-429.
- **Data** start ratios 0.81, 0.55, 0.78, 1.19, 0.71 (Q1-Q5, recomputed from the parquet). The peak is Q4, which
  is inside Q2-Q4. What is absent at the start is a hump (Q1 is above Q2 and Q3), not a peak in Q2-Q4.
- **Fix**: state the criterion as "rises from Q1 to a peak in Q2--Q4" (the build_results_tables.py text).

### L10. Platform count described as "varied in one arm"
- 03_calibration.tex:26: "Varied in one arm: four platforms and random routing". Platform count is a whole
  experiment (1-6 platforms x 4 betas, Table experiments).
- **Fix**: "Varied in an experiment: four platforms; in one arm: random routing".

### L11. Most model-level automated checks run the pre-D18 configuration
- **Thesis** 02_model.tex:346-351 lists the checks and says "All checks pass on the submitted code" (true:
  171 passed).
- **Code** test_balance_sheet.py, test_degenerate.py, test_bnpl_parameters.py, test_debt_accounting.py,
  test_peer_channel.py and test_variant_arms.py build bare `ParamSet(...)`: the streak rule, no initial arrears,
  friction 0, labour flows off. Only test_arrears_rule.py and test_beta_sweep.py use the baseline
  (`ARREARS_RULE`/`calibrated`). So the boundary checks (BNPL off, beta = 0, one platform) are not run on the
  reported model.
- **Fix**: add "most on the earlier configuration; the arrears-rule checks run on the baseline", or move the
  boundary tests to `calibrated()`.

---

## Known / disclosed items met during the audit
- B37 (shortfall path frees 3F/4 with no purchase modelled): known/disclosed (02_model.tex:222-225).
- B44 (initial-arrears placement assumed; non-performing default; persistence fitted): known/disclosed
  (03_calibration.tex:284, App B l.63-67, Alg. seed).
- B46 (credit-active book halves, 2,237 to 1,175): known/disclosed; both numbers verified.
- B47 (the 3.6\% group carries the effect): known/disclosed; 182, 109, 62, 120, 47\%, 85\%, 0.9 of 1.08,
  +0.11 ± 0.07, +0.18 ± 0.08 and +0.19 ± 0.07 all verified.
- B40 (12.6\% and 11.2\% not in any JSON): known, recorded, still unverifiable.
- B5 (accounts against households): known/disclosed.
- Memory item "stacking cap counts platforms, text says agreements": resolved within this scope. Ch2 l.282,
  register l.115 and App G l.191-193, 209, 216 all say platforms owed, which matches agents.py:576-616.

## Code-comment drift (not thesis text; for information)
- population.py:128 "all 2,892 of them": the population has 3,038 wage-dominant agents (App D l.95 is right).
- agents.py:9-10 "Borrowing happens LAST"; the code's step numbering (agents.py:245, 324, 335) differs from the
  thesis's seven steps.
- sensitivity.py:33-34 says shock_prob "sits above the QLFS band (1.4x ...)"; the derived 0.00446 is below it.
  sensitivity.py:60 and experiments.py:390-392 give the lambda band as 0.10-0.26, against 0.10-0.48 in the thesis
  and in config.py.
- calibrate.py:60-71 `evaluate()` docstring describes the superseded p-and-friction fit.
- ParamSet defaults (config.py) are the streak model; the baseline is only `calibrated()`/`ARREARS_RULE`.

## Not verified (no repository source, or out of reach without running)
- QLFS 11.6\% quarterly re-employment and 68.4\% still unemployed (typed in config.py:217, 228; not in
  qlfs_2017_labour_flows.json). The conversion 11.6\% -> 1.87\% a tick is correct.
- External figures: CBM 39.3\% and 21.7\%, CFPB 32-33\%, TransUnion 57\%, FinScope 13\% grant-card share,
  CCMR R392.0 bn book, Payflex terms, Woolard/ONS/ABS denominators (the arithmetic 39\% and 48\% is correct).
- Data-layer statements that live only in the notebooks: "every excluded record has a zero or missing weight",
  the R700 median imputed rent, the FinScope band-midpoint quintile assignment, and `w5_fwag` covering
  "primary and secondary jobs".
- Magnitudes in M3 and M4 (they need simulation runs).
