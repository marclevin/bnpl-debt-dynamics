# DECISIONS — every choice made, and why

**One of three working documents.** [`DECISIONS.md`](DECISIONS.md) is *what was chosen and why*.
[`DEFECTS.md`](DEFECTS.md) is *what is wrong or was wrong*. [`PLAN.md`](PLAN.md) is *what happens
next*. Consolidated 2026-08-13 from nine overlapping files.

Canonical strategy: [`../OVERVIEW.md`](../OVERVIEW.md).
Plain-language explanation of the whole project: [`../THESIS_GUIDE.md`](../THESIS_GUIDE.md).
Data → agent mapping: [`../household_agent.md`](../household_agent.md).

---

## Contents

**New to this document? Read Part II first** — it explains where the households came from, which is
what Part I's rules then operate on.

| | |
| --- | --- |
| **Part I** | **The eighteen model decision rules (D0–D17)** — one rule per agent behaviour, each with a stated choice, a citation, parameters, and a validation hook |
| **Part II** | **The data layer** — how 5,000 households were built from two surveys: the design commitments, the matching procedure, and the column-by-column variable map |

**The three rules that carry the thesis**, if you read nothing else: **D9** (the Regulation 23A
affordability gate), **D10** (BNPL is invisible to the credit bureau — the whole mechanism), and
**D17** (peer influence, and the `beta = 0` control arm that keeps RQ2 non-circular).

---

# PART I — The eighteen model decision rules

**Status:** **all 18 decisions (D0 to D17) are closed and cited** (2026-08-05). Each closed rule
carries a stated choice, a citation, parameters with sources or explicit sensitivity flags, and a
validation hook. D4 is closed **by assumption**, with no anchor found, and is flagged as such.

> **The contract this file enforces.** Every behavioural rule in the ABM must, before it is coded,
> have (a) a stated choice and (b) at least one cited precedent, whether an ABM paper, a BNPL or
> credit study, or a behavioural-economics finding, so the methodology can say *"we adopt X, following [cite],
> because …"* rather than *"we assumed X."* A rule with no anchor is a flagged limitation, not a
> silent guess.

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
  uses `income_source`, which the data layer already carries. The shock hits **income**, not savings.
- **REVISED 2026-08-12: the shock is PERSISTENT, not single-tick.** The original rule said
  "non-persistent (single tick) in the baseline". Implementation showed that rule cannot work, and
  re-reading the anchor showed it was never right:
  - **It contradicts the anchor.** Madeira models *flows into and out of unemployment*. An
    unemployment spell is not a one-fortnight blip.
  - **It contradicts the data now in the repo.** QLFS 2017 Q3→Q4: **68.4% of the unemployed remained
    unemployed** the following quarter, and only 11.6% moved into employment. South African
    unemployment is highly persistent.
  - **It makes D1's own calibration mandate impossible.** Measured directly: with a single-tick
    shock, sweeping `p` from 0 to 0.40 moves the 90+ arrears rate only from **1.13% to 1.47%**
    against a **14.21%** target. `p` cannot carry a validation it cannot move. With persistence the
    same sweep spans **4.0% to 16.8%** and brackets the target.
  - **Mechanism.** A one-tick wage loss is absorbed by savings or refinanced through the D9 gate,
    which is computed on income that has not yet fallen. A *spell* exhausts the buffer (median
    liquid savings is **R90**), collapses the income the Reg 23A test is computed on, and so closes
    the borrowing escape route. Arrears then age through the CCMR bands instead of clearing.
  - **Exit hazard is sourced, not assumed:** QLFS 2017 unemployed→employed of 11.6% per quarter =
    **1.87% per tick** (`shock_exit_prob`).
  - `shock_persistent = False` recovers the original single-tick rule exactly and is retained as a
    **robustness arm**, so the revision is testable rather than asserted.
  - Consequence: `p` is now unambiguously an **onset hazard**, directly comparable to the QLFS
    employed→unemployed rate. The comparison below is therefore like-for-like, which it was not
    before.
- **MAGNITUDE: SOURCED 2026-08-12. It is no longer a free parameter.** Re-reading the anchor closed
  this. Madeira does **not** model an abstract fractional income cut; he simulates *flows into and
  out of unemployment* alongside permanent and temporary wage shocks. Following the anchor properly
  means the shock is a **separation from employment**, so its magnitude is the household's **wage
  component**, which is observed rather than chosen:
  - `w5_hhwage` is present in `data/raw/NIDS_W5/hhderived.csv` (alongside `w5_hhgovt` and
    `w5_hhremitt`), so every household's wage share of income is in the data.
  - A shocked household loses its wage component for one tick. Grant and remittance income is
    untouched, which makes D1's existing WAGE/GRANT conditioning quantitative instead of categorical.
  - **No data-pipeline rebuild.** `source_w5_hhid` is already a column on
    `synthetic_population_5000.parquet`, so `w5_hhwage` joins straight onto the validated
    population. P1 to P3 are not re-run and the 14/14 validation is untouched.
  - **Join verified against the 5,000-agent parquet (2026-08-12):** 5,000 of 5,000 rows matched,
    **0 unmatched**; the joined `w5_hhincome` reproduces the backbone value exactly, which confirms
    the key; and **0 households have wage income exceeding total income**, so no clipping is needed.
  - **Wage share of income, observed:** WAGE-dominant households (n=2,892) have a mean share of
    **0.80** and a median of **0.845**, so a separation removes roughly four-fifths of their income.
    That is both larger and far better grounded than the 0.5 the earlier draft would have assumed.
  - **On the 1,811 null `w5_hhwage` values:** all fall outside the WAGE group — **zero WAGE-dominant
    households have null or zero wage income** — so mapping null to 0 is safe and does not silently
    exempt anyone who should be shocked. GRANT and OTHER households carry small residual wage shares
    (mean 0.054 and 0.024) but are exempt from the labour shock by this rule anyway.
  - Consequence: the magnitude sweep is **withdrawn**. There is nothing left to sweep.
