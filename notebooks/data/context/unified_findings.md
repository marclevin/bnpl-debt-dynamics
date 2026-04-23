# Unified Findings: Consumer Agent Calibration

**Purpose:** Exact instructions for constructing and calibrating the consumer agent balance sheet using all identified data sources.
**Reference model:** work.md (ABM design) | question.md (archetypes) | dataset_search.md (sources) | output.md (NCR CCMR Q1 2025)

---

## 0. Simulation Phase Design

The ABM runs in two mandatory phases, with an optional third:

| Phase | Ticks | World state | Purpose |
|---|---|---|---|
| **Phase 1 — Pre-BNPL baseline** | t=0 → t=T_entry | Consumers + Banks only. No BNPL platform. | Calibrate and validate the model against known SA credit market aggregates. |
| **Phase 2 — BNPL entry** | t=T_entry → end | BNPL platform agent activates. Consumers can adopt. | Observe adoption S-curve, D_bnpl accumulation, DSTI divergence, NPL drift. |
| **Phase 3 — Regulatory shock** *(optional)* | t=T_shock | `bnpl_visible_to_banks = True` | Banks recalculate DSTI with full debt. Observe distress cascade. |

**T_entry** is the tick at which BNPL enters. This is a model parameter to experiment with (e.g. early vs. late entry).

### Critical initialisation rule

At t=0, **every agent has `D_bnpl = 0` and `holds_bnpl = False`** regardless of archetype. BNPL obligations are an *emergent output* of Phase 2, not a seeded input.

### What the 57% holdership figure means

`p_bnpl_current_holders = 57%` (gem_findings.md §5) is **not** an initialisation parameter. It is a **Phase 2 validation target**: by the tick representing present-day (~2024/25), approximately 57% of agents should have adopted BNPL organically through the `p_bnpl_first_adoption` draw. If they haven't, the adoption rate parameter is miscalibrated.

Similarly, the seasonal draw multipliers, average basket sizes, and default rates are Phase 2 emergent outputs to validate — not Phase 1 inputs.

### Why this matters for the thesis

The adoption curve itself becomes a model output, not an assumption. This makes the experimental design cleaner: Phase 1 proves calibration; Phase 2 produces the adoption and debt dynamics the thesis is studying; Phase 3 tests the regulatory counterfactual. Supervisor and examiners can evaluate each phase independently.

---

## 1. Consumer Agent Structure

The consumer agent holds a balance sheet with four live quantities updated each tick:

| Side       | Component             | Symbol      | Unit        |
|------------|-----------------------|-------------|-------------|
| Asset      | Monthly income        | `Y`         | R/month     |
| Asset      | Liquid savings        | `S`         | R           |
| Liability  | Traditional debt book | `D_trad`    | R           |
| Liability  | BNPL obligations      | `D_bnpl`    | R           |

Derived quantities used in agent logic:

```
DSTI  = (monthly_debt_repayment) / Y        # triggers distress if > 0.50
NTB   = Y - expenses - debt_repayment       # net-to-bank; < 0 triggers BNPL draw
LTI   = (D_trad + D_bnpl) / (Y × 12)       # loan-to-income
```

---

## 2. Income (`Y`)

### What to do

**Step 1 — Load NIDS Wave 5 individual file**
File: `zaf-saldru-nids-2017-v1.0.0`, adult questionnaire.
Extract variable `w5_pi_hhincome` (per-capita household income, monthly rand, 2017 values).
Fallback: `w5_hhincome / w5_hhsize` if per-capita not directly available.

**Step 2 — CPI-adjust to 2022/23 rands**
CPI index 2017 → 2022/23 ≈ ×1.37 (use Stats SA CPI headline series).
Multiply all income values by 1.37 before use.

**Step 3 — Validate against IES 2022/23 income brackets**
File: `zaf-statssa-ies-2022-2023-v1`. Cross-check the distribution shape matches IES decile shares.

