# Language and simplicity edit (review 2026-10-07)

Scope: abstract (main.tex) and chapters 01 to 06. Appendices not reviewed. Line numbers refer to the files as read on 2026-10-07. All suggested revisions keep numbers, \cite, \ref, \label, \ac{} and maths unchanged. Items marked **FLAG** need the author's knowledge of the experiment before rewriting.

Approximate prose word counts (excluding tables, figure code and table notes): ch1 ~1,320; ch2 ~2,530; ch3 ~2,770; ch4 ~2,080; ch5 ~1,090; ch6 ~660. The biggest savings are in removing results repeated across sections 3.5, 4.2, 4.6, 5 and 6 (see Part A).

---

## Part A. Recurring patterns (thesis-wide)

1. **Repeated results across sections.** The same findings are restated, often with the same numbers, three or four times.
   - Stacking shares 52.0 / 85.1 / 36.6 / 22.0 %, with the seed-block note (52.6 / 85.2 %): abstract L88, 04:84-95, 04:257-263, 06:15. **4 times.** The answer to RQ2 (04:257-267) repeats 04:84-95 almost clause for clause.
   - Pattern 1 interest result explained by the smaller traditional book: 03:470-477 (said twice inside one paragraph), then 04:59-64. **3 times.**
   - RQ1 list of misses (intermediate bands, servicing share, purchase size and volume, Pattern 3, Pattern 1 interest): 03:489-492 and 06:11-12. **2 times.**
   - Reason for 100 replications in the scenario arms: 03:41-43 and 05:19. **2 times.**
   - Submodel 5 lender choice (BNPL first, kappa cap, quarter paid at checkout, traditional lender asked for the rest, "assumption"): table row 02:237, prose 02:274-283, and again 02:285-291. Submodel 13 routing: table row 02:253 and prose 02:327-333. The table note says these submodels "are elaborated in the text", so the table rows can be cut to one line each.

2. **Repeated caveats.**
   - beta = 1 is illustrative / stacks more than the CFPB evidence / beta = 0 is the better guide: 04:15-16, 04:35-40, 04:264-265, 06:18. **4 times.** Say it fully once (04:35-40) and refer back elsewhere.
   - The model has no credit score / scoring channel excluded: abstract L90, 01:39-40, 02:155-160, 05:14, 06:35, 06:41. **6 times.** Keep 02:155-160 and the future-work item; cut to a clause elsewhere.
   - "Does not estimate the historical effect / not a forecast of the reporting arrangements": 01:57-60, 05:49, 06:8. **3 times**, 06:8 nearly verbatim from 01:59-60.
   - Account versus household unit mismatch: 03:299 (table note), 03:333-338, 04:76 (figure note), 06:33. **4 times.**
   - Aggregates do not show that the same households default ("ecological" caveat): 04:46-48, 05:45, 05:61. **3 times.**
   - Statutory ceilings used as proxies for product rates: 01:170-171, 03:217-222, 03:228 (table note). **3 times.**

3. **Semicolon chains.** About 47 semicolons in running prose (ch1 2, ch2 11, ch3 15, ch4 9, ch5 5, ch6 5), plus many more in tables and notes. Most join a result to a qualification ("...; default does not", "...; the scoring channel is outside the model"). Many would read better as two sentences.

4. **Parenthetical cross-references.** About 100 parentheses in prose, roughly 72 of them "(Section~...)", "(Table~...)" etc. Several sentences carry two or three (e.g. 04:84-87, 04:93-94, 06:15). Keep one per sentence where possible; move the rest to the end of the paragraph.

5. **", which is not detectable" tag-ons.** 04:124, 04:138, 04:140, 04:240, 05:63 and similar. The result is reported, then negated in a trailing clause. Claim first instead: "Default does not change detectably (+0.14 ± 0.11 points)."

6. **Passive "was located" / "no ... located".** 02:235, 02:287, 02:291, 02:339, 03:264, 03:271, plus "No study we found" 02:270. **7 variants** of one idea. Pick one form ("we found no ...") and use it throughout.

7. **Inconsistent terms for the same thing** (house style asks for one term each).
   - Loyal routing: "loyal-routing arm" (02:253), "already owed first" (02:253), "the opposite rule" (02:340), "tries the platforms it already owes first" (02:341), "returns to a platform it already owes" (04:90), "return to platforms they owe" (04:242), "return to platforms they already owe" (04:261, 06:15). Define "loyal routing" once in 02:340 and use it everywhere; likewise "random routing".
   - Screening: "mandatory affordability screening" (01:82, 02:257, 05:15), "mandatory screening" (01:179, 05:30), "affordability screening" (01:55, 01:70, abstract L92), "the screening arm" (02:150), "screening" (ch5 throughout). Define "mandatory screening" once and use it.
   - Scenario arms: "three scenarios" and "a fourth arm" (05:11), "these four arms" (05:19), "scenario arms" (03:41), "three scenarios" (05:28 caption). Choose "the four scenario arms" or "the benchmark and three scenario arms".
   - "Invisibility" / "visibility gap" (04:107, 05:12, 06:16, 06:29): an abstract noun for "platforms cannot see one another's balances". Fine as a term if defined once in ch2.

8. **Numbers restated from tables.** 03:157-159 and 03:195-196 (Gini 0.6514 to 0.6668, also in figure note and Table E), 03:286-289 (13.93 % and 14.48 %, in Table arrears-fit), 03:457-462 (all four purchase and volume figures, in tab:bnpl-on-checks), 04:21-23, 04:84-92. Keep the headline number and the conclusion; let the table carry the rest.

