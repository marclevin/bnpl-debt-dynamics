# Next Steps: sourcing the weak parameters, RQ2, and the word budget

**Status:** planned, not executed. Written 2026-08-12 after the first full sweep (3,304 runs).
Canonical strategy: [`../OVERVIEW.md`](../OVERVIEW.md). Defect register:
[`issues.md`](issues.md). Decision rules: [`decision_rules.md`](decision_rules.md).

> **Why this file exists.** The first full sweep showed that the model's output is driven mainly by
> its two worst-sourced parameters (issues.md **B24**), that RQ2 has no affirmative answer under
> linear peer coupling (**B22**), and that the RQ3 cool-off arm has an off-by-one that inverts its
> headline claim. This is the plan to fix all three. It also sets the word budget, because the
> binding constraint on this thesis is now **16,000 words**, not model quality.

---

## P0. Fix the cool-off off-by-one (BLOCKER for RQ3, ~30 minutes)

**The bug.** In `simulation/agents.py`, a want-driven purchase at tick `t` sets
`cool_off_until = t + k_cool`, and the gate is `self.model.tick >= self.cool_off_until`. With
`k_cool = 1` the gate passes again at `t + 1`, so **nothing is ever blocked** — a household could
not buy twice in the same tick anyway. `k_cool = 1` is a silent no-op.

**Why it matters.** `k_cool = 1` is the arm the thesis presents as the **CCA s.66A statutory 14-day
right of withdrawal**, and D14 makes a point of it landing exactly on a tick boundary. The sweep
therefore reports the statutory instrument as having *precisely zero* effect (+0.0% volume at both
betas), which is an artefact, not a finding.

**The fix.** Make `k_cool = n` block the next `n` ticks: set `cool_off_until = tick + k_cool + 1`,
or change the gate to `tick > cool_off_until`. Then re-map the sweep so `k_cool = 1` is the
statutory arm.

**What the corrected result already looks like.** The current `k_cool = 2` arm is what a correct
`k_cool = 1` will produce: **−2.6% volume at β=0 and −30.4% at β=1**. So the corrected claim is
*"the statutory cool-off is close to useless against individual impulse and materially effective
against social transmission"*, which is a far better result than the one currently in the output.

**Add a regression test:** `k_cool = 1` must strictly reduce want-driven purchase count relative to
`k_cool = 0`. The existing degenerate test only asserts volume does not *increase*, which the no-op
satisfied trivially — that is why the suite missed it.

---

## P1. Derive BNPL purchase size from NIDS (removes the top vulnerability)

**The problem.** `bnpl_purchase_mean = 1568` rests on **trade press** (`sa_bnpl_basket_2026`,
flagged `% VERIFY`), it is the weakest source in the bibliography, and it is the **single largest
driver of the model's output**: sweeping R784–R3,136 moves population default by **19.6pp**, and
Sobol puts two-thirds of its influence in *interactions* with other parameters.

**Do not chase a better national average.** Contacting providers is slow, unlikely to yield a
citable figure, and asks for commercially sensitive data. One polite email each is fine; it must not
be on the critical path.

**Instead, make it an observable.** This is the same move that already worked twice: `w5_hhwage`
eliminated the D1 shock magnitude, and `indderived` supplied earner counts.

**Proposed rule.** A household's BNPL purchase is drawn relative to **its own observed discretionary
expenditure**, which NIDS already carries as `expenditure_discretionary`:

```
purchase_i ~ LogNormal( mu = log(kappa * discretionary_monthly_i), sigma )
```

- **Justification.** BNPL finances discretionary consumption, and a household's own discretionary
  budget is the observed scale at which it makes discretionary purchases. Trade sources describe SA
  BNPL as concentrated in "considered purchases" in the R800–R8,000 range — a *range*, not a mean,
  which a household-relative rule reproduces naturally.
- **`kappa` is a single multiple**, far easier to defend than a national mean, and it inherits the
  full observed heterogeneity of the population instead of imposing one number on everyone.
- **Heterogeneity is the ABM-correct choice anyway.** A constant purchase size for a population with
  a Gini of 0.67 is indefensible on its own terms.

**The key inversion.** The R1,568 figure stops being an *input* and becomes a **validation target**:
after the change, check that the population-mean purchase lands near R1,568. A weak source used as a
check is legitimate; the same source used as a load-bearing input is not. This converts B24's top
vulnerability into an additional external check.

