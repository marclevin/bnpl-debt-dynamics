# The Thesis, Explained

**What this document is.** A plain-language explanation of what this project is, how the simulation
works, what it has found, and where it currently stands. It assumes no prior knowledge of the
project and defines its terms as it goes.

It has two parts:

- **Part One** is for the researcher. It teaches the project from the ground up.
- **Part Two** is a status report suitable for the supervisor.

> ## ⚠ Read this first
>
> **Every BNPL number in this document is from the first run (2026-08-12) and is superseded.** The
> model's two dominant parameters were rebuilt on 2026-08-13 and everything BNPL-on was re-run. The
> baseline, the data layer, and all the explanatory material below are still accurate.
>
> **For current numbers use [`STATUS.md`](STATUS.md)**, which is short. Two figures quoted below are
> now wrong and should not be repeated: the 4.3× amplification (now 1.6×) and the sensitivity
> ranking in §14 (both parameters have fallen to the bottom of it).

Last updated **2026-08-12**, after the first full experimental run.
Canonical strategy: [`OVERVIEW.md`](OVERVIEW.md). Defect register:
[`scratchpad/DEFECTS.md`](scratchpad/DEFECTS.md). Forward plan:
[`scratchpad/PLAN.md`](scratchpad/PLAN.md).

---
---

# PART ONE — For the researcher

## 1. The question, in one paragraph

**Buy Now Pay Later** (BNPL) is a way of paying for a purchase in instalments, usually four
payments over six weeks, with no interest charged. In South Africa the main providers are Payflex,
PayJustNow, Mobicred and TymeBank. The question this thesis asks is: **what does introducing BNPL do
to household debt and to the rate at which households default?**

"Default" here means a household reaching the point where it cannot pay for the things it must pay
for. The precise definition is given in §6.

## 2. Why this question is hard to answer with real data

BNPL arrived in South Africa at scale from about 2021. If you tried to measure its effect by
comparing 2019 with 2023, you would be measuring BNPL *plus* COVID-19 income shocks *plus* the 2020
credit contraction *plus* post-pandemic inflation, with no way to separate them.

So the thesis does something different. It builds a **simulated population of South African
households as they were in 2017** — a year when BNPL was effectively absent — checks that this
population behaves like the real 2017 population did, and then **switches BNPL on** and watches what
changes.

This is called a **counterfactual experiment**. It answers *"what would BNPL do to a household
population like this one?"* It does **not** answer *"what happened in South Africa after 2017?"*
That distinction has to be stated explicitly in the thesis, because a reader will otherwise assume
the second.

The advantage is control: because nothing else in the simulation changes when BNPL is switched on,
any difference in the results is caused by BNPL and nothing else. That is not achievable with real
data.

## 3. What an agent-based model is

An **agent-based model** (ABM) is a simulation containing many individual decision-makers, called
**agents**, each following its own rules, whose collective behaviour produces an outcome nobody
designed.

The contrast is with an equation-based model, where you write a formula for the whole economy. In an
ABM you write rules for *one household* and then run five thousand of them.

The point is **emergence**: outcomes that appear at the population level without being programmed
in. In this model, nobody tells households to hold loans at three different BNPL providers
simultaneously. That behaviour emerges from individual households each borrowing from whoever will
lend to them, combined with the fact that the providers cannot see each other.

**A caveat you should own rather than hide.** A strict definition of ABM requires agents to interact
with *each other*. In this model they interact only weakly: each household observes the *average*
behaviour of a group it belongs to, never another household individually. This is called
**mean-field** interaction. It is a legitimate and long-established form of ABM — Granovetter's
threshold models work exactly this way — but a demanding examiner could call the model a *dynamic
microsimulation with a feedback term* rather than a full ABM. The defence is that no South African
data exists on who influences whom, so building an explicit social network would mean inventing
several unmeasurable numbers.

## 4. The population: where the households come from

The simulated households are not invented. Each one is a real household from a real survey.

**NIDS** (the National Income Dynamics Study) Wave 5 is a nationally representative South African
household survey conducted in 2017. It records income, spending, debt, savings and demographics for
about 10,800 usable households.

**FinScope** is a separate South African survey about financial inclusion — whether people have bank
accounts, formal credit, savings products, and so on. The 2019 wave is used as a stand-in for 2017,
because no 2017 wave was available. Only *categorical* information is taken from it (banked yes/no,
has-credit yes/no), never money amounts, so no inflation adjustment is needed. The two-year gap is
recorded as a limitation.

Building the population took four steps:

1. **Backbone.** Derive each NIDS household's monthly income, committed spending, discretionary
   spending, savings and debt, all in 2017 Rands.