- **Parameters:** `p` (shock probability per tick) remains **NOT SOURCED**, deliberately. NIDS W5 is
  a single wave in this design, so within-household income volatility cannot be estimated from it.
- **Treatment:** `p` is promoted from assumption to **calibration target**. It is fitted so the
  baseline (no-BNPL) arrears rate reproduces the CCMR benchmark, then held fixed for all BNPL runs.
- **NEW: `p` now carries an external plausibility check (2026-08-12).** Stats SA *Labour Market
  Dynamics in South Africa, 2022* (Report 02-11-02) publishes the QLFS panel for **2017 to 2022**,
  so a **vintage-matched 2017 figure** exists. Extracted by
  `notebooks/scripts/extract_qlfs_lmd.py` to `data/config/qlfs_2017_labour_flows.json`.
  **Q3:2017 → Q4:2017, individual basis:** 93.14% retained employment, **3.53% moved to
  unemployment**, 3.32% moved to not-economically-active, so **6.86% left employment**. Converted to
  the 14-day tick this is a hazard band of **0.54% to 1.17% per tick** (narrow to broad measure).
  - The fitted `p` is reported **against** this band. It is **not fitted to it**: fitting `p` to both
    CCMR arrears and the QLFS band would over-determine the baseline.
  - ⚠ **Unit mismatch (state it).** QLFS counts **individuals**; the model shocks a **household**.
    A multi-earner household faces a higher probability that at least one earner separates, so the
    household hazard sits at or above the individual rate. Same treatment as the
    account-versus-household mismatch on the CCMR target (D6).
  - ⚠ The model shock is non-persistent (one tick) while a QLFS separation may persist for quarters,
    so the band bounds the rate of shock **onset**, not the stock of unemployed households.
- **Validation hook:** this is the parameter that *carries* the validation. Because `p` is fitted to
  baseline arrears, the baseline is calibrated rather than validated, and only the BNPL-on results
  are genuine predictions. **State this explicitly in the limitations chapter.** The QLFS band does
  not change that, but it does mean the fitted value is no longer wholly unconstrained: a fitted `p`
  falling far outside 0.54% to 1.17% per tick is evidence the shock process is carrying stress the
  rest of the model should be generating. Report the comparison either way.

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
- **PARTIAL UPDATE 2026-08-12: the BNPL purchase *level* now has an anchor.** The *rule* stays
  closed-by-assumption, but the number it produces no longer has to be invented:
  - **South African average BNPL basket ≈ R1,568.** ⚠ Trade press, not a provider disclosure or a
    regulator statistic, and at current vintage against a 2017 population. Weak, but SA-specific,
    and it falls under Part C's existing vintage note.
  - **Cross-check, strong but foreign:** CFPB reports an **average BNPL loan of $135** and **$848
    per user per lender per year across 6.3 loans** `[cfpb2025market]`.
  - Purchase size is centred on the SA basket figure and swept. This narrows the gap; it does not
    close it, and D4 remains the model's one uncited rule.
- **This is a flagged limitation, not a cited rule.** It must appear in the limitations chapter as
  an uncited modelling choice.

- **⚠ SUPERSEDED 2026-08-12 (QA pass). The BNPL purchase level is no longer a flat national
  constant, and it is no longer the trade press.** The partial update above fixed the *number* and
  left the *specification error*: a single purchase size imposed on every household. Measured on the
  model's own banked population, R1,568 was **127% of the median Q1 household's monthly
  discretionary budget and 11.4% of Q5's**. A population with a Gini of 0.67 cannot share one
  purchase size, and the flat constant is a large part of why purchase size topped the sensitivity
  ranking (DEFECTS.md **B24**, **B30**).

  **REVISED DECISION.** A BNPL purchase is drawn lognormally about **`kappa ×` the household's own
  monthly discretionary expenditure**, so its mean is that product and the observed heterogeneity of
  the population is inherited rather than averaged away.

  - **`kappa = 0.1387` is DERIVED, not chosen** — the share of household discretionary spending that
    goes on the categories BNPL actually finances (clothing and footwear, furniture and appliances,
    ICT devices, recreational durables), computed from Stats SA **IES 2022/23** COICOP microdata
    `[statssa_ies_2023]`. Only a **ratio** is taken from that survey, never a money amount, so the
    2022/23 vintage cannot contaminate a 2017-Rand model — the identical argument already accepted
    for the FinScope 2019 categorical flags.
  - **Interpretation of the rule:** a BNPL purchase is the scale of **one month** of the household's
    own spending in the categories BNPL finances. The "one month" lumpiness is the assumption; it is
    single and interpretable, and the evidence for it is that it independently reproduces the
    provider figure below.
  - **THE LEVEL IS NOW A CHECK, NOT AN INPUT.** The population mean purchase is validated against an
    average order value **derived from a listed issuer's disclosed aggregates** — R13.1bn cumulative
    BNPL GMV over 9.4m transactions `[weaver2025results]`, `[homechoice2024ir]` — giving **R992 in
    2017 Rands**. The superseded trade-press basket deflates to R1,038, so the two independent SA
    sources agree within 4.6%, and the model's drawn mean of R1,029 sits between them. **Nothing is
    fitted to anything.**
  - `[sa_bnpl_basket_2026]` is **demoted from input to corroboration**. A weak source used as a
    check is legitimate; the same source load-bearing was not.
  - **Robustness arm:** `bnpl_purchase_base = "income"` sizes the purchase against monthly income
    instead, which is the base the three regulator figures are expressed against — CFPB US\$135
    `[cfpb2025market]`, ASIC A\$147 `[asic2020rep672]`, Woolard £88–£110 `[woolard2021]`, all near
    2–4% of median monthly household income in their own jurisdictions.
  - **Sensitivity (mandatory):** `kappa` over 0.07–0.28, and both bases.

  **The rule for the shortfall path is unchanged and remains uncited.** D4's status as the model's
  first uncited rule stands; what changed is that its BNPL *level* is now derived and externally
  checked rather than asserted.