**Work:** ~1–2 days. `expenditure_discretionary` is already on `HouseholdRecord`, so this is a change
to `_bnpl_purchase()` in `agents.py` plus a new `kappa` in `config.py`. Sweep `kappa` and `sigma`.

---

## P2. Derive the rolling platform limit from household characteristics

**The problem.** `bnpl_platform_limit = 5000` is **unsourceable** — neither Payflex nor PayJustNow
publishes a rolling limit (issues.md **B16**) — and it is the **second largest driver**, moving
default by **16.9pp** over R1,000–R15,000.

**The opening the providers themselves give us.** Both state the limit is set **per customer from
credit history and repayment behaviour**. That is a licence to model it as a *function*, not a
constant, and to cite them for the functional form:

```
rolling_limit_i = lambda * income_monthly_i     (capped at the R15,000 Payflex order cap)
```

- **Why income and not Reg 23A capacity.** Tempting, but wrong: D11's whole point is that the BNPL
  screen is *deliberately not* the Reg 23A test, and that asymmetry with D9 is the thesis mechanism.
  Using Reg 23A capacity to set BNPL limits would quietly undo the mechanism. Income is what a
  **light automated screen** can plausibly infer from bank-card activity, which is exactly what D11
  describes.
- **One free parameter `lambda`** replaces one free constant, but the *distribution* of limits
  becomes data-driven and the parameter is now interpretable ("platforms extend roughly `lambda`
  months of income").

**Validation hooks, both already required by D11:** the order cap must still bind rarely (currently
0.3%), and the rolling limit's binding rate should be reported. Note from the sweep that the limit is
**inert above ~R5,000 but binds hard at R1,000**, so the sensible `lambda` range is one that keeps
most households above that.

**Work:** ~1 day. `BNPLPlatform.rolling_limit` becomes per-agent rather than per-platform.

---

## P3. RQ2: the Granovetter heterogeneous-threshold variant

**Why this is not optional.** D17 **pre-registered** it as the structural robustness check should
linear coupling produce only a smooth response. That is exactly what happened (**B22**): every arm
is near-linear including the β=0 control (R² = 0.9992). Not running the registered fallback reads as
avoidance. Also, linear coupling producing a linear response is close to tautological — it is weak
evidence for "no threshold exists".

**The current rule (D17):**

```
q_i(t) = clip( q_base + beta * s_g(t-1), 0, 1 )
```

**The variant.** Give each household a **heterogeneous adoption threshold** `theta_i`, fixed at
initialisation, and let it adopt socially only once its reference group crosses that threshold:

```
theta_i ~ Normal(mu_theta, sigma_theta)   truncated to [0, 1]
q_i(t) = q_base                      if s_g(t-1) <  theta_i
q_i(t) = clip(q_base + gamma, 0, 1)  if s_g(t-1) >= theta_i
```

- **Granovetter's actual claim** is that it is the **variance** of thresholds, not the mean, that
  decides whether a cascade occurs. So `sigma_theta` is the primary experimental axis, and it must
  be swept explicitly — sweeping only `mu_theta` would miss the point of the citation.
- **The control arm is preserved.** `gamma = 0` (or `theta_i = 1` for all `i`) recovers the
  independent-agent model exactly, exactly as `beta = 0` does now. Keep the same degenerate test.
- **Report with the same diagnostic** already implemented in `analysis.py`: linear R² and max
  deviation from a straight line over the access range, so the linear and threshold variants are
  compared on identical terms.

**Either outcome is a result.** A threshold appears → RQ2 has an affirmative answer. No threshold
under two structurally different social mechanisms → a genuinely robust negative finding, which is
much stronger than the current single-mechanism negative.

**Work:** ~1 day. Implemented as an alternative branch in `agents.py` step 6 plus a
`peer_mechanism` parameter (`"linear"` | `"threshold"`), so both remain runnable and comparable.

---

## P4. Final re-run and publication-grade sensitivity

Once P0–P3 land:

1. **Re-run every BNPL-on suite.** The baseline calibration is **unaffected** — `shock_prob` and
   `payment_friction` are fitted with BNPL disabled, so P1–P3 cannot disturb them. That means no
   re-calibration, and the CCMR comparison, pattern 3 and pattern 4 all stand as they are.
   Cost: ~3,200 runs, roughly 75 minutes.
2. **Sobol at N >= 256.** Current indices come from N=64 with wide confidence intervals and several
   slightly negative S1 estimates (a known small-sample artefact). Rankings are stable but the point
   estimates are not quotable. `python -m simulation.sensitivity --samples 256`, ~4x the compute.
3. **Add the plausibility band to the RQ2 figure.** Anchored to the TransUnion ~20% BNPL-intention
   figure: arms producing 10–25% household adoption give default of **28.8%–42.1%** against a 24.6%
   baseline. Report magnitudes inside that band and label everything outside as mechanistic
   extrapolation (issues.md **B25**).

---

## P5. Optional, only if time allows: the reciprocal-bureau lever

Bureau visibility currently does **nothing** (issues.md **B23**) because it is only half a bureau:
BNPL platforms neither report to it nor query it, so D12 blindness survives the intervention and
only the *bank* is constrained.

A fifth lever — **platforms must both report to and query the bureau** — would attack cross-firm
stacking directly, which is the mechanism the thesis exists to study, and it is what the FCA's
PS26/1 perimeter move actually implies. Expected to be the lever that bites hardest.

Cheap to add (the bureau object already exists; the platform screen would consult it). Genuinely
optional: the existing null result is already a good finding, and word count is the binding
constraint.

---

## The word budget: 16,000 words

This is now the **binding constraint on the thesis**, tighter than any modelling question. There is
more machinery here than 16,000 words can carry, so the task is **demotion, not deletion**.

**First: confirm with the supervisor what counts.** Whether appendices, tables, figure captions and
the bibliography fall inside the limit changes everything below. If appendices are excluded, most of
this is straightforward.

Indicative allocation:

| Chapter | Words | Note |
| --- | --- | --- |
| 1 Introduction | 1,200 | state the counterfactual framing once, not three times (F5) |
| 2 Literature | 1,800 | already drafted; compress |
| 3 Data | 1,800 | P1–P4 in summary; diagnostics to an appendix |
| 4 Design (ODD) | 2,800 | currently ~3,588. Submodel table stays, prose shrinks |
| 5 Implementation | 1,200 | architecture, tick, parameter register, verification summary |
| **6 Results** | **4,500** | the largest chapter; ~6 figures, not 16 |
| 7 Limitations | 1,200 | B20, B22, B24, B25 are the four that matter |
| 8 Conclusions | 800 | |
| **Total** | **15,300** | ~700 in hand |

**What moves to appendices:** the full verification catalogue (65 tests → one paragraph plus a
table), the complete robustness suite (→ the tornado figure plus a table), the Sobol decomposition
(→ one figure plus a paragraph), the rejected design alternatives (already in Appendix A), and the
full CCMR band table.

**The six figures Chapter 6 should carry:**
1. Baseline arrears profile vs CCMR — the calibration evidence.
2. Pattern 3 debt-to-income by quintile — the statistic-dependence point.
3. RQ2 access x beta surface with the plausibility band — the central figure.
4. RQ1 emergent stacking vs the CFPB benchmark.
5. RQ3 intervention ranking and the defer-vs-desist volume test.
6. Robustness tornado — which makes the B24 vulnerability legible in five seconds.

**Lead with the strongest three results, in this order:**
1. **Transparency alone changes nothing.** Closing the reporting gap moves default 0.08pp; an
   affordability duty moves it 4.9pp. Counterintuitive, policy-relevant, and about a live
   regulatory question. This is probably the best thing in the thesis and it is currently buried
   inside RQ3.
2. **The unfitted 60+ band**, 15.96% against 16.54%, plus emergent stacking at 37% against the
   CFPB's 32%. Two independent checks the model was never tuned to.
3. **Implementation falsified the specification three times** (B15, B17, B18). A methodological
   contribution most theses cannot claim, because most never check.

---

## Order of work

`P0` (30 min, blocker) → **write Chapter 5 now**, since none of it changes when parameters change →
`P1` → `P2` → `P3` → `P4` → **then write Chapter 6 once**, against final numbers.

Do not draft Chapter 6 before P4 or it will be written twice.

**Supervisor questions**, in priority order:
1. Does the 16,000-word limit include appendices, tables and the bibliography?
2. Is a **negative result on RQ2** acceptable, given the registered fallback will have been run?
3. Which of the four validation targets can be demoted to an appendix?

Bring the robustness tornado figure. It makes the model's main vulnerability legible in seconds, and
having found it yourself is a much stronger position than having it found for you.