2. **Match.** For each NIDS household, pick a FinScope respondent with a similar income level in the
   same province, and copy across their financial-inclusion flags. This is called a **cell-donor
   match**: the "cell" is the income-quintile × province combination.
3. **Resample.** Draw 5,000 households from the 10,800, with each household's chance of being drawn
   proportional to its **survey weight** — the number of real households it represents. This makes
   the 5,000 nationally representative at a fixed, re-runnable size. They come from 3,250 distinct
   source households, so some appear more than once.
4. **Validate.** Confirm the 5,000 reproduce the survey's distributions and FinScope's national
   rates. Fourteen checks, all passing.

**Terms used throughout:**

- **Income quintile.** Sort all households by income per person and cut into five equal groups. Q1
  is the poorest fifth, Q5 the richest. The cut-points here are R900, R1,801, R3,400 and R7,712 per
  person per month.
- **Committed expenditure.** Food and rent. Treated as impossible to cut.
- **Discretionary expenditure.** Everything else. Can be cut to zero under pressure.
- **Banked.** Has a bank account. **83.1%** of this population. This matters enormously, because
  BNPL requires a bank card, so it caps who can use BNPL at all.

## 5. Money in, money out: the household balance sheet

Every household agent has a **balance sheet**, which is just an organised list of what it has and
what it owes:

| | |
|---|---|
| **Money in** | monthly income, and which source it mostly comes from (wages, government grants, other) |
| **Money out** | committed expenditure (food, rent), discretionary expenditure |
| **What it owns** | liquid savings — a cash buffer. The median household has just **R90**. |
| **What it owes** | traditional debt, and the monthly repayment on it |

**One number had to be constructed rather than measured.** Neither survey records how much
households actually repay each month. So it is calculated: take the debt, apply the legal maximum
interest rate for that type of credit, spread it over a typical term, and then cap it at what the
law says the household can afford. The interest rates are the **statutory maximum** rates set under
the National Credit Act — 21% for store cards, 28% for personal loans, and so on, at 2017's 7% repo
rate. These are ceilings rather than observed averages, which biases repayments upward; that is
recorded as a limitation.

## 6. How the simulation runs

### The clock

The simulation advances in **ticks** of **14 days**. It runs for **52 ticks**, which is 24 months.
The first **12 ticks are discarded** as **burn-in** — the period during which the model settles from
its artificial starting state into its normal behaviour. Only what happens after tick 12 is
analysed.

Fourteen days was chosen because BNPL instalments fall every two weeks. This turned out to be
luckier than intended: Payflex's actual product charges 25% at checkout and 25% every fortnight, so
BNPL payments land *exactly* on tick boundaries with no rounding error anywhere.

Because monthly survey figures must be converted to fortnightly ones, all money flows are multiplied
by **12/26** — twelve months per year divided by twenty-six fortnights.

### The seven steps of a household's tick

Every household, every tick, does this in order:

1. **Income arrives**, possibly reduced by a job loss (§7).
2. **Committed expenditure is paid first.** Food and rent outrank debt.
3. **Debt repayment is attempted.**
4. **Discretionary spending is set** from whatever cash remains.
5. **If short at step 2 or 3, the household seeks credit.**
6. **The household observes how many of its peers are using BNPL**, and its appetite for a BNPL
   purchase adjusts accordingly.
7. **Balances, arrears and distress counters update.**

**The order is a deliberate modelling decision, not an implementation detail.** Two features carry
the argument:

- **Food before debt.** If debt were paid first, a household could never fail to pay its debts —
  default would be impossible by construction. Putting consumption first is what makes default
  possible, and follows Madeira's study of Chilean household credit.
- **Borrowing last.** Credit is a response to a shortfall that has already happened. Placing it at
  step 5 is what allows a household to *borrow in order to repay*, which is the debt spiral the
  thesis exists to observe.

### Who else is in the simulation

- **One traditional lender**, representing the formal banking sector. It does not learn or adapt. It
  applies one legal test (§8) and either lends or does not.
- **One credit bureau**, holding the credit records the lender consults.
- **Four BNPL platforms**, switched off in the baseline and switched on for the experiment.

## 7. The income shock: what pushes households into trouble

Households need something to go wrong, or nothing interesting happens. In this model the thing that
goes wrong is **job loss**.

Each employed member of a household can lose their job in any tick, with probability `p`. If they
do, the household loses **that person's share of its wage income** — not all of it. A two-earner
household losing one job loses roughly half its wages. The number of employed members per household
comes from the NIDS individual records, so the size of the loss is **measured, not assumed**.

