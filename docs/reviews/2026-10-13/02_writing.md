# Writing review, 2026-10-13 (HEAD 2b9b033)

Scope: the abstract (`thesis/main.tex`) and Sections 1 to 6 (`thesis/chapters/01`–`06`). I skimmed the appendices. Line numbers refer to the .tex sources. I read the typeset PDF too. It builds with no undefined references, but the abstract runs onto a second page.

## Verdict

This reads as human academic prose by one careful author. The vocabulary tells are absent. There are no em dashes in the body. None of "crucial", "pivotal", "landscape", "underscore", "delve", "nuanced", "notably", "importantly", "however" or "moreover" appears. "Robust" occurs only as a label, and there are two "rather than" contrasts in the body. The "detectable" convention is applied consistently. Most sentences make one claim with one number and its standard error.

**AI-detection risk: low, rising to medium in four places.** The risk comes from structure, not word choice:
1. A repeated hedge template ("One candidate explanation, not tested, is ...") appears five times.
2. Section 6 copies Section 4.6 almost word for word, and opens its findings with an announcing sentence.
3. Section 3.5 ends with a three-part taxonomy of failures ("The failures differ in kind ...") that reads as designed.
4. Several paragraphs are patched with reviewer-defence sentences until the argument is lost (4:76-88, 5:34-39, 3:361-369).

An examiner would not flag the vocabulary. They would notice the repetition and the patching. The bigger risk is that they read it as a committee-edited text, not as a machine-written one.

## Problems, in priority order

**1. One hedge template, used five times.** 4:175 "One candidate explanation, not tested, is the income drift"; 4:83 "an untested explanation of the fall"; 5:67 "One candidate, not tested, is the income drift of Section 3.4, which is largest in Q4"; 5:69 "Three features of the model could explain why default does not move, none of them tested:"; 5:78 "A likely reason, not tested, is that ...". A formula repeated this often reads as generated. 5:67-68 also repeats 4:175. "A likely reason" claims more than an untested mechanism supports.
- 5:66-68 → "Its one detectable effect on default is in Q4, $+0.23 \pm 0.09$ and $+0.24 \pm 0.09$ points on the same seeds, the quintile discussed in Section~\ref{sec:results-distribution}." (Delete the "One candidate" sentence.)
- 5:69-73 → "Default may not move because a \ac{BNPL} agreement is small beside the room the Regulation 23A test allows, because the test is applied before the income shocks that drive distress, or because a refused shortfall request passes in full to the traditional lender (Algorithm~\ref{alg:gate}); we tested none of these."
- 5:77-78 "A likely reason, not tested, is that screening refuses" → "Screening may refuse"; then add "This is not tested." at the end of that sentence.

**2. Section 6 repeats Section 4.6, and the findings repeat the answers.** 4:280-281 and 6:16-17 are near-identical: "Owing several platforms at once is common ..., at a rate set mostly by the assumed routing rule and by how often households borrow." 4:285 and 6:20-21 repeat "Default does not change detectably with the routing rule and does not rise with the number of platforms." The "about 5% of the default rate among households whose income covers their food and rent" figure appears at 3:367-369, 4:283-284, 6:24-26 and 6:34-35. 6:32 "These answers support three findings." is an announcing sentence followed by a tricolon, and the three findings restate numbers from 6:16-30.
- Delete 6:32.
- 6:16-17 → "Owing several platforms at once is common, but its rate rests on an assumption (Section~\ref{sec:results-stacking})."
- 6:34-37 → "With employment held constant, \ac{BNPL} adds little to default, and the derived separation rate places the effect at the low end (Section~\ref{sec:results-robustness})." (Keep the 5% figure in 6:24-26 and 4:283 only.)

**3. 3:413-426 is a three-part taxonomy, and it contradicts itself.** "The failures differ in kind. The serious ones concern ... the missed intermediate bands ... Other gaps reflect ... Some misses are expected of a stylised model: ... cannot be expected to reproduce an account-level age analysis band by band." The first paragraph calls the missed intermediate bands serious. The third then excuses them. "Cannot be expected to" sounds defensive.
- 3:415 → "The serious failures concern how the model generates distress: ..." (Delete "The failures differ in kind.")
- 3:424-426 → "Pattern~3 comes from another model of another country, so missing it matters less." (Delete the clause about the age analysis band by band.)

