# Key Decisions — Synthetic Population & ABM

Design decisions for the **2017-anchored, single-backbone** approach. Canonical strategy lives in
[`../OVERVIEW.md`](../OVERVIEW.md) — this document records the *why* behind each decision.

> **Current direction (2026-06-01).** Work **exclusively in 2017 units**. NIDS Wave 5 is the
> backbone; FinScope provides financial-inclusion flags via a **simple cell-donor match**. No CPI
> forwarding, no IES, no 2022-level validation. Behavioural validation targets to come from BNPL
> providers later.

---

## Decision Set 1: Temporal Scope

- **Reference year:** **2017** (NIDS W5 reference period). All monetary values stay in 2017 Rands.
  **No inflation-forwarding.** This is the central simplification: one period, one set of prices.
- **Time step:** Biweekly. Aligns with pay-in-4 BNPL cadence (extension) and divides cleanly into
  monthly income/expenditure data.
- **Simulation horizon:** 24 months (52 biweekly ticks), first 6 months (12 ticks) burn-in.

*Why 2017-only:* CPI-forwarding NIDS to 2022 introduced a second reference year, distributional
assumptions, and external validation targets we are not ready to defend. Staying in 2017 removes
all three at once. FinScope flags are categorical, so the FinScope 2019 vintage needs no deflation.

---

## Decision Set 2: Population Scope

- **Geographic scope:** Abstracted, except province is available as a secondary matching cell (Set 5).
- **Population size:** **5,000 synthetic households**, weighted-resampled from NIDS W5.
- **Household definition:** NIDS definition — co-residence + resource sharing.
- **Composition dynamics:** Static across the 24-month horizon.

---

## Decision Set 3: Data Sources

| Source          | Year | Role                                                               | Status      |
| --------------- | ---- | ----------------------------------------------------------------- | ----------- |
| **NIDS Wave 5** | 2017 | **Backbone** — income, expenditure, debt, demographics, weights   | **In**      |
| **FinScope SA** | 2019 | **Donor** — banked status, credit access, savings, informal flags | **In** |

**NIDS backbone file:** `data/raw/NIDS_W5/hhderived.csv` (household-level income, expenditure,
assets, debts, size, weights). Head demographics joined from the NIDS individual-derived file.

**FinScope donor file:** `data/raw/FINMARK_2019/Finscope South Africa 2019.csv`. 

---

## Decision Set 4: Variables

Two functional roles. **Behavioural state** drives agent decisions; **conditioning** profiles
households and segments results.

- **Behavioural state (NIDS):** monthly income (+ categorical source), committed expenditure,
  discretionary expenditure, liquid savings proxy, consolidated traditional debt, monthly servicing.
- **Behavioural state (FinScope, matched in):** banked status, formal credit access, savings
  product holding, informal credit / insurance membership.
- **Conditioning (NIDS):** income quintile, household size, composition, dependency ratio, and head
  demographics (age, gender, race, education).

All monetary fields are in **2017 Rands**. Full column-level mapping in [`variables.md`](variables.md).

---

## Decision Set 5: Matching Strategy (NIDS ← FinScope)

(This replaces the old CPI/fusion set. The method is deliberately simple — see
[`data_fusion.md`](data_fusion.md) for the full procedure.)

- **Direction:** NIDS households are the **recipients**; FinScope respondents are the **donors**.
- **Method:** **Cell-donor by income quintile.** Build matching cells from income quintile
  (× province where cell sizes allow), then for each NIDS household draw a random FinScope
  respondent from the same cell and copy its financial-inclusion flags.
- **Why this and not hot-deck/regression:** It is transparent, easy to explain to a supervisor or
  examiner, and avoids over-claiming precision the 2017↔2019 vintage gap cannot support.
- **No monetary adjustment** anywhere — flags are categorical; NIDS money stays in 2017 Rands.

---

## Decision Set 6: Agents (Consumers + Single Lender Stub)

