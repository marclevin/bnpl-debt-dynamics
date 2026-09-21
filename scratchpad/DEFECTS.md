# DEFECTS — everything wrong, or once wrong, with evidence

**One of three working documents.** [`DECISIONS.md`](DECISIONS.md) is *what was chosen and why*.
[`DEFECTS.md`](DEFECTS.md) is *what is wrong or was wrong*. [`PLAN.md`](../archive/PLAN.md) is *what happens
next*. Consolidated 2026-08-13 from nine overlapping files.

Raised in the full-document review of **2026-08-05** and extended continuously since. This file is
the record; fixes are tracked here, not in commit messages. Where an issue changes a design
decision, close it *here* and propagate to [`DECISIONS.md`](DECISIONS.md) and
[`../OVERVIEW.md`](../OVERVIEW.md).

> **The four entries that matter most right now**, if you read nothing else:
> **B20** (the shock rate is 4x observed labour-market flows — the model's worst *disclosed*
> weakness), **B22** (RQ2's registered hypothesis is unsupported, and the fallback finding may have
> evaporated too), **B24** (the sensitivity ranking is superseded and must be regenerated), and
> **B31** (a wiring detail that would corrupt the Granovetter run if not decided first).
>
> **Added 2026-09-21: B34, found and closed the same day.** Granted traditional loans were never
> booked as debt (R9.96m, 20.7% of the opening book, over one baseline run). Fixed and re-fitted;
> the side effect is that **B20's overshoot fell from 3.4x to 1.4x** the QLFS upper bound.

**Line references** are against `thesis/main.tex` as at commit `47e57d0`. They will drift once
the restructure (D1) lands; re-anchor at that point.

## Legend

| Field | Values |
| --- | --- |
| **Severity** | `BLOCKER` cannot submit · `MAJOR` examiner will challenge it · `MINOR` polish |
| **Owner** | `MARC` researcher judgement, supervisor, or external work · `AGENT` executable in-repo · `BOTH` |
| **Status** | `OPEN` · `IN PROGRESS` · `CLOSED` · `WONTFIX` (with reason) |

## Standing at a glance

Re-tallied from the entry headings on **2026-08-12**.

| Group | Count | Open | Closed | Superseded |
| --- | ---: | ---: | ---: | ---: |
| A. Completeness | 5 | 5 | 0 | 0 |
| B. Substantive / methodological | 32 | 21 | 10 | 1 |
| C. Evidence and citation | 7 | 7 | 0 | 0 |
| D. Mechanical and structural | 6 | 6 | 0 | 0 |
| E. Writing register | 4 | 4 | 0 | 0 |
| F. Length and condensation | 5 | 5 | 0 | 0 |
| G. Record-keeping hygiene | 3 | 3 | 0 | 0 |
| **Total** | **62** | **51** | **10** | **1** |

> **⚠ The entry headings disagree with the resolution log below, and the log is right.** The
> 2026-08-05 document pass closed A3, A4, B1–B12, C1–C5, D1–D4, E1–E5, F1–F5 and G1–G3, but only
> the log was updated; the `OPEN` markers in the individual headings were never changed. The table
> above therefore **overstates the open count substantially** — it counts heading text, not status.
> Several entries are also stale on their facts: **A2 says "the model does not exist"**, which
> stopped being true when it was built and run.
>
> This is a record-keeping defect in the register itself, in the same family as G1/G2. It is called
> out rather than silently corrected because reconciling 40 headings against the log is a
> deliberate pass, not a side effect of a parameter fix. **Do it before the register is shown to
> anyone.** The entries added during and after implementation (B14 onward) carry accurate headings.

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

`OVERVIEW.md` reports 0.651 and `p3_resample_summary.json` reports 0.667, with nothing
distinguishing them. Both are correct and they measure different objects: **0.651** is the
weighted per-capita Gini of the 10,841-household backbone (0.611 at household level), and
**0.667** is the unweighted per-capita Gini of the 5,000-agent resample. The 0.015 gap between
them is itself validation check F, which passes its 0.02 tolerance.

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

**Partial progress 2026-08-12 (`AGENT`).** Not this issue's core — the 0.29 transfer is untouched —
but one adjacent transfer was **eliminated** rather than defended. The D1 income-shock *magnitude*
was an unsourced free parameter; re-reading Madeira showed his labour shock is a flow into
unemployment, not a fractional income cut, so the magnitude is the household's **wage component**,
observable in `w5_hhwage`. It is now data-driven, South African, and carries no parameter to sweep.
That is the pattern this issue wants: replace a transferred number with a local observable where the
data allows it. **It does not close B7.**

### B8 · RQ2's answer will be a function of two uncalibrated parameters — `MAJOR` · `BOTH` · `OPEN`

