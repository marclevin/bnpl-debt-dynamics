# Decision Rules: Open Design Register

**Status:** D0 to D10 are closed and cited (2026-08-05). D11 to D16 remain open. Each closed rule
carries a stated choice, a citation, parameters with sources or explicit sensitivity flags, and a
validation hook. D4 is closed **by assumption**, with no anchor found, and is flagged as such.

> **The contract this file enforces.** Every behavioural rule in the ABM must, before it is coded,
> have (a) a stated choice and (b) at least one cited precedent, whether an ABM paper, a BNPL or
> credit study, or a behavioural-economics finding, so the methodology can say *"we adopt X, following [cite],
> because …"* rather than *"we assumed X."* A rule with no anchor is a flagged limitation, not a
> silent guess.

Canonical strategy: [`../OVERVIEW.md`](../OVERVIEW.md). Design rationale: [`decision.md`](decision.md).
Data → agent mapping: [`../household_agent.md`](../household_agent.md).

---

## How this document will be filled (the research task)

For each decision below:

1. **Name the design space.** The realistic options.
2. **Find precedent.** Search the three anchor literatures and record what comparable models do:
   - **ABM of credit/household finance.** How do existing consumer-credit ABMs implement this rule?
   - **BNPL empirical.** What do BNPL studies and regulator reports observe about this behaviour?
   - **Behavioural economics.** What decision heuristic (not rational optimisation) fits?
3. **Choose and cite.** Fix the rule, record the citation and *why this over the alternatives*.
4. **Set parameters.** Numeric values, each with a source or a sensitivity-analysis flag.
5. **Map to validation.** What observable does this rule move, and against which target is it checked?

**Anchor-source legend used below:**
`[ANCHOR: ABM]` `[ANCHOR: BNPL]` `[ANCHOR: BEHAV]` `[ANCHOR: REG/DATA]` (NCR/CCMR/TransUnion/NCA).

---

## Documentation framing: the ODD protocol

The final write-up will follow the **ODD protocol** (Overview, Design concepts, Details; Grimm et
al. 2006/2020), the standard for communicating ABMs `[grimm2006odd, grimm2020odd]`.
This register maps onto ODD's **"Submodels"** and **"Design concepts"** sections. Filling it ≈
writing those sections.

---

## Part A. Consumer agent: the per-tick decision loop

The consumer is the only adaptive agent in the baseline. One biweekly tick proceeds through an
ordered sequence; **the order itself is a modelling decision.**

### D0. Order of operations within a tick
- **Governs:** everything downstream (does the agent pay debt before or after consuming?).
- **Anchors:** `[ANCHOR: ABM]` D'Orazio & Giulioni `[dorazio2017micro]` (households set desired
  consumption first, then approach the bank when consumption outruns income);
  Madeira `[madeira2018chile]` (households default on debt rather than fall below minimum
  consumption, so consumption has priority over servicing).
- **DECISION.** Design-space option (i), priority-ordered:
  1. Income arrives (D1).
  2. **Committed expenditure** (`expenditure_committed`) is paid first. This is the minimum
     consumption floor and it outranks debt service.
  3. **Scheduled debt service** is attempted (D6).
  4. **Discretionary consumption** is set (D2).
  5. If cash on hand is insufficient at step 2 or 3, the agent seeks credit (D3, D4, D5).
  6. Balances, arrears and distress flags update (D7).
- *Why committed expenditure before debt service:* Madeira's default condition is failure to finance
  minimum consumption, which only makes sense if consumption is prioritised. Putting servicing first
  would make default impossible by construction.
- *Why borrowing last:* in `[dorazio2017micro]` credit is a response to a realised shortfall, not an
  anticipatory decision. Borrowing at step 5 is what allows an agent to borrow in order to service
  existing debt, which is the stacking spiral the thesis is built to observe.
- **Parameters:** none numeric.
- **Sensitivity:** re-run with debt-service-first ordering (option ii) as a robustness check.
- **Validation hook:** ordering changes the timing of arrears onset. Baseline arrears profile is
  checked against the NCR CCMR age analysis (see D6).

### D1. Income arrival and shock
- **Governs:** the inflow each tick and the trigger for distress borrowing.
- **Already decided (decision.md Set 7):** static baseline income plus a biweekly Bernoulli shock.
- **Anchor:** `[ANCHOR: ABM]` Madeira `[madeira2018chile]` models households absorbing **labour
  income** shocks specifically.
