# Language audit D: Abstract, Data and Code, Sections 1-3

Scope: `thesis/main.tex` (Abstract, lines 105-116; Data and Code, lines 125-133), `thesis/chapters/01_introduction.tex`, `02_model.tex`, `03_calibration.tex`, and the two generated tables they include (`generated/tab_arrears_fit.tex`, `generated/tab_bnpl_on_checks.tex`). I skimmed `04_results.tex` lines 1-120 only to check that terms carry over. Read-only: no repo file was edited.

Format of each finding: **ID. [category, SEVERITY] file:line**. Then the exact quoted text, which is one source line so it can be found with grep (a long sentence is quoted from the line where it starts), what is wrong, and a rewrite.

Mechanical sweeps that found nothing: there are no em dashes, no "However/Moreover/Notably/Importantly/Furthermore" openers, no "delve/crucial/robust/nuanced/leverage/underscore/highlight", no "in order to", and no US spellings ("behaviour", "modelled", "instalment", "initialisation", "winsorised", "ageing" and "finalised" are used throughout). "Percentage point" is used correctly everywhere: relative changes (8% lower, 33% low, refusals up about 13%, income 15.2% above) are percent, and differences in rates are points. "Judgments" (03:349) is the correct legal spelling. Hyphenation is consistent: credit-active, pay-in-four, want-driven, two-year, debt-to-income, residual-income test, write-off rate, re-employment, per-capita.

---

## Cross-cutting HIGH finding: a result that follows from the rules is reported as a finding

**X1. [tautology, HIGH] main.tex:114; 01_introduction.tex:64-67; 03_calibration.tex:395 (and the screening half at main.tex:116, 01:66-67)**

> `The effect runs through households that use \ac{BNPL} to bridge cash shortfalls and then fall more than 90 days behind on it, most of them households whose surveyed income does not cover food and rent; it is not detectable when \ac{BNPL} cannot be used against a shortfall.` (main.tex:114)
> `The first group carries most of the \ac{BNPL} effect.` (03:395)
> `the Regulation 23A test lowers it by about as much as \ac{BNPL} adds.` (01:67)

**Problem:** For these 120 households surveyed income is below food plus rent, so no credit can be repaid from income. The Regulation 23A test, which uses the same surveyed income, will refuse most of them. The platforms' screen (banked, not in default, within λ times income) does not compare income with costs. So the result that BNPL raises their default, and that screening with the 23A test removes most of the effect, follows largely from the rules. The text presents it as something the model found, and an examiner will say so.

What the model does add is the size (47% to 85% of the group) and the small effect elsewhere (+0.11 points, not detectable). The fix is to say plainly which part is mechanical. Confirm the refusal claim against the code before using the wording below.

**Rewrite (03:395):** "The first group carries most of the BNPL effect, and the rules make this expected: these households cannot repay any credit from income, the Regulation 23A test refuses most of them, and the platforms' screen does not compare income with costs."

**Rewrite (01:66-67):** "...and screening BNPL requests with the Regulation 23A test lowers it by about as much as BNPL adds, because the test refuses the same households."

**Abstract:** add "as the screening rules imply" after "food and rent".

---

## Abstract and Data and Code (main.tex)

### HIGH

**A1. [clarity/logic, HIGH] main.tex:116**
> `Visibility, and screening without peer influence, leave slightly more households short of food and rent, and the runs do not record how much goes unpaid, so neither result shows whether households are better off.`

**Problem:** The previous sentence says visibility *raises* default. If it also leaves more households short of food and rent, households are worse off on both measures, so "neither result shows whether households are better off" is wrong for visibility. It holds only for screening, which lowers default but raises the food-and-rent shortfall. "Slightly" also stands where a number exists, and the comma placement leaves it unclear whether "without peer influence" applies to visibility too.

**Rewrite:** "Visibility also leaves more households short of food and rent. Screening without peer influence does the same while lowering default, and the runs do not record how much goes unpaid, so they cannot show whether screening leaves households better off."

### MED

**A2. [clarity, MED] main.tex:111**
> `The profile is an input and a calibration target, so it cannot validate the model, and we interpret differences between scenarios, which remain conditional on the assumptions the scenarios share.`

**Problem:** Two claims are joined by "and", so the second reads as a non sequitur. The real link is "therefore". "Scenarios" also stands in for "arms" here.

**Rewrite:** "The profile is an input and a calibration target, so it cannot validate the model. We therefore interpret differences between arms, and these remain conditional on the assumptions the arms share."

**A3. [clarity, MED] main.tex:113**
> `From a baseline in which 14.4\% of households enter default during the two-year run, adding \ac{BNPL} raises default by 1.0 percentage point, and the effect does not change detectably with peer influence over the range tested, although households borrow 2.4 times as much at its top.`

**Problem:** The sentence is 49 words with three claims, and "its top" could refer to "peer influence" or to "the range".

**Rewrite:** "In the baseline, 14.4% of households enter default during the two-year run. Adding BNPL raises this by 1.0 percentage point. The effect does not change detectably with peer influence, although at the largest value tested households borrow 2.4 times as much."

**A4. [clarity/terminology, MED] main.tex:112**
> `Many users owe several platforms at once, but default shows no detectable rise with the number of platforms.`

**Problem:** "Many" stands where a number exists (28% of ever-holders without peer influence, 70% at β = 0.3). "Users" is a term the body does not use (the body says "ever-holders").

**Rewrite:** "Between 28% and 70% of households that use BNPL owe two or more platforms at once, depending on peer influence, but default shows no detectable rise with the number of platforms."

**A5. [clarity, MED] main.tex:108**
> `Hires follow labour-force data and job losses offset them in expectation.`

