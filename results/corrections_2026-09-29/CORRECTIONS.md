# Corrections of 2026-09-29: what was wrong, what was changed, what was left alone

This record covers the simulation code. The before-and-after results are in
`BEFORE_AFTER.md`, the step-by-step diagnostic in `diagnostic_summary.md`, and the
instructions to reproduce everything in `REPRODUCE.md`.

Every behaviour below was established with a one-household example before anything was
changed (`verify_behaviour.py`; output on the original code in `behaviour_original.txt`, on the
corrected code in `behaviour_corrected.txt`). Each correction has regression tests in
`simulation/tests/`.

## 1. Confirmed implementation defects, corrected

| # | Defect | Evidence on the original code | Correction | Commit | Tests |
|---|---|---|---|---|---|
| 1 | **Traditional interest was charged twice.** Interest was added to the balance at accrual, and the payment then reduced the balance by the payment less interest. | R1,000 at 1% a tick with R100 paid left R920, where 1000 + 10 − 100 = 910. A loan amortised over 12 ticks took 15 to clear and cost R1,144 against a contract total of R1,066. | The whole payment comes off the balance. | `b483ea1` | `test_debt_accounting.py` |
| 2 | **Arrears were counted twice in total debt.** An unpaid instalment stays inside the balance, and `total_debt()` added arrears to it again. Affects the debt-to-income statistics only. | Balance R1,010 with R100 in arrears reported R1,110. | Arrears are no longer added. The amount due is also capped at the balance. | `b483ea1` | `test_debt_accounting.py` |
| 3 | **A cleared debt kept its instalment.** `scheduled_service_tick` was never reset, so the bureau went on showing the lender the service of a loan that no longer existed, and the gate refused credit on it. | After the 12-tick loan cleared the gate was still shown R88.85 a tick. | Scheduled service and arrears return to zero when the balance clears. | `b483ea1` | `test_debt_accounting.py` |
| 4 | **The next BNPL instalment was collected in the tick an agreement was opened**, on the shortfall path only, because that path borrows before it pays. Half the purchase was paid at once. The contract is 25% at checkout and 25% at each of the next three ticks. | A shortfall agreement of R200 ended its opening tick with two instalments remaining; a want-driven purchase ended it with three. | Agreements record the tick they were opened in and collection skips them until the next tick. | `d3352c4` | `test_shortfall_path.py` |
| 5 | **The checkout quarter of a shortfall agreement was requested from neither lender.** BNPL relieves a shortfall by three quarters of the amount financed, because a quarter is paid at checkout (DECISIONS.md, D5). The traditional lender was asked for the request less the *whole* amount financed. A household that used BNPL for a shortfall therefore stayed short, and was recorded as distressed, whatever either lender was willing to grant. | Shortfall R200: with traditional credit alone the household borrowed R200 and was not distressed. With BNPL enabled it financed R200, received R150, made no traditional application, paid R100 of the R200 due and was recorded as distressed. | The traditional lender is asked for the request less the cash BNPL freed. A refusal still leaves the shortfall unpaid and the tick distressed. | `1415625` | `test_shortfall_path.py` |
| 6 | **Late fees could exceed the purchase price.** Payflex caps late fees at "the lower of R285.00 (including VAT) or 50% of the Purchase Price" (terms and conditions, read 2026-09-29). The model applied the Rand cap only. | A R200 purchase could accrue R285 (nominal) in fees. | The cap is the lower of the two. The share is a sourced parameter, `bnpl_late_fee_cap_share`. | `f40e4bf` | `test_bnpl_schedule.py` |

Defect 5 is the one that matters for the thesis. At fixed parameters and on the same seeds it
accounts for almost all of the effect of BNPL on default that the thesis reported
(`diagnostic_summary.md`). It is classified as a defect, and not as a modelling assumption,
for two reasons. The decision register defines what BNPL covers: the household "pays only 25%
at checkout, and the other 75% stays in its pocket", and "traditional credit is approached for
shortfalls BNPL cannot cover". And Submodel 4 has the household request its shortfall; under
the old arithmetic its two requests together always fell short of it.

Because the classification decides the headline result, the earlier behaviour is kept as an
explicit alternative assumption, `shortfall_checkout_financed = False`, and run as one arm of
the effect suite. The thesis reports both.

## 2. Inaccurate descriptions, corrected in the text (no change in behaviour)