- **DECISION.** The shock is a **labour income** shock, applied only to households whose dominant
  income source is `WAGE`. Households dependent on `GRANT` income face no labour shock, because South
  African social grants are statutory transfers and do not vary with employment. This conditioning
  uses `income_source`, which the data layer already carries. The shock hits **income**, not savings,
  and is **non-persistent** (single tick) in the baseline.
- **Parameters:** `p` (shock probability per tick) and shock magnitude are **NOT SOURCED**.
  NIDS W5 is a single wave in this design, so within-household income volatility cannot be estimated
  from it, and QLFS was dropped from scope (decision.md Set 3).
- **Treatment:** `p` is promoted from assumption to **calibration target**. It is fitted so the
  baseline (no-BNPL) arrears rate reproduces the CCMR benchmark, then held fixed for all BNPL runs.
  Magnitude is swept.
- **Validation hook:** this is the parameter that *carries* the validation. Because `p` is fitted to
  baseline arrears, the baseline is calibrated rather than validated, and only the BNPL-on results
  are genuine predictions. **State this explicitly in the limitations chapter.**

### D2. Consumption rule
- **Governs:** how fast the cash buffer is drawn down; the main driver of running short.
- **Anchors:** `[ANCHOR: ABM]` `[dorazio2017micro]` (desired consumption formed first, credit sought
  when it outruns income); `[madeira2018chile]` (minimum consumption standards as the binding floor).
- **DECISION.** Two-tier consumption drawn directly from the data layer:
  - `expenditure_committed` (food and rent) is a **hard floor**. It is not compressible.
  - `expenditure_discretionary` is the **target**, compressible to zero when cash-constrained.
  An agent compresses discretionary spending fully before missing a debt instalment, and defaults
  (D7) only when income plus available credit cannot meet the committed floor plus scheduled service.
- *Why not an MPC or buffer-stock rule:* both require a calibrated propensity we have no South
  African estimate for, and both would discard the observed NIDS expenditure split we already hold.
- **Parameters:** compression floor on discretionary spending = 0 in baseline.
- **Sensitivity:** partial floor (habit persistence) at 25% and 50% of baseline discretionary.
- **Validation hook:** compression rate drives savings drawdown; check the share of agents reaching
  zero liquid savings against the TransUnion Consumer Pulse finding that 36% of South African
  consumers anticipated missing a bill payment `[transunion_cps_sa_2025]`.

### D3. Borrowing trigger
- **Governs:** demand for credit, and later for BNPL specifically.
- **Anchors:** `[ANCHOR: ABM]` `[dorazio2017micro]` (credit requested on shortfall);
  `[ANCHOR: BEHAV]` Meier & Sprenger `[meier2010present]` (present bias predicts borrowing);
  `[ANCHOR: BNPL]` Hayashi & Routh `[toh2025bnplconstraints]` (BNPL users are financially
  constrained; 96% of late payers at least mildly constrained);
  Ackert et al. `[ackert2025bnpl]` (BNPL chosen over a credit-card loan for the same purchase,
  with expected social approval).
- **DECISION.** The trigger is **dual, and differs by lender type**:
  - **Traditional credit: shortfall-driven only.** The agent applies when cash on hand cannot meet
    committed expenditure plus scheduled debt service.
  - **BNPL: shortfall-driven OR want-driven.** In addition to the shortfall path, a BNPL-eligible
    agent initiates a discretionary BNPL purchase with probability `q` per tick.
- *Why BNPL gets a second trigger:* `[ackert2025bnpl]` shows BNPL uptake is driven by social norm
  rather than need, and `[dehaan2024bnpl]` finds harm following adoption even among consumers who
  had credit available. A purely shortfall-driven BNPL agent would model BNPL as a pure substitute
  and could not reproduce either finding.
- **Parameters:** `q` (impulse propensity) is **NOT SOURCED**; swept across the RQ2 range.
- **Validation hook:** share of households borrowing per tick; and the D5 complementarity test below.

### D4. Borrowing amount
- **Governs:** how much debt each credit event adds.
- **STATUS: SETTLED BY ASSUMPTION. NO ANCHOR FOUND.**
- The literature sweep found no consumer-credit ABM or behavioural study that fixes a borrowing
  *amount* rule. `[dorazio2017micro]` has households request the gap between desired consumption and
  income, which is the shortfall rule, but the paper does not defend the choice.