**4. Overclaims in the abstract and conclusion.**
- main.tex:88 "how \ac{BNPL} changes household credit distress in South Africa". Section 1 (1:58-60) says the thesis does not estimate the historical effect. → "how \ac{BNPL} changes credit distress in a model of South African households".
- main.tex:91 "Job loss and hiring follow labour-force data, so employment stays constant." The separation rate is derived, not observed, and employment is constant only in expectation. → "Hires follow labour-force data and job losses offset them in expectation."
- main.tex:95 "Households often owe several platforms at once". This is a vague quantifier where a number exists. → "31\% of users owe several platforms at once at some point".
- main.tex:97 "disappears if income losses last one fortnight". That arm also removes hiring, and 4:261 says it "does not isolate persistence". → "disappears with one-fortnight income losses and no hiring".
- main.tex:98 "The model has no credit score, so we test reporting through the lender's affordability test." → "Without a credit score, reporting acts through the lender's affordability test." This pays for "in the model" in the next sentence: "because in the model refused households have no other credit".
- 6:43-45 "so the number of platforms owed matters only through the volume borrowed". 4:84 says the platform sweep "cannot isolate the effect of platforms not seeing one another". "Remove as much volume" also has no referent. → "Caps on platforms owed and on agreements remove similar volume and change default similarly, by at most about 0.1 points, consistent with platform count mattering through volume."
- 1:60-63 "a set of experiments that identify the mechanisms and assumptions on which the effect ... depends". Several mechanisms are explicitly untested. → "and experiments that show which assumptions the effect of \ac{BNPL} on default depends on."

**5. 4:76-88 is patched together.** In order, it covers routing, platform count, a capacity confound, an untested explanation, "The sweep therefore cannot isolate ..." (which follows from the sentence two back), and caps. The cap sentence reads as self-contradicting: "does not change default detectably against the benchmark ...; paired on its own seeds, a cap of two lowers it". "No arm gives platforms a shared view of exposure" is repeated at 4:292.
- 4:81-88 → "Each platform brings its own limit, so platform count and total credit capacity move together, and the sweep cannot isolate the effect of platforms not seeing one another. More capacity may give more shortfall relief, which would explain the fall at $\beta=1$; we did not test this. Against an uncapped arm on its own seeds, a cap of two platforms owed lowers default by $0.11 \pm 0.05$ points at $\beta=1$, as does a cap on agreements; against the benchmark neither is detectable (Table~\ref{tab:cap}; Appendix~\ref{app:levers})."

**6. The central distress rule is too compressed (2:190-192).** "A committed-expenditure shortfall counts as distress even when credit is granted, and the unpaid food and rent are not owed in later ticks. The credit raised pays debt service first, then discretionary consumption, and any remainder is saved." The main BNPL result disappears without this rule (4:264-271), yet the reader cannot tell what happens to the food that was not paid for.
- → "A food or rent shortfall counts as distress even when credit is granted. The unpaid amount is dropped, not carried forward. The credit pays debt service, then discretionary spending, and the rest is saved."

**7. 4:264-271 has an unclear comparison and a non sequitur.** In "from a default rate without \ac{BNPL} of 4.38\% against 7.24\%", "from ... against" does not parse. "Lends about three times as much" does not say than what. "Neither arm is recalibrated. The effect of \ac{BNPL} therefore depends on ..." puts a "therefore" after a sentence it does not follow from.
- → "...: $-0.01 \pm 0.04$ and $+0.02 \pm 0.04$ points, with default without \ac{BNPL} at 4.38\% instead of 7.24\%. Under that rule a loan clears the tick's distress, so households that lose income keep borrowing from the traditional lender, which assesses surveyed income and lends about three times as much as in the reference arm. Neither arm is recalibrated. Within the model, the effect of \ac{BNPL} depends on ..." (Check that "reference arm" is the right comparison.)

**8. Contestable-default numbers are patched into the validation section (3:366-369).** This passage reports the BNPL effect ($0.18 \pm 0.05$) and the bureau effects ($0.19$, $0.17$) a chapter early. They differ from the headline 0.17, 0.18 and 0.16 without saying why, so a reader sees two "BNPL effects at $\beta=1$".
- 3:366-369 → "Among the other households baseline default is 3.91\%, the base for the relative effects in Sections~\ref{sec:results} and~\ref{sec:scenarios}." This saves about 40 words. 4:283 and 6:25 already give the percentages.

**9. Number-dense passages lose the argument.**
- 3:250-262: fourteen numbers in one paragraph. "Income drift", used at 4:175 and 5:68, is never defined. Replace 3:260-262 ("Household income at the final tick is therefore 15.2\% and 3.2\% ... In total it is 3.9\% lower.") with "Household income at the final tick is therefore 15.2\% higher in Q1, 6.1\% lower in Q4 and 3.9\% lower in total. We call this the income drift."
- 5:35-38: "arrears and late fees (Section~\ref{sec:asymmetry}) are 0.3\% of the visible \ac{BNPL} obligation at the applications it assesses at $\beta=0$ and 0.5\% at $\beta=1$, because ..." → "arrears and late fees are under 0.5\% of the visible obligation, because nearly all \ac{BNPL} arrears belong to households that have already defaulted."
- 5:38-39: "Between 27 and 30\% of the obligation is on agreements opened in the same tick ..., which a bureau reporting with a lag would not show." This is a material caveat, and it is left hanging. Move it into the untested-rules sentence at 5:58: "The switches were not run with a reporting lag, under the other rules ...".
- 4:133-141: "default rises by at most $0.11 \pm 0.05$ points more than in the control". "At most X ± SE" does not parse. → "the extra rise in default is at most 0.11 points".

