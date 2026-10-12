# REFERENCE AUDIT: 2026-10-12

**Purpose.** A check of every citation in the thesis against its source, so that no reference is
invented and no source is credited with something it does not say. This file lists what needs
fixing. [`DEFECTS.md`](DEFECTS.md) remains the register for model and thesis defects.

**Scope.** Commit `bc92e07` (main). `thesis/main.bib` holds 56 entries, of which 50 are cited, 186
times in all. The six that are not cited (`cfpb2025market`, `ncr_ccmr_2025`, `payjustnow_limits`,
`sa_bnpl_basket_2026`, `weaver2025results`, `worldbank_gini_zaf`) do not print and were not checked.

**Method.** Each entry was checked on two counts:
- its metadata, against Crossref, DataCite or the issuer's own page;
- each citing passage, against the source text (PDF or web page, with the Wayback Machine where a
  page had changed).

Paywalled papers were checked against the working-paper or arXiv version and the published
abstract. Items marked **re-checked** were confirmed a second time, independently of the first
pass. Items marked **microdata** were reproduced from files in `data/raw`.

**Bottom line.** No reference is invented. Every cited work exists, and authors, titles, venues,
volumes, pages and DOIs match the publisher record. The defects are claims the source does not
contain (R1 to R9), citations stretched past what the source shows (R10 to R24), small metadata
gaps (R25 to R30) and wrong private notes in `main.bib` (R31 to R34).

**Severity:** `MAJOR` an examiner checking the source would catch it; `MINOR` wording or polish.
**Owner:** `Marc` (judgement or a source to find); `agent` (executable in the repo).

---

## Claims the cited source does not contain

### R1 · Regulation 23A "published worked examples" do not exist · `MAJOR` · agent · re-checked

The thesis says the regulation publishes two worked examples, R2,000 → R881.00 and
R10,000 → R1,505.38. GN R202 (GG 38557, 13 March 2015) contains none:
- the full gazette text (about 41,000 words) has no "example", "881" or "1 505";
- Table 1 on p. 19 and the Annexure A questionnaire have no examples;
- a web search found no other NCR document that publishes these figures.

The arithmetic is correct (800 + 0.0675 × 1,200 = 881.00; 1,167.88 + 0.09 × 3,750 = 1,505.38),
so these are your own checks, not published ones.

