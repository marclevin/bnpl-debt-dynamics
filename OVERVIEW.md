# Project Overview — Living Source of Truth

**Project:** Modelling BNPL impact on the South African consumer credit market (Agent-Based Model).
**This file is the canonical strategy + execution plan.** When a decision changes, change it here
first, then propagate to the companion docs. Last updated: **2026-06-01**.

---

## 1. The question

How do **Buy Now Pay Later (BNPL)** platforms affect consumer debt saturation and the potential
for systemic default in South Africa? We answer with an **agent-based model (ABM)** (Python/Mesa)
whose core engine is the household **balance sheet** — money and debt flowing through a population
of household agents over time.

---

## 2. Strategy in one breath

Build a synthetic population of **household agents from NIDS Wave 5 (2017)**, enrich each with
**financial-inclusion flags matched in from FinScope**, and keep **everything in 2017 units** — no
inflation-forwarding, no second monetary reference year. Get a clean, validated *consumer*
population working first; BNPL and a richer lender market come later.

**The five commitments that keep this simple:**

1. **One reference year: 2017.** NIDS W5 is the backbone; all monetary values stay in 2017 Rands.
   **No CPI forwarding. No IES. No 2022-level targets.**
2. **One backbone source: NIDS W5.** Income, expenditure, debt, demographics, weights.
3. **One donor source: FinScope.** Provides financial-inclusion flags only, via a simple match.
4. **Simple match, not fusion.** Cell-donor by income quintile (× province where cell sizes allow)
   — copy a random FinScope respondent's flags onto each NIDS household.
5. **Validation is light now; behavioural targets come from BNPL providers later.** We check the
   population is internally consistent and the match reproduces FinScope marginals — nothing more.

---

## 3. Data sources

| Source           | Year | Role                                                              | In/Out         |
| ---------------- | ---- | ---------------------------------------------------------------- | -------------- |
| **NIDS Wave 5**  | 2017 | **Backbone** — income, expenditure, debt, demographics, weights  | **In**         |
| **FinScope SA**  | 2019 | **Donor** — banked status, credit access, savings, informal flags| **In** (proxy) |


**FinScope note:** A 2017 FinScope wave is **not in our data** — we use **FinScope 2019** as a
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

## 5. Execution plan — building the household agent

