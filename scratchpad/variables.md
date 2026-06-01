# Variable Mapping — NIDS W5 backbone + FinScope donor

All variables resolve to one of two sources, **all monetary values in 2017 Rands (no CPI)**:

- **NIDS Wave 5 (2017)** — backbone. File: `data/raw/NIDS_W5/hhderived.csv`
  (labels: `hhderived_labels.json`); head demographics from the NIDS individual-derived file.
- **FinScope SA 2019** — donor for financial-inclusion flags, attached via the simple cell-donor
  match (see [`data_fusion.md`](data_fusion.md)). File:
  `data/raw/FINMARK_2019/Finscope South Africa 2019.csv`.

Two roles: **behavioural state** (drives decisions) and **conditioning** (profiles/segments).
There are no separate "linking" variables — the match uses conditioning fields directly.

---

## Behavioural state — from NIDS (2017 Rands)

### Income

| Field            | Description                               | NIDS column(s)                                                      | Derivation                                            |
| ---------------- | ----------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------- |
| `income_monthly` | Total monthly household income            | `w5_hhincome`                                                      | Direct, 2017 Rands.                                   |
| `income_source`  | Dominant source: WAGE / GRANT / OTHER     | `w5_hhwage`, `w5_hhgovt`, `w5_hhremitt`, `w5_hhother`, `w5_hhagric`, `w5_hhinvest` | Largest component → category. |

### Expenditure

| Field                       | Description                             | NIDS column(s)             | Derivation                                  |
| --------------------------- | --------------------------------------- | -------------------------- | ------------------------------------------- |
| `expenditure_total`         | Total monthly expenditure               | `w5_expenditure`           | Direct.                                     |
| `expenditure_committed`     | Non-discretionary (food + rent)         | `w5_expf`, `w5_rentexpend` | committed = food + rent.                    |
| `expenditure_discretionary` | Flexible spending                       | `w5_expnf`, `w5_rentexpend`| discretionary = non-food − rent (≥ 0).      |

### Balance sheet

| Field                    | Description                          | NIDS column(s)               | Derivation                                          |
| ------------------------ | ------------------------------------ | ---------------------------- | --------------------------------------------------- |
| `liquid_savings`         | Cash/transactional buffer            | `w5_f_ass`                   | Financial assets as proxy, **winsorized at 1st/99th pct** (weak field — see notes). |
| `D_trad`                 | Consolidated traditional debt        | `w5_f_deb`                   | Financial debts. (`w5_tot_deb` if incl. secured.)   |
| `monthly_trad_repayment` | Monthly servicing obligation         | `D_trad` × FinScope product mix | **Constructed in P2** (not measurable). Amortize `D_trad` over a product-mix-weighted APR/term from `data/config/credit_rate_table.csv`. See [`data_fusion.md`](data_fusion.md). |

---

## Behavioural state — from FinScope (matched in, categorical)

Attached to each NIDS household by the cell-donor match. Categorical flags — **no deflation**.
FinScope columns and codings **resolved** against `Finscope South Africa 2019.csv` (values are
text labels, not numeric codes). National weighted rates (validation targets) shown for reference.

| Field                  | Description                          | FinScope column → rule                                              | Nat. rate |
| ---------------------- | ------------------------------------ | ------------------------------------------------------------------ | --------- |
| `banked`               | Banked / unbanked (**binary**)       | `F1 == "Yes"`                                                       | 82.4%     |
| `credit_access_formal` | Uses formal credit                   | `G5` ∈ {Bank, Retail store, Micro finance, Insurance} **OR** any of `G10`–`G14` == "Yes" (lay-by `G15` excluded — not credit) | 26.4% |
| `informal_finance`     | Uses informal finance                | `G5` ∈ {Mashonisa, Stokvel/burial, Friends/family, Colleagues, Employer advance} | 9.1% |
| `savings_product`      | Saves / holds savings product        | `K7` is a valid Rand band (also import `K7` band + `K1_*` holdings) | 49.9%     |

**Match keys:** income quintile (per-capita; FinScope income from `M13_MHI_Imputed` band midpoint ÷
`Number_in_HH`, bucketed on the **NIDS** quintile bounds) × `Province` (names align exactly across
surveys). FinScope weight: `HH_WEIGHT16`.

---

## Conditioning — from NIDS

| Field                   | Description                               | NIDS column(s)          | Notes                                  |
| ----------------------- | ----------------------------------------- | ----------------------- | -------------------------------------- |
| `income_quintile`       | Q1–Q5 by weighted household income        | `w5_hhincome`, `w5_wgt` | Primary grouping **and** match cell.   |
| `household_size`        | Number of residents                       | `w5_hhsizer`            | —                                      |
| `household_composition` | Adults / children / elderly counts        | NIDS member records     | Joined per household.                  |
| `dependency_ratio`      | (Children + elderly) / working-age adults | derived                 | From composition.                      |
| `age_head`              | Age of head                               | NIDS individual-derived | Joined to head of `w5_hhid`.           |
| `gender_head`           | Gender of head                            | NIDS individual-derived | —                                      |
| `race_head`             | Population group of head                  | NIDS individual-derived | Strong SA financial-behaviour predictor. |
| `education_head`        | Highest education of head (≈25 levels)    | NIDS individual-derived | Profiling only.                        |
| `education_band`        | Coarse education: None/Primary/Secondary/Matric/Tertiary | derived from `education_head` | Profiling; explicit level→band map. |

---

## Match keys & sampling fields (not agent attributes)

| Field          | Description                          | Source        | Use                                              |
| -------------- | ------------------------------------ | ------------- | ------------------------------------------------ |
| `income_quintile` | Income quintile (above)           | both surveys  | Primary match cell (computed in each survey).    |
| `province`     | Province                             | both surveys  | Optional secondary match cell where sizes allow. |
| `w5_wgt`       | Post-stratified household weight     | NIDS          | Probability weights for the 5,000 resample.      |
| `w5_hhid`      | Household identifier                 | NIDS          | Record key for joins; not carried into the ABM.  |

---

## Notes

- **2017 Rands throughout.** No CPI multiplier anywhere; FinScope flags are categorical.
- **Committed/discretionary** split is approximate — NIDS only gives food / non-food / rent.
- **Liquid savings** is the weakest field; proxied by financial assets, floored at 0.
- **FinScope question codes** are coded blocks (e.g. `B*`, `C*`); exact columns resolved against
  the FinScope 2019 questionnaire PDF during P0.