**Step 4 — Validate against NCR income tiers**
The NCR reports three income brackets. After CPI-adjustment, confirm NIDS gives a plausible population split:

| NCR income tier | Expected approx. share of credit-active population |
|-----------------|-----------------------------------------------------|
| ≤R10K/month     | ~55%                                                |
| R10.1K–R15K/month | ~14%                                              |
| >R15K/month     | ~31%                                                |

Source: NCR CCMR 2025-Q1 Tables 4.3, 5.5, 6.5 (by number of agreements — best proxy for consumer count).

**Step 5 — Employment / grant income split**
File: `zaf-statssa-ghs-2022-v1`.
Variables: `fin_inc_grant`, `soc_grant_srd`, `soc_grant_oag`, `soc_grant_csg`.
Set `income_type` flag per agent: `WAGE` | `GRANT` | `MIXED`.

**Step 6 — Unemployment parameter**
File: `zaf-statssa-qlfs-2022-q2-v1`.
Set `p_unemployment = 0.33` as the initial share of agents with zero wage income (grant-only or informal).
Set quarterly income-shock probability from QLFS employment-transition matrix.

### Calibrated values (use these until micro-data is loaded)

| Agent archetype | Monthly income `Y` | Income type |
|---|---|---|
| Type A – Unscorable | R3,000–R7,000 | GRANT or informal wage |
| Type B – Stressed Middle | R10,000–R18,000 | Formal wage |
| Type C – Optimizer | R25,000–R60,000 | Formal wage |

---

## 3. Savings (`S`)

### What to do

**Step 1 — Proxy from NIDS W5 asset data**
Variables: `w5_h_owndebt_cat`, `hwl_assets_*` (durable assets as wealth proxy).
Savings is not directly measured in NIDS. Estimate as:
`S_init = Y × savings_ratio` where `savings_ratio` is derived from the IES 2022/23 residual (income minus expenditure).

**Step 2 — IES 2022/23 expenditure**
File: `zaf-statssa-ies-2022-2023-v1`.
Extract total household expenditure by income decile. Compute `expenditure_ratio = expenditure / income` per decile.
`savings_ratio = 1 - expenditure_ratio - debt_service_ratio`.

### Calibrated values (use as starting point)

| Archetype | Savings ratio | Initial `S` |
|---|---|---|
| Type A | 0% | R0–R500 |
| Type B | 3–5% | R1,000–R5,000 |
| Type C | 10–20% | R15,000–R50,000 |

---

## 4. Traditional Debt (`D_trad`)

This is the primary balance sheet component sourced from the NCR CCMR.

### 4.1 Aggregate calibration (market-level consistency check)

From NCR CCMR 2025-Q1 (output.md Tables 1.6, 1.8):

| Credit type       | Gross debtors book | # Accounts  | Avg balance/account |
|-------------------|--------------------|-------------|---------------------|
| Mortgages         | R1.265 trillion    | 1.65M       | ~R766K              |
| Secured (vehicles)| R534.5 billion     | 3.36M       | ~R159K              |
| Credit facilities | R347.7 billion     | 26.4M       | ~R13,200            |
| Unsecured loans   | R211.6 billion     | 4.33M       | ~R48,800            |
| Short-term credit | R2.9 billion       | 0.93M       | ~R3,100             |
| Developmental     | R63.5 billion      | 1.22M       | ~R51,900            |
| **Total**         | **R2.43 trillion** | **37.92M**  | **~R64,000**        |

SA adult population ≈ 40M → ~37.92M total credit accounts across all holders (individuals can hold multiple accounts). Use the type-level averages to initialise `D_trad` sub-components per agent.

### 4.2 Credit access by income tier

Use NCR CCMR Tables to gate which agent types hold which products:

**Mortgages (Table 2.3):** 99% held by income >R15K.
→ Only Type C agents hold mortgages in initial state.

