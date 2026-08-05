# Thesis Issue Register

Defect and shortfall register for the mini-thesis, raised in the full-document review of
**2026-08-05**. This file is the record; fixes are tracked here, not in commit messages.

Companion to [`../OVERVIEW.md`](../OVERVIEW.md) (strategy) and
[`decision.md`](decision.md) (design rationale). Where an issue changes a design decision,
close it *here* and propagate to those files.

**Line references** are against `thesis/main.tex` as at commit `47e57d0`. They will drift once
the restructure (D1) lands; re-anchor at that point.

## Legend

| Field | Values |
| --- | --- |
| **Severity** | `BLOCKER` cannot submit · `MAJOR` examiner will challenge it · `MINOR` polish |
| **Owner** | `MARC` researcher judgement, supervisor, or external work · `AGENT` executable in-repo · `BOTH` |
| **Status** | `OPEN` · `IN PROGRESS` · `CLOSED` · `WONTFIX` (with reason) |

## Standing at a glance

| Group | Count | Open | Closed | Blockers open |
| --- | --- | --- | --- | --- |
| A. Completeness | 5 | 3 | 2 | 3 |
| B. Substantive / methodological | 12 | 5 | 7 | 0 |
| C. Evidence and citation | 7 | 3 | 4 | 0 |
| D. Mechanical and structural | 6 | 1 | 5 | 0 |
| E. Writing register | 5 | 0 | 5 | 0 |
| F. Length and condensation | 5 | 0 | 5 | 0 |
| G. Record-keeping hygiene | 3 | 0 | 3 | 0 |
| **Total** | **43** | **12** | **31** | **3** |

Word count at review: **6,265** words of body prose, 24 typeset pages.
Distribution: Literature Review 1,580 · ABM Design 4,569 · everything else 116.

---

## Resolution log — 2026-08-05 document pass

The document was restructured into `thesis/main.tex` plus `thesis/chapters/*.tex`. Line
references in the entries below are against the pre-restructure `main.tex` and no longer resolve;
each entry names its new home instead.

**Word count now: 10,519 body + 791 appendix, 57 typeset pages.** Build is clean --- zero
undefined references, zero undefined citations, zero acronym warnings (was two), zero overfull
boxes.

| Chapter | Words | Status |
| --- | ---: | --- |
| 1. Introduction | 1,365 | written |
| 2. Literature Review | 1,622 | ported, humanised |
| 3. Data and Population Construction | 1,803 | **new** |
| 4. Model Design (ODD) | 3,588 | condensed from 4,569, now includes 2 tables |
| 5. Implementation | 0 | skeleton, waits on the model |
| 6. Results and Analysis | 0 | skeleton, waits on the model |
| 7. Limitations | 1,822 | **new** |
| 8. Conclusions and Future Work | 319 | skeleton; Future Work written |
| App A. Design Rationale | 693 | **new**, holds the rejected alternatives |
| App B. Parameter Register | 98 | skeleton, generate from config |

**Closed:** A3, A4 · B1, B2, B4, B5, B6, B11, B12 · C1, C2, C4, C5, C7 · D1, D2, D3, D4, D6
(partial: tables added, figures still needed) · E1, E2, E3, E4, E5 · F1, F2, F3, F4, F5 ·
G1, G2, G3.

**Style counters:** "rather than" 45 → **6**. Antithesis constructions ("X is not Y") 20+ → **4**,
each retained deliberately where the contrast carries the claim (E5).

**Still open and owned by Marc:** A1 (partial --- Chapters 5, 6, 8 need results), A2, A5,
B3, B7, B8, B9, B10 · C3, C6 · D5 (three TODOs remain live in the source, mapped to B7, B9, B10).

**New item raised during the pass:**

### B13 · `p4_validation.ipynb` renders check D under two labels — `MINOR` · `MARC` · `OPEN`

An older cell output labels it "DSTI bounded / households repay\textgreater income / 0 / exact";
the current narrative labels it "Servicing plausible pre-guard" and reports the non-circular
guard-binding test at 3.4\% of debtors. The thesis uses the latter. Clear the stale output and
re-run the notebook top to bottom so the scorecard is unambiguous. A TODO is parked at the
scorecard table in `03_data.tex`.

