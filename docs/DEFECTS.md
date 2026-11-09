# DEFECTS: current register

**Purpose.** What is still wrong with the thesis or the model, and how each earlier defect was
closed. [`DECISIONS.md`](DECISIONS.md) records what was chosen and why;
[`HISTORY.md`](HISTORY.md) what changed when. This file is the single list of open items. Status as at **2026-10-07**.

**History.** This file replaces a 1,550-line log kept from 2026-08-05 to 2026-09-29, whose entry
headings had stopped tracking status. The full log, with every measurement and the reasoning
behind each fix, is in git history: `git show 3b79e3c:scratchpad/DEFECTS.md`. The model
corrections of 2026-09-29 are in `HISTORY.md`.

**Method.** Every status below was checked against the current thesis source
(`thesis/main.tex`, `thesis/chapters/*.tex`), the generated tables, the code and the data
outputs, not against the old entry's heading. IDs are the original ones; B37 to B39 are new.

**Severity:** `BLOCKER` cannot submit; `MAJOR` an examiner will raise it; `MINOR` polish.
**Owner:** `Marc` (judgement, supervisor or external work); `agent` (executable in the repo).

---

## Open: action needed

### A5 · Front matter is provisional · `BLOCKER` · Marc

Three items in `thesis/main.tex` wait on the UCT departmental template. The declaration carries
a live TODO (line 68: "replace with the wording required by the UCT declaration and plagiarism
form"); the document class, geometry and title page carry a NOTE that they are provisional
(lines 46 to 48); and `\date{\today}` (line 55) will print the build date, not the submission
date. The citation style (`plainurl`, numeric) was never checked against the department either
(was C6). **Closes when** the template is confirmed, the declaration text replaced, the title
page and class adjusted, the date fixed and the citation style confirmed or changed.

### B40 · Unverifiable or typed-in figures · `MINOR` · agent

From the 2026-10-07 review. (1) The fine-grid calibration runs (1.5% gives 13.93%) exist only
as a summary in `calibration.json`; `calibrate.py` does not save stage-4 runs. (2) "Specified
before the run" claims (threshold rule, Pattern 3 statistic, mean-purchase comparison) can be
traced only to 2026-08-13, where git history starts. (3) The data-layer figures 12.6% (median
non-food share of credit payments) and 11.2% (Appendix C) are in no `data/processed` JSON,
presumably computed in `notebooks/p4_validation.ipynb`. (4) Several correct prose numbers are
typed rather than generated: the threshold-minus-control rises, want-off refusals and lending,
effect-block refusals, the single-tick no-BNPL default and R10,400. **Closes when** (3) and (4)
are written to JSON and covered by `check_results_tables.py`; (1) and (2) can only be disclosed.

## Open: disclosed in the thesis, no further action planned

These cannot be closed without data or a redesign that the thesis does not attempt. Each is
stated in the text; the register keeps them so they are not forgotten in the viva.

### B29 · The CPI deflator series is not re-derived from the index table · `MINOR` · agent · disclosed

`statssa_cpi` in `thesis/main.bib` (line 746) still carries `% VERIFY (narrowed)`: the
2018 to 2025 annual averages come from published releases, not from P0141 Table B1. Two checks
constrain them (the 2024 rate against Stats SA's 4.4% statement; the compounded chain against the
June 2026 index, within 0.8%). The deflator converts every BNPL money parameter to 2017 Rands.
**Closes when** the series is rebuilt from Table B1 and the flag removed, or the flag is reworded
as a stated limit. The `% VERIFY` on `sa_bnpl_basket_2026` (line 645) is harmless: the entry is
not cited and does not print.

---
The derivation and its 0.8% check are stated in the index of limitations (Appendix C, "CPI derivation").

### B5 · Accounts against households · `MAJOR` · Marc

The CCMR counts accounts; the model counts households. Arrears are compared over credit-active
households (B18, closed), which removes the definitional undershoot but not the unit mismatch.
This also limits what the fitted shock probability means. Disclosed in Section 3.5 and the note
to `tab:ccmr`. Closes only with household-level arrears data for 2017. **Disclose only** (Marc,
2026-11-09). Under D18 the CCMR account shares also place households in arrears at the start
(B44); disclosed in Sections 3.4 and 3.5 and the limitations index.

### B8 · `q_base` and beta are uncalibrated · `MAJOR` · Marc

**Updated 2026-11-09 (Milestone 2).** beta = 1 is gone. Swept over 0-0.30 at 250 replicates under the
arrears rule (`results/summary/beta_sweep.json`): the BNPL effect is flat, +1.05 +/- 0.03 pp at beta = 0,
slope +0.003 +/- 0.014 pp per 0.1 of beta; verdict linear under the pre-registered test (#97). The peer
arm downstream is beta = 0.30, the largest value swept: volume per eligible household enters the
provider range at beta = 0.2 (R1,411) and is still inside it at 0.3 (R2,014). Stacking among
ever-holders is 70.6% there against the CFPB's 32-33%; Marc's decision (2026-11-09) is to put that
gap down to the CFPB figure being United States data. **Disclose only.** Disclosed in Sections 3.5
("Behaviour with BNPL") and 4.2 (`sec:results-beta`, Table `tab:beta`), and the register's beta
row (#95, #100). The text below describes 6b0a4c7.

Neither has an empirical estimate (Section 3.4). beta = 1 is labelled illustrative: there 98.6%
of ever-holders stack, against the CFPB's 32% and 33%, so Section 4.1 treats beta = 0 as the
guide to magnitudes. The 2026-10-06 audit added the level-sensitivity justification at beta = 1
(Section 4.5). Closes only with South African adoption data.

### B20 · The fitted shock rate is 1.4 times the QLFS band · `MAJOR` · Marc

**Stale since 2026-10-12.** The separation rate is no longer fitted: it is derived at 0.00446 per tick from
the stable-employment condition, 17% below the bottom of the QLFS 2017 band (0.0054-0.0117). The
text below describes the earlier fit.

Fitted 0.016 per tick against an observed separation band of 0.0054 to 0.0117. The text reads it
as a reduced-form hazard of income loss and other distress (Section 3.4). Was 4.1x before the
population rebuild (B32) and the loan-booking fix (B34).

### B21 · The intermediate arrears bands are thin · `MINOR` · Marc

**Closed by D18 (2026-11-09).** Under the arrears rule the 31-60 and 61-90 bands are 4.50% and
2.54% against 3.59% and 2.32% (`calibration.json`). The text below describes 6b0a4c7.

31 to 60 days and 61 to 90 days sit near 1% against 3.6% and 2.3% in the CCMR; the profile is
too concentrated in brief and persistent arrears. Reported as a miss in Section 3.5 and in the
RQ1 answer. A third fitted parameter was rejected.

### B39 · The 90+ band is a rising stock · `MAJOR` · Marc

**Closed by D18 (2026-11-09).** With initial arrears and the derived write-off, 90+ averages
14.08% after burn-in and is 13.84% at the final tick. The text below describes the rule before
the labour-flows rebuild; its figures are stale.

New 2026-10-06. Nothing is written off, so every uncured account accumulates in the 90+ band: at
the fitted values it averages 14.48% after burn-in but reaches 19.9% at the final tick. The fit
matches the time average of a rising stock, not a steady state. Disclosed in Section 3.5
(`03_calibration.tex`, lines 373 to 377) and in the Appendix C caveats table. Closes only with a
write-off rule and a recalibration.

### B37 · The shortfall path: liquidity without a matching purchase, and unspent credit · `MAJOR` · Marc · tested, disclosed

**Updated 2026-11-09 (D18): now the description of the mechanism, not a flaw (Marc, 2026-11-09).**
The thesis states it as "the effect runs through households using BNPL to bridge cash shortfalls,
substituting for purchases they would otherwise pay in cash, and then falling 91+ days behind on
it", with the no-shortfall-BNPL row as evidence of the channel (Sections 4.1, 4.4 "What Moves the
BNPL Effect", 4.6 and 6; limitations index row "The shortfall path carries the effect"). See also
B47. Part (2) is gone: credit raised
against a food or rent shortfall pays it first (`committed_shortfall_funded` is the baseline). Part (1)
now carries the BNPL effect: with BNPL kept out of the shortfall path the effect is -0.05 +/- 0.16 pp at
beta = 0 and +0.11 +/- 0.13 at beta = 0.3, against +0.98 +/- 0.13 and +1.07 +/- 0.15 in the reference
row; with only the shortfall path (want-driven purchases off) it is +0.93 +/- 0.12 (`tab:effect`). Most
of the effect is households defaulting on BNPL taken against a shortfall. The figures below are from
6b0a4c7.

New 2026-10-06; the second half was first recorded under DECISIONS D7 on 2026-09-21. Two
assumptions on the shortfall path. (1) A BNPL agreement taken for a shortfall frees three
quarters of its value in cash, as though the household financed a purchase it would otherwise
have paid for in cash; no purchase is modelled. (2) Credit raised against a committed
(food and rent) shortfall is not spent on food and rent; it goes to debt service, discretionary
spending and savings, and the shortfall is still recorded as distress. Marc kept both rules as
the baseline on 2026-09-29. Tested on 2026-10-06 (`HISTORY.md`, 2026-10-06;
`tab:effect`): with no BNPL on the shortfall path the beta = 1 effect is 0.47 +- 0.11, and with
credit paying the committed shortfall first it is 0.68 +- 0.11, against a reference of
0.60 +- 0.12; at beta = 0 both are +0.06 and not detectable. Disclosed in Sections 2.3 and 2.4
and Appendix C. No further action unless the baseline rule is changed, which would need a
recalibration.

### B41 · Experiments an examiner may ask for · `MAJOR` · Marc · accepted, not run

From the 2026-10-07 review; Marc decided on 2026-10-07 not to run them. (a) The bureau switch
under the "+25%" and "credit pays committed shortfall first" rules, or over 104 ticks;
(b) following refused against granted households; (c) a four-platform arm with a shared
aggregate limit, which would separate platforms not seeing one another from extra capacity;
(d) refitting the shock rate on another window and the effects at the QLFS upper bound.
(a) and (c) are the likeliest viva questions. The thesis states each gap (Sections 4.2, 5 and 6).

### B45 · The Sobol default indices are noise-dominated under the arrears rule · `MAJOR` · agent

New 2026-11-09. With 2 replicates per design point, the first-order indices for default are near zero
for every parameter but the separation rate (0.67) and the total-order indices are about 0.4 for all
six (1.12 for the separation rate). The replicate SD of default is larger under the arrears rule, so
run-to-run noise swamps the parameter effects. Rerun `simulation.sensitivity` with more replicates per
point before Table 22 is quoted, or report only the ranking. **Disclosed 2026-11-09 (#95):** Section
4.5 and Appendix C (`app:sensitivity`) read only the separation-rate ranking and call the default
indices provisional; the separation rate's direction is given (default 21.3% in the lowest fifth of
its swept range, 22.3% in the highest; `sobol_runs.parquet`). Rerun is #104.

### B44 · The arrears rule adds two assumptions and one fitted parameter · `MAJOR` · Marc

New 2026-11-09 (D18). (1) Initial arrears are placed on the least able households by a
deterministic ranking, and 120+ ages are drawn over 9-26 ticks; no source gives which
households were in arrears in 2017. (2) A defaulted account is non-performing: the model has no
collections, debt review or partial recovery. (3) Arrears persistence (0.72) is fitted, so the
model now has two fitted parameters and five targeted bands; agreement on those bands is not
evidence. The write-off rate is derived from the CCMR, not fitted, but it assumes the 2017
profile is a steady state. CCMR shares are of accounts, applied to households (B5). **Disclose
only** (Marc, 2026-11-09). Disclosed 2026-11-09 (#95) in Section 3.4 (`sec:lim-calibration`: the
three steps and "This agreement is by construction"), Section 3.5 ("What the Validation
Supports" and the RQ1 answer), Appendix B.2, Appendix C (`app:calibration` and the limitations
row "The baseline is calibrated, not validated") and Algorithm `alg:seed` (Appendix F).

### B46 · The credit-active population halves over the run · `MAJOR` · Marc

New 2026-11-09 (D18). With BNPL off, credit-active households fall from 2,285 at tick 0 to 1,175
at the final tick (`docs/ARREARS_RULE_2026-11.md`). Written-off accounts leave, households that
repay leave, and the only new traditional borrowing is against shortfalls; the CCMR stock is
replenished by new accounts, the model's is not. The 90+ share is stationary, but it is the
share of a shrinking book, so "the profile holds for two years" is a statement about ratios, not
about a steady-state population. Fixing it needs an origination flow and a recalibration; not
planned. **Disclose only** (Marc, 2026-11-09). Disclosed 2026-11-09 (#95) in Section 3.4 (last
paragraph of `sec:lim-calibration`), Section 3.5 ("What the Validation Supports", RQ1 answer),
Section 6 (RQ1 and the extensions), and the limitations row "The credit-active book halves".

### B47 · Most of the BNPL effect comes from households whose income is below their food and rent · `MAJOR` · Marc · disclosed

New 2026-11-09 (#95). The 3.6% of agents (182) whose surveyed income is below committed
expenditure default during the run at 31% without BNPL and 56% with it at beta = 0
(`defaulter_credit.json`), about 0.9 of the 1.08-point effect on the rq0 seeds. Among the other
households the pooled effect is +0.11 +/- 0.07 pp at beta = 0 (not detectable) and +0.18 +/- 0.08 at
beta = 0.3 (`contestable_default.json`). Two-thirds of the group are in Q1, which is why the effect
is +4.12 pp in Q1 and nowhere else, and why mandatory screening (-4.68 pp in Q1) removes it. The
thesis no longer calls the group a survey artefact (#59: no source). Disclosed in Sections 3.5,
4.1, 4.5, 5 and 6 and the limitations row "Households short from the start". No fix planned.

### B7 · Behavioural parameters are imported from the United States · `MINOR` · Marc

**Updated 2026-11-09.** Under the arrears rule the minimum-payer share at 0.20 and 0.40 gives a BNPL
effect of +1.14 +/- 0.12 and +1.08 +/- 0.14 pp at beta = 0 (`tab:effect`). Payment friction is now
fitted jointly with arrears persistence (D18). The figures below are from 6b0a4c7.

The 0.29 minimum-payer share and the evidence behind payment friction and want-driven borrowing
are US. Stated in Section 3.3 (`sec:lim-transfer`); the share is swept 0.20 to 0.40 and moves the
beta = 1 effect between 0.54 and 0.65. No local source located.

---

## Closed

| ID | Summary | How closed |
| --- | --- | --- |
| A1 | Introduction, results and conclusion chapters empty | Written; six-section structure (Sections 1 to 6) |
| A2 | The model did not exist | Built, calibrated and run; commit `1d1067f` reports 134 passing tests (not rerun for this register) |
| A3 | No data-layer chapter | Section 3.2 and Appendices D and E |
| A4 | No limitations chapter | Limits placed where they apply (Sections 3.3 to 3.5, 6) and Appendix C |
| B1 | RQ promised "systemic default cascades" | RQs rewritten (supervisor, 2026-09-09; RQ2 reworded 2026-09-29); Section 4.3 states contagion is outside the test |
| B2 | Pattern 1 partly built in | Section 3.5 says Pattern 1 is not independent of model development |
| B3 | Three of four validation targets foreign or off-vintage | Patterns 1, 3 and 4 demoted to plausibility comparisons (Section 3.5) |
| B4 | Pattern 4 not operationalised | Order-of-magnitude comparison, construct difference stated (`tab:patterns`) |
| B6 | Arrears bands nested and appeared to sum | Full band table with aggregate rows marked (`tab:ccmr`) |
| B9 | Novelty claim had no search record | Searched 2026-10-07 (record below); sentence narrowed to "no South African study of how BNPL affects household distress and no agent-based model of South African household credit" (Section 1.1) |
| B42 | Default level had no external comparison | NCR Credit Bureau Monitor, March 2017, added to Section 3.5 (`ncr_cbm_2017`): 21.7% of credit-active consumers 3+ months in arrears, 39.3% impaired. Individuals at one date, so the level is still described as not validated |
| B43 | RQ1 wording ("external comparisons") and the abstract at about 265 words | Accepted by Marc, 2026-10-07 |
| B10 | Market-size figures unusable | No figure cited; TODO removed |
| B11 | Pattern 4 rests on the weakest variable | Pattern 4 is a plausibility check only; savings proxy named in Section 3.2 |
| B12 | Zero-capacity debtors not reported | Appendix D.9 now reports them: 53 indebted households, 27 agents after resampling (2026-10-06) |
| B13 | Check D shown under two labels in `p4_validation.ipynb` | Only "D. Servicing plausible pre-guard" remains |
| B14 | Two Gini figures | Both stated and named (Section 3.2, `tab:validation`) |
| B15 | Minimum-payment formula undefined | Assumption flagged in Submodel 6; swept 0.025 to 0.10 |
| B16 | BNPL limits not published | Rolling limit an assumption, swept; order cap an assumption (B36) |
| B17 | Single-tick shock could not carry the calibration | Persistent unemployment spell; single-tick arm kept (Section 4.5) |
| B18 | CCMR denominator excluded half the population | Arrears compared over credit-active households |
| B19, B19b | Pattern 3 statistic | Aggregate DTI pre-registered; corrected model peaks in Q1, reported as a failure (Section 3.5) |
| B22 | RQ2 non-linearity unsupported | Reported: no tipping point under either rule (Section 4.3) |
| B23 | Bureau visibility did nothing | Superseded by the 100-replicate rerun (2026-10-05): it raises default 0.15 to 0.22 points through refusals (Section 5) |
| B24 | Worst-sourced parameters drove the ranking | Ratios replaced flat constants (B30); Sobol rerun at N=256 (`tab:sobol`) |
| B25 | High-beta volumes implausible | beta = 1 labelled illustrative (Section 4.1); volume check reported as a failure at beta = 0 (Section 3.5) |
| B26 | Three unfitted checks passed | Kept where still true (order cap binds on 0.3%); stacking shares now attributed to routing (Section 4.2) |
| B27 | Statutory cooling-off arm was a no-op | Strict gate and regression test, 2026-08-12; lever now in Appendix C |
| B28 | Checkout debit funded by money that did not exist | Order truncated to available cash |
| B29 | BNPL money parameters nominal | Deflated once to 2017 Rands; residual flag open above |
| B30 | Flat constants on a Gini-0.67 population | kappa and lambda as ratios of household budget and income |
| B31 | `s_g` denominator | Eligible members; separate `init_rng` stream |
| B32 | Mean-purchase check moved after the rent fix | Pre-registered in DECISIONS D4; corrected run gives R633, 36.2% low, reported as a named miss (Section 3.5) |
| B33 | DSTI check compared unlike quantities | Like-for-like measure fails (12.8% against 6.1 to 9.8%), reported as a failure (Section 3.5) |
| B34 | Granted loans not booked as debt | Booked onto the consolidated balance; refit to 0.016 (2026-09-21) |
| B35 | Two activation arms were one | Duplicate removed; one fixed-order check claimed |
| B36 | R15,000 order cap attributed to Payflex | Recorded as an assumption in code, register and Section 3.3; `payflex_limits` repointed |
| B38 | `p3_resample_summary.json` gives 1.38 pp, `data_figure_numbers.json` 1.27 pp | Checked 2026-10-06: not stale. 1.38 is the largest gap from 20%; 1.27 is the largest gap from the weighted source, the statistic in `tab:validation` (1.3pp). Key names differ (`_dev_` and `_gap_`) |
| 2026-09-29 | Six implementation defects (interest charged twice, arrears double-counted, cleared debt kept its instalment, opening-tick BNPL collection, checkout quarter requested from no one, late-fee cap) | Fixed and rerun; `HISTORY.md` (2026-09-29) |
| C1 | `\ac{FCA}` undefined | In the acronym list |
| C2 | UK statute read as South African | Section 66A no longer cited in the thesis |
| C3 | `% VERIFY` on Hamill and Woolard | Published Hamill article and Woolard report details in `main.bib` |
| C4 | Bib key `toh2025bnplconstraints` | Renamed `hayashi2025constraints` |
| C5 | Informal-finance claim on a thin source | Cites FinScope (Section 2.2) |
| C6 | Citation style | Folded into A5 |
| C7 | `ncr_ccmr_2025` uncited | Deliberate; not printed |
| D1 | Starred sections | Numbered `\section` under `article` |
| D2 | Hand-numbered submodels | Fixed numbering in `tab:submodels`; accepted |
| D3 | Acronyms in the introduction | Front matter |
| D4 | `commath` with `amsmath` | Removed |
| D5 | Live TODOs | Only the front-matter TODO remains (A5) |
| D6 | No figures or tables | Generated tables and figures throughout |
| E1 to E5 | Writing register | 2026-08-05 pass and the writing audits of 2026-10-06 (`abda7e9`, `dfeabbf`) |
| F1 to F5 | Length and balance | Restructure; body 9,727 words against the 10,000 cap |
| G1 | `OVERVIEW.md` date stale | Replaced by `README.md`, which carries no dated status (2026-10-07) |
| G2 | Caveats in JSON, not prose | CCMR unit caveat in Section 3.5 and `tab:ccmr` |
| G3 | Empty `notebooks/context/` | Removed |

---

## Record: novelty search for B9 (2026-10-07)

Run by a search agent; not a systematic review. **Sources:** OpenAlex API (indexes SSRN, RePEc
and South African institutional repositories) with title/abstract phrase filters; web search,
including site-restricted queries on OpenUCT, SUNScholar, UPSpace, WIReDSpace, resbank.co.za
and econrsa.org. Google Scholar, the SSRN and IDEAS search pages and the repositories' own
search pages could not be queried directly.

**Queries (OpenAlex):** "buy now pay later" AND "South Africa"; BNPL AND "South Africa";
(BNPL OR "buy now pay later") AND (Africa OR Nigeria OR Kenya OR Ghana); "agent-based" AND
"South Africa" AND (debt OR credit OR indebtedness). **Web:** BNPL South Africa with financial
distress, indebtedness, default, thesis, dissertation, working paper, SSRN, RePEc, financial
well-being, Gen Z; SARB and ERSA working papers on household debt and arrears; agent-based
models of South African household credit.

**Result:** no South African study of BNPL's effect on household distress, arrears or default,
and no agent-based or simulation model of South African household credit. Adjacent work:
Sebola (2025), Wits Master of Management report on SMME adoption of BNPL; Ssebagala (2015, UCT
PhD; CSSR WP 368, 2016) and Daniels (2001, DPRU) on household over-indebtedness, without BNPL;
Mwase and Alhassan (2017, UCT GSB) on public-servant over-indebtedness; Cornelli, Gambacorta and
Pancotto (2023, BIS) cross-country BNPL, South Africa not covered; adoption studies in Tanzania,
Nigeria and Egypt; legal commentary (Webber Wentzel, 2025).

**Check before submission:** a GIBS MBA report by M. Pietersen, "Buy Now Pay Later, Financial
Well-Being & Overall Well-Being", seen only as a LinkedIn snippet and not found on UPSpace. If
it exists and measures distress, the sentence in Section 1.1 needs to cite it.

## Done, 2026-10-13: examiner-style review (Fable), option A approved for all

Approved by Marc on 2026-10-12 and done on 2026-10-13, uncommitted. Three new scripts write the numbers: `check_bureau_visible_split.py` (`bureau_visible_split.json`), `check_contestable_default.py` (`contestable_default.json`), and an `income_path` addition to `check_defaulter_credit.py` (`defaulter_credit.json`; existing keys reproduce exactly).

| ID | Hole | Resolution |
| --- | --- | --- |
| H1 | Under bureau visibility the lender sees mostly BNPL arrears and late fees, not live instalments. | **Premise refuted; the approved rewording was not applied.** At the applications the lender assesses (20 seeds, post-burn-in), arrears and fees are 0.3% (β = 0) and 0.5% (β = 1) of the visible BNPL obligation, at most 2.1% in any quintile. 99.9% of BNPL arrears are held by households that have already defaulted, which the bureau refuses before the test and which no longer apply. The probe's 91/75/64/31% reproduces exactly as the stock over all holders *including* defaulted households (β = 0). Only 2.3% and 3.7% of bureau-induced refusals would pass if arrears were hidden. Section 5 now states this in one sentence. It adds that 27 to 30% of the visible obligation is on agreements opened in the same tick against the same shortfall, which a lagged bureau would not show. Section 2.2 now says that late fees are counted too, until paid. |
| H2 | Labour flows hold employment constant, not income. | Done: 3.4 gives employment and income by quintile at the final tick: income +15.2% in Q1, +3.2% in Q2, −3.6% in Q3, −6.1% in Q4, −5.7% in Q5, and −3.9% in total. Employment is +30% in Q1 and −12% in Q5, because jobseekers are concentrated in the lower quintiles. The same is in the Appendix C row. "Stable" became "constant" in the abstract and the conclusion. |
| H3 | About 3.5 of 7.3 default points come from households who default regardless. | Done: 3.5 adds that the contestable baseline is 3.91%. Against it, the BNPL effect is 0.18 ± 0.05 points (4.6%) and the bureau effect is 0.19 ± 0.04 (5.1%) and 0.17 ± 0.03 (4.2%). 4.7 and the conclusion now say "about 5%" where they said "about 2%". 4.4 adds that contestable default is lowest in Q1 (2.77%) and highest in Q4 (5.93%). All 700 reruns reproduce `results/raw`. |
| H4 | The single-tick arm changes three things at once. | Done, with a corrected premise. The arm removes 69% of contestable default (3.88% → 1.19%), not "nearly all". 4.6 and the conclusion now say that the effect works through households in a spell of lost income, and that the arm does not isolate persistence. |
| H5 | The β = 0.5 access contrast is an on/off comparison. | Done (4.3): +0.17 ± 0.05 at volume R5,040 per eligible household a year, 6.0 times the control and above the R4,261 top of the provider band. |
| H6 | The derived separation rate is below the QLFS band. | Done (4.5, conclusion): the effect is at the low end along this dimension. |
| H8 | Three detectable results are left unexplained. | Done: the income drift is offered as an untested candidate for Q4 (4.4, 5). Platform capacity is offered for six platforms at β = 1 (4.2). |

Body 9,943 words (cap 10,000). Abstract 299 typeset words. Still open: `config.py` still says "as in the stable 2017 labour market" in the `labour_flows` source note, which feeds the generated register in Appendix B. It was not changed, to keep model code untouched.
