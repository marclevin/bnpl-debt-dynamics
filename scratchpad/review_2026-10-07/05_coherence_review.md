# Coherence review: does the thesis tell one story?

Reviewer pass of 2026-10-07. Read in order: `thesis/main.tex` (abstract), chapters 01 to 06,
appendices A to G, and the generated tables. Line numbers refer to the current source files.
Paths are relative to `thesis/`. No file was edited.

Priority key: **H** = a reader or examiner will notice and it affects how a claim is read;
**M** = a coherence gap that weakens the argument; **L** = a local fix.

---

## 1. The story the thesis actually tells

South African households were already in credit distress in 2017 (14.2% of unsecured accounts
90+ days in arrears), and BNPL then grew outside the view of the bureau and of competing
platforms. The thesis builds a 5,000-household ABM from NIDS 2017 with FinScope inclusion
flags, fits two parameters to the 2017 arrears profile with BNPL disabled, and admits that the
fit is narrow and the external checks are weak (RQ1, "answered only in part"). It then enables
BNPL and finds that multi-platform borrowing becomes common, but how common depends almost
entirely on an assumed routing rule. Default rises only slightly without peer influence
(+0.12 pp) and more with illustrative peer influence (+0.60 pp), where volume is ten times
higher. Default does not respond to platform count or routing (RQ2). Making BNPL visible to
the traditional lender raises default by 0.15 to 0.22 pp, because the lender refuses more
applications and a refused household has no other source of credit. Mandatory screening cuts
BNPL volume but leaves default unchanged (RQ3). **The implied punchline is that, in this
model, the invisibility of BNPL is not what drives distress. Borrowing volume drives it, and
the visibility reform works through credit rationing.** No sentence in the thesis states that
synthesis (see issue 3). The abstract, introduction and conclusion each still frame the work
around "invisible" and "concurrent" obligations, which the results show do not move default.

---

## 2. How each research question is answered

| Question (Section 1.2, `01_introduction.tex:67-84`) | Where answered | Answer given | Does the answer match the question's wording? |
|---|---|---|---|
| **Main question:** how does adding BNPL change "that distress", and how do bureau visibility and screening affect the outcome? | Not answered as a question anywhere. Pieces appear at `06_conclusion.tex:9`. | BNPL raises default by 0.1 to 0.6 pp. Visibility raises default through refusals. Screening has no detectable effect. | **Partly.** "That distress" refers back to the 90+ arrears of `01_introduction.tex:7-9`, but the injection answer is given only as default (the 7-tick cash-flow rule). The 90+ share with BNPL on (14.40 / 14.60 vs 14.20, `tab_baseline_arms`) is never reported as an answer. The conclusion rewords the question (`06_conclusion.tex:7`) and never answers it in the question's own words. |
| **RQ1:** how well does the population reproduce the selected arrears bands, and how does it perform against "benchmarks" not used in fitting? | `03_calibration.tex:486-497`, at the end of Section 3 as promised (`01_introduction.tex:86`) | Answered only in part. Fitted bands are approximated and three of four population checks pass. Intermediate bands, servicing, purchase size and volume, Pattern 3 and the interest measure of Pattern 1 fail. | **Yes**, but the answer depends on BNPL-on results (`tab_bnpl_on_checks`) that come before the reader has seen the BNPL experiments (issue 9). The abstract reports a more favourable RQ1 answer (issue 6). |
| **RQ2 (a):** how often do households owe several platforms at once? | `04_results.tex:84-95`; answer at `04_results.tex:257-263` | 52.0% of final-tick holders under random routing and 36.6% under loyal routing (β=0); 85.1% / 22.0% at β=1. | **Yes**, but the figure depends on the routing assumption and on which seed block is used (issues 4 and 11). |
| **RQ2 (b):** how do enabling BNPL, platform count, access and peer adoption affect default? | `04_results.tex:25-33`, `103-107`, `122-147`; answer at `263-267` | +0.12 pp (β=0), +0.60 pp (β=1). No effect of platform count or routing. Default rises with access only where β>0. No tipping point. | **Mostly.** "Access" is not defined as an experimental variable in the methods (issue 2). The premise "when platforms cannot observe one another" is never varied (issue 3). The quintile results in 4.4 are not part of the answer (issue 12). |
| **RQ3:** how do bureau visibility and mandatory screening change borrowing and distress, with and without peer influence? | `05_policy.tex:35-63`; answer at `05_policy.tex:71-72` | Visibility: +0.22 / +0.15 pp default, more refusals, mostly in Q1. Screening: lower holding and volume, no default effect. Screening halves the visibility effect at β=0. Peer influence does not change either effect. | **Yes.** The RQ asks about "distress", and Section 5 reports default and the 90+ share, which is broader than what Section 4 reports for RQ2 (issue 1). The lever paragraphs (`05_policy.tex:65-69`) answer no RQ (issue 13). |

