# Chapter 2 (Literature) — Review Findings and Fix List

Review date: 2026-08-18. Target file: `thesis/chapters/02_literature.tex` (1,252 words).
Reviewed against `01_introduction.tex`, `04_design.tex`, `main.bib`, and `main.log`.
Contestable citations were verified against source abstracts — evidence is recorded inline so
nothing needs re-checking tomorrow.

**Nothing has been edited yet.** This is the work list.

---

## Verdict

The chapter is competently sourced and §2.1 is genuinely well argued, but it currently reads as a
**justification narrative rather than a literature review**. Every paragraph takes the form
"X finds Y, therefore Z in my model." No source is appraised or criticised, no two sources disagree,
and no contrary hypothesis is entertained. Coverage is also misaligned with the research questions:
RQ1 and RQ3 have essentially no literature behind them. Four factual claims misstate their sources
(one with a number that does not appear in the source), and three claims contradict the model
actually built in Chapter 4.

Word budget: chapters 01–07 total ~9,877 words against a 10,000 limit. Ch2 is ~13% of the body.
About 150 of those words duplicate Chapter 1 verbatim — deleting them roughly funds the additions
below, so the chapter need not grow.

---

## Priority order (do these first)

1. **B1** — fabricated/misattributed Keys & Wang figure. Highest credibility risk if a marker checks.
2. **C1** (scheduled amortisation claim contradicts the model) and **B2** (Cardaci mischaracterised).
   Both are checkable in minutes.
3. **A1** — add an RQ3 paragraph to §2.4 (Woolard, FCA PS26/1, ASIC REP672). The intervention levers
   currently have no reviewed literature at all.
4. **A3** — add Granovetter, and state that beta has no empirical anchor.
5. Hedge **B3/B4/B5**, delete the Ch1 duplication, unify voice and spelling, fix the opening
   sentence and the Table 4 overflow.

Items 3–4 need roughly 200 words; deleting the §2.2 duplication frees about that much.

---

## A. Structural — coverage does not match the research questions

- [ ] **A1. RQ3 has no literature at all.** `04_design.tex:216` grounds mandatory affordability checks
  in `fca_ps26_1` and `woolard2021`; `asic2020rep672` sits unused in the bib. None appears in Ch2.
  RQ3 asks which platform-level interventions curb the increase — the international
  regulatory-response literature *is* the literature for that question, and §2.4 is purely domestic.
  A reader meets the Woolard Review for the first time as a parenthetical citation in Submodel 15.
  **Largest single gap.**

- [ ] **A2. RQ1 has no literature either.** RQ1 is a validation question (can the population reproduce
  behaviour it was not fitted to). That is pattern-oriented modelling, with its own methodological
  literature — Grimm et al.; Windrum, Fagiolo & Moneta on empirical ABM validation. Ch4 leans on ODD
  throughout; Ch2 never discusses how credit ABMs are validated, only that Madeira did it. RQ1 is a
  precondition for RQ2/RQ3 by the introduction's own framing (`01_introduction.tex:53`), so this is
  load-bearing.

- [ ] **A3. RQ2's peer mechanism is under-grounded.** `granovetter1978threshold` is described in the bib
  note as what "anchors the D17 peer-influence mechanism", and `04_design.tex:198` says the
  specification "maps directly to Granovetter's threshold models" — yet Granovetter never appears in
  Ch2. Ackert et al. alone cannot carry it: they establish a *preference* for BNPL mediated by
  perceived social approval; §2.2 escalates this to "social approval directly drives up indebtedness",
  which is not their result. Also state plainly that **no source gives an empirical magnitude for
  beta** — that absence is the reason beta is swept and the beta=0 arm is mandatory. Saying so turns a
  weakness into a methodological justification.

- [ ] **A4. One-sidedness — the counter-hypothesis is never stated.** Pattern 1 (`04_design.tex:23`) is
  "Complementarity, *not* substitution", a falsifiable claim. The substitution hypothesis (BNPL as a
  cheaper alternative to revolving credit, overdraft or payday lending) is never named or reviewed.
  Reviewing it and showing the evidence favours complementarity makes Pattern 1 a genuine test;
  assuming it reads as confirmation bias. Di Maggio, Williams & Katz is a conspicuous absence.

- [ ] **A5. External validity is the central threat and is never confronted.** Every behavioural and
  empirical source is US or UK; the thesis is about South Africa. §2.5 frames the gap as *regulatory*,
  but the deeper question is whether US present-bias and anchoring parameters transfer to a population
  where a large share of income is grant-based. Note also that Cardaci's household debt is
  **collateralised** (mortgages, home equity) — structurally unlike unsecured pay-in-4 — which the
  chapter does not flag.

