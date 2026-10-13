# Adversarial synthesis of the three 2026-10-13 reviews

HEAD eeddfe3. I rebuilt the thesis, read the sources, and checked every factual claim the reviewers make against `results_numbers.json`, `contestable_default.json`, `cap_definitions.md`, `bureau_visible_split.json`, `results/raw/robustness.parquet`, the generated tables, `simulation/agents.py` and the regenerated figures. Nothing in the repository was changed except this file.

## 1. Verdict on the reports

**Report 01 (facts).** The most useful of the three. Every slip it names is real: the single-tick arm's 90+ comparison uses the calibration value 9.10% where the paired reference on block 50,000 is 9.50% (`rob_amount_shortfall`, `active_90_plus_mean` = 0.0950); the "5.1% and 4.2%" in 3.5 are relative to the scenario benchmarks' contestable rates (3.84%, 4.06%), not to the 3.91% just quoted; the κ = 0.28 and income-sizing volumes are listed income-first; `labour_flows` is labelled "sourced" in the register although the hire wage is imputed; the 90+ measure promised in 1.2 is never reported for the BNPL effect (it is in Table 7 but no sentence reads it); the abstract's platform sentence contradicts the −0.15 ± 0.06 at six platforms. Its weaknesses: it recommends three new experiments (reporting lag, separation band, quintile hazards) and a 300-to-500-word literature expansion, which the author has ruled out and which its own "pass" verdict does not need. Finding 6 is half right: "only through the volume" is too strong, but the (a)-versus-(c) test it criticises is a direct one (0.00 ± 0.06), and the definition-(b) cells it cites are one 2.2-standard-error result among eighteen.

**Report 02 (writing).** Careful and mostly right at the line level. Verified: the hedge template appears five times; Section 6 lines 16-21 repeat 4.6 lines 280-285 almost verbatim; the 3.5 taxonomy calls the missed bands serious and then excuses them; 3:366-369 reports a second "BNPL effect at β = 1" (0.18) a chapter before the headline 0.17 without saying why. Two claims are wrong: 3:394's 30.3% and 4:61's 31% are not "the same share" (seed blocks 10,000 and 20,000; the table row reads 30.6), and the 0.01 standard errors at 5:57 are correct (`rq3r_bureau_default_diff_se_b0` = 0.000132). The "AI-detection risk" framing overstates a plain repetition problem.

**Report 03 (structure).** Right that no restructuring is needed, right that the introduction never says what was found (Section 1 contains no result), and right about the figures, which eeddfe3 has fixed: the hard-coded `set_ylim(12.5, 15)` calls are gone, the three PNGs were regenerated and all default panels now show data. Its "plot differences, not levels" item is overstated: with 100 replicates and standard-error bars, Figure 6(a) shows the bureau rise clearly. Recommendations 5, 7, 8 and 10 (move tables, equations, flow diagram, time path) are hours of cosmetic work with no examiner value for a finished thesis. The 100-word policy paragraph conflicts with the cap and with Section 5's own "not a forecast".

## 2. Consolidated action list, ranked

Body is 9,943 of 10,000 words. Additions below total about +135; cuts total about −245; net about −110. Abstract edits net zero on a 299-word abstract; re-count after editing.

**A1. MUST. Abstract: three sentences disagree with the chapters** (`main.tex` abstract; reports 01 §3, 02 §4).
- "Households often owe several platforms at once, but default does not change detectably with the number of platforms." → "Many users owe several platforms at once, but default does not rise with the number of platforms." (−1)
- "Job loss and hiring follow labour-force data, so employment stays constant." → "Hires follow labour-force data and job losses offset them in expectation." (0)
- "disappears if income losses last one fortnight or if borrowing" → "disappears under one-fortnight income losses without hiring, or when borrowing" (+1)
- "The model has no credit score, so we test reporting through the lender's affordability test." → "Without a credit score, reporting acts through the lender's affordability test." (−5); "because refused households have no other credit" → "because in the model refused households have no other credit" (+3).
- "how BNPL changes household credit distress in South Africa" → "how BNPL changes credit distress in a model of South African households" (+3), matching the conclusion's first sentence; pay with "so we interpret only differences between scenarios" (−3).
- "Screening BNPL requests reduces their volume by 1 to 5% and does not change default detectably." → "Screening BNPL requests does not change default detectably, but added to visibility it removes two-thirds of its rise." (+2). The combined arm is the most policy-relevant RQ3 result and appears nowhere in the abstract or conclusion.