- **DECISION (assumption).** The agent requests **exactly the shortfall**, with no precautionary
  buffer. For BNPL, the amount is anchored to the purchase size rather than to a shortfall.
- **This is a flagged limitation, not a cited rule.** It must appear in the limitations chapter as
  an uncited modelling choice.
- **Sensitivity (mandatory, not optional):** shortfall, shortfall x 1.25, and shortfall plus one
  tick of committed expenditure. If results move materially across these, the model is
  amount-rule-sensitive and the finding must be reported as such.

### D5. Lender choice
- **Governs:** substitution versus complementarity between traditional credit and BNPL. Central to
  RQ1.
- **Anchors:** `[ANCHOR: BNPL]` Ackert et al. `[ackert2025bnpl]` (consumers chose BNPL over a
  credit-card loan for the same purchase); CFPB `[cfpb2025bnpl]` (32% of BNPL borrowers held loans
  across different firms); deHaan et al. `[dehaan2024bnpl]` (BNPL adoption is followed by *rising*
  credit-card interest and late fees).
- **DECISION.** Design-space option (ii), **BNPL-first**, where BNPL exists and the need is
  BNPL-eligible. Traditional credit is approached for shortfalls BNPL cannot cover, and remains the
  only channel in the no-BNPL baseline.
- *Why not cost-ranked:* BNPL is nominally interest-free, so cost-ranking selects it trivially and
  attributes the choice to price. The evidence attributes it to convenience and social norm
  `[ackert2025bnpl]`, which is a different mechanism with different intervention implications (RQ3).
- **Validation hook (strong, external).** `[dehaan2024bnpl]` establishes **complementarity**: BNPL
  adopters' credit-card interest and late fees *rise*. Switching BNPL on in the model must therefore
  **increase**, not decrease, traditional-credit stress. If the model produces substitution
  (traditional debt falls when BNPL is enabled), it contradicts the best available causal evidence
  and the lender-choice rule is wrong. **This is the single most useful falsification test the
  model has.**

### D6. Repayment rule and arrears
- **Governs:** how debt is retired versus how it snowballs. Drives the default observable.
- **Anchors:** `[ANCHOR: BEHAV]` Keys & Wang `[Keys2019]` (29% of accounts pay at or near the
  contractual minimum; at least 22% of near-minimum payers anchor to the formula);
  Kuchler & Pagel `[Kuchler2021]` (present-biased borrowers fail to execute planned paydown);
  `[ANCHOR: REG/DATA]` NCR CCMR age-analysis bands `[ncr_ccmr_2025]`.
- **DECISION.** **Mixed repayment behaviour**, not uniform amortisation:
  - A share `m` of agents are **minimum-payers**: they pay the contractual minimum only.
  - The remainder pay the **scheduled amortised instalment** (`monthly_trad_repayment`, constructed
    in P2 on NCA statutory rates).
  - Any agent that cannot meet its due amount pays what it can; the residual accrues as **arrears**.
- **Parameters:** `m = 0.29` baseline, from `[Keys2019]`.
- **⚠ Parameter caveat:** 0.29 is a United States credit-card figure. Applying it to South African
  unsecured credit is a transfer assumption. Sweep 0.20 to 0.40.
- **Arrears definition:** CCMR age bands (current, 30, 60, 90+ days). At a biweekly tick, 90 days is
  6 ticks.
- **Validation hook:** baseline share of accounts current versus CCMR. **⚠ Vintage problem:** the
  CCMR in the repo is Q1 2025 (unsecured credit ~70.6% of accounts current) but the population is
  2017. **Obtain the 2017-vintage CCMR from the NCR before using this as a target.**

### D7. Distress and default definition
- **Governs:** the model's headline output variable. The threshold the RQs ask about.
- **Anchors:** `[ANCHOR: ABM]` Madeira `[madeira2018chile]` (households default when unable to
  finance minimum consumption standards, and the model is validated against observed default rates);
  `[ANCHOR: REG/DATA]` NCA over-indebtedness `[sa_nca_2005]`.
- **DECISION.** Design-space option (ii), **cash-flow insolvency**. A household is *distressed* in a
  tick when income plus available credit cannot cover committed expenditure plus scheduled debt
  service. It is in **default** after `k` consecutive distressed ticks.