Unemployment **persists**. Someone who loses a job regains one with probability **1.87% per tick**,
which comes from official statistics showing that 11.6% of unemployed South Africans found work in
the following quarter in 2017. South African unemployment is extremely persistent, and the model
reflects that.

Households whose income is mainly **government grants** are exempt, because grants are statutory
payments that do not depend on employment.

## 8. The legal test at the centre of the model

Under South African law, a lender must check that a borrower can afford a loan. Crucially, the
**National Credit Act prescribes no debt-to-income ratio**. What it prescribes is a **residual
income test**: a table of minimum living costs by income band, with credit affordable only from
what is left over.

```
gross income − minimum living costs − existing visible debt payments  ≥  the new repayment
```

This produces a ceiling that varies with income: a household earning R900 a month can afford about
**10.4%** of its income in debt repayments, while one earning R7,712 can afford **83.2%**. A flat
percentage cap would have been wildly too generous at the bottom.

The exact same function is used in two places — building the population's repayments and deciding
whether the lender grants a loan — so they cannot disagree.

## 9. The mechanism the whole thesis is about

Here is the core idea, and everything else exists to support it.

**BNPL falls outside the National Credit Act.** Because no interest is charged, providers argue the
Act does not apply. The consequences are:

- BNPL providers need no credit licence.
- They need not perform the affordability test of §8.
- **They do not report to credit bureaux.**

So in the model, when the bank consults the credit bureau, it sees traditional debt — and **nothing
else**. A household can owe money to four BNPL providers, and the bank's affordability calculation
will not include a cent of it.

The bank is not behaving badly. It is following the regulation correctly, using the record the
regulation gives it. That is exactly the point.

**And the BNPL providers cannot see each other either.** With no shared reporting infrastructure,
there is no channel through which one provider could learn about another's exposure. This is not an
extra assumption — it follows directly from the absence of reporting. It is what makes **stacking**
possible: holding several BNPL debts at once, each invisible to the others.

## 10. The social channel

Households in this model influence each other in exactly one way.

Each household belongs to a **reference group** — everyone in the same income quintile in the same
province. There are **45 such groups**, the smallest with 23 households.

Each tick, a household observes **what share of its reference group is currently using BNPL**, and
its own appetite for a BNPL purchase rises with that share:

```
appetite = base appetite + beta × (share of my group using BNPL)
```

`beta` measures how strongly peers matter. This is included because the evidence says BNPL uptake is
socially driven — people choose it partly because they expect their social circle to approve.

**Three things make this defensible:**

1. The group share used is the one from the **end of the previous tick**. Every household therefore
   sees the same, already-settled number, so the results do not depend on the order in which
   households happen to act. This was confirmed empirically: switching between three different
   ordering rules changes the default rate by 0.18 percentage points.
2. **`beta = 0` switches the channel off entirely** and recovers a model of completely independent
   households. This is the **control arm**, and it is reported alongside every result.
3. With BNPL switched off the share is always zero, so the channel is **inert in the baseline** and
   cannot contaminate the calibration.

Reason 2 matters for honesty. The peer channel was added partly *because* one research question
asks about a threshold effect, and thresholds need feedback to exist. Reporting "we found a
threshold" after adding the very mechanism that produces thresholds would be circular. Always
showing the `beta = 0` row is what prevents that.

## 11. Calibration versus validation

These two words get used interchangeably in ordinary speech. In modelling they mean opposite things,
and the difference decides how much your results are worth.

- **Calibration** is *tuning* a parameter until the model matches a known number. You have not tested
  anything — you have adjusted the model until it agreed with you.
- **Validation** is *checking* the model against a number you did **not** tune to. This is a real
  test, and the model can fail it.

This model has **two calibrated parameters**:

- `shock_prob = 0.048` — the job-loss rate, tuned so 90+ day arrears match the regulator's figure.
- `payment_friction = 0.09` — the chance of missing an affordable payment through inattention, tuned
  so 1–30 day arrears match.

Everything else is a genuine test. Here is the arrears profile against the **NCR Consumer Credit
Market Report** for the first quarter of 2017 — the regulator's official statistics:

| How overdue | Model | Regulator | Was it tuned? |
|---|---|---|---|
| Up to date | 74.4% | 71.6% | **no** |
| 1–30 days | 8.4% | 8.2% | yes |
| 31–60 days | 1.3% | 3.6% | **no** |
| 61–90 days | 1.2% | 2.3% | **no** |
| 90+ days | 14.8% | 14.2% | yes |
| **60+ days** | **16.0%** | **16.5%** | **no** |

**The 60+ day row is the single best result in the thesis.** Two parameters were tuned to two other
numbers, and this one came out right on its own.