9. **Signposting openers.** 02:10-16, 03:4-6, 04:4, 05:10, 05:18. "This section answers RQx" is useful; the roadmap sentences after it are not.

10. **Style rule checks.** No em dashes found. No "notably/crucially/importantly". "rather than" appears 3 times (03:299, 03:361, 03:474; 03:474 is the formulaic contrast). "robust" appears only in "robustness arm/analysis", which is a technical term; acceptable but consider "sensitivity arm" for consistency with 04:184-185, which already says "sensitivity arms".

---

## Part B. Worst passages, rewritten in full

Priority order: what a first-time reader would struggle with most.

### B1. 03_calibration.tex:36-50 (Simulation Parameters). Seed and replication bookkeeping in one 15-line paragraph.

ORIGINAL:
"Each run follows 5{,}000 households for 52 fortnightly ticks, two years. Arrears, savings and volume measures exclude a 12-tick burn-in; default is counted from the first tick (Section~\ref{sec:sequence}). Each configuration has twenty replications, using seeds $s_0+i$ with a fixed starting seed for each group of arms; the variance decomposition of Section~\ref{sec:results-robustness} has two per design point. The four scenario arms of Section~\ref{sec:scenarios} have one hundred, because the differences between them are smaller than twenty replications resolve. Arms within a group share seeds and population size, and we difference them seed by seed; because arms diverge once their random draws differ, this pairing reduces the standard error little. The scenario arms, the cap arms, the threshold-mean arms and each group of sensitivity arms have their own seed blocks, given in the table notes, and we treat differences across blocks or population sizes as independent. Thresholds use a separate random stream, so control arms reproduce exactly across threshold dispersion. Reported dispersion is simulation variance only and excludes uncertainty in the data and assumptions."

REVISED:
"Each run follows 5{,}000 households for 52 fortnightly ticks (two years). Arrears, savings and volume measures exclude a 12-tick burn-in; default is counted from the first tick (Section~\ref{sec:sequence}).

Each configuration has twenty replications. The exceptions are the four scenario arms of Section~\ref{sec:scenarios}, which have one hundred because twenty cannot resolve the differences between them, and the variance decomposition of Section~\ref{sec:results-robustness}, which has two per design point. Replication $i$ uses seed $s_0+i$, with one starting seed $s_0$ for each group of arms. Arms in a group share seeds and population size, so we difference them seed by seed, although this pairing reduces the standard error little because arms diverge once their random draws differ. The scenario arms, the cap arms, the threshold-mean arms and each group of sensitivity arms have their own seed blocks, given in the table notes; we treat differences across blocks or population sizes as independent. Thresholds use a separate random stream, so control arms reproduce exactly across threshold dispersion. Reported dispersion is simulation variance only and excludes uncertainty in the data and assumptions."

Reason: separates horizon from replication design; puts the rule before the exceptions; removes "smaller than twenty replications resolve".

### B2. 04_results.tex:4-16 (opening statistical conventions).

ORIGINAL:
"This section answers RQ2. Except in the Sobol design, every arm in this section has twenty replications at the income-shock probability and payment friction fitted in Section~\ref{sec:calibration}; no \ac{BNPL}-side parameter is re-tuned. Differences in the text carry one standard error, paired by seed where the two arms share seeds, and we describe a difference as detectable only when it exceeds two. The standard error of a difference in population default is about 0.1 percentage points, so a difference must exceed about 0.2 points to count as detectable, and a true change of that size would be missed about half the time. This section judges many contrasts at the two-standard-error threshold, so about one in twenty would exceed it by chance alone; an isolated detectable difference therefore carries less weight than an effect that repeats across seed blocks and settings. Figure error bars are 95\% confidence intervals. Table notes give denominators, seeds and measurement periods."

REVISED:
"This section answers RQ2. Except in the Sobol design, every arm has twenty replications at the income-shock probability and payment friction fitted in Section~\ref{sec:calibration}; no \ac{BNPL}-side parameter is re-tuned.

Differences carry one standard error, paired by seed where the two arms share seeds. We call a difference detectable when it exceeds two standard errors. For population default the standard error of a difference is about 0.1 percentage points, so a detectable difference must exceed about 0.2 points, and a true change of that size would be missed about half the time. We judge many contrasts this way, so about one in twenty would pass by chance; an isolated detectable difference therefore carries less weight than one that repeats across seed blocks and settings. Figure error bars are 95\% confidence intervals, and table notes give denominators, seeds and measurement periods."

Reason: "exceeds two" (two what?) is unclear on first reading; shorter sentences.

### B3. 03_calibration.tex:466-484 (Pattern 1, 3 and 4 results). One paragraph covers three patterns, and the interest explanation is given twice.

ORIGINAL (L466-477):
"Pattern~1 holds on the arrears measure and fails on the interest measure. Enabling \ac{BNPL} raises the traditional arrears rate by $0.23 \pm 0.07$ points at $\beta=0$ and $0.57 \pm 0.07$ at $\beta=1$. The interest charged on traditional debt falls by $1.5 \pm 0.4$\% at $\beta=0$, which the condition in Table~\ref{tab:patterns} counts as falsifying, and does not change detectably at $\beta=1$. The fall reflects a smaller traditional book (Section~\ref{sec:results-injection}), so this measure tracks the debt stock more than servicing stress. We record the failure as specified rather than amend the condition after the result. Aggregate interest falls whenever the book shrinks, so it was a poor proxy for servicing stress; the arrears measure tests the same mechanism and rises. On that reading, reached after the result, the lender-choice hierarchy stands and the interest condition was mis-specified."

