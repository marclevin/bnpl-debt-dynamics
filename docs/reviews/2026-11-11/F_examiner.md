# F. External examiner's report: academic quality of the argument

Read from the LaTeX source at HEAD 226a515 (main.tex, chapters 01 to 06, appendices A to G, and all generated tables), with main.log of 2026-11-10 15:24. I checked docs/DEFECTS.md, docs/DECISIONS.md and docs/ARREARS_RULE_2026-11.md only after forming each view. "Recorded" means the issue appears there. "Disclosed" means the thesis text states it. Line numbers are source lines. Points marked *judgement* are my reading of the model, not a measured result.

---

## Findings

### HIGH

**H1. The headline effect depends on counting BNPL arrears as household default, and the body never says so.**
- `appendix_c_supplementary.tex:30-33`: "the \ac{BNPL} effect without peer influence was $-0.10 \pm 0.06$ points ... Under that rule food and rent shortfalls drove default, and \ac{BNPL} arrears did not count."
- `04_results.tex:24-25`: "0.94 are households whose oldest unpaid \ac{BNPL} instalment reached 98 days and 0.13 come through traditional arrears".
- `06_conclusion.tex:41`: "Default follows the bureau's 90-day construct".
- **Problem.** Under the earlier rule the effect was about zero. Under the current rule it is +1.08, and 0.94 of that is BNPL instalments reaching 98 days. The headline therefore comes mostly from a definitional choice: a 98-day BNPL arrear counts as household default. The conclusion defends the construct as "the bureau's", but in the benchmark, and in the 2017 bureau data the model is compared with, BNPL arrears were not on bureau records. The construct can be defended as a measure of distress. It is not the bureau's construct for the 0.94 points. The only place the reader learns that the sign depended on this choice is an appendix paragraph.
- **Fix.** Add two sentences to 4.1 (or 4.6) and one clause to the conclusion. They should say that the effect comes from counting BNPL 90+ day arrears as default, that the earlier cash-flow rule gave −0.10 ± 0.06, and that BNPL arrears were not on bureau records in the benchmark. Reword 06:41 accordingly. Add a row to the limitations index.
- **Status.** Recorded as a decision (DECISIONS D18; ARREARS_RULE "The thesis story changes from 'BNPL adds little' to 'BNPL default is a channel of its own'"). Not in DEFECTS. Disclosed only in Appendix C.

**H2. In the benchmark the bureau effectively records BNPL delinquency, and a BNPL default freezes traditional debt.**
- `02_model.tex:75-76`: "The credit bureau records each household's traditional debt service and whether it has defaulted. In the benchmark it does not record \ac{BNPL}."
- `02_model.tex:199-201`: "Default is permanent and recorded by the bureau, and a defaulted household receives no further credit. Its accounts are non-performing: nothing more is due or collected".
- `appendix_g_pseudo_main.tex:103`: "$d_i \gets 1$; the bureau records the default".
- **Problem.** Default can be triggered by BNPL arrears alone. When it is, the bureau records it and traditional credit stops, even in the benchmark, which is defined as the world in which the bureau does not see BNPL. The household's traditional instalments also stop falling due. This contradicts the information structure in Figure 1 and Submodel 10. It has two consequences. (a) The benchmark already passes the most informative BNPL signal, delinquency, to the lender, so RQ3's "bureau visibility" switch only adds live instalments. (b) A small BNPL arrear relieves the household of its traditional debt service. The text states the two facts in different places and never reconciles them.
- **Fix.** Say it in 2.2 and in the limitations index: in the model a BNPL-triggered default is reported and ends all credit, whereas before 2027 it would not have reached the bureau. Give the share of defaults during the run that are BNPL-only. Re-read the RQ3 answer in that light.
- **Status.** The rule is recorded (D18 "absorbing and recorded by the bureau"; D10 "bureau record ... holds traditional debt only"). The conflict between them is not recorded in DEFECTS (H1 in the 2026-10-13 table concerns arrears inside the visible obligation, which is a different point). Not disclosed as a conflict.

