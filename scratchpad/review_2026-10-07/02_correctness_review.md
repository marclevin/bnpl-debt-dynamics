# Correctness and defensibility review (external-examiner reading)

**Thesis:** *Buy Now, Pay Later and Household Credit Distress in South Africa: An Agent-Based Model*
**Read:** `thesis/main.tex` (abstract), `thesis/chapters/01`–`06`, appendices A–C and G, every generated table in `thesis/chapters/generated/`. Context only: `OVERVIEW.md`, `scratchpad/DEFECTS.md`, `scratchpad/DECISIONS.md`.
**Date:** 2026-10-07. No thesis file was edited.

## Overall verdict

The thesis is careful. It scopes most claims to the model, states its statistical convention, separates fitted from unfitted checks, and records its failures instead of hiding them. Most issues an examiner could raise are already disclosed somewhere. What remains are four problems that a sceptical examiner would press in the viva. Each is about what the headline numbers *mean*, not about whether they were computed correctly:

1. The outcome called "default" is a cash-flow distress state that households with no credit can enter. Its level is never benchmarked (M1).
2. The calibration fits a non-stationary system: everyone starts current and nothing is written off. The fitted shock rate is therefore partly an artefact of the window chosen, and every level and effect is measured on a trending baseline (M2).
3. The model's structure largely fixes the sign of the bureau-visibility result (RQ3). That result has not been tested under the borrowing rules or horizon that the thesis itself says matter (M3).
4. The RQ2 claims that routing and platform count do not affect default are absence-of-evidence statements. The premise that platforms cannot see one another is never switched off (M4).

Below these sit seven moderate issues, mostly about inference, wording and where qualifications sit, and a short list of minor ones. The last section covers the opposite risk: too much hedging.

---

## MAJOR

### M1. "Default" is not credit default, includes households with no credit, and its level is never validated

- `02_model.tex:191-193`: "A household is distressed if it cannot cover committed expenditure from opening cash and income, or cannot meet the debt service due after seeking credit."
- `02_model.tex:198`: "Default occurs after seven consecutive distressed ticks, or 98 days, and blocks all further credit."
- `appendix_g_pseudo_main.tex:57`: `distressed ← short^c > 0 or due + b > cash` (the committed-shortfall flag holds even when credit is granted).
- `04_results.tex:21`: "With BNPL disabled, 13.31% of households have defaulted by the final tick".

**Why an examiner would challenge it.** The title and RQs concern *household credit distress*, and "default" is the main outcome in every RQ2 and RQ3 result. As specified, a household with no debt and no BNPL "defaults" if food and rent exceed its cash for seven ticks in a row. Credit cannot clear that flag, because `short^c > 0` marks the household distressed whether or not a loan is granted. At initialisation 3.6% of agents cannot cover committed expenditure from income (`03_calibration.tex:441-443`), and 56% of weighted households hold no debt (`appendix_d_variables.tex:202`). So part of the 13.3% default rate is subsistence shortfall that has nothing to do with credit. The thesis never reports what share of defaulters hold traditional debt or BNPL at the time they default. It also never compares the *level* of default with any benchmark. Only the 90+ arrears band is fitted, and that band is measured over credit-active households, not the population that "default" is reported over. The examiner will ask: "13% of all South African households defaulting within two years: compared with what?"

**Fix.**
- (a) Report the composition of defaulters: the share holding traditional debt, the share holding BNPL, and the share defaulting through committed shortfall alone. One extra observable is enough; no rerun of the experiments is needed.
- (b) Either rename the outcome (e.g., "sustained cash-flow distress (default)") in Section 2.3 and the abstract, or report default among credit-active households beside population default.
- (c) Give an external order-of-magnitude comparison for the level, e.g. the NCR Credit Bureau Monitor's impaired-record share of credit-active consumers, with the construct difference stated. If none is usable, say plainly in Section 3.5 that the default level is unvalidated.
- (d) Add a sentence to Section 2.3 saying that households without credit can enter default through a committed shortfall, and that credit cannot clear that condition.

