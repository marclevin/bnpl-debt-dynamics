# Structure and presentation against the supervisor's paper

Compared: the thesis at HEAD `2b9b033` (built PDF, 111 pages) and Davids, du Rand, Georg, Koziol and Schasfoort (2021), *Social Learning in a Network Model of Covid-19* (SSRN preprint, 57 pages). This is a structure and presentation review only. Nothing in the repository was changed except this file.

## Verdict

The thesis is already built on the paper's skeleton. Both run introduction (with the literature at its end), model, calibration, results, a separate policy-experiment section, conclusion, then pseudocode appendices split into initialisation and main loop. No restructuring is needed. Where the thesis differs, it is mostly better for a mini-dissertation: it states research questions, its validation is candid, and its inference is explicit. There are three real gaps. First, **four of the six body figures have empty default panels**, including the only figure for RQ3. Second, the introduction never says what the thesis found. Third, the most policy-relevant result, that bureau visibility raises default through refusals, is not one of the conclusion's headline findings and gets no policy paragraph. All three can be fixed without new experiments, and the word changes are neutral or save words.

## Side-by-side outline

| | Supervisor's paper | Thesis |
|---|---|---|
| Front | Abstract (~180 words, findings with numbers, no caveats), keywords, JEL codes | Declaration, abstract (299 words, findings with caveats), data and code, contents, acronyms |
| 1 | Introduction, ~2,700 words: motivation; the model; data; **every result previewed with numbers, section by section**; literature as "two strands" with an explicit contribution sentence | Introduction, ~1,700 words: background; model; scoped contribution; RQs; Related Literature in four themed subsections, "Synthesis and Gap" and Table 1. **No preview of findings** |
| 2 | The Model, ~3,800 words: free-form, not ODD; notation conventions; 3 numbered equations; 2 schematic figures | The Model, ~3,100 words: ODD, data-to-agent table, information-structure figure, 17-row submodel table, 1 equation |
| 3 | Calibration, ~2,500 words: parameter table with sources in the body; 4 free parameters estimated by SMM and Nelder-Mead; validation is one figure and one RMSE | Calibration and Empirical Grounding, ~3,900 words: runs and inference; population; product parameters; 1 fitted parameter; validation over four patterns, with failures stated; answer to RQ1 |
| 4 | Results, ~3,000 words: three subsections, each anchored on a time-path figure with 95% bands | Results, ~4,100 words: six subsections, 7 tables and 3 figures; ends with "Answer to RQ2" |
| 5 | Vaccination strategies, ~800 words: one counterfactual, one figure | Bureau Visibility and Affordability Screening, ~1,300 words: one table, one figure; answers RQ3 |
| 6 | Conclusion, ~400 words: summary, "three insights for policy makers", extensions | Conclusion, ~700 words: RQ1 to RQ3 restated, three findings, data needs, limits, extensions |
| Back | A: result tables; B and C: pseudocode; D: data; E: travel calibration | A: rejected alternatives; B: ODD and register; C: supplementary; D: variables; E: matching; F and G: pseudocode |

Word counts come from pdftotext and include table text, so they are approximate. The thesis's own count is 9,943 body words against the 10,000 cap, so every addition below is paired with a cut.

## The six points in brief

1. **Architecture.** Same order, and the literature sits in the same place. The thesis gives calibration more space (about 27% against 18%) and its policy section less (9%), though that section holds its most distinctive result. This matters a little; recommendations 3 and 5 deal with it.
2. **Model presentation.** The paper uses equations and free-form text; the thesis uses ODD and tables, with one equation. Keep ODD, but write the core rules as equations (recommendation 7).
3. **Calibration, validation, results.** The paper's validation is thin and its results are led by figures. The thesis's validation is far stronger and its results are led by tables (17 against 6 figures). The fault lies with the broken figures and the missing headline figure, not with the tables (recommendations 1, 4, 5).
4. **Abstract and introduction.** The paper tells the reader its results before Section 2; the thesis does not, and an economics reader expects it to (recommendation 2). The abstract's structure was settled in `e892ba6` and is not reopened here.
5. **Conventions.** Contribution paragraph: present, but not positioned strand by strand (recommendation 6). Headline figure: missing (4). Robustness: the thesis is stronger than the paper. Mechanism: present but not promoted. Policy implications: missing (3).
6. **Register.** Both use "we". The paper is promotional and loose; the thesis is plain and heavily hedged. Keep the hedges in the results, and state the main result once, plainly, in the introduction and the conclusion.

## Recommendations, ranked by value

**1. Fix the four empty default panels.** Figures 3(c), 4(a), 4(c) and 6(a) plot default on a y-axis from 12.5 to 15%. Default is now 7.1 to 7.9%, so every point falls off the axis and the panels print empty. The cause is `set_ylim(12.5, 15.0)` hard-coded at lines 122, 167, 169 and 202 of `notebooks/scripts/build_results_figures.py`. It is left over from before the labour-flows rebuild (`07c646b`). Figure 6 is the only figure for RQ3. The supervisor's paper argues through figures, so an empty headline panel is the first thing he will notice. Cost: under an hour, no words. Set the limits from the data, regenerate, rebuild and look at every page. While doing this, check the unused `fig_baseline_arrears.png`: its 120+ bar reads 8.7, but Table 7 gives 8.64.

