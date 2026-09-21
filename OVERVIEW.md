# Project Overview: Living Source of Truth

**Project:** Modelling BNPL impact on the South African consumer credit market (Agent-Based Model).
**This file is the canonical strategy + execution plan.** When a decision changes, change it here
first, then propagate to the companion docs. Last updated: **2026-09-21**.

> ## Where we are and what happens next (2026-09-21)
>
> The supervisor's September feedback is fully applied (`supervisor_revision_plan.md`, 2026-09-10).
> The live plan is [`SOL_PLAN_REFORMAT.md`](SOL_PLAN_REFORMAT.md): restructure to the reference
> paper's six sections. **The binding gap is the final simulation run** -- everything in `results/`
> predates the population rebuild of 2026-08-18 (DEFECTS B32).
>
> | # | Step | Status |
> | --- | --- | --- |
> | 1 | Cap the shortfall borrowing path (three discrete amount rules kept) | **done** 2026-09-21 |
> | 2 | Re-fit the two calibrated parameters | **done twice** 2026-09-21: on the rebuilt population (shock 0.048 -> 0.040), then again after DEFECTS B34 (**0.040 -> 0.016**, now 1.4x the QLFS upper bound, was 3.4x). Friction 0.09 both times |
> | 3 | Decide the comparison population for the mean-purchase check (B32, R992 anchor) | **decided** 2026-09-21: all adopters, within 35%, pre-registered in `DECISIONS.md` D4 before the run. It sits 34--36% low beforehand, so the run decides pass or named miss |
> | 3a | Code cleanup ([`CODE_CLEANUP_PLAN.md`](CODE_CLEANUP_PLAN.md)): duplicate activation arm removed, every parameter and all six arrears bands echoed in the run output, dead code deleted | **done** 2026-09-21; outputs bitwise unchanged on a four-arm golden run |
> | 3b | DEFECTS B34: granted traditional loans were never booked as debt (R9.96m, 20.7% of the opening book, in one baseline run) | **fixed** 2026-09-21: booked onto the consolidated balance at the rate table's sourced unsecured terms; step 2 re-fitted; Appendix G and the notation table updated |
> | 4 | Final run overnight: `./env/python.exe -m simulation.experiments --which all --reps 20`, then `./env/python.exe -m simulation.sensitivity --samples 256`, then `./env/python.exe -m simulation.analysis` | to do |
> | 5 | Six-section shell; Model and Calibration sections rewritten | **done** 2026-09-21 (needs no results) |
> | 6 | Results, Scenarios, Conclusion, Introduction, Abstract -- from the final outputs only | after step 4 |
> | 7 | Compression pass to 9,500 words; terminology and duplication audits | last |
>
> **The word limit is 10,000, working ceiling 9,500** -- appendices, bibliography, tables and
> figures excluded; only body prose counts. Count with `./env/python.exe scratchpad/wc_prose.py`.
>
> **Writing review, 2026-09-21:** [THESIS_REVIEW_2026-09-21.md](THESIS_REVIEW_2026-09-21.md)
> maps the recorded supervisor feedback to the current thesis. Written body prose is now
> **5,025 words** (previously 6,815), with final results still pending. Earlier BNPL outcomes
> are no longer asserted as final. The review also records two implementation qualifications:
> committed-expenditure distress persists after later borrowing, and the affordability gate
> omits separate statutory deductions. Neither code nor simulation settings changed in this pass.
>
> **Research questions, approved by the supervisor 2026-09-09.** The thesis introduction is
> authoritative. Umbrella: *in a household population already carrying substantial credit distress,
> what does the addition of a BNPL lending channel outside the affordability and reporting regime
> do to that distress, and what is the mandated extension of credit-bureau reporting to BNPL likely
> to achieve?* The model answers the second half for the **affordability channel only**; it has no
> credit score. **RQ1** -- can a synthetic population built from SA survey microdata reproduce
> credit-market behaviour it was not fitted to? **RQ2** -- does the mutual invisibility of BNPL
> platforms produce concurrent-facility stacking, and does population default rise with the number
> of platforms a household can stack across? **RQ3** -- how do three scenarios (bureau visibility,
> mandatory affordability screening, socially transmitted adoption) change the resulting distress
> and default? The cooling-off window and the facility cap are appendix material only.
>
> Old numbering maps forward as: old RQ0 -> RQ1, old RQ1 **and** old RQ2 -> RQ2, old RQ3 -> RQ3.
> Prose below uses the new numbering. **Dated changelog entries in section 9 are left as written**, since
> they record what was found on a date; read any `RQ1` there as the stacking half of today's RQ2.
> Experiment grid keys and figure filenames also keep the original scheme deliberately -- see the
> numbering note at the top of `simulation/experiments.py`.
>
> `beta` is the **RQ2** experimental axis: it is what makes peer effects in BNPL adoption visible.
> It is then toggled on and off for **RQ3**, because the cool-off lever only bites where
> `beta > 0`. The `beta = 0` control arm is reported throughout.

