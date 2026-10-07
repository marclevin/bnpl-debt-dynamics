# Structure review: thesis against the supervisor's reference paper

Date: 2026-10-07. Read-only review. No thesis files were changed.

- Thesis: `thesis/main.tex` and `thesis/chapters/*.tex` (body 9,803 words by `scratchpad/wc_prose.py`; cap 10,000).
- Reference: Davids, du Rand, Georg, Koziol and Schasfoort (2021), *Social Learning in a Network Model of Covid-19*, SSRN preprint. The brief describes it as a bank/household model. It is actually an agent-based epidemic model of Cape Town with social learning about lockdown compliance. The structural comparison still works, because it is also a calibrated South African ABM that compares counterfactual policy arms.

Word counts for the reference are approximate. They come from the text extraction with figure-axis residue, page furniture and footnote overflow removed as far as possible. Word counts for the thesis use the department's counting rule (`wc_prose.py`).

---

## 1. How the reference is built

### 1.1 Macro-structure and proportions

| Section | Approx. words | Share | Floats in body |
|---|---|---|---|
| 1 Introduction (motivation, model summary, data summary, results preview section by section, literature and contribution at the end) | 2,600 (literature about 780) | 21% | 0 |
| 2 The Model (agents, interactions, disease status updates, behaviour, implementation) | 3,600 | 28% | 2 schematics |
| 3 Calibration (simulation parameters, literature parameters, applying the model to the city, estimating free parameters, validation) | 2,400 | 19% | 2 tables, 1 figure |
| 4 Results (fit with and without the mechanism, sensitivity of the mechanism, interaction with policy) | 3,000 | 23% | 3 figures (2 more at the end) |
| 5 Policy application (vaccination strategies) | 780 | 6% | 1 figure |
| 6 Conclusion (findings, three policy insights, extensions) | 350 | 3% | 0 |
| Appendices: A results tables, B and C pseudocode, D data sources, E travel calibration | -- | -- | 6 tables, algorithms |

Thesis for comparison: Introduction 1,424 (15%), Model 1,874 (19%), Calibration 2,365 (24%), Results 2,212 (23%), Scenarios 1,109 (11%), Conclusion 819 (8%).

The thesis gives Calibration more space than the Model and has a conclusion more than twice the reference's share. Space has already been squeezed from the model description, which is where the reference spends most.

### 1.2 Order of argument within sections