- **Sensitivity (mandatory, not optional):** shortfall, shortfall x 1.25, and shortfall plus one
  tick of committed expenditure. If results move materially across these, the model is
  amount-rule-sensitive and the finding must be reported as such.

### D5. Lender choice
- **Governs:** substitution versus complementarity between traditional credit and BNPL. Central to
  RQ2.
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

- **⚠ REVIEWED AND DELIBERATELY LEFT UNCHANGED, 2026-08-13. What BNPL is used for, and the one
  asymmetry that remains.** There are two BNPL paths and they are sized differently:

  | Path | Trigger | Amount |
  | --- | --- | --- |
  | **Want-driven** (D0 step 6) | spontaneous, socially transmitted | `kappa ×` the household's own monthly discretionary budget |
  | **Shortfall-driven** (D0 step 5) | realised shortfall on committed expenditure or debt service | the **full shortfall**, bounded only by the order cap and rolling limit |

  BNPL cannot pay rent directly, and the model does not claim it does. The shortfall path works by
  **liquidity substitution**: the household finances something it was going to buy anyway, pays only
  25% at checkout, and the other 75% stays in its pocket to cover the rent. That is why
  `_seek_credit` returns `financed × 0.75` as net cash rather than the full amount. The same
  mechanism lets a household take BNPL to free cash for *its existing BNPL instalments*, which is
  the financial self-reinforcing loop D0 places borrowing last in order to permit.

  **The asymmetry.** The 2026-08-12 QA pass anchored the *want* path to the household's own budget
  and left the *shortfall* path uncapped. For a median household that permits a draw of up to
  ~4 months of BNPL-financeable spending in a single tick — more liquidity substitution than the
  household could realistically execute, since substitution is bounded by what it would actually buy.

  **Decision: leave it.** Capping the shortfall draw at the same monthly budget would be defensible
  and would reduce BNPL's measured effect, but it is a *design change* to a registered rule, not a
  defect fix, and it would land on the eve of a re-run. Recorded here as a **disclosed limitation**:
  the model is permissive about how much distress BNPL can relieve, which biases its estimated
  effect on default **upward**, and that is the conservative direction for a thesis arguing BNPL
  raises distress. Revisit as future work.

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
- **⚠ GAP FOUND 2026-08-12, during implementation planning: the minimum itself is undefined.** This
  rule fixes the *share* of agents who pay the contractual minimum but never says what the
  contractual minimum *is*, and `[Keys2019]` measures behaviour relative to whatever minimum the US
  card issuer set rather than prescribing a formula. The NCA prescribes maximum rates and the
  Reg 23A affordability test, but **no minimum-payment formula**, so there is no South African
  statutory anchor either.
- **DECISION (assumption, newly surfaced).** Minimum payment =
  `max(interest accrued this tick, 5% of the outstanding balance per month, tick-scaled)`. The
  interest floor prevents negative amortisation by construction; the 5% is an assumption.
- **This is a second uncited rule alongside D4** and must be recorded in the limitations chapter as
  such, not buried in code. **Sensitivity: mandatory**, sweep the 5% over 2.5% to 10%. If the
  minimum-payer arm drives results, the finding is minimum-formula-sensitive and must be reported
  that way.
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
- **REFINED 2026-08-12: which households form the denominator.** The mismatch has a second edge that
  was not previously stated, and it matters more than the first. CCMR accounts are held by
  **credit-active consumers**; in the 5,000-agent population only **44.2% of households hold any
  traditional debt at all**, and a household with no debt can never be in arrears. Comparing an
  all-household arrears rate to an account-level one therefore guarantees an undershoot for a purely
  definitional reason. Measured on the same run: **1.68% of all households** were 90+ against
  **3.80% of credit-active households**, a factor of 2.3 with no behavioural content whatsoever.
  - **The credit-active rate is the closer analogue and is the one compared to CCMR.**
  - **Both are always reported.** The all-household rate remains the correct denominator for the
    *population default rate* the RQs ask about; it is only the CCMR arrears comparison that uses
    the credit-active base. Metrics carry both (`pct_90_plus` and `active_90_plus`).
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
  cannot transact at all. This uses the existing `banked` flag, which caps eligibility at **82.8% of
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
- **⚠ SEARCHED AND NOT FOUND, 2026-08-12. The absence is itself the finding, and is citable.**
  A deliberate search for a published rolling limit returned nothing from either major provider:
  - **Payflex** publishes the R15,000 per-order cap but no rolling limit. Its support material
    states the spend limit is set per customer from credit history and repayment behaviour
    `[payflex_limits]`.
  - **PayJustNow** explicitly declines to publish limits: the limit is set per shopper from
    identity verification and credit profile `[payjustnow_limits]`.

  Neither firm discloses a figure, so this parameter **cannot** be sourced from published terms the
  way D13's Pay-in-4 schedule and late-fee cap were. That is worth stating in the thesis rather than
  papering over with a round number: the opacity of BNPL credit limits is consistent with the
  regulatory position in D10, where the product sits outside the NCA and carries no disclosure or
  reporting obligation.