**Problem:** A reader of the abstract cannot tell what this means or why it matters. It also needs a comma before "and" because it joins two clauses.

**Rewrite:** "Members lose and find jobs at rates that keep expected employment constant, with the hiring rate from labour-force data."

### LOW

**A6. [tautology/AI-tell, LOW] main.tex:107**
> `reportedly due from 2027.`

**Problem:** "Bureau reporting ... is reportedly due" repeats the root word and adds a hedge.

**Rewrite:** "Press reports expect BNPL to appear on bureau records from 2027."

**A7. [tautology, LOW] main.tex:114** (same line as X1)

**Problem:** "...and then fall more than 90 days behind on it" restates default. The informative part is that the default is on the BNPL itself rather than on traditional debt (0.94 of 1.07 points, Section 4.1).

**Rewrite:** "...and then default on the BNPL itself".

**A8. [terminology, LOW] main.tex:115-116**
> `The model has no credit score, so reporting acts through the lender's Regulation 23A test.`

**Problem:** The abstract uses "Bureau reporting", "reporting", "bureau visibility" and bare "Visibility" for the switch.

**Fix:** Keep "reporting" for the real-world arrangement and "bureau visibility" for the model switch: "The model has no credit score, so bureau visibility acts only through the lender's Regulation 23A test."

**A9. [clarity, LOW] main.tex:108**
> `apply a light screen and cannot see one another.`

**Rewrite:** "...cannot see one another's balances" (as at 01:51).

**A10. [clarity, LOW] main.tex:133**
> `The results are those of the commit tagged in the code release.`

**Rewrite:** "The results come from the commit tagged in the code release."

**Assessment, Abstract and Data and Code.** The abstract is dense but honest about what the calibration cannot show. Its last two sentences carry a logic slip (A1) and the framing problem in X1. Several sentences pack three claims each and should be split. The Data and Code statement is clean.

---

## Section 1: Introduction (01_introduction.tex)

### HIGH

**I1. [tautology, HIGH] 01:85-87 (RQ1)**
> `microdata reproduce the selected baseline arrears bands, and how does it perform`

**Problem:** RQ1's first half asks whether the model reproduces bands it starts from and is fitted to. Section 3.4 rightly calls that agreement "by construction", so the question as worded has a known answer. "Selected" is also unexplained, and it is the model run, not the population, that reproduces the bands. This is a sentence-level fix, not a restructure.

**Rewrite:** "How stable is the baseline's 2017 arrears profile, to which it is fitted, and how does the model perform against external comparisons not used in fitting or construction?"

### MED

**I2. [grammar/tense, MED] 01:16 and 01:19**
> `South African lenders did not see \ac{BNPL} obligations when they assessed affordability.`
> `\ac{BNPL} agreements were not displayed on consumer credit`

**Problem:** These describe a situation that still holds (records reach profiles only from 2027), but they are in the past tense. They sit next to present-tense sentences ("legal commentary takes the same view", "Reporting arrangements are changing").

**Rewrite:** "South African lenders do not yet see BNPL obligations when they assess affordability. ... BNPL agreements are not displayed on consumer credit profiles."

**I3. [terminology/ambiguity, MED] 01:26-29**
> `position that an agreement may become`

**Problem:** One sentence uses "agreement" for an accord among the NCR, SACRRA and the bureaus, and then for a BNPL contract. "Incidental credit" is also undefined jargon.

**Rewrite:** "...and report the NCR's position that a BNPL contract may become incidental credit, a category the Act regulates more lightly, once default charges are levied." Check that gloss of incidental credit before using it.

**I4. [clarity, MED] 01:57**
> `The experiments measure differences between arms of the model.`

**Problem:** "Arm" is used here for the first time and never defined, in this section or in Section 3.1. Arms belong to experiments, not to the model.

**Rewrite:** "The experiments measure differences between arms, runs of the model that differ in one setting."

**I5. [clarity, MED] 01:59-62**
> `The contribution is a household model in which lenders differ in what they`

**Problem:** The sentence is 45 words. The reader is likely to take "and a set of experiments" as part of the "so that" clause.

**Rewrite:** "The contribution has two parts: a household model in which lenders differ in what they observe, so that the reporting gap can be switched on and off, and experiments that identify the mechanisms and assumptions on which the effect of BNPL on default depends." Two sentences also work.

**I6. [clarity, MED] 01:95**
> `We measure distress mainly by default, in the two measures of`

**Problem:** "By default" reads first as the idiom meaning "normally". The phrase "by default, in the two measures of" is also awkward.

**Rewrite:** "Our main measure of distress is default, reported in the two ways set out in Section 3.1."

**I7. [clarity, MED] 01:97-99**
> `more than 90 days in arrears (the 90+ share), the household counterpart of the 2017 account figure above, and`

**Problem:** The appositive and the list run into each other, so the reader has to work out that "food and rent left unpaid" is the second item reported. "Credit-active" is used here before Section 2.3 defines it.

**Rewrite:** "We also report two other measures. The 90+ share is the share of credit-active households (those owing any balance or arrears) more than 90 days in arrears, the household counterpart of the 2017 account figure. Consumption distress is food and rent left unpaid."

**I8. [clarity, MED] 01:66**
> `food and rent. Bureau visibility raises default a little, and screening \ac{BNPL} requests with`

**Problem:** "A little" stands where the number exists (0.20 points at β = 0, per the abstract).

**Rewrite:** "Bureau visibility raises default by about 0.2 points..."

**I9. [clarity, MED] 01:125**
> `We do not count this result as evidence (Section~\ref{sec:data-validation}).`

**Problem:** The reader is not told why a study is reviewed only to be set aside.

