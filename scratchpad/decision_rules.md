# Decision Rules: Open Design Register

**Status:** **all 18 decisions (D0 to D17) are closed and cited** (2026-08-05). Each closed rule
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
  - **`q` is not a constant.** It is socially transmitted: see **D17**, where
    `q_i(t) = clip(q_base + β · s_g(t-1), 0, 1)` and `s_g` is the BNPL-adoption share of the agent's
    reference group. **Peer influence acts on the want-driven path only.** The shortfall path is
    untouched, because a household in genuine shortfall borrows regardless of what its peers do.
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
- **Validation hook (strong, external).** `[dehaan2024bnpl]` establishes **complementarity**. Note
  precisely what they measure: overdraft charges, credit-card *interest* and *late fees*, which are
  indicators of servicing stress, **not** outstanding balances. The model analogue is therefore
  **arrears and interest burden on traditional debt**, not traditional debt stock. Switching BNPL on
  must **increase** traditional-credit arrears and interest burden. If instead the model shows
  traditional stress *falling* when BNPL is enabled (pure substitution), it contradicts the best
  available causal evidence and the lender-choice rule is wrong. **This is the single most useful
  falsification test the model has.**

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
- **Arrears definition:** CCMR age bands (current, 30, 31-60, 61-90, 91-120, 120+ days).
- **Validation hook (2017 vintage, resolved).** `data/raw/CCMR_Q1_2017/` (NCR CCMR March 2017) is
  now in the repo and extracted to `data/config/ccmr_2017_baseline.json`. **2017-Q1, account basis:**

  | Credit type | % current | % 60+ days | % 90+ days |
  | --- | --- | --- | --- |
  | Unsecured credit | 71.99% | 20.19% | 18.19% |
  | Credit facilities | 71.55% | 15.74% | 13.34% |
  | **Combined (the model target)** | **71.63%** | **16.54%** | **14.21%** |

  Combined unsecured plus credit facilities is the closest analogue to the model's consolidated
  `D_trad` for an LMI household. Both figures are cross-checked against the report's own prose in
  the extraction script.
- **⚠ Unit mismatch (state it).** CCMR counts **accounts**; the model counts **households**. A
  household may hold several accounts, so an account-level arrears rate is not a household-level
  default rate. Treat as an order-of-magnitude target, not a point target.
- **⚠ Data quality note.** Section 4.4 of the converted 2017 markdown has a **corrupt** credit
  facilities "% Number of accounts" column (83.22% repeated for all 13 quarters). Appendix D
  Table 21 is authoritative and reproduces the prose figure of 71.55%. Do not read section 4.4.

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
- **Parameters:** `k = 7` ticks. **Revised from k=6 once the 2017 CCMR buckets were in hand.** At a
  14-day tick, k=7 is **98 days**, which falls inside the CCMR `91-120` bucket and therefore maps
  cleanly onto the **90+ days** impairment convention. k=6 would be 84 days, which lands inside the
  `61-90` bucket and so has **no clean CCMR analogue at all**. Choosing k for tick-alignment with the
  validation target is deliberate, and should be said out loud in the methodology rather than
  presented as a round number.
- **Sensitivity:** `k = 4` (56 days, maps to the 60+ band, target 16.54%) as the looser definition.
- **Consequences:** credit cut-off from the traditional lender (which sees the default via the
  bureau, D10) and penalty accrual.
- **⚠ Limitation:** no scarring or recovery path in the baseline. Once defaulted, an agent does not
  rehabilitate. Over a 24-month horizon this is tolerable but it must be stated.
- **Validation hook:** with `k = 7`, the baseline population default rate targets the 2017-Q1 CCMR
  **90+ days** figure of **14.21%** of accounts (combined unsecured and credit facilities). With
  `k = 4` it targets the 60+ figure of **16.54%**. Subject to the D6 account-versus-household unit
  mismatch.

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

## Part C. BNPL platform (the injected entity)

> **Vintage note applying to all of Part C.** BNPL product parameters are taken **as currently
> specified by South African providers**, and are therefore at current vintage while the population
> is 2017. This is not an oversight: the counterfactual design (OVERVIEW §1a) asks what *today's*
> product does to a 2017 population, so today's product terms are the correct ones. Where a
> parameter is a Rand amount it is generous in 2017 real terms, which is flagged per-rule and swept.

