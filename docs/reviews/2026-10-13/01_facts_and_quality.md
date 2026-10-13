# Examiner review 1: facts, accuracy, consistency and completeness

Reviewed at HEAD 2b9b033 on 2026-10-13. The thesis builds cleanly (111 pages, no undefined references). All 140 unit tests pass, and `check_results_tables.py` re-derives 41 table numbers from `results/raw`. I checked the abstract, every RQ answer, the conclusion and about 120 prose numbers against `results_numbers.json`, `contestable_default.json`, `defaulter_credit.json`, `bureau_visible_split.json`, `calibration.json` and `cap_definitions.md`. I spot-checked Table 3, Section 2, the Appendix B register and Algorithms 7 to 10 against `simulation/agents.py`, `lender.py` and `experiments.py`. I also ran one small new check (finding 2), with scratch code only.

## Verdict

This is a careful, honest and reproducible thesis, and I would pass it. Nearly every number traces to a source. The bold "detectable" marks follow the two-standard-error rule throughout, and the pseudocode matches the code. Limitations are stated where the claims are made, not hidden in an appendix. Its weakness lies in what the results mean. The headline effects are small: 0.17 points at β = 1, and nothing detectable at β = 0. The RQ3 result, that bureau visibility raises default, comes largely from the model's own rules. The abstract states three results more firmly than the chapters do. The literature review is thin for a master's, and the front matter is unfinished. None of this needs a large new experiment, and two cheap checks would settle the points most likely to come up. My mark: a solid upper second, at the first-class border (about 72 to 76%), with minor revisions.

## Findings, most important first

**1. The RQ3 headline comes largely from the model's own rules, and the abstract states it without qualification.**
*Where:* abstract (`main.tex:98`); Section 5 (`05_policy.tex:38`, `:53`, `:93`); conclusion, RQ3 paragraph.
*Evidence:* Visibility raises default because a refused household has no other credit, and a refusal causes distress in the same tick. A granted loan, by contrast, is repaid over 25 months, partly after the run ends. The gate also tests surveyed income, not current income. `bureau_visible_split.json` shows that 27 to 30% of the BNPL obligation the lender sees comes from agreements opened in the same tick against the same shortfall. Under the committed-relief rule the effect more than doubles, to 0.40 and 0.42 points. Section 5 says all of this candidly. The abstract instead says "raises ... default by 0.16 to 0.18 points ... because refused households have no other credit" and gives no condition.
*Fix:* (a) In the abstract, add "under the model's assumption that refused households have no other credit and that refusal is immediate distress" (about 15 words). (b) Add one cheap arm in which the bureau shows only agreements opened before the current tick, i.e. a one-tick reporting lag. That is a code change of about 10 lines and about 400 runs, which at roughly 3 seconds a run is minutes on 16 cores. Report it in one sentence. If the rise survives, the result becomes much stronger. If it does not, the thesis must say so.

**2. The claim that the BNPL effect is "at the low end" rests on comparing two model versions, and a cheap check supports it.**
*Where:* `04_results.tex:205-209`; `06_conclusion.tex:37`; Table 22.
*Evidence:* Table 22 shows the separation rate takes about 96% of the variance in default. The thesis's evidence that a higher rate gives a larger effect is the old model, which had no hires and a separation rate of 0.016. No current arm measures the effect at the observed QLFS band. I ran BNPL off and on, with labour flows, on seeds 90,000 to 90,019:

| separation per tick | default without BNPL | effect at β = 0 | effect at β = 1 |
|---|---|---|---|
| 0.00446 (derived) | 7.30% | −0.03 ± 0.08 | +0.08 ± 0.09 |
| 0.00545 (QLFS lower) | 7.89% | −0.00 ± 0.08 | +0.12 ± 0.08 |
| 0.01172 (QLFS upper) | 11.12% | +0.01 ± 0.10 | +0.39 ± 0.11 |

The β = 0 null holds across the observed band. The β = 1 effect grows with the separation rate. Note that the derived-rate effect on this block is not detectable on its own (0.08 ± 0.09), a reminder that single-block β = 1 effects sit at the detection floor.
*Fix:* Add these three rows to Appendix C.6, or as a short table, and cite them at `04_results.tex:205` in place of the earlier-version comparison. Cost: 10 minutes of compute and about 80 words. Note that above the derived rate, employment is no longer constant.

