# Thesis review — 21 September 2026

The written sections have been edited for shorter sentences, clearer explanations and more cautious claims. The thesis is ready for the next writing stage after the final simulation, but is not a completed submission: results, scenario outcomes, findings and the abstract remain pending.

The review uses `supervisor_revision_plan.md` as the record of supervisor feedback, together with `SOL_PLAN_REFORMAT.md` and `OVERVIEW.md`. I did not find a separate original supervisor letter or annotated feedback file. The audit below therefore confirms the recorded requests, not any additional feedback held elsewhere.

## Writing changes

I used the direct explanations in the implementation sections of `example.tex` as the style reference. Its ACM layout was not copied. The thesis retains its existing document class, section structure, research questions, equations and citation system.

The edit removes repeated motivation, long chains of clauses, rhetorical contrasts and claims such as “what survives all of them”. It favours a named subject, a concrete action and a short explanation of why the choice matters. It does not claim that prose can be classified reliably as human- or AI-written.

Counts from the existing `scratchpad/wc_prose.py`, using the same counter for the original Git HEAD and revised files:

| Body section | Before | After |
|---|---:|---:|
| Introduction | 2,138 | 1,182 |
| Model | 1,695 | 1,496 |
| Calibration | 2,139 | 1,840 |
| Results, current scope paragraph | 142 | 77 |
| Scenarios, definitions only | 262 | 220 |
| Conclusion, interpretation and extensions only | 439 | 210 |
| **Total written body prose** | **6,815** | **5,025** |

The reduction is 1,790 words, about 26%. These counts exclude floats, appendices and comments; the abstract is still unwritten. Filling Results to 2,100 words, Scenarios to 1,150, Conclusion to 800, adding 250 words of validation and a 250-word abstract would produce roughly 9,068 words before a findings preview. That leaves limited but usable room under the 9,500-word working ceiling. Recount after inserting the results.

## Supervisor-feedback audit

| Recorded request | Present location and status |
|---|---|
| Approved umbrella question and three subsidiary questions | Introduction, Research Questions. Wording preserved. |
| Reporting requirement as the motivation; affordability-only scope | Introduction and Model, Balance Sheets and Information. Credit scoring remains explicitly outside scope. Abstract and numerical policy answer must repeat this after the run. |
| Explain variable construction, especially income | Appendix D gives fields, formulas, missingness, transformations and diagnostics, including wage income, earners, expenditures, savings, debt, servicing and tick conversion. Body pointers retained. |
| Expand cell-donor matching and add an explanatory figure | Calibration, Imputing Financial Inclusion, plus the three-panel figure and Appendix E. Donor weighting, whole-vector transfer, common support, donor reuse and limitations are present. Some overstated statistical claims were corrected. |
| Three crossed scenarios; peer-free controls | Section 5 defines the scenarios and explicitly states the 2 × 3 grid. The final outcome panel is still pending. |
| Remove cooling-off and facility-cap results from the body | Removed the remaining body mentions. Appendix C retains their definitions and instructions for the supplementary results, including peer interactions. |
| Master and subsidiary pseudocode, notation, separate phases | Appendices F and G are present, including the bureau and screening branches. This review spot-checked relevant rules against code; it was not a fresh line-by-line verification of every algorithm. |
| Self-contained float notes | Existing main tables and figures retain explanatory notes. Updated the validation notes and fixed the data-to-agent table overflow. Result-float requirements remain in the drafting notes. |
| Limitations beside the relevant assumptions, no separate discussion chapter | Present in the model and calibration sections, with an appendix index. No standalone discussion or limitations chapter was introduced. |
| Policy argument grounded in retained stacking evidence | Instructions retained but made conditional on the final evidence. Null policy effects alone cannot identify their cause. |

## Substantive corrections