---

## 3. Issues (in priority order)

### H1. "Distress", "default" and "arrears" carry the RQs but are used in three senses
- **Where:** title (`main.tex:50`); `01_introduction.tex:7-9, 38, 68-69, 83`; `02_model.tex:191-203`; `03_calibration.tex:292`; `05_policy.tex:48, 59`; abstract `main.tex:84` and `88-92`.
- **Problem:**
  - In the title, the introduction and the RQs, "credit distress" means accounts 90+ days in arrears (the 14.2%).
  - In the model, "distress" is a per-tick cash-flow state, and "default" means seven consecutive distressed ticks.
  - At `03_calibration.tex:292` and `05_policy.tex:48, 59`, "distress" is used loosely (illness, "sustained distress", "postpones distress").
  - The headline outcome is default (13.31% at baseline), not the 90+ share (14.20%).
  - The abstract opens with the 14.2% arrears figure and then reports every effect as "default". It never says that default is a model construct distinct from 90+ arrears, so a reader will take the two as the same quantity.
- **Fix:**
  1. Define the outcome once in Section 1.2: "We measure distress by the population default rate (a household that cannot meet committed spending or debt service for seven consecutive fortnights, Section 2.3) and by the 90+ day arrears share among credit-active households."
  2. Reword RQ3 to "change simulated borrowing, default and arrears".
  3. In the abstract, add one clause defining default ("default, which we define as 98 days of consecutive cash-flow shortfall").
  4. Use "distressed tick" for the model state everywhere.
  5. Replace "other distress" at `03_calibration.tex:292` with "other income losses".
  6. Report the 90+ change for the BNPL injection in 4.1 (it is already in `tab_baseline_arms`), so that RQ2 and RQ3 use the same outcomes.

### H2. Most of the experimental design is never set out in the methods
- **Where:** `03_calibration.tex:33-50` (3.1) and `277-322` (3.4, titled "Estimation and Experimental Protocol" but containing only the fit); first appearances in `04_results.tex:122-130, 210-214, 66-69`; the access grid is defined only in the `tab_access` note and register row `appendix_b_register.tex:83`.
- **Problem:** RQ2 names "access" as a factor. The methods never define the access rate (the share of banked households allowed to use BNPL), its seven levels, or what "full access" means. The word "access" in Sections 2 and 3 refers only to banking (`03_calibration.tex:104`; Submodel 12, "Access capped at..."). The following also first appear in the results:
  - the β grid {0, 0.5, 1, 2, 3};
  - the choice of β=1 as the "illustrative" value (`04_results.tex:15`);
  - the decision to run the level sensitivity at β=1 only;
  - the shortfall-only arm (q_base = 0);
  - the population-size arms;
  - the Sobol design (mentioned only as "the variance decomposition", `03_calibration.tex:40`).

  The reader cannot check that every experiment was planned, or which experiment answers which RQ.