**3. Three abstract sentences disagree with the chapters.**
*Where:* `main.tex:91`, `:95`, `:97`.
- "Default does not change detectably with the number of platforms." Six platforms against one lowers default by 0.15 ± 0.06 points at β = 1, which is detectable (Section 4.2, Table 24). Sections 4.6 and 6 correctly say it "does not rise". Use the same words in the abstract.
- "[The effect] disappears if income losses last one fortnight." Section 4.5 (`:261`) says the single-tick arm also switches off labour flows and "does not isolate persistence". The abstract should say "disappears when income losses are short and there are no labour flows", or drop the clause.
- "Job loss and hiring follow labour-force data, so employment stays constant." Only re-employment comes from the QLFS. Separation is derived from the NIDS stock ratio and sits below the QLFS band. Household income also falls 3.9% over the run. Suggested wording: "Re-employment follows labour-force data, and job loss is set so that employment stays constant."
*Cost:* about 30 words.

**4. The labour market converges to equal unemployment across quintiles.**
*Where:* Section 3.4 (`03_calibration.tex:253-264`); Sections 4.4 and 5 (the Q4 and Q1 results).
*Evidence:* Every employed member separates at the same rate, and every jobseeker is hired at the same rate, whatever their quintile. Jobseekers are concentrated in Q1 (505 of 1,113). So employment drifts: +30% in Q1 and −12% in Q5 over two years (`defaulter_credit.json`). Left running, the model's steady state would have the same unemployment rate in every quintile, which is the opposite of South Africa. The thesis discloses the income drift (H2), but not this steady-state property. The quintile results depend on it: Q4 is the only detectable β = 1 quintile effect and the only detectable screening effect. Q1's income rises 15%, which probably understates the Q1 concentration under bureau visibility.
*Fix:* At minimum, add one sentence in 3.4 stating the steady-state implication (about 40 words). Better: derive separation rates by quintile, p_q = p_exit × U_q / E_q, which holds employment constant within each quintile. Then rerun rq0 and the bureau arm at 20 seeds. That is a small code change and under an hour of compute. If the Q4 results vanish, the "untested candidate" becomes a tested explanation.

**5. The secondary distress measure is promised but never reported in the answers.**
*Where:* Section 1.2 promises the 90+ arrears share as a second measure; the RQ2 answer (`04_results.tex:277ff`) and the conclusion omit it.
*Evidence:* BNPL changes 90+ arrears by −0.05 ± 0.09 points at β = 0 and +0.10 ± 0.10 at β = 1. Neither is detectable (`arrears90_change_*`). The thesis title says "credit distress". Yet the outcome it reports, default, is mostly unpaid food and rent: 84% of defaulters were short of food or rent in every tick of their default streak. The BNPL effect vanishes when credit-financed food is not counted as distress. The credit-specific measure also shows no BNPL effect, and an examiner will notice.
*Fix:* Add one sentence to 4.1 and to the RQ2 answer: "BNPL does not change the 90+ share detectably at either β." Add one sentence in Section 2.3 or 6 on why a cash-flow default is the right construct for "credit distress". About 60 words.

**6. The claim that the cap works "only through the volume it removes" picks one cell of its diagnostic.**
*Where:* `appendix_c_supplementary.tex:226`; `04_results.tex:286`; `06_conclusion.tex:45`.
*Evidence:* The inference rests on β = 1 with a cap of two, where definition (b) gives +0.02 ± 0.05 with 1.4% of volume removed. Other cells of the same diagnostic (`cap_definitions.md`) do not fit "only through volume". At β = 0, definition (b) lowers default by 0.12 ± 0.07 at a cap of two (4.8% of volume removed) and by 0.11 ± 0.05 at a cap of three (0.9% removed). All cap effects are at most 0.12 points and lie at the noise floor.
*Fix:* Replace "only through the volume it removes" with: "No cap changes default by more than about 0.12 points, and the diagnostic cannot separate a platform-count effect from a volume effect at that size." About 40 words in three places.

**7. Small factual slips.**
- `04_results.tex:203-204`: "the 90+ share from 9.10% to 7.60%". The 7.60% is the single-tick arm with BNPL at β = 1 (seed block 58,000). Its matching reference is 9.50%, the exact-shortfall arm on block 50,000, which is also the source of the 7.54% default figure in the same sentence. The 9.10% is the no-BNPL calibration value. Use 9.50%.
- `03_calibration.tex`, Section 3.5, "Against that rate ... 5.1% and 4.2%". The bureau percentages are relative to the scenario benchmark's contestable rates (3.84% and 4.06%), not to the 3.91% just quoted. Say "against each benchmark's rate".
- `04_results.tex` (Section 4.5, purchase size): the volumes and effects "R1,251 and R1,564 ... −0.02 and +0.02" are listed income-first, after the settings were named κ-first. Reorder them.
- `04_results.tex:146`: "At β = 0.5 that estimate is 0.17 ± 0.05 points, the pooled effect at β = 1". This reads as if the two were the same estimate. Write "equal to the pooled effect at β = 1".
- `results/summary/calibration.json` labels the unfitted 90+ share as `objective_column`/`objective_value`. It also reports a `default_rate` of 6.05%, which is a mean over ticks, not the final-tick rate. Anyone reproducing the work will be misled. Rename the keys.
- Register (Table 18): `labour_flows` is marked "sourced", but the hire wage is an assumption. `bnpl_access_rate = 1` is marked "derived", but it is an assumption. `k_cool = 0` is marked "sourced", but only the one-tick arm is.
- The RQ2 answer omits the threshold-rule result: holding rises 30 to 50 points with no change in default. Yet Table 1 poses that question explicitly. Add one sentence.