- *Why not DSTI > 50%:* a DSTI threshold is arbitrary, and the D9 work established that the NCA
  itself does not use a DSTI ratio. Madeira's minimum-consumption test is cited, is consistent with
  the Reg 23A affordability rule already implemented in P2, and is validated against real default
  rates in a middle-income economy.
- **Parameters:** `k = 6` ticks (3 months), aligning with the CCMR 90-day impairment convention.
- **Consequences:** credit cut-off from the traditional lender (which sees the default via the
  bureau, D10) and penalty accrual.
- **⚠ Limitation:** no scarring or recovery path in the baseline. Once defaulted, an agent does not
  rehabilitate. Over a 24-month horizon this is tolerable but it must be stated.
- **Validation hook:** population default rate versus CCMR impairment (subject to the D6 vintage
  problem).

### D8. Behavioural heterogeneity
- **Governs:** whether all agents share one rule set.
- **Anchors:** `[ANCHOR: BEHAV]` Meier & Sprenger `[meier2010present]` (present bias varies across
  individuals and predicts borrowing); `[ANCHOR: ABM]` Hamill et al. `[hamill2023creditcard]`
  (non-monotonic relationship between income and debt-to-income, with middle-income households
  carrying the highest balance-to-income).
- **DECISION.** Design-space option (ii) plus a restricted form of (iii):
  - Rule *parameters* vary by **income quintile** and by the demographic and flag attributes the
    data layer already carries (`banked_status`, `credit_access_formal`, `income_source`).
  - One **binary behavioural type** only: minimum-payer versus scheduled-payer (D6).
- *Why not a latent continuous present-bias parameter:* no South African distribution of present
  bias exists to calibrate it against, so it would add a free parameter with no discipline.
- **Parameters:** quintile assignment is data-driven, not free. Type share `m` is D6's parameter.
- **Validation hook (pattern-oriented).** `[hamill2023creditcard]` reports a non-monotonic income to
  debt-to-income relationship with a middle-income peak. If this model produces monotonically rising
  DTI in income, it disagrees with an independent ABM of the same phenomenon. Following the ODD
  second update's emphasis on stating the patterns that judge realism `[grimm2020odd]`, this is
  registered as a target pattern in advance.

---

## Part B. Lender (traditional, single stub)

### D9. Credit-granting gate (affordability / approval)
- **Governs:** supply of traditional credit; the constraint BNPL routes around.
- **Already decided (decision.md Set 6):** deterministic **visible-debt gate**, NCA-style.
- **Anchor:** `[ANCHOR: REG/DATA]` NCA Affordability Assessment Regulations, Reg 23A(9)
  (GN R202, GG 38557, 13 Mar 2015) `[cite: sa_ncr_affordability_2015]`.
- **DECISION (affordability formula).** The gate is a **residual-income test**, not a
  DSTI cap. The NCA prescribes **no debt-service-to-income ratio**; it prescribes a minimum
  expense-norms table by gross income band. The lender grants only if
  `gross income − statutory deductions − Reg 23A necessary expenses − visible existing obligations ≥ new instalment`.
  Already implemented as the servicing ceiling in P2; the *same* function is the D9 gate.
  Implied ceiling is income-varying: **10.4% of income at R900/month, 83.2% at R7,712/month.**
  *Why this over a DSTI cap:* a flat cap is unsourced and, at the bottom of the distribution,
  wildly over-permissive, since it would let a R900/month household service R585/month.
- **Still open:** what counts as *visible* existing obligations (→ D10), and whether the lender
  applies the statutory minimum or a stricter internal policy.

### D10. Information asymmetry: what the lender can and cannot see
- **Governs:** the core mechanism of the thesis. Banks cannot see BNPL obligations.
- **Anchors:** `[ANCHOR: BNPL]` Norton Rose Fulbright `[nortonrose_bnpl_sa]` (BNPL falls outside the
  NCA, so no NCR registration, no Reg 23A assessment, and no obligation to report to credit
  bureaux); `[ANCHOR: REG/DATA]` TransUnion `[transunion_cps_sa_2025]`, which lists BNPL history
  among the categories of information **absent from the standard South African credit report**. The
  second source is bureau-internal and therefore confirms the mechanism from inside the credit
  infrastructure rather than from legal commentary.
