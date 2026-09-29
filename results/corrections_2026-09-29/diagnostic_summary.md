# Diagnostic at fixed parameters (shock probability 0.016, friction 0.09)

Seeds 10,000-10,019 in every arm and at every step; differences are paired by seed, with one standard error. Default is the share of all households in default at the final tick.

|                                            | original code   | + interest and payment accounting   | + instalment timing   | + traditional fallback request   | + late-fee cap (all corrections)   |
|:-------------------------------------------|:----------------|:------------------------------------|:----------------------|:---------------------------------|:-----------------------------------|
| commit                                     | 5694751         | b483ea1                             | d3352c4               | 1415625                          | f40e4bf                            |
| default, no BNPL (%)                       | 13.40           | 13.31                               | 13.31                 | 13.31                            | 13.31                              |
| 90+ credit-active, no BNPL (%)             | 13.68           | 14.20                               | 14.20                 | 14.20                            | 14.20                              |
| BNPL effect, beta=0 (pp)                   | +1.22 ± 0.13    | +1.15 ± 0.11                        | +1.11 ± 0.09          | +0.06 ± 0.09                     | +0.03 ± 0.09                       |
| BNPL effect, beta=1 (pp)                   | +2.07 ± 0.10    | +1.99 ± 0.12                        | +2.09 ± 0.09          | +0.47 ± 0.13                     | +0.61 ± 0.11                       |
| shortfall path only (pp)                   | +1.20 ± 0.10    | +1.16 ± 0.12                        | +1.20 ± 0.09          | +0.07 ± 0.08                     | +0.07 ± 0.08                       |
| bureau less benchmark (pp)                 | +0.03 ± 0.08    | +0.12 ± 0.07                        | +0.15 ± 0.07          | +0.20 ± 0.11                     | +0.20 ± 0.10                       |
| screening less benchmark (pp)              | -0.06 ± 0.11    | -0.04 ± 0.10                        | +0.02 ± 0.11          | -0.01 ± 0.09                     | +0.02 ± 0.09                       |
| cap 1 less benchmark (pp)                  | -1.26 ± 0.11    | -1.14 ± 0.13                        | -1.01 ± 0.10          | -0.01 ± 0.10                     | +0.12 ± 0.10                       |
| cap 2 less benchmark (pp)                  | -1.18 ± 0.10    | -1.07 ± 0.09                        | -1.08 ± 0.09          | +0.02 ± 0.12                     | +0.04 ± 0.11                       |
| new traditional lending, BNPL beta=0 (R m) | 3.48            | 3.28                                | 3.43                  | 5.42                             | 5.43                               |
| BNPL volume, beta=0 (R m)                  | 5.47            | 5.45                                | 5.34                  | 6.42                             | 6.42                               |
