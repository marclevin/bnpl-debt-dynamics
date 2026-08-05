# Project Overview: Living Source of Truth

**Project:** Modelling BNPL impact on the South African consumer credit market (Agent-Based Model).
**This file is the canonical strategy + execution plan.** When a decision changes, change it here
first, then propagate to the companion docs. Last updated: **2026-08-05**.

> **Defect register:** [`scratchpad/issues.md`](scratchpad/issues.md) records every known shortfall
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
[`scratchpad/variables.md`](scratchpad/variables.md).

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
| **P5** | Instantiate agents | Household agents in Mesa | ☐ |

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
- ⚠ **The `beta = 0` control arm (D17).** The peer-influence strength `beta` is uncalibrated, and
  D17 was added partly because RQ2 needs non-linearity to be structurally possible. Reporting
  non-linearity as a finding would therefore be circular unless controlled. **All RQ1 and RQ2 output
  is reported as a surface over the swept parameter × `beta`, with the `beta = 0` row shown.** At
  `beta = 0` the model reduces exactly to independent agents. The claim becomes *"default responds
  non-linearly to BNPL access only when social transmission is present"*, which is stronger than
  asserting a threshold. The four targets above are unaffected: the peer channel is **inert in the
  baseline**, since `s_g` is identically zero when BNPL is disabled.
- BNPL-provider data remains desirable but is now an upside, not a dependency.

---

## 8. Companion documents

- [`scratchpad/decision.md`](scratchpad/decision.md): the design decisions, with rationale.
- [`scratchpad/variables.md`](scratchpad/variables.md): column-level variable mapping (NIDS + FinScope).
- [`scratchpad/data_fusion.md`](scratchpad/data_fusion.md): the simple cell-donor **matching** method.
- [`household_agent.md`](household_agent.md): data → agent mapping, presentation-ready.
- [`scratchpad/work.md`](scratchpad/work.md): ABM design narrative.

---

## 9. Changelog (living)

- **2026-08-05 (thesis document pass).** Full review of `thesis/main.tex` produced
  [`scratchpad/issues.md`](scratchpad/issues.md): **43 findings**, 5 of them blockers. 31 closed
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
    **0.671** is the *5,000-agent resample*. The 0.019 gap is validation check F and passes its
    0.02 tolerance with almost no margin.
  - **Still blocking:** the ABM itself (P5 → `simulation/`). Chapters 5, 6 and 8 are skeletons
    with per-section content requirements, ready to fill the day the first run lands.

- **2026-08-05 (D11 to D16 closed: all 18 decisions now closed).** The BNPL platform is specified
  from **published South African provider terms** rather than from provider cooperation, confirming
  no firm contact is needed. **D11:** eligibility is *banked-only*, since both major providers debit
  a bank card at checkout, which caps access at **83.1% of the population by observed data**, so the
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
  FinScope match (45 groups, min 23 agents, median 84, verified against the 5,000-agent parquet).
  Need-driven borrowing is not socially transmitted. Key discovery justifying the change:
  **Cardaci (2018), already the primary ABM anchor, models peer effects and expenditure cascades
  centrally**, so the no-interaction design was the deviation, not the addition. Mechanism anchored
  to Granovetter (1978) threshold models; domain to Ackert et al. `beta = 0` recovers the previous
  model exactly and is the **control arm**, which also lets RQ1 separate the financial loop (borrow
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
  (from 3,250 unique source households) → `synthetic_population_5000.parquet`. P4 extended with a
  live resample-fidelity section (income KS gap 0.012, flag gap 0.3pp, shares ±1.5pp), now **14/14
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
