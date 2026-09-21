# SCOPE REDUCTION — fitting the thesis into 10,000 words

**18 August 2026.** The word limit has moved from 16,000 to 10,000. This document sets out what
survives, what goes, what has to be decided, and what the reduction costs us.

Companion to [`DECISIONS.md`](DECISIONS.md) (what was chosen and why),
[`DEFECTS.md`](DEFECTS.md) (what is wrong) and [`PLAN.md`](PLAN.md) (what happens next).

---

## STATUS: executed 18 August 2026

All six decisions in §8 are settled, and the reduction has been carried out. The document compiles
clean (39 pages, zero LaTeX warnings, every reference and citation resolving).

| Decision | Answer |
| --- | --- |
| D1 appendices / bibliography | **Excluded**, prose included. Only body prose counts. Tables and figures are free everywhere |
| D2 RQ sign-off | **Not required** — the questions could be changed freely |
| D3 negative RQ2 result | **Acceptable**, and reported prominently |
| D4 validation targets | **Reduce prominence** — foreground the two strong ones, demote the two weak ones to a table |
| D5 cap the shortfall borrowing path | **Yes** — still to do, bundled with the final run |
| D6 final run | **Deferred** until after the write-up reduction |

**Structure changed from chapters to sections.** The document class is now `article`: what were
chapters are `\section`, and everything below shifted one level. File names are unchanged.

**Current position.**

| Section | Prose | Target |
| --- | ---: | ---: |
| 1 Introduction | 653 | 700 |
| 2 Literature and Gap | 1,011 | 1,000 |
| 3 The Household Population | 1,348 | 1,400 |
| 4 Model Design and Implementation | 1,700 | 1,750 |
| 5 Results | *skeleton* | 3,300 |
| 6 Discussion and Limitations | 943 | 850 |
| 7 Conclusion | *skeleton* | 650 |
| **Body written** | **5,913** | |
| **Projected at submission** | **9,605** | 10,000 |

395 words of slack. Appendix prose stands at 1,277 words and does not count.

**Still open:** write the Results and Conclusion sections against the final run (D5 and D6 first);
populate the parameter register from `simulation/config.py`; write the abstract last.
`OVERVIEW.md` and `THESIS_GUIDE.md` still describe the old research questions in depth and need a
proper pass — only their headline statements have been corrected so far.

---

## 1. The arithmetic

**Tables and figures do not count against the limit.** Every number below is prose only, LaTeX
comments stripped, tables counted separately — so these are the binding figures. This exclusion is
the most important fact in the whole plan and §5 builds the strategy around it.

| Chapter | Prose now | Tables | Status |
| --- | ---: | ---: | --- |
| 1 Introduction | 1,013 | — | written |
| 2 Literature | 1,780 | — | written |
| 3 Data | 1,645 | 379 | written |
| 4 Design | 2,630 | 1,079 | written |
| 5 Implementation | 22 | — | skeleton, targets 2,000 |
| 6 Results | 37 | — | skeleton, targets 6,000 |
| 7 Limitations | 1,169 | — | written |
| 8 Conclusions | 373 | — | skeleton, targets 1,500 |
| **Body total** | **8,669** | **1,458** | |
| Appendix A rationale | 725 | — | written |
| Appendix B register | 135 | — | skeleton |

**Written prose is already 87% of the limit.** Finished at the targets the guide sets, the body
lands at roughly **17,700 words against 10,000**. About 44% of the planned thesis has to go.

The redeeming feature: **9,463 words of the overage is in chapters that do not yet exist.** Most of
the reduction is a decision not to write, not a rewrite. The written chapters still have to fall
from 8,237 to about 5,650, which is −31%.

**Nothing in `simulation/` changes.** The results exist. This is entirely a write-up reduction.

---

## 2. What the paper does well — protect these

Ranked by how much they would cost to lose.

1. **The mechanism is documented, not invented.** BNPL levies no interest, so it argues it falls
   outside the NCA, so it does not register, does not run the Regulation 23A test, and reports
   nothing to any bureau. Norton Rose states the legal position; TransUnion confirms from inside
   the bureau system that BNPL is absent from South African credit reports. A compliant lender
   therefore runs a lawful affordability test against a liability record that is incomplete *by
   regulatory construction*. This is the single best asset in the thesis and every word spent on it
   earns its place.

2. **Every agent is a real household.** 5,000 agents carried from NIDS Wave 5, one reference year
   throughout (2017 Rands), no inflation forwarding, no second monetary vintage. Fourteen checks
   pass. The population is a reusable artefact independent of the model.

