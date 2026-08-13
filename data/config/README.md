# Config: sourced external parameters

## `cpi_deflator_2017.json`

**Every monetary quantity in this model is 2017 Rands** — the NIDS backbone, the Reg 23A expense
table, the CCMR arrears targets, the statutory rates at the 2017 repo rate. The BNPL parameters were
the exception until the 2026-08-12 QA pass: purchase size, the Payflex per-order cap and the Payflex
late fees were all taken at **current vintage** and used unadjusted, denominating the BNPL side of
the model roughly **1.4× too high** against everything it interacts with (DEFECTS.md **B29**).

This file is the single documented factor that fixes it, applied once in `simulation/config.py` so a
published nominal figure and the 2017-Rand value the model uses cannot drift apart.

Source: Statistics South Africa, *Consumer Price Index*, statistical release **P0141**, headline CPI,
**annual average** basis. The annual average is the right basis because the quantities being
deflated are averages over a year — an average order value, a tariff in force across a year — not
point-in-time observations.

| From 2017 to | Factor | Used for |
| --- | ---: | --- |
| 2024 | 1.3942 | the GMV-weighted vintage of the derived average order value |
| 2025 | 1.4391 | the FY2025 volume anchors |
| mid-2026 | 1.5111 | the published Payflex terms and the trade-press basket |

**The 2026 figure is a published anchor, not a part-year guess** (pinned 2026-08-13). 2026 has no
annual average yet, and the Payflex terms are a mid-year source, so what is needed is the mid-2026
price level. The **June 2026 release** gives it: headline index **107.5** (Dec 2024 = 100) and
**5.0%** year-on-year. The year-on-year rate is exactly the right multiplier, because an annual
average sits at the mid-point of its year under smooth price movement — so the 2025 annual average
*is* approximately the mid-2025 level, and June 2026 is twelve months later.

### The drift check that narrows the `% VERIFY`

The published June 2026 index can be compared against what the compounded rate chain implies for the
same date. It implies **106.68** against a published **107.5**, a **−0.77%** gap, which the script
asserts against a 1.5% tolerance. The residual comes from approximating each year's average by its
mid-point; it is recorded rather than tuned away, and it bounds the error on a factor of ~1.5 at
well under one per cent.

⚠ The 2018–2025 annual averages are still from published releases rather than re-derived from
**P0141 Table B1** (statssa.gov.za blocks automated retrieval; Table B1 sits in the appendix of each
monthly release). But they are now constrained by **two independent checks** — the 2024 rate against
Stats SA's own published 4,4% statement, and the whole chain against the June 2026 index. Pin to
Table B1 when convenient; the flag is narrow, not open-ended.

**Rebasing.** Stats SA rebased at Dec 2016, Dec 2021 and Dec 2024 = 100. Index numbers either side
of a rebase are not directly comparable without the published linking factors. This chain is built
from annual **rates**, which are rebase-invariant, so the issue does not arise.

Regenerate with:

```
python notebooks/scripts/extract_cpi_deflator.py
```

---

## `ies_2022_bnpl_share.json`

Supplies **`kappa`**, the share of a household's discretionary budget spent on the categories BNPL
actually finances, which is what sizes a BNPL purchase in D4. It replaces a flat national constant
of R1,568 taken from trade press, which was the model's single largest driver of output and was also
**127% of the median banked Q1 household's monthly discretionary budget** (DEFECTS.md **B24/B30**).

Source: Statistics South Africa, *Income and Expenditure Survey 2022/2023* household microdata
(DataFirst `zaf-statssa-ies-2022-2023-v1`), COICOP 2018, 19,940 households weighted to ~21.3m.

Mapping — apparel, homeware and appliances, consumer electronics and sporting goods, which is what
both major providers' merchant networks sell:

| COICOP 2018 | Included |
| --- | --- |
| 03 | Clothing and footwear, in full |
| 05.1–05.5 | Furniture, textiles, appliances, utensils, tools |
| 08.1 | ICT equipment — devices, **not** airtime or data |
| 09.1–09.2 | Recreational durables and other recreational goods |

Deliberately excluded: 05.6 routine household maintenance, 08.2–08.3 software and communication
services, and every service group in 09. Division 09 moves the result by under a quarter of a
percentage point either way, which the script reports.

