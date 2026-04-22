# DataFirst Dataset Search: Consumer Agent Calibration

**Purpose:** Identify datasets to calibrate the consumer agent in the SA BNPL ABM.
**Consumer agent balance sheet:** Assets (Income, Savings) + Liabilities (Traditional Debt, BNPL Obligations)
**Key calibration targets:** Income distribution, expenditure patterns, debt levels, DSTI ratios, credit access rates.

---

## Priority 1: Critical Datasets

### 1. National Income Dynamics Study (NIDS) Wave 5, 2017

| Field          | Value                                                              |
| -------------- | ------------------------------------------------------------------ |
| **IDNO**       | `zaf-saldru-nids-2017-v1.0.0`                                      |
| **Producer**   | SALDRU, University of Cape Town                                    |
| **Years**      | 2017 (Wave 5 of 5; panel started 2008)                             |
| **Access**     | Public (free download)                                             |
| **Variables**  | 2,697                                                              |
| **Sample**     | 39,434 individuals, nationally representative                      |
| **Portal**     | <https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/712> |
| **Local JSON** | `data/raw/nids_wave5_info.json`, `nids_wave5_credit_vars.json`     |

**Why it matters:** NIDS is the gold standard for South African income dynamics. It is a longitudinal panel so it captures how income and debt evolve over time — exactly what an ABM needs for calibration. Wave 5 includes a dedicated "Personal Ownership and Debt" module.

**Key variables for the consumer agent:**

| Variable               | Description                     | ABM Use                       |
| ---------------------- | ------------------------------- | ----------------------------- |
| `w5_hhincome`          | Household income (monthly)      | Calibrate income distribution |
| `w5_hhincome_extu`     | Income upper bound (imputed)    | Handle top-coding             |
| `w5_hhwage`            | Wage income                     | Wage vs. grant income split   |
| `w5_pi_hhincome`       | Per-capita household income     | Per-agent income              |
| `w5_expenditure`       | Household expenditure           | Spending behaviour            |
| `w5_loan`              | Total outstanding loan amount   | Liability initialisation      |
| `w5_h_owndebt_brac1–5` | Debt bracket (1=low, 5=high)    | Debt tier segmentation        |
| `w5_h_owndebt_cat`     | Categorical debt classification | Agent type classification     |
| `w5_a_dtflloan`        | Formal institution loan (flag)  | Credit access rate            |
| `w5_a_dtfrloanbal`     | Friend/family loan balance      | Informal credit               |
| `w5_a_dtemploan`       | Employer loan (flag)            | Non-bank credit               |
| `w5_a_emhearn`         | Employment earnings             | Labour income                 |
| `w5_a_incloan`         | Income from loan receipts       | Cash flow                     |

**Waves available on DataFirst:**

- Wave 1: 2008 (`zaf-saldru-nids-2008-v7.0.0`)
- Wave 2: 2010–2011 (`zaf-saldru-nids-2010-2011-v4.0.0`)
- Wave 3: 2012 (`zaf-saldru-nids-2012-v3.0.0`)
- Wave 4: 2014–2015 (`zaf-saldru-nids-2014-2015-v2.0.0`)
- Wave 5: 2017 (`zaf-saldru-nids-2017-v1.0.0`) ← **use this**

> **Action:** Download Wave 5 public release from the portal. The full multi-file dataset includes adult, child, household, and derived income files.

---

### 2. Income and Expenditure Survey 2022–2023

| Field          | Value                                                               |
| -------------- | ------------------------------------------------------------------- |
| **IDNO**       | `zaf-statssa-ies-2022-2023-v1`                                      |
| **Producer**   | Statistics South Africa                                             |
| **Years**      | November 2022 – November 2023                                       |
| **Access**     | Public (CC-BY licence)                                              |
| **Variables**  | Not yet indexed in API (data files available on portal)             |
| **Sample**     | 31,042 dwelling units, national coverage                            |
| **Portal**     | <https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/1116> |
| **Local JSON** | `data/raw/ies_2022_info.json`                                       |

**Why it matters:** The IES is the most recent and detailed snapshot of what South African households earn and spend. It uses a diary + recall methodology to capture granular expenditure by COICOP category. This is the primary source for updating income and spending distributions to 2022/23 levels — more current than NIDS Wave 5 (2017). It is also used to rebase the CPI basket, making it authoritative for consumption patterns.

**Key calibration uses:**

- Income bracket distributions (cross-sectional, 2022 rand values)
- Share of income spent on housing, food, transport, debt repayments
- Poverty and inequality metrics (Gini, headcount ratios)
- Rebuilding a synthetic population with realistic income/expenditure profiles

> **Action:** Download from portal; variable metadata will need to be obtained from the accompanying codebook/COICOP classification document. The IES 2010–2011 (`zaf-statssa-ies-2010-2011-v1`) is a good fallback with full API variable indexing.

---

## Priority 2: Important Supporting Datasets

### 3. General Household Survey 2022

| Field          | Value                                                              |
| -------------- | ------------------------------------------------------------------ |
| **IDNO**       | `zaf-statssa-ghs-2022-v1`                                          |
| **Producer**   | Statistics South Africa                                            |
| **Years**      | May – December 2022                                                |
| **Access**     | Public (CC-BY)                                                     |
| **Variables**  | 305                                                                |
| **Portal**     | <https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/945> |
| **Local JSON** | `data/raw/ghs_2022_info.json`, `ghs_2022_credit_vars.json`         |