> **Defect register:** [`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md) records every known shortfall
> in the thesis with evidence, severity and owner. Check it before starting work.

---

## 1. The question

How do **Buy Now Pay Later (BNPL)** platforms affect consumer debt saturation and the potential
for systemic default in South Africa? We answer with an **agent-based model (ABM)** (Python/Mesa)
whose core engine is the household **balance sheet**: money and debt flowing through a population
of household agents over time.

---

## 1a. What kind of claim this model makes (the injection statement)

**This is a counterfactual experiment, not a historical fit.** State it exactly this way, in the
introduction, in the ODD Purpose section, and again in limitations:

> We construct a household population calibrated to observed South African conditions in **2017**,
> a period in which BNPL was effectively absent from the South African market. We validate that
> population's credit behaviour against the **2017-Q1 NCR Consumer Credit Market Report**. We then
> **inject** a BNPL lender class into that calibrated economy and observe how the dynamics change.
> The model therefore answers *"what does BNPL do to a household population like this one?"*, and
> **not** *"what happened in South Africa between 2017 and 2019?"*

**Why this framing is a strength, not an apology.** BNPL entered the South African market at scale
from roughly 2021. Any attempt to fit a model to the actual arrival of BNPL would have to
disentangle it from COVID-19 income shocks, the 2020 credit contraction, and post-pandemic
inflation, none of which the thesis is equipped to identify. Holding the population at 2017 gives a
**clean baseline with no BNPL contamination**, which is precisely what makes the injection
interpretable. The absence of BNPL in 2017 is the experimental control.

**What this framing forbids.** No claim that model output describes any actual year after 2017. No
comparison of model output to post-2020 observed arrears. Results are read as *directional and
mechanistic* ("stacking becomes self-reinforcing when X"), not as forecasts.

---

## 2. Strategy in one breath

Build a synthetic population of **household agents from NIDS Wave 5 (2017)**, enrich each with
**financial-inclusion flags matched in from FinScope**, and keep **everything in 2017 units**: no
inflation-forwarding, no second monetary reference year. Get a clean, validated *consumer*
population working first, then **inject** BNPL into it (§1a). All 18 agent-rule decisions are now
closed and cited; a richer *traditional* lender market remains out of scope.

**The five commitments that keep this simple:**

1. **One reference year: 2017.** NIDS W5 is the backbone; all monetary values stay in 2017 Rands.
   **No CPI forwarding. No IES. No 2022-level targets.**
2. **One backbone source: NIDS W5.** Income, expenditure, debt, demographics, weights.
3. **One donor source: FinScope.** Provides financial-inclusion flags only, via a simple match.
4. **Simple match, not fusion.** Cell-donor by income quintile (× province where cell sizes allow)
   by copying a random FinScope respondent's flags onto each NIDS household.
5. **Validation: internal for the data layer, external for the ABM.** The population is checked for
   internal consistency and FinScope-marginal reproduction. The ABM is checked against four external
   targets sourced from the literature and the regulator (see §7). BNPL-provider data is no longer a
   dependency.

---

## 3. Data sources

| Source           | Year | Role                                                              | In/Out         |
| ---------------- | ---- | ---------------------------------------------------------------- | -------------- |
| **NIDS Wave 5**  | 2017 | **Backbone**: income, expenditure, debt, demographics, weights  | **In**         |
| **FinScope SA**  | 2019 | **Donor**: banked status, credit access, savings, informal flags| **In** (proxy) |
| **NCR CCMR**     | 2017 | **Validation target**: arrears age analysis (D6, D7)            | **In**         |
| **Stats SA LMD** | 2017 | **Calibration cross-check**: QLFS job-separation band for `p` (D1) | **In**      |

The last two are *targets*, not inputs: nothing flows from them into the population. Both are
vintage-matched to 2017 and both are extracted to `data/config/` by scripts that assert the source
report's own prose, so neither can silently drift.


**FinScope note:** A 2017 FinScope wave is **not in our data**, so we use **FinScope 2019** as a
proxy for the ~2017 financial-inclusion landscape. The variables we import are **categorical
flags** (banked yes/no, has-credit yes/no), which are not monetary and so need no deflation; the
2-year gap is recorded as a limitation, not corrected.

---

## 4. The household agent

A **household** carried from one NIDS W5 record into the model, with a balance sheet (2017 Rands):

- **Inflow:** monthly income (+ dominant source: wage / grant / other).
- **Outflow:** committed expenditure (food + rent) and discretionary expenditure.
- **Assets:** liquid savings buffer.
- **Liabilities:** consolidated traditional debt + monthly servicing.
- **FinScope flags (matched in):** banked status, formal credit access, savings product, informal
  credit / insurance.
- **Tags:** income quintile (Q1–Q5) + conditioning attributes (size, composition, head demographics).

Full column-level mapping: [`household_agent.md`](household_agent.md) and
[`scratchpad/DECISIONS.md`](scratchpad/DECISIONS.md).

---

## 5. Execution plan: building the household agent

```
  NIDS W5 (backbone, 2017)              FinScope 2019 (donor)
  hhderived.csv + head demog            flags + matching keys
        │                                      │
        ▼                                      │
  [P1] BACKBONE                                │
   derive: income_source, committed/           │
   discretionary, savings proxy, D_trad,       │
   quintile  (NO CPI, stays 2017)              │
        │                                      │
        ▼                                      ▼
  [P2] MATCH  ── cell-donor by income quintile (× province) ──►
   copy banked / credit / savings / informal flags onto each NIDS hh
        │
        ▼
  [P3] RESAMPLE  → 5,000 households, prob ∝ w5_wgt
        │
        ▼
  [P4] VALIDATE  internal (NIDS dists) + match diagnostics (FinScope marginals)
        │
        ▼
  [P5] INSTANTIATE  each row → Household Agent (balance sheet + flags + tags)
        │
        ▼
  ABM: consumer agents + single lender stub      (BNPL = future extension)
```

| Phase | Goal | Key output | Status |
| ----- | ---- | ---------- | ------ |
| **P0** | Load & inspect NIDS W5 + FinScope 2019 | clean dataframes, key/flag inventory | ☑ both surveys resolved |
| **P1** | Build NIDS backbone in 2017 units | per-household record + quintile tag | ☑ `notebooks/p0_backbone.ipynb` → `data/processed/nids_backbone.parquet` |
| **P2** | Simple cell-donor match from FinScope | flags attached to each household | ☑ `notebooks/p2_finscope_match.ipynb` → `synthetic_population_matched.parquet` (servicing computed, guarded) |
| **P3** | Weighted resample to 5,000 | fixed synthetic population | ☑ `notebooks/p3_resample.ipynb` → `synthetic_population_5000.parquet` |
| **P4** | Validate (internal + match diagnostics) | validation report | ☑ `notebooks/p4_validation.ipynb`: 14/14 checks pass |
| **P5** | Instantiate agents | Household agents in Mesa | ◐ in progress (`simulation/`) |

---

## 6. Scope boundaries

**In scope now**

- NIDS W5 → 5,000 weighted household agents, quintile-tagged, **2017 Rands**.
- Simple FinScope cell-donor match for financial-inclusion flags.
- Consumer balance sheets + one traditional lender operating an NCA Reg 23A gate.
- **BNPL platform agents** (4 in baseline), stacking, pay-in-4 repayment, and the four RQ3
  intervention levers. All specified in D11 to D14 from published SA provider terms and FCA PS26/1.
- **Peer influence on BNPL adoption** (D17), the model's only agent-to-agent channel.
- Internal-consistency + match-diagnostic validation, plus four external ABM targets (§7).

**Deferred (future work)**

- **Multi-lender competition** among *traditional* lenders (the traditional side stays a single
  non-adaptive stub; the BNPL side does have multiple platforms).
- **BNPL-provider behavioural data** (desirable, no longer required: see §7).
- Geography beyond the match cell, **explicit contact networks** (no SA data to calibrate degree or
  clustering), **peer effects on consumption** (Cardaci's expenditure cascades), dynamic composition.

*Moved into scope 2026-08-05:* **peer influence on BNPL adoption** (D17), via an income quintile ×
province reference group. This is the model's only agent-to-agent channel and it is what makes the
non-linear threshold in RQ2 structurally possible.

---

## 7. Validation

- **Internal consistency:** synthetic population reproduces the **weighted NIDS W5** distributions
  it was sampled from (income quintile shares, household composition).
- **Match diagnostics:** imported FinScope flags reproduce **FinScope marginals** (e.g. national
  banked rate, credit-access rate) within tolerance.
- **Behavioural validation:** **no longer dependent on BNPL-provider data.** Closing D0 to D10
  (2026-08-05) produced four externally-sourced targets, listed in priority order:
  1. **Complementarity test (strongest).** deHaan et al. (2024, *Management Science*) find BNPL
     adoption raises credit-card interest and late fees. Enabling BNPL in the model must therefore
     **increase** arrears and interest burden on traditional debt. Substitution would falsify the
     lender-choice rule (D5).
  2. **Baseline arrears** versus NCR CCMR age analysis (D6, D7). **Resolved 2026-08-05:** the
     2017-Q1 CCMR is in the repo and extracted to `data/config/ccmr_2017_baseline.json`. Account
     basis, combined unsecured plus credit facilities: **71.63% current, 16.54% 60+ days,
     14.21% 90+ days.** The default horizon `k` was revised from 6 to **7 ticks (98 days)** so it
     maps cleanly onto the 90+ band. ⚠ CCMR counts **accounts**, the model counts **households**,
     so this is an order-of-magnitude target, not a point target.
  3. **Non-monotonic income to debt-to-income pattern** with a middle-income peak, reported by
     Hamill et al. (2023) (D8). A pattern-oriented check in the sense of Grimm et al. (2020).
  4. **Savings exhaustion** versus the TransUnion Consumer Pulse finding that 36% of South African
     consumers anticipated missing a bill payment (D2).
- ⚠ **Calibration versus validation.** The income-shock probability `p` (D1) is *fitted* to baseline
  arrears, so the **baseline is calibrated, not validated**. Only the BNPL-on results are genuine
  predictions. This must be stated in the limitations chapter.
- **Calibration cross-check (2026-08-12), which is not a fifth target.** `p` is still fitted, but it
  is now *reported against* an independent official band. Stats SA **Labour Market Dynamics 2022**
  (Report 02-11-02) carries the QLFS panel for 2017–2022, so a **vintage-matched 2017** figure
  exists: Q3:2017 → Q4:2017, **93.14% retained employment, 3.53% to unemployment, 6.86% left
  employment**, implying a per-tick hazard band of **0.54%–1.17%**
  (`data/config/qlfs_2017_labour_flows.json`). This constrains the parameter that carries the four
  targets rather than adding a target, so the count stays at four. ⚠ QLFS counts **individuals**;
  the model shocks a **household** — the same class of unit mismatch as the CCMR account basis.
- ⚠ **The `beta = 0` control arm (D17).** The peer-influence strength `beta` is uncalibrated, and
  D17 was added partly because RQ2 needs non-linearity to be structurally possible. Reporting
  non-linearity as a finding would therefore be circular unless controlled. **All RQ2 output
  is reported as a surface over the swept parameter × `beta`, with the `beta = 0` row shown**, and
  every RQ3 lever is reported at both `beta = 0` and `beta > 0`. At
  `beta = 0` the model reduces exactly to independent agents. The claim becomes *"default responds
  non-linearly to BNPL access only when social transmission is present"*, which is stronger than
  asserting a threshold. The four targets above are unaffected: the peer channel is **inert in the
  baseline**, since `s_g` is identically zero when BNPL is disabled.
- BNPL-provider data remains desirable but is now an upside, not a dependency.

---

## 8. Companion documents

**Two working documents:**

- [`scratchpad/DECISIONS.md`](scratchpad/DECISIONS.md) — **what was chosen and why.** Part I is the
  eighteen model decision rules (D0–D17); Part II is the data layer: the design commitments, the
  cell-donor matching method, and the column-level variable map (NIDS + FinScope).
- [`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md) — **what is wrong, or was wrong**, with evidence,
  severity and owner. Its entry headings overstate what is open; B32 is the live one.