REVISED:
"Pattern~1 holds on the arrears measure and fails on the interest measure. Enabling \ac{BNPL} raises the traditional arrears rate by $0.23 \pm 0.07$ points at $\beta=0$ and $0.57 \pm 0.07$ at $\beta=1$. The interest charged on traditional debt falls by $1.5 \pm 0.4$\% at $\beta=0$, which the condition in Table~\ref{tab:patterns} counts as falsifying, and does not change detectably at $\beta=1$. We record this as a failure, as specified. The fall reflects a smaller traditional book (Section~\ref{sec:results-injection}): aggregate interest falls whenever the book shrinks, so it tracks the debt stock more than servicing stress. On this reading, reached after the result, the interest condition was mis-specified and the lender-choice hierarchy stands, since the arrears measure tests the same mechanism and rises."

Then start a new paragraph at "Pattern~3 is not reproduced: ..." (L478). Reason: removes the duplicated explanation and the "rather than" contrast; one pattern per paragraph.

Follow-on: 04:59-64 can then shrink to one sentence: "This smaller book explains why the interest measure of Pattern~1 falls (Section~\ref{sec:data-validation})." Whether to keep the deHaan comparability sentence (04:62-64) is the author's call; it is the only new point there.

### B4. 04_results.tex:84-95 (stacking paragraph). Thirteen lines, two seed blocks, a probability aside and the routing robustness result in one block.

REVISED (split in two):
"Households come to owe several platforms at once, more so with more platforms and, under random routing, with peer influence (Table~\ref{tab:stacking}; Figure~\ref{fig:stacking}). With four platforms, 52.0\% of final-tick holders have balances on two or more platforms at $\beta=0$, and 85.1\% at $\beta=1$ (Table~\ref{tab:baseline-arms}). These shares follow from random routing (Section~\ref{sec:stacking}), under which a second request reaches a different platform first with probability $3/4$ with four platforms and $5/6$ with six.

Under loyal routing, in which a household returns to a platform it already owes and moves on only when its limit binds, the shares fall to 36.6\% at $\beta=0$ and 22.0\% at $\beta=1$, against 52.6\% and 85.2\% under random routing on the same seeds. The share of ever-holders who stacked at $\beta=1$ falls from 98.6\% to 51.4\%, nearer the \ac{CFPB}'s 32 and 33\%. Default does not change detectably: $-0.07 \pm 0.07$ points at $\beta=0$ and $+0.02 \pm 0.13$ at $\beta=1$ (seeds of Table~\ref{tab:effect}). How often households owe several platforms depends on how they choose among platforms; default does not."

Reason: introduces the term "loyal routing"; claim first for the default result.

### B5. 04_results.tex:257-267 (Answer to RQ2). Repeats B4 nearly word for word.

REVISED:
"Households come to owe several platforms at once when platforms cannot observe one another, more so with more platforms and, under random routing, with peer influence. With four platforms, 52.0\% of final-tick holders owe two or more at $\beta=0$ and 85.1\% at $\beta=1$ under random routing, and 36.6\% and 22.0\% under loyal routing, each on its own seed block (Section~\ref{sec:results-stacking}). These shares depend on the routing rule; default does not. Enabling \ac{BNPL} raises default by $0.12 \pm 0.05$ points without peer influence, a result sensitive to the borrowing rules, and by $0.60 \pm 0.07$ at $\beta=1$, where stacking far exceeds the \ac{CFPB} evidence. Default does not respond detectably to platform count. It rises with peer influence and, where peer influence is present, with access: the arms in which households borrow most."

Reason: drops the restated 52.6 / 85.2 % (already in Section 4.2) and the clause-within-clause "when households choose platforms at random".

### B6. 05_policy.tex:10-16 (scenario set-up). Appositive chain in L11 is the hardest sentence in the chapter.

ORIGINAL (L11): "We compare three scenarios, the benchmark and the two switches taken alone, and a fourth arm, both switches together, which tests whether either switch changes the effect of the other."

REVISED (L10-16 as one paragraph):
"This section answers RQ3. We compare the benchmark with three arms: bureau visibility alone, mandatory screening alone, and both switches together; the combined arm tests whether either switch changes the effect of the other. The benchmark is the pre-2026 position, in which \ac{BNPL} obligations are invisible to the bureau and requests pass only a light screen. That light screen is a modelling assumption: whether an agreement that levies late fees is incidental credit, and which provisions would then apply, is a legal question that the scenarios do not settle (Section~\ref{sec:background}). Under bureau visibility ($\mathbb{1}^{\text{bur}}$), \ac{BNPL} obligations enter the traditional lender's Regulation 23A test, the affordability channel of the reported 2026 arrangements \cite{businessday_bnpl_2026}; the model has no scoring channel (Section~\ref{sec:asymmetry}). Under mandatory screening ($\mathbb{1}^{\text{aff}}$), the Regulation 23A test is applied to each \ac{BNPL} request, in the role of the \ac{FCA}'s affordability check \cite{fca_ps26_1, woolard2021}. Every arm is run at $\beta = 0$ and at $\beta = 1$ (Equation~\ref{eq:peer})."

Note: this drops "to test whether the results depend on peer influence" (obvious from context). It also turns the "three scenarios ... fourth arm" wording into "benchmark plus three arms"; **FLAG**: check that this matches how tables tab:scenarios and tab:switches and the figure caption ("three scenarios") label the arms, and make all four consistent.

05:19 can then drop "because the differences between them are small" (already in 03:41-43): "These four arms have one hundred replications each on shared seeds."