**Two honest caveats.** The regulator counts *accounts*; the model counts *households*, and one
household may hold several accounts. And 56% of households in this population hold no traditional
debt at all, so they can never be in arrears — which is why the comparison uses only households that
actually hold debt. Both facts must be stated wherever the table appears.

## 12. Three further tests the model was not tuned to

**Test 1 — does BNPL make traditional debt worse or better?** A large American study found that
after people start using BNPL, their credit-card interest and late fees go *up*. If this model
showed traditional debt getting *easier* when BNPL is switched on, its rules would be contradicting
the best available evidence. **Result: BNPL raises traditional arrears by 3.9 percentage points with
the peer channel off and 10.5 with it on. Passes.** Caveat: the direction is partly designed in,
because the rules were chosen so BNPL is not a pure substitute. The *size* of the effect is not.

**Test 2 — do middle-income households carry the most debt relative to income?** A UK study found
this pattern. **Result: passes**, but with an important story attached.

The first attempt said it failed, with the poorest fifth apparently carrying the most debt. That was
wrong — not about the households, but about the *statistic*. Debt-to-income explodes when income is
near zero, and it turned out the **top 1% of Q1 households carried 77% of that group's total**,
while the *median* Q1 household had a debt-to-income ratio of exactly zero. An average of ratios was
meaningless here.

The fix was to change the statistic, not the data: use the **aggregate ratio** (total debt divided by
total income within each group), which is the standard measure in financial-stability work and
cannot be blown up by one tiny denominator. On that measure the peak is at Q4, with the richest
group lowest — the expected pattern.

**All 5,000 households were kept**, including the 33 whose debt no lawful lender could have granted.
Removing them would also have flipped the result, which is precisely why they stayed. Deleting
inconvenient data to make a test pass is exactly the error this project has avoided elsewhere.

**Test 3 — how many households run out of savings?** A consumer survey found 36% of South Africans
expected to miss a bill payment. **Result: about 45% reach zero savings.** Same order of magnitude,
somewhat high.

## 13. What the experiments found

Three research questions, and 3,304 simulation runs.

> **⚠ The research questions were renumbered on 18 August 2026** for the 10,000-word limit. The
> authoritative set is in the thesis introduction; see
> [`scratchpad/SCOPE_REDUCTION.md`](scratchpad/SCOPE_REDUCTION.md) §4. In brief: **RQ1** is now
> whether the synthetic population reproduces behaviour it was not fitted to; **RQ2** absorbs the
> old RQ1 and RQ2 into *do households stack facilities, and does default rise*; **RQ3** is
> unchanged. The findings below are correct — only the labels have moved. The old RQ1 heading maps
> to the stacking half of the new RQ2, and the old RQ2 heading to its non-linearity half.

### Old RQ1 — When does debt stacking become self-reinforcing?

Households do accumulate BNPL debts across several providers, and this is **emergent** — never
programmed. At full access, **37% hold two or more BNPL facilities at once**, against an American
regulator's finding of 32% holding loans across different firms. Close, and it was never tuned.

### Old RQ2 — Does default rise suddenly past some level of BNPL access?

The registered expectation was that default would respond *non-linearly* — smoothly at first, then
sharply — but only when the social channel is switched on.

**This is not what happened.** Every case is close to a straight line, including the control arm
with the social channel off (a straight line explains 99.92% of it).

What *is* strongly supported is **amplification**: the social channel multiplies the effect of BNPL
access by **4.3×**. Same shape, four times as steep.

This is a legitimate finding, and arguably a cleaner one, since it is a claim about magnitude that
the control arm identifies precisely. But the registered plan anticipated this: if simple peer
coupling produced only a smooth response, a second mechanism — **Granovetter's heterogeneous
thresholds**, where each household has its own tipping point — should be tried before concluding no
threshold exists. That has not been run yet. Not running it would look like avoidance, and a linear
rule producing a linear result is weak evidence of anything.

### RQ3 — Do interventions stop BNPL borrowing, or merely postpone it?

Measured by total BNPL borrowing over the whole period. Unchanged total with later timing means
households **defer**; a lower total means they **desist**.

Four policies tested. The result is more interesting than a ranking:

| Policy | Social channel off | Social channel on |
|---|---|---|
| Make BNPL visible to credit bureaux | **no effect** | **no effect** |
| Require an affordability check on BNPL | default 32.9% → **28.1%** | overwhelmed |
| Cool-off period after a purchase | almost nothing | default 56.1% → **39.9%**, borrowing −58% |

**Transparency alone does nothing.** This is the model's most striking result, and it makes sense
once seen. Making BNPL visible to the bureau only constrains *the bank*. It does nothing to whether
BNPL providers will lend, nothing to their blindness to each other, nothing to the household's
desire to buy. Households keep stacking BNPL; they are simply refused additional *bank* credit.