**What happens next** lives at the top of this file, not in a separate plan.

Two revision plans from the September 2026 supervisor feedback:

- [`supervisor_revision_plan.md`](supervisor_revision_plan.md) — **content**: the seven
  feedback items as writing tasks. **APPLIED 2026-09-10.** Kept at the root because its float-note
  rules (section 6) and regulatory source table (section 0.3) still govern the Results write-up.
- [`SOL_PLAN_REFORMAT.md`](SOL_PLAN_REFORMAT.md) — **structure**: the restructure to the
  reference paper's section order. **LIVE**; revised 2026-09-21 to the three-scenario decision.

One standing reference:

- [`household_agent.md`](household_agent.md): data → agent mapping, presentation-ready.

**Archived 2026-09-21** in [`archive/`](archive/), superseded but kept for their evidence:
`STATUS.md` and `THESIS_GUIDE.md` (every number predates B32 -- do not quote them), `PLAN.md`
(16,000-word budget, old chapter numbering, and a TransUnion 20% band that was a misattribution),
`SCOPE_REDUCTION.md` (executed 2026-08-18) and `literature_2_fix.md` (applied 2026-08-24; holds the
citation-verification evidence for Chapter 2).

---

## 9. Changelog (living)

- **2026-09-21 (code cleanup; one blocker found).** Executed
  [`CODE_CLEANUP_PLAN.md`](CODE_CLEANUP_PLAN.md); its execution log lists every step and what was
  skipped. No output of the model moved: a four-arm golden run on the full population was
  identical after every step, and the analysis CSVs and printed report were byte-identical.
  - **Found and fixed: DEFECTS B34.** Granted traditional loans were never booked as debt. One
    baseline run granted R9.96m, 20.7% of the opening book, that was never repaid. A grant now
    joins the household's consolidated balance (balance, balance-weighted rate and scheduled
    service all rise), at the rate table's sourced unsecured terms. **Re-fitted: shock 0.040 ->
    0.016, friction 0.09 unchanged**, so the fitted shock rate is now 1.4x the QLFS upper bound
    (was 3.4x). 90+ 13.96% against 14.21%, 1--30 8.22% against 8.24%.
  - **Decided: the mean-purchase comparison (B32).** All adopters, within 35% of R992,
    pre-registered in `DECISIONS.md` D4. The `xfail` test is replaced by one that pins the
    explanation of the gap.
  - **Fixed: DEFECTS B35.** The "synchronous" activation arm was the "uniform" arm, bitwise. One
    fixed-order arm remains, and the thesis claims one.
  - The run output now echoes every parameter, reports all six arrears bands, and splits
    want-driven purchases by quintile (for B32). `SALib` is pinned.
  - `notebooks/00_showcase.ipynb` and `notebooks/p1p2_visualizer.ipynb` were deleted: they read
    columns no parquet has carried since the flag set was cut. Entries below that mention them are
    history. `data/processed/quintile_archetypes.csv` is now an orphan with no reader or writer.
  - P2 imports the Reg 23A gate from `simulation/affordability.py` instead of retyping it; the
    stored servicing columns reproduce bitwise. Population parquets untouched (hashes checked).