**Secured/vehicle credit (Table 3.3):**
→ ≤R10K: 32% of agreements (number); R10.1K–R15K: 8%; >R15K: 60%.
→ Type A can hold small furniture/retail accounts; Type B/C hold vehicle finance.

**Credit facilities — store cards, bank cards (Table 4.3):**
→ ≤R10K: 65% of agreements (number) — primarily store cards, not bank credit cards.
→ All three types hold credit facilities; composition differs (store cards for A, bank cards for C).

**Unsecured personal loans (Table 5.5):**
→ ≤R10K: 27% (number), R10.1K–R15K: 13%, >R15K: 60%.
→ All types access unsecured credit but at different rates and amounts.

**Short-term/payday credit (Table 6.5):**
→ ≤R10K: 54% (number) — this is the credit type BNPL most resembles.
→ Dominant for Type A. Type B uses occasionally.

### 4.3 Initial D_trad by archetype

| Archetype | Likely products held | D_trad initialisation |
|---|---|---|
| Type A | Store card + short-term loan | R3K–R15K |
| Type B | Vehicle + unsecured loan + credit facility | R80K–R200K |
| Type C | Mortgage + vehicle + credit card | R700K–R1.5M |

**Action:** Draw initial `D_trad` from a distribution fitted to NIDS W5 `w5_loan` (outstanding loan amount), segmented by `w5_h_owndebt_brac1–5`, CPI-adjusted to 2022/23.

### 4.4 DSTI initialisation

NCR/question.md calibration target: DSTI 30–50%.
Set monthly debt repayment as:
`monthly_repayment = D_trad × r / (1 - (1+r)^(-n))`
where `r` = monthly interest rate, `n` = remaining term months.

Use NIDS W5 variable `w5_a_dtflloan` (flag: holds formal loan) to set credit-access indicator per agent.

---

## 5. Default / NPL Parameters

Source: NCR CCMR Figures 2.1, 3.1, 4.1, 5.1, 6.1, 7.1 (% book reported "current", 2025-Q1).

| Credit type       | % Current (rand) | Implied NPL rate | Use in ABM as |
|-------------------|------------------|------------------|---------------|
| Mortgages         | 86.95%           | **13.1%**        | `p_default_mortgage` |
| Secured credit    | 86.74%           | **13.3%**        | `p_default_secured` |
| Credit facilities | 78.39%           | **21.6%**        | `p_default_facility` |
| Unsecured loans   | 69.41%           | **30.6%**        | `p_default_unsecured` |
| Short-term credit | 65.35%           | **34.7%**        | `p_default_shortterm` |
| Developmental     | 85.53%           | **14.5%**        | `p_default_developmental` |

These are stock NPL rates. Convert to flow default probabilities by dividing by average loan duration (months).

**Trend note:** Unsecured NPL has drifted from 28.3% (2022-Q1) to 30.6% (2025-Q1) — a structural worsening trend. In the simulation, consider a slow drift upward in `p_default_unsecured` to reflect this.

---

## 6. Credit Application Approval Rate

Source: NCR CCMR Table 1.4.

- Overall rejection rate 2025-Q1: **66.18%** → approval rate: **33.82%**
- Quarterly applications received: 18.08M; agreements entered: 5.06M.

**Action:** Set `p_credit_approved` as a function of agent income tier and DSTI:

| Condition | Approval rate |
|---|---|
| DSTI < 30% + income >R15K | 60–70% |
| DSTI 30–50% + income R10–R15K | 25–35% |
| DSTI > 50% OR income ≤R10K | 5–15% |
| No credit history (Type A, new) | 0% for bank, BNPL only |

The NCR data shows ~34% average approval but it is heavily skewed toward higher-income applicants. The overall rate is dragged down by the high volume of low-income, high-DSTI applications.

---

## 7. BNPL Obligations (`D_bnpl`)

### The structural gap