**The two effective policies work on different problems.** An affordability requirement stops
individuals borrowing more than they can repay, but is swamped once social transmission takes over.
A cool-off period barely dents individual impulse but is highly effective against social
transmission, because delaying purchases lowers the group's usage rate, which lowers everyone
else's appetite — it acts as a circuit breaker on the feedback loop.

⚠ **The numbers in this table are superseded.** Two things happened on 2026-08-12.

The **off-by-one has been fixed**. The arm representing the *statutory* 14-day cool-off was a no-op
— it reported exactly zero effect because it blocked nothing — and now blocks correctly. The test
that missed it has been replaced by one that cannot: it demands the cool-off *strictly reduce* the
number of purchases, rather than merely not increase the amount borrowed.

But the expected corrected figures (−2.6% and −30.4%) are **no longer reliable predictions**,
because the same pass changed the purchase size, the spending limit and the checkout rule underneath
them (§14). Every number in this section arrives fresh with the re-run.

## 14. What is actually driving the results — and the main vulnerability

Every uncertain input was swept across a plausible range to see how much it changes the answer:

| Input | How much it moves default | How well sourced |
|---|---|---|
| BNPL purchase size | **19.6 points** | trade press only |
| BNPL spending limit per provider | **16.9 points** | **no provider publishes one** |
| How much a household borrows when short | 7.5 points | no source found |
| Default definition (98 vs 56 days) | 2.7 points | sourced |
| Share of minimum-only payers | **0.25 points** | sourced |
| Minimum payment formula | **0.21 points** | no source found |
| Order households act in | **0.18 points** | sourced |

**The good news.** Three worries turned out to be nothing. Two rules with no citation behind them
barely affect the answer at all, and the theoretical prediction that ordering would not matter is now
confirmed by measurement rather than asserted.

**The bad news, and it is the main vulnerability.** The two biggest drivers are the two worst-sourced
inputs. A more advanced technique called **Sobol analysis** — which apportions the variation in
results across inputs and, unlike one-at-a-time sweeps, detects *interactions* — confirmed this and
added something the simple sweep could not see: **two-thirds of the purchase-size effect comes from
interactions with other inputs**, meaning it does not just shift results, it changes how everything
else behaves.

**This has now been fixed, and the diagnosis turned out to be incomplete.** "Worst-sourced" was only
half of it. Both parameters were also **flat national constants applied to a population with a Gini
of 0.67**, and the numbers make the problem obvious: R1,568 imposed on every household is **127% of
the median banked Q1 household's entire monthly discretionary budget** and 11.4% of Q5's, while the
R5,000 spending limit is **217% of Q1's monthly income — at each of four providers independently**.
A constant that is non-binding at the top and absurd at the bottom will dominate a sensitivity
ranking whatever its citation says.

Three things changed on 2026-08-12:

1. **Purchase size is now derived from each household's own budget.** A purchase is drawn around
   **13.87% of that household's monthly discretionary spending** — the share South African
   households actually spend on the things BNPL finances (clothing and footwear, furniture and
   appliances, phones and electronics, sporting goods), computed from Statistics South Africa's
   Income and Expenditure Survey. Only a *ratio* is taken from that survey, never a Rand amount, so
   its 2022/23 vintage cannot contaminate a 2017 model — the same argument already used for the
   FinScope data.
2. **The level became a test the model can fail, and it passed.** PayJustNow's parent company is
   listed, and discloses both cumulative BNPL sales (R13.1bn) and cumulative transactions (9.4m).
   Dividing one by the other gives an average purchase of **R992** in 2017 Rands. The old
   trade-press figure works out at R1,038. The model, whose scale was set by the expenditure survey
   and by nothing else, produces **R1,029**. Three numbers from wholly independent sources, within
   5% of each other, with nothing tuned to anything.
3. **The spending limit is now a quarter of each household's monthly income**, rather than R5,000
   for everyone. No provider publishes a limit, but HomeChoice's audited annual report describes a
   "low and grow" policy — limits start low and rise with good repayment — which licenses a limit
   that depends on the customer. The value is *reported against* an external range implied by UK and
   Australian regulators (roughly 10–26% of monthly income per provider), not fitted to it.

**A fourth problem surfaced while fixing these, and it was embarrassing.** Every BNPL money figure
in the model — the purchase size, the R15,000 order cap, the R95-per-week late fee — was taken from
providers' *current* published terms and used unadjusted in a model where everything else is in 2017
Rands. South African prices rose about 44% over that gap, so the BNPL side of the model was
denominated roughly 1.4 times too high against the households it was lending to. That is now
corrected with a single documented inflation factor.