| Subject | What the code does | What the text said |
|---|---|---|
| **The hypothetical cap** | Counts platforms on which the household owes a balance. A household at the cap is refused every new draw, including a draw on a platform it already uses. Below the cap it may open further agreements on a platform in use, so under a cap of two or three it can hold more agreements than the cap. A cap of one is one agreement at a time. | "A cap on concurrent agreements"; "a count of open agreements on any platform, not of platforms". |
| **Platform routing** | Every request goes to the platforms in a random order, redrawn for the request, and what one platform does not finance passes to the next. With four platforms a second request reaches a different platform first three times in four, although the first has headroom. | "Stacking arises from borrowing requests and the available platform headroom"; "emerges although no rule assigns households to several providers". |
| **Screening gate** | Is shown the household's traditional service and its BNPL instalments on every platform, whether or not the bureau switch is on. | "The same affordability gate applied to BNPL originations", with no statement of what it is shown. |
| **Switches "crossed"** | Each switch was crossed with peer influence only. No arm ran both switches. | "Crossed". An arm with both switches has been added (`rq3_both`, seeds 44,000–44,019). |
| **Default** | Absorbing, counted from tick 0, over all 5,000 households. The final-tick rate is the share that defaulted at any tick, burn-in included. | "In default at the final tick", which is correct but does not say the measure is cumulative. |
| **Income at the gates** | Both gates use income at initialisation. An unemployment spell does not reduce it. | "Declared gross income". |
| **Committed shortfall** | A committed-expenditure shortfall is recorded as distress and is not carried forward. Cash borrowed against it is spent on debt service, then discretionary spending, and the rest is saved. | "Remains recorded as distress even if later borrowing supplies enough cash to cover it", which implies the loan pays for the expenditure. |
| **Debt service in the distress test** | The amount due: the instalment or minimum payment plus arrears, and the BNPL instalments due. | "Scheduled debt service". |
| **Rolling limit** | The count is of platform requests that the limit truncates or refuses, over every platform a request reaches. | "Requests refused by the limit". |
| **Late-fee cap** | Per agreement, over its life. | The parameter register said "per missed instalment". |
| **Seed blocks** | The sensitivity groups, the scenario arms, the cap arms and the threshold-mean arms each have their own block. | "Arms within a suite share seeds, except in the scenario suite". |
| **Imputed product flags** | BNPL eligibility uses the banked flag only. The five product flags price opening traditional debt. Stacking follows from routing. | "The joint structure that cross-platform stacking depends on". |
| **Initial vulnerability** | Of the 5,000 agents, 45.2% start with no liquid savings, 3.6% with income below committed expenditure and 5.1% with income below committed expenditure plus service. | 44.3%, 3.9% and 5.2%, which are the figures of the validation summary and not of the agents. |
| **Parameter register** | Runs use the fitted shock probability 0.016 and payment friction 0.09. | The register printed the code defaults 0.01 and 0.0, decision numbers in place of submodel numbers, and development notes. |

The cap follows the register ("a maximum on concurrent facilities"; a facility is a platform
relationship with a balance) and the code was written to it, so the code is unchanged and the
text is corrected.

## 3. Modelling assumptions examined and left unchanged

- **Random platform routing.** Disclosed in the text now. Not redesigned.
- **BNPL first for a shortfall** (Submodel 5), capped at kappa times the monthly discretionary
  budget. Unchanged.
- **Cut-off when the late-fee cap is exhausted.** Unchanged as a rule. With the corrected cap a
  purchase under R251 (2017 Rands) exhausts its cap at the first missed instalment, so its
  holder is cut off by that platform one tick sooner than before.
- **One consolidated traditional balance.** A new loan adds its instalment to scheduled
  service, which then runs until the whole balance clears. Unchanged.
- **Committed shortfalls are not repaid from the loan raised against them.** The design record
  (DECISIONS.md, D7) notes that the code differs from the written rule here and reserves the
  choice for Marc. The code is unchanged and the thesis now describes what it does. Moving to
  the written rule would need a recalibration and a full rerun.
- **Seeds.** Every suite keeps its original seed block. The scenario arms therefore still use
  seed blocks different from the benchmark's, and their differences are unpaired.

## 4. Additions

- `rq3_both`: bureau visibility and screening together, at both values of beta.
- `eff_checkout_unfunded`: the earlier fallback arithmetic as an explicit assumption, at both
  values of beta, in the effect suite.
- `paid_trad_tick` and `borrowed_trad_tick` on the household, read by the tests.
- The table generator pairs a difference by seed when two arms share seeds and population, and
  uses the unpaired standard error otherwise. Every table note says which.

## 5. Remaining limitations

- The shortfall path has no empirical anchor: how much a household borrows against a shortfall,
  from which lender, and whether it can borrow for a checkout payment are assumptions.
- Both gates assess a household on income it may no longer receive.
- Scenario differences compare different seed blocks, so they carry more noise than a paired
  design would.
- The Sobol analysis has two replicates per design point and decomposes the level of default,
  not the effect of BNPL.
- The income-shock probability is fitted on a grid with steps of 0.008.
- A difference is called detectable beyond two standard errors. A true difference of that size
  would be missed about half the time, so "not detectable" is weak evidence of no effect.
- The effect of the cap depends on how the cap is defined (`cap_definitions.md`), so the lever
  results do not establish lost volume as the cause of lower default.

## 6. Independent audit of the revised thesis

Two read-only audits checked the revised text: one recomputed every number in the prose from
`results/raw` and compared the model description with the code; the other checked style and
presentation. Every recomputed number matched. The audit found claims that said more than the
data support and descriptions that did not match the code. Each finding was re-derived before
it was acted on (the scripts are in `audit_checks/`), and
the corrections are those listed in section 2 together with these changes of wording:

- "Detects a change of 0.2 points" became a statement of the threshold and of its power.
- The lender "refuses as many applications" became the measured differences, which differ by
  seed block (+1 ± 9 and -16 ± 7).
- The threshold rule does not raise default detectably more than its control (the difference
  in the rise is between +0.05 ± 0.08 and +0.14 ± 0.13).
- Adding bureau visibility to screening leaves BNPL volume and default without a detectable
  change, and raises traditional refusals by about 100.
- The cooling-off window is not the only lever that lowers the adoption share households see.
- Explanations that no experiment isolates are now stated as possible explanations.
- The sensitivity figure now uses paired intervals, as the tables do.

One audit finding was not accepted as written: the arms with a limit of 0.25 and of 1.0 months
of income are not identical runs. They give the same default in every replicate at beta = 0,
and their volumes differ slightly.
