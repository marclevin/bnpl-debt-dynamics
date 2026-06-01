# Matching — NIDS ← FinScope (simple cell-donor)

How financial-inclusion flags from **FinScope 2019** are attached to **NIDS Wave 5** households.
Deliberately simple ("ignorant") matching — transparent and easy to defend, not a precision fusion.
All NIDS monetary values stay in **2017 Rands**; FinScope flags are categorical and need no deflation.

> This replaces the earlier hot-deck/IPF fusion design. See [`decision.md`](decision.md) Set 5.

---

## Direction

```
  NIDS household (recipient)  ◄── copy flags ──  FinScope respondent (donor)
  rich: income, expenditure, debt              rich: banked, credit, savings, informal
```

NIDS is the backbone we keep; FinScope only lends its financial-inclusion flags.

---

## Method: cell-donor by income quintile

1. **Compute income quintiles separately in each survey**
   - NIDS: weighted quintiles of `w5_hhincome` using `w5_wgt`.
   - FinScope: weighted quintiles of its household-income variable using its weight (`HH_WEIGHT16`).
2. **Define matching cells**
   - Primary cell: **income quintile** (Q1–Q5).
   - Secondary (optional): **× province**, used only where the resulting cell has enough FinScope
     donors (threshold documented at build time; fall back to quintile-only if too thin).
3. **Draw a donor**
   - For each NIDS household, randomly draw one FinScope respondent from the same cell (with
     replacement) and **copy its flags**: `banked_status`, `credit_access_formal`,
     `savings_product`, `informal_finance`.
4. **Done** — no distance metric, no regression, no iterative fitting.

---

## Why this method

- **Transparent:** a supervisor or examiner can understand it in one sentence.
- **Honest about precision:** the 2017↔2019 vintage gap and the proxy nature of FinScope don't
  justify a more elaborate match.
- **Preserves cell marginals:** by construction, flag rates within each income-quintile cell match
  FinScope — which is exactly what the validation diagnostics check.

---

## What it does *not* do

- It does not preserve household-level joint structure beyond the cell variables.
- It does not correct for the 2-year vintage gap (recorded as a limitation).
- It does not use household-level FinScope income matching beyond the quintile cell.

---

## Validation (match diagnostics)

After matching, confirm:

- **Cell marginals:** flag rates per income-quintile cell in the synthetic population reproduce the
  FinScope cell rates (they should, by construction — this is a correctness check).
- **National marginals:** weighted national banked rate, formal-credit rate, etc. in the synthetic
  population fall within tolerance of FinScope's national figures.

Behavioural validation (default rates, DTI) is **deferred to BNPL-provider targets** — see
[`../OVERVIEW.md`](../OVERVIEW.md) §7.

---

## Build notes (P0/P2)

- Resolve exact FinScope question codes for each flag against the questionnaire PDF
  (`data/raw/FINMARK_2019/FinScope SA 2019 FINAL QNR REV. ...pdf`) — the CSV columns are coded
  (`A*`, `B*`, `C*` blocks).
- Confirm the FinScope household-income variable and weight column before computing quintiles.
- Log donor-cell sizes; flag any cell that falls back from quintile×province to quintile-only.