```
  NIDS W5 (backbone, 2017)              FinScope 2019 (donor)
  hhderived.csv + head demog            flags + matching keys
        │                                      │
        ▼                                      │
  [P1] BACKBONE                                │
   derive: income_source, committed/           │
   discretionary, savings proxy, D_trad,       │
   quintile  (NO CPI — stays 2017)             │
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
| **P4** | Validate (internal + match diagnostics) | validation report | ☑ `notebooks/p4_validation.ipynb` — 14/14 checks pass |
| **P5** | Instantiate agents | Household agents in Mesa | ☐ |

---

## 6. Scope boundaries

**In scope now**

- NIDS W5 → 5,000 weighted household agents, quintile-tagged, **2017 Rands**.
- Simple FinScope cell-donor match for financial-inclusion flags.
- Consumer balance sheets + one minimal lender stub.
- Internal-consistency + match-diagnostic validation.

**Deferred (future work)**

- BNPL platform agent and multi-lender market.
- **Behavioural validation targets sourced from BNPL providers.**
- Geography beyond the match cell, peer-to-peer networks, dynamic composition.

---

## 7. Validation

- **Internal consistency:** synthetic population reproduces the **weighted NIDS W5** distributions
  it was sampled from (income quintile shares, household composition).
- **Match diagnostics:** imported FinScope flags reproduce **FinScope marginals** (e.g. national
  banked rate, credit-access rate) within tolerance.
- **Behavioural validation:** **deferred** — targets to be obtained from **BNPL providers**, not
  from CPI-forwarded survey aggregates.

---

## 8. Companion documents

- [`scratchpad/decision.md`](scratchpad/decision.md) — the design decisions, with rationale.
- [`scratchpad/variables.md`](scratchpad/variables.md) — column-level variable mapping (NIDS + FinScope).
- [`scratchpad/data_fusion.md`](scratchpad/data_fusion.md) — the simple cell-donor **matching** method.
- [`household_agent.md`](household_agent.md) — data → agent mapping, presentation-ready.
- [`scratchpad/work.md`](scratchpad/work.md) — ABM design narrative.

---

## 9. Changelog (living)

- **2026-06-01 (showcase)** — Built `notebooks/00_showcase.ipynb`: a supervisor-facing guided tour
  (what each phase did, with visuals), a benchmark validation scorecard (7/7 ✓, incl. Gini 0.651 and
  FinScope flag rates), and a plain-English profile of a fixed-seed sample agent.
- **2026-06-01 (head demographics)** — Added the deferred head-of-household demographics to P0
  (`age_head`, `gender_head`, `race_head`, `education_head` + coarse `education_band`), joined via
  the roster head (`w5_r_relhead==1`) → individual-derived file (99% matched). Propagated through
  P2/P3 into `synthetic_population_5000.parquet`; added a demographics section to the visualizer.
  Education×quintile gradient is textbook (Q1 4% tertiary → Q5 54%). **Static data layer complete.**
- **2026-06-01 (P3)** — Built `notebooks/p3_resample.ipynb`: weighted resample to **5,000 agents**
  (from 3,250 unique source households) → `synthetic_population_5000.parquet`. P4 extended with a
  live resample-fidelity section (income KS gap 0.012, flag gap 0.3pp, shares ±1.5pp) — now **14/14
  pass**. Population-size stability checked at 1k/5k/10k. The static household-agent data layer is
  complete; next is the ABM (rules, environment, lender).
- **2026-06-01 (P4 + fixes)** — Diagnostics surfaced servicing/DSTI outliers (68 hh with
  repay>income, max DSTI 25×) from the stock-balance × product-term mismatch. Fixed with a term
  floor (`MIN_TERM_MONTHS=6`) + NCA-style affordability cap (`MAX_DSTI=0.65`): now 0 hh over income,
  DSTI 3–6% by quintile. Built `notebooks/p4_validation.ipynb` (benchmark comparisons + pass/fail,
  **10/10 pass**, incl. emergent Gini 0.651 in the SA band). Toned down the visualizer's clustering
  framing (PCA<50% var, weak silhouette → continuum, not natural clusters).
- **2026-06-01 (viz)** — Rate table populated → P2 re-run, `monthly_trad_repayment` computed for all
  10,841 households (4,702 debtors; quintile DSTI 3–9%). Built `notebooks/p1p2_visualizer.ipynb`:
  quintile archetype profiles (`data/processed/quintile_archetypes.csv`), balance-sheet / flag /
  source / bivariate / province views, and an unsupervised K-means structure check vs the quintiles.
- **2026-06-01 (P2)** — Built `notebooks/p2_finscope_match.ipynb`: FinScope codes **resolved** (F1
  banked, G5/G10–G14 formal credit, K7 savings, M13_MHI income); cell-donor match on per-capita
  income quintile × province (45 cells, ≥30 donors, **0 fallbacks**); matched marginals reproduce
  FinScope within **≤2.3 pp**. `monthly_trad_repayment` constructed via product-mix amortization
  over an **external, user-populated** `data/config/credit_rate_table.csv` (placeholder-guarded, so
  not yet computed). `liquid_savings` winsorized at the 99th pct. Output:
  `data/processed/synthetic_population_matched.parquet`.
- **2026-06-01 (P1)** — Built `notebooks/p0_backbone.ipynb`: NIDS W5 loaded (13,719 → **10,841
  valid households**), backbone derived in 2017 Rands (income source, committed/discretionary
  expenditure, balance sheet), **per-capita weighted income quintiles** assigned (bounds
  R900 / R1,801 / R3,400 / R7,712). Outputs in `data/processed/`. Next: P2 FinScope match.
- **2026-06-01** — Switched to **2017-only** units (dropped CPI forwarding, IES, 2022-level
  validation). Reintroduced a **simple FinScope cell-donor match** (replacing crude per-quintile
  imputation). Behavioural validation deferred to BNPL-provider targets. OVERVIEW.md promoted to
  living source of truth.
- *(earlier)* — Simplified from multi-survey hot-deck fusion to single-source NIDS resample.