### M2. The calibration fits a time average of a non-stationary system, and the fitted shock is reinterpreted after the fact

- `03_calibration.tex:372-377`: "Because households start current and no account is written off, the 90+ band accumulates every uncured account: at the fitted values it averages 14.48% after burn-in but reaches 19.9% at the final tick. The fit therefore matches the time average of a rising stock".
- `03_calibration.tex:290-293`: "The fitted shock probability is about 1.4 times the upper end of the observed separation-rate range ... so we interpret it as a reduced-form hazard of income loss and other distress, such as illness, unexpected bills or family changes."
- `02_model.tex:229` and `appendix_b_register.tex:41`: re-employment hazard 1.87% per tick, taken from the stock of all unemployed.
- `04_results.tex:21-23`: "14.20% of credit-active households are 90 or more days in arrears, against 14.21% in the CCMR".

**Why an examiner would challenge it.** Two departures from steady state pull in opposite directions.
- Every household starts current, whereas the 2017 CCMR stock has 28% of accounts in arrears. This pushes the model's window average *below* a stationary value.
- Nothing is written off, which pushes the 90+ stock up without bound.

The fitted shock probability therefore depends on the burn-in length and run length. A longer run would need a lower shock rate to hit 14.21%. The 1.4x gap to the QLFS band may be partly this artefact, not "other distress". The reinterpretation also does not fit the mechanism. The shock is a wage-earner separation applied only to wage-dominant households, so illness, unexpected bills and family changes for grant households cannot enter through it.

The re-employment hazard is the exit rate of the whole unemployed stock, long-term unemployed included. That understates the hazard for the newly separated. It implies an expected spell of about 53 ticks, longer than the 52-tick run, so in practice a shock is permanent. Persistence is the single most consequential assumption: the single-tick arm cuts default from 14.05% to 4.81% and removes the BNPL effect (`tab:robustness-appendix`, `tab:effect`).

The headline effects are differences in *final-tick* absorbing default on this trending baseline, so they may also depend on the horizon. The disclosure at 03:372-377 is honest, but its consequences are not drawn. The conclusion's limitations paragraph (`06_conclusion.tex:32-36`) does not mention the rising stock at all. Finally, 04:21-23 ("14.20% against 14.21%") suggests a precision the calibration does not have. The calibration run gives 14.48%, the replicate SD is 0.40, the grid step is 0.8 points, and 0.015 gives 13.93%, which is about as close.

**Fix.**
- (a) Minimum: in Section 3.4 state that the fitted value depends on the measurement window and the start-current initialisation. Add both points to the conclusion's limitations paragraph. In 04:21-23 replace "against 14.21%" with the calibration-run figure and its SD, or say "within replicate noise of".
- (b) Better: show the fitted shock probability under one alternative window (e.g., fit the final-tick 90+ share, or ticks 26-52). Report the reference BNPL effect and the bureau effect at that value and at the QLFS upper bound (0.0117). If the effects keep their sign and rough size, the problem is contained.
- (c) Either justify the stock-based exit hazard or test a higher hazard for the newly separated (a flow-based estimate), since persistence drives everything.
- (d) Drop "illness, unexpected bills or family changes", or say explicitly that the shock *mechanism* cannot represent them for non-wage households.

### M3. The sign of the bureau-visibility result (RQ3) is largely set by construction, and the result has not been stress-tested

- `main.tex:91`: "Adding BNPL obligations to that assessment raises refusals by about a sixth and default by 0.15 to 0.22 points, mostly in the lowest income quintile; in the model a refused household has no other source of credit."
- `05_policy.tex:48-49`: "a loan that is granted postpones distress, and its later cost may fall outside the horizon. The result therefore gives the direction of the affordability channel over two years in the model".
- `05_policy.tex:69`: "No lever was run under the alternative borrowing rules of Table effect".
- `appendix_g_pseudo_main.tex:121-127` (gate on surveyed income; loan granted in full at 28% over 25 months); `appendix_c_supplementary.tex:128-130` ("Income at the gate", filed under "Other limitations").