⚠ **What this does to the results is not yet known, and it may be substantial.** Early single-run
checks show population default falling from 32.9% to 27.5% with the social channel off, and from
56.1% to 28.0% with it on. Adoption still responds strongly to peer influence, but default now
barely does — which puts the **4.3× amplification finding of §13 in question**. The full re-run
settles it.

## 15. How confident should you be?

Honestly:

**Trust these.** The model is verified — 65 automated tests confirm it does what it is specified to
do, including that switching BNPL off exactly reproduces the baseline and that the control arm
exactly reproduces an independent-household model. The unfitted 60+ arrears match, the emergent
stacking figure, and the direction of every result are all sound.

**Treat these as directional.** The *sizes* of the BNPL effects depend heavily on two poorly-sourced
inputs. Report them as conditional on those inputs, not as forecasts.

**Do not quote these.** The extreme cases — strongest social influence, full access — produce
implausible amounts of BNPL borrowing: about R31,000 per household over two years against a median
household income near R4,800 a month. Real adoption is around 20% by survey evidence. Restricting to
realistic adoption levels gives a BNPL effect of **+4 to +17 percentage points** on default against a
24.6% baseline, rather than the headline 56%.

⚠ **Superseded, and now measurable rather than merely doubted.** The implausibility above was an
assertion; the model had no external benchmark for *how much* BNPL a household should borrow. It now
does. HomeChoice discloses that BNPL customers make **2.12 purchases a year**, which combined with
the R992 average purchase gives about **R2,100 per user per year** in 2017 Rands. That is the yardstick
the R31,000 figure should have been held against all along. After the §14 fixes the model's own
figure falls to roughly R3,700 per eligible household with the social channel off — the right order
of magnitude at last — and about R13,300 with it on, which is still high and still needs the caveat.

**One weakness with no easy fix.** The job-loss rate needed to reproduce real arrears is about **four
times** the real rate. This is a like-for-like comparison, so it cannot be explained away. The reason
is structural: this model has essentially one thing that can go wrong, while in reality households
fall behind because of illness, unexpected bills, rate rises and family changes as well. One channel
is doing the work of several. This belongs in the limitations chapter, stated plainly.

---
---

# PART TWO — For the supervisor

## Status

The agent-based model is **built, verified, calibrated, and has produced a first full set of
results**. This closes the project's standing blocker.

**Since that first run, a quality-assurance pass has closed the project's principal methodological
weakness and found three further defects** (2026-08-12; §14). The two parameters that drove the
model's output are now derived from South African data and externally validated; a budget constraint
that was not being enforced is enforced; and every BNPL monetary parameter has been converted into
the 2017 Rands the rest of the model uses. Verification has grown from 65 tests to 79, all passing.

**The baseline is unaffected** — the two calibrated parameters are fitted with BNPL switched off, so
there is no re-calibration and the arrears validation stands as reported. **But every BNPL result in
this document is now provisional**, and the magnitudes may move substantially. The remaining work is
one design decision, one pre-registered robustness check, the re-run, and the write-up.

**Repository:** `github.com/marclevin/bnpl-debt-dynamics`, all work committed and pushed.
**Reproducibility:** pinned environment, seeded runs, extraction scripts that assert their source
documents' own published figures.

## What was completed

**The model.** Implements all seventeen documented submodels on Mesa 3.5.1. Five thousand household
agents derived from NIDS Wave 5, one non-adaptive lender applying the National Credit Act
Regulation 23A residual-income test, a credit bureau holding traditional debt only, and four BNPL
platforms that cannot observe one another. Fourteen-day time step, 24-month horizon, all values in
2017 Rands.

**Verification.** Sixty-five automated tests, all passing. These include degenerate-case
reductions — with the peer channel disabled the model reproduces an independent-agent model exactly;
with BNPL disabled it reproduces the baseline bitwise; with one platform stacking collapses — plus
confirmation that the statutory affordability table reproduces both worked examples published in the
regulations, and that BNPL instalments and late-fee caps match the providers' published terms.

**Calibration.** Two parameters fitted to two separate arrears bands, deliberately leaving three
bands as independent checks.

**Experiments.** 3,304 runs: 2,280 across the three research questions and a robustness suite, plus
1,024 for a Sobol global sensitivity analysis.

## Principal results

**1. The baseline reproduces an arrears band it was not fitted to.** Sixty-plus-day arrears come out
at 16.0% against the regulator's 16.5%. Two parameters were fitted to two other bands; this one is
independent.

