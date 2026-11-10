# Arrears-based distress: old against new (Tables 7, 9 and 10)

Issue #94, 2026-11-09. The old rule is commit 6b0a4c7 (the D7 streak rule; runs kept outside git
in `results/raw_6b0a4c7/`). The new rule is D18 on branch `arrears-rule`: arrears are aged by
the oldest unpaid instalment on every facility, default is 91+ days past due, the run starts
from the CCMR 2017-Q1 age profile, defaulted accounts are non-performing and written off at a
derived rate, and payment friction and arrears persistence are fitted to the five arrears bands.
Only the calibration suite and rq0 were rerun. Every other table still holds old-rule numbers
until #96.

## Table 7 (`tab:arrears-fit`): CCMR bands, credit-active households, BNPL off

| Band | CCMR | Old | New |
|---|---|---|---|
| Current | 71.63 | 81.83 | 70.87 |
| 1-30 days | 8.24 | 8.27 (fitted) | 8.01 (fitted) |
| 31-60 | 3.59 | 0.39 | 4.50 (fitted) |
| 61-90 | 2.32 | 0.41 | 2.54 (fitted) |
| 91-120 | 1.76 | 0.46 | 1.59 (fitted) |
| 120+ | 12.45 | 8.64 | 12.49 (fitted) |
| 90+ | 14.21 | 9.10 | 14.08 |
| 60+ | 16.54 | 9.50 | 16.62 |
| 90+ at the final tick | - | 11.03 | 13.84 (not targeted) |

- **Parameters.**
  - Fitted: payment friction 0.0575 (was 0.09) and arrears persistence 0.72 (new), chosen by minimum distance over the five bands. The fit error is 0.98 points.
  - Derived, not fitted: the separation rate is unchanged at 0.00446, and the write-off rate is 0.0707 per tick.
- **Stationarity.** The 90+ share no longer rises through the run (B39 closed). The intermediate bands are filled (B21 closed).
- **What the fit can and cannot claim.** Agreement on the five bands is by construction, because they were targeted and the run starts from them. The evidence is that the profile holds over two years with only two fitted parameters.

## Table 10 (`tab:baseline-arms`), 20 replicates per arm, seeds 10,000-10,019

| Outcome | No BNPL old / new | beta = 0 old / new | beta = 1 old / new |
|---|---|---|---|
| Default rate, cumulative (%) | 7.28 / 20.73 | 7.18 / 21.81 | 7.43 / 21.97 |
| 90+ arrears, credit-active (%) | 9.17 / 13.98 | 9.12 / 12.46 | 9.27 / 6.48 |
| Traditional arrears, all households (%) | 7.52 / 9.16 | 7.60 / 9.36 | 7.75 / 9.45 |
| No liquid savings (%) | 20.4 / 19.1 | 20.5 / 19.2 | 23.1 / 21.1 |
| Interest charged (R m) | 11.53 / 6.58 | 11.43 / 6.54 | 11.48 / 6.54 |
| New lending (R m) | 2.52 / 5.35 | 2.14 / 5.25 | 2.28 / 5.79 |
| Refused applications | 1,077 / 2,796 | 1,060 / 970 | 1,061 / 967 |
| Holding BNPL at the final tick (%) | - | 13.90 / 9.93 | 68.97 / 56.93 |
| Ever held (%) | - | 69.15 / 63.04 | 75.35 / 70.47 |
| Volume (R m) | - | 5.42 / 5.46 | 71.28 / 62.19 |
| Owing 2+ platforms, holders at the final tick (%) | - | 35.2 / 21.8 | 86.3 / 75.3 |
| Owing 2+ platforms, ever-holders (%) | - | 30.3 / 28.2 | 98.4 / 98.1 |
| **BNPL effect on default (pp)** | - | **-0.10 +/- 0.06 / +1.08 +/- 0.11** | **+0.15 +/- 0.07 / +1.24 +/- 0.13** |

- **The default rate now includes households that start in default.** The 20.73% is the 6.36% placed at 91+ at tick 0 plus 14.37% that default during the run.
- **The BNPL effect is the same on both counts.** It is identical on new defaults: +1.08 +/- 0.11 and +1.24 +/- 0.13.
- **Interest charged fell** because defaulted accounts are non-performing and are written off.
- **Refusals without BNPL rose** because defaulted households hold impaired records.

## Table 9 (`tab:bnpl-on-checks`)