- **2026-08-13 (supervisor-update run: 950 runs, 5 replicates).** Results summarised for the
  supervisor in [`STATUS.md`](archive/STATUS.md). ⚠ 5 reps gives a 0.33pp sd, so anything under ~0.67pp is
  noise. Headlines:
  - **B24 is closed and the answer was "artefact".** The two rebuilt parameters fell from ranks 1
    and 2 to rank 4 and last: purchase size 19.6pp → **2.06pp**, the per-provider limit 16.9pp →
    **0.18pp**. The largest sensitivity is now `amount_rule` at 4.11pp, D4's uncited shortfall rule
    — and two of its three variants agree within the noise floor.
  - **RQ2's negative holds under both mechanisms, and more strongly than expected.** Granovetter
    thresholds produce no cascade in *adoption* either: adoption R² = 0.9999 at every dispersion.
    What replaces it is the **adoption-versus-default split** — social transmission roughly doubles
    adoption (21% → 42%) and moves default by about half a percentage point. ⚠ Amplification has
    collapsed from 4.3× to **1.6×**; the old figure must not be quoted.
  - **The headline policy result survived the rebuild.** Bureau visibility still moves BNPL volume
    by ~1%. ⚠ But the affordability duty is now roughly inert, and the **stacking cap** is the
    effective lever, cutting volume 54–63% and returning default nearly to the no-BNPL baseline.
  - **The corrected statutory cool-off behaves as predicted**: −0.2% volume at β=0, **−33.5%** at
    β=1, against a pre-run prediction of −30.4%.
  - **Two new external checks pass.** BNPL volume per eligible household is R3,015 at β=0, inside
    the R1,333–R4,261 anchor band; mean purchase R893 against the R992 anchor. Neither fitted.
  - Baseline unchanged as designed: 60+ arrears **15.38%** against CCMR 16.54%, unfitted.