- **TREATMENT: demoted from a behavioural parameter to a binding-check quantity.** This rule already
  requires verifying that the *order cap* binds rarely; the same test now governs the rolling limit.
  Set it, then measure the share of attempted transactions it blocks. If it rarely binds it is inert
  and the sweep **demonstrates** that, rather than the chosen value mattering. If it binds often,
  that is a reportable result and the parameter is promoted to a headline sensitivity.
- **⚠ Why the vintage problem is mostly moot here:** at LMI household incomes a R15,000 order cap
  will rarely bind. The binding constraint on borrowing size is the purchase amount (D4), not the
  platform cap. Verify empirically once implemented; if the cap binds for more than a few percent of
  transactions, revisit.

- **⚠ REVISED 2026-08-12 (QA pass) on both counts.**

  **The vintage problem was not moot; it was unnoticed.** Every Rand figure in this rule and in D13
  was taken at **current (2026) vintage** and used unadjusted in a model whose every other quantity
  is in **2017 Rands**. SA CPI rose 44% between the 2017 and 2025 annual averages, so the BNPL side
  of the model was denominated ~1.4× too high against the NIDS backbone, the Reg 23A table and the
  CCMR targets. The order cap is now **R9,927** in 2017 Rands, deflated once from a sourced factor
  `[statssa_cpi]` (DEFECTS.md **B29**). It binds on ~2–3% of requests after the change, so the
  "revisit if it exceeds a few percent" trigger above is now live and should be watched in the
  re-run.

  **The rolling limit is now a FUNCTION, not a constant.** The flat R5,000 was **217% of the median
  banked Q1 household's monthly income**, at each of four platforms independently. The absence of a
  published *level* still stands and remains citable as a finding; what does not stand is treating
  that absence as a licence for a flat number, because both providers state the limit is set **per
  customer**, and HomeChoice's audited credit-risk disclosure describes a **"low and grow"** policy
  — first-time customers start with lower limits, increased as they exhibit good repayment behaviour
  `[homechoice2024ir]`. That is an annual report, not a support page, and it licenses a functional
  form.

  **REVISED DECISION.** `rolling_limit_i = lambda × income_monthly_i`, per household rather than per
  platform, with **`lambda = 0.10`** (set 2026-08-13; initially 0.25) and the R9,927 order cap as
  the ceiling.

  **⚠ Why 0.10 and not the middle of the band.** The limit applies at *each* of four platforms
  independently, so what the external evidence actually measures is the **stacked total**. Woolard's
  "relatively easy to accrue around £1,000" of bureau-invisible BNPL debt is a total across all
  providers — roughly **37% of UK median monthly household income** — which is about **0.09 per
  provider across four**. At `lambda = 0.25` the model's stacked total was **1.0× monthly income,
  about 2.7× what Woolard called easy to accrue**. Since cross-provider stacking *is* the thesis's
  subject, and Woolard measures precisely that quantity, the value is set so the model's aggregate
  reproduces the only measurement of it. Afterpay's published initial limit (~8% of Australian
  median monthly income) puts 0.10 at the initial-limit end of the range, which is the conservative
  place for a baseline to sit.

  ⚠ **Consequence to report, not hide:** at `lambda = 0.10` the rolling limit binds on **54% of
  requests** at `beta = 0` (Q1 53%), against 25% at `lambda = 0.25` and 5.6% under the old flat
  R5,000. The limit has gone from a background constraint to a first-order one. That is what the
  Woolard anchor implies, and the 0.1–1.0 sweep is what demonstrates how much it matters.

  - **Income and NOT Reg 23A capacity.** Tempting but wrong: this rule's entire point is that the
    BNPL screen is deliberately *not* the statutory test, and setting BNPL limits from statutory
    capacity would quietly dissolve the asymmetry with D9 that the thesis exists to study. Income is
    what a light automated screen can plausibly infer from bank-card activity.
  - **`lambda` is reported against an external band, not fitted to it** — the same treatment D1's
    shock probability receives against the QLFS band. Woolard's "relatively easy to accrue around
    £1,000" of invisible BNPL debt is a *stacked* total across providers, ~40% of UK median monthly
    household income, so ~10% per provider; Afterpay's published initial and maximum limits are ~8%
    and ~26% of Australian median monthly household income. The band is therefore roughly
    **0.10–0.26**, and `lambda = 0.25` sits at its top.
  - **Binding rates must be reported BY QUINTILE.** A limit that scales with income binds hardest at
    the bottom, so an aggregate rate can read as inert while the constraint bites hard on Q1. First
    measurement after the change: **Q1 35.2% against Q5 21.5%** at β = 0.
  - **Future work, deliberately not built:** the "low and grow" disclosure also licenses a *dynamic*
    limit that rises with repayment history, which is the mechanism by which real households
    accumulate large invisible cross-provider exposure. Recorded rather than implemented — the
    static rule already retires the vulnerability, and adding a dynamic on the eve of a re-run is
    scope the thesis does not need.