**BNPL is not captured in the NCA.** Platforms (Payflex, PayJustNow, Float, HappyPay) operate outside NCA scope via the zero-interest loophole (NCA Section 8(3) requires interest charges for a transaction to qualify as credit). Their obligations are **invisible to the NCR and to traditional banks** — this is the core mechanism the ABM is designed to model.

NCA proxy comparison (nearest regulated equivalents):
- Short-term credit book: R2.9B (Q1 2025), 933K accounts, avg R3,100
- Retailer gross debtors book: R60.1B (Q1 2025), dominated by store cards

BNPL differs from store cards in that it is: (1) zero interest if repaid on time, (2) not reported to credit bureaus, (3) short repayment window (6 weeks), (4) fees framed as penalties not interest.

### Market calibration (direct data — no longer a proxy)

Source: SA BNPL market report (2024–2026 synthesis); see gem_findings.md.

| Year | SA BNPL market | Implied monthly volume |
|---|---|---|
| 2024 | ~USD 717M (~R13B) | ~R1.1B/month |
| 2025 | USD 815M (~R15B) | ~R1.25B/month |
| **2026 (target)** | **~R25B annual** | **~R2.1B/month** |
| 2031 | USD 2.85B (~R52B) | — |

Growth CAGR 2025→2031: **20.8%**. Apply this as the market scaling function in the simulation.

### `D_bnpl` calibration parameters

> **Phase note:** All D_bnpl parameters below are Phase 2 parameters only. At t=0 (Phase 1), every agent has `D_bnpl = 0` and `holds_bnpl = False`. See §0.

| Parameter | Value | Source | Phase |
|---|---|---|---|
| `p_bnpl_current_holders` | **57%** | Validation target: share of agents who should hold BNPL by present-day tick | Phase 2 *output* |
| `p_bnpl_first_adoption_annual` | **10%** | Share of non-holders who adopt in a given year (~0.83%/month) | Phase 2 *input* |
| `E_transaction_value` (Type A/B) | **R1,629** | Average basket, standard consumer | Phase 2 *input* |
| `E_transaction_value` (Type C) | **R2,949** | Average basket, high-affluence cohort | Phase 2 *input* |
| `repayment_instalments` | **3–4** | Equal payments | Phase 2 *input* |
| `repayment_window_weeks` | **6** | Total repayment period | Phase 2 *input* |
| `upfront_deposit_rate` | **25–33%** | Paid at point of purchase (standard model) | Phase 2 *input* |
| `p_default_bnpl_stock` | **4–6%** | Current SA estimated delinquency | Phase 2 validation target |
| `p_default_bnpl_trajectory` | **6–8%** | Near-term direction (TransUnion 2025) | Phase 2 validation target |
| `late_fee_weekly` | **R85–R125** | Per missed payment | Phase 2 *input* |
| `late_fee_cap_pct` | **25% of GMV** | Maximum fee exposure (~R255–R375 on avg basket) | Phase 2 *input* |

### `D_bnpl` agent logic (tick-level rules)

```python
# Each tick (month), for each agent:

# 1. Adoption trigger
if agent.holds_bnpl == False:
    if random() < p_bnpl_first_adoption_monthly:
        agent.holds_bnpl = True

# 2. Draw trigger (BNPL used when cash-negative)
if agent.NTB < 0 and agent.holds_bnpl:
    transaction = sample(E_transaction_value)
    upfront = transaction * upfront_deposit_rate    # paid immediately
    agent.D_bnpl += transaction * (1 - upfront_deposit_rate)
    agent.S -= upfront  # savings reduced by deposit

# 3. Repayment (each of 3 instalments due every 2 weeks = ~1.5 per month)
instalment = agent.D_bnpl_current_plan / 3
if agent.can_pay(instalment):
    agent.D_bnpl -= instalment
else:
    agent.D_bnpl += late_fee  # R85–R125, capped at 25% of plan value
    # D_bnpl accumulates; DSTI_total rises

# 4. Bank blindness (pre-regulation)
# Bank sees only D_trad when evaluating new credit
DSTI_bank_view = D_trad_repayment / Y          # what bank sees
DSTI_true      = (D_trad_repayment + D_bnpl_repayment) / Y  # reality
```

