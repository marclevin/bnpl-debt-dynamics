# The household agent: data to agent

Each agent is a NIDS Wave 5 (2017) household, resampled in proportion to its survey weight,
with financial-inclusion flags copied from one FinScope 2019 donor. Money is in 2017 Rands.
The thesis version of this mapping is Table 1 (`tab:agent-mapping`, Section 2.1); construction
detail is in Appendix D and the match in Appendix E.

## Fields

Fields marked *tick* are monthly survey flows scaled by 12/26 to the 14-day tick; stocks are
not scaled.

| Agent field | Meaning | Source |
| --- | --- | --- |
| `income_monthly` | Total monthly income | NIDS `w5_hhincome` |
| `income_wage_tick` | Wage income, the part an income shock removes | NIDS `w5_hhwage` |
| `n_earners` | Employed members on the roster | NIDS individual file |
| `income_source` | Dominant source: WAGE, GRANT or OTHER (remittances and all else) | NIDS income components |
| `committed_tick` | Food and rent paid, which the household cannot reduce | NIDS food and rent expenditure |
| `discretionary_tick` | All other non-food cash spending, including transport and utilities | NIDS non-food expenditure |
| `liquid_savings` | Financial assets, winsorised at the 99th percentile | NIDS `w5_f_ass` |
| `d_trad` | Outstanding traditional debt | NIDS `w5_f_deb` |
| `apr_annual`, `term_months` | Rate and horizon for that balance, from the donor's flagged products | statutory 2017 maxima and Table `tab:credit-terms` |
| `scheduled_service_tick` | Debt service per tick, amortised and capped by Regulation 23A | constructed |
| `banked` | Eligibility for BNPL | FinScope, imputed |
| store card, revolving credit, hire purchase, short-term loan, personal loan | Product flags that price the opening debt | FinScope, imputed |
| `income_quintile` | Weighted per-capita income quintile; match key | NIDS |
| `province` | Match key and reference-group key | NIDS |
| `reference_group` | Quintile by province, whose adoption the household observes | derived (45 groups) |
| `household_size` | Members | NIDS `w5_hhsizer` |

Two attributes are not observed: every agent starts with no BNPL balance (the injection
design), and its repayment archetype, minimum-payer or scheduled-payer, is assigned at random
with probability 0.29 of being a minimum-payer.

## How the population is built

| Step | What it does | Where |
| --- | --- | --- |
| P1 backbone | 13,719 NIDS records filtered to 10,841 households with income, size and a positive weight; income, expenditure, savings and debt derived | `notebooks/p0_backbone.ipynb` |
| P2 match | One FinScope donor per household, drawn in proportion to weight within its quintile-by-province cell (45 cells, each with at least 30 donors); all six flags copied together | `notebooks/p2_finscope_match.ipynb` |
| P3 resample | 5,000 households drawn with replacement in proportion to weight (3,221 unique sources) | `notebooks/p3_resample.ipynb` |
| P4 validate | Construction, imputation and resampling checks (Table `tab:validation`) | `notebooks/p4_validation.ipynb` |
| P5 instantiate | Each row becomes a household agent | `simulation/population.py` |

## Assumptions to keep in view

- **2017 throughout.** Results describe a 2017 population with BNPL added; they are not
  forwarded to a later year.
- **FinScope 2019 stands in for 2017.** The flags are categorical, so they need no deflation,
  but 2019 banking may overstate access in 2017.
- **The match reproduces cell marginals.** It keeps the joint structure of product holdings
  within a donor, but ignores recipient characteristics outside the match keys, such as urban
  or rural location.
