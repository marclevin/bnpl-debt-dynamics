# Decision Rules — Open Design Register (logic deferred to literature)

**Status:** scaffold. This document enumerates **which** behavioural decisions the model forces us to
make. It deliberately does **not** yet fix the logic. Each rule is an *open decision* with a
candidate design space and a slot for the literature anchor that will justify the final choice.

> **The contract this file enforces.** Every behavioural rule in the ABM must, before it is coded,
> have (a) a stated choice and (b) at least one cited precedent — an ABM paper, a BNPL/credit study,
> or a behavioural-economics finding — so the methodology can say *"we adopt X, following [cite],
> because …"* rather than *"we assumed X."* A rule with no anchor is a flagged limitation, not a
> silent guess.

Canonical strategy: [`../OVERVIEW.md`](../OVERVIEW.md). Design rationale: [`decision.md`](decision.md).
Data → agent mapping: [`../household_agent.md`](../household_agent.md).

---

## How this document will be filled (the research task)

For each decision below:

1. **Name the design space** — the realistic options (done now, in this scaffold).
2. **Find precedent** — search the three anchor literatures and record what comparable models do:
   - **ABM of credit/household finance** — how do existing consumer-credit ABMs implement this rule?
   - **BNPL empirical** — what do BNPL studies / regulator reports observe about this behaviour?
   - **Behavioural economics** — what decision heuristic (not rational optimisation) fits?
3. **Choose + cite** — fix the rule, record the citation and *why this over the alternatives*.
4. **Set parameters** — numeric values, each with a source or a sensitivity-analysis flag.
5. **Map to validation** — what observable does this rule move, and against which target it's checked.

**Anchor-source legend used below:**
`[ANCHOR: ABM]` `[ANCHOR: BNPL]` `[ANCHOR: BEHAV]` `[ANCHOR: REG/DATA]` (NCR/CCMR/TransUnion/NCA).

---

## Documentation framing — ODD protocol

The final write-up will follow the **ODD protocol** (Overview, Design concepts, Details; Grimm et
al. 2006/2020) — the standard for communicating ABMs. `[ANCHOR: ABM — Grimm et al., to cite]`.
This register maps onto ODD's **"Submodels"** and **"Design concepts"** sections. Filling it ≈
writing those sections.

---

## Part A — Consumer agent: the per-tick decision loop

The consumer is the only adaptive agent in the baseline. One biweekly tick proceeds through an
ordered sequence; **the order itself is a modelling decision.**