**H3. The mechanism the text gives is "the platforms lend where the test would not". The evidence points to repayment tenor inside a two-year window.** *(judgement)*
- `03_calibration.tex:405-406`: "Without \ac{BNPL}, 47\% of those 120 default during the run; with \ac{BNPL} at $\beta=0$, 85\% do."
- `06_conclusion.tex:26-27`: "to whom the platforms' light screen lends where the Regulation 23A test would not."
- `05_policy.tex:57-59`: "whereas a granted loan is repaid over 25 months, partly after the run ends".
- `04_results.tex:185`: "Every result belongs to the two-year horizon."
- **Problem.** The 120 at-risk households hold no traditional debt at the start, yet 47% default without BNPL. The Regulation 23A test therefore does lend to them, on 25-month terms. It can do so because it deducts the statutory expense norm (Table 28), not their actual food and rent. Under screening, a refused BNPL request passes to the same lender, and default returns to about the no-BNPL level (`05_policy.tex:65-72`). The difference BNPL makes is the tenor. A pay-in-four instalment falls due within six weeks and is paid before anything else. A 25-month loan's arrears mostly ripen after tick 52. Two further results fit this reading and are left unexplained: a tenfold limit lowers default by 0.28 ± 0.12 (`04_results.tex:175-176`), and borrowing 25% more than the shortfall lowers it by 0.51 ± 0.14 (`04_results.tex:202-203`). In both, more credit pushes arrears past the window. Chapter 5 applies this horizon argument to bureau visibility (05:57-61) but not to the headline effect. "Default within two years" mixes timing with incidence.
- **Fix.** In 4.1 and in the conclusion's RQ2 paragraph, say that without BNPL these households borrow from the traditional lender on 25-month terms. The effect therefore compares six-week with 25-month repayment for households whose recorded income does not cover food and rent, measured over two years, and may narrow over a longer horizon. Replace 06:26-27. Extend the "running past two years" further-work sentence (06:51-52) to the injection.
- **Status.** DEFECTS B41(a) records a 104-tick run for the bureau switch only. The point is not recorded for the headline. Disclosed only as the blanket sentence at 04:185.

**H4. The abstract's stacking sentence drops the qualification the body and conclusion carry.**
- `main.tex:112`: "Many users owe several platforms at once, but default shows no detectable rise with the number of platforms."
- `04_results.tex:96-97`: "How often households stack is therefore set by the routing assumption and by how often they borrow".
- `04_results.tex:104-106`: "platform count and total credit capacity move together, and the sweep cannot isolate the effect of platforms not seeing one another."
- `06_conclusion.tex:18-19` keeps the routing qualification.
- **Problem.** The abstract presents an assumption-driven quantity as a finding. Its "but" also invites the reading that stacking is harmless, which 4.3 says the design cannot show. Under loyal routing only 13% of ever-holders stack at β = 0 (`04_results.tex:95`), so "many" and "common" (04:83, 04:248, 06:18) depend on the assumption.
- **Fix.** Use "Under the assumed random routing, many users owe several platforms at once; default does not change detectably with the number of platforms, but more platforms also means more credit, so the sweep cannot show what platform blindness costs." Make the same edit at 04:248 and 06:18.
- **Status.** Recorded as an accepted gap (B41(c) shared-limit arm; B8 for the CFPB gap). The divergence in the abstract is not recorded.

### MEDIUM

**M1. The bureau-visibility result is stated more strongly in the abstract and introduction than in Chapter 5.**
- `01_introduction.tex:66`: "Bureau visibility raises default a little".
- `main.tex:115`: "raises refusals by about 13\% and default by 0.20 points without peer influence, because in the model refused households have no other credit."
- Chapter 5 also says: "at $\beta=0.3$ the rise, $0.10 \pm 0.06$, is not detectable" (05:20) and "The model's rules may favour this result ... the result gives the direction of the affordability channel in the model and is not a forecast" (05:57-61).
- 3.1 sets the rule that "a single detectable difference carries less weight than one that repeats across seed blocks" (`03_calibration.tex:71-73`), and this result comes from one block.
- **Problem.** The introduction gives the result with no qualification. The abstract gives a causal "because" that no arm tests (B41(b), following refused against granted households, was not run). Even "direction" outruns the evidence if granted loans default after tick 52 (H3).
- **Fix.** Add "at β = 0, from one seed block" to the introduction, and add "under rules that may favour it: no other lender, immediate arrears on refusal, a two-year horizon" to the abstract. In 05:61, use "the sign within two years" rather than "the direction".
- **Status.** Recorded (B41(a), (b); D10 note). Disclosed in Chapter 5 only.