**Why an examiner would challenge it.** In the benchmark, the traditional lender in effect refinances every debt-service shortfall that passes the gate. It lends the exact shortfall, repayable over 25 months. A refused household is distressed by definition, with no fallback. The gate assesses surveyed income, so it never refuses because of the income loss that actually drives distress. Under these rules, anything that makes the gate stricter can only raise default within two years. The model has no channel through which refusing unaffordable credit *prevents* later distress inside the horizon, because a granted loan's cost is spread over 25 months and the run lasts 24.

So the result shows that, in this model, the lender stops refinancing some households sooner. Calling that "the direction of the affordability channel" overstates what it reveals: given the rules, the direction was close to certain before the run. The abstract carries only the no-fallback caveat. It omits the horizon, the refinancing role of the lender and the gate's blindness to current income. The thesis's own sensitivity analysis says the borrowing-amount rules matter most (06:48), yet the RQ3 switches were never run under those rules or over a longer horizon. The outcomes also do not follow refused households (05:45, 05:61), although an ABM can do this cheaply.

**Fix.**
- (a) Evidence: track refused versus granted households, comparing their default by the end of the run and in a 104-tick extension. Rerun the bureau switch (at least at beta = 0) under the "+25%" and "credit pays committed shortfall first" rules.
- (b) Wording in the abstract, 05:71 and 06:23-24: "In the model, where the traditional lender otherwise refinances shortfalls over 25 months, assesses surveyed rather than current income, and refused households have no alternative credit, bureau visibility raises two-year default by ...". State that the model cannot show a protective effect of refusal within the horizon.
- (c) Move "Income at the gate" in the index of limitations (`appendix_c:128-130`) into the group that bounds a central claim, bounding RQ3.

### M4. "Default does not depend on routing or platform count" is absence of evidence, and inter-platform invisibility is never switched off

- `04_results.tex:94-95`: "How often households owe several platforms depends on how they choose among platforms; default does not."
- `04_results.tex:263-264`: "These shares depend on the routing rule; default does not."
- `06_conclusion.tex:15`: "the share depends on the routing rule, and default does not."
- `appendix_c_supplementary.tex:81`: "bounds every stacking share, not the default results".
- `04_results.tex:105-107`: "platform count and total credit capacity move together and the sweep does not isolate invisibility."

**Why an examiner would challenge it.** The routing contrast is -0.07 ± 0.07 at beta = 0 and +0.02 ± 0.13 at beta = 1. Those standard errors cannot exclude effects of about 0.15 to 0.25 points, the same size as the *whole* beta = 0 BNPL effect (0.12 ± 0.05). The thesis's own power statement (04:8-9; `appendix_c:85`) says such differences "cannot be distinguished from none". The abstract words this correctly ("detectably"); the body and conclusion do not.

The larger problem is that RQ2 is framed around platforms that "cannot observe one another's exposures". Yet no arm lets them observe one another, for example through an aggregate limit shared across platforms at the one-platform capacity. The platform-count sweep confounds invisibility with capacity, as the thesis admits. The cap lever (`tab:cap`) is the nearest substitute: at beta = 0 a one-platform cap changes default by -0.03 ± 0.11. That is informative but is never connected to the invisibility question. As it stands, the thesis cannot say what invisibility *between platforms* does to default, and that is half of its framing.

**Fix.**
- (a) Rewrite 04:95, 04:263-264, 06:15 and `appendix_c:81` as "default does not change detectably; the design cannot exclude differences of about 0.2 points (beta = 0) or 0.25 points (beta = 1)".
- (b) Add one arm: four platforms with an aggregate limit of lambda summed across platforms, i.e. the one-platform capacity (or a shared exposure view). That isolates invisibility from capacity. If it cannot be run, say in Section 4.2 and the RQ2 answer that inter-platform invisibility is not separately identified. Cite the cap-of-one and lambda results as indirect evidence that capacity does not matter at beta = 0.

---

## MODERATE

### m1. The abstract's validation summary is selectively favourable

- `main.tex:87`: "The model passes three of four external population checks but understates BNPL purchase size and volume."