**8. The literature review is thin for a master's.**
*Where:* Section 1.3, about three pages.
*Evidence:* Missing items an examiner may expect:
- UK transaction-level BNPL evidence: Guttman-Kenney, Firth and Gathergood (2023, *J. Behav. Exp. Finance*), on BNPL paid with credit cards.
- Policy ABMs that test credit limits: Baptista et al. (2016, Bank of England SWP 619), on LTV and LTI limits in a housing ABM. This is the closest methodological precedent for RQ3. Yun and Moon is cited only in Table 17.
- South African household over-indebtedness and reckless-lending literature.

The review describes each source but rarely sets one against another.
*Fix:* 300 to 500 words: one paragraph on policy ABMs, one on SA household debt, and one sentence on the UK evidence. Keep this within the word cap by trimming Table 1's prose.

**9. The front matter and reproducibility details are unfinished.**
*Where:* `main.tex:46-48`, `:66-68`, `:104-106`.
*Evidence:*
- The title page is marked provisional and has no degree statement, supervisor or word count.
- The declaration and the ethics statement are TODOs.
- There are no acknowledgements and no lists of figures or tables.
- Citations are numeric (`plainurl`). UCT economics usually expects author-date, so check the departmental rule.
- The thesis gives no Python or Mesa versions, no commit hash and no archive DOI.
- "The constructed population ... [is] submitted with this thesis": the 5,000 records are unit records derived from licensed NIDS and FinScope data. Confirm that the DataFirst and FinMark licences allow you to redistribute them.

*Fix:* about 2 hours. Add a software-versions sentence and a Zenodo DOI (30 minutes). Ask the supervisor about the data licence before submission.

## Is each research question answered?

- **RQ1:** yes, candidly. The inputs validate, but the arrears dynamics and the level of default do not.
- **RQ2:** yes. The stacking share is admitted to be set by the routing rule, the effects are well bounded, and the inference conventions are applied consistently. The threshold-rule part and the 90+ measure are missing from the answer (findings 5 and 7).
- **RQ3:** yes, but only through the affordability channel. The answer is a statement about the model's refusal mechanism more than about reporting (finding 1).
- **The main question** is answered as within-model comparisons, and the thesis never claims more. The conclusion follows from the results except for the cap wording (finding 6) and the persistence wording (finding 3).

## Three questions most likely in the viva

1. Would the bureau-visibility rise survive a household that could borrow elsewhere, a one-tick reporting lag, a gate on current income, or a horizon longer than the 25-month loan term? In other words, is it a finding about visibility or about refusal?
2. Default is mostly unpaid food and rent, about half of it comes from households short from tick 0, and the BNPL effect vanishes when credit-financed food is not counted. Why is this "credit distress", and why does the 90+ arrears measure show nothing?
3. The separation rate explains nearly all the variance in default. Why derive it rather than use the QLFS band? What does a uniform hazard do to the quintile results?

## Strengths to keep

- Tables are generated from raw results, and prose numbers carry source comments. I found no number without a traceable source.
- The inference convention is explicit: paired seeds, two standard errors, a warning about multiple comparisons, and pooling by precision. It is applied consistently, including in the bold marks.
- The calibration is honest: one fitted parameter, untargeted bands reported as misses, the derived separation rate explained, and the earlier "recession" fit dropped and recorded.
- The analysis decomposes structural default: the 3.5 of 7.3 points from households short at tick 0, with effects re-expressed against contestable default.
- The effect-robustness design: every assumption is run with BNPL off and on (Table 15), and purchase size and volume are checked against provider data.
- The index of limitations (Table 19) points to where each limitation bounds a claim.
- The ODD structure, the generated parameter register, and pseudocode that matches the code line for line.
- The prose is plain and does not overclaim in the body chapters.