- **Fix:** Add a short experiment table to 3.1 or 3.4. Columns: experiment, RQ, factors and levels, β values, replicates, seed block, results table. Rows: injection; platforms × β; access × β (linear and threshold); routing; level sensitivity (β=1); effect robustness (β ∈ {0,1}); Sobol; scenarios 2×2 × β; levers. Define "access rate" there, and give the reason for β=1 once (it currently appears only in the results).

### H3. The RQ2 premise ("platforms cannot observe one another") is never varied, and the conclusion claims it is
- **Where:** RQ2 `01_introduction.tex:79-81`; heading "Invisible Credit and Stacking" `04_results.tex:81`; `04_results.tex:105-107` ("the sweep does not isolate invisibility"); `05_policy.tex:53`; contribution claim `06_conclusion.tex:29` ("so that the visibility gap can be switched on and off").
- **Problem:**
  - The only switch is between the bureau and the traditional lender. No arm lets platforms see one another's exposure (for example, an aggregate limit).
  - The thesis admits that platform count does not isolate invisibility.
  - The screening arm is the one arm in which BNPL lending sees exposure on every platform (`02_model.tex:145-151`, `05_policy.tex:53`), and it leaves default unchanged. That is the nearest test of RQ2's premise, but neither the RQ2 answer nor the conclusion connects it to RQ2.
  - The conclusion's contribution sentence, and the "invisible" framing in the abstract and introduction, therefore suggest more than the experiments show. The thesis's own results show that invisibility is not what moves default; volume is.
- **Fix:**
  1. Reword `06_conclusion.tex:29` to "so that the bureau gap can be switched on and off and the platforms' mutual blindness can be bypassed by screening".
  2. Add one sentence to the RQ2 answer (`04_results.tex:263-267`) or the conclusion: "The only arm in which BNPL lending sees every platform's exposure, screening (Section 5), does not change default detectably."
  3. State the synthesis from Part 1 in the conclusion's opening paragraph: in the model, distress follows borrowing volume and credit rationing, not invisibility as such.
  4. Consider renaming 4.2 "Multi-Platform Borrowing".

### H4. Two different values are given for the fitted 90+ share
- **Where:** `03_calibration.tex:286-289, 373-375` and `tab_arrears_fit` (14.48%, seeds 1,000-); `04_results.tex:21-23` and `tab_baseline_arms` (14.20% "against 14.21%", seeds 10,000-); the abstract says "fit".
- **Problem:** Section 3 says that the selected shock probability overshoots the target (14.48%) and that the target lies between 0.015 and 0.016. Section 4 reports a near-exact match (14.20 vs 14.21) for the same parameter values. The `fig:baseline-arrears` note mentions the calibration run but not the difference. A reader will see two numbers for one quantity, and the "target lies between grid points" argument depends on the seeds (the replicate SD is 0.40, so a 0.28 pp gap between 20-replicate means is about 2 SE).
- **Fix:** Add one sentence at `04_results.tex:21-23`: "On the calibration seeds the same values give 14.48% (Table 3.x); the difference is seed noise of about two standard errors of the mean." Quote one number as "the fit" consistently (preferably the calibration-run number, since that is what was fitted).

### H5. The reason for treating β=0 as "the better guide to magnitudes" conflicts with the thesis's own checks
- **Where:** `04_results.tex:35-40`; repeated at `06_conclusion.tex:18` and in the RQ2 answer `04_results.tex:264-265`. Compare with `04_results.tex:91-93` (loyal routing at β=1 brings ever-stacking down to 51.4%, near the CFPB figure, and the effect stays at 0.62 ± 0.07) and with `03_calibration.tex:457-464` (at β=0 the model is *below* the provider volume band).
- **Problem:** β=0 is preferred because stacking at β=1 far exceeds the CFPB figure. But the thesis then shows that stacking depends on the routing rule, not on default: under loyal routing, stacking at β=1 is near the CFPB figure and the effect is unchanged. So the stacking argument cannot decide the default magnitude. The volume check points the other way:
  - β=0: R1,010 per eligible household, below the R1,333–R4,261 band.
  - β=1 (scaling `tab_baseline_arms` volume by 65.88/6.42): about R10,400 per eligible household, roughly 2.4× above the band.

  The honest reading is that the observed market lies between the two arms. The abstract's "understates BNPL purchase size and volume" holds only at β=0.