### B14 · Two different Gini figures circulate in the project — `MINOR` · `AGENT` · `CLOSED`

`OVERVIEW.md` reports 0.651 and `p3_resample_summary.json` reports 0.671, with nothing
distinguishing them. Both are correct and they measure different objects: **0.651** is the
weighted per-capita Gini of the 10,841-household backbone (0.611 at household level), and
**0.671** is the unweighted per-capita Gini of the 5,000-agent resample. The 0.019 gap between
them is itself validation check F, which passes its 0.02 tolerance with almost no margin.

Chapter~3 now states both, names which is which, and reports the narrow margin rather than
presenting a single unqualified Gini.

---

## A. Completeness — the blockers

These are the only issues that determine pass or fail. Everything below section A is
improvement to work that already exists; section A is work that does not exist.

### A1 · Three of five chapters are empty headings — `BLOCKER` · `BOTH` · `OPEN`

Introduction (all six subsections), ABM Implementation, Results and Analysis, and Conclusions
and Future Work contain no prose at all.

Evidence: [main.tex:26-68](../thesis/main.tex#L26-L68), [main.tex:732](../thesis/main.tex#L732),
[main.tex:734](../thesis/main.tex#L734), [main.tex:736](../thesis/main.tex#L736).

Only the Research Questions block (82 words) and the acronym list (34 words) exist inside the
Introduction. A mini-dissertation typically runs 15,000–25,000 words; the current 6,265 are
entirely front-half.

### A2 · The model does not exist — `BLOCKER` · `BOTH` · `OPEN`

`simulation/` and `results/` are empty directories. No Mesa code, no run, no output, no figure.
`OVERVIEW.md` phase **P5 (instantiate agents) is unticked** and is the last unticked phase.

This is the binding constraint on the whole project. The ODD chapter specifies the model in
enough detail to implement almost mechanically — Submodels 1 to 17 give rule, parameter and
validation hook for every behaviour — so the specification is not the obstacle. Until a run
produces numbers there is no Results chapter and no thesis.

Consequence for sequencing: further refinement of the design chapter is now negative-value
work. See the note under F1.

### A3 · No data-layer chapter, and a dangling reference to it — `BLOCKER` · `AGENT` · `OPEN`

[main.tex:469](../thesis/main.tex#L469) reads "the static data layer described in the previous
chapter". No such chapter exists. The work does — notebooks P0 to P4, the NIDS backbone, the
FinScope cell-donor match, the weighted resample to 5,000, the 14 validation checks — but none
of it is written up.

This is the cheapest large win available: it is transcription of completed work, and it
converts the strongest finished part of the project into thesis pages.

### A4 · No limitations chapter, and two TODOs already point at it — `BLOCKER` · `BOTH` · `OPEN`

[main.tex:183-185](../thesis/main.tex#L183-L185) defers the US-to-South-Africa behavioural
transfer defence to "the limitations chapter". `OVERVIEW.md` §7 defers the
calibration-versus-validation admission to the same place. Neither chapter nor section exists.

At minimum it must house: B3, B4, B6, B11, B12, the FinScope 2019 vintage gap, the per-consumer
Regulation 23A test applied per household, and the absence of scarring or rehabilitation after
default.

### A5 · Front matter is missing entirely — `BLOCKER` · `BOTH` · `OPEN`

No abstract, no table of contents, no declaration or plagiarism page, no list of acronyms in
front matter, no list of figures or tables. Title is literally `Mini-Thesis`
([main.tex:15](../thesis/main.tex#L15)).

Requires confirmation of the UCT departmental template — see the open question at the end of
this file.

---

## B. Substantive and methodological

### B1 · The primary research question over-promises — `MAJOR` · `BOTH` · `OPEN`

The RQ asks about "**systemic default cascades**"
([main.tex:36](../thesis/main.tex#L36)). The model cannot produce one. There is:

- one aggregate, non-adaptive lender with no balance sheet that can fail
  ([main.tex:326-328](../thesis/main.tex#L326-L328));
- no macro dynamics whatsoever, by deliberate design
  ([main.tex:699-708](../thesis/main.tex#L699-L708));
- no employment or income feedback from default;
- no household-to-household *distress* channel — the only interaction is *adoption* contagion
  ([main.tex:434-445](../thesis/main.tex#L434-L445)).

Default here is an individual cash-flow event. What the model can produce is a correlated rise
in independent defaults, which is worth having and is not a cascade. An examiner will read the
RQ, then read Submodel 16, and the mismatch is immediate.

Two resolutions, and the choice is the researcher's:
1. **Rewrite the RQ** to the language the model supports — "population-level default",
   "correlated distress", "debt saturation". Cheap, honest, and loses nothing the model
   actually delivers.
2. **Add a contagion channel** so the word is earned. Any real option (lender balance sheet,
   income feedback, expenditure cascades per Cardaci) is a scope increase on a project whose
   model is not yet built.

Recommendation: option 1, and record option 2 in future work.

### B2 · Pattern 1, the "primary falsification test", is partly built in — `MAJOR` · `AGENT` · `OPEN`

[main.tex:287-292](../thesis/main.tex#L287-L292) registers complementarity as the model's
primary falsification test: enabling BNPL must *increase* stress on traditional debt.

But Submodel 3 says the want-driven trigger exists precisely because a purely shortfall-driven
BNPL agent "would model BNPL as a pure substitute and could reproduce neither finding"
([main.tex:510-515](../thesis/main.tex#L510-L515)). The rule was chosen so that this test
would not fail.

This is the same structural problem correctly diagnosed for β and RQ2 at
[main.tex:613-627](../thesis/main.tex#L613-L627) — and the fix there is a model for the fix
here. It is not fatal: the *magnitude* of the effect remains an open prediction, and the
direction could still fail through the Regulation 23A gate or through crowd-out of servicing.
But the caveat must be stated, and "primary falsification test" should be qualified.

### B3 · Three of four validation targets are foreign and off-vintage — `MAJOR` · `MARC` · `OPEN`

Only pattern 2 (2017-Q1 CCMR) is South African and vintage-matched.

| # | Target | Source | Market | Vintage |
| --- | --- | --- | --- | --- |
| 1 | Complementarity | deHaan et al. | US | 2015–21 |
| 2 | Baseline arrears | NCR CCMR | **SA** | **2017** |
| 3 | Non-monotonic DTI | Hamill et al. | UK | 2023 |
| 4 | Savings exhaustion | TransUnion CPS | SA | **2025** |

The 2017-anchoring argument at [main.tex:277-282](../thesis/main.tex#L277-L282) is strong
*because* it refuses cross-period comparison. Pattern 4 then validates a 2017 population
against a 2025 survey, which is the thing the design forbids.

Decide, with the supervisor, whether to keep four targets with the transfer defended
explicitly, or to demote 1, 3 and 4 to plausibility checks and rest validation on pattern 2
alone. The second is more defensible and costs the phrase "four externally-sourced targets".

### B4 · Pattern 4 is not operationalised — `MAJOR` · `BOTH` · `OPEN`

[main.tex:301-303](../thesis/main.tex#L301-L303): the share of agents reaching zero liquid
savings "should be consistent with" 36% of consumers anticipating a missed bill payment.

Two different constructs — a realised stock condition versus a stated forward-looking
expectation — with no mapping and no tolerance band. As written it cannot pass or fail, which
means it is not a test. Either give it a defensible mapping and an explicit band, or demote it
(see B3).

### B5 · The account-versus-household mismatch is in the JSON but not in the thesis — `MAJOR` · `AGENT` · `OPEN`

`data/config/ccmr_2017_baseline.json` carries the caveat correctly: CCMR counts **accounts**,
the model counts **households**, so this is an order-of-magnitude target, not a point target.

[main.tex:293-296](../thesis/main.tex#L293-L296) says "account-level figures" and stops. It
never states that the model's unit differs, so the comparison reads as like-for-like.

Note the inconsistency: exactly this caveat *is* given for the CFPB stacking figures at
[main.tex:661-662](../thesis/main.tex#L661-L662). The weaker treatment is on the only
vintage-matched target.

### B6 · The arrears bands are nested and appear to sum — `MINOR` · `AGENT` · `OPEN`

[main.tex:296](../thesis/main.tex#L296) gives 71.63% current, 16.54% at 60+ days, 14.21% at
90+ days. These total 102.4%. The bands nest — 90+ sits inside 60+ — and the ~11.8% in the
30-to-60-day buckets is silently dropped.

From the source JSON, combined unsecured plus credit facilities: current 71.63, 30d 8.24,
31–60d 3.59, 61–90d 2.32, 91–120d 1.76, 120d+ 12.45. State the nesting, or give the full
band breakdown as a table.

### B7 · The behavioural parameter transfer is unresolved — `MAJOR` · `MARC` · `OPEN`

Already flagged in the source at [main.tex:183-185](../thesis/main.tex#L183-L185). The
0.29 minimum-payer share is US credit-card data applied to South African unsecured credit
([main.tex:536-539](../thesis/main.tex#L536-L539)); present bias is US; Ackert et al. is a US
experiment. Submodel 6 sweeps 0.20–0.40, which helps and should be foregrounded.

Needs either a developing-market behavioural source or an explicit defence of the transfer.
Researcher task — it is a literature search, and the answer determines how load-bearing the
sweep has to be.

### B8 · RQ1's answer will be a function of two uncalibrated parameters — `MAJOR` · `BOTH` · `OPEN`

`q_base` and β are both admitted uncalibratable
([main.tex:613](../thesis/main.tex#L613)), and Submodel 13 imposes no aggregate stacking limit
([main.tex:651-652](../thesis/main.tex#L651-L652)). "Under what conditions does stacking become
self-reinforcing" therefore risks resolving to "when `q_base` and β are large enough".

The β=0 control arm handles the *circularity*. It does not handle *plausibility*: a reader will
still ask which region of the surface corresponds to the real world.

Available anchors: the 83.1% banked ceiling, the TransUnion 20% intention figure, and the CFPB
stacking shares (63% simultaneous, 32% cross-firm). Consider using the CFPB shares to **bound**
`q_base` rather than only to check output after the fact — that converts a free parameter into
a calibrated one and materially strengthens RQ1.

### B9 · The novelty claim is not yet verifiable — `MAJOR` · `MARC` · `OPEN`

TODO at [main.tex:241-244](../thesis/main.tex#L241-L244): a targeted search of JASSS, JEDC,
JEBO and arXiv econ.GN found no ABM combining a regulated and an unregulated lender class over
a survey-derived population, and no South African BNPL modelling study.

The gap claim at [main.tex:233-239](../thesis/main.tex#L233-L239) rests entirely on this. It
must be run systematically, with search strings, databases and dates recorded, so it can be
defended in the viva. Researcher task; it cannot be delegated because the record has to be
yours.

### B10 · SA BNPL market-size figures are unusable — `MINOR` · `MARC` · `OPEN`

TODO at [main.tex:217-219](../thesis/main.tex#L217-L219): commercial vendor estimates for 2024
disagree badly (R717m to R1.07bn). The standing decision — cite no headline value or CAGR, use
TransUnion penetration rates instead, which is what RQ2 actually sweeps — is correct. Confirm
and delete the TODO.

### B11 · Pattern 4 validates on the weakest variable in the data layer — `MAJOR` · `BOTH` · `OPEN`

`liquid_savings` derives from NIDS `w5_f_ass` and is annotated "**proxy: weak field**" in
[`../household_agent.md`](../household_agent.md), and was winsorised at the 99th percentile in
P2. Pattern 4 then makes the zero-savings share a validation target.

Validating the model on its least reliable input needs saying out loud, and reinforces the case
in B3/B4 for demoting pattern 4.

### B12 · Findings recorded in the working docs never reach the thesis — `MINOR` · `AGENT` · `OPEN`

Several are worth reporting and are currently invisible to an examiner:

- **53 debtor households** have income at or below the Regulation 23A expense norm, so no
  NCA-compliant lender could lawfully have granted their debt. Reported as a finding rather
  than capped away — this is a genuinely interesting result about the survey data and belongs
  in the data chapter.
- The affordability guard binds for **3.4% of debtors**.
- P4 check D was **circular** before the 2026-08-05 fix (it tested the cap it had just
  imposed). Worth a sentence in the data chapter as evidence of validation discipline.
- Emergent Gini of 0.651, inside the South African band.
- FinScope 2019 used as a 2017 proxy; the two-year gap on categorical flags is recorded but
  not corrected.

---

## C. Evidence and citation

### C1 · `\ac{FCA}` is undefined — `MINOR` · `AGENT` · `OPEN`

[main.tex:680](../thesis/main.tex#L680). LaTeX warns twice ("Acronym `FCA' is not defined on
input line 680") and the acronym renders wrong in the PDF. Add to the list at
[main.tex:54-66](../thesis/main.tex#L54-L66).

### C2 · A UK statute is cited as though it were South African — `MINOR` · `AGENT` · `OPEN`

[main.tex:685](../thesis/main.tex#L685): "section 66A of the Consumer Credit Act". That is the
United Kingdom Consumer Credit Act 1974. Unqualified, in a thesis whose entire regulatory
argument is South African, this reads as a South African provision. Name the jurisdiction.

### C3 · Two `% VERIFY` flags still live in the bibliography — `MINOR` · `MARC` · `OPEN`

- `hamill2023creditcard` — arXiv preprint; a UCL repository copy is labelled an *International
  Journal of Bank Marketing* final manuscript. Check for a published version and cite that.
- `woolard2021` — exact report title and pagination unconfirmed.

Both are cited in load-bearing positions (Hamill supplies validation pattern 3; Woolard anchors
the RQ3 affordability lever).

### C4 · Bib key does not match its authors — `MINOR` · `AGENT` · `OPEN`

`toh2025bnplconstraints` is Hayashi and Routh (2025), Federal Reserve Bank of Kansas City. The
key will cause a miscitation eventually. Rename to `hayashi2025constraints` and update the two
call sites.

### C5 · A substantive claim rests on a thin source — `MINOR` · `MARC` · `OPEN`

[main.tex:578-581](../thesis/main.tex#L578-L581) claims South African informal finance runs
substantially through stokvels, burial societies and mashonisa lending, citing
`investing_in_social_capital` — Irving (2005), a `@book` entry with no publisher, no place and
no page reference. The claim is almost certainly true and easy to source better; FinScope
itself would do, and it is already in the repo.

### C6 · Citation style may be wrong for the discipline — `MINOR` · `MARC` · `OPEN`

`\bibliographystyle{plain}` gives numeric, alphabetically ordered references. Economics and
finance conventionally use author-year. Check the departmental requirement before the reference
list is long enough to make switching annoying.

### C7 · `ncr_ccmr_2025` is retained but uncited — `MINOR` · `AGENT` · `OPEN`

Deliberate ("retained for post-period context only"). Harmless under `plain`, which prints only
cited entries. Noted so it is not mistaken for an oversight later.

---

## D. Mechanical and structural

### D1 · Everything is `\section*` under the `report` class — `MAJOR` · `AGENT` · `OPEN`

All headings are starred, so nothing is numbered, nothing enters a table of contents, and
nothing can be cross-referenced. Chapters should be `\chapter`, and the ODD elements
`\section` / `\subsection`.

This should land **before** the document grows, because every later fix re-anchors line numbers.

### D2 · Submodels are hand-numbered — `MAJOR` · `AGENT` · `OPEN`

"Submodel 9", "Submodel 17" are bold literal text, and cross-references such as "as specified
in Submodel~11" ([main.tex:510](../thesis/main.tex#L510)) are typed by hand. There are roughly
a dozen. Insert one submodel and they all break silently. Convert to `\label` / `\ref`.

### D3 · The acronym list is buried in the Introduction — `MINOR` · `AGENT` · `OPEN`

It sits under a "Key Definitions" subsection at
[main.tex:53-66](../thesis/main.tex#L53-L66). Move to front matter.

### D4 · `commath` alongside `amsmath` — `MINOR` · `AGENT` · `OPEN`

[main.tex:3](../thesis/main.tex#L3). `commath` is unmaintained and redefines macros that clash
with `amsmath`/`mathtools`. Nothing currently breaks; drop it unless something needs it.

### D5 · Live TODO comments in the source — `MINOR` · `BOTH` · `OPEN`

[main.tex:183-185](../thesis/main.tex#L183-L185),
[main.tex:217-219](../thesis/main.tex#L217-L219),
[main.tex:241-244](../thesis/main.tex#L241-L244). They map to B7, B10 and B9. Keep them until
those close — they are doing real work — but they must not survive to submission.

### D6 · No figures or tables anywhere — `MAJOR` · `BOTH` · `OPEN`

24 pages of unbroken prose. The data layer already has plottable material (quintile archetypes,
the education-by-quintile gradient, balance-sheet views, the P4 scorecard) sitting in
`notebooks/p1p2_visualizer.ipynb` and `notebooks/00_showcase.ipynb`. This is also a
condensation lever: see F3.

---

## E. Writing register — humanisation

The prose is good and the argument is the author's. The problem is uniformity: one rhetorical
move is used relentlessly, and the polish is unvaryingly high across all 6,265 words. Several
readers would notice something stylistically off. The fixes are mechanical and should not touch
content.

### E1 · The antithesis construction is overused — `MAJOR` · `AGENT` · `OPEN`

"X is not Y, it is Z." Twenty-plus instances, including:

> "The 2017 anchor is a control rather than a limitation." · "This is not a modelling
> preference." · "Peer influence is therefore not an optional embellishment." · "It is not
> merely a reporting category." · "Seven is not a round number chosen for convenience." · "The
> invisibility of BNPL obligations is not a simplification adopted for tractability."

Target: cut by roughly two-thirds, converting most to plain declaratives. Keep the two or three
where the contrast is genuinely the point.

### E2 · "rather than" appears 45 times — `MAJOR` · `AGENT` · `OPEN`

Once every 139 words of prose. This is the single strongest stylistic tell in the document.
Target: under 15.

### E3 · Every paragraph lands on a punchline — `MINOR` · `AGENT` · `OPEN`

"…and that is the point." · "That last gap is where this thesis sits." · "The contrast is worth
stating plainly." Real academic prose has flat paragraphs that simply deliver information.
Let perhaps half of them end on an ordinary sentence.

### E4 · The register never varies — `MINOR` · `AGENT` · `OPEN`

Literature review, ODD overview and submodel details are all written at identical polish and
cadence. Submodel details in particular should read drier and more technical than the synthesis
sections. The condensation work in F is the natural opportunity to introduce that variation.

### E5 · Retain the evidence of authorship — `MINOR` · `MARC` · `NOTE`

Not a defect — a countervailing instruction for the E1–E4 work. **Do not sand off** the
self-critical passages: the β circularity admission
([main.tex:613-627](../thesis/main.tex#L613-L627)), the calibration-not-validation flag
([main.tex:306-309](../thesis/main.tex#L306-L309)), "this submodel is an assumption with no
literature anchor" ([main.tex:517](../thesis/main.tex#L517)), and the working TODOs. They are
the strongest signals of genuine authorship in the document and the best methodological
material in it.

---

## F. Length and condensation

### F1 · The design chapter is 73% of the document — `MAJOR` · `BOTH` · `OPEN`

| Chapter | Words | Share |
| --- | ---: | ---: |
| Introduction | 116 | 2% |
| Literature Review | 1,580 | 25% |
| **ABM Design (ODD)** | **4,569** | **73%** |
| Implementation / Results / Conclusions | 0 | 0% |

Detail within the design chapter: Submodels 2,534 · Design concepts 688 · Purpose and patterns
418 · Entities 371 · Scheduling 279 · Initialisation 111 · Input data 26.

The ODD chapter deserves substantial space — it is the methodological core, and its rigour is
the project's main strength. It does not deserve three-quarters of a word budget that must
still absorb a data chapter, an implementation chapter, results, limitations and conclusions.

**Target: 4,569 → roughly 2,600, a 40–45% cut, with no loss of specification detail.** The
mechanism is form, not deletion: prose that is really a lookup table becomes a table.

### F2 · Design concepts: 688 words of prose that is really a table — `MAJOR` · `AGENT` · `OPEN`

Eleven ODD design-concept headings, each a bold run-in paragraph. Most say little more than
"none" or one sentence — Learning, Prediction, Objectives, Adaptation.

Convert to a compact table (concept · treatment · source), and keep extended prose only for the
two that carry the argument: **Emergence** (the two separable feedback loops) and **Sensing**
(the information asymmetry). Estimated 688 → ~250.

### F3 · Submodels: 2,534 words across 17 entries — `MAJOR` · `AGENT` · `OPEN`

Roughly 150 words each, all at the same depth regardless of importance. Restructure to:

- **A specification table for all 17**: rule · source · parameter and sweep · validation hook.
  This is exactly the four-field structure the entries already follow, so nothing is lost, and
  it doubles as the D6 fix.
- **Extended prose for the five that are load-bearing**: 9 (the Regulation 23A gate),
  10 (information asymmetry), 11 (peer influence), 13 (stacking), 15 (intervention levers).
- **Everything else compressed to its table row**, plus a sentence where a rejected alternative
  matters.

Estimated 2,534 → ~1,500.

### F4 · Rejected-alternative justifications should move to an appendix — `MINOR` · `AGENT` · `OPEN`

"A propensity-to-consume rule was rejected because…" · "Cost ranking was rejected…" · "A
continuous present-bias parameter was rejected…" · "A cash-flow insolvency test was chosen
over…". Valuable for the viva, expensive in the body. Move to a design-rationale appendix —
`scratchpad/decision.md` already holds most of this material and can be adapted directly.
Appendices are usually outside the word limit; confirm.

### F5 · The counterfactual statement is scheduled to appear three times — `MINOR` · `BOTH` · `OPEN`

`OVERVIEW.md` §1a instructs stating it "in the introduction, in the ODD Purpose section, and
again in limitations". It currently occupies 418 words at
[main.tex:269-282](../thesis/main.tex#L269-L282). Three full statements is a large slice of a
constrained budget. Recommend one full statement in the Introduction, a two-sentence recall in
the ODD purpose element, and a cross-reference in limitations.

---

## G. Record-keeping hygiene

### G1 · `OVERVIEW.md` header date is stale — `MINOR` · `AGENT` · `OPEN`

Header says "Last updated: **2026-06-01**" while the changelog runs to 2026-08-05 with four
entries. It is the declared source of truth, so its own date should be right.

### G2 · Caveats live in JSON but not in prose — `MINOR` · `AGENT` · `OPEN`

`data/config/ccmr_2017_baseline.json` carries three caveats, only one of which reaches the
thesis. The same pattern in `OVERVIEW.md` §7 (see B12). Establish the rule: a caveat recorded
in a data artefact must have a home in the limitations chapter.

### G3 · `notebooks/context/` is an empty tracked directory — `MINOR` · `AGENT` · `OPEN`

Remove or populate.

---

## Open questions for the researcher

These block or materially change the plan and cannot be answered from the repository.

1. **What is the word limit, and does it include appendices, references and captions?** F1 to
   F5 are sized against it; the current condensation target of ~2,600 for the design chapter is
   inferred, not given.
2. **Is there a UCT or departmental LaTeX template or formatting specification?** Determines
   A5 and D1, and both are cheaper to do once, early.
3. **How much scope is available?** Specifically B1: rewrite the research question to match the
   model, or extend the model to earn the word "systemic". This is a supervisor conversation.
4. **What is the submission date?** A2 is the binding constraint and everything else is
   sequenced behind it.
