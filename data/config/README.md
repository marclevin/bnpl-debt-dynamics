# Config: sourced external parameters

## `qlfs_2017_labour_flows.json`

Supplies the **plausibility band for the fitted income-shock probability `p`** (D1), and underpins
the shock *mechanism*: following Madeira, the shock is a **separation from employment**, not an
abstract fractional income cut, so its magnitude is the household's wage component (`w5_hhwage`)
rather than a chosen parameter.

Source: Statistics South Africa, *Labour Market Dynamics in South Africa, 2022*, **Report 02-11-02**.
The 2022 edition reports the QLFS panel for **2017–2022**, so a **vintage-matched 2017** figure is
available for the NIDS W5 population.

**Q3:2017 → Q4:2017, individual basis (Table 2.1a, p.15):**

| Transition from employed | Thousands | % |
| --- | --- | --- |
| Retained employment | 15 081 | 93.14 |
| To unemployed | 572 | 3.53 |
| To not economically active | 538 | 3.32 |
| **Left employment (combined)** | **1 110** | **6.86** |

Converted to the 14-day tick (6.52 ticks per quarter, constant hazard), this gives a band of
**0.54% (narrow, employed→unemployed) to 1.17% (broad, employed→not employed) per tick**.

Regenerate with:

```
python notebooks/scripts/extract_qlfs_lmd.py
```

The script asserts **two of the report's own prose statements** (retention fell 1.9 pp between 2017
and 2022 → 93.1 − 91.2; unemployment→employment "11,6 % in 2017") and requires headline **Table
2.1a** and appendix **Table A.1** to agree on the same transition, so the extraction cannot silently
drift. Same discipline as `ccmr_2017_baseline.json`.

### ⚠ This is a cross-check, not a fifth validation target

`p` is **fitted to CCMR arrears**. Fitting it to the QLFS band as well would over-determine the
baseline. The band is reported alongside the fitted value; a fitted `p` far outside it is evidence
the shock process is carrying stress the rest of the model should be generating.

### ⚠ Limitation: individual vs household

QLFS counts **individuals**; the model shocks a **household**. A multi-earner household faces a
higher probability that at least one earner separates, so the household hazard sits at or above the
individual rate. Order-of-magnitude band, exactly like the account-vs-household mismatch on the CCMR
target. Also, the model shock is non-persistent (one tick) while a real separation may last
quarters, so the band bounds shock **onset**, not the stock of unemployed households.

---

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
| Incidental credit agreements | 2% per month | n/a |

### ⚠ Limitation: these are ceilings, not observed averages

The NCR **Consumer Credit Market Report does not publish interest rates**; it reports credit
granted, gross debtors book, and age analysis (arrears) only. No public 2017 source gives observed
average APRs by product class for this population, so the statutory maximum is used as the
best-sourced available figure. This **biases servicing upward**. It is defensible for a low-to-middle
income population, where unsecured lenders price at or near the cap, but must be stated as a
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
| apr_annual | Annual rate (decimal): statutory max for the sub-sector |
| apr_source | Provenance of the rate |
| term_months | Representative repayment term |
| term_source | Provenance, or the explicit marker `ASSUMPTION` |

`other_default` (no `finscope_col`) is the fallback when `D_trad > 0` but the donor flags no
specific product.

---

## Affordability rule: NCA Regulation 23A(9)

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

### ⚠ Limitation: household vs individual

Reg 23A applies to an individual **consumer**. It is applied here to NIDS **household** income,
because the agent is a household. This is a stated simplification, not an oversight.

### Diagnostic

53 debtor households have income at or below the Reg 23A minimum-expense norm, so **no
NCA-compliant lender could have granted their debt**. This is reported as a finding: evidence of
informal or reckless credit, or of NIDS income under-reporting, rather than silently capped away.
