# PLAN — what happens next

**One of three working documents.** [`DECISIONS.md`](DECISIONS.md) is *what was chosen and why*.
[`DEFECTS.md`](DEFECTS.md) is *what is wrong or was wrong*. [`PLAN.md`](PLAN.md) is *what happens
next*. Consolidated 2026-08-13 from `PLAN.md`, `PLAN.md` and `literature.md`.

Canonical strategy: [`../OVERVIEW.md`](../OVERVIEW.md).
Plain-language explanation of the project: [`../THESIS_GUIDE.md`](../THESIS_GUIDE.md).

---

## Where things stand, 2026-08-13

The model is **built, verified, calibrated, and has produced a first full set of results**. A QA
pass on 2026-08-12 then closed the project's principal methodological weakness and fixed three
further defects. **79 tests pass.**

**The baseline is not at risk from any outstanding work.** `shock_prob` and `payment_friction` are
fitted with `bnpl_enabled=False`, and the peer channel is inert in that arm, so there is **no
re-calibration**. The CCMR arrears comparison, pattern 3 and pattern 4 stand exactly as reported.
Everything BNPL-on must be re-run.

**The binding constraint is the write-up, not the model.** Chapters 5, 6 and 8 are empty headings
and there is no front matter. That is the only thing that can stop submission.

---

## The sequence

**Current position: writing.** The decision taken 2026-08-13 is to refine the existing chapters and
write Chapter 5 before returning to the simulation. This is the right order — Chapter 5's content
(architecture, tick order, parameter register, verification summary) depends on none of the
outstanding decisions, and writing it is the fastest way to actually own the model.

| # | Step | Status |
| --- | --- | --- |
| 1 | Fix the cool-off off-by-one (B27) | **done** 2026-08-12 |
| 2 | Enforce the checkout budget constraint (B28) | **done** 2026-08-12 |
| 3 | Deflate all BNPL money parameters to 2017 Rands (B29) | **done** 2026-08-12 |
| 4 | Derive purchase size and the rolling limit from household characteristics (B30) | **done** 2026-08-12 |
| 5 | Pin the two `% VERIFY` sources | **done** 2026-08-13 |
| 6 | Settle `lambda` at 0.10; settle the shortfall path | **done** 2026-08-13 |
| 7 | Implement Option A for `s_g` (B31) | **done** 2026-08-13 |
| 8 | Build the Granovetter threshold arm | **done** 2026-08-13, 91 tests pass |
| 9 | Supervisor-update run: 950 runs at 5 reps, all figures | **done** 2026-08-13 |
| 10 | **Refine chapters; write Chapter 5** | **in progress** |
| 11 | Cap the shortfall draw; continuous `amount_rule` sweep | proposed, see below |
| 12 | Final run at 20 reps + Sobol at N >= 256 | after step 11 |
| 13 | Write Chapter 6 once, against final numbers | after step 12 |

**Do not draft Chapter 6 before step 12**, or it will be written twice.

The 2026-08-13 run was a **supervisor update, not the final report**: 5 replicates, no Sobol.
Replicate noise is 0.33pp (sd), so **nothing under ~0.67pp is distinguishable from noise** at that
setting. Results are in [`../STATUS.md`](../STATUS.md).

### The one substantive change the run argues for

`amount_rule` is now the largest sensitivity at 4.11pp, and it governs the **shortfall-driven BNPL
path** — the one place D5 records that draws are still uncapped relative to what BNPL could
plausibly finance. The tornado found by measurement what the code review found structurally, which
is a good reason to act on it.

Two changes, both small:

1. **Cap the shortfall draw** at the household's monthly BNPL-financeable budget, the same quantity
   that already sizes want-driven purchases. Expected to shrink this sensitivity, because the
   outlier arm is the most aggressive borrower.
2. **Replace the three discrete `amount_rule` variants with a continuous buffer parameter** and
   sweep it, so the thesis can say *where* the sensitivity lives rather than reporting three points.
   Note that the first two variants currently agree to within the noise floor; the whole 4.11pp
   range comes from the third and most generous one.

---

## Decisions taken 2026-08-13

