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

## 7. Marc's decisions of 2026-09-29, and what was done

Sections 1 to 6 are left as the record of the corrections. Where this section differs from
them, this section is the current position.

**1. The corrected shortfall rule is the only one.** Marc confirmed that defect 5 was a defect:
a household is distressed only if the lender refuses. The alternative assumption
`shortfall_checkout_financed = False` is removed from the code (commit `4ef473c`): the
parameter, the branch in `_seek_credit`, the arm `eff_checkout_unfunded`, its test, and its
entries in the table builder, the check script and the register generator. The thesis no
longer reports the arm (commit `c29300a`). Section 1's closing sentence, "The thesis reports
both", and the second item of section 4 describe the position before this decision.

- The 40 runs of the arm were moved from `results/raw/effect.parquet` to
  `effect_checkout_unfunded.parquet` in this folder, together with the parameter column that
  only they varied. The file is not tracked, like the other raw runs. The arm can be
  reproduced from commit `e366631`, and from no later commit.
- `remove_checkout_arm.py` reran the baseline suite (60 runs) and the remaining effect suite
  (880 runs) at commit `4ef473c` and compared every numeric column with the stored runs. The
  largest absolute difference is 0.0 in both (`remove_checkout_arm.log`).
- `rerun_effect.py` and `before_after.py` read the removed arm. They belong to the record and
  run at commit `e366631`, not at the current one.
- Two conclusions rested on the comparison and were removed with it: that the size of the
  effect depends on the checkout assumption more than on any other setting, and that it
  depends more on how households finance a shortfall than on what lenders can see. No
  remaining experiment compares those two things. The limits in the conclusion are now three.

**2. Committed shortfalls stay as they are.** Marc considered carrying an unpaid committed
shortfall forward and kept the rule of section 3. No code or text changed.

**3. RQ2 is reworded** (commit `03bf1ab`): "When BNPL platforms cannot observe one another's
exposures, how often do households owe several platforms at once, and how do enabling BNPL,
platform count, access and peer adoption affect population default?" The restatements in
Sections 1, 3, 4 and 4.6 follow it. Nothing in the thesis describes stacking as emergent.

**4. Four figures were checked against their sources** (commit `7eb36b8`). No parameter and no
validation tolerance changed.

| Figure | Source read on 2026-09-29 | Result |
|---|---|---|
| Order cap, R15,000 | Payflex terms and conditions; the pages in the payflex.co.za sitemap and archived copies of the terms, 2019 to 2026 (scanned by a search agent); Payflex's archived FAQ "What's the maximum I can spend with Payflex?" | **Not sourced.** No Payflex page states a maximum order value. Clause 4.4 of the terms reserves the right to amend a customer's spend limit, and the FAQ says the limit depends on an individual assessment. Third-party pages give R10,000 (loanrating.co.za) and "e.g., R20,000" (Peach Payments). The cap is now recorded as an assumption. It binds on 0.3% of platform requests at beta = 0. |
| UK median income behind the 37% | ONS, "Average household income, UK: financial year ending 2020", released 21 January 2021, corrected 22 March 2022 | Median equivalised household disposable income, 30,500 pounds a year. 1,000 pounds is **39.3%** of a month's income. The text now says 39%. The earlier 37% matches the median for the year to March 2022, published after the Woolard Review. |
| Australian median income behind 0.26 | ABS, "Household Income and Wealth, Australia, 2019-20", released 28 April 2022; ASIC REP 672, Table 2 | Afterpay's maximum of A$2,000 is **25.8%** of median gross household income (A$1,786 a week), so 0.26 stands on that measure. On median equivalised disposable income (A$959 a week), the measure used for the UK, it is 48.1%. The text names the measure and gives both. |
| Gini bounds, 0.63 and 0.70 | World Bank API, archive vintages of February and April 2026 and the live series; Stats SA Report 03-10-19, Table B3; Hundenborn, Leibbrandt and Woolard, WIDER Working Paper 2018/162, Table 1 | The World Bank citation is accurate: 63.0 for 2014 in the February vintage, 59.6 and 54.1 (2022) in the April vintage, consumption-based. The upper bound matches Stats SA's per-capita income Gini for 2009, 0.70. Income comparisons added: 0.67 (Stats SA, 2015) and 0.66 (NIDS 2014). No published income Gini computed from NIDS Wave 5 was found. |

One bibliography entry was wrong and is corrected: `payflex_limits` pointed at
support.myboost.co, the help centre of Boost PayFlex, a Malaysian product.