**A2. MUST. Factual slips** (report 01 §7; all verified).
- `04_results.tex:204`: "the 90+ share from 9.10% to 7.60%" → "from 9.50% to 7.60%", and update the source comment to `rob_amount_shortfall`. (0)
- `03_calibration.tex:368-369`: see A6, which removes the misattributed "5.1% and 4.2%" base.
- `04_results.tex:247-249`: swap to κ-first: "R1,564 and R1,251 ... +0.02 ± 0.06 and −0.02 ± 0.07". (0)
- `04_results.tex:146`: "points, the pooled effect at β = 1" → "points, equal to the pooled effect at β = 1". (+2)
- Register (`config.py` source notes, regenerated Table 18): `labour_flows` "sourced" → "derived" or "assumed" (hire wage imputed); `bnpl_access_rate = 1` "derived" → "assumed". `k_cool` can stay: the one-tick value is sourced to the section 66 withdrawal right. (0; the code comment change is a note, not a model change, but rerun `generate_param_register.py`.)

**A3. MUST. Report the 90+ measure the thesis promises** (`04_results.tex` 4.1, after line 25; report 01 §5). Add: "The 90+ share changes by −0.05 ± 0.09 points at β = 0 and +0.10 ± 0.10 at β = 1, neither detectable." (+20, source `arrears90_change_beta*`.) Section 1.2 promises this measure; Table 7 carries it; no sentence reads it.

**A4. SHOULD. Preview the findings in the introduction** (`01_introduction.tex`, new paragraph after line 63; report 03 §2). About 90 words: "Three results follow. Without peer influence, enabling BNPL does not change default detectably; under illustrative peer influence it raises default by 0.17 points from a base of 7.3%, and the effect disappears when borrowing for food and rent is not counted as distress. Default does not rise with the number of platforms. Making BNPL instalments visible to the traditional lender raises default by 0.16 to 0.18 points through refusals, most in the poorest quintile, and screening BNPL requests does not change it." (+90.) An economics reader expects this; the supervisor's paper does it. Paid for by A5.

**A5. SHOULD. Compress the conclusion's RQ paragraphs and add the combined arm** (`06_conclusion.tex:11-32`; reports 02 §2 and 03 §2-3, reconciled). Keep the RQ paragraphs, because a mini-dissertation is marked against its questions, but cut them from 241 to about 130 words: they repeat the answers at the ends of 3.5, 4.6 and 5. Delete "These answers support three findings." Replace 6:16-17 with "Owing several platforms at once is common, at a rate set by the routing assumption (Section 4.2)." In the RQ3 paragraph replace "Mandatory screening reduces BNPL borrowing and does not change default detectably. Neither measure lowers aggregate default under the model's rules." with "Screening alone does not change default detectably; added to visibility it removes about two-thirds of the rise. What reporting does to distress therefore depends on where refused households borrow next, which the model does not represent." This carries the policy reading report 03 asks for in one sentence, with the hedge. (About −110 net.)

**A6. SHOULD. One "BNPL effect at β = 1", not two** (`03_calibration.tex:366-369`; report 02 §8). Replace with: "Among the other households baseline default is 3.91%. Against each arm's rate among those households, the BNPL effect at β = 1 is 4.6% and bureau visibility (Section 5) is 5.1% and 4.2%." (−30.) This also fixes report 01's base error. Keep the source comment.

**A7. SHOULD. The taxonomy in 3.5 contradicts itself** (`03_calibration.tex:413-426`; report 02 §3). Delete "The failures differ in kind."; open with "The serious failures concern how the model generates distress: ...". Replace the last paragraph with "Pattern 3 comes from another model of another country, so missing it matters less." (−25.)

**A8. SHOULD. Soften "only through the volume"** (`04_results.tex:286`, `06_conclusion.tex:43-45`, `appendix_c_supplementary.tex:226-227`; reports 01 §6 and 02 §4 agree). 4:286: "A cap on platforms owed and a cap on agreements that removes the same volume change default equally (Appendix C)." 6:43-45: "Caps on platforms owed and on agreements remove similar volume and change default alike, by at most about 0.1 points, so the sweep gives no sign that platform count matters beyond volume." Appendix: "The cap therefore works mainly through the volume it removes." (0.)