- **Fix:** Base the choice on volume, and present the two arms as bracketing the market. For example: "At β=0 volume is below the provider disclosure and at β=1 well above it, so the two effects, 0.12 and 0.60 points, bracket the model's estimate." Remove the stacking justification, or keep it only as supporting evidence. Change the abstract to "understates BNPL purchase size, and volume without peer influence".

### H6. The abstract reports RQ1 more favourably than the RQ1 answer does
- **Where:** `main.tex:87` compared with `03_calibration.tex:486-497` and `06_conclusion.tex:11-12`.
- **Problem:** The abstract lists only the failed purchase-size and volume checks. It omits the failed intermediate arrears bands, the failed debt-to-income pattern (Pattern 3), the failed interest measure of Pattern 1, and the verdict "answered only in part" / "limited confidence in the empirical accuracy of outcome levels". The conclusion lists all of these. The abstract therefore promises a better-validated model than the thesis delivers.
- **Fix:** Rewrite as: "It approximates the two fitted arrears bands and passes three of four population checks under broad tolerances, but misses the intermediate arrears bands, the income profile of debt, and BNPL purchase size and volume, so we read its results as comparisons between arms rather than levels." This adds about 15 words.

### M7. "37% to 52%" in the abstract mixes seed blocks, and 37% is easily confused with the CFPB-comparable 36.8%
- **Where:** `main.tex:88`; `03_calibration.tex:449-450` (36.8% = ever-stacked share, random routing); `04_results.tex:91` (36.6% = final-tick share, loyal routing); `appendix_c_supplementary.tex:81` (compares 52.0→36.6 and 85.1→22.0 across seed blocks, which 4.2 is careful not to do).
- **Problem:** Two different statistics with almost the same value (36.6 and 36.8) answer different questions. The abstract's "37%" is the loyal final-tick share, but a reader who has just read 3.5 will take it as the ever-stacked share. The limitations index makes exactly the cross-block comparison that `04_results.tex:91` and `06_conclusion.tex:15` avoid.
- **Fix:**
  1. In the abstract, quote the same-block pair (36.6% vs 52.6%) or say "about 37% to 53%".
  2. Write "of households holding BNPL at the end of the run".
  3. In `appendix_c_supplementary.tex:81`, use the same-block figures 52.6→36.6 and 85.2→22.0.
  4. Always attach the denominator to these figures: "of final-tick holders" or "of ever-holders".

### M8. The interpretation of the income shock changes between Section 2 and Section 3
- **Where:** `02_model.tex:229` (Submodel 1: "Households whose income is mainly grants... are exempt, because the shock is a job separation"); `appendix_d_variables.tex:86-87`; compare `03_calibration.tex:289-293` (the fitted rate is "a reduced-form hazard of income loss and other distress, such as illness, unexpected bills or family changes"); register `appendix_b_register.tex:37`.
- **Problem:** If the shock stands in for illness, bills and family changes, then exempting grant-dominant households and ending the shock at the QLFS re-employment hazard are both inconsistent with that interpretation. The reinterpretation is introduced to explain why the fitted rate is 1.4× the separation band, but it is never carried back into the mechanism or the limitations index. (The index row `appendix_c_supplementary.tex:73` says "possibly because one channel does the work of several".)
- **Fix:** Pick one interpretation. Either (a) keep "job separation" and treat the 1.4× gap as a calibration limitation (the shock absorbs omitted channels *in wage households only*, which may load default onto wage households), or (b) state in Submodel 1 that the exemption and the recovery hazard are kept for tractability even though the rate is read as reduced-form. Add the resulting bias (non-wage households are never shocked) to the limitations index.