3. **The patterns were registered before the results.** ODD's second update used as intended. And
   it was honoured: the pre-registered non-linearity hypothesis for RQ2 was **falsified and is
   reported as falsified**, under two structurally distinct social mechanisms. Examiners reward
   this heavily and it is unusual to see it done properly.

4. **The β = 0 control arm.** Makes the peer-influence claim non-circular. Structurally the
   sharpest decision in the design, and it must survive any cut.

5. **A surprising, policy-relevant headline.** The three interventions regulators actually propose
   — bureau visibility, mandatory affordability check, cool-off — do almost nothing. The one that
   works, a cap on concurrent facilities, is proposed nowhere. The damage is not any single
   unaffordable loan; it is holding several at once, and only the cap touches that.

6. **Convergent validation with nothing tuned.** Average BNPL purchase: R992 from Weaver's
   disclosed GMV ÷ transactions, R1,038 from trade press, R1,029 from the model whose scale comes
   from the expenditure survey alone. Three independent sources within 5%. Cheap in words, very
   strong in effect.

7. **The 60+ day arrears band.** 15.38% against the regulator's 16.54%, never fitted. Two
   parameters were tuned to two *other* bands and this one came out close by itself.

8. **The limitations chapter is genuinely self-critical** — calibrated-not-validated, the
   account-versus-household unit mismatch, pattern 1's partial circularity. Keep the honesty, cut
   the length.

---

## 3. The literature that must stay

A citation is core if removing it removes something load-bearing.

### Tier 1 — cannot be removed without breaking the thesis (11)

| Source | What it carries |
| --- | --- |
| `sa_nca_2005` + `sa_ncr_affordability_2015` | The Regulation 23A residual-income test **is** the credit-granting gate |
| `nortonrose_bnpl_sa` | The legal claim that BNPL sits outside the NCA — the entire mechanism |
| `transunion_cps_sa_2025` | Bureau confirmation BNPL is absent from SA credit reports; also a validation target |
| `ncr_ccmr_2017` | The calibration target. No baseline without it |
| `madeira2018chile` | Cash-flow insolvency default condition, plus precedent for a middle-income household credit ABM held to external targets |
| `dehaan2024bnpl` | The phenomenon, and validation pattern 1 |
| `cfpb2025bnpl` | The 63% / 32% stacking shares — the RQ2 comparator |
| `Keys2019` | The 0.29 minimum-payer share is an actual model parameter |
| `ackert2025bnpl` | Licenses the want-driven path and the social mechanism |
| `grimm2020odd` | The specification protocol whose purpose-and-patterns element we use |
| `cardaci2018inequality` | Methodological premise for a bottom-up household credit ABM; reference-group precedent |

### Tier 2 — keep, one sentence each (7)

`granovetter1978threshold` (the pre-registered threshold variant was actually run — load-bearing for
the negative result) · `woolard2021` + `fca_ps26_1` (real-world provenance of levers 2 and 3, and
the λ anchor; RQ3 is ungrounded without them) · `payflex_terms` (Pay-in-4 mechanics, order cap,
late fee) · `weaver2025results` + `statssa_ies_2023` (the convergent purchase-size validation) ·
`sa_ncr_ratecaps_2016` (statutory maxima used to build servicing) · `hamill2023creditcard`
(validation pattern 3) · `dorazio2017micro` (one sentence: credit answers a *realised* shortfall,
which is what fixes the step ordering).

### Tier 3 — demote to the appendix register or drop (12)

`yun2020housing` (drop) · `hayashi2025constraints`, `wang2026buynow`, `cfpb2025market` (compress to
one grouped cite or drop) · `Kuchler2021`, `meier2010present` (keep as a single grouped cite in one
sentence) · `comer2013activation`, `alizadeh2015activation` (appendix, with the activation-order
check) · `asic2020rep672`, `homechoice2024ir`, `payjustnow_terms`, `payflex_limits`,
`payjustnow_limits`, `sa_bnpl_basket_2026`, `statssa_lmd_2022`, `statssa_cpi` (parameter register) ·
`ncr_ccmr_2025` (drop — 2017 is the vintage).

Nothing needs deleting from `main.bib`; uncited entries do not print.

### Two citation gaps to fix

- **NIDS Wave 5 has no bibliography entry at all.** The backbone dataset of the entire thesis is
  uncited. Must be added.