**2. Preview the findings in the introduction.** Add one paragraph of about 120 words after the contribution paragraph in Section 1.1. It should give the three headline results with numbers: BNPL adds little to default without peer influence and 0.17 points with it; bureau visibility raises default by about 0.17 points through refusals, most in Q1; screening does not change default. Pay for it by folding the conclusion's RQ1 to RQ3 paragraphs (about 255 words) into its "three findings". Those paragraphs repeat the in-section answers at the ends of Sections 3.5, 4.6 and 5. Net change: about 130 words saved. Cost: 1 to 2 hours.

**3. Promote the bureau-visibility mechanism and add a short policy paragraph.** The paper closes with "three insights for policy makers", and its stated key contribution is a mechanism (lockdowns raise compliance before social learning does). The thesis's three findings are all about RQ2. Its most counterintuitive and policy-relevant result appears only in the RQ3 paragraph: visibility works through refusals, refused households have no other credit, and screening alongside visibility removes about two-thirds of the rise. Make that one of the headline findings. Then add about 100 words on what follows for the reporting rollout, with the existing hedges kept: the effect of reporting depends on where refused households go next, screening at the point of sale offsets part of it, and those are the data that are missing. Pay for it from the saving in recommendation 2. Cost: 1 hour.

**4. Plot differences, not levels, and add one headline figure.** The paper can plot levels because its effects are large (up to 50%). The thesis's effects are 0.1 to 0.2 points on a 7% base, with a replicate SD of about 0.2. Even with correct axes, level plots will show overlapping points. Redraw Figure 6(a), and possibly 4(a), as paired changes from the benchmark with 95% intervals, the same way the tornado figure is drawn. Ideally, add one compact headline figure with the BNPL effect at β = 0 and β = 1 and the visibility, screening and combined effects. It would play the role of the paper's Figure 4. The data are already in `results/raw` (`effect.parquet`, `rq3.parquet`). Cost: 2 to 3 hours, no words.

**5. Let figures carry the results and move the duplicate tables to the appendices.** The paper keeps two tables in the body and its numeric tables in Appendix A. Table 11 repeats Figure 3 and Table 12 repeats Figure 4, so both could move to Appendix C. Table 6 could move to Appendix D. Table 15 could move to Appendix C if it is replaced in the body by a forest plot of the BNPL effect under each setting. Keep Tables 7, 9, 10 and 16. This also frees words if tables count toward the cap. Cost: 3 to 5 hours, including cross-references.

**6. Replace "Synthesis and Gap" and Table 1 with a positioning paragraph.** The paper says "our paper relates to two strands" and then "our major contribution relative to these models is". The thesis lists studies by theme, then gives a table whose caption disclaims novelty. Write three sentences, one for each strand. Relative to household-credit ABMs, this model adds lenders that differ in what they observe. Relative to the United States BNPL evidence, it asks the question for a South African survey population. Relative to the regulatory debate, it isolates the affordability channel of reporting. Economics papers rarely use a literature table. This saves words or costs none. Cost: 1 hour.

**7. Write two or three core rules as equations.** Good candidates are the Regulation 23A gate with and without the bureau switch, the distress indicator and k-tick default, and the shortfall split (an agreement of F covers 3F/4). Each equation replaces prose of about the same length. Cost: 2 hours.

**8. Optional: a within-tick flow diagram.** It would replace the seven-step list in Section 2.3, as the paper's disease-progression schematic does for its states. Figure 1 shows who sees what, not the order of events. It saves about 80 words if the list moves into the caption. Cost: 2 to 3 hours of TikZ.

**9. Small conventions.** Rename "4.6 Answer to RQ2" to "Summary", or make it the closing paragraph of 4.5; the paper uses descriptive headings. If the UCT format allows, add keywords and JEL codes under the abstract, for example C63, D14, G51 and G28. Cost: 10 minutes.

**10. Optional, lowest priority: one time-path figure.** Every results figure in the paper is a time path; the thesis shows no dynamics (burn-in, default building up, the 90+ band rising to 11%). The saved outputs are summaries per run, so this needs one existing arm rerun with per-tick logging. That is not a new experiment, but skip it if time is short.

## Things to keep

- **The architecture.** It already matches the supervisor's paper, down to the pseudocode appendices.
- **Research questions with an answer in each section.** A mini-dissertation is marked against its questions; the paper needs none.
- **The validation section and its stated failures.** The paper validates with one RMSE and calls the fit reasonable. An examiner will reward the thesis's candour. Do not cut it down to the paper's level.
- **The inference conventions:** seed pairing, standard errors, the detectability rule, power statements and the multiple-comparison warnings. The paper reports point percentages, and its abstract disagrees with its own Section 5: a 50% cut in fatalities in the abstract against 72% in the text, and 64% more fatalities against 46%. It also gives the social-learning weight as 0.85 in one place and the private weight as ρ = 0.15 in another, and calls 11.28 both a squared difference and an RMSE. Do not copy that looseness.
- **ODD, the submodel table, the provenance table and the generated register.** They are the ABM convention and make the model examinable. The paper's free-form description suits a 57-page paper, not a capped thesis.
- **The scoping sentences up front.** "The experiments measure differences between arms…" is right for a thesis. The paper's near silence on limits is not a model to follow.
- **One fitted parameter and a short introduction.** Copying the paper's SMM estimation would mean new experiments, and a paper-length introduction would take 27% of the cap.
- **The plain, exact register.** Add confidence only where the main result is stated.