### B7. 02_model.tex:191-203 (distress, arrears and default). One paragraph defines three states, a robustness arm and a timing convention.

REVISED (split in two):
"Distress and arrears are distinct states. A household is distressed in a tick if it cannot cover committed expenditure from opening cash and income, or cannot meet the debt service due after seeking credit. A committed-expenditure shortfall counts as distress and is not carried forward. Credit raised against it pays debt service first, then discretionary consumption, and any remainder is saved; a robustness arm spends it on the unpaid committed expenditure first (Section~\ref{sec:results-effect}). Arrears track unpaid debt obligations through the \ac{CCMR} age bands.

Default occurs after seven consecutive distressed ticks, or 98 days, and blocks all further credit. Seven ticks is the nearest 14-day approximation to the 90-day impairment convention, although the distress rule differs from an account being 90 days in arrears. Default is permanent within a run and counted from the first tick, so the final-tick default rate is the share of all households that defaulted at any point in the two years."

### B8. 02_model.tex:274-291 (Submodel 5 and the shortfall cap).

REVISED:
"Under Submodel~5 an eligible household uses \ac{BNPL} first, up to $\kappa$ times its monthly discretionary budget. \ac{BNPL} cannot pay rent or an instalment directly; it relieves a shortfall because the household finances a purchase it would otherwise have paid for in cash. An agreement of value $F$ takes $F/4$ at checkout and leaves $3F/4$ in the household's hands, so it covers $3F/4$ of the shortfall. The household asks the traditional lender for the rest, an assumption, and the lender grants or refuses that amount in full under Submodel~9. A refused household leaves the remainder unpaid and is distressed in that tick.

The shortfall path reflects evidence that \ac{BNPL} users are disproportionately liquidity-constrained \cite{hayashi2025constraints, dehaan2024bnpl}; we found no study measuring how much of a shortfall they finance with it. Because \ac{BNPL} finances retail purchases and not general spending, the model caps the amount financed for a shortfall at the mean want-driven purchase. We found no empirical maximum, so the sensitivity analysis repeats each borrowing-amount rule with the cap removed, and a further arm removes \ac{BNPL} from the shortfall path altogether."

Also cut table row 02:237 (Submodel 5 "Rule" column) to: "Eligible households use \ac{BNPL} first, up to a cap; the traditional lender is asked for the remainder (text)."

### B9. 02_model.tex:130-160 (what the lender sees; the two switches; no credit score).

L130-138 REVISED:
"The traditional lender assesses an application on the household's surveyed gross income and on the scheduled service on its traditional debt, which the bureau records. The model does not reduce income while a member is unemployed, so a household in a spell of unemployment is assessed on income it is not receiving. In the benchmark the assessment excludes \ac{BNPL} commitments \cite{nortonrose_bnpl_sa, transunion_cps_sa_2025}, and the model omits informal borrowing, which South African households use \cite{finscope2019}. The lender therefore applies an affordability rule to an incomplete view of household obligations."

L155-160 REVISED:
"The bureau switch acts only through the affordability calculation. The model has no credit score and no risk-based pricing, so it cannot represent score-based refusals. This omission may matter, given the preliminary score reductions reported by \ac{FINASA} \cite{finasa_bnpl_2026}; Section~\ref{sec:future-work} discusses it as an extension."

Reason: original lists "creates no credit score, changes no lending prices and cannot represent score-based refusals", where the first and third say the same thing.

### B10. 01_introduction.tex:28-40 (reporting arrangements paragraph). Long, with a hedged date and a dangling "They also describe".

REVISED:
"Reporting arrangements are now changing. Reports describe an agreement between the \ac{NCR}, the \ac{SACRRA} and the Credit Bureau Association to include \ac{BNPL} payment behaviour in bureau records, and the \ac{NCR}'s position that an agreement may become incidental credit when default charges are levied \cite{businessday_bnpl_2026}. Providers reportedly began submitting records in 2026 while the reporting format was being finalised \cite{dcasa_bnpl_2026}, and records are reported to be expected on consumer profiles from February 2027 \cite{businessday_bnpl_2026}. The \ac{FINASA} reports one bureau's preliminary estimate that scores could fall for roughly a quarter of credit-active consumers \cite{finasa_bnpl_2026}.

How far would making \ac{BNPL} visible to lenders change household distress? Our model has no credit score, so it tests reporting only through the traditional lender's affordability assessment, which we call the affordability channel (Section~\ref{sec:asymmetry})."

Reason: "has been reported ... we treat this as a reported timetable, not a confirmed statutory commencement date" says "reported" twice and uses a "not X" contrast. **FLAG**: if the author wants to stress that no commencement date is legislated, keep one short clause; check the citation placement for the NCR incidental-credit position (the original attributes both to the same "reports").

---

## Part C. Line edits by chapter

### Abstract (main.tex)

- main.tex:84 — ORIGINAL: "In 2017, before \ac{BNPL} spread in South Africa, 14.2\% of unsecured and credit-facility accounts were more than 90 days in arrears, and credit bureaus did not record \ac{BNPL}." — REVISED: "In 2017, before \ac{BNPL} spread in South Africa, 14.2\% of unsecured and credit-facility accounts were more than 90 days in arrears. Credit bureaus do not yet record \ac{BNPL}; industry arrangements reported in 2026 are expected to add it from 2027." — joins the two reporting facts. **FLAG**: tense ("did not" vs "do not yet") depends on whether you mean 2017 only.
- main.tex:88 — ORIGINAL: "depending on how they choose among platforms; default responds detectably to neither that choice nor the number of platforms." — REVISED: "depending on how they choose among platforms. Neither that choice nor the number of platforms changes default detectably." — awkward inversion.
- main.tex:91 — ORIGINAL: "Adding \ac{BNPL} obligations to that assessment raises refusals by about a sixth and default by 0.15 to 0.22 points, mostly in the lowest income quintile; in the model a refused household has no other source of credit." — REVISED: "Adding \ac{BNPL} obligations to that assessment raises refusals by about a sixth and default by 0.15 to 0.22 points, mostly in the lowest income quintile. In the model a refused household has no other source of credit." — split.
- main.tex:92 — "affordability screening" — REVISED: "mandatory screening" if that becomes the single term (Part A7).