- **Validation hook:** share of eligible households ≈ 82.8% by construction; check that the order
  cap binds rarely.

### D12. Multi-platform stacking (RQ2)
- **Governs:** the self-reinforcing debt mechanism. The core of RQ2.
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
  against `data/processed/synthetic_population_5000.parquet`: **45 groups, min 17 agents, median 82,
  max 357, none below 15.** Groups are fixed at initialisation and static, consistent with static
  household composition (decision.md Set 2).
  - *Why not province alone:* 9 groups with less noise, but it drops income homophily, so a Q1
    household would treat Q5 households as peers.
  - *Why not an explicit contact network:* no South African data exists to calibrate degree or
    clustering, so it would add several free parameters. Recorded as future work.
  - ⚠ All five Northern Cape cells sit between 17 and 35 agents, so their peer share is noise-prone.
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

- **Consequence for RQ2.** The model now holds two distinct self-reinforcing loops: a **financial**
  one (borrow to service existing debt, D0 step 5) and a **social** one (adopt because peers
  adopted). Running `beta = 0` isolates the financial loop, so RQ2 can be answered for each
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

- **⚠ IMPLEMENTED 2026-08-13: the pre-registered threshold variant now exists, and the peer signal
  was renormalised.** Two changes, both made *before* the arm was run so neither could be chosen
  after seeing a result.

  **1. `s_g` is measured against the ELIGIBLE subpopulation** (`peer_mechanism` unaffected; see
  DEFECTS **B31**). Counting the unbanked and the ineligible in the denominator capped the signal at
  each group's eligible share, and that ceiling is proportional to `bnpl_access_rate` — which is
  RQ2's own x-axis. Harmless under linear coupling, where it is absorbed into `beta`; fatal under
  thresholds, where a fixed `theta_i` would be compared against a signal whose maximum was being
  swept alongside the axis under test, producing a threshold-shaped response that is partly an
  artefact. Peak `s_g` rises from ~0.53 to **0.96**. ⚠ This rescales `beta`; pre-2026-08-13 linear
  results are not comparable.

  **2. The Granovetter arm.** `peer_mechanism = "threshold"` replaces smooth coupling with a jump:

  ```
  theta_i ~ Normal(mu_theta, sigma_theta)  clamped to [0, 1], fixed for life
  q_i(t) = q_base                          if s_g(t-1) <  theta_i
  q_i(t) = clip(q_base + gamma, 0, 1)      if s_g(t-1) >= theta_i
  ```

  - **`sigma_theta` is the primary axis, `mu_theta` the secondary.** Granovetter's claim is that the
    *variance* of thresholds decides whether a cascade occurs — a distribution with someone standing
    at every level propagates, a clustered one does not, at identical means. Sweeping the mean alone
    would test the wrong quantity.
  - **Clamping, not resampling, is the faithful choice.** The point mass at 0 is Granovetter's
    **instigators**, who act with no peers at all and are what seeds a cascade; the mass at 1 is
    households social influence can never reach. Resampling would delete both.
  - **`gamma = 0` is the control arm** and reproduces the independent-agent model **bitwise**, which
    required drawing `theta_i` from a separate `init_rng` stream so the endowment draw cannot shift
    the simulation's own. That also makes the `sigma_theta` sweep a **paired** comparison: only the
    thresholds change, every shock and purchase draw is identical.

  **What this arm is for, restated.** Not one more attempt to find a threshold. It **separates
  adoption tipping from distress tipping**. The model has peer feedback in its input and none in its
  output (DEFECTS **B1**), so a sharp adoption cascade alongside a linear default response would be
  a much stronger answer to RQ2 than the linear arm can give: the cascade mechanism demonstrably
  works and still does not move the outcome.

---

## Part E. Calibration & experiment knobs (tie rules → research questions)

| RQ | Mechanism it tests | Rules involved | Swept parameter(s) |
| -- | ------------------ | -------------- | ------------------ |
| RQ1: does the population reproduce behaviour it was not fitted to? | the data layer and the calibrated baseline, judged against patterns nothing was fitted to | D0-D2, D6, D9 | none - answered by construction and baseline, not by a sweep |
| RQ2: do households stack facilities no lender sees, and does default rise? | two loops: **financial** (borrow to service) and **social** (adopt because peers adopted), plus population default vs BNPL access | D3, D5, D6, D7, D11, D12, **D17** | stacking depth, BNPL-first propensity, BNPL access rate × **`beta`** (2-D surface) |
| RQ3: do cool-off periods work? | **defer vs desist, measured as total BNPL volume over the horizon, not timing** | D3, D14 | cool-off length `k_cool` (0 to 4 ticks; **1 tick = the CCA s.66A 14-day statutory figure**), and each lever on/off |