### D11. BNPL eligibility and limit
- **Governs:** who can use BNPL at all, and how much. Sets the ceiling on the RQ2 access sweep.
- **Anchors:** `[ANCHOR: BNPL/REG]` Payflex `[payflex_terms]` (automated credit assessment, orders
  capped at **R15,000**); PayJustNow `[payjustnow_terms]` (an *available balance* rather than a
  credit limit; where a purchase exceeds the facility the difference is added to the first
  instalment); `[ANCHOR: BNPL]` Hayashi & Routh `[toh2025bnplconstraints]` (users are financially
  constrained, so the screen cannot be a serious affordability test).

- **DECISION (eligibility).** A household is BNPL-eligible only if it is **banked**. Both major
  South African providers debit a bank card for the checkout instalment, so an unbanked household
  cannot transact at all. This uses the existing `banked` flag, which caps eligibility at **83.1% of
  the population** by data rather than by assumption. **The RQ2 access sweep therefore runs within
  the banked subpopulation, not over the whole population**, and the ceiling is observed rather than
  chosen.
- **DECISION (screen).** A **light automated screen**, explicitly *not* the Reg 23A residual-income
  test of D9. That asymmetry is the mechanism: BNPL routes around the affordability assessment
  precisely because it is outside the NCA (D10). Making the BNPL screen a real affordability test is
  an *intervention*, not the baseline (D14, lever 2).
- **DECISION (limit).** A per-order cap of R15,000 following Payflex, plus a rolling available
  balance per platform.
- **Parameters:** order cap R15,000 (Payflex, current vintage); rolling balance **NOT SOURCED**,
  swept.
- **⚠ Why the vintage problem is mostly moot here:** at LMI household incomes a R15,000 order cap
  will rarely bind. The binding constraint on borrowing size is the purchase amount (D4), not the
  platform cap. Verify empirically once implemented; if the cap binds for more than a few percent of
  transactions, revisit.
- **Validation hook:** share of eligible households ≈ 83.1% by construction; check that the order
  cap binds rarely.

### D12. Multi-platform stacking (RQ1, RQ2)
- **Governs:** the self-reinforcing debt mechanism. The core of RQ1.
- **Anchors:** `[ANCHOR: BNPL]` CFPB `[cfpb2025bnpl]`: across 2021 and 2022, **63% of BNPL borrowers
  held simultaneous loans** at some point, **32% held them across different firms**, and roughly
  **20% originated more than one loan per month**.

- **DECISION (concurrency).** A household may hold **N concurrent BNPL facilities**, one per
  platform, with no aggregate limit across platforms.
- **DECISION (platform blindness follows from D10, it is not a new assumption).** Platforms **cannot
  see one another**. This is a direct consequence of BNPL sitting outside the NCA with no
  bureau-reporting obligation: with no shared reporting infrastructure there is no channel through
  which one platform could observe another's exposure. Each platform applies its own screen and its
  own cap to a liability set it cannot fully see, exactly as the traditional lender does in D9.
- **Parameters:** `N_platforms = 4` baseline (PayJustNow, Payflex, Mobicred and TymeBank are all
  active in South Africa), swept 1 to 6. `N = 1` is a useful control: it isolates single-platform
  debt accumulation from cross-platform stacking.
- **Validation hook (external, transferable with care).** Stacking depth is **emergent, not
  imposed**. At a realistic access rate the model should approximate the CFPB shares: roughly 63% of
  adopters holding simultaneous loans and 32% holding across firms. ⚠ United States figures applied
  to a South African model; treat as an order-of-magnitude check and state the transfer.

### D13. BNPL repayment structure and penalties
- **Governs:** how BNPL obligations retire or snowball.
- **Anchors:** `[ANCHOR: BNPL/REG]` Payflex `[payflex_terms]`: **Pay in 4** splits a purchase into
  four interest-free instalments over six weeks, 25% at checkout then three further 25% instalments
  **every two weeks**; late fee **R95 per week capped at three weeks**. PayJustNow
  `[payjustnow_terms]`: Pay in 3, first instalment at checkout then two monthly instalments.

- **DECISION.** **Pay in 4 on the Payflex schedule**: 25% of the purchase at checkout, then 25% at
  each of the next three ticks.
- **This retroactively validates the 14-day tick.** decision.md Set 1 chose a biweekly step because
  it "aligns with pay-in-4 BNPL cadence". That alignment is now confirmed against an actual South
  African product rather than assumed: Payflex instalments fall **exactly** on the model tick, so no
  discretisation error is introduced anywhere in the BNPL schedule.
- **Interest:** zero. That is the product, and it is the basis on which providers claim to fall
  outside the NCA (D10).