| Check | Old | New |
|---|---|---|
| Pattern 1, traditional arrears rise | +0.07 / +0.23 pp (beta 0 / 1): no change; rises | +0.20 +/- 0.05 / +0.29 +/- 0.06: rises at both |
| Pattern 1, traditional interest rises | -0.9 / -0.4%: falls; no change | -0.6 / -0.6%: no change |
| Pattern 3, DTI peaks mid-distribution | Q1 0.70, Q4 0.50: not reproduced | Q4 0.21, Q3 0.17: reproduced |
| Pattern 4, no savings | 20.4% | 19.1% |
| Stacking, ever-holders at beta = 0 | 30.3% | 28.2% (CFPB 32-33%) |
| Volume per eligible household | R852 | R860 (provider R1,333-R4,261) |
| Volume per ever-holder | R1,021 | R1,130 |
| Mean purchase | R647, 35% low | R666, 33% low |

**Check Pattern 3 before the thesis claims it.** It is now reproduced, probably because write-offs remove debt from Q1 households, which is a mechanical channel rather than behaviour. #95 must say why it moved.

## The BNPL effect, by measure (pp, paired by seed, +/- 1 SE)

| Measure | Old, beta 0 | Old, beta 1 | New, beta 0 | New, beta 1 |
|---|---|---|---|---|
| Default during the run, all households | -0.10 +/- 0.06 | +0.15 +/- 0.07 | +1.08 +/- 0.11 | +1.24 +/- 0.13 |
| 90+ share of all households, post-burn-in mean | -0.03 +/- 0.04 | +0.06 +/- 0.04 | +0.33 +/- 0.05 | +0.31 +/- 0.05 |
| 90+ share of all households, final tick | -0.03 +/- 0.06 | +0.17 +/- 0.07 | +0.07 +/- 0.08 | +0.01 +/- 0.10 |
| 90+ share of credit-active, post-burn-in mean | -0.05 +/- 0.09 | +0.10 +/- 0.10 | -1.53 +/- 0.13 | -7.50 +/- 0.11 |
| Consumption distress, ever (all households) | n/a | n/a | +0.13 +/- 0.06 | +0.20 +/- 0.05 |

**The credit-active 90+ share is not a valid measure of the BNPL effect.**
- Credit-active now includes BNPL holders, so the denominator grows from 1,175 to 1,479 households at beta = 0 and to 3,200 at beta = 1 (final tick).
- The share then falls even though more households are in arrears.
- Use it for the level, with BNPL off, against the CCMR. Use default during the run, or the 90+ share of all households, for effects.
- The final-tick 90+ stock also understates the effect, because written-off accounts leave it.

**Where the effect comes from** (10 seeds, beta = 0, `calibrated()`):
- New defaults are 14.34% without BNPL and 15.41% with it.
- Of the 1.07-point rise, 0.94 points are households whose oldest unpaid BNPL instalment reached 98 days. Only 0.13 points come through traditional arrears.
- The headline effect is therefore mainly households defaulting on BNPL itself. That follows from counting BNPL arrears (#91 C1) and from BNPL arrears never curing without cash.
- Persistence applies to traditional debt only.

## Against the external figures

| Measure | Model, new rule, BNPL off | External |
|---|---|---|
| 90+ arrears, credit-active, post-burn-in mean | 14.08% | CCMR 2017-Q1: 14.21% of accounts |
| 90+ arrears, credit-active, final tick | 13.84% | NCR CBM March 2017: 21.7% of credit-active consumers 3+ months in arrears |
| Default during the run, two years | 14.37% of all households | no direct counterpart |
| Default, cumulative, including the initial stock | 20.73% of all households | |

**Units.**
- The CCMR counts accounts, the CBM counts consumers, and the model counts households (B5).
- The CBM figure covers every credit product, including retail and telecoms accounts that the model does not hold, so the model is expected to sit below it.

## Open for the supervisor and for #95

1. **The headline effect is now large and detectable at beta = 0.** At about +1.1 points it is ten times the old effect, and it runs mainly through BNPL arrears. The thesis story changes from "BNPL adds little" to "BNPL default is a channel of its own".
2. **The credit-active denominator.**
   - It now includes BNPL holders, so effects should be read on all-household measures.
   - It also shrinks over the run (2,237 at the start to 1,175 at the final tick with BNPL off; corrected 2026-11-10 from 2,285, probably the count at the end of the first tick, after its shortfall loans; 2,237 is the count with `D_trad > 0` in the population and the only one that reproduces the 6.36% starting stock), because defaulted accounts are written off and the model has no new borrowers other than through shortfalls.
3. **Pattern 3** moved to "reproduced", probably through write-offs. Check before claiming it.
4. **The bands are no longer evidence.** The starting profile and the five bands are inputs or targets. What the model now shows is that the profile is stable over two years with two fitted parameters (B44).
5. **beta = 1 in these tables will be replaced by the range from Milestone 2 (#97 to #100).**
