# Reformat and Rewrite Plan

## Purpose

This document specifies how I will rewrite the thesis so that its argument follows the structure of
`Davids_duRand_Georg_Koziol_Schasfoort_2021_Covid.pdf`, while retaining Marc's writing style,
research questions, evidence, and appropriate caution. It is a writing and restructuring plan only.
It does not authorise changes to the thesis source files.

The reference paper will be used for its architecture and rhetorical habits, not as a prose
template. Its topic, notation, wording, page design, preprint markings, and sentence-level
idiosyncrasies will not be copied.

## Starting point and binding constraint

As inspected on 8 September 2026, the manuscript has seven body sections:

1. Introduction
2. Existing Literature on Household Credit and Buy Now, Pay Later
3. The Household Population
4. Model Design and Implementation
5. Results and Analysis
6. Discussion and Limitations
7. Conclusion

The current body files contain approximately 7,790 words of prose before the Results and Conclusion
are completed. The existing Results skeleton budgets 3,300 words and the Conclusion skeleton 650.
If those targets were followed without another structural pass, the body would reach approximately
11,485 words. The 9,605-word projection in `scratchpad/SCOPE_REDUCTION.md` therefore no longer
describes the expanded Data and Model drafts.

The rewrite will target **9,500 words at most, counting the abstract conservatively**, even though
the confirmed exclusions are figures, tables, appendices, and the cover page. This leaves at least
500 words below the rough 10,000-word limit for counting differences, late corrections, and captions
if the department counts them.

Before any rewrite begins, Opus's supervisor-driven edits must be complete. I will then establish a
fresh baseline from the resulting files rather than treating the present snapshot as authoritative.

## What the reference paper's structure actually does

The reference paper has six main sections:

1. **Introduction.** It functions as a miniature paper: motivation, mechanism, model, data,
   principal results, policy exercise, contribution, and focused literature review all appear before
   the model section. It has no separate literature-review section.
2. **The Model.** It starts with the simplest formal statement of the model, then moves from agents
   to interactions, state changes, and implementation. Definitions appear where first used.
3. **Calibration.** It cleanly separates what is imposed from data or literature from what is
   estimated. It opens with an inventory of parameter groups and ends with validation.
4. **Results.** It begins from the calibrated benchmark, states the comparison protocol, and then
   varies the mechanism of interest. Figures carry numerical detail; prose interprets contrasts.
5. **A policy application.** The intervention experiment is promoted to its own main section rather
   than being buried inside general results.
6. **Conclusion.** It is short and unnumbered below the section level. It synthesises findings,
   gives policy implications, and names a small number of extensions.

The appendices hold result tables, pseudocode, detailed data-source descriptions, and specialist
calibration material. The main text remains an argument rather than a specification manual.

The useful writing habits are equally important:

- open each main section with its purpose and sequence;
- use present tense and first-person plural for model choices and experiments;
- organise paragraphs around one claim or comparison;
- state the baseline before the counterfactual;
- report a result, contrast it with the relevant control, and immediately explain the mechanism;
- use explicit transitions such as "however", "in contrast", and "finally" only when they mark a
  real turn in the argument;
- let tables, figures, equations, and appendices carry inventories and numerical detail;
- keep the conclusion much shorter than the results.

## Target manuscript

### Front matter - Abstract: 250 words

Write this last. It will contain six moves in this order: the South African regulatory gap; the
counterfactual injection design; the population and calibration basis; the stacking/default result;
the negative peer-threshold result; and the intervention ranking. It must distinguish calibrated
agreement from counterfactual prediction and must not contain a number that is absent from the final
results tables.

### 1. Introduction: 1,500 words

Remove the current `Background and Context` and `Research Questions` subsection headings. The
introduction should read as one continuous, escalating argument, as in the reference paper.

The paragraph sequence will be:

1. Establish the regulated-credit benchmark: Regulation 23A, bureau reporting, and aggregate
   visibility among registered lenders.
2. Introduce the exception: BNPL falls outside that perimeter and creates mutually invisible
   obligations. End with the concrete household-level problem of concurrent facilities.
3. Explain why the question cannot be answered from South African administrative data and why a
   controlled counterfactual model is useful.
4. Describe the model in one paragraph: survey-grounded households, traditional lender, bureau,
   BNPL platforms, shocks, borrowing, repayment, and default.
5. Describe the empirical grounding in one paragraph: NIDS, FinScope, NCR data, calibration, and
   independent checks.
6. Preview the main findings in descending order of importance. Include the smooth rather than
   threshold response as a finding, not an apology.
7. Preview the policy experiment and its mechanism: instruments aimed at individual transactions do
   little where the harm comes from cross-platform accumulation; only the hypothetical facility cap
   directly targets that margin.