### D0 — Order of operations within a tick
- **Governs:** everything downstream (does the agent pay debt before or after consuming?).
- **Design space:** (i) income → committed expenses → debt service → discretionary → borrow if short;
  (ii) income → debt service first (priority-of-debt); (iii) behavioural ordering (pay what's
  salient, not what's optimal).
- **Anchor needed:** `[ANCHOR: ABM]` (typical balance-sheet update order) + `[ANCHOR: BEHAV]`
  (mental-accounting / salience of bills).
- **Decision:** _TODO._

### D1 — Income arrival & shock
- **Governs:** the inflow each tick and the trigger for distress borrowing.
- **Already decided (decision.md Set 7):** static baseline income + a single biweekly **Bernoulli
  shock**. *Open sub-decisions:* shock probability `p`, shock magnitude (fraction of income? fixed
  Rand?), whether it hits income or savings, persistence (one-tick vs lasting).
- **Anchor needed:** `[ANCHOR: REG/DATA]` (income volatility for LMI SA households) + `[ANCHOR: ABM]`
  (how comparable models inject shocks).
- **Decision:** _TODO._

### D2 — Consumption rule (how much discretionary spend)
- **Governs:** how fast the cash buffer is drawn down; the main driver of "running short".
- **Design space:** (i) fixed from NIDS `expenditure_discretionary`; (ii) propensity-to-consume out
  of cash-on-hand (Keynesian MPC); (iii) buffer-stock / target-savings behaviour; (iv) habit /
  reference-dependent consumption.
- **Anchor needed:** `[ANCHOR: BEHAV]` (buffer-stock theory, MPC heterogeneity) + `[ANCHOR: ABM]`.
- **Decision:** _TODO._

### D3 — Borrowing **trigger**: when does an agent seek credit?
- **Governs:** demand for credit (and later, for BNPL specifically).
- **Design space:** (i) shortfall-driven (borrow only when cash < committed expenses); (ii)
  consumption-smoothing (borrow to maintain a discretionary target); (iii) want-driven / impulse
  (BNPL at point of sale regardless of need).
- **Anchor needed:** `[ANCHOR: BNPL]` (is BNPL use need-driven or impulse/convenience?) +
  `[ANCHOR: BEHAV]` (present bias / hyperbolic discounting).
- **Decision:** _TODO._

### D4 — Borrowing **amount**: how much does it ask for?
- **Design space:** (i) exactly the shortfall; (ii) shortfall + buffer; (iii) capped by a desired
  DSTI; (iv) anchored to the purchase size (BNPL).
- **Anchor needed:** `[ANCHOR: BEHAV]` + `[ANCHOR: ABM]`.
- **Decision:** _TODO._

### D5 — Lender **choice**: who does it ask, and in what order?
- **Governs:** the substitution/complementarity between traditional credit and BNPL — central to the
  debt-stacking question (RQ1).
- **Design space:** (i) traditional first, BNPL as fallback when refused; (ii) BNPL-first
  (convenience/low friction); (iii) cost-ranked; (iv) availability/eligibility-ranked.
- **Anchor needed:** `[ANCHOR: BNPL]` (why consumers pick BNPL over store/credit) + `[ANCHOR: BEHAV]`.
- **Decision:** _TODO._

### D6 — Repayment rule & arrears
- **Governs:** how debt is retired vs how it snowballs; directly drives the default observable.
- **Design space:** (i) scheduled amortised payment (current `monthly_trad_repayment` logic);
  (ii) minimum-payment behaviour (revolving); (iii) avalanche/snowball ordering across multiple debts;
  (iv) partial / missed payment when cash-constrained → arrears accrual.
- **Anchor needed:** `[ANCHOR: BEHAV]` (minimum-payment bias) + `[ANCHOR: REG/DATA]` (arrears
  definitions — CCMR/NCR).
- **Decision:** _TODO._  *(See also [[servicing-not-grounded]] — the APR/term table feeding this is
  currently unsourced.)*

### D7 — Distress / default **definition** and consequences
- **Governs:** the model's headline output variable; the threshold the RQs ask about.
- **Design space:** (i) DSTI > threshold = distressed (work.md suggests 50%); (ii) cash-flow
  insolvency (cannot meet committed + minimum service for k consecutive ticks); (iii) NCA
  "over-indebtedness". *Consequences:* credit cut-off, penalty fees, recovery, scarring/recovery path.
- **Anchor needed:** `[ANCHOR: REG/DATA]` (NCA over-indebtedness; CCMR impairment) + `[ANCHOR: ABM]`.
- **Decision:** _TODO._

### D8 — Behavioural heterogeneity across agents
- **Governs:** whether all agents share one rule set or differ (by quintile, by present-bias type…).
- **Design space:** (i) homogeneous rules; (ii) parameters vary by income quintile / demographics
  (data we already have); (iii) latent behavioural "types" (e.g. present-biased vs patient).
- **Anchor needed:** `[ANCHOR: BEHAV]` (distribution of present bias) + `[ANCHOR: ABM]`.
- **Decision:** _TODO._

---

## Part B — Lender (traditional, single stub)

### D9 — Credit-granting gate (affordability / approval)
- **Governs:** supply of traditional credit; the constraint BNPL routes around.
- **Already decided (decision.md Set 6):** deterministic **visible-debt gate**, NCA-style. *Open:*
  the actual affordability formula (DSTI cap? residual-income? credit-score proxy?), and the cutoff.
- **Anchor needed:** `[ANCHOR: REG/DATA]` (NCA affordability assessment regs) + `[ANCHOR: ABM]`.
- **Decision:** _TODO._

### D10 — Information asymmetry: what the lender can/can't see
- **Governs:** the core mechanism of the thesis — banks **cannot see BNPL obligations**
  (work.md / decision.md). *Open:* can the lender see other traditional debt? informal debt? Does a
  bureau exist in-model?
- **Anchor needed:** `[ANCHOR: BNPL]` (BNPL invisibility to bureaus) + `[ANCHOR: REG/DATA]`.
- **Decision:** _TODO._

---

## Part C — BNPL platform (deferred extension, but decisions named now)

### D11 — BNPL eligibility & limit
- **Design space:** near-universal acceptance (low friction) vs light affordability screen; per-purchase
  limit vs rolling limit.  **Anchor:** `[ANCHOR: BNPL]`. **Decision:** _TODO._

### D12 — Multi-platform **stacking** (RQ1, RQ2)
- **Governs:** the self-reinforcing debt mechanism. *Open:* can an agent hold N concurrent BNPL
  facilities? Do platforms see each other? Is there an aggregate limit?
- **Anchor:** `[ANCHOR: BNPL]` (evidence on concurrent BNPL use) + `[ANCHOR: REG/DATA]`.
  **Decision:** _TODO._

### D13 — BNPL repayment structure & penalties
- **Design space:** pay-in-4 biweekly (decision.md Set 1 cadence), late fees, default handling.
  **Anchor:** `[ANCHOR: BNPL]`. **Decision:** _TODO._

### D14 — Intervention levers (RQ3)
- **Governs:** the policy experiments. *Open:* "cool-off period" mechanics; stacking cap; mandatory
  affordability check; bureau visibility switch.
- **Anchor:** `[ANCHOR: BNPL/REG]`. **Decision:** _TODO._

---

## Part D — Environment & scheduling

### D15 — Macro environment
- **Already decided (Set 7):** homogeneous, exogenous, held in 2017 terms. *Open:* are any macro
  variables time-varying within the run, or fully static? **Decision:** _TODO._

### D16 — Scheduling / activation order
- **Already decided (Set 7):** synchronous biweekly clock (consumers act → lender processes → state
  updates). *Open:* agent activation order within the consumer step (random / staged / simultaneous) —
  a known ODD design concept that affects results. **Anchor:** `[ANCHOR: ABM]`. **Decision:** _TODO._

---

## Part E — Calibration & experiment knobs (tie rules → research questions)

| RQ | Mechanism it tests | Rules involved | Swept parameter(s) |
| -- | ------------------ | -------------- | ------------------ |
| RQ1 — when does stacking self-reinforce? | debt accumulates faster than repayment | D5, D6, D12 | stacking depth, BNPL-first propensity |
| RQ2 — non-linear default threshold | population default vs BNPL access | D3, D7, D11 | BNPL access/penetration rate |
| RQ3 — do cool-off periods work? | defer vs desist | D3, D14 | cool-off length, on/off |

**Validation targets (provider-independent fallback):** baseline (no-BNPL) default/arrears should
reproduce a **CCMR / TransUnion** aggregate before any BNPL is switched on. See
[[behavioural-validation-hedge]] and [`../OVERVIEW.md`](../OVERVIEW.md) §7.

---

## Open-decision checklist (fill as research lands)

- [ ] D0 tick order · [ ] D1 income/shock · [ ] D2 consumption · [ ] D3 borrow trigger
- [ ] D4 borrow amount · [ ] D5 lender choice · [ ] D6 repayment/arrears · [ ] D7 default def.
- [ ] D8 heterogeneity · [ ] D9 credit gate · [ ] D10 info asymmetry · [ ] D11 BNPL eligibility
- [ ] D12 stacking · [ ] D13 BNPL repayment · [ ] D14 interventions · [ ] D15 macro · [ ] D16 scheduling

Each box closes only when it has: a stated rule, a citation, parameters with sources, and a
validation hook.