### `lambda` = 0.10 — the rolling-limit multiple

`rolling_limit_i = lambda x income_monthly_i`, applied at **each** of four platforms independently.

| Source | Published figure | As a share of median monthly household income | Per provider |
| --- | --- | --- | ---: |
| Woolard (UK, 2021) | ~GBP1,000 invisible BNPL debt, a **stacked total across providers** | ~37% | ~0.09 |
| Afterpay (AU) | initial limit ~A$600 | ~8% | ~0.08 |
| Afterpay (AU) | maximum limit ~A$2,000 | ~26% | ~0.26 |

**The reasoning, recorded because the value is not derived.** The limit applies at each platform
independently, so what the evidence actually measures is the **stacked total**. Woolard's figure is
a total across all providers, about 0.09 each across four. At `lambda = 0.25` the model's stacked
total was 1.0x monthly income, ~2.7x what Woolard called "relatively easy to accrue". Since
cross-provider stacking *is* the thesis's subject, and Woolard measures precisely that quantity,
0.10 is the value that makes the model's aggregate match the only measurement of it. Afterpay's
initial limit puts 0.10 at the conservative end of the range.

⚠ **Consequence, to be reported not hidden:** the limit now binds on **54% of requests** at beta=0
(Q1 53%), against 25% at 0.25 and 5.6% under the old flat R5,000. It has become a first-order
constraint. That is what the anchor implies; the 0.1-1.0 sweep demonstrates how much it matters.

Unlike `kappa`, `lambda` is **not derived** — no SA provider publishes a rolling limit (B16). Its
provenance is `ASSUMPTION`, reported against a band the way `shock_prob` is reported against QLFS.
⚠ The income denominators in that table are the author's arithmetic and must be pinned to each
jurisdiction's official household income statistic before the band is published.

### The shortfall-driven BNPL path — left unchanged

The want-driven path is anchored to the household's own budget; the shortfall path requests the full
shortfall, bounded only by the order cap and the rolling limit. That asymmetry is **disclosed rather
than fixed**: capping it would be a design change to a registered rule on the eve of a re-run. The
model is therefore permissive about how much distress BNPL can relieve, which biases its estimated
effect on default **upward** — the conservative direction for this thesis. See DECISIONS D5.

### Both `% VERIFY` sources are now pinned

**CPI.** The **June 2026 P0141 release** supplies a published mid-year anchor — headline index
**107.5** (Dec 2024 = 100) and **5.0%** year-on-year — replacing the part-year guess. The reasoning:
an annual average sits at the mid-point of its year, so the 2025 annual average *is* the mid-2025
price level, and June 2026 is twelve months later, so the published year-on-year rate is exactly the
multiplier. The factor is unchanged at **1.5111**, but it is now derived rather than assumed.

The release also gave a **drift check on the whole chain**: compounding the 2018-2025 annual
averages forward implies a June 2026 index of 106.7 against the published 107.5, a **-0.77% gap**,
which bounds the deflator error at well under one per cent. The `% VERIFY` on the 2018-2025 series
is now *narrow* — two independent checks constrain it — rather than open-ended.

**Weaver.** The **Integrated Report 2025, page 14** is now the primary source and it settles
everything on one panel: cumulative BNPL GMV **R13.1bn**, cumulative transactions **9.4m**,
**3.7m signed-up customers**, and an annual frequency series of **1.8x, 2.2x, 2.8x, 3.9x, 4.4x**
(FY2021-FY2025). The average order value of **R992 in 2017 Rands** is confirmed. The FY2024 annual
GMV series reproduces this report's cumulative chart at every shared year.

⚠ **The R7,000 / 2.12 discrepancy is resolved and the figure is dropped.** It is a **group-wide**
fintech metric — Weaver cross-sells lending, a wallet and insurance alongside BNPL, so R7,000 across
2.12 transactions describes a blended portfolio, not a BNPL basket. Read as an order value it would
imply R3,302, anomalously high for South African apparel and homeware checkouts. The FY2025 report
supersedes it with a BNPL-specific frequency series.