**`beta` is the RQ2 experimental axis and the RQ3 toggle.** It is the strength of peer influence on
BNPL adoption, so sweeping it is what makes social transmission visible at all in RQ2; it is then
switched on and off under RQ3, because the cool-off lever only bites where `beta > 0`. **`beta = 0`
is the control arm and is always reported.** It recovers the independent-agent model exactly,
isolating the financial loop from the social one.
See D17 for why this matters methodologically.

**Validation targets:** four external targets, listed in OVERVIEW §7. The baseline (no-BNPL) arrears
profile targets the **2017-Q1 CCMR** (`data/config/ccmr_2017_baseline.json`): 71.63% current,
16.54% 60+ days, 14.21% 90+ days, account basis. All four are unaffected by D17, since the peer
channel is inert in the baseline. See [[behavioural-validation-hedge]].

**Plus one calibration cross-check (2026-08-12), which is not a fifth target.** The fitted `p` is
reported against the QLFS 2017 job-separation band in
`data/config/qlfs_2017_labour_flows.json` (**0.54% to 1.17% per tick**). This checks the
*calibration* rather than the model output, so it does not join the four validation targets; it
constrains the one parameter that carries them. See D1.

---

## Open-decision checklist (fill as research lands)

- [x] D0 tick order · [x] D1 income/shock · [x] D2 consumption · [x] D3 borrow trigger
- [~] D4 borrow amount *(assumption, no anchor)* · [x] D5 lender choice · [x] D6 repayment/arrears · [x] D7 default def.
- [x] D8 heterogeneity · [x] D9 credit gate · [x] D10 info asymmetry · [x] D11 BNPL eligibility
- [x] D12 stacking · [x] D13 BNPL repayment · [x] D14 interventions · [x] D15 macro · [x] D16 scheduling
- [x] D17 peer influence / reference group

**All 18 decisions are closed.** Four carry explicit caveats rather than clean anchors:

- **D4** (borrowing amount) is closed *by assumption* with no anchor for the *shortfall* rule. Its
  BNPL *level* is now **DERIVED** (2026-08-12 QA pass): purchases are `kappa ×` the household's own
  discretionary budget, `kappa` computed from Stats SA IES 2022/23, and the level is validated
  against a listed-issuer disclosure rather than set by trade press.
- **D6** (minimum-payment formula) was found undefined on 2026-08-12 during implementation planning.
  Now closed by assumption, with mandatory sensitivity. **This is the model's second uncited rule.**
- **D11** (rolling available balance) was searched on 2026-08-12 and **no published figure exists**
  for either major SA provider. The absence stands for the *level*; it does not stand for the
  *form*. The limit is now `lambda ×` monthly income per household, reported against a Woolard/ASIC
  band, with the functional form licensed by HomeChoice's audited "low and grow" disclosure.
- **⚠ Vintage** (2026-08-12): every BNPL Rand figure in D4, D11 and D13 was nominal at current
  vintage in a 2017-Rand model, and is now deflated once from a sourced CPI factor. See DEFECTS.md
  **B29** — the fourth case of implementation falsifying a specification that read as complete.
- **D14 lever 4** (stacking cap) has no real-world instrument and is labelled hypothetical.

Every other rule carries a citation, parameters with sources or sweep flags, and a validation hook.

**Resolved on 2026-08-12:** the D1 income-shock **magnitude**, which was `NOT SOURCED`, is now
data-driven from `w5_hhwage` and carries no free parameter at all; and the fitted `p` gained an
external plausibility band from the QLFS 2017 panel.

Each box closes only when it has: a stated rule, a citation, parameters with sources, and a
validation hook.

---
---

# PART II — The data layer: how 5,000 households were built

Merged 2026-08-13 from `decision.md` (design commitments), `DECISIONS.md` (the matching
procedure) and `DECISIONS.md` (the column map). Those three files are deleted; this is their
content.

**In one line:** every household in the model is a real NIDS Wave 5 household from 2017, given
financial-inclusion flags borrowed from a similar FinScope respondent, and drawn 5,000 times in
proportion to how many real households it represents.

## II.0 The claim: a counterfactual injection, not a historical fit

The model is a **counterfactual experiment**. A 2017 population is calibrated against the 2017-Q1
CCMR, and a BNPL lender class is then **injected** into that calibrated economy.

*Why 2017 is the right control:* BNPL reached the South African market at scale from roughly 2021.
Fitting to its actual arrival would require disentangling it from COVID-19 income shocks, the 2020
credit contraction and post-pandemic inflation. **The absence of BNPL in 2017 is the experimental
control**, and it is what makes the injection interpretable.

*What this forbids:* no claim about any actual year after 2017, and no comparison to post-2020
observed arrears. Results are directional and mechanistic, never forecasts.

## II.1 The eight design commitments

| Set | Commitment |
| --- | --- |
| 1. Temporal | **2017 only**, 14-day ticks, 24-month horizon (52 ticks), 12-tick burn-in. **No CPI forwarding of the population.** |
| 2. Population | 5,000 households, province as a match cell, NIDS household definition, composition static across the horizon |
| 3. Sources | NIDS W5 backbone + FinScope 2019 donor |
| 4. Variables | Behavioural state (drives decisions) vs conditioning (profiles results); all money in 2017 Rands |
| 5. Matching | **Simple cell-donor by income quintile x province**; categorical flags only |
| 6. Agents | Households + one traditional lender stub + 4 BNPL platforms; multiple *traditional* lenders deferred |
| 7. Topology | Bipartite household/lender, **plus** peer influence on BNPL adoption (D17); static income + per-earner shock |
| 8. Validation | Internal (~5%) + match diagnostics + four external targets |