**Rewrite:** "Section 3.5 uses this profile as Pattern 3 and explains why we do not count it as evidence."

**I10. [tautology, MED] 01:89 (RQ2)**
> `households owe several platforms at once, and how do enabling \ac{BNPL}, platform`

**Problem:** Sections 2.4 and 4.3 say that how often households owe several platforms is "set by the routing assumption", so this half of RQ2 asks what an assumption sets. "Peer adoption" here and "exposures" (L88) are also second terms for peer influence and balances.

**Rewrite:** "...how often do households owe several platforms at once under the model's routing rule, and how do enabling BNPL, platform count, access and peer influence affect default?"

### LOW

**I11. [grammar, LOW] 01:23**
> `to household indebtedness and notes that approval rests on less rigorous credit checks than`

**Problem:** The comparison mismatches checks with credit.

**Rewrite:** "...less rigorous credit checks than those for traditional unsecured credit."

**I12. [clarity, LOW] 01:31**
> `records are reportedly expected on consumer profiles from`

**Problem:** Two hedges are stacked.

**Rewrite:** "records are expected on consumer profiles from February 2027, according to press reports".

**I13. [grammar, LOW] 01:33 against 02:158**
> `The \ac{FINASA} reports one bureau's preliminary estimate`
> `reported by \ac{FINASA}` (02:158)

**Problem:** The article is used in one place and dropped in the other.

**Fix:** Use "the" in both.

**I14. [grammar, LOW] 01:119**
> `shortfall as a cash-flow failure in the same way, which is the logic of the residual-income`

**Problem:** "Which" has no clear antecedent.

**Rewrite:** "We also treat a shortfall as a cash-flow failure, the same logic as the residual-income test, but count default only once..."

**I15. [clarity, LOW] 01:137-138**
> `increase stress on traditional debt. We check the model against this through traditional`

**Problem:** Two "this"s in a row, the second pointing at a whole finding.

**Rewrite:** "Table 3.6 checks the model against this pattern through traditional arrears and interest."

**I16. [grammar, LOW] 01:165-166**
> `regularly pay at or near the contractual minimum.`

**Problem:** Accounts do not pay; their holders do.

**Rewrite:** "...find that the holders of 29% of United States credit-card accounts regularly pay at or near the contractual minimum."

**I17. [terminology, LOW] 01:185**
> `\ac{BNPL} sat outside Australia's National Credit Act.`

**Problem:** The South African NCA is the "National Credit Act" in this thesis, so the same name now covers two statutes. Australia's statute is the National Consumer Credit Protection Act; the reference checkers should confirm.

**Rewrite:** "...while BNPL sat outside Australia's consumer credit law."

**I18. [terminology, LOW] 01:127-128**
> `the pattern-oriented approach of`

**Problem:** Pattern-oriented modelling is its own approach, not part of the ODD protocol. 03:326 calls it "pattern-oriented modelling".

**Rewrite:** "Following Windrum, Fagiolo and Moneta and pattern-oriented modelling~\citep{grimm2020odd}, we distinguish...". Whether this citation is the right one is for the reference audit.

**I19. [grammar, LOW] 01:110**
> `inequality and consumption emulation, leading to debt-financed spending and eventually`

**Problem:** The participle dangles: it is the inequality, not the modelling, that leads to the spending.

**Rewrite:** "Cardaci models how rising inequality and consumption emulation lead to debt-financed spending and eventually a banking crisis."

**I20. [tautology, LOW] 01:41-45 against 01:192-197**

**Problem:** The gap is stated twice: "We found no South African study ... It is therefore not known how much..." and "None of the reviewed studies examines how these mechanisms interact in a South African household population...". This is noted only, since restructuring is on hold. When the supervisor's guide arrives, one of the two can go.

**Assessment, Introduction.** The background and literature are written in a plain, declarative voice that mostly meets the house standard. The defects are sentence-level: a past tense for a present state, "agreement" used in two senses, the undefined "arm", and the "by default" pun. The substantive problems are that RQ1 asks a question answered by construction (I1) and that the summary paragraph presents the mechanical concentration of the effect as a finding (X1).

---

## Section 2: The Model (02_model.tex)

No HIGH findings.

### MED

**M1. [clarity, MED] 02:150 and 02:153**
> `Both tests therefore count each live agreement's fortnightly instalment,`
> `of a one-off arrear. Traditional arrears enter neither test, which sees only scheduled`

**Problem:** The text has described one test (Regulation 23A) applied in two places: by the lender when visibility is on, and by mandatory screening. "Both tests" makes the reader look for a second test. "Neither test, which sees" also mixes singular and plural. "A one-off arrear" is not standard; "arrears" is plural-only in British usage.

**Rewrite:** "Wherever the test counts BNPL, under bureau visibility or mandatory screening, it counts each live agreement's fortnightly instalment, multiplied by 26/12, as a monthly obligation. ... which overstates the burden of a single missed instalment. The test never counts traditional arrears; it sees only scheduled traditional service."

**M2. [clarity, MED] 02:7, 02:79, 02:276 (row 12)**
> `while \ac{BNPL} platforms apply a lighter screen.`
> `applies an automated screen, and limits both individual orders and each`
> `Banked households only, with a light screen; defaulted households are refused.`

**Problem:** The platforms' "light", "lighter" or "automated" screen is a central contrast of the thesis, but no sentence says what it checks.

**Fix:** Add one sentence in Section 2.1 or 2.2: "The platforms' screen, which we call light, checks only that the household is banked, not in default, under the platform's fee cap and within its limit of λ times monthly income. It does not compare income with expenses." Then use "light screen" everywhere.