**The volume anchor is now a BAND**, because the frequency rate's denominator is not defined in the
source: **R1,333 per signed-up customer per year** (FY2025 GMV / 3.7m, most of whom are dormant) to
**R4,261 per active customer per year** (4.4 x R992), both in 2017 Rands. Compare the model's volume
per *adopting* household against the upper bound and per *eligible* household against the lower.

⚠ Entity renamed: HomeChoice International plc is now **Weaver Fintech Ltd (JSE: WVR)**. FY2024
documents carry the old name, FY2025 documents the new one.

---

## The RQ2 position, stated before the re-run

**Registered claim:** population default responds non-linearly to BNPL access, but only where social
transmission is present. **Result: not supported.** Every arm is near-linear including the beta=0
control (linear R-squared 0.9992).

**The researcher's position, 2026-08-13: the hypothesis should be falsified**, and there is a
structural reason stronger than the empirical one.

**The model has no contagion channel for distress — only for adoption** (B1). Households observe how
many peers are *using* BNPL. Nothing propagates distress: one household's default does not reduce
another's income, tighten another's credit, or impair a lender balance sheet. A genuine tipping
point requires positive feedback in the **outcome** variable; this model has feedback in the input
and none in the output. It is therefore *structurally incapable* of the non-linearity RQ2 asks
about, which is a far better basis for a negative than "the line looked straight".

**Two claims must be kept separate**, because RQ2 currently conflates them:

| | Question | Expected |
| --- | --- | --- |
| (a) | Does **adoption** tip? | Plausibly yes — that is what heterogeneous thresholds do |
| (b) | Does **default** respond non-linearly to access? | Probably no — nothing converts an adoption jump into a disproportionate distress jump |

The QA diagnostics already hint at the split: beta moved adoption 21.5% to 48.9% while default moved
27.5% to 28.0%.

**A prediction recorded before the run.** With income-scaled limits the rolling limit binds on 35% of
Q1 requests. As access rises, more low-income households gain BNPL and hit their limits — a
*saturating* mechanism. So if the corrected model deviates from linear at all, expect **concavity**
(diminishing returns to access), not the convexity the registered hypothesis expected.

**The literature supports the prior.** de Haan finds BNPL raises credit-card interest and fees, a
*level* effect. CFPB documents stacking prevalence, not thresholds. No study documents a tipping
point in BNPL-driven default.

**The likely reportable answer:** *BNPL's effect on default is roughly proportional to access and
largely insensitive to social transmission; social transmission determines who adopts, not who
defaults.* Policy reading: eligibility rules matter more than peer-driven demand.

---

## After the re-run

1. **Regenerate the tornado and Sobol tables.** Both are superseded (B24). The open question is
   whether purchase size still ranks first now that it is a data-derived ratio rather than a flat
   trade-press constant. If it does, the sensitivity is structural and is a finding; if it does not,
   the original result was largely an artefact of a bad parameterisation. **Either answer is
   reportable and neither is known.**
2. **Sobol at N >= 256.** Current indices come from N=64 with wide confidence intervals and several
   slightly negative S1 estimates. Rankings are stable, point estimates are not quotable.
   `python -m simulation.sensitivity --samples 256`.
3. **Add the plausibility band to the RQ2 figure**, anchored to the TransUnion ~20% BNPL-intention
   figure, and label everything outside it as mechanistic extrapolation (B25). The BNPL volume
   anchor (~R2,103 per user per year, 2017 Rands) is now the harder check.
4. **Re-check B20.** The fitted shock rate was 4.1x the QLFS upper bound. The corrected parameters
   change how much stress BNPL contributes, so the fitted `shock_prob` may move.

---

## Optional, and currently declined

- **"Low and grow" dynamic limits.** HomeChoice's audited disclosure licenses a limit that *rises
  with repayment history* — arguably the true mechanism behind invisible cross-provider exposure.
  ~20 lines. Declined for now: it adds a dynamic on the eve of a re-run.
- **The reciprocal-bureau lever (RQ3 lever 5).** Bureau visibility currently does nothing (B23)
  because it is only half a bureau: platforms neither report to it nor query it. A lever forcing
  both would attack cross-firm stacking directly and is what the FCA's PS26/1 perimeter move
  implies. Expected to bite hardest. Declined because word count, not model richness, is the
  binding constraint.