**Why it matters:** Annual cross-section. Useful for understanding income composition — specifically the salary vs. social grant split. Over 18 million South Africans receive social grants; this must be reflected in the consumer population.

**Key variables:**

| Variable        | Description                                                          |
| --------------- | -------------------------------------------------------------------- |
| `lab_salary_hh` | Household receives salary income (flag)                              |
| `lab_salary`    | Individual salary                                                    |
| `fin_inc_grant` | Household receives social grant                                      |
| `soc_grant_csg` | Child Support Grant                                                  |
| `soc_grant_oag` | Old Age Pension                                                      |
| `soc_grant_srd` | Social Relief of Distress grant                                      |
| `hwl_assets_*`  | Durable asset ownership (fridge, car, TV...) — proxy for wealth tier |

> GHS 2024 (`zaf-statssa-ghs-2024-v1`) is also available and is the most recent.

---

### 4. Quarterly Labour Force Survey 2022, Q2

| Field          | Value                                                              |
| -------------- | ------------------------------------------------------------------ |
| **IDNO**       | `zaf-statssa-qlfs-2022-q2-v1`                                      |
| **Producer**   | Statistics South Africa                                            |
| **Years**      | Q2 2022                                                            |
| **Access**     | Public                                                             |
| **Variables**  | 161                                                                |
| **Portal**     | <https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/909> |
| **Local JSON** | `data/raw/qlfs_2022_info.json`                                     |

**Why it matters:** The QLFS tracks employment status quarterly. For the ABM, it provides the fraction of agents who are employed vs. unemployed and the earnings distribution by employment type. SA's ~33% unemployment rate is a critical structural parameter that shapes income shock probabilities.

> QLFS 2025 Q1 (`zaf-statssa-qlfs-2025-q1-v1`) is the most recent available.

---

## Priority 3: Supplementary

### 5. All Media and Products Survey (AMPS) 2015

| Field          | Value                                                              |
| -------------- | ------------------------------------------------------------------ |
| **IDNO**       | `zaf-saarf-amps-2015-v1.1`                                         |
| **Producer**   | South African Audience Research Foundation (SAARF)                 |
| **Years**      | 2015 (final AMPS year; survey discontinued)                        |
| **Access**     | Public                                                             |
| **Variables**  | 8,079                                                              |
| **Portal**     | <https://www.datafirst.uct.ac.za/dataportal/index.php/catalog/754> |
| **Local JSON** | `data/raw/amps_2015_info.json`, `amps_2015_variables.json`         |

**Why it matters:** AMPS collects data on product and service ownership. The financial products module likely covers credit card ownership, store account usage, and banking product adoption by income tier — all directly relevant to modelling how consumers access credit. However, the variable names are coded and require the SAARF layout/codebook file to interpret.

> **Caveat:** Variable metadata labels are not populated in the DataFirst API. Download the dataset with layout files from the portal to identify credit-relevant variables.

---

## Data Gaps: Sources Outside DataFirst

These are not available via DataFirst but are essential for calibrating the credit market aggregate:

| Source | Data | URL |
| --- | --- | --- |
| **National Credit Regulator (NCR)** | Consumer Credit Market Report (quarterly) — total credit agreements by type, NPL rates, DSTI distribution, impaired records | <https://www.ncr.org.za/> |
| **South African Reserve Bank (SARB)** | Quarterly Bulletin — household debt-to-income ratio, total household credit outstanding, bank-level credit growth | <https://www.resbank.co.za/> |
| **FinMark Trust / FinScope** | FinScope Consumer Survey — financial inclusion, BNPL awareness, credit product adoption by income quintile | <https://finmark.org.za/> |

> BNPL-specific data does not exist in formal South African surveys yet (it is too recent). FinScope or the NCR's emerging credit data are the best proxies.

---

## Mapping to Consumer Agent Balance Sheet

| Agent Component                  | Calibration Dataset             | Key Variables                                          |
| -------------------------------- | ------------------------------- | ------------------------------------------------------ |
| **Income (wages)**               | NIDS W5, IES 2022/23, QLFS 2022 | `w5_hhincome`, `w5_hhwage`, IES income brackets        |
| **Income (grants)**              | GHS 2022                        | `soc_grant_*`, `fin_inc_grant`                         |
| **Savings**                      | NIDS W5                         | `w5_h_owndebt_cat`, asset variables                    |
| **Traditional Debt level**       | NIDS W5                         | `w5_loan`, `w5_h_owndebt_brac*`                        |
| **Credit access (formal)**       | NIDS W5, AMPS 2015              | `w5_a_dtflloan`, AMPS product ownership                |
| **Expenditure patterns**         | IES 2022/23, NIDS W5            | COICOP categories, `w5_expenditure`                    |
| **DSTI threshold calibration**   | NCR CCMR, NIDS W5               | Debt/income ratio from NCR aggregate data + NIDS micro |
| **Employment shock probability** | QLFS 2022                       | Unemployment rate, employment transitions              |
| **BNPL obligations**             | FinScope, NCR                   | No direct survey data; use NCR BNPL credit category    |

---

## Recommended Download Order

1. **NIDS Wave 5** — most complete micro-level income + debt data (public, free)
2. **IES 2022/23** — update income/expenditure distributions to current rands (public, free)
3. **GHS 2022** — supplement with grant income and asset-based wealth proxies (public, free)
4. **NCR Consumer Credit Market Report** (external, free download) — aggregate credit calibration
5. **AMPS 2015** — if modelling credit product adoption explicitly (public, free)