**M3. [terminology, MED] 02:308, 02:314, 03:67**
> `identify its strength, so both parameters are swept. The defaults are`
> `$\mathcal{N}(\mu_\theta, \sigma_\theta^2)$, with defaults $\mu_\theta=0.30$ and`
> `default parameters, four platforms and access for every banked household. We call a`

**Problem:** "Default" is the thesis's main outcome. Using it for parameter values creates real ambiguity, for example "Runs use the default parameters" in the inference paragraph.

**Rewrite:** "The standard values are q_base = 0.05 and β = 0"; "with standard values μθ = 0.30 and σθ = 0.20"; "Runs use the standard parameter values". The same applies elsewhere in the thesis.

**M4. [clarity/contradiction, MED] 02:268 (row 8)**
> `Behavioural parameters are common to all households; heterogeneity comes from the survey data. The repayment archetype is assigned at random.`

**Problem:** The second sentence contradicts the first: the archetype is behavioural heterogeneity that does not come from the survey.

**Rewrite:** "Behavioural parameters are common to all households. Apart from the repayment archetype, which is assigned at random, heterogeneity comes from the survey data."

**M5. [terminology, MED] 02:319 (and Table 2.2 row 13)**
> `\subsubsection*{Submodel 13: Stacking}`

**Problem:** "Stacking" and "stack" are used from here on (03:441 "70.6\% of ever-holders stack", Section 4.3) but never defined. Five other phrases name the same idea: "owing several platforms at once", "concurrent obligations", "simultaneous borrowing", "overlapping agreements" and "cross-platform stacking".

**Fix:** Define it in the first sentence of the subsection: "A household that owes more than one platform at once is said to stack." Then use "stack" and "owe several platforms at once" only.

**M6. [clarity, MED] 02:189-190**
> `agreement is as old as its oldest unpaid instalment. A household's arrears age is the largest`

**Problem:** This states the agreement's age, but what is meant is its arrears age.

**Rewrite:** "...so an agreement's arrears age is the age of its oldest unpaid instalment."

**M7. [clarity/logic, MED] 02:196-199**
> `arrears''~\citep{ncr_cbm_2017}, so a household two months behind that catches up in the third`

**Problem:** "So" draws the consequence from the match with the Credit Bureau Monitor, when it actually follows from the 98-day rule. "Catches up in the third" leaves the noun implied, and "past 90 days past due" (L196) repeats "past".

**Rewrite:** "...the first tick boundary beyond 90 days past due. This is close to the threshold at which the NCR's Credit Bureau Monitor classes a record as impaired, 'three or more payments or months in arrears'. Under this rule a household that falls two months behind and catches up in the third month never defaults."

**M8. [terminology, MED] 02:14-15**
> `enabled and no regulatory change the benchmark.`

**Problem:** "Baseline" (BNPL off) and "benchmark" (BNPL on, no regulatory change) are near-synonyms for two different runs. Table 3.2 adds "injection", and Section 4 compares "the baseline with BNPL enabled". A reader will mix them up.

**Fix:** Keep both terms, but restate the pair once where Section 5 first relies on "benchmark", or rename the second "the BNPL benchmark" throughout.

**M9. [terminology, MED] 02:190, 02:200, 02:264, 02:266, main.tex:110**

**Problem:** The unit of credit is called an "agreement" (BNPL contract, and at 02:190-191 traditional debt too), a "facility" (abstract L110, rows 6 and 7, L347), an "account" (02:200, "Its accounts are non-performing") and a "loan" (row 9). Traditional debt is one consolidated balance per household, so "its agreements" (02:191) suggests a structure the model does not have.

**Fix:** Use "agreement" for BNPL, "traditional balance" for traditional debt, "facility" only for "any facility" (either kind), and keep "account" for the CCMR's unit.

### LOW

**M10. [tautology, LOW] 02:254 (row 1)**
> `Separations and hires balance, so expected employment is constant.`

**Problem:** Balance and constancy are the same statement, and the separation rate is derived to make it true.

**Rewrite:** "The separation rate is set so that expected separations equal expected hires."

**M11. [terminology, LOW] 02:332**
> `agreements overlap and say nothing about why households use several providers. We found`

**Problem:** These are model households, so the word is "platforms". Keep "provider" for real firms. The same slip appears in the row label "Owing two or more providers at once" in `tab_bnpl_on_checks.tex:18`, where the model column counts platforms.

**M12. [clarity, LOW] 02:330**
> `The routing rule alone spreads overlapping agreements across platforms; no rule sets how`

**Problem:** "No rule sets how many platforms a household uses" contradicts "the routing rule alone spreads"; the routing rule does set it.

**Rewrite:** "No household chooses how many platforms to use; random routing alone spreads its overlapping agreements across platforms."

**M13. [clarity, LOW] 02:216**
> `alternatives add 25\% or one tick of committed expenditure.`

**Problem:** The sentence does not say what is added to.

**Rewrite:** "Two alternatives add 25% of the shortfall or one tick of committed expenditure to the request."

**M14. [clarity, LOW] 02:230**
> `The shortfall path reflects evidence`

**Problem:** "Shortfall path" becomes a key term in Section 4 but is never defined.

**Fix:** At 02:222 add: "We call BNPL used against a shortfall the shortfall path."

**M15. [clarity, LOW] 02:264 (row 6), also 03:291**
> `pays nothing again with a fixed probability, arrears persistence.`

**Problem:** "Pays nothing again" can be read as "never pays again".

**Rewrite:** "misses its payment again with a fixed probability (arrears persistence)."

**M16. [clarity, LOW] 02:226**
> `traditional lender for the rest, an assumption, and the lender grants or refuses that`