### Type C BNPL variant (Float model)
Type C agents use the card-linked model: no upfront deposit, up to 24-month repayment, basket sizes 2–10× larger (R2,949 average). Implement as a separate plan type with `upfront = 0`, `n_instalments = 12–24`, `p_default_bnpl = 1–2%` (lower risk profile).

### Regulatory shock scenario (tick 36)

At tick 36, activate `bnpl_visible_to_banks = True`:
- Banks now include `D_bnpl` in DSTI calculation
- Consumers above DSTI 50% threshold face immediate bank credit refusal
- Expected cascade: Type B agents with accumulated `D_bnpl` breach 50% → distress → potential systemic default

This is the primary experiment in question.md: "Introduce a BNPL Shock into a stable credit environment."

### Seasonal draw multipliers (apply to `p_bnpl_draw`)

| Month | Multiplier | Driver |
|---|---|---|
| November (Black Friday) | ×1.6 | Volume surge (+60%) |
| December | ×1.4 | Festive discretionary |
| January–February | ×1.1 (volume), ×0.7 (value) | Janu-worry: high frequency, low basket |
| February–March | ×1.0 + bonus repayment rule | Bonus pays D_trad; BNPL used for new spend |
| June–August | ×1.2 | Winter clothing/appliances |

---

## 8. Consumer Agent Archetypes — Full Initialisation

### Type A — The Unscorable Entry-Level

| Parameter | Value | Source |
|---|---|---|
| `Y` | R3,000–R7,000/month | NIDS W5 lower quintiles |
| `income_type` | GRANT or informal | GHS 2022 |
| `S` | R0–R500 | IES residual |
| `D_trad` | R0 (no credit history) | NIDS `w5_a_dtflloan = 0` |
| `DSTI_trad` | 0% | Implied |
| `p_credit_approved_bank` | 0–5% | NCR rejection data |
| `p_default_unsecured` | 34–35% | NCR short-term NPL |
| Credit products (traditional) | None at t=0 | By design |
| `holds_bnpl` | **False at t=0** — adopts early in Phase 2 (first gateway) | gem_findings.md §2; see §0 |
| `p_bnpl_draw` | High once active — triggered by NTB < 0 most months | Low Y, low S |
| `E_transaction_value_bnpl` | R800–R1,629 | Essential categories (groceries, clothing) |
| `p_default_bnpl` | 6–8% (highest risk tier) | TransUnion trajectory |
| BNPL model | Standard 3-party (Payflex/PayJustNow) | Dominant SA model |
| BNPL rationale | Only credit available; expected to be among first adopters in Phase 2 | gem_findings.md §2 |

### Type B — The Stressed Middle Class

| Parameter | Value | Source |
|---|---|---|
| `Y` | R10,000–R18,000/month | NIDS W5 middle deciles, CPI-adj |
| `income_type` | WAGE (formal) | GHS 2022 |
| `S` | R1,000–R5,000 | IES residual ~3–5% savings |
| `D_trad` | R80,000–R200,000 | NCR unsecured + vehicle avg |
| `DSTI_trad` | 35–45% | NCR/question.md target |
| `p_credit_approved_bank` | 25–35% | NCR rejection data |
| `p_default_unsecured` | 30–31% | NCR unsecured NPL |
| Credit products (traditional) | Unsecured, credit facility, vehicle | NCR Table 5.5 |
| `holds_bnpl` | **False at t=0** — adopts during Phase 2; core adopter demographic | gem_findings.md §5; see §0 |
| `p_bnpl_draw` | Moderate once active — triggered at month-end (Janu-worry) | NTB < 0 seasonally |
| `E_transaction_value_bnpl` | R1,629 | National average basket |
| `p_default_bnpl` | 4–6% (mid-tier, rising) | gem_findings.md §4 |
| BNPL model | Standard 3-party | Dominant SA model |
| BNPL rationale | Month-end bridge; bonus season debt clearance | gem_findings.md §2 |
| **Key risk** | Multi-BNPL plan accumulation invisible to bank | DSTI_true > DSTI_bank_view |