Trimmed to the minimum needed for a baseline. BNPL and a richer lender market are **future work**.

**Consumer agents (households):**

- 5,000 households from the synthetic population.
- *Static attributes:* full variable set from Set 4 (NIDS + matched FinScope flags + quintile).
- *Dynamic state:* current liquid balance, consolidated traditional debt, monthly debt service due,
  recent-default flag.
- *Decision domains:* consumption, borrowing, repayment. Rules deferred to `decision_rules.md`.

**Single Lender (stub):** One aggregate lender holding all traditional debt; a deterministic
visible-debt gate decides applications. No competition, no adaptation.

**Deferred:** BNPL platform agent, multiple lenders, informal lenders, merchants. Informal debt
enters only as static balance-sheet state from NIDS.

---

## Decision Set 7: Topology

- **Consumer-to-lender:** Bipartite; all consumers may apply to the single lender, subject to the gate.
- **Consumer-to-consumer:** None in baseline.
- **Macro environment:** Homogeneous, exogenous (inflation, unemployment) — held in 2017 terms.
- **Income dynamics:** Static income baseline per household + a single biweekly Bernoulli shock that
  reduces savings / cash flow and can trigger borrowing.
- **Time:** Synchronous biweekly clock — consumers act, lender processes applications, state updates.

---

## Decision Set 8: Validation

- **Internal consistency:** synthetic population reproduces the **weighted NIDS W5** distributions
  it was sampled from (income quintile shares, household composition) within ~5%.
- **Match diagnostics:** imported FinScope flags reproduce **FinScope marginals** (e.g. national
  banked rate, credit-access rate) within tolerance.
- **Behavioural validation:** **deferred** — targets to be obtained from **BNPL providers**, not
  from CPI-forwarded survey aggregates.

---

## Summary of Commitments

| Set            | Commitment                                                                       |
| -------------- | -------------------------------------------------------------------------------- |
| 1. Temporal    | **2017-only**, biweekly steps, 24-month horizon, 6-month burn-in; **no CPI**     |
| 2. Population  | 5,000 households, province as match cell only, NIDS definition, static composition |
| 3. Sources     | NIDS W5 backbone + FinScope 2019 donor; IES/GHS/QLFS dropped                      |
| 4. Variables   | Behavioural (NIDS + FinScope flags) / conditioning; all money in 2017 Rands       |
| 5. Matching    | **Simple cell-donor by income quintile (× province)**; categorical flags only     |
| 6. Agents      | Consumers + single minimal lender stub; BNPL & multi-lender deferred             |
| 7. Topology    | Bipartite consumer–lender; no consumer network; static income + biweekly shock    |
| 8. Validation  | Internal (~5%) + match diagnostics; behavioural targets deferred to BNPL providers |

---

## Companion Documents

- [`../OVERVIEW.md`](../OVERVIEW.md) — living source of truth (strategy + execution plan).
- [`variables.md`](variables.md) — variable mapping to NIDS + FinScope columns.
- [`data_fusion.md`](data_fusion.md) — the simple cell-donor matching procedure.
- [`../household_agent.md`](../household_agent.md) — data → agent mapping.
- [`work.md`](work.md) — ABM design narrative.
- `decision_rules.md` — agent decision rules (to be written).

---

## Known Limitations (for methods/limitations chapter)

- **2017 reference year** — population reflects 2017 conditions; results are not forwarded to a
  current year. This is a deliberate scope choice, stated up front.
- **FinScope 2019 as a 2017 proxy** — 2-year vintage gap on financial-inclusion flags, uncorrected.
- **Cell-donor match** is crude — it preserves cell-level marginals, not household-level joint
  structure beyond the cell variables.
- **Liquid savings** is the weakest NIDS field; proxied by financial assets.
- No external behavioural validation yet (deferred to BNPL-provider targets).
- No informal credit supply, no consumer network, no spatial heterogeneity beyond the match cell,
  static household composition, single static lender rule.