**Problem:** The appositive "an assumption" interrupts the sentence.

**Rewrite:** "We assume the household asks the traditional lender for the rest..."

**M17. [clarity, LOW] 02:127**
> `Boxes represent the five entity types.`

**Problem:** The figure has eight boxes, four of them platforms.

**Rewrite:** "Boxes represent the five entity types; each platform has its own box."

**M18. [grammar, LOW] 02:131**
> `and the scheduled service on its traditional debt, which the bureau records.`

**Problem:** "Which" could refer to the debt or to the service.

**Rewrite:** "...and the scheduled service on its traditional debt, as the bureau records it."

**M19. [terminology, LOW] 02:180, 02:344, 02:134, 02:51**

**Problem:** These four sentences introduce second terms for concepts that already have one:
- "essential living costs" (L180) means committed expenditure.
- "The credit gate reuses the" (L344, and row 9 "Credit gate") means the Regulation 23A test.
- "commitments" (L134) means obligations.
- "Rate and horizon pricing that balance" (L51) is unclear.

**Rewrite for L51:** "Rate and term used to amortise that balance". Replace the other three with the main term.

**M20. [clarity, LOW] 02:159**
> `discusses it as an extension.`

**Problem:** "It" is the omission, but the extension would be adding a score.

**Rewrite:** "...discusses adding a score as an extension."

**M21. [grammar, LOW] 02:10**
> `The experiment begins with a traditional-credit baseline calibrated to 2017`

**Problem:** The thesis runs many experiments, so the singular is wrong.

**Rewrite:** "The experiments begin with..."

**M22. [clarity, LOW] 02:188**
> `Arrears are aged by contractual delinquency.`

**Problem:** This is jargon, and "delinquency" appears nowhere else. The next sentence explains it anyway, so this one can go.

**M23. [acronym, LOW] 02:254, 02:260; 03:231**
> `(\acs{QLFS})` and `(\acs{IES})`

**Problem:** In Table 2.2, `\acs` prints QLFS and IES before they are expanded (the first `\ac` is in Section 3). APR appears only as `\acs{APR}` in the Table 3.3 header, so it is never expanded in the text.

**Fix:** Use `\ac` at the first use, or `\acl` in the Source column.

**Assessment, Model.** This is the cleanest of the three sections: present tense throughout, short sentences, and honest statements of what the stacking measure can and cannot show (02:322-336). The weaknesses are terms used before or without definition (light screen, stacking, shortfall path, arm) and "default" used for parameter values. The one passage a reader must read twice is "Both tests" (M1).

---

## Section 3: Calibration and Empirical Grounding (03_calibration.tex and the generated tables)

### HIGH

**C1. [contradiction within scope, HIGH] 03:427-429; tab_bnpl_on_checks.tex:16**
> `debt-to-income is highest in Q4, the shape of Pattern~3, but the shape appears only as Q1's debt`
> `is written off. At the start Q1's ratio is 0.81 against Q4's 1.19, and by the final tick it is`
> `Not counted: absent at the start; appears as Q1's debt falls`

**Problem:** The text's own numbers show the ratio already highest in Q4 at the start (1.19 against 0.81), and the table's criterion is "Peak in Q2--Q4". So the pattern is present at the start, and "absent at the start" and "appears only as Q1's debt is written off" contradict the figures beside them. The source comment gives start values 0.81, 0.55, 0.78, 1.19, 0.71. The real reason not to count it seems to be that the start profile is not a middle-income hump, since Q1 is second highest, and that the final shape is driven by write-offs.

**Rewrite:** "At the start the ratio is already highest in Q4 (1.19), but Q1 is second (0.81), so the profile is not a middle-income hump. By the final tick Q1's ratio is 0.08, because Q1 has the highest default rate and its debt is written off. We do not count Pattern 3 as evidence."

**Table result cell:** "Not counted: Q1 second-highest at start; final shape set by Q1 write-offs".

**C2. [contradiction, HIGH] 03:218-219**
> `rates, which cannot exceed the ceilings, so payments are overstated. The product allocation,`
> `horizons and ceiling err in unknown directions.`

**Problem:** Two different ceilings, the statutory rate ceiling and the Regulation 23A payment cap, appear in adjacent sentences. The first is said to overstate payments and the second "errs in unknown directions", which reads as a contradiction. "Are overstated" should also be "at or above the true payments", because realised rates can equal the ceiling.

**Rewrite:** "No 2017 source we consulted, the CCMR included, reports realised rates. Realised rates cannot exceed the statutory ceilings we use, so the constructed payments are at or above the true ones. The product allocation, the horizons and the Regulation 23A cap on the payment err in unknown directions."

**C3. [terminology/contradiction, HIGH] 03:11 against 02:260, 02:264, 03:259**
> `every swept input is also assumed`

**Problem:** Table 2.2 sweeps κ, which Table 3.1 classes as Derived (IES), from 0.07 to 0.28. It sweeps the minimum-payer share, classed as Imported, from 0.20 to 0.40, and k = 7 ticks. So "swept" means two things: a provenance class (no source) and an action (varied in the sensitivity analysis). The note's rule is false as written.

**Rewrite of the note:** "Swept: no source fixes the value, so a range is tested. Some sourced inputs (κ, the minimum-payer share, the default threshold) are also varied in the sensitivity analysis; they keep their sourced class here." Table 2.2's "swept" can then mean "varied".

### MED

**C4. [tautology, MED] 03:147-148**
> `reuse. National imputed rates differ from their \ac{FinScope} targets by at most 1.8`

**Problem:** Donors are drawn within cells in proportion to weight, so close agreement is expected by construction. Appendix E's table note says so; this sentence does not.