**Result: 13.87% of discretionary expenditure.** The denominator matches the model's own
`expenditure_discretionary` definition — total consumption less food (division 01) and less actual
rentals (04.1) — with imputed rentals (04.2) removed from both sides, since NIDS non-food
expenditure carries no imputed rent for owner-occupiers.

The script asserts Stats SA's published headline for this survey — clothing and footwear at **5.0%**
of total household consumption expenditure, against **5.18%** extracted — so it cannot silently
drift. Regenerate with:

```
python notebooks/scripts/extract_ies_bnpl_share.py
```

### ⚠ Vintage: a ratio, never an amount

The survey is 2022/23 and the model is 2017. **Only a ratio is taken, never a money amount**, so the
vintage cannot contaminate the model. This is the identical argument already made and accepted for
the FinScope 2019 categorical flags in P2, and it is the reason the level comes from elsewhere.

### The share is flat across Q1–Q4 and lower at the top

By expenditure quintile: **0.196, 0.225, 0.217, 0.200, 0.110**. The near-flatness across the first
four quintiles is what makes a single proportional `kappa` defensible; Q5's lower share is the one
place a single ratio does violence to the data, and is worth a sentence. The value used is the
**aggregate** ratio (0.1387), not the mean of household ratios — the same choice, for the same
reason, as the aggregate debt-to-income statistic in B19b: a mean of ratios over a population with
near-zero denominators is not a meaningful measure.

---

## `bnpl_anchors_2017.json`

**Validation targets, not inputs.** Quantities the model is checked against *after* the purchase
rule above has already fixed its own scale from IES.

**Primary source (pinned 2026-08-13): Weaver Fintech, *Integrated Report 2025*, page 14**, the
"Profitable BNPL network" panel. PayJustNow is the BNPL business in that group and one of the four
SA platforms the model represents. ⚠ The entity was renamed: **HomeChoice International plc → Weaver
Fintech Ltd (JSE: WVR)**.

One page discloses all of it: cumulative BNPL GMV **R13.1bn**, cumulative transactions **9.4m**,
**3.7m signed-up customers**, and an annual frequency series of **1.8x, 2.2x, 2.8x, 3.9x, 4.4x**
(FY2021–FY2025). **No document states an average order value** — it falls out of dividing two
disclosed aggregates, which is why this is an extraction script rather than a citation.

| Target | 2017 Rands | Derivation |
| --- | ---: | --- |
| Mean BNPL purchase | **R992** | R13.1bn ÷ 9.4m, deflated at the GMV-weighted vintage (2024.2) |
| Volume per **signed-up** user per year | **R1,333** | FY2025 GMV R7.1bn ÷ 3.7m signed-up |
| Volume per **active** user per year | **R4,261** | 4.4 × R992 |

**The volume target is a band, not a point**, because the frequency rate's denominator is not
defined on the page. Compare the model's volume per **adopting** household against the upper bound
and per **eligible** household against the lower.

**Two cross-checks are asserted.** The FY2024 annual GMV series must reproduce this report's
cumulative chart at every shared year (R0.9bn, R2.4bn, R6.3bn) — two documents, two presentations,
one quantity. And the derived FY2025 GMV must land near the separately stated R7.1bn; it comes in at
R6.7bn, a −5.7% gap recorded rather than tuned away.

### ⚠ The R7,000 metric is dropped, and why

The FY2024 report states *"Frequency is up to 2.12 per annum, average spending is up 21% to 7 000."*
Read as a BNPL order value that implies R3,302 — contradicting the R1,394 the cumulative aggregates
give, and anomalously high for South African apparel and homeware checkouts. It is a **group-wide
fintech metric**: Weaver cross-sells personal lending, a wallet and insurance alongside BNPL, so
R7,000 across 2.12 transactions describes a blended portfolio, not a basket. The FY2025 report
settles it by publishing a **BNPL-specific** frequency series, which is what this file now uses.

This band is the check the thesis previously lacked entirely, and it is what turns B25's "these
volumes look implausible" into a measured statement.

```
python notebooks/scripts/extract_bnpl_anchors.py
```

---

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