**Why 2017-only.** CPI-forwarding NIDS to 2022 would have introduced a second reference year,
distributional assumptions, and external validation targets that could not be defended. Staying in
2017 removes all three at once.

⚠ **This commitment was later broken on the BNPL side and had to be repaired** — the BNPL
parameters were taken at current vintage and used unadjusted. See DEFECTS **B29**. The population
itself was never affected.

## II.2 The matching procedure (NIDS receives, FinScope donates)

Deliberately simple ("ignorant") matching: transparent and easy to defend, not a precision fusion.
NIDS is the backbone that is kept; FinScope only lends its financial-inclusion flags.

**The match cell.** Both surveys are bucketed into the *same* cells, then donors drawn within cell:

1. **Per-capita income quintile.** NIDS bounds R900 / R1,801 / R3,400 / R7,712. FinScope per-capita
   income = `M13_MHI_Imputed` band midpoint divided by `Number_in_HH`, bucketed on the **NIDS**
   bounds so the edges are identical. Band midpoints: No Income to 0, R1-999 to 500, R1,000-2,999
   to 2,000, R3,000-7,999 to 5,500, R8,000-11,999 to 10,000, R12,000-29,999 to 21,000, R30,000+ to
   40,000.
2. **By province.** Names align exactly across surveys. 45 cells, **min 30 donors, none below 20**,
   so the province split is used directly with no fallback needed in practice.
3. **Fallback** to quintile-only for any thin cell (logged; not triggered).

**Donor draw.** For each NIDS household, draw one FinScope respondent from its cell (weighted by
`HH_WEIGHT16`, with replacement) and copy its flags.

**Why cell-donor and not hot-deck or regression fusion:** transparent, easy to explain to an
examiner, and it avoids over-claiming precision that the 2017-to-2019 vintage gap cannot support.

**What it does NOT do:** preserve household-level joint structure beyond quintile x province;
correct the vintage gap; or measure servicing from data.

## II.3 The one number that had to be constructed

> **CORRECTED 2026-08-18.** The claim below that neither survey records a repayment amount was
> **wrong**. The NIDS W5 household questionnaire measures monthly repayments directly for two
> product classes in its non-food expenditure module: `w5_h_nfhpspn` (e2_2_30, hire purchase,
> 243 payers, median R620/month) and `w5_h_nfclthaspn` (e2_2_33, clothing store accounts, 1,044
> payers, median R455/month). 1,219 households (8.9%) report one or both. These are the same
> households, survey and vintage as the backbone. Servicing is still *derived* by amortisation,
> because the measurement covers only two of five product classes, but the repayment horizons
> are no longer assumptions -- see the revised term table below and `data/config/README.md`.

NIDS records a debt **stock** and the model needs a monthly **flow**, so servicing is *derived*:

```
weighted_apr, weighted_term = mix over the donor's held products (G10-G14)
                              using data/config/credit_rate_table.csv
monthly_trad_repayment      = amortize(D_trad, weighted_apr, weighted_term)
```

APRs are the **NCA statutory maximum prescribed rates** per sub-sector (regime in force 6 May 2016,
so valid for 2017), at the **2017 repo rate of 7.00%**: credit facilities 21%, other credit
agreements 24%, unsecured 28%, short-term 5% per month. ⚠ These are **ceilings, not observed
averages**, which biases servicing upward — a stated limitation.

**Two guards**, because a NIDS debt *stock* is paired with a FinScope product *type* drawn
independently within the cell, so naive amortisation could force impossible debt service:

- `MIN_TERM_MONTHS = 1.0` (was 6). The old 6-month floor was never sourced and **never bound**:
  the shortest term in the rate table was itself 6, so `max(term_raw, 6) == term_raw` for every
  household. With the terms now sourced it *would* bind, overriding the 1-month short-term loan
  for 1.1% of donors, so it is reduced to a numerical guard against a zero or negative term.
  The affordability guard is Reg 23A, which is sourced and does bind.
- **Repayment horizons, sourced 2026-08-18.** store card 11m and hire purchase 8m measured
  directly in NIDS (balance / observed payment, n=782 and n=121); personal loan and unflagged
  balances 25m from the CCMR 2017-Q1 stock-flow implied life of the unsecured book (24.8m,
  cross-checked against Table 5.2 origination terms at 28m); short-term loan 1m from the
  FinScope G13 wording ("repayable within 31 days") and CCMR Table 6.2 (65.8% at <=1 month).
  Only revolving credit remains underived, and it is tied to `min_payment_frac`, already swept.
  Two old values were materially wrong: hire purchase at 36m implied a third of the observed
  payment, and short-term at 6m came from the NCA statutory ceiling, not the product surveyed.
  Mean applied horizon moves 21.95 -> 21.45 months, so the centre barely shifts; the tails do.
- **Servicing now has external validation targets.** NIDS observed DSTI among the 1,219 payers:
  median 5.36%, mean 11.19%. FinScope C8 (21-matchstick budget game), categories 5 and 9, among
  holders of >=1 modelled product: 9.78% of monthly spending. Model DSTI by quintile 2.8-6.1%.