**Rewrite:** "...by at most 1.8 percentage points, and by at most 2.3 points within any quintile. Close agreement is expected from the design of the match, so this checks the implementation."

**C5. [tautology/AI-tell, MED] 03:299; tab_arrears_fit.tex:7, 22**
> `What the run can show is stability: the 90+ share at the final tick, which was not a target, is 13.84\%, so after two`

**Problem:** The fit targets the average over ticks 13 to 52, which includes the final tick, so the final-tick share is not independent of the target. It shows the absence of a strong trend and nothing more. "Not targeted" overstates how separate it is. The colon-then-reveal construction is also one of the listed tells.

**Rewrite:** "The run can show stability. The 90+ share at the final tick is 13.84%. The fit targets the post-burn-in average, so this is not an independent check, but it shows the profile has not drifted after two years."

**C6. [number conflict within scope, MED] 03:299 against 03:351**
> `is 13.84\%, so after two` (03:299)
> `The third is arrears at the final tick: 14.16\% of credit-active households are 91 or more days` (03:351)

**Problem:** The same quantity (BNPL off, final-tick 90+ share of credit-active households) is reported as 13.84% and 14.16% about 50 lines apart. They come from different seed blocks (1,000-1,019 and 10,000-10,019), but only the second says so in the text.

**Fix:** Add "on the calibration seeds 1,000-1,019" at L299, or report both blocks.

**C7. [tautology, MED] 03:423-426**
> `Households pay \ac{BNPL} instalments before traditional`

**Problem:** The rise in traditional arrears follows directly from the assumed payment order. Here the explanation comes after the sentence about interest, so it reads as a separate remark, and Pattern 1 is still framed as "holds". The design-dependence noted at 03:330-332 is a separate caveat.

**Rewrite:** "Traditional arrears rise at both values of β, as Pattern 1 expects, but this follows from the assumed payment order: households pay BNPL instalments first, so any BNPL obligation leaves less cash for traditional debt. Traditional interest does not change detectably; it tracks the size of the book more than servicing stress."

**C8. [terminology, MED] 03:403**
> `The 62 members who hold traditional debt have the least income left after food, rent and debt`

**Problem:** "Members" means household members (persons) at 03:265 and 03:270 and in row 1. Here it means agents in the short group.

**Rewrite:** "The 62 agents in this group who hold traditional debt..."

**C9. [clarity/numbers, MED] 03:406-409**
> `with \ac{BNPL} at $\beta=0$, 85\% do. The group therefore accounts for about 0.9 of the`
> `1.08-point effect of Table~\ref{tab:baseline-arms}. Among the other households the pooled`

**Problem:** The group's share is taken from the single-block 1.08, and the rest from the pooled estimate (+0.11). A reader who adds 0.9 and 0.11 gets 1.01, not 1.08. "About 0.9 of the" also leaves out the unit, and "which is." at L409 is elliptical.

**Rewrite:** "The group therefore accounts for about 0.9 points of the 1.08-point effect in Table 4.1. Among the other households, pooled across seed blocks, the effect is +0.11 ± 0.07 points at β = 0, which is not detectable, and +0.18 ± 0.08 at β = 0.3, which is."

**C10. [grammar, MED] 03:43-44**
> `\emph{Default during the run} is the number of households that`

**Problem:** The definition says "number", but the value given is a percentage. "The number of households ... over all 5,000 households" is a garbled ratio.

**Rewrite:** "Default during the run is the share of all 5,000 households that enter default after the start."

**C11. [clarity, MED] 03:47-48**
> `share ever in default, and tables and figures report it unless they say otherwise.`

**Problem:** "This" and "it" could refer to either of the two measures just defined. This is the sentence that tells the reader which measure every table uses, so it must be unambiguous.

**Rewrite:** "Default is permanent, so default including the starting stock is also the share ever in default. Tables and figures report this measure unless they say otherwise."

**C12. [clarity, MED] 03:55-58**
> `Table~\ref{tab:experiments} lists the experiments. Each arm has twenty replicates, except the`

**Problem:** Three exceptions, each with its own "which" clause, sit in one 45-word sentence, and the reader has to parse the list twice.

**Rewrite:** "Each arm has twenty replicates, with three exceptions. The four scenario arms have one hundred, because twenty cannot resolve the differences between them. The β sweep has 250, and the variance decomposition has eight per design point."

**C13. [correctness, MED] 03:71**
> `We judge many contrasts this way, so about one in twenty would pass`

**Problem:** The 5% rate applies to contrasts with no true difference, not to all contrasts.

**Rewrite:** "We judge many contrasts this way, and about one in twenty contrasts with no true difference would pass by chance, so a single detectable difference carries less weight than one that repeats across seed blocks."

**C14. [clarity/logic, MED] 03:271-274**
> `out of work at the final tick. Employment is constant in total but not within quintiles, because`

**Problem:** The second "because" (hire pay versus mean wage) explains why income drifts, not why employment shifts between quintiles. The sentence is 46 words.

**Rewrite:** "Employment is constant in total but not within quintiles, because jobseekers are concentrated in the lower quintiles. Income drifts as well, because a hire brings the median pay of employed adults in its quintile, which is above the mean wage per earner in Q1 and Q2 and below it in Q3 to Q5."

**C15. [clarity, MED] 03:289-291**
> `parameters are fitted jointly to the five arrears bands: payment friction, the chance of`

**Problem:** Two appositives inside a list read as four items.

**Rewrite:** "Third, two parameters are fitted jointly to the five arrears bands. Payment friction is the chance of skipping an affordable traditional instalment. Arrears persistence is the chance that a household already behind misses its payment again."