- [ ] **A6. No chapter introduction, no scope statement.** The chapter opens straight into §2.1 with no
  orientation and never states how the literature was selected. Feeds directly into A7.

- [ ] **A7. The gap table asserts a universal negative.** "None incorporate a shadow lender class that
  bypasses both affordability checks and bureau visibility" — from a four-paper sample, with no stated
  search strategy. Hedge to "to the author's knowledge", or state the search.

---

## B. Factual and citation accuracy (verified against sources)

- [ ] **B1. The Keys & Wang figure is wrong in both number and denominator.** Line 47 says "at least 22%
  of these near-minimum payers adjust their payments whenever the minimum formula changes."
  **Verified:** the published finding is that **9–20% of *all accounts*** respond more to formula
  changes than liquidity constraints alone predict, as a lower bound on anchoring. The 22% does not
  appear in the abstract, and the base is all accounts, not near-minimum payers. Rebasing 9–20% onto
  the 29% near-minimum group would give roughly 31–69%, so the error is not conservative.
  Check the JFE published version and correct. Source: NBER w22742 / JFE 131(3) 528–548.

- [ ] **B2. Cardaci is mischaracterised.** Lines 10–13 claim the link "runs through the structure of that
  network rather than through aggregate leverage." **Verified:** that is not his finding. The chain is
  inequality → expenditure cascades → collateralised household debt → defaults → bad debt →
  credit crunch → recession; the comparative statics are across credit-market conditions and
  consumption emulation, not network topology. The sentence names expenditure cascades and then
  attributes the result to network structure — internally inconsistent as well as inaccurate.

- [ ] **B3. deHaan et al. is overstated twice.** "Demonstrate that BNPL adoption exacerbates financial
  distress", and especially "their conclusion, that BNPL **inherently** facilitates overborrowing."
  **Verified:** they use an instrument on pre-BNPL shopping habits to *bolster* causal inference, and
  the result is that new users experience rapid increases in overdraft and credit-card charges
  relative to non-users, concentrated among the liquidity-constrained. "Inherently" is our word, not
  theirs. Use "find" and drop "inherently."

- [ ] **B4. Hamill is another ABM being used as an empirical validation target.** Lines 30–31 call the
  non-monotonic income–DTI relationship "an independent validation target". `04_design.tex:25` is more
  honest ("in independent modelling"); Ch2 is not. Model-to-model agreement is a consistency check,
  not external validation, and presenting it otherwise weakens the RQ1 claim that rests on
  out-of-sample patterns. Either locate the empirical source for the non-monotonic profile, or
  relabel Pattern 3 explicitly as a cross-model check.

- [ ] **B5. The TransUnion 20% is intention-to-apply, used as revealed demand.** Line 56 says it
  "provides the baseline for simulating local demand". A stated-intention statistic is not an adoption
  rate; acknowledge the gap rather than silently bridging it.

- [ ] **B6. Two citations dropped with no exposition.** "We know this distress is heavily concentrated in
  LMI populations \cite{hayashi2025constraints, wang2026buynow}" — neither source is described, and
  `wang2026buynow` is a non-peer-reviewed Fed Richmond brief dated four months before submission.
  "We know" is doing work the text does not.

---

## C. Claims contradicted by our own model

- [ ] **C1. "Scheduled amortisation is rejected as a repayment rule in this model" (line 49) is false.**
  `04_design.tex:155` sets minimum-payer share at 0.29, meaning **71% of agents are scheduled-payers**,
  and Pay-in-4 (line 171) is fixed exogenous amortisation. What was actually rejected is *universal*
  scheduled amortisation. As written, a reader who checks Ch4 finds the literature review describing a
  different model.

- [ ] **C2. "Naturally varies in how strongly it does both" (line 49) overstates the implementation.**
  `04_design.tex:58` gives each household a **fixed binary archetype**, not continuous heterogeneity
  in bias strength.

- [ ] **C3. §2.5 contradicts §2.4.** "Since administrative data is fundamentally blind to BNPL, empirical
  measurement is impossible" — yet §2.4 cites South African survey evidence measuring BNPL uptake. The
  claim is also too absolute; "not measurable from administrative data" is both true and sufficient.

---

## D. Table 4 (`tab:gap`)

- [ ] **D1. It overflows the text block.** `main.log` records
  `Overfull \hbox (16.08444pt too wide) in paragraph at lines 67--82` inside `02_literature.tex` —
  that is the tabular exactly. Columns sum to 14 cm against a 14.7 cm measure (textwidth 418.25pt)
  before `\tabcolsep`; the table currently runs ~5.7 mm into the margin.

