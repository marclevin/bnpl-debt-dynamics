# Config — sourced external parameters

## `credit_rate_table.csv`

Drives `monthly_trad_repayment` in the P2 notebook. Because **neither NIDS nor FinScope records a
debt repayment amount**, monthly servicing is *constructed*, not measured:

```
monthly_trad_repayment = min( amortize(D_trad, weighted_apr, weighted_term),
                              NCA Reg 23A affordable capacity )
```

APR and term are a **product-mix-weighted** average over the FinScope credit products the matched
donor holds (`G10`–`G14`).

### Where the APRs come from

Each product class is mapped to its **NCA sub-sector**, and the APR is set to the **statutory
maximum prescribed interest rate** for that sub-sector under the *Limitations on Fees and Interest
Rates Regulations*, in force from **6 May 2016** and therefore the regime applicable in **2017**.
Rates are evaluated at the **2017 repo rate of 7.00%** (SARB; cut to 6.75% on 21 July 2017).

| NCA sub-sector | Formula | At repo 7.00% |
| --- | --- | --- |
| Mortgage agreements | repo + 12% p.a. | 19% |
| Credit facilities (store/revolving cards) | repo + 14% p.a. | **21%** |
| Other credit agreements (hire purchase) | repo + 17% p.a. | **24%** |
| Unsecured credit transactions (personal loans) | repo + 21% p.a. | **28%** |
| Developmental credit | repo + 27% p.a. | 34% |
| Short-term credit transactions | 5% per month (first loan) | **60% nominal p.a.** |
| Incidental credit agreements | 2% per month | — |

### ⚠ Limitation — these are ceilings, not observed averages

The NCR **Consumer Credit Market Report does not publish interest rates**; it reports credit
granted, gross debtors book, and age analysis (arrears) only. No public 2017 source gives observed
average APRs by product class for this population, so the statutory maximum is used as the
best-sourced available figure. This **biases servicing upward**. It is defensible for a low-to-middle
income population — where unsecured lenders price at or near the cap — but must be stated as a
limitation and swept in sensitivity analysis.

### Terms are still assumptions

The NCA prescribes rates, not terms. Only `short_term_loan` has a statutory term basis (NCA s.1
caps short-term credit transactions at 6 months). Every other `term_months` value is an
**assumption** flagged in the `term_source` column and must be sensitivity-tested.

| Column | Meaning |
| --- | --- |
| product_class | Credit product class label |
| finscope_col | FinScope yes/no column flagging this product |
| nca_subsector | NCA sub-sector the class maps to |
| apr_annual | Annual rate (decimal) — statutory max for the sub-sector |
| apr_source | Provenance of the rate |
| term_months | Representative repayment term |
| term_source | Provenance — or explicit `ASSUMPTION` |

`other_default` (no `finscope_col`) is the fallback when `D_trad > 0` but the donor flags no
specific product.

---

## Affordability rule — NCA Regulation 23A(9)

**The NCA does not prescribe a debt-service-to-income cap.** It prescribes a **residual-income
test**: a table of minimum necessary living expenses by gross monthly income band, with credit
affordable only out of what remains. The earlier flat `MAX_DSTI = 0.65` had no statutory basis.

Source: *National Credit Regulations including Affordability Assessment Regulations*, GN R202,
Government Gazette 38557, 13 March 2015, Reg 23A(9).

| Gross monthly income | Minimum monthly fixed factor | % of income above band minimum |
| --- | --- | --- |
| R0.00 – R800.00 | R0.00 | 100% |
| R800.01 – R6,250.00 | R800.00 | 6.75% |
| R6,250.01 – R25,000.00 | R1,167.88 | 9.00% |
| R25,000.01 – R50,000.00 | R2,855.38 | 8.20% |
| R50,000.01 + | R4,905.38 | 6.75% |

The P2 notebook asserts both published worked examples (R2,000 → R881.00; R10,000 → R1,505.38) so
the table cannot silently drift.

This yields an **income-varying** affordability ceiling, far tighter at the bottom of the
distribution than the flat 65% it replaced:

| Income (quintile bound) | Necessary expenses | Max debt service | Implied DSTI ceiling |
| --- | --- | --- | --- |
| R900 | R806.75 | R93.25 | **10.4%** |
| R1,801 | R867.57 | R933.43 | 51.8% |
| R3,400 | R975.50 | R2,424.50 | 71.3% |
| R7,712 | R1,299.46 | R6,412.54 | 83.2% |

### ⚠ Limitation — household vs individual

Reg 23A applies to an individual **consumer**. It is applied here to NIDS **household** income,
because the agent is a household. This is a stated simplification, not an oversight.

### Diagnostic

53 debtor households have income at or below the Reg 23A minimum-expense norm, so **no
NCA-compliant lender could have granted their debt**. This is reported as a finding — evidence of
informal or reckless credit, or of NIDS income under-reporting — not silently capped away.