**10. Inconsistent terminology.**
- Comparison arms go by four names. "Baseline" means BNPL off and "benchmark" means BNPL on (2:14-15). "Control" means $\beta=0$ (4:7, 4:136-138) or $\gamma=0$ (4:125). "Reference" is the sensitivity arm. Change 4:125 "in its control" → "at $\gamma=0$", and 4:136-138 "the control's" → "the $\beta=0$ arm's".
- 4:210 "the default threshold" clashes with the Granovetter thresholds two subsections earlier. → "the default streak length".
- 5:95 and 6:29-30 "Neither measure" → "Neither switch". 5:19 uses "switch", and "measure" also means a statistic (2:330, 3:381).
- 3:394 says "30.3\%" and 4:61 says "31\%" for the same stacking share. 4:61 says "the \ac{CFPB}'s 32 to 33\%" and the Figure 3 note says "32\%". Use one figure each.
- 4:202-204 "lowers default from 7.54\% to 4.78\% and the 90+ share from 9.10\% to 7.60\%". 7.54\% is never identified as the $\beta=1$ reference arm. → "lowers default at $\beta=1$ from ...".
- 1:133 cites "Pattern~1" two chapters before Patterns are defined at 3:290. → "(Table~\ref{tab:bnpl-on-checks})" only.

**11. Hedge stack on the tipping point (4:113-120).** The paragraph has three qualifications in a row. 4:115-117 → "..., so nothing in these data suggests one, although seven widely spaced access levels could miss one."

**12. Restated limitations.** The credit-score omission appears at main.tex:98, 1:55-56, 2:156-159, 6:63-64 and 6:66-68. Stacking set by routing appears at 2:329-331, 3:395-396, 4:64-72, 4:280 and 6:16. The baseline 90+ numbers repeat at 4:14-17. Cut 1:55-56 ("The model has no credit score, so it represents reporting only through the traditional lender's affordability test.") and 4:14-17 after the first sentence. These cuts pay for the additions above.

**13. Smaller items.**
- 4:144-147 "$0.17 \pm 0.05$ points, the pooled effect at $\beta=1$" reads as if it were the $\beta=1$ estimate. → "equal to the pooled effect at $\beta=1$".
- 4:255 "When households borrow rarely, larger purchases have little to act on." This is an aphorism. → "At $\beta=0$ a user makes about 2.5 purchases in two years, so purchase size matters little."
- 4:186-188 is a stranded two-sentence paragraph on platform limits. Merge it into 4:179-183 after "small purchases mean small instalments" as "Platform limits also bind more on poorer households: ...".
- 3:438 "which supports the inputs rather than the model" → "which tests the inputs only".
- 5:48-49 "because the switch acts on traditional lending and not on \ac{BNPL} requests" → "because the switch acts only on traditional lending".
- 1:121-123 is a one-sentence paragraph. Join it to the Hamill paragraph.
- 3:334-339 "Debt service is the one clear failure" conflicts with 3:415-417, which lists three serious failures. → "Debt service is the one clear failure in Table~\ref{tab:pop-external}."
- The abstract leaves out the combined-arm result (screening removes about two-thirds of visibility's rise, 5:94-95), and so does 6:23-30. That is arguably the most policy-relevant RQ3 finding. Worth checking: 5:57 reports standard errors of 0.01 when the others are 0.03.

## What works and should not change

- The register: plain verbs, no em dashes, no filler openers, and "detectable" defined once (3:52) and used consistently.
- Honest single-sentence limits where the claim is made: "Being distressed for 98 days is not the same as an account being 90 days in arrears." (2:200); "The model's rules may favour this result." (5:53); "the model cannot say whether visibility helps or harms households" (6:27-28); "chosen after seeing them" (4:175); "so the level of default is not validated" (3:323).
- Plain, human topic sentences: "The effect at $\beta=1$ comes with much more borrowing by about as many borrowers." (4:29); "That near-universal share follows from the model's rules." (4:64); "Neither switch lowers default." (5:19); "Purchase size is poorly measured." (4:243); "Simulation noise is small beside the assumptions." (4:195).
- The mechanism explanations: the $3F/4$ shortfall arithmetic (2:272-279), the tick conversion (2:17-22), the grant-card caveat (3:115-117) and the fallback that was never used (3:125-126).
- The multiple-comparison arithmetic at 4:179-180 and 5:86-89, and the power statements at 3:53-55 and 5:14-16.
- The abstract's sentence order and its one-number-per-claim results.