**M2. The RQ3 answer implies that peer influence removes the bureau effect.**
- `05_policy.tex:101-102`: "with peer influence the rise is not detectable."
- `05_policy.tex:85-86`: "($-0.09 \pm 0.08$ points for bureau visibility)" (the interaction is not detectable).
- **Problem.** The two values of β do not differ detectably, so the honest summary is a rise of 0.10 to 0.20 at both. The abstract and conclusion repeat the β = 0 figure alone.
- **Fix.** "Bureau visibility raises default by 0.20 ± 0.07 points at β = 0 and 0.10 ± 0.06 at β = 0.3, which do not differ detectably."
- **Status.** Not recorded.

**M3. The main question asks about "distress", but the BNPL injection is answered on default alone.**
- `04_results.tex:38-39`: "and the share ever short of food and rent by $0.06 \pm 0.01$. The share with no liquid savings rises by $0.17 \pm 0.04$."
- The RQ2 answer (04:245-261) and the conclusion (06:18-27) mention only default.
- **Problem.** For RQ3 the thesis rightly warns that lower default may come with more food shortfall. For the injection it does not report that BNPL worsens both measures. That asymmetry leaves the main question half-answered.
- **Fix.** Add one sentence to the RQ2 answer and to the conclusion.
- **Status.** Not recorded.

**M4. The null effect of peer influence is largely implied by the design.**
- `02_model.tex:280`: "A want-driven order is reduced to what the household can pay at checkout."
- `04_results.tex:71-72`: "A slope this small is consistent with the shortfall path: $\beta$ acts only on want-driven purchases."
- `main.tex:113`: "the effect does not change detectably with peer influence over the range tested, although households borrow 2.4 times as much at its top".
- **Problem.** β acts only on want-driven purchases. Those purchases are sized at κ of the discretionary budget, cut to cash at checkout, and made after the tick's debts are paid, and BNPL arrears are not subject to persistence. The Sobol table makes the same point: q_base from 0.01 to 0.30 sets holding (S1 0.89) but not default. The flat slope is mostly a consequence of these rules, and the checkout cut is one of the six assumptions that are never varied (`appendix_b_specification.tex:69-73`). The abstract presents it as a finding.
- **Fix.** Say in 4.2, the abstract and the conclusion that the rules make want-driven borrowing unlikely to reach 98 days, so the flat slope is expected by design.
- **Status.** Not recorded. Partly disclosed ("consistent with").

**M5. The abstract carries no measurement caveat for the 3.6% group.**
- `main.tex:114`: "most of them households whose surveyed income does not cover food and rent".
- `03_calibration.tex:399-401`: "for 68\% of the group's respondents, the household's own answer to a single income question covers food and rent."
- Among the other households the effect is +0.11 ± 0.07, not detectable (`03_calibration.tex:407-409`).
- **Problem.** This is the accepted position, and I criticise only how the abstract handles it. The reader of the abstract takes "1.0 percentage point" as a population effect. They are not told that it is undetectable for 96% of households, or that the survey cannot say whether the remaining group is genuinely short.
- **Fix.** Add a half-sentence to the abstract covering both points.
- **Status.** Recorded (B47). Disclosed in 3.5, Appendix C and the conclusion's limits paragraph, but not in the abstract.

**M6. The reported precision is Monte Carlo precision on a single population draw.**
- `03_calibration.tex:73-74`: "The standard errors measure simulation variance only, not uncertainty in the data, the drawn population or the assumptions." This is good.
- `06_conclusion.tex:20` and `04_results.tex:250` then report "$1.03 \pm 0.06$" with no qualification.
- **Problem.** About 0.9 of the effect comes from 182 agents copied from 109 NIDS records in one resample (seed 20260818). *Judgement:* the binomial variation of 182 in 5,000 alone is about ±13 agents, or ±7% of 0.9 points (about ±0.07). That is as large as the reported SE, before NIDS sampling error is counted. With 250 replicates, effects of 0.06 points become "detectable" (04:38), and the text never says what size of effect would matter economically.
- **Fix.** Put a one-line reminder beside the headline ± in 4.1 and the conclusion. State the order of magnitude of population-draw uncertainty for the group's share. Distinguish "detectable in the simulation" from "material".
- **Status.** Not recorded. Disclosed once in 3.1.