**Why an examiner would challenge it.** The three passes (household size, Gini, aggregate debt) are broad construction checks of the input data, as Section 3.5 itself says (03:486-488). Several behavioural misses are left out: the intermediate arrears bands (about 1% against 3.6% and 2.3%), Pattern 3, the interest measure of Pattern 1, and the rising 90+ stock. The abstract also says the model "fit[s] two parameters to the 2017 arrears profile" without saying the fit is to a time average.

**Fix.** "The population passes three of four broad external checks; the model misses the intermediate arrears bands, the debt-to-income pattern and BNPL purchase size and volume, and its 90+ band rises within a run because nothing is written off." The abstract is at 225 words, so cut elsewhere, e.g. the 2027 sentence.

### m2. Inference on the beta = 0 effect: post-hoc pooling, correlated "k of 20" counts, and a comparison that breaks the stated convention

- `04_results.tex:25-30`: "Four seed blocks give +0.03 ± 0.09 ... and only the second exceeds two standard errors. Pooled by precision, the effect is +0.12 ± 0.05".
- `04_results.tex:234` and `246-247`: "detectable under nineteen of the twenty settings" / "exceeds two standard errors under five of the twenty settings".
- `05_policy.tex:36`: "at beta = 0 that is more than the 0.12 ± 0.05 by which enabling BNPL raises default ..., although the two come from different seeds."

**Why an examiner would challenge it.**
- *Pooling.* The block designed to measure the effect (`tab:baseline-arms`) gives +0.03 ± 0.09. The pooled +0.12 rests on three other blocks, two of which are access end-points (zero against full access) and a threshold-rule control, not an "on against off" contrast. Pooling is legitimate if the estimand is the same. The text should say that it is (that zero access is equivalent to BNPL disabled) and that pooling was decided after the primary block came out null.
- *Counts.* All twenty `tab:effect` settings share one seed block (70,000-70,019), and many share the same no-BNPL arm (the 13.30 (0.22) entry recurs). The twenty effects are therefore positively correlated, not twenty independent tests. Two of the five beta = 0 detections (lambda = 0.25 and 1.0) are identical, which the text does acknowledge. One other is the reference itself. "5 of 20" and "19 of 20" read as replication evidence they cannot supply.
- *Convention.* 0.22 - 0.12 = 0.10 with an independent SE of about 0.064 is not detectable, so "more than" breaks the thesis's own rule. A policy reader will take it as "reporting does more harm than BNPL".

**Fix.** State the pooling rule and the equivalence of the estimands. Present the `tab:effect` counts as "settings under which the effect on this seed block exceeds two SE; the settings share seeds and are not independent". Report the effect's range rather than the count. Replace 05:36 with "comparable in size to the effect of enabling BNPL (the difference, 0.10 ± 0.06, is not detectable)".

### m3. The choice of beta: "beta = 0 is the better guide" is one-sided, yet the conclusion's headline still gives the illustrative beta equal weight

- `04_results.tex:39-40`: "We therefore treat the beta = 0 arm as the better guide to magnitudes".
- `06_conclusion.tex:9`: "In the model, enabling BNPL raises default by 0.1 to 0.6 points, more where households borrow more".
- `03_calibration.tex:460-464`: the beta = 0 volume falls below the lower bound of the provider band.

**Why an examiner would challenge it.** The case for beta = 0 rests on stacking, which the thesis says the routing *assumption* determines. On volume, the other available moment, beta = 0 is too *low* (R1,010 against at least R1,333 per eligible household). One check therefore says beta is too high at 1 and the other says it is too high at 0. The two moments bracket beta, so the truth may lie between, e.g. beta = 0.5, where the access effect is 0.27 ± 0.11 (`tab:access`). Meanwhile 06:9 presents "0.1 to 0.6" as if the illustrative beta = 1 were an equal candidate. An examiner will ask why q_base and beta were not at least bounded by the two moments at hand.