- The Gini benchmark in §3.6 is attributed to "the World Bank and Statistics South Africa" with no
  citation. Must be added or the claim dropped.

---

## 4. The research questions

The current set asks three questions the results answer awkwardly. The proposed set asks three the
results answer directly, and converts the data layer from overhead into a contribution.

### Proposed

> **Primary.** How does the exemption of BNPL from South Africa's credit-reporting and
> affordability regime affect credit distress among LMI households, and which platform-level
> interventions reduce it?

**RQ1 — Can a synthetic household population built from South African survey microdata reproduce
credit-market behaviour it was not fitted to?**

Answered by Chapter 3 plus the baseline. Yes, on four of five independent checks: 60+ day arrears
15.38% vs 16.54% (never fitted), average BNPL purchase R893 vs R992 from an independent source,
debt-to-income peaks mid-distribution, stacking 15–39% vs 32%. No on one: zero savings 45% vs 36%,
resting on the weakest variable in the dataset.

**RQ2 — Do households accumulate concurrent BNPL facilities that no lender observes in aggregate,
and does that raise population default?**

Yes. Stacking is emergent, not programmed. Default 24.2% → 27.2%, and 29.1% with strong peer
influence. The increase is **smooth in access, not a threshold** — the pre-registered non-linearity
hypothesis is falsified under both the linear peer rule and the Granovetter threshold variant.

**RQ3 — Which platform-level interventions curb the increase?**

Bureau visibility ≈1%. Mandatory affordability check ≈0. Cool-off: nothing alone, −33% where peer
influence is present. Concurrent-facility cap: −54% to −63%, with default returning nearly to the
no-BNPL level.

### Why this is better

- RQ1 is answered by work already done and validated. Chapter 3 stops being setup and becomes a
  third of the contribution.
- The old RQ1 ("under what conditions does stacking become self-reinforcing") had no interesting
  answer, because no threshold exists. The new RQ2 absorbs it as a paragraph.
- The old RQ2 made the *negative* result the headline answer to a headline question. Under the new
  set the positive finding leads and the negative is reported as a named sub-finding with its
  structural explanation — which is honest and reads far better.
- RQ3 is essentially unchanged and holds the strongest, most novel result.

### Sharpening RQ1

Do **not** phrase it as "can we build a representative population" — that is a task with a
near-certain yes, and an examiner will say so. The version above is falsifiable: it could have
returned no, and on one check it does.

---

## 5. Target structure and budget

Merge Design and Implementation; fold Limitations into a Discussion chapter. Seven chapters.

| New chapter | From | Target | Now | Δ |
| --- | --- | ---: | ---: | ---: |
| 1 Introduction | 01 | 700 | 1,013 | −313 |
| 2 Literature and Gap | 02 | 1,000 | 1,780 | −780 |
| 3 The Household Population (RQ1) | 03 | 1,350 | 1,645 | −295 |
| 4 Model and Implementation | 04 + 05 | 1,500 | 2,652 | −1,152 |
| 5 Results (RQ2, RQ3) | 06 | 3,300 | 37 | +3,263 |
| 6 Discussion and Limitations | 07 | 800 | 1,169 | −369 |
| 7 Conclusion | 08 | 650 | 373 | +277 |
| **Body prose** | | **9,300** | 8,669 | |

700 words of slack, which the results chapter will need.

### Tables are free — this is the main tool

Since tables carry no cost, **the reduction is primarily a conversion exercise, not a deletion
one.** The rule of thumb: *anything that is a list of parallel items each with a value and a source
should be a table, not prose.* This changes several earlier assumptions for the better.

| Content | Old plan | Revised |
| --- | --- | --- |
| Submodel specification (17 rows) | demote to appendix | **stays in the body, free.** ODD completeness is preserved |
| ODD design-concepts (11 rows) | demote to appendix | **stays in the body, free** |
| Appendix A design rationale, 725 words | delete or reduce | **convert to a table** — survives at ~zero cost |
| Appendix B parameter register | table | unchanged, free |
| Validation scorecard, independent checks, intervention ranking | body tables | unchanged, free |
| Limitations 6–12 | delete from body | **convert to a caveat table** — nothing is lost |
| Results numbers | prose walkthrough | **tables plus short interpretive prose.** Report the number in the table; spend prose only on what it means |

The last row is the largest single saving in the thesis. A results chapter that tabulates its
numbers and reserves prose for interpretation runs at roughly half the length of one that narrates
them, and reads better.