- **Introduction.** Problem and gap, then the model in one paragraph with a pointer to Section 2, then data and free parameters with a pointer to Section 3, then a section-by-section preview of results with headline numbers, then the literature and contribution. The reader knows the answers before the model is described. The literature comes last and is used to position the contribution, not to justify individual rules.
- **Model.** One sentence stating the formal object, then an explicit list of the subsections, then agents, interactions, dynamics, the behavioural mechanism (labelled as the paper's main contribution), and implementation. The section contains no parameter values. These are all deferred to Calibration, apart from a few in footnotes. Pseudocode is in an appendix and the text points to it once.
- **Calibration.** Opens with a four-part roadmap and a count of parameters and input files. The parts are simulation settings (three sentences), literature parameters (a table), data-driven parameters, estimation of the remaining free parameters, and finally validation (one figure and one paragraph).
- **Results.** Opens with purpose, the replication protocol in one sentence and a three-part roadmap. Each subsection opens by linking back to the previous one, sets out the experiment, presents a figure, describes the pattern (shape, timing, peak, duration), explains the mechanism, and closes with a "main insight" sentence.
- **Application.** Motivation and policy relevance, then design, then results with one figure, then a short interpretation.
- **Conclusion.** Mechanism-level summary with almost no numbers (about 1 number per 100 words), three policy insights, then extensions.

### 1.3 Tables, figures and text

- The body carries figures. Every detailed numeric results table is in Appendix A. The text points to those tables only for exact values.
- Figure and table notes are short and descriptive (30 to 80 words), saying what is plotted and over how many runs.
- The text describes patterns ("flattens", "shortens", "brings the peak forward", "non-linear above 0.8") and gives one or two percentages per claim. It does not restate whole table rows.

### 1.4 Limitations

The paper has no limitations section. Simplifying assumptions appear inline, usually in a footnote of one or two sentences (for example, isolation of critical patients, transmission held constant, travel survey covering only work and school trips). The conclusion presents extensions, not caveats. This is too light for a master's examination, so the thesis should not copy it. What the thesis can borrow is the principle that a caveat is stated once, briefly, at the point of use, and not repeated.

### 1.5 Interpretation, openings and density

- Interpretation is concentrated in Results, in mechanism paragraphs and a closing "main insight" paragraph. The conclusion restates findings at mechanism level and draws policy implications.
- Sections open with purpose and roadmap. Subsections open with a link to the previous one.
- Paragraphs are longer than the thesis's (roughly 100 to 180 words) and narrative. A typical paragraph has one claim, its evidence and its explanation.

---

## 2. The thesis as it stands: section-by-section outline

Word counts are body prose under the counting rule.

| Section | Words | Purpose as written | Floats |
|---|---|---|---|
| Abstract (not counted) | ~230 | Context, method, validation, results for all three research questions | -- |
| **1 Introduction** | **1,424** | | 1 table |
| 1.1 Background and Context | 532 | Arrears in 2017; BNPL outside the NCA and the bureau; 2026 reporting changes; United States evidence; what the thesis does; scope statement | |
| 1.2 Research Questions | 143 | Main question, RQ1 to RQ3, and which section answers each | |
| 1.3 Related Literature (4 unnumbered subsections, plus synthesis and gap) | 748 | ABMs of household credit; BNPL evidence; behavioural foundations; regulation; gap table | Table 1 (gap) |
| **2 The Model** | **1,874** | | 3 |
| Opening and purpose | 144 | Overview, appendix pointers, benchmark design | |
| 2.1 Agents and Institutions | 173 | Five entity types | Data-to-agent mapping table |
| 2.2 Balance Sheets and Information | 343 | Information structure, two switches, scoring channel excluded | Information structure figure |
| 2.3 Within-Tick Sequence and State Changes | 412 | Tick length, seven steps, distress and default definitions | |
| 2.4 Credit and Adoption Mechanisms | 18 + 671 | Seventeen-row submodel longtable, then Submodels 4 and 5, 11 and 13 elaborated | Submodel longtable (about 2 pages) |
| 2.5 Implementation and Verification | 112 | Mesa, tests | |
| **3 Calibration and Empirical Grounding** | **2,365** | Answers RQ1 | 11 |
| Opening | 52 | | Provenance table |
| 3.1 Simulation Parameters | 174 | Replications, seed blocks, pairing | |
| 3.2 The Household Population | 470 | NIDS backbone, FinScope match, resampling | Cell-donor figure, imputation table, two fidelity figures |
| 3.3 Debt-Service and Product Parameters | 312 + 77 | Servicing construction, BNPL terms, transfer limitation | Credit terms table |
| 3.4 Estimation and Experimental Protocol | 221 | Two fitted parameters; peer parameters not identified | CCMR target table |
| 3.5 Validation | 1,059 | Patterns, missed bands, scorecard, Gini and debt discussion, BNPL-on checks, Pattern 1 failure, RQ1 answer | Patterns table, arrears-fit table, 18-row scorecard, BNPL-on checks table |
| **4 Results** | **2,212** | Answers RQ2 | 10 |
| Opening | 176 | Standard errors, detectability threshold, multiple comparisons, choice of beta | |
| 4.1 Baseline and the BNPL Injection | 489 | Baseline replication, pooled effect, beta=1 versus CFPB, volume, substitution, Pattern 1 mechanism, shortfall-only arm | Baseline arrears figure, baseline arms table |
| 4.2 Invisible Credit and Stacking | 305 | Stacking shares, routing arm, volume by platform count, default by platform count | Stacking table and figure |
| 4.3 BNPL Access, Peer Influence and Default | 294 | Access gradient, shape, threshold rule, no tipping point | Access figure and table |
| 4.4 Distribution Across Income Quintiles | 177 | Quintile effects, limit binding | Distribution table |
| 4.5 Sensitivity and Robustness | 358 + 259 | Level sensitivity, Sobol, then robustness of the BNPL effect | Robustness table, tornado figure, effect table |
| 4.6 Answer to RQ2 | 153 | Summary | |
| **5 Scenarios for the Lending Environment** | **1,109** | Answers RQ3 | 3 |
| Opening | 260 | Redefines the scenarios, legal caveat, protocol | Scenarios table and figure, switches table (all three before any results text) |
| Results paragraphs | 608 | Visibility, screening, interaction, untested explanations, peer influence | |
| Appendix levers paragraph | 180 | Cooling-off and cap results with numbers | |
| RQ3 answer | 61 | | |
| **6 Conclusion** | **819** | | 0 |
| Opening | 102 | Question, scope, one-line findings | |
| Answers to RQ1 to RQ3 | 384 | Restates the chapter-end answers with standard errors | |
| Contribution | 55 | | |
| Limitations ("lim-reading") | 108 | | |
| Future work | 170 | | |
| **Body total** | **9,803** | | 28 body floats |

Appendices: A rationale (658), B specification and register, C supplementary (gate, activation order, index of limitations, two further levers, supplementary sensitivity, further extensions; 965), D variable construction (1,745), E matching (1,074), F and G pseudocode.

---

## 3. Where the thesis is harder to follow than the reference

### 3.1 Findings are stated three or four times, and interpretation is thin

Each research question is answered at the end of its chapter (Section 3.5 last paragraph, Section 4.6, Section 5 last paragraph). The answers are then restated in the Conclusion with the same standard errors (384 words), and again in the abstract. For example, "52.0%" appears four times in the body, "0.60 ± 0.07" and "0.12 ± 0.05" each appear three times, and the remark that "beta=1 stacks far more than the CFPB evidence" appears in 4.1, 4.6 and the Conclusion.

In the reference, each finding is stated once in full in Results, previewed in the Introduction and abstracted in the Conclusion. The thesis's repetition uses about 500 words that buy no new understanding. Meanwhile there is almost no space anywhere for *what the findings mean*: no discussion of implications for the 2027 reporting arrangements, and no synthesis across RQ2 and RQ3. For example, how do "BNPL raises default mainly via want-driven volume" and "visibility raises default via refusals" fit together? The reference's conclusion spends half its length on exactly this kind of synthesis.

### 3.2 Limitations are argued in many places and indexed three times

The thesis's stated design is that each limitation is argued where the claim it qualifies is made. In practice:

- The same caveat recurs across chapters. The scoring channel is excluded in Intro 1.1, Model 2.2, Scenarios opening, Conclusion limitations and future work. "Not a forecast" appears in the Intro, Scenarios and Conclusion. "Refused household has no other credit" appears in the abstract, Scenarios, Conclusion (twice) and Appendices B and C. "Platform count moves capacity" appears in 4.2, the Conclusion and Appendix C. The detectability threshold appears in 3.1, the Results opening, the Scenarios opening and Appendix C.
- Labelled limitation blocks are scattered: `sec:lim-transfer` sits inside 3.3, `sec:lim-calibration` is 3.4, `sec:lim-validation` is inside 3.5, and `sec:lim-reading` is in the Conclusion. There are also three indexes: Appendix C's 21-row table, Appendix B's "standing flags" and Appendix E.4.
- Nearly every Results and Scenarios paragraph closes with a hedge, such as "the experiment does not isolate this", "these aggregates do not show that ..." or "none of these explanations is tested". Each one is justified, but together they make the argument hard to follow, because the reader meets the qualification before knowing what the main pattern is.

The reference goes too far the other way. A middle course, close to its spirit, is to keep a one-clause qualifier at the point of use and argue each central limitation once in a short dedicated subsection.

### 3.3 Methodological detail interrupts the argument

- **Model chapter carries calibration content.** The submodel longtable's fourth column holds parameter values, sources, sweep ranges and validation targets (for example κ=0.139 from IES, R992 derived from Weaver, the λ comparison with Woolard, re-employment 1.87%). The reference keeps the model free of values and puts all of them in Calibration. The data-to-agent mapping table is also data construction placed in the Model chapter.
- **The switches are defined three times:** in 2.2 (full prose), in Submodel 15, and again in the Scenarios opening (260 words, including a legal caveat).
- **Statistical conventions are split.** Replications, seed blocks and pairing are in 3.1 (174 words). The detectability threshold and multiple comparisons open Results (176 words). The protocol is re-explained in the Scenarios opening. The reference covers its protocol in one sentence at the start of Results plus three sentences in Calibration.
- **Construction diagnostics fill the Calibration body.** The cell-donor schematic, imputation-error table and two fidelity figures test the implementation. The table note itself says agreement "is expected by construction". The reference keeps comparable material (travel-survey mapping) in an appendix.

### 3.4 RQ1 depends on results not yet presented, and the Pattern 1 discussion is split

Section 3.5 reports the BNPL-on checks (stacking against the CFPB, purchase size, volume, Pattern 1). Its Pattern 1 paragraph refers forward to Section 4.1 for the explanation (a smaller traditional book), and Section 4.1 refers back to it and gives that explanation again. The reader meets BNPL-enabled outcomes before the Results chapter has introduced the BNPL injection.

In the reference, validation is purely about the fitted baseline, and model behaviour with the mechanism switched on is entirely in Results.

### 3.5 RQ2 is answered out of order, with forward references

RQ2 asks, in order: (a) how often households owe several platforms, then (b) how enabling BNPL, platform count, access and peer adoption affect default. Results presents (b-enabling) first, then (a) together with platform count, then access and peer adoption. Section 4.6 then summarises in the RQ order, so the order changes twice.

Section 4.1 also pools the injection effect over seed blocks taken from Tables `tab:effect` and `tab:access`, which the reader has not yet seen.

The duplicated baseline evidence is another symptom. Calibration shows the baseline arrears profile as `tab:arrears-fit`, and Results shows it again as Figure `fig:baseline-arrears` on different seeds.

### 3.6 Text restates numbers and does not lead with the pattern

Results prose has about 12 numbers per 100 words and 54 "±" values. The reference has about 6 per 100 words in Results and 1 per 100 in its conclusion. Many thesis paragraphs are one number-dense finding of 70 to 80 words, so the chapter reads as a list of contrasts. Sections 4.1 and 4.5 are the clearest cases. The reference's paragraphs start from the shape of a figure ("flattens without lengthening") and use numbers only to size it.

In the Scenarios chapter, all three floats (two tables and a figure) come before the first sentence of results, so the reader meets 1,000 cells of numbers before the claim.

### 3.7 Section openings and transitions

- Chapter openings state which RQ is answered. That is good and does more than the reference does. However, no chapter except Calibration gives a roadmap of its subsections. The Model chapter's second paragraph is a list of four appendix pointers before the reader knows what the chapter contains.
- Results subsections open with a number ("With BNPL disabled, 13.31% ...") rather than a link to the previous subsection or the question being addressed.
- The Introduction never previews the findings. It maps RQs to sections, but the only place a reader sees the results before Chapter 4 is the abstract. In the reference, the introduction's results preview is its longest part.

### 3.8 Sections whose purpose is unclear or mixed

- **Section 4.5 "Sensitivity and Robustness"** mixes two questions. "What moves the default level" (tornado, Sobol) is secondary to the RQs. "Is the BNPL effect robust" (`tab:effect`) bears directly on RQ2. The RQ-relevant part comes second, as an unnumbered subsubsection.
- **Section 4.4 Distribution** is not in any RQ. It is motivated only in the literature review ("We therefore report outcomes by income quintile"), but its quintile result is used for RQ3 and the abstract.
- **Appendix C** is a mixture: specification detail (gate, activation order), the index of limitations, supplementary results (levers, sensitivity) and extensions.
- **Literature review, "Behavioural Foundations" subsection.** This subsection mainly justifies individual model rules, with forward pointers to sweeps and limitations. The reference's literature review positions the contribution, and its rule justifications sit in the model section.

---

## 4. Recommendations (prioritised)

Each item gives an estimated net change in body words. Tables, figures and appendices are not counted under the cap.

### Priority 1: consolidate findings and limitations, and make room for interpretation

**R1. Rewrite the Conclusion as "Discussion and Conclusion" with four parts, keeping its length roughly unchanged (about 800 words).**
- 6.1 *Findings* (about 280 words, down from 384). Give one paragraph per RQ at mechanism level, with at most one or two headline numbers each and no "±" values, because the chapter-end answers already carry them. Lead with the cross-cutting result, for example "effects scale with volume; stacking shares depend on routing and default does not; visibility acts through refusals".
- 6.2 *Implications for the reporting arrangements* (about 150 words, new). Set out what the affordability-channel result does and does not imply for the 2027 arrangements, and why screening does little in this model. This is where interpretation that is now missing should go, playing the role of the reference's policy insights. Keep it conditional on the model.
- 6.3 *Limitations* (about 250 words, replacing the 108-word `lim-reading` paragraph). Argue the ten central limitations once each, in two or three sentences grouped by what they bound: level of default; behavioural transfer; borrowing and routing rules; detectability; the RQ3 channel (scoring, fallback, horizon). Repoint the labels `sec:lim-calibration`, `sec:lim-validation` and `sec:lim-transfer` here, or to a sub-label for each.
- 6.4 *Future work* (about 120 words, down from 170), keeping the closing priority sentence.
- Move the 55-word contribution paragraph into 6.1's opening.
- Net: about 0.

**R2. Cut repeated caveats at the point of use to one clause plus a pointer to 6.3.** Specific cuts:
- Scoring-channel paragraph in Model 2.2 (lines 155-160, about 60 words): reduce to one sentence.
- Intro lines 39-40 and 57-60: keep one scope sentence, cut about 40 words.
- Scenarios opening legal caveat (line 13) and the "no fallback, two-year horizon" paragraph (lines 48-49): reduce to one sentence, cut about 50 words.
- Calibration `lim-transfer` paragraph (77 words): move into 6.3.
- Calibration 3.5 second and third paragraphs (lines 332-346, about 150 words on why Patterns 1, 3 and 4 are weak): keep the classification of the four patterns in the table note, keep one sentence in the text, and move the argument to 6.3.
- Results: drop "does not isolate / does not show" sentences where 6.3 covers the general point, about 60 words.

Make Appendix C's index point to 6.3 instead of to scattered sections. Net: about -350 words, partly spent in R1.

**R3. Stop restating chapter-end RQ answers in full.** Keep the end-of-chapter answers, which work like the reference's "main insight" paragraphs, but shorten them:
- Section 4.6 down to about 90 words: drop the second statement of the routing-arm percentages and seed-block note, which already appear in 4.2.
- RQ1 answer at the end of 3.5 down to about 90 words.

The Conclusion (R1) then summarises at a higher level instead of repeating. Net: about -100.

### Priority 2: separate model, calibration and protocol, following the reference

**R4. Move parameter content out of the Model chapter.**
- Cut the submodel longtable (`tab:submodels`) to three columns: Submodel, Rule, Source/assumption flag. Move the "Parameters and validation" column into the parameter register (Appendix B.2), which is already generated from code and has the right home.
- Move the data-to-agent mapping table (`tab:agent-mapping`) to Calibration 3.2 or Appendix D, leaving the one-sentence pointer in 2.1.
- Body words are unchanged (floats are not counted), but the chapter shrinks by about two pages and reads like the reference's model section: mechanism only.

**R5. Define the switches once.** Keep the full definition in 2.2 and drop the Submodel 15 prose to "see Section 2.2". Cut the Scenarios opening from 260 to about 110 words: purpose, a one-line reminder of what each arm switches, why there are 100 replications, and the volume rationale. Net: about -150.

**R6. Put all simulation and statistical conventions in one place: Calibration 3.1, retitled "Simulation Protocol".**
- Cut 3.1 to about 110 words: horizon, burn-in, replications, the detectability rule and its power, and the multiple-comparison caution.
- Move the seed-block bookkeeping (lines 42-49) to a short appendix paragraph, since table notes already give seeds.
- Cut the Results opening from 176 to about 60 words: one sentence pointing to 3.1, the choice of beta=0 and beta=1, and a roadmap sentence (see R10).
- The Scenarios opening then needs only the "100 replications" sentence.
- Net: about -170.

**R7. Move construction diagnostics in Calibration 3.2 to Appendix E/D.** Move the cell-donor schematic (`fig:cell-donor`), the imputation-error table, `fig:inclusion-fidelity` and `fig:pop-fidelity`. Keep one paragraph in the body (about 220 words, down from 470) covering what is imputed, how (one sentence), the largest gap, and the resampling Gini shift. In the scorecard (`tab:validation`), keep only Groups C and D in the body (the external and servicing checks) and move Groups A, B and E (construction checks) to the appendix, keeping the sentence that they pass. Net: about -250 words and 4 floats out of the body.

**R8. Move "Implementation and Verification" (2.5, 112 words) to Appendix B or G.** Leave one sentence at the end of 2.3 or 2.4 ("implemented in Python/Mesa; verification tests in Appendix X"). Net: about -90.

### Priority 3: reorder so each RQ is answered in sequence

**R9. Keep RQ1 strictly about the fitted baseline and the population. Move the BNPL-on checks to the start of Results.**
- Move the BNPL-on checks paragraph and the purchase-size, volume and Pattern 1 discussion (Calibration lines 447-484, about 370 words) into a new opening subsection 4.1, "The simulated BNPL market", with Table `tab:bnpl-on-checks`.
- Merge Pattern 1 with the duplicate in current 4.1 (lines 59-64) so it is explained once. Saves about 100 words.
- If RQ1 must keep the "benchmarks not used in fitting" clause for the BNPL market, end 4.1 with one sentence closing that part of RQ1 and point to it from the RQ1 answer.
- Move the baseline arrears comparison into Calibration as a single object. Keep `fig:baseline-arrears` there and send `tab:arrears-fit` to the appendix, or the reverse. Delete the replication of that comparison in 4.1's first paragraph.
- Net: about -150.

**R10. Reorder Results to follow RQ2, and add a roadmap.** Suggested sequence, with current material mapped:
1. Opening: one sentence of purpose and a three-sentence roadmap, with each subsection linked back to the previous one, as the reference does.
2. 4.1 The simulated BNPL market: holding, volume, stacking shares and the routing arm (from current 4.2, first paragraph, plus R9). This answers RQ2(a) first.
3. 4.2 Enabling BNPL and default: the injection effect on its own seed block, substitution for traditional credit, the shortfall-only arm and the Pattern 1 mechanism (from current 4.1).
4. 4.3 Platform count, access and peer adoption: the platform-count default paragraph (from current 4.2) plus current 4.3.
5. 4.4 Robustness of the BNPL effect: lead with `tab:effect`, then a shortened level-sensitivity paragraph. Cut level sensitivity from 358 to about 200 words, keep the single-tick-shock result, and reduce Sobol to one sentence. This puts the RQ-relevant robustness first.
6. 4.5 Distribution across quintiles (or fold into 4.2 and 4.3 as one paragraph each). Either add "and for whom" to RQ2/RQ3 or label it explicitly as supporting RQ3.
7. 4.6 Answer to RQ2: report the pooled effect *here*, once all seed blocks have been shown. This removes the forward references to `tab:effect` and `tab:access` from 4.1.

Net: about -150 from the sensitivity cut. The rest is reordering.

**R11. Move result tables that duplicate a body figure to Appendix C.** The reference keeps numeric tables in an appendix and figures in the body. `tab:stacking` duplicates `fig:stacking`, `tab:access` duplicates `fig:access-default`, and `tab:robustness` duplicates `fig:tornado`. Keep `tab:baseline-arms`, `tab:effect`, `tab:distribution` and the two scenario tables in the body. No word change; three fewer body floats.

### Priority 4: Scenarios chapter, introduction and prose density

**R12. Scenarios chapter.**
- Put the first results paragraph ("Bureau visibility raises default, and screening does not change it detectably") before the floats, and move `tab:switches` after the interaction paragraph.
- Cut the appendix-levers paragraph from 180 to about 50 words: one sentence on what was run, one on the beta=1 result, and a pointer. The agreements-cap diagnostic belongs only in Appendix C.
- Keep the "three features may explain" paragraph. It is the chapter's best interpretation and matches the reference's habit of explaining mechanisms.
- Net: about -130.

**R13. Introduction: add a short findings preview and slim the behavioural literature.**
- Replace the "This thesis examines ..." and scope paragraphs (118 words) with about 170 words. Cover the approach in two sentences, then one sentence per RQ giving the answer and the section where it is answered (absorbing the RQ-to-section sentence), then the scope sentence.
- In "Behavioural Foundations" and "Empirical Evidence", delete the design sentences that the submodel table already carries ("We therefore assign ...", "the propensity to borrow is swept ...", "payment friction is fitted ...", about 80 words). Keep the literature review positioning-focused, as the reference does.
- Net: about -30.

**R14. Paragraph density in Results and Scenarios.** Merge adjacent single-finding paragraphs into units of claim, evidence and mechanism (about 120 to 160 words). Lead each with the pattern ("Peer influence changes how much households borrow far more than how many ever borrow" is a good model, already in 4.1). Keep at most two or three numbers in the text when the table gives the rest, and drop "±" values for contrasts that are not the paragraph's point. Specifically:
- Merge 4.1's six paragraphs into three.
- Merge Scenarios lines 35-39 and 41-46 into one visibility paragraph.

Net: about -150 from removing restated numbers.

**R15. Model chapter opening.** Replace the appendix-pointer paragraph with a two-sentence roadmap of 2.1 to 2.4, and move the appendix pointers to the points of use, where most already exist. Consider moving the stacking subsubsection (Submodel 13) directly after 2.2, since together they make up the "invisible credit" mechanism that is the thesis's equivalent of the reference's core contribution. Net: about -40.

**R16. Appendices.** Split Appendix C:
- Gate and activation order go to Appendix B (specification).
- Levers, sensitivity and the stacking grid make up a "Supplementary Results" appendix placed first among results-type appendices, as the reference puts its results tables in Appendix A.
- The limitations index is either dropped (once 6.3 exists) or kept as a short appendix pointing to 6.3.

Order the appendices by first reference in the body.

### Word budget summary

| Change | Approx. net words |
|---|---|
| R1 Conclusion restructure (adds implications and limitations, cuts restated answers) | 0 |
| R2 One-clause caveats | -350 |
| R3 Shorter chapter-end answers | -100 |
| R5 Switches defined once | -150 |
| R6 Protocol consolidated | -170 |
| R7 Construction diagnostics to appendix | -250 |
| R8 Implementation to appendix | -90 |
| R9 BNPL-on checks moved and Pattern 1 de-duplicated | -150 |
| R10 Sensitivity shortened | -150 |
| R12 Levers paragraph | -130 |
| R13 Intro preview plus literature trim | -30 |
| R14 Fewer restated numbers | -150 |
| R15 Model roadmap | -40 |
| **Total** | **about -1,760** |

That would leave the body at about 8,000 words. This gives room to spend 300 to 500 words where the reference spends more than the thesis: mechanism explanation in Results (one "why" paragraph per subsection, as the reference does) and the implications subsection. The body would still sit comfortably under the cap.

### Suggested target outline (approximate words)

1. Introduction (1,400): background, research questions, approach and findings preview, literature (positioning only), gap table.
2. The Model (1,600): roadmap; agents; information structure and switches; stacking; tick sequence; borrowing and peer submodels; slimmed submodel table.
3. Calibration and Validation (1,700, answers RQ1 for the baseline): simulation protocol; population (short); servicing and BNPL terms; fitted parameters; baseline validation and scorecard (external checks only); RQ1 answer.
4. Results (2,000, answers RQ2): the simulated BNPL market and stacking; enabling BNPL and default; platform count, access and peer adoption; robustness of the effect; distribution; RQ2 answer with pooled estimate.
5. Scenarios for the Lending Environment (900, answers RQ3): design (short); visibility; screening; interaction and explanations; further levers (one sentence); RQ3 answer.
6. Discussion and Conclusion (850): findings; implications for the reporting arrangements; limitations; future work.