Locations:
- [`appendix_d_variables.tex:212`](../thesis/chapters/appendix_d_variables.tex#L212) ("the regulation's two published worked examples")
- [`appendix_c_supplementary.tex:34`](../thesis/chapters/appendix_c_supplementary.tex#L34) ("both worked examples published with the regulation")
- [`02_model.tex:349`](../thesis/chapters/02_model.tex#L349) ("the Regulation 23A worked examples")
- [`simulation/affordability.py:35`](../simulation/affordability.py#L35) (comment)
- `simulation/tests/test_affordability.py:22` (docstring)
- `data/config/README.md:395`

**Closes when** every location says "two hand-computed checks from Table 1" (or similar), unless
a published source for the figures turns up.

### R2 · deHaan et al.: "larger increases among liquidity-constrained consumers" · `MAJOR` · Marc · re-checked

[`01_introduction.tex:37-39`](../thesis/chapters/01_introduction.tex#L37). This clause was not
found in either version checked:
- **Published abstract** (Crossref, *Management Science* 70(8)): it reports overdraft charges and
  card interest and fees rising after adoption, "consistent with BNPL facilitating overborrowing",
  with no split by liquidity constraint.
- **Working paper** (October 2022): its only cross-sectional test (§4.4) splits users by usage
  intensity (number of BNPL providers). Effects are "significantly larger for high-intensity
  users".

The rest of the sentence is supported (10.6 million consumers; overdraft charges, card interest
and late fees; IV estimates +8.9%, +2.5%, +8.4%). The same claim appears in the `dehaan2024bnpl`
annote.

**Closes when** a table in the published version is found and cited, or the clause is removed or
changed to "larger among heavier users".

### R3 · The CPI factor is said to reproduce the published index · `MINOR` · agent · re-checked

[`appendix_d_variables.tex:264`](../thesis/chapters/appendix_d_variables.tex#L264) says "the
factor reproduces the published index to within 0.8%". Two problems:

1. **The check does not test the factor.** `implied_june_2026_index()` in
   `notebooks/scripts/extract_cpi_deflator.py:126` computes 100 × √1.0322 × 1.05 = 106.68 against
   107.5. It uses only the 2025 rate and the June 2026 year-on-year rate. The 2018 to 2024 links,
   which make up most of the 1.511 factor, are never tested. The `statssa_cpi` annote and the
   `verify` field of `data/config/cpi_deflator_2017.json` overstate the check in the same way
   ("the whole compounded chain").
2. **Two rates are not Stats SA's published annual averages.** `cpi_deflator_2017.json` has
   2022 = 7.04 and 2023 = 6.08. Stats SA publishes 6.9 (P0141 December 2022, Table B2) and 6.0
   (P0141 June 2026, Table B2). 2018 to 2021, 2024 and 2025 match.

With the published rates the factors become about 1.4364 (2025) and 1.506 (mid-2026), against
1.4391 and 1.5111. That moves R15,000 to about R9,957 instead of R9,927: immaterial to results,
but the description is wrong.

**Closes when** 2022 and 2023 are set to 6.9 and 6.0 and the factor regenerated (or the
discrepancy explained), and the thesis says what the check actually tests.

### R4 · BNPL bureau invisibility is labelled "sourced" to a survey that does not establish it · `MAJOR` · Marc

The benchmark assumes the traditional lender does not see BNPL, citing `transunion_cps_sa_2025`.
The survey's Fig. 16 only lists "buy now, pay later loans" as an example of "information not on
standard credit report", in a question about how credit scores would change. That is how the
survey framed a question, not a statement about bureau data. Meanwhile:
- Payflex terms cl. 11.4: "You agree and consent that we may transmit to registered credit
  bureau(s) information concerning – 11.4.1 this Agreement … 11.4.2 any non-compliance". The same
  clause is in the Wayback copy of 19 May 2022.
- PayJustNow terms: consent to "submitting information to credit bureaus related to any
  agreement".

Consent does not prove that reporting happened. But the already-cited `dcasa_bnpl_2026` ("not
yet being displayed on consumer credit profiles") and `finasa_bnpl_2026` (the NCR disallowed live
processing) support "lenders could not see BNPL" better.

Locations:
- [`appendix_b_register.tex:79`](../thesis/chapters/appendix_b_register.tex#L79) ("BNPL was not reported to the bureau before the 2026 arrangements", class *sourced*)
- [`02_model.tex:136`](../thesis/chapters/02_model.tex#L136) and [`02_model.tex:246`](../thesis/chapters/02_model.tex#L246) (Submodel 10)
- `appendix_b_specification.tex:34`
- [`01_introduction.tex:21`](../thesis/chapters/01_introduction.tex#L21) (fine as literally worded, but the next sentence leans on it)

**Closes when** the claim is reworded to "BNPL obligations were not displayed on bureau profiles"
and cited to DCASA and FINASA, or relabelled *assumed*.

### R5 · Submodel 14: a rule the Payflex terms do not contain · `MINOR` · agent

[`02_model.tex:254`](../thesis/chapters/02_model.tex#L254) cites `payflex_terms` for the whole row.

Supported by the terms:
- pay-in-four (cl. 1.1.7);
- interest-free (cl. 7.1);
- R95 a week, at most three charges (cl. 1.1.5);
- cap at the lower of R285 or 50% of the price (cl. 8.5).

Not in the terms:
- "Once the cap is reached, that platform refuses the household new agreements". The terms
  provide for accelerating other plans (cl. 8.3.3) and court judgment (cl. 9.2) instead.
- "A want-driven order is reduced to what the household can pay at checkout."

The row's source column says "None". **Closes when** the row marks these two rules as assumed.

### R6 · Hamill et al. said to "find" that promotions increase indebtedness · `MAJOR` · agent

[`01_introduction.tex:117`](../thesis/chapters/01_introduction.tex#L117) and
[`appendix_c_supplementary.tex:246`](../thesis/chapters/appendix_c_supplementary.tex#L246).
Checked against arXiv:2311.01901v2, whose abstract matches the published one.
- **What the paper says.** Promotions "may enhance access to credit … but could potentially
  escalate customer indebtedness" (§6). Its headline results are about lender profit and market
  share.
- **What appendix C needs.** It uses the paper to suggest that competing lenders "could add a
  driver of distress", but the paper reports: "the fractions of accounts with missed payments
  remain approximately constant, indicating no significant increase in the risk of default".
- **What is supported.** "Longer interest-free promotions raise card balances": balances
  "increase with the length of the interest-free duration".

**Closes when** "find" becomes "suggest … could", and appendix C notes that default risk did not
rise in their model.

### R7 · Equivalised income and multi-member households (UK) · `MINOR` · agent · re-checked

[`appendix_b_specification.tex:77`](../thesis/chapters/appendix_b_specification.tex#L77): "Equivalised
income is below the income of a household with more than one member, so both shares overstate
the limits". The ONS rescales the modified OECD scale so that a childless couple = 1 (first
adult 0.67, each further person aged 14+ 0.33, child 0.2;
[ONS 2020](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/articles/howaccountingfordifferencesinneedforpublicservicesimpactsukincomeinequalitystatistics/2020-10-12)).
On that scale:
- a couple's equivalised income equals its actual income;
- a single adult's is above it;
- only households of three or more are above their equivalised income.

The statement holds for the ABS measure, where a lone person = 1. **Closes when** the sentence is
restricted to the Australian figure, or rewritten for both scales.

### R8 · FinScope "debt service 6.1–9.8%" is your own calculation · `MINOR` · agent · microdata

[`03_calibration.tex:336`](../thesis/chapters/03_calibration.tex#L336) and
[`appendix_d_variables.tex:231`](../thesis/chapters/appendix_d_variables.tex#L231) ("FinScope
self-reported range"). FinScope publishes no such figure. It reproduces as an **unweighted** share
of the C8 "21 matchsticks" budget game among 1,291 credit holders:
- 6.07% for category 9 ("Other debt repayments, e.g. clothing store accounts, hire purchase");
- 9.78% for categories 5 + 9 (adding "Bond or home loan, credit card, car financing").

Weighted it is 6.32–9.46% (HH_WEIGHT16) or 6.27–9.30% (BENCHWGT_PP). The measure is an allocation
of matchsticks by individual adults, not measured debt service. Its scope also differs from the
model's: the upper bound includes mortgages and vehicle finance, which the model excludes, and
the lower bound omits personal and short-term loans, which the model includes. The "above the
range" conclusion survives.

**Closes when** the text says it is derived from the budget-allocation question and states
whether it is weighted.

### R9 · "Informal borrowing is absent from the data" · `MAJOR` · Marc · microdata (not re-checked)

[`03_calibration.tex:389`](../thesis/chapters/03_calibration.tex#L389) and
[`02_model.tex:137`](../thesis/chapters/02_model.tex#L137) ("the model omits informal borrowing").
D_trad is NIDS `w5_f_deb`, which includes mashonisa (g22) and loans from friends (g21):
- 437 households hold only such loans and still have non-zero `w5_f_deb` (e.g. hhid 500060: R400
  informal, `f_deb` R400);
- about 2.8% of households (weighted) hold mashonisa debt and 4.3% hold loans from friends;
- together these are 0.85% of weighted D_trad.

So the informal debt is in the data and is treated as bureau-visible traditional debt. This also
weakens any argument that informal borrowing explains the debt-stock gap. **Closes when** the
figures are re-checked and the text corrected; the FinScope half of the sentence is fine.

---

## Citations stretched past what the source shows

### R10 · Grimm 2006 cited for pattern-oriented modelling · `MINOR` · agent

[`01_introduction.tex:123`](../thesis/chapters/01_introduction.tex#L123). The 2006 paper never
discusses pattern-oriented modelling, and Grimm et al. (2020) say the earlier ODD "is not clearly
linked to pattern-oriented modelling". Drop `grimm2006odd` from this citation; keep it at
`02_model.tex:24`.

### R11 · Windrum cited as "pattern-oriented modelling" · `MINOR` · agent

[`03_calibration.tex:275`](../thesis/chapters/03_calibration.tex#L275). Windrum et al. write about
stylised facts and indirect calibration, never pattern-oriented modelling. Suggested wording:
"Following pattern-oriented modelling \cite{grimm2020odd} and the validation literature
\cite{windrum2007validation}".

### R12 · Madeira is the only citation for the seven-tick default rule · `MINOR` · agent

[`02_model.tex:240`](../thesis/chapters/02_model.tex#L240) (Submodel 7). Madeira supports the
cash-flow definition of distress. The k = 7 (98-day) persistence rule is yours (the 90-day
convention, `02_model.tex:199-200`). Mark the rule as your own. Separately, "a middle-income
economy" ([`01_introduction.tex:115`](../thesis/chapters/01_introduction.tex#L115),
`appendix_a_rationale.tex:40`) is out of date: Chile has been high-income in the World Bank
classification since July 2013, though it was upper-middle for most of Madeira's 1990–2012 window.
Use "an emerging economy" or "Chile".

### R13 · CFPB stacking benchmark described as "loans at two or more firms in a year" · `MINOR` · agent

`thesis/chapters/generated/tab_stacking.tex:7` (generated: fix in
`notebooks/scripts/build_results_tables.py`). The CFPB measures *simultaneous* loans: "having
originated a subsequent BNPL loan within 42 days of the first" (Table 4 note, p. 18; 31.7% in
2021, 32.6% in 2022). Footnote 24 (p. 17) calls the figure "likely an undercount" because one
firm (about 19% of transactions) could not be matched. It is also a per-year share, while the
model's ever-holder share covers a two-year run. The caption at `04_results.tex:88` is fine.

### R14 · deHaan et al. cited for "arrears" · `MINOR` · agent

[`03_calibration.tex:278`](../thesis/chapters/03_calibration.tex#L278) and
`generated/tab_bnpl_on_checks.tex:14-15` (Pattern 1). The paper measures credit-card late-fee
counts and interest charges, not arrears. Say "late fees", or note that late fees are a proxy for
arrears.

### R15 · ASIC: "while BNPL sat outside Australia's credit law" · `MINOR` · agent

[`01_introduction.tex:178`](../thesis/chapters/01_introduction.tex#L178). REP 672, p. 3: BNPL
providers "are generally considered not to be regulated under the National Consumer Credit
Protection Act 2009 … However, buy now pay later arrangements are regulated as credit under the
… ASIC Act 2001". Say "outside the National Credit Act".

### R16 · Submodel 9 loan pricing cited to the affordability regulations · `MINOR` · agent

[`02_model.tex:244`](../thesis/chapters/02_model.tex#L244). "Repurchase rate plus 21 points, 25
months" is cited only to `sa_ncr_affordability_2015`. The rate comes from
`sa_ncr_ratecaps_2016` (Table A item 3) and the term from `ncr_ccmr_2017`. Add both.

### R17 · CCMR cited for "repayable within 31 days" · `MINOR` · agent

[`03_calibration.tex:214`](../thesis/chapters/03_calibration.tex#L214). The CCMR defines
short-term credit as "amounts not exceeding R8 000 and repayable within 6 months" (Definitions,
p. 23). It shows only that 65.83% of agreements by number were "≤1 Month" (Tables 6.1 and 6.2,
p. 17). The 31 days comes from FinScope G13 alone. Cite the CCMR only for "most agreements within
a month".

### R18 · Fourteen-day withdrawal period attributed to FCA PS26/1 · `MINOR` · agent

`appendix_b_register.tex:101` and `appendix_c_supplementary.tex:175`. PS26/1 confirms only that
s.66A applies to regulated deferred payment credit (CONC 11.1.2A G). The 14 days is in CCA s.66A
itself, not the cited document. Either cite the Act or drop "fourteen-day".

### R19 · Comer and Alizadeh marked *sourced* for random activation order · `MINOR` · agent

`appendix_b_register.tex:107`. Both papers show that the activation scheme changes results.
Neither recommends random order. They justify the robustness arm, not the benchmark choice.
Relabel the benchmark as *assumed*, with the papers cited for the robustness arm.

### R20 · Gini comparison is not like-for-like · `MINOR` · agent · microdata

[`03_calibration.tex:334`](../thesis/chapters/03_calibration.tex#L334). The model's 0.651 is
household-weighted. Weighted by persons (w5_wgt × household size), as Stats SA and Hundenborn et
al. compute their per-capita Ginis, it is 0.663. That is essentially equal to 0.66 (2014) and
close to 0.67 (2015), so "slightly lower" is partly a weighting artefact.

### R21 · Ackert et al. used beyond an experiment on purchase financing · `MINOR` · Marc

The study elicits young people's choices and beliefs about BNPL versus a credit card for a
purchase (abstract-level check; full text paywalled). It is cited for:
- BNPL first for a cash shortfall (`02_model.tex:236`);
- a peer rule driven by the observed adoption share (`02_model.tex:248` and `:305`,
  `appendix_b_specification.tex:36`);
- "social approval rather than price" (`appendix_a_rationale.tex:29`).

The existing hedges ("support the channel but do not identify its strength") mostly cover this.
Check two things: whether the experiment's two options differed in cost (if BNPL was cheaper,
price is not ruled out), and whether to mention that the sample is young people.

### R22 · Kuchler and Pagel cited for a missed-instalment friction · `MINOR` · agent

`02_model.tex:238` and `appendix_b_register.tex:73`. The paper studies voluntary, self-set
paydown plans above the minimum, not missed contractual instalments. "Motivated by" is
defensible; do not say more than that.

### R23 · Meier and Sprenger, and Keys and Wang, cited for heuristic rules · `MINOR` · agent

`appendix_b_specification.tex:22` and `:28` (ODD rows: "heuristic rules replace intertemporal
optimisation", "fixed priority order"). Quasi-hyperbolic preferences are still forward-looking.
These papers motivate departing from standard optimisation, not the specific heuristic.

### R24 · Minor wording · `MINOR` · agent

- **SARB FSR** (`01_introduction.tex:24`). "Less rigorous credit checks" is presented as a risk.
  The box presents it as part of the product's appeal, within an overall framing of "rising
  financial vulnerability".
- **DCASA** (`01_introduction.tex:31`). "Began submitting records in 2026" goes slightly beyond
  the notice, which only records submissions during May 2026.
- **Cardaci** (`appendix_b_specification.tex:40`). Same-quintile reference groups are a loose
  analogy for upward-looking expenditure cascades (abstract-level check only).
- **Weaver IAR** (`generated/tab_bnpl_on_checks.tex:22`). The "±35%" beside the citation is the
  project's tolerance (`build_results_tables.py:307`), not the source's. Make that clear.

---

## Bibliography metadata

### R25 · Affordability regulations URL shows a wrong figure · `MINOR` · agent

The `sa_ncr_affordability_2015` URL (acts.co.za) shows **R900.00** as the second band's fixed
factor. The gazette (GG 38557, p. 19, Table 1) says **R800.00**, which the thesis table and
`simulation/affordability.py` use. Cite the gazette instead, e.g.
`https://www.ncr.org.za/documents/pages/NCA-amendment-Regulations-March-20151.pdf`, and add a
`lastchecked` date (this is the only URL entry without one).

### R26 · IES version · `MINOR` · agent

`statssa_ies_2023` says `zaf-statssa-ies-2022-2023-v1`, but the file analysed is v1.1
(`ies-2022-2023-total-v1.1.dta`). The DOI now lands on v1.2 (DataFirst 2026). State "Version 1.1".

### R27 · Hundenborn et al. DOI · `MINOR` · agent

Add `doi = {10.35188/UNU-WIDER/2018/604-3}` to `hundenborn2018drivers`.

### R28 · FinScope entry gives no access route · `MINOR` · Marc

`finscope2019` is a `@techreport` with no URL. The thesis uses licensed microdata
(`data/raw/FINMARK_2019/*.dta`), released by FinMark Trust to syndicate members, not through
DataFirst. Cite it as a dataset obtained from FinMark Trust. The public companion is the
*FinScope South Africa 2019 Pocket Guide* (FinMark Trust, 2020). Related: the Pocket Guide
(p. 19) splits adults into 68% banked, 13% SASSA card only and 19% unbanked, so the ~81% "banked"
flag probably counts SASSA-card-only adults as banked (likely, not confirmed).

### R29 · Year printed twice in `@misc` entries · `MINOR` · agent

`plainurl` appends `year` after `howpublished`, so dates appear twice. Examples: "FINASA
statement, 30 April 2026, 2026."; "13 March 2015, 2015."; "archived 10 November 2024, 2024.";
"corrected 22 March 2022, 2021."; "in force from 6 May 2016, 2015."; "Released 28 April 2022 …,
April 2022." Remove the date from `howpublished` or drop `year`/`month`.

### R30 · Small optional additions · `MINOR` · agent

- `sa_nca_2005` gives no Gazette number or date. This was not confirmed online:
  - a recollection, not checked, gives GG 28619 of 15 March 2006;
  - gov.za lists only the commencement notice, GG 28824 of 11 May 2006.
- `nids_w5_2018`: DataCite gives publication year 2017 (DataFirst's citation says 2018).
  Immaterial.
- Several reports print as "Technical report"; set `type` where a better label exists.

---

## Private notes in `main.bib` that are wrong

These do not print, but they record the reasoning behind modelling choices.

### R31 · TransUnion "CORRECTED 2026-08-24" note is itself wrong · `MINOR` · agent

`transunion_cps_sa_2025`: Fig. 11 ("Type of new credit and loan activity planned in next 12
months, among those who plan to apply") lists "New buy now, pay later payment services 20%", and
separately "New car loan or lease 20%". The original note (20% intend to apply for BNPL) was
right. Also, the 57% holding figure is not in this report; it is in the 24 March 2026 release
(`transunion_cir_sa_2026`) only.

### R32 · HomeChoice "2.12 per annum, R7,000" is not group-wide · `MAJOR` · Marc

The `homechoice2024ir` note dismisses this metric as "group-wide fintech spend per customer, not
a BNPL basket". The report states it in the BNPL paragraph: "Customers purchase more frequently
and at higher amounts as they get familiar with the concept and affordable convenience of
splitting payments at the till. Frequency is up to 2.12 per annum, average spending is up 21% to
7 000". Two consequences:
- The FY2025 report gives 3.9× for FY2024, against 2.12 here, so the two frequency measures are
  defined differently. That weakens reading 4.4× as a rate per active customer.
- If R7,000 is annual BNPL spend per customer (about R5,021 in 2017 Rands), it lies above the
  band top of R4,261 (`tab_bnpl_on_checks.tex:20-21`).

The β = 0 "below the band" verdict would not change. **Closes when** the note is corrected and
the band's definition is checked against this.

### R33 · HomeChoice note overstatements · `MINOR` · agent

- "Audited basis" for the "low and grow" policy: it is narrative in the integrated report, not
  audited financial statements, and it is group-wide credit strategy, not BNPL-specific.
- "Reproducing the cumulative chart at every shared year" is approximate. The annual series sums
  to R0.95bn, R2.48bn and R6.40bn, against the charted R0.9bn, R2.4bn and R6.3bn (gaps of 5.4%,
  3.2% and 1.6%).
- `extract_bnpl_anchors.py` says "~3%" for the derived FY2025 GMV gap. The actual gap is 5.7%
  (R6,698m against the stated R7.1bn).

### R34 · Business Day note · `MINOR` · agent

`businessday_bnpl_2026`:
- The article says "memorandum of **agreement**", not of understanding.
- The note says the February 2027 date is attributed only to an industry CEO. The article's lead
  paragraph attributes it to the NCR ("the NCR ordering providers to begin reporting … from
  February next year"). It is true that no quoted NCR text contains the date.
- The body is the "Credit Bureaus Association".

The thesis text itself is fine.

---

## Checked and correct

No change needed. Metadata matches the publisher or issuer record and the cited claims are
supported for:
- **ODD and methods:** `grimm2020odd`, `windrum2007validation` (except R11), `yun2020housing`,
  `dorazio2017micro`, `granovetter1978threshold`.
- **BNPL evidence:** `dimaggio2022bnpl`, `hayashi2025constraints`, `wang2026buynow` (45% + 16% =
  61% subprime), `Keys2019`, `cfpb2025bnpl` (except R13), `woolard2021` (para 4.42 quotation;
  £88 and £110 confirmed absent).
- **Regulators and income statistics:** `fca_ps26_1` (except R18), `asic2020rep672` (Table 2,
  21% missed a payment), `ons_income_fye2020` (£30,500 after the 2022 correction; 39.3%),
  `abs_income_2019_20` ($959 a week; 48.1%).
- **South African statistics:** `statssa_cs_2016` (3.3; 16.9m households), `statssa_lmd_2022`
  (all transition rates), `nids_w5_2018` (10,841 of 13,719; 18.67m; store-card and hire-purchase
  medians reproduced from microdata), `statssa2019inequality`, `hundenborn2018drivers`,
  `ncr_cbm_2017` (21.7%, 39.3%), `ncr_ccmr_2017` (14.21%, R392.0bn, 24.8 months), `statssa_ies_2023`
  (κ = 0.1387 reproduced).
- **South African regulation and press:** `sa_ncr_ratecaps_2016` (every Table A rate),
  `nortonrose_bnpl_sa` (quotation verbatim), `sarb_fsr_2026_1` (Box 4 quotations verbatim),
  `finasa_bnpl_2026`, `dcasa_bnpl_2026`.
- **Providers and issuers:** `payflex_terms` and `payflex_limits` (clauses and fees; R95 →
  R125.74 and R285 → R188.61 at 1.511057), `payjustnow_terms` (purchase limit; 25% fee cap),
  `weaver2025iar` (R13.1bn / 9.4m = R1,393.6 → R992 in 2017 Rands; band R1,333 to R4,261
  recomputed).

---

## Resolution: 2026-10-12

Two independent verifiers re-checked every finding against the sources before anything changed. A third checked the edits afterwards. All 34 findings were confirmed, some in part. Every one is now reflected in the thesis, bibliography or code, except R22, which needs no change. Where the verifiers changed a finding:

- **R3.** 2022–2024 (7.04, 6.08, 4.36) are the World Bank FP.CPI.TOTL.ZG series, not Stats SA. Not regenerated: a whole-chain check against Stats SA's CPI history table gives 107.5/71.4 = 1.506 against the chain's 1.511, so no deflated parameter moves by more than 0.4%. Documented in appendix D, appendix C, the config, the script and the bib.
- **R9.** Reproduced, and slightly understated: with family loans, informal loans are 2.7% of weighted D_trad (`notebooks/scripts/check_reference_audit_figures.py`, `results/summary/reference_audit_checks.json`). Section 2.2 states it; the claim that informal borrowing is absent from the data is removed.
- **R12.** Hamill et al. use a consecutive-period default rule, so they are cited for the form of the rule. `k_default` is relabelled *assumed*.
- **R16.** The 25-month term is derived from the CCMR book and flow, not published.
- **R20.** Reproduced: 0.651 by household and 0.663 by person.
- **R21.** Not resolved: Marc should check in the full text whether the experiment's two options differed in cost. The text now says only what the abstract supports.
- **R28.** Confirmed from the questionnaire: FinScope's banked flag counts SASSA-card-only adults by design (13% of adults). Stated in Section 3.2. Whether they should be BNPL-eligible is Marc's call; the model treats them as eligible.
- **R32.** The R7,000 figure is BNPL spend in the PayJustNow passage, about R5,000 in 2017 Rands, above the band's top. The note to `tab:bnpl-on-checks` now says so. The β = 0 "below" verdict does not depend on the band's top.