**Fix.** Report the beta at which volume per eligible household reaches the lower bound (from the existing beta grid), and the effect there. In 06:9 lead with the beta = 0 figure and give 0.6 as "under illustrative heavy borrowing (beta = 1)". In 04:39-40 add that beta = 0 understates volume, so its effect is plausibly a lower bound.

### m4. Pattern 1 rescued after the fact, and partly built in by the payment order

- `03_calibration.tex:474-477`: "the arrears measure tests the same mechanism and rises. On that reading, reached after the result, the lender-choice hierarchy stands and the interest condition was mis-specified."
- `02_model.tex:178`: "Pay the BNPL instalments that fall due, then traditional debt subject to payment friction."
- `03_calibration.tex:489-490`: "the arrears measure of Pattern 1, Pattern 4 and the ever-stacked share agree in direction or order of magnitude."

**Why an examiner would challenge it.** Recording the failure is good practice. Then declaring "the hierarchy stands" undoes it. The arrears rise also follows almost mechanically from two rules: BNPL is paid before traditional debt, and friction applies only to traditional debt. *Any* BNPL obligation will therefore raise traditional arrears, whatever the lender-choice hierarchy. Pattern 1 already "is not independent of model development" (03:340-342), so it cannot corroborate the hierarchy. Likewise, the ever-stacked share "agreeing" with the CFPB (03:489-490) is not evidence, because the thesis says stacking "carr[ies] no information about why" (02:335-338) and loyal routing would give a different share.

**Fix.** Delete "the lender-choice hierarchy stands". Say: "the arrears measure rises, as the payment order (BNPL first) implies; Pattern 1 is therefore not a test of the hierarchy". List the BNPL-first payment order as an assumption in `tab:submodels` and Appendix A. Remove the ever-stacked share from the list of agreements, or mark it as determined by the routing assumption.

### m5. Qualifications attached to the wrong claim, or missing where the claim is made

- `appendix_c_supplementary.tex:128-130`: "Income at the gate" sits among limitations that "do not bound a central claim". It bounds RQ3 (see M3) and the screening null (05:59).
- `appendix_c_supplementary.tex:134-136`: "Committed shortfalls are not repaid ... bounds: Little". This was tested only for the BNPL effect, not for the RQ3 switches.
- `06_conclusion.tex:32-36` (limitations paragraph): leaves out the rising 90+ stock, the gate on surveyed income, and the default construct (M1).
- `02_model.tex:149-151`: "the screening arm is an upper bound on what a platform's own check could see." It is an upper bound on information about *obligations*, not on screening's effect, because the test still uses surveyed income.

**Fix.** Move the two index rows. Add to each "bounds" cell the claims it was *not* tested against. Add one sentence each to 06:32-36 for M1 and M2. Reword 02:150-151 as "an upper bound on the obligations a platform's check could see; it still assesses surveyed, not current, income".

### m6. The tipping-point conclusion is stronger than the test

- `04_results.tex:127`: "The experiment cannot distinguish a straight line from a curved response."
- `04_results.tex:143`: "Neither rule shows a tipping point."
- `06_conclusion.tex:21`: "neither rule shows a tipping point."

**Why an examiner would challenge it.** R² of a line through seven noisy means (0.57 to 0.94) has little power against non-linearity. The thesis says so at 04:127, then states a negative at 04:143. The holding result (R² ≥ 0.998) does support "no adoption cascade on this grid"; the default result does not support "no tipping point".

**Fix.** "Holding shows no cascade on this grid; for default the design cannot distinguish a line from a curve, so the absence of a tipping point is not established." Apply the same change in 06:21.

### m7. Stacking shares are presented in the abstract as findings, though an assumption determines them

- `main.tex:88`: "Without peer influence, 37% to 52% of BNPL holders owe two or more of four platforms, depending on how they choose among platforms".

**Why an examiner would challenge it.** The thesis says these shares "follow from the routing rule" and carry no behavioural information (02:335-338; 04:88-89). In the abstract they read as an RQ2 result about South African households.

**Fix.** "Under the two routing rules assumed (no evidence on provider choice exists), 37% to 52% ...".

---

## MINOR