### Chapter 1

- 01:17-18 — ORIGINAL: "\ac{BNPL} obligations were not part of the information that South African lenders used to assess affordability." — REVISED: "South African lenders did not see \ac{BNPL} obligations when assessing affordability." — noun-heavy.
- 01:22-24 — ORIGINAL: "A household could therefore take on obligations with several providers without any one lender seeing everything the household owed." — REVISED: "A household could therefore owe several providers without any lender seeing all its debts." — shorter.
- 01:57-60 — ORIGINAL: "The experiments measure the effect of these changes within a specified model of household finances, in which additional obligations interact with existing debt, cash buffers and income shocks. They do not estimate..." — REVISED: "The experiments measure these effects within a model of household finances in which new obligations interact with existing debt, cash buffers and income shocks. They do not estimate..." — "specified" adds nothing. Keep this disclaimer here and cut its near-copy in 06:8.
- 01:73 — ORIGINAL: "Three subsidiary questions, referred to as RQ1 to RQ3, guide the analysis:" — REVISED: "The subsidiary questions are:" — the enumerate already numbers them; RQ labels can be added in the list items.
- 01:76-78 — ORIGINAL: "How well does a synthetic household population built from South African survey microdata reproduce the selected baseline arrears bands, and how does it perform against benchmarks not used in fitting or construction?" — REVISED: "How well does a synthetic population built from South African survey data reproduce the baseline arrears bands to which it is fitted, and how does it compare with benchmarks not used to build or fit it?" — plainer verbs.
- 01:99-101 — D'Orazio and Giulioni sentence does not say what it contributes to this model, unlike its neighbours. **FLAG**: add a half-clause on relevance (e.g. credit rationing) or drop.
- 01:139-141 — ORIGINAL: "With the extra spending that Di Maggio et al.\ find, this motivates want-driven purchases, made without a cash shortfall, and a peer channel in adoption." — REVISED: "Together with the extra spending that Di Maggio et al.\ find, these results motivate two features of the model: want-driven purchases, made without a cash shortfall, and peer influence on adoption." — vague "this"; "peer channel in adoption" is jargon.
- 01:157-158 — ORIGINAL: "Responses to changes in payment formulas also suggest anchoring beyond what liquidity constraints alone explain." — REVISED: "Their evidence on responses to changes in payment formulas also suggests anchoring beyond what liquidity constraints explain." — whose responses was unclear.
- 01:174-176 — ORIGINAL: "informed the approach of the \ac{FCA} to deferred payment credit" — REVISED: "informed the \ac{FCA}'s approach to deferred payment credit" — shorter.
- 01:178-180 — ORIGINAL: "We therefore compare a lightly screened \ac{BNPL} channel with mandatory screening under the South African residual-income test, and test bureau visibility alone and with screening, each with and without peer influence." — REVISED: "We therefore compare a lightly screened \ac{BNPL} channel with one screened under the South African residual-income test, alone and with bureau visibility." — design detail belongs in Section 5 (05:11-16).
- 01:188-192 — ORIGINAL: "This thesis addresses that gap by combining survey-derived household finances with explicit lender-specific decisions." — REVISED: "We address that gap by combining household finances from South African surveys with lenders that differ in what they observe and how they screen." — "explicit lender-specific decisions" is jargon; also enforces "we".

### Chapter 2