- **OPEN: debt service is double-counted.** e2_2_30 and e2_2_33 are components of NIDS non-food
  expenditure (sum of all 54 E2 components / `w5_expnf` has median ratio 1.04), so
  `expenditure_discretionary` already contains them (median 12.6% of non-food spend for payers)
  and the model deducts derived servicing on top. `w5_h_nfcarspn` too. Not yet fixed.
- **NCA Regulation 23A(9) residual-income ceiling.** Replaced an earlier flat `MAX_DSTI = 0.65`,
  which had no statutory basis. Debt service is capped at gross income minus Reg 23A necessary
  expenses, giving an **income-varying** ceiling: 10.4% of income at R900/month rising to 83.2% at
  R7,712/month.

Result: max DSTI 0.911, **zero** households repaying more than income, weighted-mean DSTI by
quintile 2.8-6.1%. The guard binds for only **3.4% of debtors** (158 of 4,702).

**Diagnostic kept as a finding, not capped away:** 53 debtor households have income at or below the
Reg 23A norm, so **no NCA-compliant lender could lawfully have granted their debt**. 33 survive into
the 5,000-agent resample, all in Q1.

## II.4 Variable map

All monetary values in **2017 Rands, no CPI**. Backbone: `data/raw/NIDS_W5/hhderived.csv`. Donor:
`data/raw/FINMARK_2019/Finscope South Africa 2019.csv`.

### Behavioural state, from NIDS

| Field | Description | NIDS column(s) | Derivation |
| --- | --- | --- | --- |
| `income_monthly` | Total monthly household income | `w5_hhincome` | Direct |
| `income_source` | Dominant source: WAGE / GRANT / OTHER | `w5_hhwage`, `w5_hhgovt`, `w5_hhremitt`, `w5_hhother`, `w5_hhagric`, `w5_hhinvest` | Largest component wins |
| `expenditure_total` | Total monthly **cash** expenditure | `w5_expf`, `w5_expnf`, `w5_rentexpend` | committed + discretionary; excludes imputed rentals |
| `expenditure_committed` | Non-discretionary (food + rent paid) | `w5_expf`, `w5_rentexpend` | food + rent |
| `expenditure_discretionary` | Flexible spending | `w5_expnf` | non-food; rent is a separate NIDS component, so it is not subtracted |
| `liquid_savings` | Cash buffer | `w5_f_ass` | Financial assets as proxy, winsorised at 1st/99th pct. **Weakest field in the layer** |
| `D_trad` | Consolidated traditional debt | `w5_f_deb` | Financial debts |
| `monthly_trad_repayment` | Monthly servicing | constructed | See II.3 |

Two further columns were joined later, for the model rather than the population: `w5_hhwage` (the
wage component, which is the income-shock magnitude under D1) and an employed-member count from the
NIDS individual file (`n_earners`, which makes the shock a per-earner hazard).

### Behavioural state, from FinScope (categorical, no deflation)

| Field | Rule | National rate |
| --- | --- | --- |
| `banked` | `F1 == "Yes"` | 82.4% |
| `credit_access_formal` | `G5` in {Bank, Retail store, Micro finance, Insurance} **OR** any of `G10`-`G14` == Yes (lay-by `G15` excluded: not credit) | 26.4% |
| `informal_finance` | `G5` in {Mashonisa, Stokvel/burial, Friends/family, Colleagues, Employer advance} | 9.1% |
| `savings_product` | `K7` is a valid Rand band | 49.9% |

`banked` is the one that matters most: BNPL requires a bank card, so it caps BNPL eligibility at
**82.8%** of the resampled population.

### Conditioning, from NIDS

`income_quintile` (primary grouping **and** match cell), `household_size`, `household_composition`,
`dependency_ratio`, and head demographics: `age_head`, `gender_head`, `race_head`, `education_head`,
`education_band`.

### Sampling fields, not agent attributes

`w5_wgt` (post-stratified household weight, used as the resampling probability), `w5_hhid` (record
key for joins, not carried into the ABM).

## II.5 Validation of the data layer

- **National marginals** reproduce FinScope national rates: banked +0.4, credit +2.3, informal +0.1,
  savings +1.8 (pp).
- **Cell marginals** match by construction (correctness check).
- **14 checks in P4, all passing**, including the Gini check: 0.651 weighted per-capita on the
  10,841-household backbone against 0.667 unweighted on the 5,000-agent resample, a 0.015 gap
  against a 0.02 tolerance.

## II.6 Known limitations of the data layer

- **2017 reference year.** Not forwarded to a current year. Deliberate, and stated up front.
- **FinScope 2019 as a 2017 proxy.** Two-year vintage gap on categorical flags, uncorrected.
- **Cell-donor matching is crude:** preserves cell-level marginals, not household-level joint
  structure beyond quintile x province.
- **`liquid_savings` is the weakest NIDS field**, proxied by financial assets — and pattern 4
  validates against it, which needs saying out loud (DEFECTS B11).
- **Committed/discretionary split is approximate:** NIDS gives only food / non-food / rent, so
  "discretionary" carries transport, utilities and education, none of which is truly discretionary.
- **Reg 23A is a per-consumer test applied to a household**, because the agent is a household.
- No informal credit supply, no spatial heterogeneity beyond the match cell, static household
  composition, one static lender rule.
- **Social structure is minimal, not absent.** Households interact only through the D17 reference
  group and only on BNPL adoption. Three Northern Cape groups hold 23-31 agents, so their peer share
  is noise-prone.