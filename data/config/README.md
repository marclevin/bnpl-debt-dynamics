# Config — external assumptions you populate

## `credit_rate_table.csv`

Drives `monthly_trad_repayment` in the P2 notebook. Because **neither NIDS nor FinScope records a
debt repayment amount**, the monthly servicing cost is *constructed*, not measured:

```
monthly_trad_repayment = amortize(D_trad, weighted_apr, weighted_term)
```

where the APR and term are a **product-mix-weighted** average over the FinScope credit products the
matched donor holds (`G10`–`G14`), using the per-product-class rates in this table.

**The APR values are PLACEHOLDERS** (prefixed `PLACEHOLDER_`). Replace them with sourced figures —
e.g. NCR product-class averages, regulatory caps, or rates obtained directly from a BNPL/credit
provider — and delete the prefix. The pipeline halts/warns on any remaining `PLACEHOLDER_` so a
placeholder can never silently enter results.

| Column        | Meaning                                                          |
| ------------- | --------------------------------------------------------------- |
| product_class | Credit product class label                                      |
| finscope_col  | FinScope yes/no column that flags holding this product          |
| apr_annual    | Annual percentage rate (decimal, e.g. 0.22 = 22%) — **fill in** |
| term_months   | Representative repayment term in months — **fill in**           |
| source_note   | Where the figure came from (for the methods chapter)            |

`other_default` (no `finscope_col`) is the fallback when a household has `D_trad > 0` but the donor
flags no specific product.