**M7. The external checks reported in RQ1 are partly designed in, and the failed half is not reported.**
- `03_calibration.tex:475-476`: "traditional arrears rise with \ac{BNPL} as Pattern~1 expects, though the design was chosen with that pattern in view".
- `03_calibration.tex:423-426`: "traditional interest does not change detectably ... Households pay \ac{BNPL} instalments before traditional debt, so \ac{BNPL} obligations can crowd out traditional payments."
- **Problem.** The arrears half of Pattern 1 follows from the payment order (BNPL first), which is assumed and never varied (`appendix_b_specification.tex:70-71`). The interest half fails, and the RQ1 answer omits it. Neither the RQ1 answer nor the conclusion's RQ1 paragraph names any validation that could have gone against the model.
- **Fix.** In the RQ1 answer, add "and traditional interest does not change", and say that the arrears rise follows from the assumed payment order.
- **Status.** B2 (closed: "partly built in"). The payment-order link is not recorded.

**M8. RQ1 asks a question the design answers by construction.**
- `01_introduction.tex:85-86`: "How well does a synthetic household population ... reproduce the selected baseline arrears bands".
- **Problem.** The run starts from the bands, and two parameters are fitted to them (03:296-298). The text is honest about this, but the question as posed is not a research question.
- **Fix.** Use "whether the calibrated baseline holds the 2017 arrears profile over the run, and how the model compares with external figures not used in fitting or construction".
- **Status.** B43 accepted the "external comparisons" wording. This half is not recorded.

**M9. The assumptions that carry the effect are not listed where the effect is qualified.**
- `03_calibration.tex:466-467`: "no arm varies the debt-service construction or the starting profile."
- **Problem.** The effect also rests on several assumptions that no arm varies:
  - food and rent are incompressible (Submodel 2, source "None"). This is what makes the 3.6% group short every tick;
  - the placement rule, under which all 62 debt-holders in the group start in default, so only 120 are at risk (03:403-405);
  - the payment order;
  - for RQ3, the fitted arrears persistence of 0.72, which keeps a refused household in arrears "whatever its cash" (register line 85) and is not in the Sobol design.
- **Fix.** Extend the sentence at 03:466-467 and the limitations index to name these assumptions.
- **Status.** B44 records the placement rule and the persistence parameter as assumptions. Their link to the effect and to RQ3 is not recorded.

**M10. "Shortfall" is never defined in prose, and the shortfall path contradicts Submodel 2.**
- `02_model.tex:215`: "a household short of cash requests exactly its shortfall".
- `02_model.tex:223-225`: "it relieves a shortfall because the household finances a purchase it would otherwise have paid for in cash".
- `appendix_g_pseudo_main.tex:61`: the shortfall includes BNPL instalments due ($b$).
- **Problem.** The prose never says that a shortfall includes instalments due, BNPL ones included. A household can therefore take a new agreement to meet an old one, which is a rollover mechanism readers will want named. Submodel 2 also cuts discretionary spending to zero before an instalment is missed, so a household in shortfall has no planned cash purchase to substitute for.
- **Fix.** Define the shortfall in 2.3 (food and rent unpaid plus instalments due) and name the rollover. Acknowledge the tension with Submodel 2, or say the purchase is food.
- **Status.** B37 records "liquidity without a matching purchase", tested and disclosed. The definition gap is not recorded.

**M11. The literature misses the evidence needed to interpret RQ3.** *(judgement)*
- `01_introduction.tex:108-187`.
- **Problem.** The RQ3 result is a refusal-against-consumption trade-off. That is the subject of the credit-access literature, including a South African field experiment: Karlan and Zinman (2010, *Review of Financial Studies*), who find that marginal access to high-cost consumer credit improved applicants' outcomes. The payday-lending evidence (for example Morse 2011; Melzer 2011; Skiba and Tobacman) and the South African over-indebtedness literature (for example James 2014; Ssebagala, found by the B9 search) also bear on it. Without these the gap is "none of the reviewed studies" (01:195), which is weak, and Chapter 5 cannot place its sign against the empirical evidence.
- **Fix.** Add two to four sentences to "Empirical Evidence" and one sentence of interpretation in Chapter 5.
- **Status.** Not recorded (the B9 novelty search covered BNPL and agent-based models only).

**M12. Platform blindness frames RQ2 but is never tested.**
- `01_introduction.tex:88`: "When \ac{BNPL} platforms cannot observe one another's exposures".
- `04_results.tex:260-261`: "No arm gives platforms a shared view of exposure".
- **Problem.** The question's conditional suggests a comparison the thesis does not make. The RQ2 answer should say plainly that the model cannot estimate what the blindness costs.
- **Fix.** Add one sentence to the RQ2 answer and the conclusion, or drop the conditional clause from RQ2.
- **Status.** Recorded (B41(c)). Disclosed in 4.3 and 4.7.