- 02:10-16 — ORIGINAL paragraph of pointers ("Parameter choices and calibration are in ... Appendix ... explains ... Appendix ... records ... Appendices ... provide the pseudocode.") — REVISED: "The specification follows the \ac{ODD} protocol \cite{grimm2006odd, grimm2020odd}; Table~\ref{tab:submodels} summarises the rules, Section~\ref{sec:calibration} sets the parameters, and Appendices~\ref{app:rationale} to~\ref{app:pseudo-main} give the design rationale, exclusions and pseudocode." — excessive signposting. **FLAG**: check that the appendix range reference reads correctly in the compiled order.
- 02:31-32 — ORIGINAL: "\textbf{Households} respond to their current finances through the borrowing and repayment rules below." — REVISED: delete; start the item with "\textbf{Households} are each based on a \ac{NIDS} Wave 5 household..." — empty sentence.
- 02:39-41 — ORIGINAL: "Its contents determine which recorded obligations enter the traditional lender's assessment." — REVISED: "The traditional lender's assessment uses what it records." — simpler.
- 02:51-52 — "Table~\ref{tab:agent-mapping} links each initial household variable to its source, and Section~\ref{sec:calibration} explains the construction." — delete; the table is already referenced in the Households bullet. Signposting.
- 02:149-151 — ORIGINAL: "The model does not say how a platform would obtain that information without bureau reporting, so the screening arm is an upper bound on what a platform's own check could see." — REVISED: "The model does not specify how a platform would obtain this information without bureau reporting, so mandatory screening represents the most a platform's own check could see." — term consistency; "upper bound on what ... could see" is abstract.
- 02:165-167 — "Monthly survey flows are converted to tick amounts using $12/26$, the ratio of months to ticks in a year." — already in the agent-mapping table note (02:58). Keep one.
- 02:268-272 — ORIGINAL: "When a household faces a shortfall, Submodel~4 determines how much it requests. By default, the request equals the shortfall." — REVISED: "Under Submodel~4 a household requests exactly its shortfall by default." — two sentences into one.
- 02:335-338 — ORIGINAL: "No rule assigns a household a number of platforms, and the routing rule alone determines how overlapping agreements are spread across them. The stacking measures therefore show how often a household's agreements overlap, and carry no information about why a household would use several providers." — REVISED: "The routing rule alone spreads overlapping agreements across platforms; no rule sets how many platforms a household uses. The stacking measures therefore show how often agreements overlap and say nothing about why households use several providers." — shorter.
- 02:339-342 — ORIGINAL: "A robustness arm uses the opposite rule: a household tries the platforms it already owes first and moves to another only when a limit binds" — REVISED: "A robustness arm uses loyal routing: a household tries the platforms it already owes first and moves to another only when a limit binds" — define the term once (Part A7).
- 02:251 (Submodel 12, parameters column) — very dense: Woolard comparator, 0.10-0.48 band and the "respect in which they overstate the limits". **FLAG**: the derivation is already in Appendix B; the cell could keep "λ swept 0.1-1.0; comparator band 0.10-0.48 (Appendix~\ref{app:specification})" plus the binding-rate note.
- 02:217 (table note) — ORIGINAL: "Behavioural rules are either grounded in literature or flagged as assumptions, and free parameters are sourced, derived, fitted or assumed, as defined in the note to Table~\ref{tab:param-register}, which gives each parameter's default value, provenance and sweep range." — REVISED: "Rules are grounded in literature or flagged as assumptions; Table~\ref{tab:param-register} gives each parameter's value, provenance and sweep range." — long nested note.

### Chapter 3

- 03:4-6 — ORIGINAL: "This section answers RQ1. We construct the population from South African survey data, assign debt-service and product parameters, fit two parameters to the baseline arrears profile, and then check what the model reproduces beyond those targets." — REVISED: "This section answers RQ1." (merge with the next sentence about Table param-taxonomy) — roadmap duplicates the subsection headings.
- 03:55-56 — one-sentence paragraph on 2017 Rands. Move to the end of 03:61-65.
- 03:101-103 — ORIGINAL: "The match does not recover relationships with recipient characteristics omitted from it, such as urban or rural location; within a cell, flags are assigned without regard to them." — REVISED: "Within a cell, flags are assigned without regard to characteristics outside the match, such as urban or rural location, so relationships with them are lost." — one idea, said once.
- 03:195-196 — ORIGINAL: "Figure~\ref{fig:pop-fidelity} compares the resample with its source; the per-capita income Gini rises by 0.015, from 0.6514 to 0.6668." — the Gini change is also in the figure note and Table validation row E. Keep in one place.
- 03:217-222 — ORIGINAL: "The statutory rates are proxies. Realised product rates were not available in the \ac{CCMR} \cite{ncr_ccmr_2017} or the other 2017 sources consulted. Because realised rates cannot exceed the ceilings, this choice biases calculated payments upward." — REVISED: "Realised product rates were not available in the \ac{CCMR} \cite{ncr_ccmr_2017} or the other 2017 sources consulted, and because they cannot exceed the statutory ceilings, using the ceilings biases calculated payments upward." — the proxy point is already in 01:170-171 and the table note.
- 03:248-253 — ORIGINAL: "The cap binds for only 3.8\% of debtors but removes 22.8\% of calculated service (Appendix~\ref{app:var-servicing}). The non-food aggregate already includes clothing-account, hire-purchase and vehicle payments, a median 12.6\% of non-food outlay among the households reporting them, so adding reconstructed service partly counts that flow twice. This overstates compressible outlay and understates service as a share of it; the net effect on default is unsigned." — REVISED: "The cap binds for only 3.8\% of debtors but removes 22.8\% of calculated service (Appendix~\ref{app:var-servicing}).

  The non-food aggregate already includes clothing-account, hire-purchase and vehicle payments, a median 12.6\% of non-food outlay among the households reporting them, so reconstructed service partly double-counts them. Compressible outlay is therefore overstated and service as a share of it understated; the direction of the net effect on default is unknown." — "unsigned" is jargon; two unrelated points split.