- **Penalties:** R95 per week late, capped at three weeks, so **R190 per tick to a maximum of R285**
  per missed instalment. Once the fee cap is exhausted the balance converts to arrears and the
  household is cut off from that platform, while remaining eligible at others, since platforms are
  blind to each other (D12).
- **Parameters:** all sourced from Payflex except the post-cap handling, which is an assumption.
- **Sensitivity:** Pay in 3 monthly (PayJustNow) as the structural alternative.

### D14. Intervention levers (RQ3)
- **Governs:** the policy experiments. RQ3.
- **Anchors:** `[ANCHOR: REG/DATA]` FCA `[fca_ps26_1]`, which brings Deferred Payment Credit into
  the UK regulatory perimeter from **15 July 2026** and requires **proportionate affordability
  checks**; the Woolard Review `[woolard2021]`, whose 26 recommendations initiated that process;
  and **CCA s.66A**, which gives a **14-day right of withdrawal** on regulated credit agreements.

Four levers, three of which correspond to instruments that actually exist:

1. **Bureau visibility** (`bnpl_bureau_visible`, boolean, default false). Closes the South African
   reporting gap identified in D10. The gap between on and off measures the cost of the reporting
   exemption directly.
2. **Mandatory affordability check.** Applies the D9 Reg 23A residual-income test to BNPL as well as
   to traditional credit. This is the FCA's "proportionate affordability checks" expressed in South
   African statutory terms.
3. **Cool-off period.** `k_cool = 1` tick baseline, which is **14 days, the CCA s.66A statutory
   figure**, and again falls exactly on a tick boundary. Mechanics: after initiating a want-driven
   BNPL purchase, a household cannot initiate another for `k_cool` ticks. The shortfall-driven path
   is not blocked, since a cool-off on emergency borrowing would be a different instrument.
   Swept 0 to 4 ticks.
4. **Stacking cap.** A maximum on concurrent facilities. ⚠ **No jurisdiction currently imposes
   this.** It is the genuinely hypothetical lever and must be labelled as such rather than presented
   alongside the three real instruments.

- **Operationalising "defer versus desist" (this is what RQ3 actually asks).** Compare **total BNPL
  volume over the full horizon** with and without the cool-off, not just the timing. If volume is
  unchanged and only the timing shifts, agents **defer**. If cumulative volume falls, they
  **desist**. This gives RQ3 a direct, unambiguous answer rather than a narrative one.

---

## Part D. Environment and scheduling

### D15. Macro environment
- **Governs:** whether anything outside the household and lender moves during a run.
- **Already decided (Set 7):** homogeneous, exogenous, held in 2017 terms.
- **DECISION. Fully static. No macro variable varies within a run.** The 2017 repurchase rate of
  7.00% is held constant, so the NCA maximum prescribed rates feeding D6 servicing are constant too.
- *Why, and this is a design consequence rather than a literature question:* the counterfactual
  design (OVERVIEW §1a) exists to isolate the effect of injecting BNPL. **Any macro time-variation
  would confound the injection effect with a macro effect and destroy the experimental control.**
  A moving interest rate or unemployment path would make it impossible to attribute a change in
  default to BNPL rather than to the macro path.
- *Deliberate divergence from the anchors:* both `[cardaci2018inequality]` and `[madeira2018chile]`
  carry macro dynamics, because both are asking macro questions. This thesis is asking a
  product-level question over a 24-month horizon, so the macro layer is held fixed on purpose. Say
  this explicitly rather than letting it look like an omission.
- **Parameters:** none. This is a control, not a knob.
- **⚠ Limitation:** no business cycle, so the model cannot speak to how BNPL stress interacts with a
  downturn. Given that BNPL grew in South Africa through a period of rising rates, that interaction
  is plausibly important and is named as future work.

### D16. Scheduling and activation order
- **Governs:** the order in which households act within a tick. A known ODD design concept.
- **Already decided (Set 7):** synchronous biweekly clock, households act, then the lender processes,
  then state updates.
- **Anchors:** `[ANCHOR: ABM]` Comer & Loerch `[comer2013activation]`, who replicate a
  well-documented civil-violence model and find **statistically significant differences in emergent
  population behaviour** across uniform, synchronous and random activation; and Alizadeh &
  Cioffi-Revilla `[alizadeh2015activation]`, who compare four regimes in an opinion-dynamics model
  and find that **different regimes produce different results, with no scheme dominating**.

- **DECISION. Random asynchronous activation of households within a tick, reseeded every tick.**
  The lender processes applications only after all households have acted.