**A9. SHOULD. Break the hedge template** (`05_policy.tex:67-78`, `04_results.tex:175`; report 02 §1). Apply report 02's three rewrites at 5:66-68, 5:69-73 and 5:77-78. "A likely reason, not tested" claims more than an untested mechanism supports. (−10.)

**A10. SHOULD. Cut the repeats that pay for A3 and A4** (report 02 §12). `01_introduction.tex:55-56` (credit score; it is at 2:156 and 6:63) (−19); `04_results.tex:14-17` after the first sentence, keep only "the baseline's 90+ share after burn-in is 9.17%" (−20); `05_policy.tex:35-38` → "arrears and late fees are under 0.5% of the visible obligation, because nearly all BNPL arrears belong to households that have already defaulted" (−25); `04_results.tex:81-88` per report 02 §5 (−15).

**A11. SHOULD. Two sentences for the viva** (report 01 §4, §7).
- `03_calibration.tex:259`, after "12% below it in Q5": "Left running, the uniform hazards would equalise unemployment across quintiles." (+12.) Verified in `agents.py:160-175`: one `shock_prob` and one `shock_exit_prob` for every member, no quintile term.
- `04_results.tex`, RQ2 answer: "Under the threshold rule holding rises 30 to 50 points with no detectable change in default." (+15.) Table 1 poses the question; the answer omits it.

**A12. SHOULD. Report 02's parse fixes** (§7, §9, §10, §13), all verified against the sources: 4:266 "from a default rate without BNPL of 4.38% against 7.24%" → "with default without BNPL at 4.38% instead of 7.24%"; 4:269 "lends about three times as much" → "as much as in the reference arm"; 4:137 "rises by at most 0.11 ± 0.05 points more than" → "the extra rise is at most 0.11 points"; 4:125 "in its control" → "at γ = 0"; 5:95 and 6:29 "Neither measure" → "Neither switch"; 1:133 drop "Pattern 1," (undefined until 3:290); 4:202 "lowers default" → "lowers default at β = 1". (About −5.)

**A13. SHOULD. Front matter and reproducibility** (report 01 §9; outside the body count). Add to Data and Code: "Python 3.14.4 and Mesa 3.5.1 (`simulation/requirements.txt`); the results are those of commit [hash]." Ask the supervisor three things before submission: the declaration wording, whether the department wants author-date citations (the thesis uses numeric), and whether the DataFirst and FinMark licences allow the 5,000 derived unit records to be submitted. The last is a real risk, not a formality.

**A14. SKIP. One-tick reporting-lag arm** (report 01 §1b). Section 5 already discloses that 27 to 30% of the visible obligation is same-tick and that the rules may favour the result; the claim stands as "the direction of the affordability channel". If one experiment were ever run, this is the one, but it would reopen Section 5, Table 16, the abstract and the conclusion.

**A15. SKIP. Separation-band rows and quintile-specific hazards** (report 01 §2, §4). The reviewer's own numbers support the "low end" sentence as written, and the quintile rerun changes the model. A11 covers the disclosure.

## 3. Rejected

- Literature review expansion of 300 to 500 words (01 §8): author's constraint; the cap has no room; the review is marked "thin" by a reviewer who passes it.
- Replace Table 1 with a positioning paragraph (03 §6): the table is uncounted; prose in its place costs words.
- Plot differences, headline figure, move tables to appendices, equations, flow diagram, time-path figure (03 §4, 5, 7, 8, 10): cosmetic for a finished thesis; Figure 6(a) is legible after eeddfe3; a time path needs a rerun.
- Separate 100-word policy paragraph (03 §3): no room; A5 carries it in one sentence.
- Rewrite of the distress rule at 2:190-192 (02 §6): the existing text says the same thing in the same length.
- "31% vs 30.3%" harmonisation (02 §10): different seed blocks, both correct.
- Check the 0.01 standard errors (02 §13): correct.
- Rename "default threshold" at 4:210 (02 §10): Figure 5 was just relabelled to match it (319a695).
- Rename `calibration.json` keys (01 §7): harmless, but not a thesis change; do it only if the scripts are touched anyway.
- Keywords and JEL codes, "Summary" heading (03 §9): harmless; only if the UCT template asks.
- Rewrite `fig_baseline_arrears` (03 §1): the figure is not included in the thesis.

Counts: MUST 3, SHOULD 10, SKIP 2, rejected 11. Net body change about −110 words (to about 9,830); abstract net 0.