**C16. [terminology/consistency, MED] 03:370 against 03:453**
> `Debt service is the one clear failure.`
> `The serious failures concern how the model generates distress: an arrears profile set by its`

**Problem:** "The one clear failure" is followed a page later by a list of "serious failures". That list includes items that are limitations, not failures: an arrears profile set by its start and two fitted parameters, which the text earlier treats as design, and "a default rate with no external counterpart", which is a data gap.

**Rewrite (L453):** "The main limitations concern how the model generates distress: ..." Move "a default rate with no external counterpart" to the next sentence, which lists data gaps.

**C17. [clarity, MED] 03:439**
> `volume is below the provider's range and the mean purchase is 33\% below the provider-based`

**Problem:** "The provider" appears with no antecedent in the text, and the reader learns only from the citation three lines later which firm it is.

**Fix:** Name it at first mention, for example "below the range implied by [provider]'s disclosures~\citep{weaver2025iar}".

**C18. [grammar, MED] 03:347**
> `have defaulted, 13.4 points of them placed in default at the start, against the 39.3\% of credit-active consumers with`

**Problem:** "13.4 points of them" mixes a rate unit with a count pronoun.

**Rewrite:** "By the final tick 43.7% of the households that held credit at any tick have defaulted, 13.4 points of it from households placed in default at the start. This compares with 39.3% of credit-active consumers..."

**C19. [clarity, MED] 03:48**
> `Within a seed block the`

**Problem:** "Seed block" is used here before it is explained (L59 and the Table 3.2 note). "The starting stock is the same households" is also awkward.

**Rewrite:** "Within a seed block, the set of seeds an experiment's arms share (Table 3.2), the starting stock consists of the same households in every arm..."

**C20. [tautology/repetition, MED] 03:139-141 against 03:197**
> `per-capita income quintile and province. Each \ac{NIDS} household draws one donor from its`
> `\tabnote{(a) Both surveys are divided into 45 cells by per-capita income quintile and province. (b) Each \ac{NIDS} household draws one \ac{FinScope} donor from its cell, with probability proportional to the donor's survey weight (circle area), and copies all six flags from it.`

**Problem:** The figure note repeats the text almost word for word.

**Fix:** Cut the note to the panel key ("(a) The same 45 cells in both surveys. (b) Circle area is survey weight. (c) The alternative not used..."), or shorten the text to "Figure 3.1 shows the matching" plus the fallback sentence.

### LOW

**C21. [contradiction, LOW] 03:26**
> `Varied in one arm: four platforms and random routing`

**Problem:** The number of platforms is varied across a whole experiment (1-6 platforms, Table 3.2), not in one arm.

**Rewrite:** "Varied in separate experiments: four platforms (1-6) and random routing (loyal routing)."

**C22. [clarity, LOW] 03:11**
> `In the register (Appendix~\ref{app:register}), sourced covers Observed, Constructed and Imported.`

**Problem:** "Sourced" is a class label not in this table, and Derived is not placed. The note also defines three of the seven classes and leaves Observed, Constructed, Derived and Fitted to inference.

**Fix:** Add "Derived" to the list or say where it falls.

**C23. [grammar, LOW] 03:331**
> `because want-driven borrowing was added partly when shortfall-only borrowing failed to`

**Problem:** "Partly when" is unclear; the meaning is "partly because".

**Rewrite:** "...because want-driven borrowing was added partly because shortfall-only borrowing failed to reproduce it." The sentence is also 51 words, so end it after "interest" and start a new one with "It is not independent of the design".

**C24. [number style, LOW] 03:55, 03:69, 03:71**
> `twenty replicates`; `with one hundred replicates and 0.04 with 250`

**Problem:** Words and digits are mixed in one sentence ("one hundred" beside "250"), and the same paragraphs use digits for 12, 40 and 52 ticks.

**Fix:** Pick one rule (for example digits for all counts of 10 or more: 20, 100, 250) and apply it.

**C25. [clarity, LOW] tab_arrears_fit.tex:7**
> `(those owing traditional or \ac{BNPL} debt or arrears), by the age of the oldest unpaid instalment, \ac{BNPL} disabled`

**Problem:** BNPL is disabled in this run, so "or BNPL debt" is redundant here and may puzzle a reader.

**C26. [consistency, LOW] 03:284**
> `bands. Those placed at 91 days or more, 6.4\% of all households, start in default. No source`

**Problem:** The run's default rule is 98 days (seven ticks). A reader will ask whether households placed at 91-97 days are in default by the start rule but not by the run rule.

**Fix:** One clause saying that the start treats the whole 91+ band as in default.

**C27. [clarity, LOW] 03:342**
> `Three comparisons place the level`

**Problem:** The first comparison "checks consistency only", so it does not place the level.

**Rewrite:** "Three comparisons bear on the level."

**C28. [clarity, LOW] 03:266**
> `are strictly unemployed.`

**Problem:** This is jargon.

**Rewrite:** "...are unemployed under the strict (searching) definition."

**C29. [clarity, LOW] 03:122-123**
> `Asset, debt and rent fields are`

**Problem:** "Recorded only for holders" does not fit rent.

**Rewrite:** "...recorded only for households that hold the asset or debt or pay rent".

**C30. [grammar, LOW] 03:473-474**
> `which supports the inputs` / `which shows`

**Problem:** Two trailing "which" clauses, each pointing back at a whole clause.

**Rewrite:** "...the order of magnitude of household debt, so the inputs are sound on these measures. With two parameters fitted to its five bands, the baseline holds the 2017 arrears profile as a share for two years while the credit-active book halves; this is stability, not validation."

**C31. [repetition, LOW] 03:298, 03:319, 03:332, 03:345, tab_arrears_fit.tex:7**