- **2026-08-13 (sources pinned; peer channel rebuilt).** **91 tests pass.** The model is now
  parameter-frozen and ready to run; the run itself awaits instruction.
  - **Both `% VERIFY` flags closed.** The **P0141 June 2026** release supplies a published mid-2026
    anchor (index 107.5 on Dec 2024 = 100; 5.0% year-on-year), replacing the part-year guess that
    deflated the Payflex figures. The factor is unchanged at 1.5111 but is now *derived*: an annual
    average sits at its year's mid-point, so the 2025 average is the mid-2025 price level and the
    published year-on-year rate carries it exactly twelve months forward. It also gave a **drift
    check on the whole chain** — compounding 2018-2025 forward implies a June 2026 index of 106.7
    against the published 107.5, a −0.77% gap, bounding the deflator error at under 1%.
  - **Weaver Fintech's Integrated Report 2025, page 14, is now the primary BNPL source** and settles
    everything on one panel: cumulative GMV R13.1bn, 9.4m cumulative transactions, 3.7m signed-up
    customers, and a BNPL-specific frequency series (1.8x → 4.4x, FY2021-FY2025). The R992 order
    value in 2017 Rands is **confirmed**. Entity renamed from HomeChoice International plc.
  - **The R7,000 / 2.12 metric is dropped**, resolved as *group-wide fintech spend per customer*,
    not a BNPL basket. The volume anchor becomes a **band**: R1,333 (per signed-up) to R4,261 (per
    active) per year in 2017 Rands.
  - **`lambda` set to 0.10.** The rolling limit applies at each of four platforms, so the evidence
    that constrains it is Woolard's *stacked* ~£1,000, ~37% of UK median monthly income across all
    providers → ~0.09 each. At 0.25 the model's stacked total was 2.7x that. ⚠ The limit now binds
    on **54% of requests** at β=0 — a first-order constraint, to be reported rather than hidden.
  - **B31 closed as Option A**: `s_g` is measured against the **BNPL-eligible** subpopulation, so its
    ceiling no longer moves with `bnpl_access_rate` (RQ2's own x-axis). Peak `s_g` rises 0.53 → 0.96.
    ⚠ This rescales `beta`; earlier linear results are not comparable.
  - **The Granovetter threshold arm is built** — D17's pre-registered alternative. `sigma_theta` is
    the primary axis because Granovetter's claim is about threshold *variance*, not mean. `gamma = 0`
    reproduces the independent-agent model **bitwise**, which required a separate `init_rng` stream
    for agent endowments; that also makes the dispersion sweep a **paired** comparison.
  - **The shortfall-driven BNPL path is left unchanged and disclosed** (DECISIONS D5): it is
    permissive about how much distress BNPL can relieve, biasing the estimated effect on default
    upward, which is the conservative direction.

- **2026-08-12 (QA pass: the two dominant parameters, and three defects).** The first full run showed
  the model's output was driven mainly by its two worst-sourced parameters (DEFECTS.md **B24**). A
  code-and-data pass found that "worst-sourced" was only half the diagnosis, and fixed all of it.
  **All 79 tests pass** (65 existing, 14 new). **The baseline is untouched** — `shock_prob` and
  `payment_friction` are fitted with BNPL disabled, so there is no re-calibration and the CCMR
  comparison, pattern 3 and pattern 4 stand exactly as reported. **Everything BNPL-on must be
  re-run.**
  - **BNPL purchase size is now DERIVED, and its level is a CHECK.** It was a flat R1,568 from trade
    press applied to every household — which is 127% of the median banked Q1 household's monthly
    discretionary budget and 11.4% of Q5's. A population with a Gini of 0.67 cannot share one
    purchase size. Purchases are now drawn about **`kappa` × the household's own monthly
    discretionary expenditure**, with **`kappa` = 0.1387 computed from Stats SA IES 2022/23 COICOP
    microdata** — the share of discretionary spending going to the categories BNPL finances. Only a
    *ratio* is taken from that survey, so the 2022/23 vintage cannot contaminate a 2017-Rand model,
    exactly as with the FinScope 2019 flags.
  - **And the level is now externally validated rather than assumed.** PayJustNow's average order
    value falls out of two disclosed aggregates — R13.1bn cumulative BNPL GMV over 9.4m
    transactions — giving **R992 in 2017 Rands**. The superseded trade-press basket deflates to
    R1,038. **Two independent SA sources, 4.6% apart, and the model's drawn mean of R1,029 sits
    between them, fitted to neither.** The trade source is demoted from input to corroboration.
  - **The rolling platform limit is a function, not a constant.** The flat R5,000 was 217% of the
    median banked Q1 household's monthly income, at each of four platforms. It is now **`lambda` ×
    monthly income per household**, `lambda` = 0.25, reported against a **0.10–0.26** band implied by
    Woolard and ASIC REP 672 — the same "report it against a band, don't fit to it" treatment `p`
    gets against QLFS. The functional form is licensed by HomeChoice's audited **"low and grow"**
    credit-risk disclosure, which is an annual report rather than a support page. Binding rates are
    now reported **by quintile**, because a limit that scales with income binds hardest at the bottom
    and an aggregate rate hides that.
  - **B29, new: every BNPL money parameter was in the wrong year's Rands.** Purchase size, the
    R15,000 order cap and the R95/week late fees were all current-vintage nominal in a model whose
    every other quantity is 2017 Rands — a ~1.4× overstatement. Fixed with one sourced CPI factor
    applied in `config.py`. **Fourth instance of implementation falsifying a signed-off
    specification**, after B15, B17 and B18, and the cleanest: the spec was not silent, it
    contradicted a global convention the rest of the model obeyed.
  - **B28, new: want-driven purchases were partly funded by money that did not exist.** The 25%
    checkout instalment was deducted without a balance check and the negative cash silently floored
    to zero. Now the checkout debit must clear or the purchase is declined — which is what both SA
    providers actually do, so this is a sourced rule rather than a patch.
  - **B27 closed: the statutory cool-off is no longer a no-op.** The gate is strict, and the new
    regression test asserts a **strict** reduction in the want-driven purchase **count** — the old
    test asserted non-increase of *volume*, which a no-op satisfies trivially and which mixes in the
    shortfall path the lever does not block.
  - **B31 raised before it can do damage.** `s_g` is computed over all group members, so it is capped
    at each group's **eligible share** — and that ceiling is proportional to `bnpl_access_rate`,
    which is **RQ2's own x-axis**. At 15% access no Granovetter threshold above ~0.125 can fire
    anywhere, so sweeping access would sweep the peer signal's maximum at the same time and produce
    a threshold-shaped response that is partly an artefact. Harmless under linear coupling, where
    the denominator is absorbed into `beta`. **Decide the denominator before building the threshold
    variant**; the recommendation is to normalise `s_g` by the eligible share, which also requires
    re-running the linear arm — cheap, since everything is being re-run.
  - ⚠ **Single-seed diagnostics suggest the changes are large**: default falls 32.9% → 27.5% at
    β = 0 and 56.1% → 28.0% at β = 1. Adoption still responds strongly to β; default barely does, so
    **B22's 4.3× amplification finding is itself now in question.** Illustrations, not results —
    the re-run decides.

- **2026-08-12 (P5 begins; sourcing pass on two assumed parameters).** Before writing the ABM, the
  two parameters the implementation plan would have had to invent were sent back to the sources.
  One was eliminated, one was proved unsourceable, and a third gap was found in a rule already
  marked closed.
  - **D1 shock magnitude: eliminated, not assumed.** Re-reading the anchor settled it. Madeira does
    not model a fractional income cut; he models **flows into and out of unemployment**. Following
    the anchor properly makes the shock a *separation from employment*, so its magnitude is the
    household's **wage component** — observable in `w5_hhwage`, which is in the NIDS hhderived file
    all along. **No free parameter and no sweep.** No pipeline rebuild either: `source_w5_hhid` is
    already on the 5,000-agent parquet, so the column joins onto the validated population and the
    14/14 checks are untouched.
  - **D1 `p` gains an external band.** `p` stays *fitted* to CCMR arrears (D1 requires that), but is
    now reported against Stats SA **Labour Market Dynamics 2022** (Report 02-11-02), whose QLFS panel
    spans 2017–2022 and so yields a **vintage-matched 2017** figure. Q3:2017 → Q4:2017: **93.14%
    retained, 3.53% to unemployment, 6.86% left employment** → **0.54%–1.17% per tick**. Extracted
    by `notebooks/scripts/extract_qlfs_lmd.py`, which asserts two of the report's own prose
    statements and requires headline Table 2.1a and appendix Table A.1 to agree — the same discipline
    used for the CCMR. Partially answers DEFECTS.md **B8**: the template is "bound it, don't only
    check it afterwards", which is what `q_base` still needs.
  - **D11 rolling balance: searched, and it does not exist publicly.** Neither major SA provider
    discloses a rolling limit — Payflex publishes only the R15,000 per-order cap and sets the rest
    per customer; PayJustNow declines to publish limits at all. Recorded as a **citable absence**
    consistent with D10's no-disclosure regime, and demoted from a behavioural parameter to a
    **binding-check quantity** under D11's existing "check the cap binds rarely" test.
  - **D6 gap found: the minimum payment was never defined.** D6 fixes the *share* of minimum-payers
    (`m = 0.29`) but never says what the contractual minimum *is*, and the gap survived the design
    pass because `[Keys2019]` measures behaviour *relative to* an issuer's minimum, which reads as
    though it settles the question. No NCA anchor exists either. Now closed by assumption and swept.
    **This is the model's second uncited rule** — the limitations chapter currently claims D4 is the
    only one, and that sentence must change (DEFECTS.md **B15**).
  - **D4 purchase size: weakly anchored.** SA average BNPL basket ≈ **R1,568**, cross-checked against
    CFPB's $135/loan and $848 per user per lender per year (new bib entry `cfpb2025market`, distinct
    from the existing `cfpb2025bnpl`). ⚠ The SA figure is **trade press** and is now the weakest
    source in the bibliography, flagged `% VERIFY`. The D4 *rule* remains uncited.
  - Net effect on the register: **assumed parameters the ABM must invent fall from four to two**,
    and both survivors carry mandatory sensitivity.