### M9. Section 3 reports BNPL-on results before the reader meets the BNPL experiments, and Pattern 1 is explained twice in a circle
- **Where:** `03_calibration.tex:447-477` (`tab_bnpl_on_checks`: stacking 52.0% / 36.8%, purchase size, Pattern 1 under BNPL); `03_calibration.tex:471-472` forward-refers to 4.1 for the explanation; `04_results.tex:59-64` refers back and repeats it. The CFPB comparison is made three times (`03_calibration.tex:449-453`, `04_results.tex:35-40`, `04_results.tex:91-93`).
- **Problem:** RQ1 includes post-injection checks, so the injection results appear in Section 3 before the injection is introduced in 4.1. The Pattern 1 explanation then bounces between the two sections, and the stacking/CFPB comparison is repeated.
- **Fix:** Either (a) open 3.5 with one sentence such as "Four checks require BNPL to be enabled; they use the β=0 arm of Section 4.1 (Table 4.x)", and remove the repeated Pattern 1 paragraph from `04_results.tex:59-64` (keep one sentence and a back-reference); or (b) move the BNPL-on checks to the end of 4.1 and finish the RQ1 answer there. Make the CFPB comparison once, in 4.2, and refer back to it elsewhere.

### M10. Section 4.1 uses the stacking measures before Section 4.2 defines them
- **Where:** `04_results.tex:35-40` (98.6% ever-stacked at β=1 vs CFPB) comes before `04_results.tex:81-95`.
- **Problem:** The β=0/β=1 framing for the rest of the thesis is justified with a measure that is introduced one subsection later. RQ2 also asks the stacking question *first*, while the results answer it second.
- **Fix:** Put 4.2 (stacking) before 4.1 (injection effect) so the order follows RQ2's wording. Alternatively, move the β choice to the methods (H2) and remove the forward dependency.

### M11. The headline stacking share differs across three seed blocks, and the figure denominators do not match the text
- **Where:** `04_results.tex:84-86` cites `tab:stacking` and `fig:stacking` for "52.0% of final-tick holders". `tab_stacking` gives 52.4 (seeds 20,000-), `tab_baseline_arms` gives 52.0 (10,000-), and the routing block gives 52.6 (70,000-). The `fig:stacking` panel (a) note (`04_results.tex:116`) uses *all households* (9.2%), not holders.
- **Problem:** The reader looks up the cited table or figure and finds a different number or a different denominator.
- **Fix:** Cite only `tab:baseline-arms` for 52.0%. Note once that the platform sweep gives 52.4% on its own seeds. Either plot panel (a) as a share of holders or state in the text that the panel uses all households.

### M12. The quintile results are reported but not carried into any answer, and one of them contradicts the motivation
- **Where:** promise at `01_introduction.tex:130-135` ("users more constrained... we therefore report outcomes by income quintile"); results at `04_results.tex:166-172` (at β=1: Q4 +1.17, Q1 +0.03, so Q4 exceeds Q1 by 1.14 ± 0.38); not mentioned in the RQ2 answer (`04_results.tex:254-267`), the conclusion or the abstract. Only the Q1 result for bureau visibility reaches the abstract and conclusion.
- **Problem:** The introduction leads the reader to expect the poorest households to be hit hardest. For the BNPL effect itself the model shows the opposite (no detectable effect in Q1, the largest in Q4). This finding is reported and then dropped.
- **Fix:** Add one sentence to the RQ2 answer and the conclusion: "With peer influence the rise is concentrated in the middle and upper-middle quintiles and is not detectable in Q1, so the model does not reproduce the concentration among the most constrained that the US evidence suggests; the rise under bureau visibility, by contrast, falls mostly on Q1."

