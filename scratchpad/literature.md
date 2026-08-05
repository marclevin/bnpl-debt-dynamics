# Literature Plan — closing `decision_rules.md` by writing the Lit Review

**Purpose.** `decision_rules.md` says every behavioural rule needs a citation before it is coded.
So the literature review and the ABM specification are the *same task*. This file is the hunting
list: what to read, and which open decision each reading closes.

Seeded entries live in [`../thesis/main.bib`](../thesis/main.bib). Status legend:
`[HAVE]` in bib · `[FIND]` still to source.

---

## Tier 1 — the three core anchors (work.md demands one each)

| Anchor | Candidate | Closes |
| ------ | --------- | ------ |
| **ABM** | `cardaci2018inequality` — credit-network ABM, heterogeneous households + banks, inequality → debt → instability `[HAVE]` | D0 tick order, D2 consumption, D15 macro |
| **ABM** | `yun2020housing` — JASSS, explicit **LTV / DTI** lending gate in an ABM `[HAVE]` | D9 credit gate, D7 distress threshold |
| **BNPL** | `cfpb2025bnpl` — 145m applications 2017–22; **63% of BNPL borrowers held simultaneous loans, 32% across different firms**; ~20% originated >1 loan/month `[HAVE]` | **D12 stacking** (this is the headline number for RQ1) |
| **BEHAV** | `meier2010present` — present bias predicts credit-card borrowing `[HAVE]` | D3 borrow trigger, D8 heterogeneity |

These four alone are enough to start writing §Literature Review and §ABM Design.

---

## Tier 2 — one decision each

- **D6 repayment / minimum-payment bias** — `keys2019minimum` (anchoring at the minimum, ~29% of
  accounts) + `kuchler2021sticking` (present bias in paydown). `[HAVE]`
- **D3/D11 BNPL user profile** — `toh2025bnplconstraints`: 96% of late-paying BNPL users are at
  least mildly financially constrained vs 86% of non-late users. `[HAVE]` Directly justifies making
  the borrow trigger constraint-driven and heterogeneous by quintile.
- **D10 information asymmetry** — `nortonrose_bnpl_sa`: BNPL sits outside the NCA, so no mandatory
  affordability assessment and **no bureau reporting**. `[HAVE]` This is the citation that makes the
  bank-can't-see-BNPL mechanism a documented fact rather than a modelling convenience.
- **D14 interventions** — `[FIND]` UK FCA Woolard Review; Australia ASIC BNPL reviews; EU CCD2.
  Cool-off periods, stacking caps, mandatory affordability checks — need the actual instrument text.

## Closed since this file was written (2026-08-05)

- **D9 affordability formula — SETTLED.** NCA Reg 23A(9) residual-income test, not a DSTI cap.
  `[HAVE: sa_ncr_affordability_2015]`
- **Servicing APRs — SOURCED.** NCA statutory maximum prescribed rates by sub-sector at the 2017
  repo rate. `[HAVE: sa_ncr_ratecaps_2016]`
- **Correction:** the NCR CCMR **does not publish interest rates** — it reports credit granted,
  gross debtors book, and age analysis only. It remains the right source for the *arrears*
  validation target, but not for APRs.

## Consumer-credit ABM sweep (2026-08-05) — gap now filled

The Tier 1 list was weak here: Cardaci is macro-SFC, Yun & Moon is housing. Three proper
consumer-credit ABMs found, all now in the bib:

- **`madeira2018chile`** — *J. Financial Stability* 39:209-220. **The single best precedent.**
  Central Bank of Chile; middle-income economy; households default when they cannot finance
  **minimum consumption** (= the D7 definition this thesis wants); and it is **validated against
  observed default rates**. Proof that a household credit ABM in an emerging market can be held to
  external behavioural targets, which is exactly the hedge in [[behavioural-validation-hedge]].
- **`dorazio2017micro`** — JASSS 20(1):9. Households form employment beliefs, set consumption,
  approach the bank when consumption outruns income; bank rations proportionally. Closes D2, D3.
- **`hamill2023creditcard`** — UK credit-card market ABM. Lender promotional strategy raises
  borrower indebtedness; reproduces the non-monotonic income vs debt-to-income relationship
  (middle-income households carry the highest balance-to-income). Useful for D9/lender conduct.

## BNPL evidence upgrade (2026-08-05)