8. State the primary question and three subsidiary questions compactly. Preserve explicit research
   questions because they improve examinability, even though the reference paper does not list them.
9. Integrate the literature by contribution rather than by bibliography: household-credit ABMs;
   empirical BNPL harm and stacking; behavioural adoption and repayment; regulatory interventions.
   Each strand should end with the precise gap this model addresses.
10. Close with the contribution and a one-sentence roadmap.

This section will absorb the load-bearing content of the present Literature section. The standalone
Literature section will disappear. The literature synthesis table may remain in the body if it adds
clarity and is excluded from the count, but its prose must not repeat the introduction.

### 2. The Model: 1,850 words

This section will be rebuilt primarily from the current Model Design and Implementation material.
It will describe the mechanism before its calibration and will avoid mixing rules with source
defence.

Proposed subsections:

#### 2.1 Agents and institutions

Define household agents, the traditional lender, the credit bureau, BNPL platforms, and reference
groups. Give only the state variables needed to understand later equations and results. Detailed
attribute mappings belong in a table or appendix.

#### 2.2 Household balance sheets and interactions

Explain income, committed and discretionary expenditure, savings, traditional debt, BNPL debt, and
what each institution can observe. The information asymmetry should be shown once, preferably in a
small flow diagram or compact visibility table.

#### 2.3 Within-tick sequence and state changes

Present the 14-day clock and the household activation sequence. Explain why consumption precedes
debt service and why borrowing follows a realised shortfall. Define distress, arrears, and default
at the point where they enter the sequence.

#### 2.4 Credit and adoption mechanisms

Present the Regulation 23A gate, traditional borrowing, want-driven BNPL use, the peer signal, the
Granovetter robustness variant, pay-in-four repayment, and stacking. Keep the beta-zero control
visible. Equations should be accompanied by plain-language interpretations, not followed by a
second verbal specification.

#### 2.5 Implementation and verification

Use approximately 200 words for Python/Mesa, seeding, activation, and reuse of the affordability
function. Put the test inventory and degenerate-case checks in a table. Pseudocode, the full ODD
register, alternative designs, and activation-order detail go to appendices.

The current 17-row submodel table should be retained only if it can serve as the single definitive
summary. Any prose that merely restates a row will be removed.

### 3. Calibration and Empirical Grounding: 2,000 words

This section will absorb the current Household Population section and the calibration material now
scattered through Model Design, Results, and Discussion. It should mirror the reference paper's
strict separation between sourced quantities and estimated quantities.

Open with a parameter and input inventory: which values are observed, constructed, imported from
literature, fitted, or swept. Then use these subsections:

#### 3.1 Simulation parameters

State population size, tick length, horizon, burn-in, replication, and seed protocol. Do not defend
each choice here if the defence is already in the appendix.

#### 3.2 Household population

Explain NIDS as the balance-sheet backbone, FinScope donor matching, the 2017-Rand convention,
resampling, and the banked-access ceiling. Move question codes, cleaning edge cases, and long lists
of derived variables to the appendix or a table.

#### 3.3 Debt-service and product parameters

Explain the stock-to-flow problem, statutory rate ceilings, repayment horizons, BNPL order sizing,
and credit limits. Clearly label upper bounds, proxies, assumptions, and imported behavioural
parameters.

#### 3.4 Estimation and experimental protocol

Identify the two fitted parameters and their two targets. Then state which parameters remain fixed,
which are swept, and which counterfactual switches answer each research question. Avoid calling a
fitted match validation.

#### 3.5 Validation

Lead with the unfitted 60+ day arrears band and the independently derived average purchase size.
Then provide a scorecard of all checks, identifying which are South African, vintage-matched,
cross-country, directional, or only plausibility checks. Close with an explicit answer to RQ1.

This arrangement converts the present population material from setup into an empirical contribution,
while keeping genuine model validation distinct from calibration.

### 4. Results: 2,100 words

This section will answer the central mechanism question. It will open with the baseline, replication
count, uncertainty convention, and a short roadmap. Every comparison must show the beta-zero control
and identify the denominator for BNPL access.

Proposed subsections:

#### 4.1 Invisible credit and stacking

Show that stacking is emergent rather than coded as a target. Use the one-platform case to establish
that cross-platform stacking is exactly absent there, then show how concurrent facilities change as
platform count rises. Compare the model with the CFPB benchmark only as an order-of-magnitude check.

#### 4.2 BNPL access, peer influence, and default