- **2026-08-12 (first full sweep: 3,304 runs).** RQ0/RQ1/RQ2/RQ3 + robustness (2,280) and a Sobol
  variance decomposition (1,024). Raw output in `results/raw/`, summaries and figures in
  `results/summary/`. Five findings, in order of how much they change the write-up:
  - **RQ2's registered claim is NOT supported** (DEFECTS.md **B22**). Every arm is near-linear,
    *including* `beta = 0` (linear R² = 0.9992). What IS supported is **amplification**: peer
    influence multiplies the access response **4.3x**. Curvature peaks at *intermediate* beta and
    vanishes at high beta as the system saturates. D17's pre-registered **Granovetter
    heterogeneous-threshold variant** should now be run before concluding no threshold exists.
  - **Bureau visibility does nothing** (**B23**). The lever D10 called "the comparison the whole
    model was built to make" moves default by 0.08pp and volume by under 1%. Coherent, not a bug:
    it constrains the *traditional* lender while leaving BNPL eligibility, platform blindness and
    the want-driven trigger untouched. The lever that works is the **mandatory Reg 23A check on
    BNPL** (32.9% → 28.1% default, volume −15.3%). Policy reading: **transparency alone is not a
    remedy.**
  - **The two most influential parameters are the two worst-sourced** (**B24**). BNPL purchase size
    (trade press) moves default **19.6pp**; the rolling limit (unpublished by any SA provider)
    moves it **16.9pp**. Sobol confirms it and adds what OFAT could not: **two-thirds of purchase
    size's influence is interactive**. Both must be first-order sensitivities in ch.6, not appendix
    material.
  - **Two worries retired.** `min_payment_frac` has a total-order Sobol index of **0.0006** and the
    minimum-payer share moves default by 0.25pp over 0.20–0.40 — so **B15** and much of **B7** are
    disclosure items, not threats. **D16's** activation-order independence is now confirmed
    empirically (0.18pp across three regimes), as predicted by the one-tick lag.
  - **Three unfitted external checks passed** (**B26**): emergent stacking at **37%** holding 2+
    facilities against the CFPB's 32% cross-firm; the R15,000 order cap binding on **0.3%** of
    requests exactly as D11 predicted; and BNPL-at-zero-access reproducing the BNPL-free baseline.
  - **Pattern 1 (deHaan complementarity) passes**: enabling BNPL raises traditional arrears
    +3.9pp at `beta = 0` and +10.5pp at `beta = 1`, with interest burden up 3.8% and 6.4%. Direction
    is partly designed in (the want-driven trigger); the magnitude is not.
  - ⚠ **High-beta arms are implausible in absolute terms** (**B25**): R31,097 of BNPL per eligible
    household over 40 ticks against a ~R4,800 median monthly income. Label the upper reaches of the
    RQ2 surface as mechanistic, per §1a.
  - ⚠ Sobol confidence intervals are wide at N=64; **re-run at N≥256 before quoting indices.**

- **2026-08-12 (the ABM exists; baseline calibrated).** `simulation/` built to the 17-submodel
  specification on Mesa 3.5.1. **60/60 verification tests pass**, including every degenerate case
  chapter 5 commits to: `beta = 0` recovers the independent-agent model, BNPL-disabled reproduces
  the baseline exactly, `N = 1` collapses stacking, and `s_g` is identically zero in the baseline.
  - **Two fitted parameters, against two different bands, leaving three unfitted checks:**
    `shock_prob = 0.048` per tick fitted to the 90+ tail, and `payment_friction = 0.09` per tick
    fitted to the 1-30 band. They are near-orthogonal, so the pair is identified rather than
    over-determined.

    | Band | Model | CCMR 2017 | Status |
    | --- | --- | --- | --- |
    | current | 74.41% | 71.63% | unfitted |
    | 1-30 d | **8.38%** | 8.24% | FITTED |
    | 31-60 d | 1.25% | 3.59% | unfitted, thin |
    | 61-90 d | 1.21% | 2.32% | unfitted, thin |
    | 90+ d | **14.75%** | 14.21% | FITTED |
    | **60+ d** | **15.96%** | **16.54%** | **unfitted — the strongest independent result** |

  - **Pattern 3 HOLDS** on the pre-registered aggregate statistic (DEFECTS.md **B19b**): aggregate
    debt/income peaks at **Q4** with Q5 lowest, which is Hamill's shape. The earlier "fails" verdict
    came from a **mean of ratios**, which over this population is a division artefact — the top 1%
    of Q1 carries 77% of its DTI mass and the median Q1 household has DTI 0.00. **The statistic was
    fixed, not the data**: all 33 zero-capacity debtors are retained, and the thesis reports all
    three statistics and states that the verdict is statistic-dependent.
  - **Pattern 4:** ~45% reach zero liquid savings against TransUnion's 36% — same order, high.
  - **The QLFS band earned its place immediately** (DEFECTS.md **B20**): fitted `p` is **4.1x** its
    upper bound, and since the hazard now applies **per earner** the comparison is **like-for-like**
    — the household-versus-individual caveat no longer explains any of the gap. Servicing is
    affordable by construction for 98.2% of households, so the shock channel is doing the work of
    several missing stressors.
  - **Three closed decisions were revised by running the model**, all recorded: D1's single-tick
    shock could not move the quantity it was fitted to (**B17**); the CCMR comparison used a
    denominator excluding the 56% of households holding no debt (**B18**); and D6 fixed the *share*
    of minimum-payers without ever defining the minimum (**B15**).
  - **A second stressor was added and cited, not invented**: `payment_friction`, anchored to
    Kuchler & Pagel — already in the bibliography and already cited in D6 for exactly this
    behaviour. D7 distress is assessed *before* friction, so it moves arrears without contaminating
    the headline default rate; verified by test.
  - Replicate dispersion at the fitted values is tight (sd ~0.004 on 90+ across 20 replicates),
    which is the dispersion argument chapter 5 asks for in place of a round number.
  - **Global sensitivity analysis added** (`simulation/sensitivity.py`, SALib Sobol) over the six
    uncalibrated or weakly-grounded parameters. OFAT sweeps show whether a result moves; Sobol
    apportions output variance and exposes interactions, which OFAT cannot.