- **`dehaan2024bnpl`** — *Management Science* 70(8):5586-5598. **Now the lead BNPL citation**,
  displacing the CFPB report as the causal anchor. Banking records for **10.6m US consumers**,
  2015-2021. BNPL adoption raises overdraft charges 4.0%, credit-card interest 1.1%, late fees 2.3%;
  IV estimates 8.9% / 2.5% / 8.4%. Effects concentrate in liquidity-constrained consumers.
- **`ackert2025bnpl`** — *J. Behavioral Finance* 26(4):558-569. Incentivised experiment: consumers
  pick BNPL over a credit-card loan for the same purchase, expecting social approval. Demand-side
  explanation for D3.

## ⚠ South African BNPL market size — DO NOT CITE A HEADLINE FIGURE

Every available estimate is from a commercial market-research vendor, and they contradict each
other badly. Collected estimates:

| Claim | Source |
| --- | --- |
| 2024 market = **US$717.3m**, → $1.30bn by 2030 (9.8% CAGR) | IMARC |
| 2024 market = **US$1.07bn**, → $1.78bn by 2029 (10.6% CAGR) | via Yahoo Finance, researcher unnamed |
| 2025 market = US$815.1m (13.6% growth) | ResearchAndMarkets |
| 2026 market = US$1.11bn (25.2% growth) → 2031 | GlobeNewswire |
| US$1.17bn → $2.66bn, 17.9% CAGR 2026-2031 | Ozow blog |
| US$1.2bn by 2029 | BusinessWire 2024 |

The two 2024 estimates differ by **49%** for the same year, and CAGRs range 9.8% to 25.2% over
overlapping windows. None is a primary source. **Use penetration rates, not market value** — RQ2
sweeps a BNPL *access rate*, so a USD market size was never the right quantity anyway.

**Use instead (already in the repo):** `data/raw/TU_CPS_Q4_2025/` — TransUnion Consumer Pulse SA
Q4 2025. BNPL is the 4th most-planned credit product (20% of intending applicants), and TransUnion
lists BNPL history among information **absent from the standard SA credit report**, which is
bureau-internal confirmation of the D10 invisibility mechanism. Far stronger than the Norton Rose
law-firm note. Secondary: Statista 2022 (91% aware, 27% used in past year); Stitch 2023 survey
(n>300, industry-run, use with care).

**No South African academic BNPL study was found.** Supports the novelty claim, but see the
systematic-search TODO in `main.tex`.

## Tier 3 — South African calibration `[FIND]`

- **NCR Consumer Credit Market Report (CCMR)** — already in `data/raw/CCMR_Q1_2025/`. Gives the
  baseline impairment/arrears rate the no-BNPL run must reproduce (see
  [[behavioural-validation-hedge]]).
- **TransUnion SA Consumer Pulse / CPS** — already in `data/raw/TU_CPS_Q4_2025/`.
- **NCA over-indebtedness + affordability regulations (2015)** — the statutory definition for D7,
  and the DSTI/residual-income formula for D9. Currently `MAX_DSTI=0.65` is asserted, not sourced.
- **`[FIND]` APRs and terms for SA unsecured credit / store cards / personal loans** — this is the
  gap flagged in [[servicing-not-grounded]]; `data/config/credit_rate_table.csv` is hand-populated.
  NCR CCMR reports average rates by product class — that is the fix.
- **`[FIND]` SA BNPL market size / penetration** — PayJustNow, Payflex, Float. Needed to set the
  BNPL access rate that RQ2 sweeps.

---

## Search strings that worked

- `agent-based model household credit market debt default heterogeneous agents`
- `Buy Now Pay Later empirical study consumer debt financial distress`
- `CFPB Buy Now Pay Later report multiple concurrent loans stacking`
- `Buy Now Pay Later South Africa regulation National Credit Act`
- `present bias hyperbolic discounting minimum payment anchoring household debt`

Good venues to sweep directly: **JASSS** (jasss.org — most credit ABMs land here), *Journal of
Economic Behavior & Organization*, *Journal of Economic Dynamics and Control*, *Journal of Financial
Economics*, CFPB / FCA / ASIC / BIS working papers.

---

## Writing order (literature → text → code)

1. **§Literature Review** — three subsections mirroring the three anchors. Writing it forces a
   position on D0–D8.
2. **Fill `decision_rules.md`** as you write; each `_TODO._` becomes "we adopt X, following [cite]".
3. **§ABM Design** — this is just `decision_rules.md` re-expressed in ODD form (`grimm2020odd`).
4. **Then** code `simulation/` against a spec that is already written and already cited.
