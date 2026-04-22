# BNPL Gem Findings: SA Market Analysis

**Source document:** "The Structural Transformation of South African Retail Credit: A Longitudinal Analysis of Buy Now Pay Later (BNPL) Adoption and Consumer Behavior" (synthesised analyst report, 2024–2026 data).
**Purpose:** Extract actionable calibration data and modeling mechanics for the BNPL component of the SA consumer ABM.

---

## 1. Market Size & Trajectory

| Metric | 2021–2024 | 2025 (current) | 2026 (projected) | 2031 (forecast) |
|---|---|---|---|---|
| Market size (USD million) | ~$717M | **$815.1M** | $1,110M | $2,850M |
| Annual growth rate | 23.5% CAGR | 13.6% | 25.2% | 20.8% CAGR |
| African market (USD billion) | — | $5.2B | $6.5B | $16.8B |
| BNPL users in SA | — | — | — | ~6 million |
| SA retail spend via BNPL | — | — | **~R25 billion** | — |

**Simulation scaling anchor:** Target R25B total BNPL market by 2026 (~tick 12–18 in a monthly simulation starting 2024).

CAGR formula used in report:
$$CAGR = \left( \frac{V_{final}}{V_{initial}} \right)^{\frac{1}{t}} - 1$$

At 20.8% CAGR from $815.1M (2025), the 2031 value of $2.85B implies the market roughly triples in 6 years.

---

## 2. Consumer Psychographics — Archetype Mapping

The report identifies distinct BNPL user segments that map directly to ABM archetypes:

### Credit-Invisible Entry-Level (→ Type A)
- No formal credit history; BNPL is their **first credit gateway**
- No hard credit check on initial signup (key draw)
- Typical purchase: professional clothing, electronics entering workforce
- Thin credit file → formal banking rejection → BNPL as sole option

### Stressed Middle-Class (→ Type B)
- Millennials, ~70% female
- "Janu-worry" and month-end liquidity bridging
- Frequent usage, multi-loan holder across platforms
- Uses BNPL to bridge essential spending gaps, not discretionary
- Annual bonus behaviour: pays down high-interest debt first, uses BNPL for new purchases simultaneously

### Strategic Optimizer (→ Type C)
- "Premier Existence" / high-income cohort (FAS 1–3)
- Average basket size **R2,949** (vs R1,629 national average)
- Keeps cash liquid; uses BNPL for 0% interest arbitrage
- Highest adoption of digital wallets: Google Pay (53%), Apple Pay (40%), Samsung Pay (39%)
- Lowest default rates

### Demographic summary

| Segment | Gender skew | Repayment behaviour | Primary rationale |
|---|---|---|---|
| Gen Z (18–24) | Balanced | High sensitivity to late fees | Accessing "unlocked" assets |
| Millennials (25–40) | 70% Female | Frequent usage, multi-loan | Managing family liquidity |
| High Earners (FAS 1–3) | 65% Female | Lowest default rates | Strategic cash flow control |
| Low Earners (FAS 7–10) | 80% Female | Highest repayment pressure | Bridging essential gaps |

**Key figure:** 73% of all SA BNPL users identify as female. Women drove 69% of Black Friday 2025 transactions (PayJustNow data).

---

## 3. BNPL Transaction Mechanics

These are the rules governing how a BNPL transaction works — use directly in agent logic.

### Standard three-party model (Payflex, PayJustNow)
- Consumer pays **25–33% upfront** at time of purchase
- Remaining balance split into **3 or 4 equal instalments over 6 weeks**
- Provider pays merchant **100% upfront**, charges merchant **MDR of 3–6%**
- Zero interest to consumer if on time

### Card-linked model (Float)
- No upfront deposit; full amount reserved on existing credit card
- Repayment up to **24 months**, much higher basket sizes
- Pre-approved pool: **7 million credit cards** in SA
- AOV increase: **134%** vs regular purchases; up to **10×** vs standard BNPL

### Ad-subsidised model (HappyPay)
- Zero interest AND zero late fees (cost borne by advertisers)
- 600K users; raised $5M to scale

