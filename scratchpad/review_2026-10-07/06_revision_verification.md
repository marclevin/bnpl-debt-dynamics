# 06 Revision verification (working-tree diff vs HEAD, 2026-10-07)

Scope: every added or changed sentence in `git diff HEAD -- thesis/ notebooks/scripts/build_results_tables.py`. Checked against the generated tables, results_numbers.json, calibration.json, simulation/*.py, results/raw/{rq0,effect}.parquet and the two editor check scripts. Line numbers are working-tree lines.

## Findings

1. **INCONSISTENT**, 03_calibration.tex:466 vs 03_calibration.tex:350 (tab:patterns), 02_model.tex:235 (Submodel 5), 01_introduction.tex:134, appendix_c:77.
   New: "Pattern~1 therefore does not test the lender-choice rule." Table tab:patterns (unchanged) still says "A reduction falsifies the lender-choice hierarchy". Submodel 5 still says "Compared with Pattern~1". The text also says "We record this as a failure, as specified". Under the stated condition, that failure falsifies the hierarchy, and the new sentence then says the pattern cannot test it. The reader gets both readings.
   Fix: keep the pre-specified condition and add one sentence: "As specified, the interest measure falsifies the lender-choice rule. Neither measure can discriminate, however: interest tracks the book, and the payment order raises arrears whatever the rule." Then change Submodel 5's last cell to "Pattern~1 was specified as a test (Table~\ref{tab:patterns}); Section~\ref{sec:data-validation} explains why it cannot discriminate."

2. **OVERCLAIM**, 06_conclusion.tex:10.
   "Across the experiments, default follows how much households borrow and whether the traditional lender refuses them; how many platforms a household owes makes no detectable difference."
   (a) "How much households borrow": borrowing more on a shortfall *lowers* default (−0.28, −1.02; tab:robustness). At β=0, larger purchases leave the effect unchanged (κ=0.28: −0.02±0.09; income sizing: +0.09±0.07; tab:effect). The default *level* is driven mainly by shock probability and persistence (Sobol; 14.05→4.81). (b) "Whether the lender refuses them" is a household-level claim, but Section 4 says these are population aggregates that do not show which households default. The caveat that refused households are not shown to be the defaulters was deleted from 05 (old lines 61–62).
   Fix: "Across the experiments, the \ac{BNPL} effect on default grows with peer-driven \ac{BNPL} borrowing, and bureau visibility raises default through the traditional lender's refusals; neither the routing rule nor the platform count changes default detectably."

3. **OVERCLAIM**, 06_conclusion.tex:20 and 04_results.tex:33–37.
   "...so the $\beta=0$ effect probably understates the effect at the market's volume."
   The effect grows with β and access. At β=0, raising volume through purchase size does not raise it (κ=0.28 −0.02±0.09; income sizing +0.09±0.07). So "probably understates" holds only if the missing volume would arrive through more frequent, peer-driven borrowing. The same caution applies to 01_introduction.tex:58: "the effect grows with how much households borrow".
   Fix: "...so the $\beta=0$ effect may understate the effect at the market's volume if the extra volume comes from more frequent borrowing; larger purchases at $\beta=0$ do not raise it (Table~\ref{tab:effect})."

4. **MINOR (imprecise referent)**, 04_results.tex:273–274 and 06_conclusion.tex:22.
   "With peer influence the rise is detectable in Q2 to Q4, and not in Q1." The quintile figures come from tab:distribution: BNPL on vs off at β=1 on seeds 10,000–. They do not come from the access sweep. The numbers themselves are correct: Q2 0.56±0.25 (2.2 SE), Q3 0.83±0.27, Q4 1.17±0.32; Q1 0.03±0.22 and Q5 0.49±0.27 (1.8 SE) are not detectable. The conclusion cites tab:access for it.
   Fix: "At $\beta=1$ the \ac{BNPL} effect is detectable in Q2 to Q4 but not in Q1 or Q5 (Table~\ref{tab:distribution})."

5. **MINOR (garbled)**, 06_conclusion.tex:7.
   "...in a model of South African households already exposed to it". "It" now reads as BNPL, but the baseline has no BNPL. The RQ says "already exposed to credit distress".
   Fix: "...households already in credit distress".

6. **MINOR (hedge stronger than evidence)**, 05_policy.tex:47.
   "The model's rules favour this result." The mechanism argued next is right: all-or-nothing grant (lender.py), immediate distress on refusal (agents.py), a 25-month term (lender.py, NEW_LOAN_TERM_MONTHS), surveyed income. But the claim is untested, and the next lines admit that no alternative rule or longer horizon was run.
   Fix: "The model's rules may favour this result."

7. **MINOR**, 05_policy.tex:15.
   "a strict analogue of the FCA's affordability check" can be read as "exact analogue". The screen is stricter than a proportionate check and sees every platform.
   Fix: "a stricter counterpart of".

8. **MINOR (accidental deletion)**, 05_policy.tex old lines 93–97.
   This caveat was removed and does not appear elsewhere: "No lever was run under the alternative borrowing rules of Table~\ref{tab:effect}, and the model has no measure of what a household loses when a purchase or a shortfall loan is refused." The agreements-cap diagnostic does survive in Appendix C (line 182).
   Fix: restore the caveat in app:levers or as an Appendix C index row.

9. **MINOR**, appendix_c_supplementary.tex:83.
   "default differences of about 0.2 points cannot be excluded". At β=1 the routing difference is +0.02±0.13, so differences of about 0.25 cannot be excluded. Section 4.2 says so correctly.
   Fix: "about 0.2 to 0.25 points".

10. **MINOR (scope of new check)**, 04_results.tex:195 and the tab_robustness_appendix note (build_results_tables.py:814–817).
    The 7.3–7.6% single-tick check holds friction at its persistent-shock value of 0.09 (single_tick_calibration_check.py). Friction was not re-fitted, so the claim covers the shock-probability grid only.
    Fix: add "with friction at 0.09".

11. **MINOR (provenance)**, 02_model.tex:198–201, appendix_c:73, build_results_tables.py:815.
    90.5%, 98.4% and 7.3–7.6% are typed in from scripts in scratchpad/. These are not submitted artefacts, and the numbers are not written to results/. This breaks the "every number from generated tables or json" convention in the chapter header comments.
    Fix: move both scripts to notebooks/scripts/ and write their output to results/summary/, or cite them in the Data and Code statement.

12. **MINOR (hedge mismatch)**, 03_calibration.tex:284 vs appendix_c:75.
    The body says "The shock probably absorbs other income losses"; the index says "possibly because one channel does the work of several". Window dependence and the account/household unit mismatch are competing explanations.
    Fix: change "probably" to "may".

13. **MINOR (structure)**, 03_calibration.tex:29 and :265.
    The new "Simulation Protocol" (3.1) sits beside the existing "Estimation and Experimental Protocol". The near-duplicate headings will confuse readers.
    Fix: rename 3.1 "Runs, Replications and Inference", or rename the later one "Estimation".

14. **MINOR (moved content)**.
    tab:imputation_errors, fig:inclusion-fidelity and fig:pop-fidelity moved to Appendix E.5 intact, and their labels survive. Two loose ends: 03_calibration.tex:182–191 now cites them without saying they are in the appendix, and the moved tabnote of tab:imputation_errors refers to "(Appendix~\ref{app:matching})" from inside that appendix.
    Fix: add "Appendix~\ref{app:matching}" at the 03 citations and drop the self-reference.

## Verified as correct

- R10,400: 1,010.13 × 65.878/6.419 = R10,367, and "ten times" (10.26×). β=0 is below the band per eligible (1,010 < 1,333) and per ever-holder (1,196 < 4,261); β=1 is above 4,261. "Bracket" holds.
- 14.20 vs 14.48: SDs 0.41 and 0.40, unpaired SE 0.128, difference 0.274 = 2.1 SE.
- Routing (effect.parquet, recomputed): β=0 −0.071±0.065; β=1 +0.015±0.130. "About 0.2 and 0.25 cannot be excluded" is right. Ever-stacked share at β=1 is 98.6→51.4. Abstract 37–53% (36.6/52.6, same seeds). "About half / just over a third" is right.
- Experiments table vs experiments.py/sensitivity.py: seeds 10k/20k/30k/60k+61k/50k–59k/70k/100k/80k/40k+43k, reps 20 / Sobol 2 / scenarios 100, β grids {0,0.5,1,2,3}, {0,1}, 1, Sobol β∈[0,3], seven access levels, σθ five values, γ∈{0,0.3}, μθ 0.15–0.45, cooling-off 0–4, cap 1–3.
- Sequential calibration vs calibrate.py: grid of 0.008 steps with friction off; friction grid {0,…,0.16}; p re-fitted; fine check at ±0.001; seeds 1,000. Selection in stage 2 is on the 1–30 error, consistent with "smallest absolute error". 13.93/14.48 match.
- 26/12: lender.py `visible_monthly_service` and agents.py screening divide per-tick instalments+arrears by MONTHLY_TO_TICK (12/26). Traditional arrears are excluded (scheduled_service_tick only). Surveyed `income_monthly`.
- BNPL paid before traditional (agents.py). Arrears age bands count traditional arrears only. Committed shortfall counts as distress even with credit. Credit order: service, then discretionary, then savings. Seven ticks = 98 days, the first boundary past 90.
- Mean spell 1/0.018724 = 53.4 ticks > 52.
- Lending, refusals, purchase sizes and "ever" measures are whole-run (metrics.py:269–275); interest and volume are post-burn-in. tab notes and Appendix G updated consistently.
- "Paired except population-size and single-tick arms" matches the ‡ marks.
- Single-tick rounding change in tab_effect (−0.015±0.013, +0.018±0.015; 1.1–1.2 SE).
- 05: 0.22−0.12 = 0.10, SE √(0.04²+0.05²) = 0.06.
- Appendix C counts: 12 rows in the first group, 10 in the remainder.
- "Six" misses in the conclusion match the RQ1 list. 13.3% default level. R633 is "just outside" 35% (36.2%).
- Cross-references resolve: sec:sim-params, sec:lim-calibration, sec:asymmetry, sec:results-injection, tab:experiments, tab:distribution.
- Terminology: random/loyal routing, mandatory screening and default threshold are used consistently. No "default horizon" remains.
- The Gini upper-bound citation (statssa2019inequality) is retained in the tab:validation note.