- **Earlier findings were written as final.** Removed assertions of a near-null bureau effect and an established smooth default response. Results and conclusion drafting notes now require the observed outcome, including contrary or uncertain findings. The completed calibration refit remains: its numbers match `results/summary/calibration.json`.
- **Validation was overstated.** The cumulative 60+ arrears share includes the fitted 90+ band. It is now labelled partly fitted. Unfitted bands in the same distribution are not independent observations, and untested counterfactual predictions are not validation.
- **The construction scorecard was misclassified.** Household size uses an external Community Survey benchmark. The text now reports four external benchmark comparisons, three passing, alongside thirteen construction checks and one cap-binding diagnostic. It also notes that the servicing comparator comes from a survey used elsewhere in construction.
- **Matching preserves variation but loses associations.** Whole-vector draws preserve donor combinations and the cell distribution in expectation. They do not eliminate within-cell variation. They can lose associations with unmatched recipient characteristics, which may affect both subgroup outcomes and aggregate default.
- **Initial vulnerability is not initial default.** Zero savings alone does not cause distress. The income-shortfall and zero-savings shares overlap and cannot be read as counts of households already in distress at time zero.
- **Several bounds were unsupported.** Removed the claim that all servicing-sensitive outcomes are upper bounds. Rate ceilings, repayment horizons and expenditure overlap have different effects. A later-vintage spending ratio avoids currency conversion but still assumes transferable spending shares.
- **Activation order does not ration a shared pool.** The lender has no shared funding constraint and platform limits are per household. The rationale now describes implementation and random-draw sensitivity instead of first-come access to scarce aggregate funds.
- **Threshold draws are clipped, not truncated.** The description now matches the implemented clipping, including the possible mass at zero.

## Two implementation qualifications relevant before tonight's run

No simulation code, parameters, data or experiment outputs were changed, and no simulation was started.

1. **Committed-expenditure distress is retained after borrowing.** In `simulation/agents.py`, `committed_shortfall` is recorded before the credit application. The later distress test includes `committed_shortfall > 0`, even if new borrowing supplies enough cash to cover that amount. The thesis now describes the implemented rule. This differs from a general “all obligations remain unaffordable after borrowing” definition and deserves a deliberate modelling decision if that was the intended definition. Changing it would require checking calibration and results again.
2. **The affordability gate is simplified.** `simulation/affordability.py` subtracts the statutory expense norm and visible service from gross household income. It does not separately deduct tax or other statutory deductions. Appendix C now discloses this, alongside the existing household-versus-individual limitation. The gate should not be described as a complete implementation of all regulatory assessment requirements.

The existing open mean-purchase comparison also remains: `OVERVIEW.md` and defect B32 record a choice of comparator population for the R629 versus R992 check. Set a defensible denominator and scope, then report any mismatch; do not choose a tolerance after seeing the final outcome.

## Remaining work after the run

Use only outputs from the final rebuilt population and current parameters. Write the RQ1 assessment, stacking/access results, scenario panel, sensitivity results and supplementary tables before the conclusion, introduction preview and abstract. Keep household/account, banked/eligible/adopting and point-in-time/ever-stacked denominators explicit. Report uncertainty for differences; a difference below twice the raw replicate standard deviation is not automatically “noise”.

The original department-specific declaration and title-page template checks remain open in `main.tex`. They are separate from this writing review.

## Verification and source limits

The revised `thesis/main.pdf` builds successfully with `latexmk`. The final LaTeX log has no unresolved references or citations and no overfull boxes. `git diff --check` passes. Representative introduction, table and pending-results/scenario pages were visually inspected; this was not a page-by-page redesign of the 77-page document.

The FCA's affordability-check framework was checked against [PS26/1](https://www.fca.org.uk/publications/policy-statements/ps26-1-regulation-deferred-payment-credit). FINASA's reporting and potential credit-score effects were checked against its [30 April statement](https://www.finasa.org.za/post/statement-from-fintech-association-of-south-africa-on-buy-now-pay-later-bnpl-reporting-and-regula). FINASA is an industry source, not a regulatory instrument. The DCASA page could not be fetched during this review. No primary instrument confirming the February 2027 South African timetable was located, so that date remains expressly attributed to press reporting. This was a targeted source check, not a full bibliography audit.
