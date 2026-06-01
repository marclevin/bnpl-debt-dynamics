# Matching — NIDS ← FinScope (simple cell-donor)

How financial-inclusion flags from **FinScope 2019** are attached to **NIDS Wave 5** households.
Deliberately simple ("ignorant") matching — transparent and easy to defend, not a precision fusion.
All NIDS monetary values stay in **2017 Rands**; FinScope flags are categorical and need no deflation.

> Replaces the earlier hot-deck/IPF fusion. See [`decision.md`](decision.md) Set 5. Resolved and
> validated against real data in `scratchpad` (P2 logic) — marginals reproduce within ≤1.8%.

---

## Direction

```
  NIDS household (recipient)  ◄── copy flags ──  FinScope respondent (donor)
  rich: income, expenditure, debt              rich: banked, credit, savings, informal
```

NIDS is the backbone we keep; FinScope only lends its financial-inclusion flags.

---

## Match cell

Both surveys are bucketed into the **same** cells, then donors are drawn within cell:

1. **Income quintile (per-capita).**
   - NIDS: per-capita income quintiles already on the backbone (bounds R900 / R1,801 / R3,400 / R7,712).
   - FinScope: per-capita income = `M13_MHI_Imputed` **band midpoint** ÷ `Number_in_HH`, then bucketed
     using the **NIDS** quintile bounds (identical edges → comparable cells). Band midpoints:
     No Income→0, R1–999→500, R1,000–2,999→2,000, R3,000–7,999→5,500, R8,000–11,999→10,000,
     R12,000–29,999→21,000, R30,000+→40,000.
2. **× Province** (secondary). Province names align **exactly** across surveys (no harmonization
   needed). Feasibility checked: 45 quintile×province cells, **min 30 donors, none < 20** — so the
   province split is used directly, no fallback required in practice.
3. **Fallback.** If any cell is too thin, fall back to quintile-only for that cell (logged).

## Donor draw

For each NIDS household, draw one FinScope respondent from its cell (weighted by `HH_WEIGHT16`,
with replacement) and copy its flags: `banked`, `credit_access_formal`, `informal_finance`,
`savings_product` (+ the `K7` saving band and `G10`–`G14` product holdings for servicing).

---

## Flag derivation (FinScope 2019, text-labelled)

| Flag                   | Rule                                                                               | Nat. rate |
| ---------------------- | ---------------------------------------------------------------------------------- | --------- |
| `banked`               | `F1 == "Yes"` (binary)                                                              | 82.4%     |
| `credit_access_formal` | `G5` ∈ {Bank, Retail store, Micro finance, Insurance} **OR** any `G10`–`G14` == Yes (excl. lay-by `G15`) | 26.4% |
| `informal_finance`     | `G5` ∈ {Mashonisa, Stokvel/burial, Friends/family, Colleagues, Employer advance}    | 9.1%      |
| `savings_product`      | `K7` is a valid Rand band                                                           | 49.9%     |

---

## Servicing rate → `monthly_trad_repayment`

**Neither survey records a repayment amount**, so the monthly servicing cost is *constructed*:

```
weighted_apr, weighted_term = mix over the donor's held products (G10–G14)
                              using data/config/credit_rate_table.csv
monthly_trad_repayment       = amortize(D_trad, weighted_apr, weighted_term)
                              = D_trad · r / (1 − (1+r)^(−n)),  r = apr/12, n = term_months
```

- The APR/term table is **external and user-populated** (`data/config/credit_rate_table.csv`) — fill
  from NCR / regulator / BNPL provider. The pipeline **refuses to run** while any `PLACEHOLDER_`
  remains, so a placeholder can never silently enter results.
- If `D_trad > 0` but the donor flags no product, use the `other_default` class.

**Realism guards (documented assumptions).** Because a NIDS debt *balance* (a stock) is paired with a
FinScope product *type* (independent within the cell), naïve amortization could force impossible debt
service (e.g. a large balance labelled a 1-month "short-term loan"). Two parameters bound this:

- `MIN_TERM_MONTHS = 6` — term floor: a stock balance is never amortized faster than 6 months.
- `MAX_DSTI = 0.65` — NCA-style affordability ceiling; `monthly_trad_repayment` is capped at
  `MAX_DSTI × monthly income`.

After the fix: max DSTI = 0.65, **0** households with repayment > income (was 68), weighted-mean DSTI
by quintile 3–6%. The raw (pre-cap) value is retained as `repay_uncapped` for transparency.

---

## Validation (match diagnostics)

- **National marginals** of the matched synthetic population reproduce FinScope national rates
  within tolerance. *Validated:* banked +0.4, credit +1.5, informal +0.1, savings +1.8 (pp).
- **Cell marginals** match by construction (correctness check).
- Behavioural validation (default rates, DTI) is **deferred to BNPL-provider targets** — see
  [`../OVERVIEW.md`](../OVERVIEW.md) §7.

---

## What it does *not* do

- Preserve household-level joint structure beyond the cell variables (quintile × province).
- Correct the 2017↔2019 vintage gap (recorded as a limitation).
- Measure servicing from data (constructed from an external rate table).