1. **`04_results.tex:166-172`, quintile contrasts.** "The rise in Q4 exceeds the rise in Q1 by 1.14 ± 0.38". This one contrast is picked from many (5 quintiles x 2 betas plus pairwise). At 3 SE it probably survives, but say it was not pre-specified, and note that Q5, with the largest purchases, does not fit the purchase-size story (already said).
2. **`tab_effect.tex` row "single-tick shock", beta = 0: -0.02 ± 0.01.** At the printed precision this is exactly 2 SE, while 04:247 says the effect "is detectably negative under none". Print three decimals, as 04:240 does for beta = 1.
3. **`main.tex:92`, "reduces BNPL borrowing".** Volume falls 1.1% to 3.9%. Say "slightly reduces".
4. **`05_policy.tex:15`, "playing the role of the FCA's affordability check".** The FCA rule requires *proportionate* checks, not a statutory residual-income test. Say "a strict analogue of".
5. **`03_calibration.tex:318-322`.** The 70% ever-held share is mainly the arithmetic of q_base = 0.05 over 52 ticks (1 - 0.95^52 ≈ 0.93 of eligible households). Comparing it with TransUnion's 57% for 2026 is weak discipline; say so, or drop it.
6. **Accounts against households (B5) and US behavioural parameters (B7).** Both are disclosed where they matter (03:333-338; 03:268-273) and swept where possible. No change needed, but expect a question on B5 in connection with M2.
7. **`01_introduction.tex:47`, "We found no comparable South African study".** Keep a dated search record for the viva (DEFECTS B9).

---

## The reverse problem: what the hedging hides

The limitations are mostly in the right places, and the index in Appendix C is good practice. The hedging becomes a problem in two ways.

- **Repetition.** The sentence pattern "consistent with ..., although the aggregates do not show that ..." appears at 04:46-48, 05:45 and 05:61. "Not detectable" qualifiers are stacked in the RQ answers. Together these make the results read as uniformly null. Say once, in Section 4's opening, that aggregates do not follow households, and drop the repeats.
- **Robust findings not stated as findings.** The thesis does establish several things robustly *within the model*, and should say so plainly:
  - Without peer influence, BNPL raises default by at most a few tenths of a point under every tested rule (maximum 0.52 at beta = 0, across 20 settings).
  - Default is governed by the persistence and rate of income shocks, not by any BNPL-side parameter: Sobol total-order indices are about 0.01 for each BNPL parameter, and the single-tick arm removes the effect.
  - BNPL's harm scales with borrowing volume (the beta, kappa and income-sizing arms all move together).
  - Screening at origination on surveyed income does little in a model where distress comes from later shocks.

  These are useful negative and bounding results. The contribution paragraph (06:29-30) describes the *apparatus* but none of these *findings*. A sentence such as "Within the model, the BNPL channel matters for default far less than the persistence of income shocks, and its effect scales with borrowing volume" would state what the thesis establishes without overreach.

---

## Questions most likely in the viva

1. **On the outcome.** "Of your 13.3% of households in default, how many hold any credit when they default? Why should a debt-free household that cannot pay rent for 98 days count as 'credit distress', and what external figure does 13.3% compare with?" (M1)
2. **On calibration.** "Your 90+ band starts at zero and rises to 19.9%. If you ran the model for four years, what shock probability would you fit, and would the BNPL and bureau effects survive at the QLFS separation rate?" (M2)
3. **On RQ3.** "Isn't the bureau-visibility result simply your lender ceasing to refinance shortfalls over 25 months, with the cost of granted loans falling beyond your horizon? What happens to the households it refuses, compared with those it grants, after two more years, and under your alternative borrowing rules?" (M3)
4. **On invisibility.** "Your research question is about platforms that cannot see one another. Which experiment compares that with platforms that can, and what is the smallest effect of routing or platform count your design could detect?" (M4)
5. **On beta.** "Stacking says beta = 1 is too high; your volume check says beta = 0 is too low. Why not bound beta with those two moments instead of declaring beta = 0 the better guide?" (m3)