`q_base` and β are both admitted uncalibratable
([main.tex:613](../thesis/main.tex#L613)), and Submodel 13 imposes no aggregate stacking limit
([main.tex:651-652](../thesis/main.tex#L651-L652)). "Under what conditions does stacking become
self-reinforcing" therefore risks resolving to "when `q_base` and β are large enough".

The β=0 control arm handles the *circularity*. It does not handle *plausibility*: a reader will
still ask which region of the surface corresponds to the real world.

Available anchors: the 82.8% banked ceiling, the TransUnion 20% intention figure, and the CFPB
stacking shares (63% simultaneous, 32% cross-firm). Consider using the CFPB shares to **bound**
`q_base` rather than only to check output after the fact — that converts a free parameter into
a calibrated one and materially strengthens RQ2.

**Related precedent set 2026-08-12 (`AGENT`).** The same "bound it, don't just check it afterwards"
move has now been applied to the *third* uncalibrated parameter, the income-shock probability `p`.
`p` stays fitted to CCMR arrears (D1 requires that), but it is now **reported against an independent
official band**: Stats SA Labour Market Dynamics 2022 (Report 02-11-02) gives vintage-matched 2017
QLFS job-separation rates, implying **0.54%–1.17% per tick**
(`data/config/qlfs_2017_labour_flows.json`). A fitted `p` outside that band is evidence the shock
process is carrying stress the rest of the model should generate.

This is the template for `q_base`: fit or sweep, then report against an external band rather than
leaving the reader to ask which region of the surface is real. **B8 stays OPEN** — `q_base` and β
themselves are still unbounded.

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

### B15 · The minimum-payment formula was never defined — `MAJOR` · `AGENT` · `OPEN`

Found 2026-08-12 while planning the implementation. **D6 fixes the *share* of agents who pay the
contractual minimum (`m = 0.29`) but never says what the contractual minimum *is*.** The rule was
recorded as closed and cited, and the gap survived the whole design pass because `[Keys2019]`
measures behaviour *relative to* whatever minimum a US issuer set, so citing it feels like it
settles the question when it does not. The NCA prescribes maximum rates and the Reg 23A
affordability test but **no minimum-payment formula**, so there is no SA statutory anchor either.

Now closed by assumption in D6 — `max(interest accrued, 5% of balance per month)`, tick-scaled, with
the interest floor preventing negative amortisation by construction — and swept 2.5%–10%.

**This is the model's second uncited rule, alongside D4.** The limitations chapter currently
presents D4 as the only one. That sentence has to change, and the minimum-payment assumption must
appear in the parameter register flagged as an assumption, not buried in code. If the minimum-payer
arm turns out to drive results, the finding is minimum-formula-sensitive and must be reported so.

### B16 · SA BNPL credit limits are not publicly disclosed — `MINOR` · `AGENT` · `CLOSED`

Searched 2026-08-12. D11's rolling available balance was marked `NOT SOURCED`; a deliberate search
confirms **no published figure exists for either major SA provider**. Payflex publishes the R15,000
per-order cap but sets the rolling limit per customer from credit history `[payflex_limits]`;
PayJustNow declines to publish limits at all `[payjustnow_limits]`.

Closed as "cannot be sourced", and the absence is worth a sentence in the thesis rather than a
silent round number: the opacity of BNPL credit limits is consistent with the regulatory position
in D10, where the product sits outside the NCA with no disclosure or reporting obligation. The
parameter is demoted to a binding-check quantity under D11's existing "check the cap binds rarely"
requirement — if it rarely binds it is inert, and the sweep demonstrates that.

⚠ Related and weaker: BNPL **purchase size** now leans on an SA average basket of R1,568 from
**trade press** (`sa_bnpl_basket_2026`, flagged `% VERIFY`). It is the weakest source in the
bibliography and is retained only because it is the sole SA-specific figure, cross-checked against
CFPB. If a regulator or provider figure surfaces, replace it.

**⚠ UPDATE 2026-08-12 — a provider figure did surface, and the "cannot be sourced" verdict was
half wrong.** Two things changed:

- **Purchase size is now sourced.** HomeChoice International plc, a listed issuer, discloses BNPL
  gross merchandise value; Weaver Fintech discloses cumulative GMV and transaction counts. The
  average order value falls out of dividing two published aggregates: **R1,394 nominal, R992 in 2017
  Rands**. The trade-press figure deflates to R1,038, so the two agree within 4.6%. The trade source
  is **demoted from input to corroboration** (B30). The lesson generalises: search the primary
  disclosures — listed-issuer reports, regulator returns — before accepting an absence. A support
  page saying "we don't publish this" is not evidence that the quantity is unobtainable.
- **The rolling limit is still not published, but its FUNCTIONAL FORM now is.** HomeChoice's audited
  credit-risk section states a **"low and grow"** policy — first-time customers start with lower
  limits, which are increased as they exhibit good repayment behaviour, with lower maximum limits
  for externally-acquired customers. That is an annual report rather than a support page, and it
  licenses modelling the limit as a *function of household characteristics*, which is what B30 now
  does. It also licenses a **dynamic** limit that grows with repayment history — recorded as future
  work, not built, since the static income-scaled rule already retires the vulnerability.

So the absence stands for the **level** and is still worth a sentence in the thesis; it does not
stand for the **form**, and it never stood for purchase size.

### B17 · D1's single-tick shock could not carry its own calibration — `MAJOR` · `AGENT` · `CLOSED`

Found 2026-08-12 by running the model. D1 specified the income shock as **non-persistent (single
tick)** and simultaneously made `p` the parameter that *carries* the baseline validation. Those two
commitments are incompatible, and the register never noticed because nothing had been executed.

Measured: with a single-tick shock, sweeping `p` from **0 to 0.40** moves the 90+ arrears rate only
from **1.13% to 1.47%**, against a **14.21%** target. The parameter cannot move the quantity it is
supposed to be fitted to. A one-tick wage loss is absorbed by savings or refinanced through the D9
gate, which is computed on income that has not yet fallen.

Closed by making the shock an **unemployment spell** with a sourced exit hazard (QLFS 2017:
11.6% per quarter → 1.87% per tick). The same sweep then spans **4.0%–16.8%** and brackets the
target. The revision moves the model *toward* its anchor — Madeira models flows into and out of
unemployment — and toward the SA data, where 68.4% of the unemployed remain unemployed a quarter
later. `shock_persistent=False` recovers the original rule as a robustness arm.

**Worth reporting in the thesis, not just fixing.** It is a clean example of implementation
falsifying a specification that looked complete on paper, which is an argument for building the
model rather than only designing it.

### B18 · The CCMR denominator excluded over half the population — `MAJOR` · `AGENT` · `CLOSED`

Found 2026-08-12. The account-vs-household mismatch (B5) was recorded, but only one edge of it. The
second edge: CCMR accounts are held by **credit-active** consumers, whereas **only 44.2%** of the
5,000 households hold traditional debt. A household with no debt can never be in arrears, so
comparing an all-household arrears rate to an account-level target builds in an undershoot with no
behavioural content.

Measured on one run: **1.68%** of all households 90+ against **3.80%** of credit-active households —
a factor of 2.3, definitional.

Closed by reporting both. The **credit-active** rate is compared to CCMR; the **all-household** rate
remains the population default rate the RQs ask about. B5's thesis text needs extending to state
this second edge, not just the first.

### B19b · Pattern 3 resolved by fixing the STATISTIC, not the data — `MAJOR` · `AGENT` · `CLOSED`

Supersedes B19 below, which recorded the first (wrong) measurement. The failure was **not**
behavioural and **not** caused by the zero-capacity debtors as such. It was a badly chosen
statistic: a **mean of ratios** over a population containing near-zero incomes.

Diagnostic: in Q1 the **top 1% of households carry 76.9% of the total DTI mass**, and the median Q1
household has DTI of **0.000**. The Q1 mean of 2.92 was three households with tiny incomes, not a
finding. A mean of ratios is not a meaningful measure over this population.

**Pre-registered primary statistic: the AGGREGATE ratio** (total debt / total income per quintile),
chosen on its own merits before checking whether it passes — it is the standard financial-stability
measure, it is the form the CCMR reports in, and it cannot be driven by a near-zero denominator.

| | Q1 | Q2 | Q3 | Q4 | Q5 | Peak |
| --- | --- | --- | --- | --- | --- | --- |
| **PRIMARY aggregate** | 1.163 | 0.612 | 1.172 | **1.446** | 0.561 | **Q4 — pattern HOLDS** |
| secondary mean | 3.394 | 0.886 | 1.317 | 1.074 | 1.163 | Q1 |
| secondary median (debtors) | — | — | — | — | — | reported alongside |

Non-monotonic with a middle-upper peak and Q5 lowest, which is Hamill's qualitative shape.

**All 5,000 households retained**, including the 33 zero-capacity debtors, all of which sit in Q1.
Excluding them would also flip the verdict, and that is precisely why they stay: P2's decision was
to report them, and dropping data to make a test pass is the circularity avoided elsewhere.
**The thesis must report all three statistics and state that the verdict is statistic-dependent.**

⚠ A median over *all* households is identically zero in every quintile (participation is below 50%
everywhere), so the median is computed over debtors only.

### B19 · Pattern 3 fails as specified — `MAJOR` · `BOTH` · `SUPERSEDED by B19b`

First baseline calibration, 2026-08-12, 20 replicates at the fitted `p`. Pattern 3 (Hamill et al.:
non-monotonic income to debt-to-income with a **middle-income** peak) **does not hold** as written.
Debt-to-income by quintile:

| Q1 | Q2 | Q3 | Q4 | Q5 |
| --- | --- | --- | --- | --- |
| **3.396** | 0.903 | 1.341 | 1.065 | 1.157 |

The relationship *is* non-monotonic, which is half the pattern, but the peak is at **Q1**, not the
middle. Two readings, and the thesis should give both:

- **Q1's ratio is a denominator artefact.** Debt-to-income explodes as income approaches zero, and
  Q1 contains the households whose debt no NCA-compliant lender could have granted (the 53/33
  zero-capacity debtors). This is arguably not a behavioural result at all.
- **Excluding Q1, the peak is at Q3** — an actual middle-income peak, consistent with Hamill.

**Do not quietly report the Q2-Q5 version as a pass.** Report the full profile, state that the
pattern fails on the stated test, and give the Q1-excluded reading as a secondary observation with
the denominator caveat attached. A failed independent test is a result, and this is the first
genuinely unfitted test in the thesis.

### B20 · The fitted shock rate is ~4x observed labour-market flows — `MAJOR` · `BOTH` · `OPEN`

> **⚠ UPDATE 2026-09-21: the overshoot is now 1.4x, not 4x, and a large part of it was a bug.**
> Fitted `p` has moved twice since this entry was written: 0.048 → 0.040 on the rebuilt population
> (B32), then **0.040 → 0.016** once granted traditional loans were booked as debt (B34). Against
> the sourced band of 0.0054–0.0117 that is **1.37x the upper bound**. The explanation below still
> holds in kind — one channel is doing the work of several — but most of the "missing channels"
> reading was wrong: the shock rate had been inflated to generate CCMR arrears *in spite of* free
> traditional credit. The entry stays OPEN because `p` is still outside the band, and the thesis
> says so (the Calibration section and Appendix C, both updated to "about 1.4 times").

The QLFS cross-check added on 2026-08-12 did its job on the first run. Fitted
`p = 0.048` per tick against a sourced band of **0.0054-0.0117**, so **4.1x the upper bound** — and
still roughly 2.8x after a rough adjustment for multi-earner households.

The model needs a job-separation rate several times the real one to reproduce CCMR arrears. The
likely reason is structural: the population was built so that debt service is **affordable by
construction** (P2 caps servicing at Reg 23A capacity), so **98.2%** of households can meet their
instalment out of income, and the single labour shock is the only channel into arrears. In reality
arrears are generated by many stressors at once — expense shocks, illness, household composition
change, rate changes — none of which this model carries (D15 holds macro static deliberately).

Read it as: the shock parameter is absorbing the work of several missing channels. It belongs in
the limitations chapter next to the calibrated-not-validated caveat, and it strengthens rather than
weakens the case for the QLFS band, which is what exposed it.

**⚠ UPDATE 2026-08-12: the comparison is now LIKE-FOR-LIKE, so the gap can no longer be explained
away.** The shock hazard now applies **per earner** — each employed member separates independently —
so `p` is an *individual* separation rate, directly comparable to the QLFS *individual* transition
rate. The household-versus-individual caveat that previously absorbed part of the gap **no longer
applies**. The overshoot stands at **4.1x on a like-for-like basis**, and adding the second
(friction) stressor did not reduce it, because friction generates mild delinquency rather than the
deep arrears `p` is fitted to. State it plainly in the limitations chapter.

### B21 · Arrears mass is bimodal; the middle CCMR bands are underpopulated — `MINOR` · `AGENT` · `OPEN`

At the fitted `p`: 90+ is **14.9%** against a target of 14.21% and 60+ is **16.2%** against 16.54%,
both close, but `current` is **81.4%** against **71.6%** — about 10pp too high. The shortfall sits
in the mild bands (1-30 and 31-60 days), which are nearly empty.

**Cause, correctly diagnosed on the second attempt.** The first diagnosis (no recovery path) was
wrong: arrears *can* cure in the model. What cannot recover is **income**. The unemployment spell
has a sourced exit hazard of 1.87%/tick, giving a mean spell of ~53 ticks against a 52-tick horizon,
so a shocked household is effectively absorbed. Meanwhile 98.2% of unshocked households can afford
their instalment out of income. The population therefore has exactly two states.

**Attempted fix that did NOT work (2026-08-12).** Splitting the shock by earner count, so a job loss
costs one earner's wage rather than all of it, was implemented and re-calibrated. It made things
marginally worse on this measure (`current` 81.4% → 82.7%), because 72% of WAGE households are
single-earner, so for most of them the shock is still total. **Kept anyway**: it is more faithful to
the data, and it makes `p` a per-earner hazard directly comparable to the QLFS *individual* rate,
which removes the household-vs-individual fudge from the calibration check. It just does not fix
bimodality.

**Full band profile at the fitted `p`, credit-active denominator:**

| Band | Model | CCMR 2017 | Gap |
| --- | --- | --- | --- |
| current | 77.13% | 71.63% | +5.50 |
| 1–30 d | **0.82%** | **8.24%** | **−7.42** |
| 31–60 d | 0.89% | 3.59% | −2.70 |
| 61–90 d | 0.69% | 2.32% | −1.63 |
| 91–120 d | 0.79% | 1.76% | −0.97 |
| 120+ d | 19.69% | 12.45% | +7.24 |

Total delinquency is roughly right (**22.9%** vs 28.4%); its **distribution** is not. The single
largest gap is the **1–30 day band**, which is the *largest* delinquent band in reality and is
nearly empty in the model.

**What is actually missing is transient mild delinquency** — households a fortnight late that then
catch up. That is not unemployment; it is payment friction. The model has exactly one stressor and
it is persistent, so it cannot generate it. Same root cause as **B20**'s 4x overshoot: one channel
doing the work of many.

**RESOLVED 2026-08-12 by adding a second, cited stressor.** `payment_friction`: a per-tick
probability of missing a traditional instalment **despite having the cash**, anchored to
Kuchler & Pagel `[Kuchler2021]` (present-biased borrowers fail to execute planned paydown) — already
in the bibliography and already cited in D6. Traditional debt only, because BNPL auto-debits a card,
so inattention cannot stop a BNPL instalment. Fitted to the 1-30 band at **0.09 per tick**.

D7 distress is assessed **before** friction is applied, so a household that skips an affordable
instalment is not counted as cash-flow insolvent and the headline default rate stays clean. Verified
by test: heavy friction more than doubles the 1-30 band while moving default by under 1pp, and
*downward* rather than up (withholding a payment conserves cash). Not perfectly orthogonal, but the
residual is explicable and bounded.

**Result — two parameters, two targets, three unfitted bands:**

| Band | Before | After | CCMR | Status |
| --- | --- | --- | --- | --- |
| current | 77.13% | **74.41%** | 71.63% | unfitted, +2.78 |
| 1-30 d | 0.82% | **8.38%** | 8.24% | FITTED |
| 31-60 d | 0.89% | 1.25% | 3.59% | unfitted, −2.34 |
| 61-90 d | 0.69% | 1.21% | 2.32% | unfitted, −1.11 |
| 90+ d | 20.47% | **14.75%** | 14.21% | FITTED |
| **60+ d** | 14.93% | **15.96%** | **16.54%** | **unfitted, −0.58** |

Total delinquency **25.6%** against 28.4%, up from 22.9%. The 60+ band remains the strongest
independent result in the thesis. The 31-60 and 61-90 bands are still roughly 2pp and 1pp thin,
which is the residual of the same one-persistent-stressor problem and should be reported as such
rather than fitted away with a third parameter.

### B22 · RQ2's conditional non-linearity claim is NOT supported — `MAJOR` · `BOTH` · `OPEN`

First full sweep, 2026-08-12, 700 runs (7 access levels x 5 beta x 20 replicates). The registered
claim was *"population default responds non-linearly to BNPL access only where social transmission
is present"*. It does not hold. **Every arm is near-linear, including `beta = 0`:**

| beta | rise over access range | linear R² | max deviation from linear |
| --- | --- | --- | --- |
| **0 (control)** | +8.48% | **0.9992** | 1.4% of rise |
| 0.5 | +20.83% | 0.9681 | 8.8% |
| 1 | +31.68% | 0.9702 | 9.5% |
| 2 | +35.98% | 0.9914 | 6.3% |
| 3 | +36.33% | 0.9965 | 3.8% |

**What IS strongly supported is amplification, not non-linearity.** Peer influence multiplies the
access response by **4.3x**. That is a clean result and arguably a better one, because it is a
*magnitude* claim that the `beta = 0` control identifies cleanly.

Two secondary observations worth reporting:
- **Curvature peaks at INTERMEDIATE beta** (R² lowest at 0.5-1.0) and disappears at high beta. The
  system saturates: beta=2 and beta=3 are nearly indistinguishable.
- The registered fallback now applies. D17 pre-registered the **Granovetter heterogeneous-threshold
  variant** as the structural robustness check should linear coupling give only a smooth response.
  That is exactly what happened, so the variant should be run before concluding no threshold exists.
  Linear coupling producing a linear response is close to tautological; heterogeneous thresholds are
  the mechanism that would actually generate tipping.

**Do not restate the RQ as if it had been answered affirmatively.** The honest headline is
amplification, with non-linearity unsupported under linear coupling and still open under the
threshold variant.

### **UPDATE 2026-08-13: the threshold variant has been run. The negative holds, and is now much stronger.**

Granovetter heterogeneous thresholds **do not produce a cascade either**, and the striking part is
that they do not even produce one in *adoption*:

| Arm | Adoption rise | Adoption R² | Default rise | Default R² |
| --- | ---: | ---: | ---: | ---: |
| `gamma = 0` (control) | +21.1% | **0.9999** | +3.07% | 0.954 |
| `gamma = 0.3`, `sigma = 0.1` | +42.1% | 0.9994 | +3.62% | 0.995 |
| `gamma = 0.3`, `sigma = 0.4` | +35.1% | **0.9999** | +3.56% | 0.988 |

The adoption response is **more linear than the default response**. Thresholds fire at the household
level, but aggregated across 45 reference groups they average into a straight line, at every
dispersion setting. **Two structurally distinct social mechanisms, and neither produces
non-linearity in adoption or in default.** That is the robust negative D17 pre-registered this arm
to obtain.

⚠ **Amplification has collapsed from 4.3× to 1.6×.** Under corrected parameters peer influence
multiplies the access response by 1.6, not 4.3. The amplification finding survives but is much
weaker, and **the 4.3× figure must not be quoted anywhere**.

**What replaces both claims** is the adoption-versus-default split, which is a cleaner result than
either: social transmission roughly **doubles adoption** (21% → 42%) while moving default by about
**half a percentage point**. People catch BNPL from their peers; they do not catch distress from
them. Figure: `results/summary/figures/rq2_threshold_adoption_vs_default.png`.

### B23 · Bureau visibility, the model's headline policy lever, does nothing — `MAJOR` · `BOTH` · `OPEN`

RQ3, 400 runs. Closing the reporting gap (D14 lever 1) has **essentially no effect** on population
default: 32.99% against 32.91% with no lever at `beta = 0`, and 56.38% against 56.12% at `beta = 1`.
Cumulative BNPL volume moves by under 1%.

D10 called this "the comparison the whole model was built to make", so a null result needs stating
loudly rather than being buried. **It is a coherent finding, not a bug** — the degenerate-case test
confirms the lever does tighten the traditional gate. It constrains the *wrong lender*: bureau
visibility only affects what the **traditional** lender will grant. It does nothing to BNPL
eligibility, nothing to the platforms' mutual blindness (D12), and nothing to the want-driven
trigger. Households keep stacking BNPL regardless; they are simply refused additional *bank* credit.

The policy reading is genuinely interesting and should be foregrounded: **transparency alone is not
a remedy.** The lever that does work is the mandatory Reg 23A affordability check on BNPL (lever 2),
which cuts default from 32.91% to 28.05% and volume by 15.3% at `beta = 0`. Disclosure without an
accompanying affordability duty changes who lends, not how much debt is taken on.

### **CONFIRMED 2026-08-13, and the ranking of the OTHER levers has inverted.**

**The null result survives a complete parameter rebuild**, which is the strongest thing that could
have happened to it: bureau visibility moves cumulative BNPL volume by **+1.9%** at `beta = 0` and
**−1.0%** at `beta = 1`. Still nothing. This is the finding to lead the thesis with.

⚠ **But the affordability duty is no longer the lever that works.** It has gone from cutting default
4.9pp to roughly inert (+1.9% / −1.4% on volume). The most effective lever is now the **stacking
cap**, which cuts volume 54–63% and pulls default back to 24.6%, against a 24.2% no-BNPL baseline.

**Plausible mechanism, worth checking before RQ3 is written.** With income-scaled limits already
binding on ~54% of requests, an affordability test adds little that the limit is not already doing,
whereas capping concurrent facilities attacks the stacking mechanism directly. If that holds, the
policy story sharpens considerably: **the harm is in the NUMBER of concurrent facilities, not in any
single loan being unaffordable**, which is exactly why per-loan instruments fail and a cap works.
⚠ The cap remains **hypothetical** — no jurisdiction imposes one — and must stay labelled as such.

**The corrected statutory cool-off (B27) behaves as predicted:** `k_cool = 1` gives −0.2% volume at
`beta = 0` and **−33.5%** at `beta = 1`, against a pre-run prediction of −30.4%. "Close to useless
against individual impulse, materially effective against social transmission" is confirmed.

### B27 · The statutory cool-off arm is a no-op (off-by-one) — `BLOCKER` · `AGENT` · `CLOSED`

**Closed 2026-08-12.** The gate in [`agents.py`](../simulation/agents.py) is now strict
(`tick > cool_off_until`), so `k_cool = n` blocks want-driven initiation for exactly the next `n`
ticks and `k_cool = 1` is the statutory 14-day arm as D14 always intended.

**The regression test the suite was missing** is
`test_statutory_cool_off_strictly_reduces_want_driven_purchases` in
[`test_bnpl_parameters.py`](../simulation/tests/test_bnpl_parameters.py). Two changes from the old
test, and both were necessary:

- it asserts a **strict** reduction, which a no-op cannot satisfy;
- it asserts on the **want-driven purchase count**, not on cumulative volume. Volume mixes in the
  shortfall-driven path, which the cool-off deliberately does not block (D14), so volume was never
  the quantity the lever acts on. A second test checks the count is monotonically non-increasing
  across `k_cool ∈ {0,1,2,4}`.

The old `test_cool_off_cannot_increase_bnpl_volume` is **kept**, with a comment recording that it is
necessary but not sufficient and why. That comment is the useful artefact: it is the reason the
defect survived 65 passing tests and a full experimental run.

⚠ The corrected RQ3 numbers are **not yet measured** — they arrive with the re-run. The expectation
from the old `k_cool = 2` arm (−2.6% volume at β=0, −30.4% at β=1) is now itself uncertain, because
B28/B29/B30 changed the model underneath it.

### B27-original · The statutory cool-off arm is a no-op (off-by-one) — historical record

Found 2026-08-12 while reading the RQ3 output. In `simulation/agents.py` a want-driven purchase at
tick `t` sets `cool_off_until = t + k_cool`, and the gate is `tick >= cool_off_until`. With
`k_cool = 1` the gate passes again at `t + 1`, so **nothing is ever blocked** — a household could not
purchase twice within one tick anyway.

`k_cool = 1` is the arm the thesis presents as the **CCA s.66A statutory 14-day right of
withdrawal**, and D14 makes a point of it landing exactly on a tick boundary. The sweep therefore
reports the statutory instrument as having *precisely zero* effect (+0.0% volume at both betas).
**That is an artefact, and it inverts the headline RQ3 claim.**

The current `k_cool = 2` arm is what a corrected `k_cool = 1` will produce: **−2.6% volume at β=0
and −30.4% at β=1**. So the corrected finding is *"the statutory cool-off is close to useless
against individual impulse and materially effective against social transmission"* — a much better
result than the one currently in the output.

⚠ **The test suite missed this** because `test_cool_off_cannot_increase_bnpl_volume` only asserts
volume does not *increase*, which a no-op satisfies trivially. Fix requires a regression test that
`k_cool = 1` **strictly reduces** want-driven purchase count against `k_cool = 0`.

Plan: [`PLAN.md`](../archive/PLAN.md) **P0**. Nothing else in RQ3 is affected — the affordability,
bureau and stacking-cap arms are unaffected by this bug.

---

## The 2026-08-12 QA pass

Four defects found and closed in one pass, plus one raised for the Granovetter work. Plan and
evidence: [`PLAN.md`](../archive/PLAN.md). All 79 tests pass (65 existing, 14 new).

**The baseline is untouched.** `shock_prob` and `payment_friction` are fitted with `bnpl_enabled =
False`, and the peer channel is inert in that arm, so **no re-calibration is needed** and the CCMR
comparison, pattern 3 and pattern 4 all stand exactly as reported. Everything BNPL-on must be
re-run.

### B28 · Want-driven purchases were partly funded by money that did not exist — `MAJOR` · `AGENT` · `CLOSED`

Found 2026-08-12 reading `agents.py` during the QA pass. In the tick, discretionary spending leaves
`cash >= 0`, then:

```python
cash -= self._bnpl_purchase()   # could drive cash NEGATIVE
...
self.savings = max(cash, 0.0)   # and the negative was silently discarded
```

The checkout instalment — 25% of the purchase under D13 — was deducted **without any check that the
household had it**, and the resulting negative balance was floored away at the state update. A
household with R0 could make a R1,568 purchase and "pay" the R392 checkout debit out of nothing. No
arrears were recorded, and D7 distress is assessed earlier in the tick, so nothing caught it.

**Why it mattered beyond tidiness.** The leak is proportional to purchase size, so it was largest
exactly where purchase size was least plausible (B30, the Q1 households), and it **inflated BNPL
volume and suppressed measured distress simultaneously**. Part of the purchase-size sensitivity in
**B24** was therefore an artefact of a budget constraint that was not being enforced.

**Closed by enforcing D13's own mechanics rather than by patching.** Both SA providers debit a card
at checkout and decline if it fails, so the order is truncated to `cash × n_instalments` and
abandoned outright if `cash <= 0`. That is a *sourced* rule, not a guard. Three tests: no purchase
on zero cash, checkout payment never exceeds available cash, and savings never negative across a
full population run.

### B29 · Every BNPL money parameter was nominal in a 2017-Rand model — `MAJOR` · `AGENT` · `CLOSED`

Found 2026-08-12. The thesis states throughout that all values are **2017 Rands** — the NIDS
backbone, the Reg 23A expense table, the CCMR targets, the statutory rates at the 2017 repo rate.
The BNPL parameters were the exception and nobody had noticed:

| Parameter | Was | Vintage | Now (2017 R) |
| --- | ---: | --- | ---: |
| `bnpl_purchase_mean` | R1,568 | 2026 trade press | superseded by B30 |
| `bnpl_order_cap` | R15,000 | 2026 Payflex terms | **R9,927** |
| `bnpl_late_fee_per_tick` | R190 | 2026 Payflex terms | **R125.74** |
| `bnpl_late_fee_cap` | R285 | 2026 Payflex terms | **R188.61** |

South African CPI rose **44%** between the 2017 and 2025 annual averages, so the BNPL side of the
model was denominated roughly 1.4× too high against everything it interacts with. The late-fee pair
matters more than it looks: R285 per missed instalment per loan, across up to four platforms,
against a 2017 median household income of R5,500.

Closed with a single sourced deflator in `data/config/cpi_deflator_2017.json`, generated by
`notebooks/scripts/extract_cpi_deflator.py`, applied once in `config.py` so a published nominal
figure and the 2017-Rand value the model uses cannot drift apart. The product *mechanics* — four
instalments, fortnightly, zero interest, a three-week fee cap — are vintage-free and unchanged.

⚠ `% VERIFY` stands on the deflator itself: the annual averages come from published Stats SA
releases and are not yet re-derived from **P0141 Table B1** index numbers. The 2024 figure is
asserted against Stats SA's own published 4,4% statement. **Pin the full series before quoting the
factor in the thesis.**

**Worth reporting, not just fixing.** This is the fourth instance of the pattern already recorded
for B15, B17 and B18, and the cleanest: the specification was not merely silent, it was internally
inconsistent with a stated global convention that the rest of the model obeyed.

### B30 · Flat national constants imposed on a population with a Gini of 0.67 — `MAJOR` · `AGENT` · `CLOSED`

Found 2026-08-12. This is the substantive half of **B24**, and it turned out to be a specification
error rather than a sourcing gap. Measured on the model's own banked households:

| Quintile | Median monthly income | R1,568 as % of income | R1,568 as % of discretionary | R5,000 limit as % of income |
| --- | ---: | ---: | ---: | ---: |
| Q1 | R2,300 | **68.2%** | **127.0%** | **217.4%** |
| Q3 | R4,700 | 33.4% | 79.0% | 106.4% |
| Q5 | R27,000 | 5.8% | 11.4% | 18.5% |

The model had the poorest banked households making single BNPL purchases worth **more than their
entire monthly discretionary budget**, on a rolling facility worth **more than two months of income
at each of four providers independently**. A flat constant that is non-binding for Q5 and absurd for
Q1 will move the answer enormously when slid across a range, which is a large part of why these two
parameters topped the sensitivity ranking, and it is the likely mechanism behind **B25**'s
implausible volumes.

**Closed by making both parameters ratios applied to household characteristics.**

*Purchase size.* `purchase_i ~ LogNormal(mean = kappa × discretionary_monthly_i)`, with **kappa =
0.1387 DERIVED from Stats SA IES 2022/23 COICOP microdata** — the share of a household's
discretionary budget spent on the categories BNPL actually finances (clothing and footwear,
furniture and appliances, ICT devices, recreational durables). Only a ratio is taken from that
survey, never a money amount, so the 2022/23 vintage cannot contaminate a 2017-Rand model — the
identical argument already accepted for the FinScope 2019 categorical flags.

*Rolling limit.* `limit_i = lambda × income_monthly_i`, lambda = 0.25, per household rather than per
platform. Income and **not** Reg 23A capacity: D11's whole point is that the BNPL screen is
deliberately not the statutory test, and setting BNPL limits from statutory capacity would quietly
dissolve the asymmetry the thesis exists to study.

**⚠ The convergence is the result here, and it is unfitted.** kappa comes from Stats SA expenditure
microdata. The check comes from a listed issuer's disclosed BNPL GMV and transaction count. Nothing
was tuned to anything:

| Quantity | 2017 Rands | Source |
| --- | ---: | --- |
| Model's drawn mean purchase (kappa × mean discretionary) | R1,029 | IES 2022/23 |
| **Realised mean purchase, after limits and the checkout guard bite** | **R872–R883** | model output |
| **Average order value, PayJustNow** | **R992** | R13.1bn GMV / 9.4m transactions |
| Average basket, trade press | R1,038 | the superseded source, now corroboration |

The two independent South African sources land 4.6% apart, and the model's realised mean sits just
below both, which is the right side to be on — real orders are truncated by limits too. `test_bnpl_parameters.py`
asserts this as a standing validation check.

**Also closed: the volume anchor the thesis never had.** HomeChoice discloses BNPL frequency of
**2.12 purchases per customer per annum**, giving **R2,103 per user per year in 2017 Rands**. B25's
"these volumes look implausible" now has a number behind it.

### B31 · The `s_g` denominator would have corrupted the Granovetter arm — `MAJOR` · `AGENT` · `CLOSED`

**Closed 2026-08-13 as Option A.** `_recompute_group_shares` now divides by the group's
**BNPL-eligible** members rather than all its members. `s_g` therefore means *"what share of the
people who could use BNPL are using it"* — which is also closer to what a household actually
observes — and its ceiling no longer moves with `bnpl_access_rate`.

**Measured effect:** peak `s_g` across the run rises from ~0.53 to **0.96** at `beta = 1`. A
Granovetter threshold drawn on `[0, 1]` is now meaningful across the whole range, and the access
sweep no longer moves the maximum attainable signal alongside the axis under test.

⚠ **This rescales `beta`**, so linear-arm results are not comparable across the change. Everything
BNPL-on is being re-run regardless.

**A second determinism fix landed with it.** Drawing `theta_i` from the model's main random stream
would have shifted every subsequent draw, so `gamma = 0` could only have matched the linear control
*in distribution*, not bitwise. Agent endowments are now drawn from a **separate `init_rng`**
stream. Two payoffs: `gamma = 0` reproduces `beta = 0` **exactly**, and sweeping `sigma_theta`
changes only the thresholds while leaving every shock, purchase and friction draw identical — which
makes the D17 dispersion sweep a **paired** comparison rather than a noisy one.

Tests: `test_peer_channel.py`, eleven of them, including that the signal reaches high values at 15%
access and that the linear arm draws no thresholds at all.

### B31-original · The `s_g` denominator will manufacture a false negative — historical record

Raised 2026-08-12 during the QA pass, **before** the threshold variant is built, which is the point
of raising it now.

`_recompute_group_shares` in [`model.py`](../simulation/model.py) computes the reference-group
adoption share over **all** group members, including the unbanked and the BNPL-ineligible. `s_g` is
therefore structurally capped at each group's **eligible share**, which is
`banked_share_g × bnpl_access_rate`.

**⚠ Measured 2026-08-12, and the first statement of this issue overstated the magnitude.** The claim
that `s_g` peaks near 0.5 came from reading the population-wide adoption rate, which averages over
groups and over time. The per-group peaks are much higher. At full access:

| | min | median | max |
| --- | ---: | ---: | ---: |
| Structural ceiling (eligible share by group) | 0.444 | 0.836 | 1.000 |
| Peak `s_g` actually reached, β=1 | 0.200 | **0.650** | 0.898 |
| Peak `s_g` actually reached, β=3 | 0.322 | 0.681 | 0.939 |

37 of 45 groups exceed 0.5 at β=1. So thresholds drawn on `[0, 1]` would **not** leave half the
population untriggerable. That version of the concern is withdrawn.

**Two real problems survive the correction, and the second is the serious one.**

1. **The ceiling varies across groups** (0.444 to 1.000, driven by each group's banked rate, which
   correlates with income). An identical `theta_i` therefore means a different thing in a
   low-banked group than in a high-banked one, so the threshold mechanism acquires a group-level
   heterogeneity that was never intended and that is correlated with the income dimension RQ2 and
   RQ3 already cut on.
2. **The ceiling is proportional to `bnpl_access_rate` — which is RQ2's own x-axis.** At
   `access = 0.15` the eligible share within a group is about `0.15 × 0.83 ≈ 0.125`, so **no
   threshold above ~0.125 can fire anywhere on that arm**, by construction. Sweeping access
   therefore sweeps the *maximum attainable value of the peer signal* at the same time, and a
   threshold model would produce a response to access that is partly an artefact of the ceiling
   moving with the axis. That is precisely the shape of result RQ2 is asking about, so it would be
   **indistinguishable from the finding**.

Under **linear** coupling none of this bites: the denominator is absorbed into `beta`, which is
swept and uncalibrated, and a rising ceiling with rising access is arguably the desired behaviour
(more access really does mean more visible usage). It bites only under thresholds, where `theta_i`
is a fixed number compared against a signal whose maximum moves.

**Decided 2026-08-13: Option A**, implemented as recorded above.

- **Option A — normalise `s_g` by the group's eligible share.** ✅ **CHOSEN.** `s_g` then means "what
  share of the people who *could* use BNPL are using it", which is arguably the quantity a household
  actually observes, and it removes both problems at once. ⚠ It changes the meaning of `beta`, so the
  linear arm must be re-run too — cheap, since everything is being re-run anyway.
- **Option B — draw `theta_i` on each group's attainable range.** Rejected. Keeps `s_g` as-is and
  leaves the linear arm untouched, but makes `theta_i` group-dependent, which muddies the
  Granovetter reading of "the *variance* of thresholds decides whether a cascade occurs".

### B24 · The two most influential parameters are the two worst-sourced — `MAJOR` · `BOTH` · `OPEN`

Robustness suite, 520 runs. Ranked by movement in population default:

| Parameter | Range | Default rate | Movement | Provenance |
| --- | --- | --- | --- | --- |
| `bnpl_purchase_mean` | R784 – R3,136 | 45.07% → 64.68% | **19.6pp** | **trade press, `% VERIFY`** |
| `bnpl_platform_limit` | R1,000 – R15,000 | 39.61% → 56.48% | **16.9pp** | **unsourceable (B16)** |
| `amount_rule` | 3 variants | 48.55% → 56.04% | **7.5pp** | **uncited (D4)** |
| `k_default` | 4 vs 7 | 58.73% → 56.05% | 2.7pp | sourced |
| `min_payer_share` | 0.20 – 0.40 | 56.02% – 56.27% | **0.25pp** | sourced (US transfer) |
| `min_payment_frac` | 0.025 – 0.10 | 55.90% – 56.11% | **0.21pp** | uncited (B15) |
| activation order | 3 regimes | 56.08% – 56.26% | **0.18pp** | sourced |
| population size | 1k / 5k / 10k | 55.80% – 56.22% | 0.42pp | — |

**Good news, and it retires two worries.** The **B7** transfer concern is largely defused: the
minimum-payer share barely matters over 0.20–0.40. **B15**'s newly-found uncited minimum-payment
formula also barely matters. And **D16's** prediction that the peer channel is activation-order
independent by construction is **confirmed empirically**, not merely asserted.

**Bad news, and it is the headline.** The model's output is driven mainly by **BNPL purchase size**
and the **per-platform rolling limit** — respectively a trade-press figure and a quantity no South
African provider publishes. Both must be reported as first-order sensitivities in Chapter 6, not
buried in a robustness appendix, and every RQ2/RQ3 magnitude must be stated as conditional on them.
Finding a better source for either would do more for the thesis than any further modelling.

**⚠ UPDATE 2026-08-12 — the diagnosis was right, the attribution was wrong, and the fix is in.**
"Worst-sourced" turned out to be only half the story. Both parameters were also **flat national
constants imposed on a population with a Gini of 0.67** (**B30**), one of them denominated in the
wrong year's Rands (**B29**), and one of them interacting with an unenforced budget constraint
(**B28**). A constant that is non-binding for Q5 and absurd for Q1 will dominate an OFAT ranking
whatever its citation says.

Both are now **ratios applied to household characteristics**: kappa derived from Stats SA IES
2022/23, lambda reported against an external band from Woolard and ASIC. The tornado and Sobol
tables above are therefore **superseded and must be regenerated**, and the sweep bounds in
`experiments.py` and `sensitivity.py` are now ranges on the ratios rather than on Rand amounts.

**The open question this leaves is a good one.** If purchase size still ranks first once it is a
data-derived ratio rather than a flat trade-press constant, that is a *structural* sensitivity worth
reporting as a finding. If it drops down the ranking, the original result was largely an artefact of
a badly chosen parameterisation. **Either answer is reportable and neither is known yet** — it
arrives with the re-run. Do not restate B24's headline until it does.

### **✅ ANSWERED 2026-08-13 by the 950-run supervisor-update sweep. B24 is CLOSED.**

The original result was largely an artefact of the parameterisation. Both parameters fell out of the
top of the ranking:

| Parameter | Old range | New range | Rank |
| --- | ---: | ---: | --- |
| BNPL purchase size | 19.6pp | **2.06pp** (kappa 0.07–0.28) | 1st → 4th |
| Per-provider limit | 16.9pp | **0.18pp** (lambda 0.1–1.0) | 2nd → last |
| `amount_rule` (D4, uncited) | 7.5pp | **4.11pp** | 3rd → **1st** |
| `k_default` | 2.7pp | 1.97pp | — |
| Purchase base (new arm) | — | 1.03pp | — |

⚠ **Replicate noise at 5 reps is 0.33pp (sd), so anything under ~0.67pp is not distinguishable from
noise.** `lambda` at 0.18pp is therefore **inert**, and that needs stating carefully: the limit binds
on 54% of requests but barely moves default, because a constrained household simply borrows less per
purchase rather than defaulting less. Report both facts together or it reads as a contradiction.

**The new leader is `amount_rule`, and the number is smaller than it looks.** The three arms are
28.91% (shortfall), 28.24% (+25%), **24.80%** (shortfall plus committed). The first two agree to
within 0.67pp, exactly the noise floor; the whole range comes from the third and most generous
variant. So this is not "the answer swings on an invented rule" — it is "two plausible variants
agree and one outlier pulls the range".

**It also points somewhere real.** `amount_rule` governs the shortfall-driven path, which D5 records
as the one place BNPL draws are still uncapped relative to what the product could plausibly finance.
The tornado found independently what the code review found structurally. **Capping that draw is now
the highest-value remaining modelling decision**, and the continuous-buffer sweep proposed in PLAN
should replace the three discrete variants.

The tornado and Sobol tables above are superseded. ⚠ **The Sobol figure in
`results/summary/figures/` is stale** — it is from the N=64 run on the old parameterisation and was
deliberately not regenerated for this pass. Delete or relabel it before anything is shown.

⚠ Single-seed diagnostics after the fixes, at default access and `q_base = 0.05`, indicate the
change is **large**: population default falls from 32.9% to 27.5% at β = 0 and from 56.1% to 28.0%
at β = 1. Adoption still responds strongly to β (21.5% → 48.9%) but **default barely does**, so
**B22's 4.3× amplification finding is itself now in question**. These are one-seed illustrations,
not results.

**Confirmed by Sobol variance decomposition** (1,024 runs, N=64, 6 parameters), which OFAT could not
have shown. Total-order indices on the population default rate:

| Parameter | S1 | **ST** | interaction (ST−S1) |
| --- | --- | --- | --- |
| `bnpl_purchase_mean` | 0.102 | **0.307** | **0.206** |
| `beta` | 0.189 | 0.255 | 0.066 |
| `shock_prob` | 0.230 | 0.174 | −0.056 |
| `bnpl_platform_limit` | 0.074 | 0.163 | 0.090 |
| `q_base` | −0.029 | 0.033 | 0.062 |
| `min_payment_frac` | 0.002 | **0.0006** | −0.001 |

Two things OFAT missed entirely:
- **Two-thirds of `bnpl_purchase_mean`'s influence is INTERACTIVE** (ST−S1 = 0.206). It does not
  merely shift the level; it changes how the other parameters act. On BNPL adoption the interaction
  term is larger still (0.402 of ST 0.533).
- **`min_payment_frac` has ST ≈ 0.0006**, i.e. it is essentially inert. **This retires B15 as a
  substantive concern** — the newly-found uncited rule should still be disclosed, but it cannot be
  driving any result. The same holds for the B7 minimum-payer transfer.

⚠ **Confidence intervals are wide at N=64** and several S1 estimates come out slightly negative, a
known small-sample artefact. The *rankings* are stable across all five outputs, but the point
estimates are not publication-grade. **Re-run at N≥256 before quoting numbers in the thesis**
(`python -m simulation.sensitivity --samples 256`), which is roughly 4x the compute.

### B25 · High-beta arms produce implausible BNPL volumes — `MINOR` · `BOTH` · `OPEN`

At full access and `beta = 1`, cumulative BNPL volume reaches **R31,097 per eligible household over
40 post-burn-in ticks**, roughly R2,000 per month against a median household income near R4,800.
Adoption reaches 49% and population default 56%.

These are mechanistic illustrations, not plausible states, and the upper reaches of the RQ2 surface
should be labelled as such. It is consistent with OVERVIEW §1a (results are directional and
mechanistic, never forecasts), but the point needs making where the surface is presented, since a
reader will otherwise read 56% default as a prediction.

### **MEASURED 2026-08-13. The assertion now has a number behind it, and the control arm passes.**

The volume anchor derived from Weaver's disclosures gives a band of **R1,333 to R4,261 per user per
year** in 2017 Rands. Against it, over ~15 post-burn-in months:

| Arm | BNPL volume per eligible household | Verdict |
| --- | ---: | --- |
| `beta = 0` | **R3,015** | **inside the band** |
| `beta = 1` | R13,767 | 3.2× the upper bound |

So the control arm now passes an external volume check it was never fitted to, and the high-beta
arm's implausibility is **quantified** rather than asserted. Report the multiple, not just the
adjective. Mean realised purchase is R893 against the R992 anchor, about 10% low, which is expected
since limits truncate orders.

### B26 · Three external checks passed that were NOT fitted — `NOTE` · `AGENT` · `CLOSED`

Worth recording as positives alongside the problems above:

- **Stacking depth versus CFPB.** At full access and `beta = 1`, **37%** of households hold two or
  more concurrent facilities, against the CFPB's **32%** holding loans across different firms.
  Order-of-magnitude agreement, US-to-SA transfer stated — and **emergent, not imposed** (D12).
- **The D11 binding checks pass.** The R15,000 order cap binds on **0.3%** of requests, confirming
  D11's prediction that it would rarely bind at LMI incomes. The rolling limit binds on **5.6%** at
  R5,000, so it is largely inert at that value — though B24 shows it is *not* inert at R1,000.
- **Internal consistency.** BNPL enabled at zero access reproduces the BNPL-disabled baseline
  (24.43% versus 24.56% default), and adoption is exactly zero, confirming the injection design.

---

### B32 · Two calibration checks moved when P0 stopped counting imputed rent — `MAJOR` · `BOTH` · `OPEN`

`w5_expenditure` decomposes exactly into `w5_expf + w5_expnf + w5_hhimprent + w5_rentexpend`. P0
built `expenditure_discretionary` as total less food less rent, which leaves **`w5_expnf` plus
imputed rentals** — the consumption value of owner-occupied housing, carried by **82.6%** of
households at a median of **R700/month**, and not cash. Agents could therefore compress a
non-existent flow to service debt. Discretionary spending was inflated by ~78% at the median
(R2,105 against R1,336). Fixed 2026-08-18; P0–P4 re-run.

Two consequences, both of which were previously masked:

- **`test_realised_mean_purchase_lands_near_the_sa_provider_anchor` now fails**, R629 against the
  R992 Weaver anchor. The old agreement was an artefact: IES `kappa` was already computed on an
  imputed-rent-free denominator (`ies_2022_bnpl_share.json`), so the two sides were mismatched and
  the inflation happened to close the gap. The means are over **different populations** — R992 is a
  provider's own customers, which `kappa` puts at ~R7,151 monthly discretionary, the Q4/Q5 boundary
  and above 80% of banked agents; banked Q4 alone gives R613 and Q5 R2,186. Marked `xfail(strict)`.
  **Resolving it means choosing the comparison population, which is a design decision, not a
  tolerance.**
- **Every arrears/default result shifts**, since discretionary spending is the buffer compressed
  before an instalment is missed. A smaller buffer means less absorption, so the fitted shock
  probability should re-fit **lower** — this bears directly on **B20**.

**Update 2026-09-21 — re-calibrated; the prediction held.** `python -m simulation.calibrate
--reps 20` on the rebuilt population: shock probability **0.048 → 0.040**, payment friction
unchanged at **0.09**. Fitted bands 13.96% (90+, target 14.21%) and 8.32% (1–30, target 8.24%);
**unfitted 60+ 15.01% against 16.54%**; the 31–60 and 61–90 bands stay underpopulated at ~1.1%
each (B21 stands). The ratio to the QLFS upper bound falls from 4.1x to **3.4x** (B20 eases, does
not close). Zero-savings rate falls from 45.6% to **32.1%**, against TransUnion's 36% (Pattern 4).
`FITTED_SHOCK_PROB` in `experiments.py` is updated; **nothing in `results/raw` has been re-run
yet** — every sweep there still predates this fix and must not be quoted. `sensitivity.py` was
also found to decompose variance about an *uncalibrated* baseline (payment friction at its 0.0
default); it now starts from `calibrated()`.

**The mean-purchase gap, diagnosed (2026-09-21).** Same configuration as the xfail test, recorded
per want-driven purchase. The rolling limit is **not** the cause: requested and financed means are
identical at λ = 0.10, 0.25 and 10, because a purchase routes across four platforms. The gap is
entirely **who buys**. Adoption propensity is uniform across eligible households, so transactions
spread almost evenly over quintiles (16–24% each) while purchase size scales with budget:

| Quintile | Share of transactions | Mean order | Share of GMV |
| --- | ---: | ---: | ---: |
| Q1 | 16% | R113 | 3% |
| Q2 | 18% | R158 | 4% |
| Q3 | 23% | R258 | 9% |
| Q4 | 21% | R390 | 13% |
| Q5 | 23% | R1,932 | 70% |
| **All adopters** | | **R629** | |

Restricted means: Q3–Q5 **R875** (−12% on the R992 anchor), Q4–Q5 **R1,195** (+20%). **No source
in the repo gives the income profile of a South African provider's customers** (Weaver IAR, the
TransUnion pulse and the anchors file were checked), so any restricted comparison population
would be chosen by looking at the answer. ~~Decision still open and Marc's~~

**Decided by Marc, 2026-09-21: all adopters.** The comparison, statistic, target and tolerance
(within 35% of R992, the tolerance the test had carried since 2026-08-12) are pre-registered in
`DECISIONS.md` D4, written before the final run. `kappa` is not re-tuned whatever the outcome. The
run now reports purchases by quintile, so the bracket above is reproduced from the final output
and not from a side calculation. The `xfail(strict)` test is replaced by one that pins the
*explanation*: all adopters average below the anchor, and the anchor lies between the Q3–Q5 and
Q4–Q5 means. It deliberately does not assert pass or fail against the tolerance, because on the
full population the all-adopter mean sits 34–36% low, on the edge of the band. **This entry closes
when the final run reports which side it fell.**

---

### B33 · The DSTI validation compared unlike quantities — `MAJOR` · `AGENT` · `CLOSED`

Section 3.3 reported model DSTI of 2.8–6.1% "between" benchmarks of 5.36% and 9.78%. The model
figure was service / gross **income** over **all** households (56% hold no debt); both benchmarks
are shares of **spending** among **credit holders**. Three mismatches at once: denominator,
conditioning population, and mean-versus-median.

On the FinScope denominator, conditioned on debtors, the model gives **12.8% of monthly outlay**
against a 6.07–9.78% band. It sits **above** both, in the direction ceiling APRs predict, not
between them. The NIDS 5.36% figure is also **not independent**: it is built from the same
`w5_h_nfhpspn` / `w5_h_nfclthaspn` variables that set the store-card and hire-purchase terms.

Now check `D. Debt service vs FinScope C8` in P4, and **the one check of eighteen that fails**. It
is reported as a failure in Section 3.5, with traditional debt service stated as an upper bound.
The known double-count (`data/config/README.md`) pushes it further up, not down.

## The 2026-09-21 code review

Found while reviewing `simulation/` for over-engineering and then executing
[`CODE_CLEANUP_PLAN.md`](../CODE_CLEANUP_PLAN.md).

### B34 · Granted traditional loans were never booked as debt — `BLOCKER` · `BOTH` · `CLOSED`

**Closed 2026-09-21, the day it was found. Marc chose option (a), using only figures the repo
already sources.**

- **What is booked.** A granted loan joins the household's one consolidated traditional balance,
  which is how NIDS records debt and how the model already carries it. The balance rises by the
  amount; the rate moves to the balance-weighted mean of the rate carried and the new loan's;
  scheduled service rises by the new loan's level instalment, due from the next tick. The bureau
  shows scheduled service, so each grant uses up Reg 23A headroom and repeated borrowing limits
  itself. `HouseholdAgent._book_trad_loan`; Appendix G gained a `BookLoan` function; the notation
  table moves `r_i` and `iota_i` from constants to state.
- **Terms are read, not retyped.** 28% (repo + 21%) over 25 months (CCMR 2017-Q1 unsecured
  stock-flow life), from the `other_default` row of `credit_rate_table.csv`.
- **Effect at the old fitted parameters** (seed 11, BNPL off): the book now *grows* from R48.2m to
  R52.5m where it used to fall to R39.8m, and 90+ arrears stand at 20.3% against the 14.21%
  target. Hence the refit.
- **Refit** (`simulation.calibrate --reps 20`, grid extended one step down to 0.008 so the optimum
  is interior): **shock probability 0.040 → 0.016; friction 0.09, unchanged.** 90+ 13.96% against
  14.21%; 1–30 8.22% against 8.24%. Unfitted: 31–60 0.94%, 61–90 0.96%, current 75.93%, 60+
  14.91%; zero-savings share 26.0% (was 32.1%); final default rate 13.6%. Pattern 3 still peaks
  mid-distribution (aggregate DTI highest in Q4).
- **The side effect that matters most: B20.** The shock rate had been inflated to produce CCMR
  arrears *in spite of* free credit. It is now **1.4x** the QLFS upper bound, down from 3.4x.
- **Tests:** a grant is booked (balance, service, blended rate); a refusal books nothing; three
  loans each worth 40% of headroom give granted, granted, refused. 95 passed.
- **Still true and now recorded under DECISIONS D7:** cash raised against a committed-expenditure
  shortfall is not spent on it. That is a separate question from this defect and was not changed.

*The entry as first written follows.*

`TraditionalLender.apply` returns the granted amount and `_seek_credit` adds it to cash. Nothing
increases `d_trad` or `scheduled_service_tick`, so a new traditional loan is a **non-repayable
transfer**: no balance, no interest, no instalment. Because the Reg 23A gate reads visible service
from `scheduled_service_tick`, a grant also leaves the household's headroom untouched, so the same
household passes the same test again next tick. Appendix G's `LenderApply` has the same omission,
so the pseudocode agrees with the code and both disagree with D10 ("the lender observes its own
outstanding loans to that household").

Measured on the calibrated baseline, seed 11, full population, 52 ticks:

| Arm | Loans granted | Households | Cash granted, never booked | Share of opening debt book | Share of all income |
| --- | ---: | ---: | ---: | ---: | ---: |
| BNPL off | 10,562 | 1,214 | R9.96m | 20.7% | 0.68% |
| BNPL on, beta 1 | 7,555 | 1,186 | R6.24m | 13.0% | 0.42% |

1,084 of the 1,214 households are granted five or more times; one is granted in all 52 ticks. The
closing traditional book *falls* from R48.2m to R39.8m while R10m of new lending vanishes.

**Why it matters.** (1) BNPL loans *are* booked and repaid, so the comparison the thesis exists to
make is asymmetric by construction: one credit class costs something and the other does not.
(2) `shock_prob` and `payment_friction` were fitted with free credit in the baseline. (3) It makes
any "distress assessed after credit" rule meaningless, which is why the `distress_after_credit`
robustness arm proposed in the cleanup plan (decision B2) was **not** implemented.

**Options, Marc's decision.** (a) Book the loan: add the amount to `d_trad`, add the 28% / 25-month
instalment to scheduled service, and settle how interest accrues on a balance that now mixes the
household's product-mix APR with the new-loan APR; then re-run `simulation.calibrate`, update
`FITTED_*`, Appendix G and the tests. A full-population run takes about 3 seconds, so the refit is
minutes, not a night. (b) Run as is and disclose new traditional credit as a transfer. **Do not
start the final run before choosing.**

### B35 · The "synchronous" activation arm was the "uniform" arm — `MAJOR` · `AGENT` · `CLOSED`

Agents are created in `agent_id` order, so the unshuffled sweep (`"synchronous"`) and the
sort-by-id sweep (`"uniform"`) were one schedule. `rob_act_uniform` and `rob_act_synchronous` were
bitwise identical on every seed in `results/raw/robustness.parquet`, while the thesis reported two
distinct activation checks. **Closed 2026-09-21** by removing the duplicate arm (saves 20 runs) and
rewording Submodel 17, Appendix B (regenerated) and Appendix C to the one fixed-order check that
exists. Genuinely simultaneous updating is not implemented and is not claimed.

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

*Note, 2026-09-21:* both notebooks were deleted in the code cleanup. They read three FinScope
columns no parquet has carried since the flag set was cut to `banked` plus `G10`–`G14`, so neither
ran. The data-layer figures now come from `notebooks/scripts/build_data_figures.py`, and both
notebooks remain in git history.

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
`scratchpad/DECISIONS.md` already holds most of this material and can be adapted directly.
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