- 03:272-273 — ORIGINAL: "which shows how much the value matters but cannot show that it transfers." — fine; keep.
- 03:285-289 — ORIGINAL: "The selected values are 1.6\% and 9\% per tick. The shock probability is chosen from a grid with steps of 0.8 percentage points. A check in steps of 0.1 points places the target between 1.5\%, which gives a 90+ share of 13.93\%, and the selected 1.6\%, which gives 14.48\% (Table~\ref{tab:arrears-fit})." — REVISED: "The selected values are 1.6\% and 9\% per tick. The shock probability comes from a grid in steps of 0.8 points; a finer check in steps of 0.1 points places the target between 1.5\% and the selected 1.6\% (Table~\ref{tab:arrears-fit})." — numbers in the table. **FLAG**: keep 13.93/14.48 if they are not in tab:arrears-fit.
- 03:327-330 — ORIGINAL: "Construction checks test whether the population preserves the properties of its sources, and calibration checks test the fit to the two targets. External comparisons, against quantities neither fitted nor imposed, test more than the construction, but only as far as they measure comparable populations and outcomes." — REVISED: "Construction checks test whether the population preserves its sources, and calibration checks test the fit to the two targets. External comparisons test the model against quantities it was neither fitted to nor built from, and are only as informative as those quantities are comparable." — abstract nouns.
- 03:383-387 — ORIGINAL: "That measure was not used to fit servicing, although the survey supplies other construction inputs. The remaining fourteen checks comprise thirteen construction checks and one diagnostic on how often the Regulation 23A cap binds. Passing them demonstrates the internal consistency of the construction only." — REVISED: "\ac{FinScope} supplies other construction inputs, but this measure was not used to fit servicing. The remaining fourteen checks, thirteen construction checks and one diagnostic on how often the Regulation 23A cap binds, test only the internal consistency of the construction." — clause order.
- 03:457-464 — restates all four purchase and volume figures from tab:bnpl-on-checks. REVISED: "The model fails the purchase-size and volume checks (Table~\ref{tab:bnpl-on-checks}). The mean want-driven purchase is R633 against a target of R992, just outside the 35\% tolerance, and annual volume falls below both provider-derived bounds. The model's \ac{BNPL} market therefore has smaller purchases and less volume per user than the provider disclosure." — **FLAG**: keep the replication counts (4 of 20; 0 at β=1) if they are not in the table.
- 03:474 — "We record the failure as specified rather than amend the condition after the result." — formulaic "rather than"; see B3.
- 03:486-497 — ORIGINAL: "These results give limited confidence in the empirical accuracy of the model's outcome levels." — REVISED: "We therefore place limited confidence in the model's outcome levels." — noun stack.
- 03:299 (table note) — "compared with it for shape and scale rather than point for point" — REVISED: "compared with it for shape and scale only" — "rather than" contrast.

### Chapter 4

- 04:35 — ORIGINAL: "The $\beta=1$ arm stacks far more than the only external evidence records." — REVISED: "At $\beta=1$ households stack far more than the external evidence shows." — awkward personification of an arm.
- 04:46-48 — ORIGINAL: "Default and depleted savings rise together where borrowing is heavy, although these population aggregates do not show that the households which default are those whose savings were depleted." — REVISED: "Default and depleted savings rise together where borrowing is heavy, although the aggregates do not show that the same households are affected." — shorter; this caveat recurs (Part A2).
- 04:59-64 — see B3 follow-on (cut to one sentence).
- 04:103-107 — "the sweep does not isolate invisibility" — REVISED: "the sweep cannot separate the effect of platforms not seeing one another from the effect of extra capacity." — **FLAG**: confirm this is the intended meaning of "invisibility".
- 04:122-124 — ORIGINAL: "At $\beta=0$, moving from zero to full access changes default by $+0.14 \pm 0.11$ points, which is not detectable." — REVISED: "At $\beta=0$, moving from zero to full access does not change default detectably ($+0.14 \pm 0.11$ points)." — claim first. Same pattern at 04:138, 04:140, 04:240.
- 04:143-144 — ORIGINAL: "The test is limited, however." — delete; the next sentence shows the limit. Mechanical transition.
- 04:199-208 — Order problem: 04:202 mentions "Apart from the single-tick shock" before the single-tick shock is introduced at 04:206. Move "Shock persistence matters more than any of these..." (04:206-208) to before "Three other assumptions move the default level" and change "more than any of these" to "more than any other assumption". 
- 04:234-244 — split after "...where households borrow one tick of committed expenditure beyond the shortfall and the shortfall cap is removed." Start a new paragraph at "Under the single-tick shock...". Then: "The three alternative rules for routing and the shortfall path leave the effect near its reference value of $0.60 \pm 0.12$: $0.62 \pm 0.07$ under loyal routing, $0.68 \pm 0.11$ when credit pays a committed shortfall first, and $0.47 \pm 0.11$ when \ac{BNPL} cannot relieve a shortfall at all. Most of the effect therefore runs through want-driven borrowing." — overlong sentence; term consistency.
- 04:248-250 — ORIGINAL: "Two of the five, $\lambda=0.25$ and $\lambda=1.0$, give identical defaults in every replicate, because the limit seldom binds at either value, so they amount to one result." — REVISED: "Two of the five, $\lambda=0.25$ and $\lambda=1.0$, are one result: the limit seldom binds at either value, so defaults are identical in every replicate." — claim first.
- 04:257-267 — see B5.
- **FLAG (consistency, not language)**: 04:235-236 gives the detectable β=1 effect range as 0.25 ± 0.09 to 1.27 ± 0.11; 06:39 gives "0.37 ± 0.09 to 1.27 ± 0.11" under the borrowing rules. If 06:39 means a subset of settings, say which.

### Chapter 5