### M13. The lever paragraphs in Section 5 answer no RQ, and the diagnostic they contain belongs in the appendix
- **Where:** `05_policy.tex:65-69` (cooling-off, platform cap, agreements-cap diagnostic). The abstract, RQ3 and the conclusion do not mention the levers.
- **Problem:** RQ3 covers visibility and screening only. Five sentences of lever results, including a definitional diagnostic, interrupt the RQ3 answer and are never used in the conclusion.
- **Fix:** Cut to one sentence ("Two further levers, a cooling-off window and a hypothetical cap on platforms owed, lower default only at β=1 (Appendix C.4)") and move the agreements-cap diagnostic entirely into Appendix C.4. Alternatively, add the levers to RQ3 and the conclusion. Do one or the other.

### M14. The term "benchmark" has three meanings, one of them inside RQ1
- **Where:** RQ1 `01_introduction.tex:78` ("benchmarks not used in fitting"); definition `02_model.tex:23-24` (BNPL-on, no regulatory change); `05_policy.tex:12`; `tab_cooloff` / `tab_cap` ("the benchmark arm of the lever runs", a different seed block, default 13.41 vs 13.30).
- **Problem:** The RQ uses the word that the model chapter then defines as an arm. There are also two "benchmark" arms with different default levels.
- **Fix:** Change RQ1 to "external comparisons not used in fitting or construction" (the wording 3.5 already uses). Call the lever arm "the lever benchmark (seeds 40,000-)".

### M15. "Horizon" is used for three quantities
- **Where:** simulation horizon (`01_introduction.tex:53-54`, `05_policy.tex:48`); default threshold k ("default horizon", `04_results.tex:199`, `tab_robustness`, `tab_effect`); repayment term ("horizons", `03_calibration.tex:213, 228-243`).
- **Fix:** Use "default threshold k" (or "default duration") for k and "repayment term" for loans. Keep "horizon" for the 52-tick run.

### M16. "Burn-in" handling is inconsistent between the prose and the pseudocode, and some volume figures do not state their window
- **Where:** `appendix_g_pseudo_main.tex:19` ("Discard the first T₀ ticks; summarise the run") versus `02_model.tex:201-203` and `03_calibration.tex:37-38` (default counted from tick 1; "ever" quantities include burn-in, per the `tab_baseline_arms` note); `04_results.tex:44` ("cumulative volume is R6.42 million", window not stated; the table says post-burn-in).
- **Problem:** Appendix F says the algorithms govern where they differ from the prose, so the pseudocode as written contradicts the default definition.
- **Fix:** Change the algorithm line to "Summarise: default and 'ever' measures over all ticks; arrears, savings and volume over ticks after T₀". Add "post-burn-in" at `04_results.tex:44`.

### M17. The β=0 control is not reported "in all comparisons" as Submodel 11 claims
- **Where:** `02_model.tex:249` ("β=0 control arm reported in all comparisons"); `appendix_b_specification.tex:66-67`; but the level-sensitivity arms (`tab_robustness`, `tab_robustness_appendix`, `fig:tornado`) are β=1 only (register `appendix_b_register.tex:47`).
- **Fix:** Change the claim to "reported beside every comparison of the BNPL effect". This is also where the reason for running level sensitivity at β=1 belongs (H2).

### L18. The "lim-" labels send readers to sections that do not discuss the point cited
- **Where:** `sec:lim-transfer` sits without a heading inside 3.3 "Debt-Service and Product Parameters" (`03_calibration.tex:268`). It is cited as the place where the transfer assumption is argued (`01_introduction.tex:162, 188`; `06_conclusion.tex:44`; `tab:param-taxonomy`). `sec:lim-reading` (`06_conclusion.tex:32`) is never referenced. The compiled `main.aux` still shows Section 5 as "Three Scenarios..." (stale build only).
- **Fix:** Give the transfer paragraph a run-in heading (`\subsubsection*{Transferred Behavioural Evidence}`) so the reference reads naturally, or point the references to 3.3 by name. Delete the unused label.

### L19. Model text suggests that income is never reduced during unemployment
- **Where:** `02_model.tex:132-134` ("Income is the amount observed in the survey. The model does not reduce it while a member is unemployed") versus Submodel 1 (`02_model.tex:229`), which removes the wage share.
- **Fix:** Write "The lender assesses the household on its surveyed income, which the assessment does not reduce while a member is unemployed, although the household's received income falls (Submodel 1)." `appendix_c_supplementary.tex:128-130` already words it correctly.