**Problem:** "By construction / not evidence / consistency check only" appears five times in about 50 lines. Each is accurate, but L332 (Pattern 2) and L345 could shrink to a clause once L298 and L319 have made the point.

**C32. [style, LOW] throughout**

**Problem:** "2017 Rands" is capitalised and plural. South African and SARB usage is "2017 rand" (lower case, invariant plural). It is used consistently, so change it only if the supervisor's guide asks.

**Assessment, Calibration.** This is the most careful section about what is and is not evidence: the four-way separation at 03:317-323 is exactly right, and the book-halving paragraph is clear and honest. It also has the most defects. Two adjacent sentences contradict each other (C1, C2), the provenance note's "every swept input is also assumed" is false as written (C3), and two by-construction results are presented without saying so (C4, C5). The rest is dense inference prose that would gain from splitting long sentences and pinning down "this", "it" and "members".

---

## Glossary of key terms as used, with conflicts

| Concept | Main term (keep) | Second terms found | Where | Recommendation |
|---|---|---|---|---|
| Simulated unit | household | agent (Table 2.1, 03:203, 03:394-396); member, used for persons (row 1, 03:265) and for agents in the short group (03:403); users (main.tex:112) | as listed | "household" in prose; "agent" only when contrasting with the NIDS record; never "member" for an agent |
| Real-world people | consumer, borrower, user | none | Section 1, Table 1.1 | fine for cited studies |
| BNPL firm in the model | platform | provider (02:332; tab_bnpl_on_checks:18 row label) | as listed | "platform" in the model, "provider" for real firms |
| Traditional firm | traditional lender | "lender classes" (Table 1.1) | 01:230 | fine |
| Unit of credit | agreement (BNPL) | facility (main.tex:110, rows 6 and 7, 02:347), account (02:200), loan (row 9), "its agreements" for traditional debt (02:191) | as listed | agreement = BNPL; traditional balance; facility = either; account = CCMR only |
| The word "agreement" used for other things | | an accord among regulators (01:26); a match between figures (03:298, 03:438) | | change 01:26 (I3); the match sense is tolerable |
| Default | default (98 days, permanent) | impaired (Credit Bureau Monitor only), non-performing (accounts), delinquency (02:188, once); "default(s)" for parameter values (02:308, 02:314, 03:67) | | drop "delinquency"; never "default" for parameter values (M3) |
| Two default measures | default during the run; default including the starting stock | "share ever in default" (= the second) | 03:43-48 | fine once C11 is fixed |
| Distress | credit distress (RQ), distress | consumption distress = food and rent left unpaid; "short of food and rent", "food and rent shortfall", "food and rent left unpaid" | 01:99, 02:206, 03:359 | "consumption distress" for the measure, "short of food and rent" for the state; note that "shortfall" alone means the cash shortfall that triggers borrowing |
| Committed spending | committed expenditure (= food and rent) | essential living costs (02:180), incompressible food and rent costs (Table 2.1) | | "committed expenditure" |
| Time step | tick (= 14 days) | fortnight, fortnightly for conversions only | | consistent; no "period" |
| Peer channel | peer influence | peer adoption (RQ2 01:90, 02:164, Table 2.1), social approval (02:306), peer approval (Table 1.1) | | "peer influence"; "approval" only when describing Ackert et al. |
| 23A test | Regulation 23A test | residual-income test (01:119, 01:186, 02:6), credit gate (row 9, 02:344), residual-income ceiling (03:214) | | "Regulation 23A test"; "residual-income" as a gloss once |
| Platform check | light screen | lighter screen (02:7), automated screen (02:79); never defined | | define once (M2) |
| Reporting switch | bureau visibility | reporting (main.tex:115), Visibility (main.tex:116) | | "reporting" for the real arrangement, "bureau visibility" for the switch |
| Screening switch | mandatory screening (02:143) | affordability screening (main.tex:105, 01:55, main RQ), mandatory affordability screening (RQ3), screening | | pick one and define it once; "screening" alone is fine after that |
| Run configurations | arm | experiment, run, scenario (the four visibility-by-screening arms), lever (cooling-off, platform cap), switch; "seed block" | 01:57, 03:48, 03:55, 03:99, row 15 | define "arm" and "seed block" at first use (I4, C19); row 15 "Scenario switches" also lists the levers |
| Reference runs | baseline (BNPL off); benchmark (BNPL on, no regulatory change); control (β = 0) | injection (Table 3.2), enable, add | 02:14, 03:90 | keep, but restate the baseline/benchmark distinction where Section 5 relies on it (M8) |
| Owing several platforms | stack, stacking | owing several platforms at once, concurrent obligations, simultaneous borrowing, overlapping agreements | 01:22, Table 1.1, 02:330 | define "stack" once (M5) |
| BNPL holdings | balance, obligations | exposure(s) (02:13, 02:80, 02:325, RQ2), commitments (02:134) | | "balance" or "obligations"; "exposure" only for a platform's own risk |
| Ever-holder | ever-holder | adopter, user | 03:436 on | defined implicitly by "ever" at 03:41; fine |

---

## Summary by severity

- **HIGH (6):** X1 (concentration and screening results follow from the rules), A1 (abstract's last sentence is illogical for visibility), I1 (RQ1 asks about calibration targets), C1 (Pattern 3 "absent at the start" against Q4 1.19 > Q1 0.81), C2 (rate-ceiling sentences contradict), C3 ("every swept input is also assumed" is false).
- **MED (39):** A2-A5, I2-I10, M1-M9, C4-C20.
- **LOW (41):** A6-A10, I11-I20, M10-M23, C21-C32; polish only.