**M13. The headline numbers cannot be traced from the text.**
- `04_results.tex:14-15`: "Pooled by precision over four seed blocks". The blocks are named only in a LaTeX comment.
- `04_results.tex:23-25`: "On ten replicates the rise at $\beta=0$ is 1.07 points, of which 0.94 ...". No seeds, no SE, and the source is a docs file.
- `03_calibration.tex:407`: "the pooled effect is $+0.11 \pm 0.07$". The pooling is not stated.
- **Problem.** These are the abstract's central numbers, and a reader cannot reproduce them from the text. It is also unclear why the four-block 1.03 ± 0.06, rather than the 250-replicate 1.05 ± 0.03, is the headline.
- **Fix.** Name the blocks, either in Table 3 or in the text. Give seeds and an SE for the decomposition. Say why the pooled figure is preferred.
- **Status.** Not recorded (B40 covers typed-in figures generally).

**M14. The variance decomposition is of levels, which the thesis says it does not interpret.**
- tab_sobol note: "they do not decompose the \ac{BNPL} effect".
- `03_calibration.tex:461-462`: "supports comparisons between arms ... better than statements about levels".
- **Problem.** The only global sensitivity analysis addresses the quantity the thesis disowns. It also leaves out persistence, friction and the placement rule. Section 4.6's opening ("Simulation noise moves default less than the main assumptions do") does not tell the reader this.
- **Fix.** Add one sentence in 4.6.
- **Status.** B45 (resolved) covers the noise only.

### LOW

**L1. Level confidence intervals in the figures hide paired differences.** Captions such as 05:34 ("error bars: 95\% confidence intervals over 100 replicates") describe intervals on levels. In fig_scenarios(a) the bureau-visibility interval overlaps the benchmark's, although the paired difference is 2.9 SE. The same applies to fig_stacking(c) and fig_access. **Fix:** say in each caption that the intervals are on levels and that the paired differences are in Table X. Not recorded.

**L2. "Pre-registered" overstates.** `appendix_b_register.tex:49`: "the top of the pre-registered sweep". The body says only "fixed the reporting rule before the runs" (04:58-59). **Fix:** use the body's wording. Related to B40(2).

**L3. The abstract credits the model with properties of the survey.** `main.tex:111`: "The model matches household size, income inequality and the order of magnitude of debt". These are properties of the survey sample, as 03:317-318 says ("tests the data"). **Fix:** "The constructed population matches". Not recorded.

**L4. Definitions drift.**
- "credit-active" is used in the abstract and at 01:97 before it is defined at 02:191-192.
- Default appears as "more than 90 days" (abstract), "91 or more days" (04:23; limitations row 1) and "98 days" (02:195). These are consistent on the tick grid, but one form should be used throughout.
- The "Distress" block of tab_baseline_arms includes "No liquid savings".
- "Traditional arrears, all households (\%)" (tab_baseline_arms:17), the Pattern 1 measure, is never defined: any age? the mean after burn-in?
- "detectably" is applied to Sobol indices (04:194), where no two-SE difference exists.
- The platforms' "light screen" and "mandatory screening" use one word for different things.

**L5. Results Chapter 5 does not discuss.** Screening's detectable −0.29 ± 0.14 in Q5 and +0.21 ± 0.08 in traditional lending at β = 0 (tab_scenarios:25, :18) go unmentioned. The multiple-comparison caveat at 05:50-51 covers only the bureau quintiles.

**L6. Results in the wrong section.** `03_calibration.tex:409-410`, "Bureau visibility raises their default by $0.19 \pm 0.07$ points", is an RQ3 result inside the RQ1 validation section.

**L7. Build log.**
- No undefined references or citations, no multiply-defined labels, no overfull boxes.
- About 17 "ignored error: Infinite glue shrinkage found in box being split" messages in the longtables of Appendices B to D (pp. 61-79 and 86). They are harmless but worth silencing.
- "Text page 40 contains only floats".
- Underfull hboxes at appendix_a:22-26 and appendix_e:80-89.
- Labels on starred subsubsections print the parent number: sec:results-effect and sec:results-robustness both print "4.6", and the sec:lit-* labels print "1.3". Acceptable, but the reader cannot tell the targets apart.
- Every float label is referenced at least once.