**2. Cross-provider debt stacking emerges at a realistic rate.** 37% of users hold two or more
concurrent facilities, against 32% in comparable US regulatory data. This is emergent, never imposed,
and never fitted.

**3. Enabling BNPL increases stress on traditional debt.** Traditional arrears rise 3.9 to 10.5
percentage points, consistent with the causal literature. This was the pre-registered falsification
test; the model passes it. The direction is partly built into the rules and this is disclosed; the
magnitude is not.

**4. Transparency alone is ineffective. This is the most policy-relevant finding.** Making BNPL
obligations visible to credit bureaux — the intervention the model was principally designed to
evaluate — changes population default by 0.08 percentage points. Requiring an affordability
assessment on BNPL reduces it by 4.9 points. Disclosure constrains only the traditional lender; it
does not touch BNPL origination, provider mutual blindness, or household demand. It changes who
lends, not how much debt is taken on.

**5. Interventions address different failure modes.** An affordability requirement is effective
against individual over-borrowing but is overwhelmed once social transmission is active. A cool-off
period is nearly useless against individual impulse but reduces borrowing by 58% where social
transmission is present, by damping the feedback loop. This suggests the two instruments are
complements rather than alternatives.

## Results requiring careful handling

**RQ2's registered hypothesis is not supported.** Population default responds to BNPL access in a
manner statistically indistinguishable from linear in every configuration, including the control arm
(linear fit R² = 0.9992). What *is* strongly supported is amplification: social transmission
multiplies the response 4.3-fold.

The design register pre-registered a contingency for exactly this outcome — a Granovetter
heterogeneous-threshold formulation as a structural robustness check. **We propose to run it before
finalising RQ2.** A linear coupling rule producing a linear response is close to tautological, so the
current negative result is weakly evidenced. Either outcome is reportable: a threshold gives RQ2 an
affirmative answer, and its absence under two structurally distinct mechanisms is a considerably
stronger negative than the present one.

**One defect is outstanding and affects RQ3.** The arm representing the statutory 14-day cool-off is
a no-op due to an off-by-one error, so it currently reports zero effect for the statutory instrument.
The corrected result is expected to show −2.6% borrowing without social transmission and −30.4% with
it. This inverts the reported conclusion about the statutory figure and is a blocker for writing RQ3.
Approximately half an hour of work; logged as B27.

## Principal methodological weakness

Sensitivity analysis establishes that the two most influential parameters are the two least
well-sourced: **BNPL purchase size**, which rests on a trade-press figure, moves population default
by 19.6 percentage points across a plausible range; and the **per-provider spending limit**, which no
South African provider publishes, moves it by 16.9 points. Sobol decomposition confirms this and
shows two-thirds of the purchase-size effect operates through interactions with other parameters.

**This has been addressed, and the analysis that fixed it produced a better result than expected.**
Both parameters are now ratios applied to household characteristics rather than flat national
constants. Purchase size is set by the share of discretionary expenditure South African households
devote to BNPL-financeable categories, derived from Stats SA's Income and Expenditure Survey
2022/23; the per-provider limit is a multiple of household income, with its functional form taken
from HomeChoice's audited "low and grow" credit-risk disclosure and its magnitude reported against a
band implied by the Woolard Review and ASIC.

The unplanned finding is that **the purchase-size level can now be validated externally, and it
passes**. PayJustNow's parent is listed and discloses cumulative BNPL gross merchandise value
(R13.1bn) and cumulative transactions (9.4m); their quotient is an average order value of R992 in
2017 Rands. The trade-press figure deflates to R1,038, and the model — whose scale is fixed by the
expenditure survey alone — produces R1,029. Three independent sources within 5%, none fitted to
another. A quantity that was the thesis's principal weakness is now one of its better-evidenced
inputs, and the model has gained a validation target on BNPL *volume*, which it previously lacked
entirely.

Approaching providers directly was not necessary and remains low-yield.

**A fourth specification defect surfaced during the same pass and is worth reporting rather than
quietly fixing.** Every BNPL monetary parameter — purchase size, the R15,000 per-order cap, the
R95-per-week late fee — was taken at current vintage and used unadjusted in a model denominated
throughout in 2017 Rands, a discrepancy of roughly 44%. This is the cleanest of the four
implementation-falsifies-specification cases below, because the specification was not silent on the
point; it contradicted a convention stated explicitly elsewhere in the same document.

⚠ **We do not yet know what this does to the results, and it may be material.** Preliminary
single-run checks show population default falling from 32.9% to 27.5% with social transmission off
and from 56.1% to 28.0% with it on — meaning the 4.3× amplification result reported above is itself
now uncertain. Adoption continues to respond strongly to peer influence; default appears not to. The
full re-run is the next step and no magnitude in this document should be quoted until it completes.