- **2026-08-05 (thesis document pass).** Full review of `thesis/main.tex` produced
  [`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md): **43 findings**, 5 of them blockers. 31 closed
  in this pass. The document was restructured from a single flat file of unnumbered `\section*`
  headings into `thesis/main.tex` + `thesis/chapters/*.tex`, with numbered chapters,
  `\label`/`\ref` throughout, front matter and a ToC. **Body prose 6,265 → 10,519 words**
  (57 pages), against a ~25,000 limit.
  - **New chapters written:** Introduction; **Data and Population Construction** (P0–P4 written
    up at last, including the 53 zero-capacity debtors and the circular-check episode as
    findings); **Limitations**; Appendix A (design rationale, holding the rejected alternatives
    moved out of the body).
  - **RQ rewritten.** The primary RQ asked about *systemic default cascades*; the model has one
    non-adaptive lender, no contagion channel and a static macro environment, so nothing can
    cascade. It now asks about **population-level default**, and §1.2 states explicitly what the
    model cannot answer. Contagion channels are recorded as future work.
  - **Pattern 1 caveat added.** The "primary falsification test" is partly designed in: the
    want-driven trigger (D3) was chosen *because* a shortfall-only agent could not reproduce
    deHaan et al. The magnitude stays open; the direction does not. Same treatment as the
    `beta = 0` circularity.
  - **ODD chapter condensed 4,569 → 3,588 words** while *gaining* two specification tables, by
    converting the 11 design concepts and all 17 submodels from prose to tables and keeping
    extended prose only for D9, D10, D11, D13, D15.
  - **Errors fixed:** `\ac{FCA}` undefined (2 LaTeX warnings); CCA s.66A attributed to the UK;
    CCMR arrears bands presented as if they summed (they nest — full band table now given); the
    account-vs-household unit mismatch now stated in the thesis, not only in the JSON; bib key
    `toh2025bnplconstraints` → `hayashi2025constraints`; Irving (2005) replaced by FinScope for
    the stokvel/mashonisa claim.
  - **Humanised.** "rather than" 45 → 6; antithesis constructions 20+ → 4, kept only where the
    contrast carries the claim. Self-critical passages deliberately retained.
  - ⚠ **Gini disambiguated.** 0.651 is the *weighted backbone* per-capita Gini (0.611 household);
    **0.667** is the *5,000-agent resample*. The 0.015 gap is validation check F and passes its
    0.02 tolerance.
  - **Still blocking:** the ABM itself (P5 → `simulation/`). Chapters 5, 6 and 8 are skeletons
    with per-section content requirements, ready to fill the day the first run lands.

- **2026-08-05 (D11 to D16 closed: all 18 decisions now closed).** The BNPL platform is specified
  from **published South African provider terms** rather than from provider cooperation, confirming
  no firm contact is needed. **D11:** eligibility is *banked-only*, since both major providers debit
  a bank card at checkout, which caps access at **82.8% of the population by observed data**, so the
  RQ2 sweep runs inside the banked subpopulation rather than over a free parameter. Screen is
  deliberately **not** the Reg 23A test; that asymmetry is the mechanism. **D12:** platforms are
  blind to each other, which *follows from* D10 rather than being a new assumption; stacking depth is
  emergent and checked against CFPB (63% simultaneous, 32% cross-firm). **D13:** Payflex Pay in 4 is
  25% at checkout then 25% every two weeks, which **lands exactly on the 14-day tick**, retroactively
  validating the tick choice made in decision.md Set 1; late fee R95/week capped at 3 weeks.
  **D14:** four RQ3 levers, three of which are real instruments (bureau visibility, mandatory
  affordability check per FCA PS26/1, and a **14-day cool-off from CCA s.66A**, again exactly one
  tick); the stacking cap is labelled hypothetical since no jurisdiction imposes one. RQ3's
  "defer versus desist" is operationalised as **cumulative BNPL volume over the horizon**, not
  timing. **D15:** macro fully static, because any time-variation would confound the injection
  effect and destroy the experimental control. **D16:** random asynchronous activation, anchored to
  Comer & Loerch and Alizadeh & Cioffi-Revilla; note that **D17's one-tick lag makes the peer channel
  activation-order independent**, so the main interaction does not inherit that sensitivity.
  Bibliography now 28 entries.

- **2026-08-05 (D17 peer influence).** Added the model's **only agent-to-agent channel**. Motive was
  structural, not cosmetic: with independent households, population default is close to a smooth
  function of BNPL access, so **RQ2 was asking for a threshold the topology could not produce**.
  Peer influence acts on the **want-driven BNPL trigger only** (`q_i(t) = clip(q_base + beta·s_g(t-1), 0, 1)`),
  over a reference group of **income quintile × province**, the same cell already used for the
  FinScope match (45 groups, min 17 agents, median 82, verified against the 5,000-agent parquet).
  Need-driven borrowing is not socially transmitted. Key discovery justifying the change:
  **Cardaci (2018), already the primary ABM anchor, models peer effects and expenditure cascades
  centrally**, so the no-interaction design was the deviation, not the addition. Mechanism anchored
  to Granovetter (1978) threshold models; domain to Ackert et al. `beta = 0` recovers the previous
  model exactly and is the **control arm**, which also lets RQ2 separate the financial loop (borrow
  to service) from the social loop (adopt because peers adopted). **No data-pipeline change:**
  `province` and `income_quintile` are already columns, so the reference group is derived at model
  init. Baseline calibration untouched, since the channel is inert with BNPL disabled.

- **2026-08-05 (decision rules D0 to D10 closed).** Literature sweep found the consumer-credit ABM
  anchors the register was missing: **Madeira (2018, *J. Financial Stability*)**, a Central Bank of
  Chile household credit ABM in a middle-income economy that defaults on failure to finance minimum
  consumption and is **validated against observed default rates**; **D'Orazio & Giulioni (2017,
  JASSS)**; and **Hamill et al. (2023)** on the UK credit-card market. BNPL evidence upgraded with
  **deHaan et al. (2024, *Management Science*)**, causal, 10.6m US consumers. Ten of sixteen
  decisions now closed with rule, citation, parameters and validation hook.
  **D4 (borrowing amount) is closed by assumption with no anchor found** and is flagged, with
  mandatory sensitivity analysis. Consequence: §7 rewritten, since behavioural validation no longer
  depends on BNPL-provider data. Remaining open: D11 to D16 (BNPL platform, macro, scheduling).
  Bibliography now 20 entries. Literature review drafted in `thesis/main.tex`.

- **2026-08-05 (servicing grounded).** Replaced the two unsourced servicing parameters.
  (1) **APRs**: `credit_rate_table.csv` placeholders → **NCA statutory maximum prescribed rates**
  per sub-sector (regime in force 6 May 2016, so 2017-valid) at the **2017 repo rate of 7.00%**:
  credit facilities 21%, other credit agreements 24%, unsecured 28%, short-term 5%/month.
  (2) **Affordability**: flat `MAX_DSTI = 0.65` → the **NCA Reg 23A(9) residual-income test**
  (GN R202, GG 38557). The NCA prescribes *no* DSTI ratio; it prescribes a minimum expense-norms
  table, giving an **income-varying** ceiling (10.4% of income at R900/mo vs 83.2% at R7,712/mo).
  Both published worked examples are asserted in-notebook. **P4 check D was circular**: it tested
  `dsti.max() <= 0.66`, i.e. the cap it had just imposed; replaced with a non-circular test of how
  often the guard binds (**3.4% of debtors**, passes at ≤10%). Still **14/14**. New diagnostic:
  **53 debtor households** have income at or below the Reg 23A norm, so no NCA-compliant lender
  could have granted their debt, reported as a finding rather than capped away. **Closes D9's
  affordability formula.** Known limits: statutory maxima are ceilings not observed averages (NCR
  CCMR publishes no rates); terms remain assumptions; Reg 23A is per-consumer, applied per-household.
- **2026-06-01 (showcase).** Built `notebooks/00_showcase.ipynb`: a supervisor-facing guided tour
  (what each phase did, with visuals), a benchmark validation scorecard (7/7 ✓, incl. Gini 0.651 and
  FinScope flag rates), and a plain-English profile of a fixed-seed sample agent.
- **2026-06-01 (head demographics).** Added the deferred head-of-household demographics to P0
  (`age_head`, `gender_head`, `race_head`, `education_head` + coarse `education_band`), joined via
  the roster head (`w5_r_relhead==1`) → individual-derived file (99% matched). Propagated through
  P2/P3 into `synthetic_population_5000.parquet`; added a demographics section to the visualizer.
  Education×quintile gradient is textbook (Q1 4% tertiary → Q5 54%). **Static data layer complete.**
- **2026-06-01 (P3).** Built `notebooks/p3_resample.ipynb`: weighted resample to **5,000 agents**
  (from 3,221 unique source households) → `synthetic_population_5000.parquet`. P4 extended with a
  live resample-fidelity section (income KS gap 0.016, flag gap 0.5pp, shares ±1.4pp), now **14/14
  pass**. Population-size stability checked at 1k/5k/10k. The static household-agent data layer is
  complete; next is the ABM (rules, environment, lender).
- **2026-06-01 (P4 + fixes).** Diagnostics surfaced servicing/DSTI outliers (68 hh with
  repay>income, max DSTI 25×) from the stock-balance × product-term mismatch. Fixed with a term
  floor (`MIN_TERM_MONTHS=6`) + NCA-style affordability cap (`MAX_DSTI=0.65`): now 0 hh over income,
  DSTI 3–6% by quintile. Built `notebooks/p4_validation.ipynb` (benchmark comparisons + pass/fail,
  **10/10 pass**, incl. emergent Gini 0.651 in the SA band). Toned down the visualizer's clustering
  framing (PCA<50% var, weak silhouette → continuum, not natural clusters).
- **2026-06-01 (viz).** Rate table populated → P2 re-run, `monthly_trad_repayment` computed for all
  10,841 households (4,702 debtors; quintile DSTI 3–9%). Built `notebooks/p1p2_visualizer.ipynb`:
  quintile archetype profiles (`data/processed/quintile_archetypes.csv`), balance-sheet / flag /
  source / bivariate / province views, and an unsupervised K-means structure check vs the quintiles.
- **2026-06-01 (P2).** Built `notebooks/p2_finscope_match.ipynb`: FinScope codes **resolved** (F1
  banked, G5/G10–G14 formal credit, K7 savings, M13_MHI income); cell-donor match on per-capita
  income quintile × province (45 cells, ≥30 donors, **0 fallbacks**); matched marginals reproduce
  FinScope within **≤2.3 pp**. `monthly_trad_repayment` constructed via product-mix amortization
  over an **external, user-populated** `data/config/credit_rate_table.csv` (placeholder-guarded, so
  not yet computed). `liquid_savings` winsorized at the 99th pct. Output:
  `data/processed/synthetic_population_matched.parquet`.
- **2026-06-01 (P1).** Built `notebooks/p0_backbone.ipynb`: NIDS W5 loaded (13,719 → **10,841
  valid households**), backbone derived in 2017 Rands (income source, committed/discretionary
  expenditure, balance sheet), **per-capita weighted income quintiles** assigned (bounds
  R900 / R1,801 / R3,400 / R7,712). Outputs in `data/processed/`. Next: P2 FinScope match.
- **2026-06-01.** Switched to **2017-only** units (dropped CPI forwarding, IES, 2022-level
  validation). Reintroduced a **simple FinScope cell-donor match** (replacing crude per-quintile
  imputation). Behavioural validation deferred to BNPL-provider targets. OVERVIEW.md promoted to
  living source of truth.
- *(earlier)* Simplified from multi-survey hot-deck fusion to single-source NIDS resample.