- *Why random rather than uniform:* under a fixed order the same households would hold first claim
  on a scarce resource every single tick, and credit here **is** scarce, being rationed by the D9
  affordability gate and by per-platform limits (D11). Uniform activation would manufacture a
  persistent, purely artefactual advantage for households early in the ordering.

- **⚠ The peer channel is activation-order independent by construction, and this is a payoff of an
  earlier decision.** D17 reads the reference-group adoption share **lagged one tick**. Every
  household in a tick therefore sees the same, already-settled share, regardless of when it acts.
  The model's principal new interaction consequently does **not** inherit the activation-order
  sensitivity that `[comer2013activation]` and `[alizadeh2015activation]` warn about. Had the peer
  share been read live within the tick, results would have depended on activation order and the two
  decisions would have become entangled.
- **Sensitivity (mandatory, not optional).** Following `[comer2013activation]` directly, re-run
  under uniform and under fully synchronous activation. Any material movement in results is reported
  as activation-order sensitivity. Given that the literature says this matters and the model has a
  positive feedback loop, asserting robustness without testing it would not be defensible.
- **Validation hook:** none directly. This is a robustness dimension rather than a fitted quantity.

---

## Part F. Social structure

### D17. Peer influence and the reference group
- **Governs:** whether households influence one another at all. Without this the model has no
  agent-to-agent interaction, which makes it closer to a dynamic microsimulation than an ABM, and
  more seriously leaves **RQ2 asking for a non-linear threshold the topology cannot produce**:
  with independent households, population default is close to a smooth function of BNPL access,
  because thresholds are products of feedback.
- **Anchors (all three roles covered):**
  - `[ANCHOR: BNPL]` **domain.** Ackert et al. `[ackert2025bnpl]`: consumers chose BNPL over a
    credit-card loan for the same purchase and expected their social networks to approve. BNPL
    uptake specifically is norm-driven.
  - `[ANCHOR: ABM]` **method.** Cardaci `[cardaci2018inequality]`, already this thesis's primary ABM
    anchor, models **peer effects and expenditure cascades** as a central mechanism, generating a
    debt-financed consumption boom and an endogenous banking crisis. Adding a peer channel moves the
    model *closer* to its anchor. The no-interaction design was the deviation needing defence.
  - `[ANCHOR: BEHAV]` **mechanism.** Granovetter `[granovetter1978threshold]`: share-dependent
    adoption with heterogeneous thresholds produces discontinuous aggregate outcomes. This is the
    canonical account of how individual-level rules generate population-level tipping.

- **DECISION (reference group).** `g(i) = (income_quintile_i, province_i)`. This is the **same cell
  already used for the FinScope donor match**, so no new construct enters the thesis. Verified
  against `data/processed/synthetic_population_5000.parquet`: **45 groups, min 23 agents, median 84,
  max 353, none below 20.** Groups are fixed at initialisation and static, consistent with static
  household composition (decision.md Set 2).
  - *Why not province alone:* 9 groups with less noise, but it drops income homophily, so a Q1
    household would treat Q5 households as peers.
  - *Why not an explicit contact network:* no South African data exists to calibrate degree or
    clustering, so it would add several free parameters. Recorded as future work.
  - ⚠ Three Northern Cape cells sit between 23 and 31 agents, so their peer share is noise-prone.
    Report Northern Cape separately, or pool it, in any group-level result.

- **DECISION (mechanism).** Let `s_g(t-1)` be the share of households in group `g` holding a
  non-zero BNPL balance at the end of the previous tick. Then

  ```
  q_i(t) = clip( q_base + beta * s_g(i)(t-1),  0, 1 )
  ```

  The one-tick lag keeps the synchronous update well defined.
  - **`q_base > 0` is structurally required.** With `s_g(0) = 0` everywhere and a purely
    multiplicative rule, adoption could never start. `q_base` is the spontaneous-adoption term and
    `beta` the imitation term, exactly the innovation and imitation coefficients of Bass diffusion.
  - **`beta = 0` recovers the pre-D17 independent-agent model exactly.**

- **Parameters:** `q_base` and `beta` are both **NOT SOURCED**. No South African data fixes either.
  Both are swept, and `beta` is the primary experimental axis rather than a nuisance parameter
  (see below).

