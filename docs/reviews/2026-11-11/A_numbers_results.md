# Audit A: numbers on the results side

Scope: Abstract (thesis/main.tex), thesis/chapters/01_introduction.tex (own-result numbers only), 04_results.tex, 05_policy.tex, 06_conclusion.tex, appendix_c_supplementary.tex, and the generated tables, captions and notes those files input. Read-only: no repo file was edited.

## Summary

- About 320 numbers in prose, captions and table notes were checked against results/summary (results_numbers.json, beta_sweep.json, contestable_default.json, short_group.json, default_level.json, defaulter_credit.json, sobol_indices.json, sobol_noise_check.json, bureau_visible_split.json, cap_definitions.md) and against the generated tables. Another 60 or so table cells were recomputed independently from results/raw/*.parquet with pandas.
- 314 of them are correct to the stated rounding. Two numbers are wrong (stale), one claim is not strictly supported under the thesis's own two-SE convention, and three items are LOW (wording or rounding).
- Repo checker: `PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py` printed "OK: 47 numbers re-derived from results/raw match the generated fragments" and "OK: 67 typed prose numbers match results/summary". It fails without `PYTHONPATH=.` (ModuleNotFoundError: simulation). It does not check the income-path numbers in Finding 1.
- Recomputed from raw with pandas, all matching the tables and prose:
  - rq0: baseline 14.37% (SD 0.36); effects +1.08 ± 0.11 and +1.12 ± 0.11; β=0.3 less β=0 +0.04 ± 0.14; credit-active 90+ 13.98 / 12.46 / 10.04; no-savings change +0.17 ± 0.04.
  - rq0 quintiles: every Q1-Q5 cell of tab:distribution.
  - rq3s: every default, Q1, Q3, refusals and food-and-rent cell of tab:scenarios and tab:scenarios-distress; both less bureau −1.09 ± 0.07; both less screening +0.04 ± 0.05 and +0.18 ± 0.06.
  - effect: reference +0.98 ± 0.13 and +1.07 ± 0.15; no-shortfall-BNPL −0.05 ± 0.16 and +0.11 ± 0.13.
  - rq1: every platform-count contrast (see Finding 2).
  - rq2t: threshold-rule rise less the control's, for every σθ. All within 1.4 SE, which supports "without changing the effect on default detectably" (04:146-148).
  - Pooled precision estimate recomputed from the four block estimates: 1.0271 ± 0.0624, which matches 1.03 ± 0.06.

Chapters 1, 5 and 6 are clean apart from the shared platform-count wording (Finding 2), which also appears in the abstract and the conclusion. Chapter 4 is clean apart from Findings 2 and 4.

---

## Findings

### 1. MED: Appendix C income path quotes the previous run (stale numbers)

- **Where:** appendix_c_supplementary.tex:114 (and the same sentence in 03_calibration.tex:274-275, outside this audit's scope).
- **Text:** "by the final tick household income is 15.2\% higher in Q1, 6.1\% lower in Q4 and 3.9\% lower in total". The LaTeX comment at :115 names `income_rel_t52_*` in the "income path" entry of defaulter_credit.json as the source.
- **What the source says:** results/summary/defaulter_credit.json, "income path, baseline with labour flows":
  - income_rel_t52_Q1 = +0.1487, so **14.9%**, not 15.2%.
  - income_rel_t52_Q4 = −0.0531, so **5.3%**, not 6.1%.
  - income_rel_t52_all = −0.0392, so 3.9%. This one is correct.
  - income_rel_t52_Q5 = −0.0581, so Q5, not Q4, now has the largest fall.
- **Cause:** 15.2 / 6.1 / 3.9 are exactly the values in the file before commit 504b668 ("Full rerun under the arrears rule…"). `git show 504b668^:results/summary/defaulter_credit.json` gives Q1 0.1519 and Q4 −0.0607. The text was not updated after the rerun.
- **Known?** Not recorded. docs/DEFECTS.md:389 (H2, "Done") still quotes the old +15.2% / −6.1% / −5.7% figures.
- **Fix:** "…household income is 14.9% higher in Q1, 5.8% lower in Q5 and 3.9% lower in total" (or "5.3% lower in Q4" if Q4 is kept for a reason).
- **Outside scope, same cause, in 03_calibration.tex:270-271:**
  - "13.5% of the members employed at the start are out of work": the file now says earners_out_of_work_t52 = 0.1361, so **13.6%**. It was 0.1351 before 504b668.
  - "After two years employment is within 0.1% of its starting level": employment_index_t52 = 0.99777, so **0.22% below** the start. It was 0.9994 before 504b668.
  - Whoever audits Chapter 3 should fix these together with the Appendix C row.

### 2. MED: "No detectable rise with the number of platforms" rests on the six-vs-one contrast only

- **Where:**
  - main.tex:112: "Many users owe several platforms at once, but default shows no detectable rise with the number of platforms."
  - 04_results.tex:255: "and does not change detectably with the routing rule or the number of platforms."
  - 06_conclusion.tex:22-23: "and does not rise detectably with the number of platforms."
- **What the source says:** recomputed from results/raw/rq1.parquet (seeds 20,000-20,019, paired by seed, default_rate_final). Results_numbers.json agrees: `nmax_minus_n1_beta0` = 0.00219 ± 0.000972 with n = 2, and `nmax_minus_n1_beta0.3` = 0.00216 ± 0.00107 with n = 5. The keys are computed by build_results_tables.py:333-338 but not used in the text.
  - Two platforms less one, β=0: **+0.22 ± 0.10, 2.25 SE**.
  - Five platforms less one, β=0.3: **+0.22 ± 0.11, 2.02 SE**.
  - The other 18 contrasts with one platform are within 1.81 SE.
  - Six less one: +0.13 ± 0.13, −0.08 ± 0.11, +0.15 ± 0.11 and +0.17 ± 0.12. None is detectable, so the text at 04:101-104 is correct as worded.
- **Judgement:** two of 20 contrasts pass two SE, which is about what chance gives (P(≥2 of 20) ≈ 0.23 at p = 0.0455). There is no monotone pattern. The substantive conclusion is defensible, but under the thesis's stated convention the blanket "no detectable rise" is not literally true. An examiner reading Table tab:stacking-full, where default with one platform is the lowest cell in three of four columns, could ask.
- **Known?** Not recorded in DEFECTS.md or DECISIONS.md.
- **Fix:** keep the six-vs-one sentence at 04:102-104 and add one clause, for example: "of the twenty contrasts of two to six platforms with one, two pass two standard errors (+0.22 ± 0.10 for two platforms at β = 0, +0.22 ± 0.11 for five at β = 0.3), about as many as chance would give, and default shows no rise with platform count." Then soften the abstract and conclusion to "no systematic rise".

### 3. LOW: "(95% bootstrap bound)" does not fit "within 0.03 of zero"

- **Where:** appendix_c_supplementary.tex:263.
- **Text:** "with it removed each is within 0.03 of zero (95\% bootstrap bound)".
- **What the source says:** results/summary/sobol_noise_check.json, rows[*].ST_noise_corrected and its 95% interval (_ci):
  - q_base: −0.016, interval [−0.041, 0.009]
  - β: −0.004, interval [−0.028, 0.021]
  - minimum-payment fraction: −0.015, interval [−0.041, 0.012]
  - κ: −0.021, interval [−0.043, 0.002]
  - λ: −0.013, interval [−0.036, 0.013]
- The point estimates are within 0.021 of zero, and every upper bound is ≤ 0.021. Four of the five lower bounds lie more than 0.03 below zero, so "within 0.03 of zero" is true of the point estimates, not of the 95% bounds.
- 04_results.tex:199 ("each of the five is within 0.03 of zero") is correct as worded.
- **Known?** DEFECTS.md:182 has the precise wording, "(upper 95% bound 0.021)". The appendix lost the word "upper".
- **Fix:** "…each is within 0.03 of zero, with an upper 95% bootstrap bound of at most 0.021."

### 4. LOW: Refusals without BNPL are rounded down (2,796.5 printed as 2,796)

- **Where:** 04_results.tex:30 ("from 2{,}796 to 970") and the generated tab_baseline_arms ("2{,}796 (116)").
- **What the source says:** results_numbers.json refused_off = 2796.5. Python rounds half to even, so it prints 2,796; conventional rounding gives 2,797.
- **Fix:** cosmetic. Either leave it or round half up in the builder. Prose and table agree with each other.

### 5. LOW (uncertain): the agreements-cap contrast sits on the detection threshold and the text does not say so

- **Where:** appendix_c_supplementary.tex:231-236.
- **Text:** "changes the cap's effect on default by at most $0.24 \pm 0.12$ points … $+0.24 \pm 0.12$ at a cap of three".
- **What the source says:** results/summary/cap_definitions.md, β=0.3, cap 3, "(a) less (c)" = +0.24 ± 0.12. The numbers are correct.
- **Why it is uncertain:** the ratio is 2.0 SE at the printed rounding. The md file stores only rounded values and the diagnostic runs are not in results/raw, so I could not establish which side of two SE it falls. The text never says whether it is detectable, although elsewhere the thesis states detectability for every contrast.
- **Fix:** state it, for example "(about two standard errors)". The unrounded value can be had from notebooks/scripts/check_cap_definitions.py output.

---

## Verified as correct (by file)

### Abstract (main.tex:105-116)

All correct:

| Number | Source |
|---|---|
| 14.4% baseline during the run | baseline_new_default 0.14373 |
| 1.0 point | beta0_effect_pooled 0.01027 |
| 2.4 times | volume_ratio_peer_over_beta0 2.378 |
| Book of credit-active households halves | 2,237 to 1,175, i.e. 0.4474 to 0.23495 × 5,000, ratio 0.525 |
| About 13% more refusals | 124.26/953.76 = 13.0%; 120.54/953.78 = 12.6% |
| 0.20 points | scen_bureau_beta0_default 0.001972 |
| 0.9 to 1.0 points | −0.93 and −1.03 |
| "Almost all in the poorest quintile" | Q1 −4.68 × 1,017/5,000 = 0.95 pp of 0.93 at β=0; 0.96 of 1.03 at β=0.3 |

Also correct:
- "Most of them households whose surveyed income does not cover food and rent": contestable effect 0.11 pp of the 96.4% majority, about 0.11 pp of the 1.03, so the 3.6% group carries about 89%.
- "Not detectable when BNPL cannot be used against a shortfall": −0.05 ± 0.16 and +0.11 ± 0.13.
- Food and rent: bureau +0.125 ± 0.016 and +0.114 ± 0.015; screening +0.036 ± 0.015 at β=0 and +0.014 ± 0.015 at β=0.3.

The only problem in the abstract is the platform-count clause (Finding 2).

### 01_introduction.tex:64-67

"About one percentage point" and "about as much as BNPL adds" are both correct.

### 04_results.tex

Every number is correct except Findings 2 and 4.

**Baseline and injection**
- 14.37 / 20.73; +1.08 ± 0.11 and +1.12 ± 0.11.
- Block estimates: 0.94 to 1.08 (four blocks) and 1.07 to 1.12 (three); pooled 1.03 ± 0.06 and 1.10 ± 0.07.
- Decomposition 1.07 = 0.94 + 0.13 (see Not verified).
- −0.05 ± 0.16 and +0.93 ± 0.12; 3.6% (182/5,000); refusals 970.
- 90+ credit-active 13.98 / 12.46.
- Sweep 90+ change +0.23 ± 0.01 (0.235 ± 0.0145); ever short of food and rent +0.06 ± 0.01 (0.057 ± 0.0145); no savings +0.17 ± 0.04.
- Volume ratio 2.4; want-driven purchases 6.1 vs 2.5; +0.04 ± 0.14; lending −R0.10 ± 0.25 m and +R0.15 ± 0.25 m.

**β sweep**
- Eight values, 250 replicates; +1.05 ± 0.03; SD 0.53; slope +0.003 ± 0.010.
- Quadratic and hinge terms at 1.23 and 0.34 SE, so "neither two SE" is correct.
- 0.07-point difference detected half the time (2 × 0.0366); R862 to R2,014; 28% to 70%.

**Stacking**
- 22% / 28% / 70%; loyal routing 70 to 20 and 28 to 13; "about the same volume" (5.34 vs 5.39 R m; 12.51 vs 12.89 R m).
- Routing −0.07 ± 0.12 and +0.01 ± 0.13 (0.005 pp).
- Six vs one −0.08 to +0.17, none detectable.

**Access**
- Holding 10 to 21 points; default 0.99 to 1.25, all bold.
- R² 0.94 to 0.98; steps −0.09 to +0.40; one of 24 steps beyond two SE.
- 0.73 ± 0.12 and 0.09 ± 0.14.
- Threshold rule: 14 to 34 against 10; 0.89 to 1.09 against 0.94; holding 41% to 13%; −0.18 ± 0.14; volume ratio 1.3 to 4.4.

**Distribution**
- 26.03 / 16.85; +4.12 ± 0.24 and +4.21 ± 0.16; no other quintile detectable (largest Q3 +0.52 ± 0.29).
- Two-thirds (121/182 = 0.665); R108 / R1,911; limit binds 20.6 / 20.4 vs 12.9; −0.28 ± 0.12.

**Sensitivity**
- Replicate SD 0.27 to 0.59 across 5,000-household arms, so "about 0.3 to 0.6" is correct.
- Population size and activation order are not detectable (+0.52 ± 0.27 is 1.93 SE).
- 6.36 of 20.73; +13.13 ± 0.13 = 1.81 + 11.32 ± 0.13; six weeks (98 − 56 = 42 days).
- S1 0.84 ± 0.15; separation-rate fifths 14.9% to 15.9%; other S_T 0.12 to 0.14; noise 14%.
- Single-tick shock −0.86 ± 0.15; amount rules −0.51 ± 0.14 and −0.39 ± 0.15; purchase size, minimum payment and min-payer share all within two SE.

**What moves the effect**
- Detectable in every setting but one (19 rows at β=0, matching eff_b0_detectable plus the want-off row).
- Range 0.79 to 1.18; reference 0.98 ± 0.13 and 1.07 ± 0.15.
- κ rows 0.89 to 1.09; volume roughly halves or doubles (447 and 1,589 vs 840).
- Income sizing: R1,075 is the closest to R992; effects +1.13 ± 0.13 and +1.12 ± 0.14.

**Answer to RQ2**
- 1.03 ± 0.06; +0.003 ± 0.010.
- Contestable households +0.11 ± 0.07 and +0.18 ± 0.08 (contestable_default.json). The β=0.3 value is 2.4 SE but the text makes no detectability claim, and DEFECTS B47 discloses it.

### 05_policy.tex

Every number is correct:
- 0.13 points detected half the time (2 × switch_se_max 0.065).
- +0.20 ± 0.07; +0.10 ± 0.06 not detectable (1.84 SE); −0.93 ± 0.06 and −1.03 ± 0.06.
- About 13% more refusals; lending 12 to 15% lower (−11.9% and −15.0%); 9.9% arrears and a quarter same-tick (bureau_visible_split.json).
- Food and rent +0.125 ± 0.016 and +0.091 ± 0.024.
- Q1 +0.17 ± 0.08 (2.12 SE) and Q3 +0.43 ± 0.13; none at β=0.3; chance probability 7% (0.073 recomputed); volume −1.3 to −1.5%.
- Q1 −4.68 ± 0.10 and −4.70 ± 0.10; refusals +1,827, close to 2,796 (2,781 = 954 + 1,827).
- Holding −0.3 and −0.7; volume about 3%; 20.88% (0.218106 − 0.009332); 20.73%.
- Screening food and rent +0.036 ± 0.015 (2.32 SE) and +0.055 ± 0.027 (2.01 SE), "just detectable"; β=0.3 not detectable.
- Both switches −0.90 ± 0.05 and −0.85 ± 0.05; −1.09 ± 0.07; +0.04 ± 0.05; +0.18 ± 0.06; peer gap −0.09 ± 0.08 (switch_bureau_interaction).
- Fourteen lever contrasts, none detectable; window up to 41% (40.5); cap of one 35 to 40% (35.1 and 40.3).
- RQ3 answer: every number repeats the above correctly.

### 06_conclusion.tex

Correct:
- 1.03 ± 0.06; +0.003 ± 0.010; 2.4 times; 3.6%.
- 0.20 ± 0.07; 0.93 to 1.03.
- "Default rises with access under both adoption rules" (all ten tab:access rows bold).
- "Most of it comes from the 3.6%" (about 0.92 of 1.03 pp; defaulter_credit 31% to 56% × 0.0364).
- "Credit-active book halves."

The only problem is the platform-count wording at :22-23 (Finding 2).

### appendix_c_supplementary.tex

Correct except Findings 1, 3 and 5:
- Calibration: 0.00446 (0.0187 × 1,113 / 4,670 = 0.004457); 0.0707; 0.0575 and 0.72; 0.98 points (0.978).
- Earlier rule: 0.09 and 9.10% (pre_arrears_rule/calibration.json); 0.4 to 0.5% (0.39 / 0.41 / 0.46), 11.03%, 7.28% and −0.10 ± 0.06 (docs/ARREARS_RULE_2026-11.md).
- Earlier fit: 0.016 ≈ 1.4 × 0.011718 (1.37); 39% (earners_out_of_work_t52 0.387).
- Limitations rows:
  - 20.73 / 6.36 / 13 points.
  - 2,237 to 1,175.
  - 3.6%; +0.11 ± 0.07; 68% (0.678).
  - −0.05 ± 0.16.
  - Loyal routing holders 21.2 to 13.5 and 20.1 to 9.0 (stack_holders_*).
  - "Up to about 0.25" (2 × 0.12 to 0.13).
  - SE about 0.13, range 0.08 to 0.17 across tab:effect, tab:cooloff and tab:cap (checked against all three tables); 0.26 missed half the time.
  - Scenario SEs 0.05 to 0.07; sweep SEs 0.03 to 0.04.
  - 82.8% (banked_ceiling 0.8284).
- Levers:
  - Cap of one lending +R0.13 ± 0.21 m and +R0.24 ± 0.19 m (lever_cap1_*).
  - Window 4.2 to 11.7% and 13.7 to 40.5%, default −0.18 to +0.05.
  - Caps 11.1 to 35.1% and 6.8 to 40.3%, default −0.19 to −0.01.
  - Cap definitions −0.02 ± 0.10 / 13.9%; 14.1% / −0.05 ± 0.12; +0.03 ± 0.11; +0.24 ± 0.12; 2.5% / +0.07 ± 0.15; definitions coincide at a cap of one.
- Sobol:
  - Noise 14%; S_T 0.12 to 0.14.
  - Gap between the separation rate's S1 and S_T 0.13 ≈ noise.
  - Swept range 0.0013 to 0.0071 = 0.29 to 1.59 times 0.00446.
  - "Holding almost entirely q_base" (S1 0.89, S_T 0.90).

### Generated tables in scope

- Checked against results_numbers.json, beta_sweep.json and sobol_indices.json, and spot-checked from raw parquet: tab_baseline_arms, tab_beta, tab_stacking, tab_stacking_full, tab_cap, tab_cooloff, tab_access, tab_distribution, tab_effect, tab_robustness, tab_robustness_appendix, tab_sobol, tab_scenarios, tab_scenarios_distress.
- No mismatch apart from the rounding in Finding 4.
- Bold cells agree with |effect| > 2 SE in every cell checked.
- Table and figure references in the prose point at the table that holds each number.

---

## Not verified, and why

1. **04_results.tex:23-25.** The decomposition (10 replicates: 1.07 = 0.94 BNPL-arrears + 0.13 traditional) exists only in docs/ARREARS_RULE_2026-11.md:85-87; no results/summary file holds it. The doc is internally consistent.
2. **appendix_c:21.** "the 90+ share at 9.9%" for the one-band fit appears only in docs/DECISIONS.md:1160 (D18).
3. **appendix_c:32.** "bureau visibility raised default by 0.18 points" under the earlier rule appears only in docs/HISTORY.md:522 (the 2026-10-12 labour-flows entry). No stored data for the last pre-arrears-rule scenario run was found, so it could not be confirmed that 0.18 was still the value just before the rule change.
4. **appendix_c:56 and 64-65.** Gate ceilings are specification numbers, not results. 10.4% and 83.2% match DECISIONS.md:600. For 93.2% and 49.6% no summary file was found.
5. **appendix_c:168, 183 and 190.** 11.2%, Gini 0.6514 / 0.6668 and CPI 1.511 / 1.506 are data-side numbers outside the results data, so they were not checked here.
6. **appendix_c:266.** The "37%" noise share in the two-replicate run is recorded in DEFECTS B45 and the message of commit 06fb3d5. results/summary/sobol_reps2/sobol_indices.json has no noise-share key, so it was not recomputed.
7. **External figures** (CFPB 32-33%, provider bands R1,333-R4,261, R992) were not re-sourced; only their use was checked.
