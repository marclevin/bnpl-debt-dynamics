# Matching: NIDS ← FinScope (simple cell-donor)

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

- The APR/term table (`data/config/credit_rate_table.csv`) is **sourced from the NCA statutory
  maximum prescribed interest rates** per sub-sector (regime in force 6 May 2016, so 2017-valid),
  evaluated at the **2017 repo rate of 7.00%**: credit facilities 21%, other credit agreements 24%,
  unsecured 28%, short-term 5% per month. See `data/config/README.md` for the full mapping and the
  ceilings-not-averages limitation.
- If `D_trad > 0` but the donor flags no product, use the `other_default` class.

**Guards.** Because a NIDS debt *balance* (a stock) is paired with a FinScope product *type*
(independent within the cell), naive amortization could force impossible debt service, for example a
large balance labelled a short-term loan. Two parameters bound this:

- `MIN_TERM_MONTHS = 6`. Term floor: a stock balance is never amortized faster than 6 months.
  **Still an assumption**, not sourced.
- **NCA Regulation 23A(9) residual-income ceiling** (replaced the earlier flat `MAX_DSTI = 0.65`,
  which had no statutory basis). The NCA prescribes no debt-service-to-income ratio; it prescribes a
  minimum expense-norms table by gross income band. Debt service is capped at
  `gross income − Reg 23A necessary expenses`, giving an **income-varying** ceiling: 10.4% of income
  at R900/month rising to 83.2% at R7,712/month.

Result: max DSTI 0.911, **0** households with repayment > income, weighted-mean DSTI by quintile
2.8–6.1%. The guard binds for only **3.4% of debtors** (158 of 4,702), so the APR/term assumptions
produce affordable servicing unaided for the rest. The raw pre-cap value is retained as
`repay_uncapped`, and `nca_max_service` records each household's ceiling.

**Diagnostic:** 53 debtor households have income at or below the Reg 23A norm, so no NCA-compliant
lender could have granted their debt. Reported as a finding, not capped away.

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