### Type C — The Strategic Optimizer

| Parameter | Value | Source |
|---|---|---|
| `Y` | R25,000–R60,000/month | NIDS W5 upper quintile, CPI-adj |
| `income_type` | WAGE (formal, senior) | GHS 2022 |
| `S` | R15,000–R50,000 | IES residual ~15–20% savings |
| `D_trad` | R700,000–R1,500,000 | NCR mortgage avg ~R766K + vehicle |
| `DSTI_trad` | 20–30% | Comfortable range |
| `p_credit_approved_bank` | 60–70% | NCR implied high-income approval |
| `p_default_unsecured` | 13–14% | NCR mortgage/secured NPL |
| Credit products (traditional) | All types | NCR Tables 2.3, 3.3 |
| `holds_bnpl` | **False at t=0** — adopts during Phase 2 for strategic reasons | gem_findings.md §5; see §0 |
| `p_bnpl_draw` | Low once active — driven by strategy not necessity | NTB > 0; S buffer exists |
| `E_transaction_value_bnpl` | **R2,949** | Premier Existence avg basket |
| `p_default_bnpl` | 1–2% (lowest risk tier) | gem_findings.md §4 |
| BNPL model | **Float (card-linked)** — 0% upfront, up to 24 months | gem_findings.md §3 |
| BNPL rationale | 0% interest arbitrage; keeps cash in savings | gem_findings.md §2 |

---

## 9. Population Mix

Based on NCR income-tier shares across credit products and GHS 2022/QLFS data:

| Archetype | Share of simulated population | Rationale |
|---|---|---|
| Type A | 40% | ≤R10K income share; high unbanked/underbanked |
| Type B | 35% | R10K–R20K income; core stressed consumer |
| Type C | 25% | >R20K income; credit-active, mortgage-holding |

Adjust if NIDS W5 income distribution suggests different proportions after CPI-adjustment.

---

## 10. Outstanding Data Gaps

| Gap | Status | Impact | Action |
| --- | --- | --- | --- |
| **BNPL market data** | **FILLED** — gem_findings.md | `p_bnpl_draw`, `E_transaction_value`, `p_default_bnpl`, fee structure | Use gem_findings.md §5 parameters directly |
| **BNPL regulatory mechanics** | **FILLED** — gem_findings.md | Regulatory shock scenario calibrated | Use gem_findings.md §7 for tick-36 shock |
| **FinScope Consumer Survey** | Partially filled by BNPL report; micro-level adoption by income tier still missing | Fine-grained `p_bnpl_first_adoption` by archetype | Obtain from FinMark Trust for income-tier breakdown |
| **Eighty20 2025 Credit Stress Report** | **NOT YET OBTAINED** | DSTI distribution by income tier; share of consumers at >50% DSTI | Request from Eighty20 or check UCT Libraries subscription |
| **NIDS W6 / post-2017 debt micro-data** | Not available | Debt levels are 2017, CPI-adjusted estimates are rough | Use NIDS W5 as structural baseline; adjust to match NCR aggregate totals |
| **DSTI distribution** | Partially addressed | NCR reports aggregate NPL but not individual DSTI distributions | Use NCR NPL + NIDS micro to impute; Eighty20 report will resolve this |
| **TransUnion SA Consumer Pulse 2025** | Not yet obtained | Validates the "BNPL delinquency nearly doubled" claim | Obtain directly to verify gem_findings.md §4 delinquency figures |
| **Savings rate by income tier** | Not yet obtained | IES 2022/23 codebook needed to extract COICOP expenditure by decile | Download IES codebook from DataFirst portal |