**Figures: five in the body, not nine.** Baseline arrears profile · stacking depth ·
default-vs-access surface (carries the negative result) · intervention ranking · robustness
tornado. The others go to the appendix — they are free either way, but a body with nine figures in
9,300 words of prose reads as padded.

**Experiments demoted to the appendix:** Sobol indices, activation-order re-runs, population-size
stability, minimum-payer sweep, the full 1–6 platform-count detail (report endpoints only), and one
of the two `rq3_interventions` figures. Demoted as *tables*, so the evidence survives in full.

---

## 6. Files we will touch

| File | Action |
| --- | --- |
| `thesis/main.tex` | Drop `05_implementation` from the `\input` list; rename 07/08; write the abstract last |
| `chapters/01_introduction.tex` | New RQs. Delete §Research Outcomes (duplicates objectives). Cut objectives to three or delete. Cut §Methodology to ~90 words. Trim the regulatory detail that Ch2 §2.4 repeats |
| `chapters/02_literature.tex` | Drop Yun & Moon. Delete the closing paragraph of §2.1 (forward-describes the model — Ch4's job) and of §2.3 (duplicates §lim-transfer). Compress Hayashi & Wang to one sentence |
| `chapters/03_data.tex` | Becomes the RQ1 chapter. Design-principles list → two sentences. Drop FinScope question codes. 53-household diagnostic → one clause. **Receives** the four registered patterns and the CCMR table from Ch4. Add the RQ1 answer |
| `chapters/04_design.tex` | Absorbs Ch5 (~300 words). **Both tables stay** — they are free. Cut the surrounding prose hard: keep submodels 10, 11, 13, 15 in prose; fold 9 into 10; move 17 into the table row only. Patterns move out to Ch3 |
| `chapters/05_implementation.tex` | **Delete as a chapter.** Verification and protocol become a table in Ch4; ~300 words of prose survive |
| `chapters/06_results.tex` | Rewrite from skeleton to 3,300 words against `results/summary/*.csv` and STATUS.md. One section per RQ. **Numbers in tables, prose for interpretation only** |
| `chapters/07_limitations.tex` | Becomes Discussion and Limitations. Five limitations in prose; the other seven become a caveat table |
| `chapters/08_conclusions.tex` | Write to 650. Future-work list five items → three |
| `chapters/appendix_a_rationale.tex` | **Convert the six rejected-alternative arguments to a table** (choice · alternative · why rejected · source). Survives at near-zero cost |
| `chapters/appendix_b_specification.tex` | Populate **generated from `simulation/config.py`**, not typed |
| `chapters/appendix_c_results.tex` | **New.** Demoted sensitivity evidence as tables: Sobol, activation order, population-size stability, minimum-payer sweep, full platform-count detail |
| `thesis/main.bib` | Add NIDS Wave 5. Add the Gini benchmark source |
| `THESIS_GUIDE.md` | Line 674 still says 16,000. Update, and update the three decisions requested |
| `OVERVIEW.md`, `STATUS.md` | Update the RQ statement so the working docs do not contradict the thesis |
| `scratchpad/DECISIONS.md` | Log the RQ change and the scope decision |

---

## 7. Where the cuts come from, ranked

| # | Cut | Words | Cost |
| --- | --- | ---: | --- |
| 1 | Write Results to 3,300, not 6,000 — numbers in tables, prose for interpretation | 2,700 | Planning only. **No evidence is lost**, because the tables are free |
| 2 | Ch5 never written as a standalone chapter | 1,700 | Implementation detail compresses to ~300 words plus a verification table |
| 3 | Ch4 prose: concepts, entities, scheduling, submodels 9/17 | 1,150 | Some design defence thins, but the submodel table stays in the body so the specification survives intact |
| 4 | Conclusions to 650, not 1,500 | 850 | Less room to qualify findings |
| 5 | Ch2 duplication and marginal papers | 780 | Two ABM papers and two corroborating BNPL papers go |
| 6 | Ch1 duplication with Ch2 and Ch3 | 525 | None — this is pure redundancy |
| 7 | Ch3 construction detail | 440 | Reproducibility from the document alone weakens slightly |
| 8 | Ch7 twelve limitations → five in prose, seven in a table | 370 | None — the caveats survive as a table |
| 9 | Appendix A prose → table | 700 | None — the argument survives in tabular form |

Items 1, 8 and 9 are conversions rather than deletions: about 3,770 words leave the count without
any evidence leaving the thesis. That is what makes 10,000 achievable without gutting the work.

---

## 8. Decisions required

**D1 — Does the 10,000 include appendix *prose* and the bibliography?**
Tables and figures are confirmed excluded, which removes most of the force of this question: nearly
everything being demoted is tabular. What remains open is whether appendix *prose* counts. Under
this plan the appendices are almost entirely tables, so even a strict answer costs perhaps 200–300
words. Confirm it, but it no longer gates the design of the thesis.

**D2 — Do the research questions need supervisor or departmental sign-off to change?**
If they were formally registered, the restructure in §4 needs approval before any rewriting starts.
This gates everything.

**D3 — Is the negative RQ2 result acceptable, and how prominently is it reported?**
Recommendation: name it in the abstract and as a titled finding under RQ2. A pre-registered
hypothesis that quietly disappears would damage the one thing this thesis has most of.

**D4 — May the four validation targets be reduced in prominence?**
Recommendation: yes. Foreground the two strong independent ones (60+ arrears, purchase size);
demote the two weak ones (zero savings, DTI shape) to the appendix with a one-line summary each.

**D5 — Do we still cap the shortfall borrowing path before the final run?**
It is the largest remaining sensitivity (4.11pp) and the rule has no citation. Recommendation:
yes — it is a small change and it is cheaper than defending the sensitivity in prose we no longer
have room for.

**D6 — Final run at 20 replicates?** Cheap compute, and the 0.33pp noise floor gets tighter.
Recommendation: yes, before the results chapter is written.

---

## 9. What this costs us

Stated plainly, because these are real.

1. **The prose defence of the design thins, though the specification survives.** The submodel and
   ODD tables stay in the body, so the model remains reproducible from the document. What goes is
   the surrounding argument — the paragraphs explaining *why* each rule was chosen. Appendix A in
   tabular form partly covers this, but a reader who wants the reasoning gets a table row instead
   of a paragraph.

2. **The feedback-loop decomposition is abandoned.** The old RQ1 asked which of the financial and
   social loops drives the increase. Under the new RQ2 we can still say it via β = 0 versus β > 0,
   but with less analysis behind it.

3. **RQ1 is a methods contribution.** Some examiners rank a population-construction result below a
   substantive finding. Mitigated by the fact that the population is genuinely reusable
   independently of the model, and by phrasing RQ1 so it could have failed.

4. **The negative result loses headline status.** Honest only if D3 is honoured. This is the sharpest
   risk in the plan.

5. **RQ2 bundles two questions.** "Do they stack" and "does default rise" can diverge — and partly
   do: the credit limit binds on 54% of requests but barely moves default, because a constrained
   household borrows less per purchase rather than defaulting less. Both facts have to be reported
   together or it reads as a contradiction.

6. **Thinner robustness *prose* in the body.** One tornado figure plus a table carries what was
   going to be a full sensitivity section. The evidence survives; the interpretation of it does not.
   More exposure in the viva.

7. **Seven limitations become table rows.** Nothing is lost factually, but a caveat argued in a
   paragraph lands differently from one stated in a cell. Choose the five that stay in prose on the
   basis of which ones actually bound the claims — calibration, the uncited amount rule, the US
   parameter transfer, the absence of contagion, and the weak-input/unit-mismatch pair.

8. **A table-heavy thesis can read as thin.** The conversion strategy is sound, but nine body
   figures and a dozen tables against 9,300 words of prose invites the criticism that the argument
   is carried by exhibits. Hence five figures, and prose that interprets rather than restates.

---

## 10. Sequence

Order matters; step 1 gates everything else.

1. **Settle D2 with the supervisor** — the RQ sign-off. D1 is now minor but worth confirming in the
   same conversation.
2. Rewrite the RQs in `01_introduction.tex`; propagate to `OVERVIEW.md`, `STATUS.md`,
   `THESIS_GUIDE.md`, `DECISIONS.md`. One statement, four places, no drift.
3. D5 and D6: cap the shortfall path, final run at 20 replicates. Compute runs while prose is cut.
4. Cut Ch1, Ch2, Ch3, Ch4 to budget. Create Appendix C and move the tables. Delete Ch5.
5. Write Ch5 Results to 3,300 against the final numbers — once, not iteratively.
6. Cut Ch7 to five limitations; write Ch7 Conclusion.
7. Write the abstract last. Name the negative result in it.
8. Full recount before submission, by the same method used in §1.