### L20. Method features that are introduced but never reported
- `02_model.tex:251`: "λ ... reported against a 0.10–0.48 band" and "Order-cap and limit binding rates reported by quintile". Only limit binding by quintile is reported (`tab_distribution`). The λ band and order-cap binding by quintile do not appear.
- `appendix_d_variables.tex:57`: head demographics are merged but never used.
- **Fix:** Delete the promises or add the two numbers to `tab_distribution` and the λ row of `tab_robustness_appendix`.

### L21. The conclusion does not use the wording of the main question
- **Where:** `06_conclusion.tex:7-9` compared with `01_introduction.tex:67-71`.
- **Fix:** Open the conclusion with the main question and answer it in its own terms (BNPL channel, bureau visibility, affordability screening; outcome = default and 90+ arrears, per H1). Then give the RQ paragraphs. RQ1 and RQ3 answers are closing paragraphs, while RQ2 has its own subsection (`sec:results-answer`). Either give all three a subsection or none.

---

## 4. Terms used in more than one way

| Concept | Variants found (file:line) | Problem | Recommended single term |
|---|---|---|---|
| Outcome of interest | "credit distress" = 90+ arrears (`01_introduction.tex:7-9`, title); "distress" = per-tick cash-flow state (`02_model.tex:191-198`); "distress" loosely (`03_calibration.tex:292`; `05_policy.tex:48, 59`); "default" = 7 distressed ticks | RQs ask about "distress" but the results report "default" | **default** (outcome); **distressed tick** (state); **credit distress** only in the framing, defined once as default plus 90+ arrears |
| Arrears | CCMR account-level bands; "90+ day share, credit-active households" (`05_policy.tex:43`); "traditional arrears rate, all households" (Pattern 1, `03_calibration.tex:467`); "arrears" on BNPL agreements (Submodel 14) | Three denominators | **90+ arrears share (credit-active)**; **traditional arrears rate (all households)**; **BNPL arrears** |
| Who holds BNPL | "BNPL holders" (`main.tex:88`); "final-tick holders" (`04_results.tex:85`); "holders" (`03_calibration.tex:448`); "ever-holders" / "households that ever held" (`03_calibration.tex:461`; `04_results.tex:36, 92`); "holding" = % of all households at final tick (`05_policy.tex:52`); TransUnion "hold a BNPL product" vs "ever hold" (`03_calibration.tex:320-322`) | Abstract and 3.5 omit the denominator | **final-tick holders**; **ever-holders**; **holding rate (% of all households, final tick)** |
| Owing several platforms | "stacking" (Submodel 13 name, the routing mechanism); "stacking depth" (`02_model.tex:253`; `appendix_g_pseudo_main.tex:222`, agreements); "ever-stacked share" (`03_calibration.tex:489`); "owe several platforms"; "balances on two or more platforms"; "cross-platform stacking" (`02_model.tex:345`); Woolard "stacked exposure" = sum of limits (`02_model.tex:251`, `03_calibration.tex:266`) | "Depth" counts agreements in one place and platforms in another; Woolard's exposure is a different quantity | **multi-platform share** (final tick, of holders) and **ever-multi-platform share** (of ever-holders); reserve "stacking" for the mechanism; call Woolard's figure "combined limit" |
| Visibility / reporting | "bureau visibility" (switch); "reporting" (real-world arrangement); "affordability channel"; "scoring channel"; "invisible credit" (`04_results.tex:81`, inter-platform); "visibility gap" (`06_conclusion.tex:29`) | Bureau-to-lender and platform-to-platform invisibility are conflated | **bureau visibility** (switch); **reporting arrangements** (real world); **platform blindness** (inter-platform); drop "invisible credit" |
| Screening | "light automated screen" (Submodel 12); "light screen" (`05_policy.tex:12-13`); "mandatory affordability screening" / "screening test" / "screening arm"; "affordability check" (FCA) | "Screen" names both the benchmark eligibility rule and the intervention | **platform eligibility checks** (benchmark); **affordability screening** (switch) |
| Benchmark / baseline / control / reference | "benchmark" = BNPL-on arm (`02_model.tex:23`), = external targets (RQ1 `01_introduction.tex:78`), = lever arm (`tab_cooloff`); "baseline" = BNPL off; "control" = β=0 and γ=0; "reference arm/value" (sensitivity) and "reference group" (peer) | Four overlapping labels; "reference" used for both an arm and a peer group | **baseline** (BNPL off); **benchmark** (BNPL on, no switch); **control** (β=0 / γ=0); **reference arm** (sensitivity); **peer group** for quintile × province |
| Peer influence | "peer influence", "peer adoption" (RQ2), "peer coefficient", "linear coupling" (`tab_access`), "linear peer rule", "illustrative peer influence" | "Coupling" appears only in a table | **peer influence (β)**; **linear peer rule** vs **threshold rule** |
| Access | banking access (`03_calibration.tex:104`); "Access capped at 82.8%" (Submodel 12); access rate = share of banked households eligible (`tab_access`; register); "full access" | The experimental variable is never defined in the methods (H2) | **access rate** (share of banked households allowed BNPL); "banked share" for 82.8% |
| Caps | "shortfall cap" / "BNPL cap" (`04_results.tex:196`; `tab_effect`); "per-order cap"; "Regulation 23A cap" (`03_calibration.tex:248`); "cap on platforms owed" (lever); "late-fee cap" | Five caps with overlapping names | **shortfall BNPL cap**, **order cap**, **service cap (Reg. 23A)**, **platform cap (lever)**, **fee cap** |
| Horizon | run length; default threshold k; repayment term | See M15 | **horizon** (run); **default threshold k**; **repayment term** |
| Burn-in | default from tick 1 vs "discard first T₀" (`appendix_g_pseudo_main.tex:19`); unlabelled volume (`04_results.tex:44`) | See M16 | State the window with each measure |
| Lender | "traditional lender"; "two classes of lender" (`06_conclusion.tex:29`, includes platforms); "provider" / "firm" (CFPB) | Minor | **traditional lender** vs **platform**; "provider" only for real firms |
| Reporting date | "pre-2026 position" (`05_policy.tex:12`; register `appendix_b_register.tex:79`); "from 2027" (`main.tex:85`); "February 2027" (`01_introduction.tex:33-34`) | The benchmark is dated by different years in different places | "the position before the reporting arrangements (records expected from 2027)" |
| Quintile | "income quintile" (`tab:agent-mapping`) vs "per-capita income quintile" (3.2, tables) | Minor | **per-capita income quintile (Q1–Q5)**, defined once |

---

## Numbers checked and found consistent

- Abstract: 14.2%; 0.1 and 0.6 pp; refusals "about a sixth" (1388/1190 = +17%, 1417/1204 = +18%); 0.15–0.22 pp.
- Pooled +0.12 ± 0.05 and +0.60 ± 0.07 in the results, the policy section and the conclusion.
- 19/20 and 5/20 effect-robustness counts.
- Screening holding drop of 1.9–2.6 pp; "roughly halves" (0.22 → 0.10; 198 → 114 refusals).
- Peer influence +0.53 to +0.61 across arms.
- Lever ranges (−0.28 to −0.39; 31.8–76.3% of volume).
- 1.02 pp amount-rule effect; 0.37–1.27 effect range under the borrowing rules (conclusion) versus 0.25–1.27 across all 19 settings (results). These have different scopes and both are correctly labelled.
- Single-tick 14.05 → 4.81 and the 0.018 effect.
- Validation counts (18 checks = 4 external + 13 construction + 1 diagnostic; "three of four" in the abstract and the conclusion).

The mismatches are those listed in H4, H5, M7 and M11.