- 05:10-16 — see B6.
- 05:19 — drop the reason clause (repeated from 03:41-43).
- 05:36 — ORIGINAL: "The rise is $0.22 \pm 0.04$ points at $\beta = 0$ and $0.15 \pm 0.04$ at $\beta = 1$; at $\beta = 0$ that is more than the $0.12 \pm 0.05$ by which enabling \ac{BNPL} raises default (Section~\ref{sec:results-injection}), although the two come from different seeds." — REVISED: "The rise is $0.22 \pm 0.04$ points at $\beta = 0$ and $0.15 \pm 0.04$ at $\beta = 1$. At $\beta = 0$ this exceeds the $0.12 \pm 0.05$ by which enabling \ac{BNPL} raises default (Section~\ref{sec:results-injection}), although the two come from different seeds." — split semicolon.
- 05:37-38 — ORIGINAL: "Screening changes it by $+0.02 \pm 0.05$ and $+0.02 \pm 0.06$ points. With standard errors of 0.05 and 0.06 points, an effect of screening of about a tenth of a point in either direction cannot be ruled out." — REVISED: "Screening changes it by $+0.02 \pm 0.05$ and $+0.02 \pm 0.06$ points, so an effect of about a tenth of a point in either direction cannot be ruled out." — repeats the standard errors just given.
- 05:44 — ORIGINAL: "The rise in default is largest in Q1, at $0.59 \pm 0.07$ and $0.46 \pm 0.08$ points, is not detectable in Q2 to Q4, and is $0.23 \pm 0.10$ and $0.22 \pm 0.11$ points in Q5, just beyond two standard errors." — REVISED: "The rise in default is largest in Q1, at $0.59 \pm 0.07$ and $0.46 \pm 0.08$ points. It is not detectable in Q2 to Q4, and in Q5 it is $0.23 \pm 0.10$ and $0.22 \pm 0.11$ points, just beyond two standard errors." — split; reader loses which pair is which β. Consider "(β = 0 and β = 1)" once.
- 05:48-49 — ORIGINAL: "A refused household has no other source of credit in the model, and the horizon is two years: a loan that is granted postpones distress, and its later cost may fall outside the horizon. The result therefore gives the direction of the affordability channel over two years in the model, not a forecast of the reporting arrangements." — REVISED: "Two features of the model favour this result: a refused household has no other source of credit, and a granted loan postpones distress whose later cost may fall after the two-year horizon. The result therefore shows the direction of the affordability channel in the model and does not forecast the effect of the reporting arrangements." — "not a forecast" contrast; disclaimer already in 01:59-60. **FLAG**: "favour this result" is an interpretive claim; check that it is what you intend.
- 05:53-55 — ORIGINAL (one sentence of 50 words from "Bureau visibility then acts only on..."). REVISED: "Bureau visibility then acts only on the traditional lender, and at $\beta = 0$ screening roughly halves its effect. With both switches the lender refuses 114 more applications than in the benchmark, against 198 under bureau visibility alone, and default is $0.12 \pm 0.04$ points lower than under bureau visibility alone." — split.
- 05:63 — ORIGINAL: "...the effect of bureau visibility is $0.07 \pm 0.06$ points smaller at $\beta = 1$ than at $\beta = 0$, which is not detectable." — REVISED: "...the effect of bureau visibility at $\beta = 1$ differs undetectably from that at $\beta = 0$ ($-0.07 \pm 0.06$ points)." — claim first.
- 05:68 — long sentence; split at "(Appendix~\ref{app:levers})": "...against $-0.35 \pm 0.09$ for the cap as modelled on the same seeds (Appendix~\ref{app:levers}). The experiments therefore do not show that lost volume is what lowers default."
- 05:71-72 — answer is fine; leave.

### Chapter 6

- 06:8 — ORIGINAL: "We answered with a controlled counterfactual under 2017 conditions, so the results describe mechanisms in the model; they neither estimate the historical effect of \ac{BNPL} nor forecast default under the new reporting arrangements." — REVISED: "We answered with a controlled counterfactual under 2017 conditions, so the results describe mechanisms in the model." — the rest repeats 01:59-60 nearly verbatim.
- 06:9 — ORIGINAL: "In the model, enabling \ac{BNPL} raises default by 0.1 to 0.6 points, more where households borrow more; making it visible to the traditional lender raises default through refusals; and screening \ac{BNPL} requests does not change default detectably." — REVISED: "In the model, enabling \ac{BNPL} raises default by 0.1 to 0.6 points, more where households borrow more. Making it visible to the traditional lender raises default through refusals, and screening \ac{BNPL} requests does not change default detectably." — semicolon chain.
- 06:11-12 — repeats the miss list from 03:489-492. Fine for a conclusion, but shorten to "It misses five behavioural and market comparisons (Tables~\ref{tab:arrears-fit}, \ref{tab:validation} and~\ref{tab:bnpl-on-checks}), so the outcome levels warrant limited confidence." — **FLAG**: author's call whether the examiner needs the full list here.
- 06:15 — ORIGINAL: "...and 36.6\% when they return to platforms they already owe, each measured on its own seed block (Section~\ref{sec:results-stacking}); the share depends on the routing rule, and default does not." — REVISED: "...and 36.6\% under loyal routing (Section~\ref{sec:results-stacking}). The share depends on the routing rule; default does not." — drop the seed-block note (made twice in ch4).
- 06:16 — ORIGINAL: "Nor does default change detectably with the number of platforms, but because each platform brings its own limit, the sweep does not isolate invisibility (Table~\ref{tab:stacking})." — REVISED: "Default does not change detectably with the number of platforms either, but each platform brings its own limit, so the sweep cannot isolate the effect of platforms not seeing one another (Table~\ref{tab:stacking})." — "invisibility" jargon.
- 06:17-18 — the β = 1 caveat is the fourth occurrence. REVISED for 06:18: "The $\beta = 1$ setting is illustrative, so the $\beta = 0$ arm is the better guide to magnitudes." — "stacks far more than United States borrowers do" already given in ch4.
- 06:39 — see the consistency FLAG under chapter 4 (0.37 vs 0.25).

---

## Part D. Things that are fine and should stay

- Claim-first topic sentences in 04:25, 04:42, 04:103, 05:35, 05:41, 05:51 are good models for the rest.
- "Detectable" is defined once and used consistently; keep it.
- Chapter 1's literature section is already tight; only the edits above are needed.
- No em dashes and no banned filler words were found in the body.