- **DECISION.** A single in-model **bureau record** exists and holds **traditional debt only**.
  When assessing an application the traditional lender observes:
  - the household's gross income (declared),
  - its own outstanding loans to that household,
  - all other **traditional** debt, via the bureau.

  It does **not** observe:
  - **BNPL obligations** (the thesis mechanism),
  - **informal debt** (mashonisa, stokvel advances), which is not reported to bureaux in reality and
    enters the model only as static balance-sheet state carried from NIDS.
- *Consequence for D9:* the Reg 23A residual-income test is computed on an incomplete liability
  set. The lender is not behaving unlawfully or carelessly; it is complying with the regulation
  using the record the regulation gives it. That is precisely the point.
- **Parameters:** `bnpl_bureau_visible` (boolean, default `False`). This is also the RQ3 intervention
  lever in D14.
- **Validation hook (internal, and useful).** Running with `bnpl_bureau_visible = True` should
  recover affordability outcomes close to the no-BNPL baseline, because the lender can then price
  and gate against the full liability set. The **gap between the two runs is the measured cost of
  the regulatory reporting gap**, which is a direct quantitative answer to the policy question
  behind RQ3.

---

## Part C. BNPL platform (deferred extension, but decisions named now)

### D11. BNPL eligibility & limit
- **Design space:** near-universal acceptance (low friction) vs light affordability screen; per-purchase
  limit vs rolling limit.  **Anchor:** `[ANCHOR: BNPL]`. **Decision:** _TODO._

### D12. Multi-platform **stacking** (RQ1, RQ2)
- **Governs:** the self-reinforcing debt mechanism. *Open:* can an agent hold N concurrent BNPL
  facilities? Do platforms see each other? Is there an aggregate limit?
- **Anchor:** `[ANCHOR: BNPL]` (evidence on concurrent BNPL use) + `[ANCHOR: REG/DATA]`.
  **Decision:** _TODO._

### D13. BNPL repayment structure & penalties
- **Design space:** pay-in-4 biweekly (decision.md Set 1 cadence), late fees, default handling.
  **Anchor:** `[ANCHOR: BNPL]`. **Decision:** _TODO._

### D14. Intervention levers (RQ3)
- **Governs:** the policy experiments. *Open:* "cool-off period" mechanics; stacking cap; mandatory
  affordability check; bureau visibility switch.
- **Anchor:** `[ANCHOR: BNPL/REG]`. **Decision:** _TODO._

---

## Part D. Environment & scheduling

### D15. Macro environment
- **Already decided (Set 7):** homogeneous, exogenous, held in 2017 terms. *Open:* are any macro
  variables time-varying within the run, or fully static? **Decision:** _TODO._

### D16. Scheduling / activation order
- **Already decided (Set 7):** synchronous biweekly clock (consumers act → lender processes → state
  updates). *Open:* agent activation order within the consumer step (random, staged or simultaneous),
  a known ODD design concept that affects results. **Anchor:** `[ANCHOR: ABM]`. **Decision:** _TODO._

---

## Part E. Calibration & experiment knobs (tie rules → research questions)

| RQ | Mechanism it tests | Rules involved | Swept parameter(s) |
| -- | ------------------ | -------------- | ------------------ |
| RQ1: when does stacking self-reinforce? | debt accumulates faster than repayment | D5, D6, D12 | stacking depth, BNPL-first propensity |
| RQ2: non-linear default threshold | population default vs BNPL access | D3, D7, D11 | BNPL access/penetration rate |
| RQ3: do cool-off periods work? | defer vs desist | D3, D14 | cool-off length, on/off |

**Validation targets (provider-independent fallback):** baseline (no-BNPL) default/arrears should
reproduce a **CCMR / TransUnion** aggregate before any BNPL is switched on. See
[[behavioural-validation-hedge]] and [`../OVERVIEW.md`](../OVERVIEW.md) §7.

---

## Open-decision checklist (fill as research lands)

- [x] D0 tick order · [x] D1 income/shock · [x] D2 consumption · [x] D3 borrow trigger
- [~] D4 borrow amount *(assumption, no anchor)* · [x] D5 lender choice · [x] D6 repayment/arrears · [x] D7 default def.
- [x] D8 heterogeneity · [x] D9 credit gate · [x] D10 info asymmetry · [ ] D11 BNPL eligibility
- [ ] D12 stacking · [ ] D13 BNPL repayment · [ ] D14 interventions · [ ] D15 macro · [ ] D16 scheduling

Each box closes only when it has: a stated rule, a citation, parameters with sources, and a
validation hook.