- **⚠ The circularity risk, and how it is handled.** D17 is being added partly because RQ2 wants
  non-linearity. Reporting non-linearity as a finding would then be circular. **`beta = 0` is the
  control arm.** All RQ2 output is reported as a surface over (BNPL access rate × `beta`), with the
  `beta = 0` row shown. The claim then becomes:

  > Population default responds non-linearly to BNPL access **only when social transmission is
  > present**; without it the response is smooth.

  That is stronger than "a threshold exists", and it converts an uncalibrated parameter into the
  experimental variable. **Whether a sharp threshold emerges is left as an empirical question of the
  model, not an assumption.** Linear coupling produces diffusion; whether that plus the affordability
  gate (D9) and arrears accrual (D6) yields a *sharp* default threshold is not presupposed.
  Granovetter-style heterogeneous thresholds are **pre-registered now** as the structural robustness
  check should the linear form give only a smooth response.

- **Consequence for RQ1.** The model now holds two distinct self-reinforcing loops: a **financial**
  one (borrow to service existing debt, D0 step 5) and a **social** one (adopt because peers
  adopted). Running `beta = 0` isolates the financial loop, so RQ1 can be answered for each
  mechanism separately. Distinguishing them is a genuine analytical contribution.

- **Baseline safety.** With BNPL disabled, `s_g` is identically zero, so **the peer channel is inert
  in the baseline**. The CCMR 2017 calibration (`data/config/ccmr_2017_baseline.json`) is
  mathematically untouched and needs no re-verification.

- **Validation hook.** Not a validation target: no South African household-level BNPL adoption time
  series exists to fit an S-curve against. The adoption path is reported descriptively, and the
  `beta = 0` versus `beta > 0` contrast is the experiment. The four patterns in OVERVIEW §7 are
  unaffected, since all four are evaluated at the baseline or on traditional-credit outcomes.

- **Deliberately excluded.** Peer effects on **consumption** (Cardaci's actual expenditure-cascade
  mechanism) are not implemented: they would add further uncalibrated parameters and, critically,
  would make the baseline **non-inert**, requiring the CCMR calibration to be re-verified. Recorded
  as the natural extension. **Distress contagion** (peer distress suppressing adoption) is rejected
  because the suppression effect has no literature anchor, and the model already carries one uncited
  rule in D4.

---

## Part E. Calibration & experiment knobs (tie rules → research questions)

| RQ | Mechanism it tests | Rules involved | Swept parameter(s) |
| -- | ------------------ | -------------- | ------------------ |
| RQ1: when does stacking self-reinforce? | two loops: **financial** (borrow to service) and **social** (adopt because peers adopted) | D5, D6, D12, **D17** | stacking depth, BNPL-first propensity, **`beta`** |
| RQ2: non-linear default threshold | population default vs BNPL access, amplified by social transmission | D3, D7, D11, **D17** | BNPL access rate × **`beta`** (2-D surface) |
| RQ3: do cool-off periods work? | **defer vs desist, measured as total BNPL volume over the horizon, not timing** | D3, D14 | cool-off length `k_cool` (0 to 4 ticks; **1 tick = the CCA s.66A 14-day statutory figure**), and each lever on/off |

**`beta = 0` is the control arm for RQ1 and RQ2.** It recovers the independent-agent model exactly,
isolating the financial loop in RQ1 and providing the no-social-transmission comparison in RQ2.
See D17 for why this matters methodologically.

**Validation targets:** four external targets, listed in OVERVIEW §7. The baseline (no-BNPL) arrears
profile targets the **2017-Q1 CCMR** (`data/config/ccmr_2017_baseline.json`): 71.63% current,
16.54% 60+ days, 14.21% 90+ days, account basis. All four are unaffected by D17, since the peer
channel is inert in the baseline. See [[behavioural-validation-hedge]].

---

## Open-decision checklist (fill as research lands)

- [x] D0 tick order · [x] D1 income/shock · [x] D2 consumption · [x] D3 borrow trigger
- [~] D4 borrow amount *(assumption, no anchor)* · [x] D5 lender choice · [x] D6 repayment/arrears · [x] D7 default def.
- [x] D8 heterogeneity · [x] D9 credit gate · [x] D10 info asymmetry · [x] D11 BNPL eligibility
- [x] D12 stacking · [x] D13 BNPL repayment · [x] D14 interventions · [x] D15 macro · [x] D16 scheduling
- [x] D17 peer influence / reference group

**All 18 decisions are closed.** Two carry explicit caveats rather than clean anchors: **D4**
(borrowing amount) is closed *by assumption* with no anchor found, and **D14 lever 4** (stacking cap)
has no real-world instrument and is labelled hypothetical. Every other rule carries a citation,
parameters with sources or sweep flags, and a validation hook.

Each box closes only when it has: a stated rule, a citation, parameters with sources, and a
validation hook.
