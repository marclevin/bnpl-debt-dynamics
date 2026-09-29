# Headline results before and after the corrections

Before: code at tag `pre-correction-2026-09-29`, outputs preserved in `results/superseded_2026-09-29_pre-correction/raw`. After: corrected code, outputs in `results/raw`. Both use shock probability 0.016 and payment friction 0.09, which the recalibration confirmed. Twenty replicates per arm. Differences carry one standard error, paired by seed where the two arms share seeds and unpaired otherwise. An asterisk marks a difference beyond two standard errors.

| Result                                                                | Before        | After         |
|:----------------------------------------------------------------------|:--------------|:--------------|
| Baseline default, no BNPL (%)                                         | 13.40         | 13.31         |
| Baseline 90+ arrears, credit-active (%); target 14.21                 | 13.68         | 14.20         |
| Baseline 1-30 day arrears (%); target 8.24                            | 8.22          | 8.20          |
| Baseline 31-60 day arrears (%); CCMR 3.59                             | 0.91          | 0.94          |
| Baseline 61-90 day arrears (%); CCMR 2.32                             | 0.93          | 0.96          |
| BNPL effect on default, beta=0 (pp)                                   | +1.22 ± 0.13* | +0.03 ± 0.09  |
| BNPL effect on default, beta=1 (pp)                                   | +2.07 ± 0.10* | +0.61 ± 0.11* |
| BNPL effect on traditional arrears rate, beta=0 (pp)                  | +0.64 ± 0.07* | +0.23 ± 0.07* |
| BNPL effect on traditional arrears rate, beta=1 (pp)                  | +1.14 ± 0.06* | +0.57 ± 0.07* |
| BNPL effect on traditional interest, beta=0 (R m)                     | -0.38 ± 0.06* | -0.20 ± 0.05* |
| New traditional lending, no BNPL / beta=0 (R m)                       | 6.57 / 3.48   | 6.12 / 5.43   |
| BNPL volume, beta=0 / beta=1 (R m)                                    | 5.47 / 64.32  | 6.42 / 65.88  |
| Holding BNPL at final tick, beta=0 / beta=1 (%)                       | 16.79 / 65.66 | 17.55 / 66.80 |
| Holders on 2+ platforms, final tick, beta=0 / beta=1 (%)              | 45.0 / 83.0   | 52.0 / 85.1   |
| Ever on 2+ platforms, of ever-adopters, beta=0 / beta=1 (%)           | 37.0 / 98.6   | 36.8 / 98.6   |
| Mean want-driven purchase, beta=0 (R); band 645-1339                  | 645.60        | 633.16        |
| Default, six platforms less one, beta=0 (pp)                          | -0.04 ± 0.09  | +0.02 ± 0.09  |
| Default, six platforms less one, beta=1 (pp)                          | +0.18 ± 0.12  | +0.01 ± 0.08  |
| Default, six platforms less one, beta=2 (pp)                          | +0.43 ± 0.12* | -0.04 ± 0.12  |
| Default, six platforms less one, beta=3 (pp)                          | +0.28 ± 0.11* | +0.14 ± 0.13  |
| Default, full access less none, beta=0 (pp)                           | +1.41 ± 0.10* | +0.14 ± 0.11  |
| Default, full access less none, beta=1 (pp)                           | +2.07 ± 0.10* | +0.60 ± 0.11* |
| Default, full access less none, beta=3 (pp)                           | +2.35 ± 0.08* | +0.95 ± 0.09* |
| Bureau visibility less benchmark, default, beta=0 (pp)                | +0.26 ± 0.11* | +0.04 ± 0.10  |
| Bureau visibility less benchmark, default, beta=1 (pp)                | +0.04 ± 0.12  | +0.09 ± 0.12  |
| Screening less benchmark, default, beta=0 (pp)                        | +0.02 ± 0.10  | -0.02 ± 0.10  |
| Screening less benchmark, default, beta=1 (pp)                        | -0.05 ± 0.10  | -0.09 ± 0.13  |
| Both switches less benchmark, default, beta=0 (pp)                    | not run       | +0.05 ± 0.10  |
| Both switches less benchmark, default, beta=1 (pp)                    | not run       | -0.09 ± 0.11  |
| Cap of one platform less benchmark, default, beta=0 (pp)              | -1.21 ± 0.10* | -0.03 ± 0.11  |
| Cap of one platform less benchmark, default, beta=1 (pp)              | -1.83 ± 0.13* | -0.31 ± 0.12* |
| Cap of two platforms less benchmark, default, beta=0 (pp)             | -1.01 ± 0.11* | +0.04 ± 0.12  |
| Cap of two platforms less benchmark, default, beta=1 (pp)             | -1.47 ± 0.11* | -0.32 ± 0.10* |
| Cap of three platforms less benchmark, default, beta=0 (pp)           | -0.06 ± 0.11  | +0.06 ± 0.09  |
| Cap of three platforms less benchmark, default, beta=1 (pp)           | -0.14 ± 0.12  | -0.11 ± 0.10  |
| Cooling-off, one tick less benchmark, default, beta=0 (pp)            | +0.15 ± 0.11  | -0.06 ± 0.11  |
| Cooling-off, one tick less benchmark, default, beta=1 (pp)            | -0.31 ± 0.12* | -0.28 ± 0.08* |
| Cooling-off, four ticks less benchmark, default, beta=0 (pp)          | +0.04 ± 0.09  | -0.01 ± 0.09  |
| Cooling-off, four ticks less benchmark, default, beta=1 (pp)          | -0.55 ± 0.09* | -0.39 ± 0.12* |
| BNPL effect under shortfall +25%, beta=0 (pp)                         | +0.73 ± 0.08* | +0.12 ± 0.09  |
| BNPL effect under shortfall + committed, beta=0 (pp)                  | +0.31 ± 0.07* | +0.22 ± 0.10* |
| BNPL effect under BNPL share uncapped, beta=0 (pp)                    | +1.46 ± 0.06* | +0.05 ± 0.09  |
| BNPL effect under single-tick shock, beta=0 (pp)                      | +0.68 ± 0.01* | -0.02 ± 0.01  |
| BNPL effect, shortfall path only, beta=0 (pp)                         | +1.16 ± 0.11* | +0.05 ± 0.09  |
| BNPL effect, checkout quarter not requested, beta=0 (pp)              | not run       | +1.11 ± 0.10* |
| BNPL effect, checkout quarter not requested, beta=1 (pp)              | not run       | +1.92 ± 0.10* |
| Sensitivity: shortfall + committed less exact, default at beta=1 (pp) | -2.15 ± 0.08* | -1.02 ± 0.13* |
| Sensitivity: default horizon 56 days less 98, beta=1 (pp)             | +1.34 ± 0.09* | +0.84 ± 0.11* |
| Sensitivity: single-tick shock, default at beta=1 (%)                 | 5.66          | 4.81          |