### Which model to use in ABM
Use the **standard three-party model** as the default. It is the dominant form in SA (Payflex + PayJustNow have largest user bases). Implement Float as a Type C variant for high-basket transactions.

| Feature | Payflex | PayJustNow | Float | HappyPay |
|---|---|---|---|---|
| Upfront deposit | 25–33% | 33% | 0% | 0% |
| Instalments | 3 or 4 | 3 or 4 | Up to 24 | 2 |
| Credit check | Automated assessment | None (initial) | None | Soft affordability |
| Late fee | R85–R125 | Reprocessing fee | None | R100 |
| Max basket | Spend limit | Spend limit | Card limit | R25,000 |

---

## 4. Default Rates & Fee Mechanics

### BNPL-specific default rates

| Benchmark | Rate | Source |
|---|---|---|
| Global BNPL default (baseline) | 2–3% | Industry norm |
| SA BNPL estimated (current) | **4–6%** | Analyst estimate 2025 |
| SA BNPL (near-term trajectory) | **6–8%** | TransUnion 2025 trend |
| P(late fee assessed, global) | **4.1%** | Final modeling parameters |
| TransUnion finding | Consumers unable to meet BNPL obligations **nearly doubled** 2024→2025 | TransUnion |

### Comparison to traditional SA credit delinquency (Q4 2025)

| Credit product | Delinquency rate | YoY change (bps) |
|---|---|---|
| Credit card | 12.9% | +33 |
| Clothing accounts | 24.5% | -213 |
| Retail installment | 26.8% | -110 |
| Bank personal loan | 27.0% | -271 |
| Non-bank personal loan | **48.0%** | +50 |
| **BNPL (estimated)** | **4–6%** | **+200** |

BNPL delinquency is currently low relative to other SA credit products — attributed to: (1) upfront deposit filter, (2) short repayment window (6 weeks) limiting exposure, (3) small transaction sizes. However, it is rising fastest (+200bps YoY).

### Late fee structure (for ABM penalty logic)

| Event | Fee |
|---|---|
| Missed payment (Payflex, day 1) | R85–R95 |
| Missed payment (day 7) | Additional fee |
| Missed payment (day 14) | Additional fee |
| Total fee cap | **25% of transaction value** |
| Equivalent ceiling | R255–R375 on a R1,629 avg basket |

Important: fees are **not classified as interest** → BNPL avoids NCA interest rate caps.

---

## 5. Key Modeling Parameters (Direct Use in ABM)

From the report's "Final Modeling Data Points" section — the most citable quantitative inputs:

| Parameter | Value | Notes |
|---|---|---|
| `p_bnpl_first_adoption` | **10% per year** | Share of non-users who try BNPL for first time |
| `p_bnpl_current_holders` | **57%** | Share of shoppers already holding a BNPL product |
| `E_transaction_value_standard` | **R1,629** | Average basket, standard consumer |
| `E_transaction_value_premium` | **R2,949** | Average basket, high-affluence (Type C) |
| `p_default_bnpl_stock` | **4.1–6%** | Current SA range |
| `p_default_bnpl_trajectory` | **6–8%** | Near-term direction (TransUnion) |
| `conversion_lift` | **25–30%** | Retailer checkout conversion uplift |
| `repayment_instalments` | **3–4** | Number of equal payments |
| `repayment_window_weeks` | **6** | Total repayment period |
| `upfront_deposit_rate` | **25–33%** | Proportion paid at purchase |
| `late_fee_weekly` | **R85–R125** | Per missed payment |
| `late_fee_cap_pct` | **25% of GMV** | Maximum fee exposure |
| `merchant_discount_rate` | **3–6%** | Provider revenue from merchants |

---

## 6. Seasonal / Temporal Patterns

Critical for tick-level behaviour in the simulation:

| Period | BNPL behaviour | Mechanism |
|---|---|---|
| **Black Friday (Nov)** | Volume surge **+60%**, stable basket ~R1,629 | Intentional budget-based purchasing |
| **Festive season (Dec)** | Peak total spend | Discretionary indulgence |
| **Janu-worry (Jan–Feb)** | High volume, **lower rand value** | Essential spending, cash stretching |
| **Bonus season (Feb–Mar)** | BNPL maintained while bonus used to clear high-interest debt | Debt prioritisation heuristic |
| **Winter (Jun–Aug)** | Secondary spending surge | Seasonal clothing + heating |

**Simulation rule:** In monthly ticks, apply a seasonal multiplier to `p_bnpl_draw` and `E_transaction_value`. At minimum, model the Janu-worry dip and Black Friday peak.

---

## 7. Regulatory Status & Shock Scenario

### Current legal position (2025)
- BNPL operates **outside the NCA** via the "zero-interest loophole" (NCA Section 8(3) requires interest/fees to be charged for a transaction to qualify as credit)
- No affordability assessment required
- No credit bureau reporting obligation
- Consumers accumulate BNPL across multiple platforms with **zero lender visibility**

### Incoming regulation (2026–2027 estimated)
Drawing on Australian model (effective June 2025):
- NCA Section 8 expansion to capture zero-cost deferred payment
- Mandatory NCR registration for BNPL providers
- Credit bureau integration (BNPL obligations become visible to banks)
- Standardised affordability assessment

**FINASA BNPL working group** currently drafting industry position paper for NCR engagement.

### Simulation shock: Regulatory transparency event
At a specified tick (e.g., tick 36), activate a **regulatory shock**:
- Set `bnpl_visible_to_banks = True`
- Banks recalculate consumer DSTI to include `D_bnpl`
- New credit applications recalculated with `DSTI_total = (D_trad_repayment + D_bnpl_repayment) / Y`
- Expected effect: Type B agents with high `D_bnpl` suddenly breach the 50% DSTI threshold → bank credit refusal → distress cascade

---

## 8. Product Category Mix (for transaction-type distribution)

| Category | Usage share | Avg basket (ZAR) | Growth potential |
|---|---|---|---|
| Fashion & apparel | 50%+ | R1,300–R1,700 | Mature |
| Marketplaces (Takealot/Makro) | 25% | R1,800–R2,200 | High |
| Electronics & tech | 15% | R2,500–R5,000 | Emerging |
| Travel & leisure | 5% | R4,000–R8,000 | High |
| Groceries | <5% | R800–R1,500 | Exploding |

Relevant for ABM: the shift toward **essential spending categories** (groceries, utilities) confirms that Type A and B agents are increasingly using BNPL for needs, not wants — which increases the systemic risk of non-repayment.

---

## 9. Key Insight: The Invisibility Problem

The central thesis alignment:

> "Because many BNPL providers operate outside the formal National Credit Act (NCA) framework, the visibility of a consumer's total debt is fragmented. This lack of shared data creates a potential for systemic over-indebtedness."

Banks cannot see `D_bnpl`. When approving new traditional credit, they compute DSTI using only `D_trad`. The consumer's true DSTI is higher. This is exactly the mechanism the ABM is designed to model.

Supporting data point: Traditional retail installments saw a **19.4% YoY decrease in Q4 2025** even as BNPL climbed — suggesting consumers are **substituting** traditional instalment credit with BNPL, not adding to it. This makes `D_bnpl` partially offset against `D_trad`, but the offset is invisible to the bank.

---

## 10. Source Caveats

The source document is a **secondary synthesis** (analyst report), not primary research. Specific figures to verify before citing in the thesis:
- USD market size figures → cross-check with Statista/GlobalData BNPL reports
- TransUnion "nearly doubled" delinquency claim → obtain TransUnion SA Consumer Pulse 2025 directly
- PayJustNow 1.3M customers → verify from PayJustNow press releases or NCR submissions
- Float "7M pre-approved cards" → verify from Float investor/press materials
- Delinquency rate table (clothing 24.5%, retail 26.8%) → cross-check with NCR CCMR retailer NPL data (available in output.md retailer book)