---

## 11. Download & Extraction Checklist

Work through this list in order:

- [ ] **NIDS W5** — Download from DataFirst (`zaf-saldru-nids-2017-v1.0.0`). Extract: `w5_pi_hhincome`, `w5_loan`, `w5_a_dtflloan`, `w5_h_owndebt_brac*`, `w5_expenditure`. Apply CPI × 1.37.
- [ ] **IES 2022/23** — Download from DataFirst (`zaf-statssa-ies-2022-2023-v1`). Download codebook. Extract expenditure by COICOP category per income decile to get `expenditure_ratio`.
- [ ] **GHS 2022** — Download from DataFirst (`zaf-statssa-ghs-2022-v1`). Extract: `fin_inc_grant`, `soc_grant_*`, `lab_salary_hh`. Set `income_type` distribution.
- [ ] **QLFS 2022 Q2** — Download from DataFirst (`zaf-statssa-qlfs-2022-q2-v1`). Extract unemployment rate and employment-transition matrix for income-shock probability.
- [x] **NCR CCMR** — Obtained (output.md). NPL rates and income-tier tables extracted above.
- [x] **BNPL market report** — Obtained. Key parameters extracted into gem_findings.md. Use §5 directly.
- [ ] **FinScope** — Contact FinMark Trust for micro-level adoption by income tier (broad parameters now covered by BNPL report). Can't do this.
- [ ] **Eighty20 2025 Credit Stress Report** — Request from Eighty20 or check UCT Libraries. Needed for DSTI distribution.
- [ ] **TransUnion SA Consumer Pulse 2025** — Obtain to verify BNPL delinquency doubling claim.
- [ ] **SARB Quarterly Bulletin** — Extract household debt-to-income ratio (aggregate cross-check).

---

## 12. Calibration Validation Targets

Validation is phase-specific. Phase 1 targets must be met *before* BNPL is introduced. Phase 2 targets are emergent outputs to check after BNPL entry.

### Phase 1 targets (pre-BNPL baseline — must pass before running Phase 2)

| Metric | Target value | Source |
| --- | --- | --- |
| Overall credit rejection rate | ~66% | NCR CCMR 2025-Q1 Table 1.4 |
| Unsecured NPL rate | ~30–31% | NCR CCMR Figure 5.1 |
| Short-term NPL rate | ~34–35% | NCR CCMR Figure 6.1 |
| Mortgage NPL rate | ~13% | NCR CCMR Figure 2.1 |
| Total gross debtors book (scaled) | R2.43T at market level | NCR CCMR Table 1.6 |
| Credit facilities share of accounts | ~70% of all accounts | NCR CCMR Table 1.8 |
| DSTI at distress trigger (>50%) | ~15–20% of indebted consumers | NCR/Eighty20 estimate |
| Share receiving social grants | ~45% of Type A agents | GHS 2022 |

### Phase 2 targets (post-BNPL entry — emergent outputs to validate)

| Metric | Target value | Source |
| --- | --- | --- |
| BNPL holders by present-day tick (~2024/25) | ~57% of simulated population | gem_findings.md §5 |
| BNPL market size at tick representing 2026 | ~R25B annualised | gem_findings.md §1 |
| BNPL default rate (stock, pre-shock) | 4–6% | gem_findings.md §4 |
| BNPL default rate (post-shock trend) | 6–8% | TransUnion 2025 via gem_findings.md |
| Avg BNPL basket (Type A/B) | ~R1,629 | gem_findings.md §5 |
| Avg BNPL basket (Type C) | ~R2,949 | gem_findings.md §5 |
| DSTI_true vs DSTI_bank_view gap | DSTI_true > DSTI_bank_view for Type B | Core thesis mechanism |