---

## Oral examination questions

1. **"Under your earlier default rule the BNPL effect was −0.10. Under the current rule it is +1.08, 0.94 of it from BNPL instalments reaching 98 days. Is the headline a finding or a definition?"**
   Partial defence: D18 and 2.3 justify the 90-day convention. The conflict with the benchmark bureau (H1, H2) is not addressed, and the earlier result is only in Appendix C.

2. **"In your benchmark the bureau does not record BNPL, yet a BNPL-triggered default is recorded, cuts off the bank and stops the household's traditional instalments. Why?"**
   No defence in the text.

3. **"Your 120 at-risk households default at 47% without BNPL, on 25-month bank loans, and at 85% with pay-in-four. What would the gap be at four years?"**
   Partial: the horizon argument is made for bureau visibility only (05:57-61), and 04:185 gives a blanket caveat.

4. **"Food and rent cannot be cut and income does not respond, so a household whose recorded income is below food and rent is insolvent every fortnight by construction. Is 'BNPL raises default' more than relabelling a consumption shortfall as a credit default? And 68% of these households' own income answer covers food and rent."**
   Partial: 3.5 discusses measurement and the conclusion's limits paragraph names further work. Incompressibility is never defended.

5. **"Peer-driven purchases are cut to cash at checkout and paid from a discretionary budget left after debts. Wasn't a flat β slope guaranteed?"**
   Partial: 04:71-72 says "consistent with".

6. **"Your ± 0.06 is Monte Carlo error on one draw. How much of the effect would survive a different resample of 109 source households, or NIDS sampling error?"**
   Disclosed (03:73-74), but not quantified.

7. **"Bureau visibility raises default because a refused household goes straight into arrears, a fitted persistence of 0.72 keeps it there whatever its cash, and the granted loans' arrears fall after tick 52. Why should a regulator read even the sign?"**
   Partial: 05:57-61. B41(a) and (b) were not run. Persistence is not discussed in this connection.

8. **"Name one validation check that could have gone against the model."**
   Defensible: 3.5 "What the Validation Supports" is candid, and debt service and default are named failures. The candidate should be ready to say that Pattern 1 follows from the payment order.

9. **"Your research question is about platforms not seeing one another. What does the model say about the cost of that blindness?"**
   Conceded: 4.3 and 4.7 say no arm tests it (B41(c)).

10. **"Karlan and Zinman found in South Africa that marginal access to expensive credit helped applicants. How does your result that refusal raises default and food shortfall relate to that literature?"**
    No defence: the literature is not cited.

---

## Overall judgement

The thesis has real strengths. It is unusually honest about the line between calibration and validation: "This agreement is by construction" and "The stable 90+ share is a ratio of two shrinking counts" are sentences most agent-based model theses never write. The experimental design is disciplined: paired seeds, stated power, a β test fixed before the runs, generated tables and a limitations index. The no-shortfall-BNPL arm is a good identification device.

The weakest point is the construct behind the headline. The 1.0-point effect comes from 120 model households whose recorded income is below food and rent that cannot be cut. It counts a 98-day BNPL arrear as default, with bureau consequences the benchmark's information structure rules out. It compares six-week with 25-month repayment inside a two-year window. A change of default rule turned it from −0.10 to +1.08, and the reader is told that only in an appendix. The thesis identifies who carries the effect but not why the model produces it. The abstract and introduction also drop qualifications the body is careful to keep, on routing, on β for the bureau result, on the measurement doubt about the 3.6% group, and on what the ± measures.

*Judgement:* as it stands, a sound pass that will draw corrections. Three text-only changes would most raise the mark:
1. A short "what the headline effect is" paragraph in 4.1, mirrored in the abstract and conclusion. It should cover the dependence on the default definition (with the −0.10 figure), the fact that the benchmark bureau records BNPL-triggered default, and the tenor and horizon reading, with the further-work runs named.
2. Bring the abstract, introduction and RQ answers into line with the body's qualifications (H4, M1, M2, M3, M5, M6), and reword RQ1 and RQ2 so that what the design answers by construction is marked as such.
3. Add the credit-access and payday-lending literature, including the South African field evidence, and use it in Chapter 5 to interpret the refusal-against-consumption trade-off.
