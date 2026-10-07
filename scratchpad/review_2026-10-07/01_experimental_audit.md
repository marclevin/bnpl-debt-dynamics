# Experimental audit: thesis against code and outputs (2026-10-07)

Scope: thesis/main.tex (abstract) and thesis/chapters/*.tex against simulation/*.py,
results/raw/*.parquet (all eight suites present), results/summary/*.json|csv,
data/processed/*.json and the build scripts. Read-only. Commands run:

- `PYTHONPATH=. .venv/bin/python -m pytest simulation/tests -q`: **134 passed**.
  (results/corrections_2026-09-29/REPRODUCE.md:31 still says "tests (128)". That is a note, not thesis text.)
- `notebooks/scripts/check_results_tables.py`: **OK, 43 numbers re-derived from results/raw match the generated fragments.**
- Ad hoc re-derivations from results/raw (scripts in /tmp, not saved in the repo). Every number below marked "recomputed" comes from these.
- A spot check of the single-tick shock rule: 3 seeds × 2 shock probabilities, 52 ticks, BNPL off, nothing written to disk.

**Overall verdict.** No BLOCKER found. Every headline number in the abstract, Sections 3–6 and
Appendix C matches results_numbers.json, the generated tables or a recomputation from raw.
That includes the four β = 0 seed blocks, the pooled effects, the access steps, the threshold-minus-control rises, the
want-off refusals and lending, the scenario contrasts and the lever results. The submodel
descriptions and the pseudocode (Appendices F and G) match the code line by line. The findings
below are wording drift, a mis-stated measurement period, a few claims stronger than the
two-standard-error rule allows, and descriptions that leave out what the code does.

**The β = 1 effect question.** All three quoted figures are correct, each for its own context.
- 0.61 ± 0.11 is the rq0 block (seeds 10,000–10,019; tab_baseline_arms; `injection_beta1` 0.00611 ± 0.001112).
- 0.60 ± 0.11 is the access sweep, access 0 to 1 (seeds 30,000–; tab_access; `access_rise_beta1` 0.00598 ± 0.001067).
- 0.60 ± 0.12 is the effect-suite reference (seeds 70,000–; tab_effect; `eff_ref_b1` 0.00603 ± 0.001233).
- 0.60 ± 0.07 is the inverse-variance pool of those three (`beta1_effect_pooled` 0.006039 ± 0.000653).

Every occurrence in the thesis uses the right one:
- 04_results:33 lists all four.
- 04_results:125 is the access figure.
- 04_results:241 and appendix_c:136 are the effect table.
- 04_results:264 and 06_conclusion:17 are the pool.
- main.tex:89 rounds to "0.6".

The β = 0 equivalents (+0.03 ± 0.09, +0.15 ± 0.07, +0.14 ± 0.11, +0.17 ± 0.10, pooled +0.12 ± 0.05) are also correct. I recomputed the pooling.

---

## A. Factual inconsistencies

**1. MINOR. The measurement period of traditional lending and refusals is wrong.**
- **Where:** generated tab_baseline_arms.tex:7, written by notebooks/scripts/build_results_tables.py:130. Also 03_calibration.tex:37–38 and appendix_g_pseudo_main.tex:19.
- **Thesis says:**
  - Table note: "interest, lending and volume are sums over the post-burn-in horizon".
  - Section 3.1: "Arrears, savings and volume measures exclude a 12-tick burn-in".
  - Algorithm 5: "Discard the first $T_0$ ticks; summarise the run".
- **Artefacts:**
  - `trad_granted_value`, `trad_refused_gate` and `trad_applications` are the lender's running counters (simulation/lender.py:99–112), copied unfiltered into the summary (simulation/metrics.py:272–275). They cover all 52 ticks, burn-in included.
  - The following also include burn-in: the want-driven purchase mean (model.py:138–143; metrics.py:210–214, 269–270), order-cap and limit binding rates (metrics.py:191–205, 265–267), and the "ever" quantities. The tab_baseline_arms note already states the last of these correctly.
  - Only interest, BNPL volume, fees and the per-tick band, savings and arrears means are post-burn-in (metrics.py:139–146, 239–247).
- **Effect:** The lending, refusal and application figures that 04_results:50–56, 05_policy:42 and 05_policy:54 quote therefore cover the whole run.
- **Fix (table note):** "interest and volume are sums over the post-burn-in horizon; lending granted, refusals and applications are counted over the whole run, burn-in included."
- **Fix (3.1:37):** "Arrears, savings, interest and volume measures exclude a 12-tick burn-in; default, lender counts, purchase sizes, binding rates and the 'ever' measures are counted from the first tick."
- **Fix (Alg. 5):** "Average the per-tick observables over ticks $T_0$ to $T$; carry default and the run counters over the whole run."

**2. MINOR. Appendix C compares stacking shares across seed blocks.**
- **Where:** appendix_c_supplementary.tex:81.
- **Thesis says:** "falls from 52.0% to 36.6% at β = 0 and from 85.1% to 22.0% at β = 1".
- **Artefacts:**
  - 52.0 and 85.1 come from the rq0 block (`stack2_holders_beta0/1`, seeds 10,000–).
  - 36.6 and 22.0 come from the effect block (`stack_holders_loyal_beta0/1`, seeds 70,000–).
  - On the same seeds, random routing gives 52.6 and 85.2 (`stack_holders_random_beta0/1`).
  - 04_results:91 and 04_results:260–262 already make the same-seed comparison.
- **Fix:** "falls from 52.6% to 36.6% at β = 0 and from 85.2% to 22.0% at β = 1 on the same seeds".

**3. MINOR. Submodel 12 says the order cap is reported by quintile.**
- **Where:** 02_model.tex:251.
- **Thesis says:** "Order-cap and limit binding rates reported by quintile."
- **Artefacts:**
  - Only the rolling-limit binding rate is computed by quintile (`bnpl_rolling_bind_{q}`, metrics.py:278–283; tab_distribution "Limit binds").
  - The order-cap rate is aggregate only (`bnpl_order_cap_bind_rate`, metrics.py:266). The thesis reports it as 0.3% in 03_calibration:259–260 (`order_cap_bind_beta0` = 0.002593).
- **Fix:** "Limit binding rate reported by quintile; order-cap binding rate reported in aggregate."

**4. MINOR. Submodel 11 says the β = 0 control is reported in every comparison.**
- **Where:** 02_model.tex:249.
- **Thesis says:** "$\beta=0$ control arm reported in all comparisons".
- **Artefacts:**
  - The level-sensitivity suite runs at β = 1 only (simulation/experiments.py:282, `base = dict(bnpl_enabled=True, beta=1.0)`), so tab_robustness, tab_robustness_appendix and fig_tornado have no β = 0 rows.
  - The Sobol design draws β from 0–3.
- **Fix:** "$\beta=0$ control arm reported beside every peer-influence comparison (the level-sensitivity arms are run at $\beta=1$ only; Table effect gives the effect at both)".

**5. MINOR. Section 4.5 says every sensitivity arm is compared on the same seeds.**
- **Where:** 04_results.tex:186.
- **Thesis says:** "Each arm is compared with its group's reference arm on the same seeds."
- **Artefacts:**
  - The single-tick shock arm (seeds 58,000–) has no same-seed reference. It is compared unpaired with the exact-shortfall arm on seeds 50,000– (build_results_tables.py:787–789; ‡ in tab_robustness_appendix).
  - The 1,000- and 10,000-household arms share seeds with the 5,000 reference but not the population, so they are also unpaired (‡; `shares_seeds` returns False).
- **Fix:** "Each arm is compared with its group's reference arm, paired by seed except where the table marks ‡ (population size and the single-tick shock)."

## B. Incorrect numbers

No incorrect number was found in the prose. One table cell misleads through rounding:

**6. MINOR. The single-tick row of tab_effect looks like exactly two standard errors.**
- **Where:** generated tab_effect.tex, row "single-tick shock", written with two decimals by build_results_tables.py:1009 (`pm`).
- **Table shows:** "$-0.02 \pm 0.01$" at β = 0 and "$+0.02 \pm 0.01$" at β = 1. Read against the two-standard-error rule, both look borderline detectable.
- **Artefacts:** `eff_shock_single_tick_b0` = −0.00015 ± 0.000134 (1.1 SE) and `eff_shock_single_tick_b1` = 0.00018 ± 0.000148 (1.2 SE). The prose (04_results:240, 06_conclusion:34) correctly gives "0.018 ± 0.015" and calls it not detectable.
- **Fix:** print this row to three decimals: −0.015 ± 0.013 and +0.018 ± 0.015.

## C. Methodological inaccuracies or omissions

**7. MINOR. The bureau and screening tests treat BNPL arrears as a recurring monthly obligation, and the prose does not say so.**
- **Where:** 02_model.tex:140–148, 05_policy.tex:14–15 and Submodel 15 (02_model:257).
- **Thesis says:** BNPL "instalments and arrears ... enter this calculation".
- **Artefacts:**
  - The visible obligation is `o_i / χ`. Here `o_i` is one instalment per live agreement plus the whole BNPL arrears balance (bnpl.py:152–164), divided by 12/26 (lender.py:65–68; agents.py:493–495). Arrears, a stock, are therefore counted as 26/12 ≈ 2.17 times their value per month.
  - Traditional arrears never enter either test. Only scheduled traditional service does (lender.py:65).
  - Appendix G (lines 94 and 124–125, 169) states this exactly. The body does not, and the treatment bears on the size of the bureau effect.
- **Fix:** add to 02_model after line 148: "Both tests convert each live agreement's instalment and any BNPL arrears to a monthly figure at 26/12, so an unpaid BNPL balance enters as if it recurred every month; traditional arrears are not shown to either test, which sees only scheduled traditional service."

**8. MINOR. The arrears definition is broader than the code.**
- **Where:** 02_model.tex:197–198.
- **Thesis says:** "Arrears track unpaid debt obligations through the \ac{CCMR} age bands."
- **Artefacts:**
  - Only traditional arrears are aged (agents.py:242, 290–293; metrics.py:44, 53).
  - The age is the number of consecutive ticks with any traditional arrears outstanding. Partial payment does not reset it, and only full cure does.
  - BNPL arrears are never in the bands.
- **Fix:** "Unpaid traditional instalments are carried as arrears, and the number of consecutive ticks a household has carried any traditional arrears places it in a \ac{CCMR} age band; \ac{BNPL} arrears are not in the bands."

**9. MINOR. The calibration procedure is under-described.**
- **Where:** 03_calibration.tex:280–289.
- **Thesis says:** the two parameters are "fitted" to the two bands, and the shock grid has 0.8-point steps.
- **Artefacts:** simulation/calibrate.py:121–164 fits in stages, all on 20 replicates, seeds 1,000–1,019.
  1. Fit p on {0.008, …, 0.064} with friction 0.
  2. Fit friction on {0, 0.02, 0.04, 0.06, 0.09, 0.12, 0.16} at that p, by absolute error to the 1–30 band.
  3. Refit p on the same grid at the chosen friction, by absolute error to the post-burn-in mean 90+ share of credit-active households.
  4. Run a fine-grid check (0.014–0.018) that does not change the selection.
- **Fix:** add one sentence: "The fit is sequential: the shock probability is chosen with friction off, friction is then chosen from {0, 0.02, 0.04, 0.06, 0.09, 0.12, 0.16} at that probability, and the shock probability is re-chosen at the selected friction, each by the smallest absolute error over twenty replications (seeds 1,000–1,019)."

## D. Ambiguous descriptions

**10. MINOR. tab_access does not explain the dashes in its holding column.**
- **Where:** generated tab_access.tex, written by build_results_tables.py:614.
- **Table note says:** "The holding column gives the same diagnostic for the share holding BNPL at the final tick."
- **Artefacts:** every linear-coupling row prints "--" in that column, because the script never computes it there. A reader may take the dash for "not detectable".
- **Fix:** add to the note: "The holding diagnostic is computed for the threshold rule only."

**11. MINOR. The want-driven purchase mean has no stated window.**
- **Where:** 03_calibration.tex:457–460 and tab_bnpl_on_checks.
- **Artefacts:** R633 and R610 average every want-driven origination over all 52 ticks, burn-in included (model.py:138–143). The volume checks in the same table are post-burn-in.
- **Fix:** state "over all 52 ticks" for the purchase mean in the table note.

## E. Results interpreted too strongly

**12. MINOR. "Default does not" depend on routing or platform count is stated as fact.**
- **Where:** 04_results.tex:95, 04_results.tex:103, 04_results.tex:263, 06_conclusion.tex:15.
- **Thesis says:** "default does not" depend on routing, and "Default does not respond to platform count."
- **Artefacts:** the differences are only not detectable, and at β = 1 effects of ±0.26 points cannot be excluded.
  - Routing: −0.07 ± 0.07 and +0.02 ± 0.13 (`routing_default_diff_beta0/1`).
  - Platforms, six against one: +0.02 ± 0.09 and +0.01 ± 0.08.
  - The abstract (main.tex:88) and 04_results:265 already say "detectably".
- **Fix:** "default does not change detectably" at each of the four places.

**13. MINOR. Section 5 says the bureau effect is "more than" the BNPL effect.**
- **Where:** 05_policy.tex:36.
- **Thesis says:** "at β = 0 that is more than the 0.12 ± 0.05 by which enabling BNPL raises default".
- **Artefacts:** 0.22 ± 0.045 against 0.12 ± 0.045, from independent blocks. The difference is 0.10 ± 0.06, about 1.6 SE, which is not detectable under the thesis's own rule.
- **Fix:** "at β = 0 that is comparable to, and if anything larger than, the 0.12 ± 0.05 by which enabling BNPL raises default (the difference, 0.10 ± 0.06 points across different seeds, is not detectable)".

**14. MINOR. "Mostly in the lowest income quintile" is marginal.**
- **Where:** main.tex:91 and 05_policy.tex:71.
- **Artefacts:** the Q1 rise is 0.59 ± 0.07 (β = 0) and 0.46 ± 0.08 (β = 1) points within Q1, which has 1,017 of 5,000 households. That is about 54% (β = 0) and 62% (β = 1) of the population rise of 0.22 and 0.15. Q5 also rises detectably (0.23 ± 0.10 and 0.22 ± 0.11; `switch_bureau_beta{0,1}_default_Q5_diff`) and contributes about a fifth.
- **Fix:** "largest in the lowest income quintile", which is the conclusion's wording at 06_conclusion:24.

## F. Statements that cannot be verified from the artefacts

**15. The single-tick shock cannot be calibrated.**
- **Where:** 04_results.tex:207–208 and the tab_robustness_appendix note.
- **Thesis says:** "no shock probability in the tested range reproduces the CCMR 90+ band" under the single-tick rule.
- **Artefacts:** no stored run tests this. calibrate.py has no single-tick stage, and DEFECTS.md B17 predates the B34 model correction.
- **Spot check (3 seeds, friction 0.09, BNPL off):** the 90+ share is 7.2–7.6% at p = 0.016 and 7.0–7.4% at p = 0.064, the top of the grid, against a 14.21% target. The claim is very likely true.
- **Needed:** a stored single-tick calibration grid, or soften to "no shock probability on the calibration grid tested in a spot check".

**16. The fine-grid calibration check.**
- **Where:** 03_calibration.tex:287–289 and the tab_arrears_fit note.
- **Thesis says:** 1.5% gives 13.93%.
- **Artefacts:** this exists only as a summary in calibration.json (`fine_grid_90_plus`). calibrate.py:149 saves only stages 1–3 to calibration_runs.parquet, so the stage-4 runs cannot be re-derived.
- **Needed:** save df4.

**17. The agreements-cap diagnostic.**
- **Where:** 05_policy.tex:68 and appendix_c:175–185.
- **Thesis says:** 32.9% of volume, −0.11 ± 0.07 points, and −0.35 ± 0.09 points with 31.7% of volume for the cap as modelled.
- **Artefacts:** the numbers match results/corrections_2026-09-29/cap_definitions.md exactly. That file predates the 2026-10-05 and 2026-10-06 code changes. It still holds only if those changes preserve behaviour, which REPRODUCE.md and variants README assert for the stored suites but which was not re-run for this diagnostic.
- **Needed:** re-run cap_definitions.py on the current commit.

**18. "Specified before the run" claims.**
- **Where:** the threshold rule (02_model:249), the Pattern 3 statistic (03_calibration:361) and the mean-purchase comparison (tab_bnpl_on_checks).
- **Artefacts:** git history starts 2026-08-13. The threshold mechanism enters config.py on that date (commit 12b1244), before the September final run, which is consistent. Nothing earlier can be verified.

**19. Two data-layer figures are not in any data/processed JSON.**
- **Where:** 03_calibration.tex:250–251 and appendix_c:115.
- **Thesis says:** 12.6% median and 11.2%.
- **Status:** not checked. They presumably sit in notebooks/p4_validation.ipynb.

---

## Checked and found correct

**Clock and design**
- 14-day tick; 12/26 conversion; 52 ticks (two years); 12-tick burn-in; 5,000 agents; 4 platforms.
- 20 replicates per arm with seeds `seed0+i`; 100 in rq3s (seeds 80,000–80,099); Sobol N = 256, 2,048 design points × 2 = 4,096 runs.
- Seed blocks as stated in every table note (checked against the parquet files).

**Parameters against config.py and experiments.py**
- Fitted values: p = 0.016, friction 0.09.
- Shock process: re-employment hazard 0.018724; QLFS band 0.54–1.17%; ratio 1.37.
- Defaults: q_base 0.05; β = 0; μθ 0.30; σθ 0.20; γ arm 0.3; κ 0.1387; CV 0.6; minimum-payer share 0.29; minimum-payment fraction 0.05; k = 7 (k = 4 arm); λ 0.10.
- BNPL money terms: order cap R9,926.83 = 15,000/1.511057; late fee R125.74 per tick; fee cap R188.61, or half the purchase price.
- New loans at 28% over 25 months; repo rate 7%; product terms table (credit_rate_table.csv).
- Sweep grids for β, access, platforms, σθ, μθ, k_cool, cap, λ, κ, the amount rules and the Sobol bounds.

**Submodels against the code**
- Tick order, steps 1–7 (agents.py:133–297).
- Distress before friction; default after 7 consecutive distressed ticks, absorbing; a defaulted household is refused all credit.
- No write-off.
- Committed shortfall recorded as distress and not funded, with the `committed_shortfall_funded` arm.
- BNPL-first shortfall path: 3F/4 relief, capped at κ·E^d; the remainder goes in full to the lender; all-or-nothing Reg 23A gate on gross surveyed income, not reduced while a member is unemployed; loan booking reweights the rate and raises scheduled service.
- Reg 23A norms and both worked examples; ceiling 10.4% at R900 and 83.2% at R7,712; maximum 93.2%; weighted Q1 mean 49.6% (recomputed on the source).
- Per-earner shocks applied to wage-dominant households only.
- Want-driven purchase lognormal with mean κ·E^d, truncated to 4 × cash.
- Random routing redrawn per request; loyal routing; the cap counts platforms owed.
- Pay-in-four timing, nothing collected in the tick of opening; fee cap and per-platform cut-off.
- Cool-off is strict and blocks only want-driven purchases.
- Peer signal: share of eligible members holding a balance, lagged one tick, computed after all households act.
- Threshold draws from a separate stream; the γ = 0 control is identical across all five σθ (recomputed).
- Activation reshuffled every tick.
- Appendix F and G pseudocode match the code.

**Standard errors and detectability**
- Paired SE = sd(diff)/√n when seeds are shared, unpaired otherwise (results_common.py:65–95).
- Detectable means |d| > 2 SE (results_common.py:104–106).
- Every "detectable" or "not detectable" statement in the abstract and Sections 3–6 and Appendix C was checked against its SE and is correct, apart from items 12–14.
- β = 0 effect: 1 of 4 blocks detectable; the pool is 2.7 SE.
- Access steps: 6 of 30 detectable, range −0.09 to +0.33, SE 0.07–0.14.
- Effect suite: 19 of 20 settings detectable at β = 1 and 5 of 20 at β = 0, none negative.
- Switches: bureau detectable; screening not; both just beyond 2 SE.
- Levers: cooling-off and caps of 1 and 2 detectable only at β = 1.

**Calibration and validation**
- Fit: 90+ 14.48%, 1–30 8.19%, 31–60 0.97%, 61–90 0.99%, 60+ 15.46%; 90+ reaches 19.9% at the final tick.
- Grid neighbours 11.31% and 17.10%; fine grid 13.93% and 14.48%.
- At start: 44.7% credit-active; 3.6% / 5.1% / 45.2% vulnerable; 76.6% of zero-savings agents have income above their outlays.
- Validation scorecard: 17 of 18 pass; the servicing share (12.8%) fails; three of four external checks pass.
- Imputation and resample figures match data/processed/*.json.

**Every prose number in the abstract, Sections 3.3–3.5, 4.1–4.6, 5, 6 and Appendix C**
- Matched against results_numbers.json or the generated tables, or recomputed from raw where typed.
- Typed numbers recomputed:
  - threshold-minus-control rises of 0.05 ± 0.08 and 0.14 ± 0.13;
  - want-off refusals of −17 ± 8 and lending −R0.83m;
  - effect-block refusals of −16 ± 7;
  - single-tick no-BNPL default of 4.82%;
  - +0.01 points default under committed funding.
- These typed values should be added to results_numbers.json, because 06_conclusion's header comment says "nothing is typed".

**Tables, figures, Sobol**
- check_results_tables.py passes.
- Figure error bars are t-based 95% CIs; the tornado uses paired CIs as captioned.
- Sobol: S1 for the shock probability is 0.99 ± 0.15, its range 0.005–0.026, and no other parameter has ST above 0.011.
- λ = 0.25 and λ = 1.0 give identical default in every replicate (the limit binds on 3.2% and 0.4% of requests), as 04_results:248–249 states.