- [ ] **D2. The table's citations do not match the body.** `nortonrose_bnpl_sa` appears in row 4 but is
  never cited in Ch2's prose — its first appearance in the chapter is inside a summary table, which is
  backwards. Conversely `sa_nca_2005` and `sa_ncr_ratecaps_2016` are discussed at length in §2.4 but
  absent from that row, and `hayashi2025constraints` / `wang2026buynow` are missing from the Empirical
  BNPL row.

- [ ] **D3. Row 2's "leaves open" is a category error.** Faulting behavioural economics because it
  "cannot explain how these individual biases aggregate into systemic market failure" criticises a
  field for not being agent-based modelling. Reframe as what our model *adds* (an aggregation
  mechanism), not what they failed to do.

---

## E. Prose, register and consistency

- [ ] **The first sentence is ungrammatical.** "Distress at the level of a population is more than the sum
  of distress at the level of a household, which is the case for modelling it from the bottom up."
  Presumably meant "which is the *argument* for". Worst possible location for a broken sentence.
- [ ] **Line 38:** "what appears like an benign, interest-free deferral" — "an benign", and "appears like"
  should be "appears to be".
- [ ] **Comma splices:** lines 13–14 ("reach a similar conclusion from a different direction, unsustainable
  debt emerging from local rules"); line 40's "but" signals a contrast that is not there.
- [ ] **Voice is inconsistent.** §2.1, §2.3, §2.4 are impersonal; §2.2 and §2.5 switch to first person
  ("We know this distress...", "If we cannot observe this... we must simulate..."). Pick one.
- [ ] **Spelling is inconsistent.** §2.2 uses US forms ("modeled", "behavioral"); the rest of the chapter
  and thesis use UK forms ("modelling", "behavioural").
- [ ] **Four different self-referents** in one chapter: "this thesis", "this paper", "this model", "this
  study". For a mini-dissertation "this paper" (line 40) is wrong regardless.
- [ ] **Register drops noticeably in §2.2 and §2.5**: "help explain the demand side", "the complete picture
  of the puzzle", "where the reviewed research stops", "the actual impact". §2.1 is written at a
  visibly higher level — they read as different authors.
- [ ] **Filler connectives**: "Crucially,", "Furthermore,", "Because of this,", "The exact same logic".
- [ ] **Two of five subsections open by leaning on Ch1** ("As established...", "Building on the regulatory
  exemptions... discussed earlier"). A literature chapter should stand on its own.
- [ ] **~150 words duplicate Chapter 1** — deHaan's 10.6 million consumers and the CFPB 63%/32% appear in
  both, near-verbatim. Cheapest available saving under the word limit.
- [ ] **Formatting:** §2.1/§2.3/§2.4 are hard-wrapped at ~100 characters; §2.2 and §2.5 are single long
  lines with trailing whitespace. Cosmetic, but it makes diffs noisy.

---

## F. What works — keep this

- **§2.1 is the strongest writing in the chapter.** Each ABM is tied to a specific modelling decision
  rather than merely summarised, and the closing argument — that a household holding obligations to
  mutually blind lenders exists only on an individual balance sheet and cannot be expressed by a
  representative agent — is exactly the right justification, correctly made.
- **Mapping Madeira's minimum-consumption default condition onto the Regulation 23A residual-income
  test** is genuinely elegant. It makes a foreign modelling choice locally necessary rather than
  merely convenient.
- **The gap table is the right instrument** under a word limit — it does in ~200 words what would
  otherwise take 600.
- **§2.4 derives a design decision from the legal position** (bureau visibility as a switchable lever
  rather than a constant), which is precisely what a literature review inside a modelling thesis
  should produce.
- Sourcing is current and real; there is no padding anywhere in the chapter.

---

## Sources used for verification

- Keys & Wang, NBER w22742 — https://www.nber.org/papers/w22742
- Keys & Wang, JFE 131(3) — https://www.sciencedirect.com/science/article/abs/pii/S0304405X18302721
- Cardaci, JEBO 149 — https://www.sciencedirect.com/science/article/abs/pii/S0167268118300106
- deHaan et al., Management Science 70(8) — https://pubsonline.informs.org/doi/10.1287/mnsc.2022.03266
- CFPB, Consumer Use of BNPL, Jan 2025 — https://files.consumerfinance.gov/f/documents/cfpb_BNPL_Report_2025_01.pdf