Two secondary limitations are disclosed rather than resolved. The job-separation rate required to
reproduce observed arrears is approximately four times the rate in official labour-force statistics,
on a like-for-like basis; the model carries a single stress channel where reality has several, and
the shock parameter absorbs the difference. And agent interaction is mean-field rather than networked,
because no South African data exists to calibrate a contact network.

## A methodological result worth reporting

Building the model, and then subjecting it to a quality-assurance pass, falsified **four** elements
of a specification that had been reviewed and signed off on paper:

- The income shock was specified as lasting a single time step. That specification could not move the
  arrears rate it was designated to be fitted to — sweeping the parameter across its entire range
  moved the target statistic by 0.34 percentage points against a required 14. Re-reading the cited
  source showed it models unemployment *spells*, not momentary shocks.
- The validation comparison used a denominator including households holding no debt, who cannot by
  definition be in arrears. This introduced a factor-of-2.3 discrepancy with no behavioural content.
- One rule specified the *proportion* of households making minimum-only payments without ever
  defining what the minimum was.
- Every BNPL monetary parameter was specified at the providers' current published prices, in a model
  the same specification states is denominated in 2017 Rands throughout — a discrepancy of about
  44%. This is the strongest of the four, because the specification was not silent on the point: it
  contradicted a convention it had itself set out, and the contradiction survived a full design
  review, an implementation, 65 passing tests and a complete experimental run.

None of these were visible on paper. We suggest this is worth a short passage in the methodology
chapter as evidence for implementation and quality assurance as verification steps in their own
right, rather than presenting the corrections as errata.

## Decisions requested — all settled 18 August 2026

1. **Word limit and what counts.** The limit is **10,000 words, not 16,000**. Appendices, the
   bibliography, tables and figures are all **excluded**; only body prose counts. The reduction was
   carried out accordingly, and the primary tool was converting prose to tables rather than deleting
   material. See [`scratchpad/SCOPE_REDUCTION.md`](scratchpad/SCOPE_REDUCTION.md).

2. **A negative result on RQ2 is acceptable** and is reported prominently — named in the abstract
   and as a titled finding. The pre-registered Granovetter threshold variant has been run and also
   returns a negative, so the claim is "no threshold under two structurally distinct social
   mechanisms".

3. **The four validation targets are reduced in prominence.** The two strong independent ones, the
   60+ day arrears band and the average purchase size, are foregrounded; the two weaker ones are
   demoted to a table.

4. **The research questions were free to change** and have been restructured. The authoritative set
   is in the thesis introduction.

## Remaining work

| | | |
|---|---|---|
| Fix the cool-off defect | 0.5 hours | **done** 2026-08-12 |
| Derive purchase size and spending limits | 2–3 days | **done** 2026-08-12, in under a day |
| Enforce the checkout budget constraint; deflate to 2017 Rands | — | **done**, both found in the same pass |
| Decide the reference-group denominator for the threshold arm | 0.5 hours | **open** — blocks the next item |
| Granovetter threshold variant for RQ2 | 1 day | not started |
| Final experimental run and publication-grade sensitivity analysis | ~2 hours compute | not started |
| Write-up: implementation, results, conclusions | the critical path | not started |

The parameter work is complete and the verification suite has grown from 65 to 79 tests, all
passing. **The sequence matters and is not negotiable**: the threshold variant must be built and run
*after* the parameter changes, not before, because the sensitivity analysis showed that two-thirds
of purchase size's influence operates through interactions with other parameters — so a "no
threshold found" result obtained under the old flat purchase size would not transfer, and an
examiner would be right to ask whether it survived.

One decision is outstanding and blocks the threshold work. The model measures peer influence as the
share of a household's reference group currently using BNPL, counted over *everyone* in that group
including the unbanked and those without access. That share therefore has a ceiling — and the
ceiling is proportional to the BNPL access rate, **which is the very quantity RQ2 sweeps**. At 15%
access, no household whose tipping point sits above about 0.125 could ever be triggered, anywhere.
Sweeping access would then move the maximum attainable peer signal at the same time as it moves
access, and the threshold model would show a response that is partly an artefact of that — which is
indistinguishable from the finding the test is meant to detect. Under the current linear rule this
is harmless, because the effect is absorbed into the peer-strength parameter. The recommended fix is
to measure the share against those who *could* use BNPL rather than against everyone, which is
arguably what a household observes anyway; it also requires re-running the linear arm, which is
free given everything is being re-run.

**The binding constraint is still the write-up.** Draft the implementation chapter now — none of its
content depends on the outstanding decision — and defer the results chapter until after the final
run, so it is written once.
