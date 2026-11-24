# Term ledger

Once the thesis names something, every later mention uses that name, in the body, the tables,
the captions and the appendices.

The ledger was built from the text at `81e6ee9` (2026-11-24). Section numbers point to where
the term is defined. When the thesis changes, this file changes in the same commit.

## How to use it

- **Writing.** Before naming a model object, a group, a measure or an experiment, find it here
  and copy the term exactly.
- **A new thing.** If it is not here, it needs a name. Choose one, define it in one sentence at
  first use, add a row here, and add its likely drift forms to `rules.tsv`. Then use only that
  name. Never introduce a second label "for variety".
- **A new arm.** Name it by what changes, as a noun phrase that can be a table row ("platform
  cap", "cooling-off window", "mandatory screening"). Say what it does in one sentence in the
  section that reports it, add it to `tab:experiments`, and use the same phrase in the table row,
  the caption and the text. Pick one of "screen", "test" and "check" and keep it: the lender
  applies a "test", the platforms a "screen".
- **A fixed framing.** Section "Fixed sentences" lists wordings the thesis repeats on purpose.
  Reuse them word for word; do not paraphrase them.

## Actors and institutions

| Write | Meaning, and where defined | Do not write |
|---|---|---|
| household | The modelled unit, 5,000 of them (Section 2) | agent, consumer, borrower, user, individual. "Agent" stays in "agent-based model", the data-to-agent tables and Appendices D to G. "Consumer", "borrower", "user" only for a cited source's own population |
| platform | A BNPL seller in the model; four in the benchmark | BNPL lender, BNPL firm, fintech. "Provider" is for real firms and sources only |
| the traditional lender, then "the lender" | The one aggregate lender of traditional debt | the bank, formal lender, registered lender, regulated lender. "Banked" is the eligibility flag |
| traditional debt | Everything the lender grants | formal credit, bank debt |
| the credit bureau, then "the bureau" | What the lender's test sees | credit registry |
| agreement | One BNPL contract | BNPL loan, plan, facility, order ("order" is one request, as in "order cap") |
| instalment; pay-in-four | | installment, pay-in-4 |
| loan | Traditional lender only, or a cited source's term | |

## Time

| Write | Meaning | Do not write |
|---|---|---|
| tick | 14 days (Section 2). 52 ticks is two years | period, step, round, iteration. Before Section 2 (abstract, introduction) write days and "two years" |
| the run | One simulation of 52 ticks; also its two-year span ("default during the run") | simulation, trajectory |
| two-year horizon | Scope of every result | long run, steady state |

## States and thresholds

| Write | Meaning | Do not write |
|---|---|---|
| arrears | Unpaid instalments. "In arrears" for the CCMR bands | overdue, delinquent, late, behind (four old "90 days behind" survive; add no more) |
| past due | Age of an unpaid instalment: "more than 90 days past due" | |
| default | "A household defaults when an instalment on any of its credit, BNPL included, is more than 90 days past due." In the model: arrears age of seven ticks, 98 days | impaired (NCR's word, only when quoting the Monitor) |
| write-off (noun), written off (verb) | A defaulted account leaving the book | charge-off |
| arrears rule | The current default rule | |
| streak rule | The rule it replaced. Name it when citing an "earlier rule" result | "the earlier rule" with no name |
| credit-active | Owing any traditional or BNPL balance or arrears (Section 2) | indebted (a different set in Appendix D) |
| non-performing | A defaulted account under the arrears rule | frozen (code name) |

## Money gaps and the group that drives the result

| Write | Meaning | Do not write |
|---|---|---|
| shortfall | Cash a household lacks in a tick before borrowing (Section 2) | gap, deficit, short of cash (three old uses survive) |
| committed expenditure | Food and rent (Section 2) | committed spending, essentials, necessities, necessary expenses (the last is Regulation 23A's statutory table, a different thing) |
| short of food and rent | The outcome: committed expenditure unpaid after borrowing. About 3.4% of households in a tick | |
| consumption distress | The name of that measure | |
| households short from the start | The group: surveyed income does not cover committed expenditure. 3.6% of households, 182 of 5,000 (Section 3.5) | the very poor, poor households, deficit households, structurally short. Do not confuse with the outcome above |
| households not short from the start | Everyone else | other households (only after the group is named in the same paragraph) |
| surveyed income | Income as NIDS records it | reported, stated, declared income |
| "possibly understated" | The standing hedge on that income: for about two-thirds of the group's respondents, the answer to a single income question covers food and rent | |
| the shortfall path | Borrowing with BNPL against a shortfall | route, pathway, channel for this meaning ("routing" is the order in which a household tries platforms) |
| want-driven purchase | The other use of BNPL: a purchase not prompted by a shortfall | discretionary, impulse, voluntary purchase |

## Outcomes and uncertainty

| Write | Meaning | Do not write |
|---|---|---|
| default during the run | Share of all households that default in the 52 ticks. 14.37% without BNPL (Section 3.1). "Default" alone means this | default rate, population default (survives in frozen RQ2 and two older places) |
| default including the starting stock | Adds households already in default at the start: 20.73% | |
| the BNPL effect, then "the effect" | Difference in default during the run, BNPL arm less baseline, paired by seed | impact, treatment effect |
| points | A difference in a rate, in the text. "pp" in table headers. `\%` for a level | percentage points (once in the abstract, once where Section 3.1 states the convention), per cent |
| `$X \pm Y$ points` | Estimate and one standard error, paired by seed (Section 3.1) | confidence interval for an effect, p-value, stars |
| detectable | Exceeds two standard errors (Section 3.1). Tables print it in bold. Forms: "not detectable", "does not change detectably", "no detectable slope", "do not differ detectably" | significant, insignificant, no effect, negligible |
| replicates; seeds; seed block | Runs of one arm; their random seeds; a set of seeds used together | repetitions, trials, samples |
| pooled by inverse variance | How blocks are combined | averaged |
| simulation variance | What the standard errors measure, outside the redrawn population. The redrawn population's standard errors also cover the drawn population; say so by name each time | noise, sampling error |

## Experiments

| Write | Meaning | Do not write |
|---|---|---|
| the fixed population | The 5,000 households that every run except the redrawn population uses | benchmark population (the benchmark is an arm), canonical population |
| arm | One configuration of the model | treatment, condition, variant, specification |
| baseline | BNPL off | benchmark, base case, status quo |
| benchmark | BNPL on at the reference values, no switch or lever | baseline (the conclusion-level slip to avoid: "the baseline's 20.73%" beside the benchmark's figure) |
| reference (values, arm) | The comparison point inside a sweep | default values |
| control | The arm without the studied feature: β = 0 or γ = 0 | control group |
| switch | Bureau visibility; mandatory screening | policy, intervention, instrument |
| lever | Cooling-off window; platform cap | switch for these two; "lever" for all four |
| scenario | The Section 5 arms only | scenario for any other arm |
| sweep | A grid over one or two parameters | |
| the redrawn population | The design in which each replicate has its own population draw and derived separation rate, at β = 0 (Sections 3.1 and 4.1; `tab:effect-split`). Reported beside the headline as a check; the headline stays the pooled fixed-population estimate | resampled population (that is the fixed 5,000 of Section 3.2), bootstrap draw, bootstrap population, new population, population redraw, fresh population |
| population draw | One replicate's 5,000 households in the redrawn population. "Across population draws"; "the draws" after it is named | resample, bootstrap sample, redraw (noun), population sample |
| sensitivity | Headings and prose for varying an assumption | robustness |
| without BNPL; enabling BNPL | Prose | BNPL-free, BNPL disabled ("No BNPL", "BNPL off" are table labels) |
| without peer influence; with peer influence | β = 0; β = 0.3, in the abstract, Section 1, the RQ answers and Section 6 | "at β = 0" in those places |

## Rules, tests and caps

| Write | Meaning | Do not write |
|---|---|---|
| the Regulation 23A test, then "the lender's test" | The traditional lender's affordability test | affordability check, credit check, income check, credit gate in prose (the gate is the submodel's name) |
| light screen | What the platforms apply: banked and not in default. "The platforms' screen does not compare income with living costs" | eligibility check |
| the wage-income screen | The arm in which the platforms lend only to households with wage income (Section 4.1; `tab:effect-split`). Always in full where the light screen is also in play. It does not compare income with food and rent, so it is never an affordability test | income screen, wage screen, wage test, employment screen, income check, affordability test for this arm |
| wage income | Surveyed income from employment or self-employment (NIDS `w5_hhwage`), above zero. "Households with no wage income" | labour income, earnings, salaried, employed households (a household can have wage income and still be short from the start) |
| mandatory screening, then "screening" | The switch that applies the lender's test to BNPL requests | affordability screening (only in the frozen research questions and the Section 5 title), strict screening |
| bureau visibility, then "visibility" | The switch that shows BNPL to the lender's test | bureau reporting, "reporting raises default" |
| reporting arrangements | The real-world change in South Africa | bureau visibility for the real event |
| peer influence | β. "Peer adoption" appears only in frozen RQ2 | social influence, peer effect, contagion, herding |
| payment friction; arrears persistence | The two fitted parameters, always in full | friction alone on first use in a section |
| platform limit | λ: a balance of at most λ times monthly income per platform | cap, ceiling |
| platform cap | The lever on the number of platforms owed | stacking cap (code name), agreements cap |
| order cap; fee cap; shortfall cap; Regulation 23A payment cap | Four other caps, each always with its full name | "the cap" unless the paragraph has named it |
| cooling-off window | The other lever | waiting period |
| stacking | Owing two or more platforms at once | multi-homing, loan stacking |
| ever-holders; holders | Held a BNPL balance at some tick; hold one now. Stacking shares are of ever-holders | BNPL users (for a model share), adopters |
| routing (random, loyal) | The order in which a household tries platforms | |

## Parameters, calibration and validation

| Write | Meaning | Do not write |
|---|---|---|
| Observed, Constructed, Imported, Derived, Fitted, Assumed, Swept | The seven provenance classes (Section 3). The register uses sourced, derived, fitted, assumed | calibrated, tuned, estimated, free parameter |
| fitted | Only payment friction and arrears persistence, to the five CCMR bands | fitted for anything else |
| derived | Computed from other values (the separation rate, the write-off rate, κ) | set, calibrated |
| "is an assumption" | A value no source gives. Formula: "We found no X, so Y is an assumption." | "we assume" |
| calibration targets | The five CCMR arrears bands | fitted bands |
| external checks; Pattern 1 to 3 | Comparisons not used in fitting | validation tests |
| "by construction"; "checks consistency only"; "no independent check"; "weak evidence"; "supports orders of magnitude only" | The fixed verdicts on a comparison | validates, confirms, fits well, closely matches |
| starting stock; starting profile; starting arrears | State at the first tick | initial, opening (three old "opening debt service" survive) |

## Symbols

Give the plain name with the symbol at its first use in each section; the bare symbol is fine in
the next paragraph or two (Cochrane).

| Symbol | Name |
|---|---|
| β | strength of peer influence (linear rule). β = 0 is the control without peer influence; β = 0.3 is the largest value swept |
| γ | propensity step (threshold rule) |
| λ | platform limit, as a multiple of monthly income |
| κ | purchase ratio: mean want-driven purchase as a share of the monthly discretionary budget (0.139) |
| k | default threshold in ticks (seven) |
| s_g | lagged adoption share of the reference group; "the peer signal" |

Prose writes `$\beta=0$` with no spaces. Captions and table notes write `$\beta = 0$`.

## Research questions and structure

- "the main research question", then RQ1, RQ2, RQ3. Their wording is frozen. Do not reword them
  and do not suggest rewording them.
- Sections 3, 4 and 5 open "This section answers RQn." and close with a subsection "Answer to RQn".
  Those subsections are the only per-RQ summaries. The conclusion does not restate them.
- Top-level units are "Section~\ref{...}". "Chapter" never appears.
- Data sets by their acronym through `\ac{}`: NIDS (Wave 5, 2017), FinScope 2019, IES 2022/23,
  QLFS, the NCR's CCMR and Credit Bureau Monitor, SARB.
- Authors in full: "deHaan et al." (lower-case d), "Di Maggio et al.", "Keys and Wang",
  "the Woolard Review".

## Spelling and form

- British spelling: behaviour, labour, modelling, initialise, amortise, instalment, favour.
- No contractions, no "e.g.", no em dashes. An en dash joins number ranges only (`1--30 days`).
- Words for one to nine, digits for 10 and above; a number that opens a sentence is spelled out.
- Thousands as `5{,}000`. Money as `R862`, `R2{,}014`, "2017 Rands".
- Rates per tick as decimals (0.0575, 0.0187), not percentages.
- Hyphens: two-year (modifier), want-driven, pay-in-four, credit-active, cooling-off window,
  write-off (noun), seed-paired (modifier) but "paired by seed", debt service (noun) but
  debt-service (modifier), shortfall (one word).
- LaTeX quotes: ``like this''. References with a tie: `Section~\ref{}`, `Table~\ref{}`.

## Fixed sentences

Reuse these word for word. Each appears more than once in the thesis on purpose.

**An effect.** "[Enabling BNPL / Screening / Visibility] raises [lowers] default by `$X \pm Y$`
points at `$\beta=0$` and `$X \pm Y$` at `$\beta=0.3$` (Table~\ref{...})." The unit follows the
first value only. After a verb of direction the number is unsigned; after "is" or "at" it carries
its sign (`$+0.11 \pm 0.07$`).

**A null.** "... is `$+0.11 \pm 0.07$` points, not detectable." A null always carries its estimate
and standard error, and where it matters a power sentence: "so a true change of 0.26 points
would be missed about half the time."

**Many comparisons.** "Of the 20 contrasts, two exceed two standard errors. Two in 20 is about
what chance gives."

**What the experiments show.** "The experiments show which assumptions an effect depends on. They
do not identify the mechanisms at work in South African households, estimate the historical
effect of BNPL or forecast default."

**How results are read.** "We therefore interpret mainly differences between runs, conditional on
their shared assumptions."

**What the effect depends on.** "The effect depends most on two features of the model, that
households can borrow with BNPL against a shortfall and that BNPL arrears count toward default."

**The group.** "households short from the start": "surveyed income does not cover food and rent";
"the traditional lender's Regulation 23A test never grants a loan to 55 and lends to 65";
"the platforms, whose screen does not compare income with living costs, lend to them".

**The wage-income screen.** "Under the wage-income screen the platforms lend only to households
with wage income, surveyed income from employment or self-employment." "About half of the effect
depends on the platforms lending to households with no wage income."

**The redrawn population.** "In the redrawn population the effect is `$+1.13 \pm 0.06$` points";
"each replicate has its own population draw"; "The draws resample households independently and
reflect neither the survey's clustering nor uncertainty in the match."

**The refused household.** "in the model a refused household has no other source of credit".

**Screening and welfare.** "The runs record no Rand amount unpaid, so the fall in default does
not show that households are better off." "Whether screening leaves households better off is open."

**Scope.** "Every result holds for the two-year horizon only." "... in the model within two years
and is not a forecast."

**A missing source.** "We found no South African provider that publishes a limit, so λ is an
assumption." "No study measures X, so the sensitivity analysis sweeps it."

## The headline, wherever it appears

| Place | Form |
|---|---|
| Abstract | Rounded, no standard error: "by 1.0 percentage point, from 14.4%" |
| Introduction, Answer to RQ2, Conclusion | "`$1.03 \pm 0.06$` points without peer influence" (pooled over four seed blocks) |
| Section 4.1 | The single block first, `$1.08 \pm 0.11$` at `$\beta=0$`, then the pooled value |

A finding is stated once in the abstract, once in the introduction and once in the body. The
number, its standard error and the words "without peer influence" must agree in every place.
When a result changes, grep for the old number in every `.tex` file and in the `%` provenance
comments beneath the paragraphs.

## Drift still in the text at 81e6ee9

Accepted in `baseline.tsv` so that the checker stays quiet, but worth fixing when the sentence is
next edited. Do not copy these forms into new text.

1. `01_introduction` "28% of BNPL users owe two or more platforms": should be "ever-holders".
2. Abstract "the number of indebted households halves": should be "credit-active".
3. "committed spending" in two generated tables: "committed expenditure" (fixed in `04_results` on 2026-11-24).
4. "more than 90 days behind" (fixed in `03_calibration` and `04_results` on 2026-11-24; check `01_introduction`): "past due".
5. "bureau reporting" and "reporting raises default" for the switch (`01`, `05`, `06`): "bureau visibility".
6. "the earlier rule" in Section 4.1 with no name: fixed on 2026-11-24 ("the earlier streak rule").
7. "lever" for all four arms in one Appendix C caption.
8. "ceiling" beside "cap" for the Regulation 23A payment cap.
9. "route" in the conclusion for the shortfall path.
10. Labour rates as percentages in Section 3.3, decimals elsewhere.
11. "population default" outside the frozen RQ2.
12. "twenty", "fourteen", "eleven" in the appendices against digits in the body.
13. "short of cash" for shortfall; "opening" for starting; "makes better off" for "leaves better off";
    "no other credit" for "no other source of credit"; "runs" and "arms" for the same claim.