Report the no-BNPL baseline before BNPL-on outcomes. Separate the financial channel from the social
channel. Give the negative result its own bold lead sentence: default rises smoothly rather than at
a threshold. Present the linear and heterogeneous-threshold specifications together and explain the
structural reason: peer influence spreads adoption, but the model has no channel through which one
household's default damages another household.

#### 4.3 Distribution and mechanism

Show where debt service and default concentrate by quintile. Keep the apparently contradictory facts
together: the credit limit frequently binds but barely changes default because it reduces purchase
size rather than eliminating borrowing. State which direction is partly induced by the lender-choice
rule and which magnitude is genuinely produced by the model.

#### 4.4 Sensitivity and robustness

Use one tornado figure and one compact table. Discuss only parameters that materially change the
answer, especially the borrowing-amount rule. Replicate noise, Sobol results, population-size checks,
activation order, and full sweep grids belong in the appendix unless they change the interpretation.

Limitations will be attached to the claim they qualify rather than repeated in a later standalone
Discussion section. The two load-bearing limits - calibrated baseline and inability to generate a
systemic cascade - must remain visible in the main prose.

### 5. Effectiveness of Policy Interventions: 1,150 words

Promote RQ3 to its own main section, directly paralleling the reference paper's separate vaccination
application. Begin with why the calibrated model is useful for comparing interventions and define
the common counterfactual protocol.

Compare four levers in one ranked table and one principal figure:

1. bureau visibility;
2. mandatory affordability screening;
3. a 14-day cooling-off period; and
4. a **hypothetical** cap on concurrent facilities.

For each lever, report its effect on cumulative BNPL volume and default, then interpret the operative
margin. Distinguish deferral from desistance. Explain the cooling-off result through the peer signal.
Explain the near-null bureau result as a valid finding. Label the facility cap hypothetical every
time it is compared with enacted or proposed instruments. Conclude with a direct answer to RQ3 and
recommend policy direction, not a numerical statutory threshold.

### 6. Conclusion: 650 words

Remove all conclusion subsections. Use four short paragraphs:

1. answer the primary question and summarise the three RQ answers without replaying the results;
2. state the empirical and modelling contributions in descending order of defensibility;
3. state the policy implication and its bounds, including that the exercise is a counterfactual and
   not a forecast of post-2017 South Africa;
4. name only the three most valuable extensions: a contagion channel, better identification of
   adoption parameters, and South African behavioural evidence.

The current standalone Discussion and Limitations section will disappear. Its claim-specific
limitations will move into Sections 3-5; a compact concluding qualification will remain here; and
secondary caveats will sit in an appendix table.

## Word budget

| Component | Maximum prose words |
| --- | ---: |
| Abstract | 250 |
| 1. Introduction | 1,500 |
| 2. The Model | 1,850 |
| 3. Calibration and Empirical Grounding | 2,000 |
| 4. Results | 2,100 |
| 5. Effectiveness of Policy Interventions | 1,150 |
| 6. Conclusion | 650 |
| **Maximum planned total** | **9,500** |
| **Safety margin to 10,000** | **500** |

Tables and figures should reduce prose, not become a way to hide an overlong argument. All captions
will be counted during drafting unless the departmental rule expressly excludes them. The working
limit for ordinary prose will therefore be lower than the formal maximum whenever captions grow.

## Evidence placement

The body should contain no more than six principal figures:

1. population or inclusion fidelity, only if needed for RQ1;
2. baseline arrears profile;
3. stacking depth or platform-count result;
4. default against access and peer influence;
5. intervention comparison; and
6. sensitivity tornado.

The body tables should carry the parameter-source taxonomy, validation scorecard, central outcome
values, and intervention ranking. Full parameter registers, ODD detail, alternative designs,
pseudocode, complete sweep grids, secondary robustness results, and additional caveats belong in the
appendices.

## Rules for preserving Marc's voice

The rewrite will preserve the strongest features already present in the draft:

- lead with the institutional or causal fact, not a generic topic sentence;
- use precise causal chains, especially the sequence from exemption to non-reporting to incomplete
  affordability assessment to stacking;
- prefer concrete nouns and verbs over abstract academic padding;
- distinguish what is measured, derived, fitted, assumed, swept, and predicted;
- name failed checks and falsified hypotheses directly;
- keep memorable formulations only where they clarify a mechanism, for example the distinction
  between households catching BNPL from neighbours and not catching financial distress from them;
- use cautious claims without burying the result in caveats;
- retain South African institutional specificity.

I will not import the reference paper's weaker habits: long result inventories in the introduction,
repetitive roadmaps, awkward passive constructions, or claims stronger than the design permits.

## Rewrite sequence

The writing order will differ from the reading order:

1. **Freeze the post-Opus baseline.** Record the changed files, compile status, exact section word
   counts, unresolved comments, final RQs, and whether final simulation outputs exist.
2. **Build the six-section shell.** Agree the file map, move headings and labels, and compile before
   rewriting prose. Do not leave duplicate Literature or Discussion sections in the shell.
3. **Rewrite the Model.** This is least dependent on final numerical outputs and establishes the
   vocabulary used everywhere else.
4. **Rewrite Calibration and Empirical Grounding.** Consolidate data, parameter provenance,
   calibration, and validation. Produce the source taxonomy and validation scorecard first.
5. **Write Results from final outputs only.** Create the final tables and figures, then write prose
   that interprets them. Do not copy provisional values from `STATUS.md` into the thesis.
6. **Write the policy section.** Use the same baseline, seeds, denominators, and uncertainty rules as
   the central results.
7. **Distribute limitations.** Attach each limitation to its affected claim, then place only
   secondary caveats in the appendix.
8. **Rewrite the Conclusion.** Answer the RQs, state contributions, bound the claims, and name three
   extensions.
9. **Rewrite the Introduction.** Once the paper's actual results and contribution are fixed, write
   the miniature-paper opening and integrated literature review.
10. **Write the Abstract.** Verify every number against the final tables.
11. **Perform a compression pass.** Remove repeated definitions, repeated numerical narration,
    section previews that add no orientation, and any paragraph that does not advance a claim.

## File-level implementation map

The eventual implementation should use filenames that match the new argument:

| Target file | Source material |
| --- | --- |
| `01_introduction.tex` | Current Introduction plus compressed, integrated Literature |
| `02_model.tex` | Current Model Design and Implementation, stripped of calibration detail |
| `03_calibration.tex` | Current Household Population plus parameterisation, estimation, and validation |
| `04_results.tex` | Final baseline, stacking, default, distribution, and robustness results |
| `05_policy.tex` | Intervention experiment currently planned inside Results |
| `06_conclusion.tex` | Current Conclusion plus only the necessary synthesis from Discussion |

The existing appendix files should be retained and reorganised rather than discarded. File renaming
must occur only after Opus has finished, because concurrent structural edits would create avoidable
merge conflicts. Labels should be semantic (`sec:model`, `sec:calibration`, `sec:policy`) rather than
preserving obsolete chapter numbers.

## Claim-control checklist

Before sign-off, the rewrite must satisfy all of the following:

- The manuscript calls the experiment a controlled 2017 counterfactual, not an account of what
  happened in South Africa after 2017.
- The baseline fit is called calibration; only held-out comparisons are called validation.
- Every BNPL access percentage states whether its denominator is eligible/banked households or all
  households.
- Every key comparison contains a no-BNPL or beta-zero control as appropriate.
- Stacking is described as emergent, not programmed.
- The smooth response and failed threshold hypothesis are prominent in the Abstract, Results, and
  Conclusion.
- Claims about systemic cascades are excluded because the model has no contagion channel.
- The bureau-visibility near-null result is reported without being reframed as model failure.
- The concurrent-facility cap is always identified as hypothetical.
- Policy language concerns direction and mechanism, not an estimated optimal legal threshold.
- Provisional results are replaced with final-run values everywhere, including captions and
  appendices.
- Each research question is answered once explicitly and supported by one clearly identified
  evidence block.

## Verification and completion criteria

The rewrite will be complete only when:

1. `texcount` and a second manual count agree that counted prose is below 9,500 words under the
   conservative counting rule;
2. the LaTeX project compiles without unresolved references, citations, missing figures, overfull
   boxes, or stale section numbers;
3. every table and figure is introduced before it appears and interpreted after it appears;
4. every result in the Abstract and Conclusion can be traced to a final table or figure;
5. a duplication audit finds no repeated definition of the regulatory gap, counterfactual design,
   default rule, peer mechanism, or principal limitations;
6. a terminology audit confirms consistent use of `calibration`, `validation`, `distress`,
   `default`, `access`, `adoption`, `facility`, and `stacking`;
7. rendered-page review confirms readable tables, non-crowded figures, coherent section starts, and
   an article-like visual rhythm; and
8. a final read-through shows the same argumentative sequence at three scales: Abstract,
   Introduction, and full paper.

## Definition of success

The final paper should feel structurally related to the supervisor's paper without sounding written
by its authors. A reader should encounter one continuous arc: a regulatory visibility problem;
a model designed to isolate it; transparent calibration to a South African household population;
evidence on stacking and default; a distinct policy experiment; and a concise statement of what the
model can and cannot establish. It should remain recognisably Marc's work: direct, mechanism-led,
empirically explicit, and unusually candid about identification and model limits.
