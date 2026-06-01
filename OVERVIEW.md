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
| **P0** | Load & inspect NIDS W5 + FinScope 2019 | clean dataframes, key/flag inventory | ☐ |
| **P1** | Build NIDS backbone in 2017 units | per-household record + quintile tag | ☐ |
| **P2** | Simple cell-donor match from FinScope | flags attached to each household | ☐ |
| **P3** | Weighted resample to 5,000 | fixed synthetic population | ☐ |
| **P4** | Validate (internal + match diagnostics) | validation report | ☐ |
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

- **2026-06-01** — Switched to **2017-only** units (dropped CPI forwarding, IES, 2022-level
  validation). Reintroduced a **simple FinScope cell-donor match** (replacing crude per-quintile
  imputation). Behavioural validation deferred to BNPL-provider targets. OVERVIEW.md promoted to
  living source of truth.
- *(earlier)* — Simplified from multi-survey hot-deck fusion to single-source NIDS resample.