---

## Word budget: 16,000 words

Tighter than any modelling question. There is more machinery here than 16,000 words can carry, so
the task is **demotion, not deletion**.

**First: confirm with the supervisor what counts.** Whether appendices, tables, figure captions and
the bibliography fall inside the limit changes everything below.

| Chapter | Words | Note |
| --- | ---: | --- |
| 1 Introduction | 1,200 | state the counterfactual framing once, not three times |
| 2 Literature | 1,800 | already drafted; compress |
| 3 Data | 1,800 | DECISIONS Part II in summary; diagnostics to an appendix |
| 4 Design (ODD) | 2,800 | currently ~3,588. Submodel table stays, prose shrinks |
| 5 Implementation | 1,200 | architecture, tick, parameter register, verification summary |
| **6 Results** | **4,500** | the largest chapter; ~6 figures, not 16 |
| 7 Limitations | 1,200 | B20, B22, B24, B25 are the four that matter |
| 8 Conclusions | 800 | |
| **Total** | **15,300** | ~700 in hand |

**What moves to appendices:** the full verification catalogue (79 tests to one paragraph plus a
table), the complete robustness suite (to the tornado figure plus a table), the Sobol decomposition
(one figure plus a paragraph), the rejected design alternatives, and the full CCMR band table.

**The six figures Chapter 6 should carry:**

1. Baseline arrears profile vs CCMR — the calibration evidence.
2. Pattern 3 debt-to-income by quintile — the statistic-dependence point.
3. RQ2 access x beta surface with the plausibility band — the central figure.
4. RQ2 emergent stacking vs the CFPB benchmark.
5. RQ3 intervention ranking and the defer-vs-desist volume test.
6. Robustness tornado — makes the B24 vulnerability legible in five seconds.

**Lead with the strongest three results, in this order:**

1. **Transparency alone changes nothing.** Closing the reporting gap moves default 0.08pp; an
   affordability duty moves it 4.9pp. Counterintuitive, policy-relevant, about a live regulatory
   question, and currently buried inside RQ3.
2. **The unfitted 60+ arrears band** (15.96% against 16.54%) plus emergent stacking at 37% against
   the CFPB's 32%. Two independent checks the model was never tuned to.
3. **Implementation and QA falsified the specification four times** (B15, B17, B18, B29). A
   methodological contribution most theses cannot claim, because most never check.

⚠ Result 1's magnitudes are pre-QA and will move. The *direction* is a null result and is robust.

---

## Literature strategy (largely executed)

The lit review is drafted at ~1,622 words. The strategy that produced it, retained because the viva
may probe it: every behavioural rule had to be anchored in one of three literatures before being
coded — **ABM of credit and household finance** (how comparable models implement the rule), **BNPL
empirical and regulatory** (what is observed about the behaviour), and **behavioural economics**
(what decision heuristic, rather than rational optimisation, fits). A rule with no anchor is a
flagged limitation, not a silent guess. Two rules ended up with no anchor and are flagged as such:
D4's borrowing amount and D6's minimum-payment formula.

**Outstanding literature task: B9, the novelty claim.** The gap claim rests on a targeted search of
JASSS, JEDC, JEBO and arXiv econ.GN finding no ABM combining a regulated and an unregulated lender
class over a survey-derived population, and no South African BNPL modelling study. **It must be run
systematically, with search strings, databases and dates recorded**, so it can be defended in the
viva. This cannot be delegated — the record has to be the researcher's own.

---

## Supervisor questions, in priority order

1. Does the 16,000-word limit include appendices, tables and the bibliography?
2. **Is a negative result on RQ2 acceptable**, given the registered fallback will have been run?
   Worth asking *before* the re-run, so the answer is not shaped by the result.
3. Which of the four validation targets can be demoted to an appendix?
4. Is there a UCT or departmental LaTeX template? Determines the front matter and numbering.

Bring the robustness tornado figure. It makes the model's main vulnerability legible in seconds, and
having found it yourself is a much stronger position than having it found for you.
