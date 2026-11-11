# C. Reference audit: thesis at commit 226a515 (main), 2026-11-11

This audit was read-only: no repo file was edited. It covers `thesis/main.tex`, `chapters/*.tex`, `chapters/generated/*.tex`, `main.bib`, `main.bbl`, `main.log`, `main.blg` and the compiled `main.pdf` of 10 Nov 15:24, which postdates the last commit.

**How it was done.**
- **My own checks:** the mechanics (aux, bbl, blg and log), the rendered reference list and in-text citations in the PDF, and two sources from their local copies:
  - `references/NCR_CBM_March_2017.pdf`, which is byte-identical (same md5) to the live NCR URL;
  - `references/sarb_fsr_2026_1.pdf`.
- **Delegated checks:** four parallel verifiers covered academic articles, international regulators, SA statutes and statistics, and SA press and providers. Each opened the source (DOI or Crossref, publisher page, or downloaded PDF/HTML) and returned quotes with page numbers. Their working copies are in the scratchpad (`refs2/`, `regsrc/`, `dl_sa/`, `dl_press/`).
- **The previous audit** (`docs/REFERENCE_AUDIT.md`, 2026-10-12) was read first but not relied on. Every source was re-opened.
- **How each source was read** is stated wherever it matters: **[FT]** means the cited passage was read in the full text; **[ABS]** means abstract or publisher summary only.

**Bottom line.**
- Every cited key exists, every work exists, and the metadata are right. Hayashi & Routh is the one entry that is incomplete.
- No claim is contradicted by its source, and no number differs from its source. Every number checked reproduces.
- The problems are of three kinds:
  - wording that goes past the source (February 2027, Ackert's design, s.66A, the NIDS denominator);
  - one secondary-for-primary citation (Wang for CFPB data);
  - in-text citation forms that render badly.
- There are **no HIGH findings**.

---

## (a) Status of every cited key (52)

| Key | Status | Notes (what was opened) |
|---|---|---|
| abs_income_2019_20 | VERIFIED | ABS page: "Household Income and Wealth, Australia", released 28/04/2022. Table 1a gives $959 a week. |
| ackert2025bnpl | VERIFIED | Crossref: JBF 26(4) 558–569. Full text was paywalled in this pass [ABS + T&F endnotes]. |
| alizadeh2015activation | VERIFIED | JASSS 18(3) 8 [FT]. |
| asic2020rep672 | VERIFIED | REP 672, cover "November 2020", released 16 Nov 2020 [FT]. |
| businessday_bnpl_2026 | VERIFIED | Mochiko, 15 Aug 2026, Business Times [FT]. Paywalled ("PREMIUM"). The URL slug differs from the headline, but it is the publisher's own slug. |
| cardaci2018inequality | VERIFIED | JEBO 149, 434–458 [ABS]. |
| cfpb2025bnpl | VERIFIED | Cover "January 2025", 35 pp. [FT]. |
| comer2013activation | VERIFIED | Procedia CS 20, 183–188 [ABS]. |
| dcasa_bnpl_2026 | VERIFIED | Dated 21 Jul 2026. The page title uses an en dash ("BUY NOW PAY LATER – SACRRA Roundtable Feedback") where the bib has a colon. Trivial. |
| dehaan2024bnpl | VERIFIED | Management Science 70(8) 5586–5598 [ABS + working paper FT]. |
| dimaggio2022bnpl | VERIFIED | NBER WP 30508, Sep 2022 [FT]. No published version found (NBER, OpenAlex, search on 11 Nov 2026). |
| dorazio2017micro | VERIFIED | JASSS 20(1) 9 [FT]. |
| fca_ps26_1 | VERIFIED | Title exact; published 11 Feb 2026. Optionally add the day. |
| finasa_bnpl_2026 | VERIFIED | Title exact; 30 Apr 2026. |
| finscope2019 | VERIFIED in part | Pocket Guide URL 200 (PDF created Nov 2020). The licensed dataset's release year cannot be checked externally. |
| granovetter1978threshold | VERIFIED | AJS 83(6) 1420–1443 [ABS]. |
| grimm2006odd | VERIFIED | All 28 authors, in order (Crossref). |
| grimm2020odd | VERIFIED | JASSS 23(2) 7, 19 authors [FT]. |
| hamill2023creditcard | VERIFIED | IJBM 43(4) 849–870, 2025 (Crossref). Claims read in arXiv:2311.01901v2 [FT]. The key says 2023, but keys do not print. |
| **hayashi2025constraints** | **ENTRY ERROR (incomplete)** | Volume, issue and DOI are right, but the printed entry has no pages, no URL and no DOI, so a reader cannot locate it. Add `pages = {1--18}` (the article is paginated separately) and `url = https://www.kansascityfed.org/research/economic-review/financial-constraints-among-buy-now-pay-later-users/`. |
| homechoice2024ir | VERIFIED | "HomeChoice International plc / 2024 Integrated Annual Report", PDF created Apr 2025 [FT]. |
| hundenborn2018drivers | VERIFIED | WIDER WP 2018/162, Dec 2018; DOI correct [FT]. |
| Keys2019 | VERIFIED | JFE 131(3) 528–548 [ABS + NBER w22742 FT]. |
| Kuchler2021 | VERIFIED | JFE 139(2) 359–388 [ABS + NBER w24881]. |
| madeira2018chile | VERIFIED | JFS 39, 209–220 [ABS]. |
| meier2010present | VERIFIED | AEJ: Applied 2(1) 193–210 [ABS]. |
| ncr_cbm_2017 | VERIFIED | Checked by me; local copy identical to the live URL (HTTP 200). |
| ncr_ccmr_2017 | VERIFIED | 31-page PDF, HTTP 200 [FT]. |
| nids_w5_2018 | VERIFIED (minor) | DataFirst catalogue 712, v1.0.0, produced 13 Aug 2018. DataCite gives 2017 (a metadata quirk; keep 2018). The entry has no access date, omits the DPME funder line and renders "wave 5" in lower case. |
| nortonrose_bnpl_sa | VERIFIED | Jan 2023. The en-za URL now redirects to /en-africa/. |
| ons_income_fye2020 | VERIFIED | Released 21 Jan 2021, corrected 22 Mar 2022 (£30,500) [FT]. |
| payflex_limits | VERIFIED | Live FAQ now 404; the cited Wayback copy of 10 Nov 2024 works. |
| payflex_terms | VERIFIED | Live page modified 23 Oct 2026, after the access date. The relevant clauses are identical in the Wayback copy of 25 Sep 2026; consider citing that snapshot. |
| payjustnow_terms | VERIFIED | Live page modified 22 Oct 2026, after the access date. Not diffed against an archive. |
| sa_nca_2005 | VERIFIED | GG 28619, Notice 230, 15 Mar 2006 (front page read). |
| sa_ncr_affordability_2015 | VERIFIED | GN R202, GG 38557, 13 Mar 2015; Table 1 on p. 19. |
| sa_ncr_ratecaps_2016 | VERIFIED | GN R1080, GG 39379, 6 Nov 2015, Table A pp. 108–109. Commencement on 6 May 2016 confirmed by the NCR release. |
| sarb_fsr_2026_1 | VERIFIED | Checked by me; local PDF and URL 200. Box 4, pp. 24–25. |
| sarb_mpc_2017_03 | VERIFIED | 30 Mar 2017 statement, p. 9 [FT]. |
| statssa2019inequality | VERIFIED | Report 03-10-19, 2019 [FT]. |
| statssa_cpi | VERIFIED | P0141 June 2026, released 22 Jul 2026 [FT]. |
| statssa_cpi_history | VERIFIED | Table B1, HTTP 200. The file is updated monthly (current copy dated Oct 2026), so the access date matters. |
| statssa_cs_2016 | VERIFIED | Archive URL 200, original 404, as the note says. The annote's "p. 68" is wrong (printed p. 59 / PDF p. 69); it does not print. |
| statssa_ies_2023 | VERIFIED | v1.1 matches the file used. The DOI now lands on v1.2 (2026). |
| statssa_lmd_2022 | VERIFIED | The CIP says 2022, but the PDF was produced Nov 2023, so 2023 is defensible. Optionally add "published November 2023". |
| transunion_cir_sa_2026 | VERIFIED | Media release, 24 Mar 2026. |
| transunion_cps_sa_2025 | VERIFIED (LOW) | `month = oct` is the PDF's creation date; the public release was 13 Jan 2026. The URL is a third-party host (fanews); TransUnion's own report page returns 403 to scripts. |
| wang2026buynow | VERIFIED | Economic Brief 26-05, February 2026 [FT]. |
| weaver2025iar | VERIFIED | Weaver Fintech, PDF created 30 Apr 2026 [FT]. |
| windrum2007validation | VERIFIED | JASSS 10(2) 8; no DOI exists for this issue [FT]. |
| woolard2021 | VERIFIED | "Report to the FCA Board, published 2 February 2021" [FT]. |
| yun2020housing | VERIFIED | JASSS 23(4) 5 [FT]. |

---

## (b) Claim-support findings

No HIGH findings: no cited source contradicts the thesis, and no number differs. The findings are ordered by severity.

### MED

**M1. Feb 2027: what the source attributes to the NCR versus to an industry CEO.** `01_introduction.tex:31-32`; abstract `main.tex:106-107`.
- **Thesis (01:31-32):** "records are reportedly expected on consumer profiles from February 2027~\citep{businessday_bnpl_2026}".
- **Thesis (abstract):** "Bureau reporting of BNPL is reportedly due from 2027."
- **What Business Day says [FT]:**
  - The lead, attributed to the NCR: "the National Credit Regulator (NCR) ordering providers to begin **reporting** consumer payment behaviour to credit bureaus from February next year".
  - Display on profiles comes only from the Happy Pay CEO: "this information will begin **appearing on consumers' credit profiles** from February 2027. The reporting itself is already live and ongoing."
- **Why both sentences need care:**
  - The body sentence matches the CEO's statement, not the NCR's reported order.
  - The abstract's "reporting … due from 2027" sits uneasily with DCASA ("more than two million BNPL records were submitted during May"), with FINASA ("Reporting of BNPL data to [SACRRA] is currently live", as test data) and with the CEO himself.
- **Fix:**
  - Body: "the NCR is reported to require providers to report from February 2027, and one provider expects the records to appear on consumer profiles from then".
  - Abstract: "Bureau records of BNPL are reportedly to be displayed from 2027".

**M2. Ackert et al.: a between-subject design described as a choice.** `appendix_a_rationale.tex:29-32`; also `01_introduction.tex:148-149`.
- **Thesis (appendix A):** "In the one experiment on the choice, BNPL was interest-free and the card charged 24.99% a year … For groceries, the one necessity, participants chose the two equally often."
- **Thesis (01):** students "more often finance a discretionary purchase with interest-free BNPL than with a credit card".
- **The design:** the published note 6 [T&F endnotes] and the bib annote (from the SSRN full text) both describe random assignment to separate BNPL and card arms. Participants decided whether to buy under one method; they did not choose between BNPL and a card.
- **Abstract:** participants are "more likely to purchase an item with a BNPL loan, as compared to a credit card loan".
- **"The one experiment"** is also too strong. Jose, Kelly, King & McCarthy (Central Bank of Ireland RTP 2025 No. 15) run a BNPL experiment, against debit cards.
- **Not re-verified in this pass (paywalled):** 24.99%, "neither clearly cheaper" and 69% vs 72%. They rest on the previous audit's reading of the SSRN text.
- **Fix:**
  - Appendix A: "In the one experiment we found that compares BNPL with a credit card … grocery purchase rates were similar under the two".
  - 01: "are more likely to buy a discretionary item when it is offered with interest-free BNPL than with a credit card".

**M3. Section 66A's fourteen-day right attributed to PS26/1.** `appendix_b_register.tex:113`; `appendix_c_supplementary.tex:201-204`.
- **Thesis:** "the fourteen-day right of withdrawal under section 66A of the United Kingdom's Consumer Credit Act 1974, which the FCA confirms applies to regulated deferred payment credit~\citep{fca_ps26_1}".
- **What PS26/1 says [FT]:**
  - It mentions s.66A once, conditionally, in new guidance CONC 11.1.2A G (instrument FCA 2026/2, PDF p. 96): "there is no right to cancel under CONC 11.1.1R in respect of a regulated deferred payment credit agreement to which section 66A (Right to withdraw) of the CCA applies".
  - It never says "14 days".
- **Where the clear statement is:** CP25/23, Table 1, p. 17: "consumers will have recourse to withdrawal rights under section 66A CCA".
- **Where the 14 days is:** s.66A of the Act itself.
- **Fix:** cite CP25/23 (Table 1, p. 17) and the Act (legislation.gov.uk, s.66A) alongside PS26/1, or write "which the FCA's rules treat as applying".

**M4. Wang cited for CFPB data (a secondary source).** `01_introduction.tex:143-145`.
- **Thesis:** "Wang~\citeyearpar{wang2026buynow} reports that borrowers with subprime or deep subprime credit scores accounted for most BNPL originations in 2021 and 2022".
- **Wang [FT]:** "From 2021 to 2022, borrowers with deep subprime credit scores … accounted for 45 percent of BNPL originations, while those with subprime … another 16 percent". His footnote 9 gives the source as the CFPB's January 2025 report.
- **The CFPB report** (`cfpb2025bnpl`, p. 2, Key findings; I read this in the downloaded PDF) says the same: "Borrowers with subprime or deep subprime credit scores make up the majority of BNPL originations. From 2021 to 2022 … 45% … another 16%".
- **Fix:** cite `cfpb2025bnpl` (p. 2) for the figure, and optionally "61% of originations over 2021–22". The number itself is right.

**M5. The NIDS 13,719 denominator.** `03_calibration.tex:112-114`.
- **Thesis:** "Keeping the records with reported income, a valid household size and a positive sampling weight leaves 10,841 of 13,719 households; every excluded record has a zero or missing weight."
- **What the data show:** DataFirst's `w5_h_outcome` gives 10,842 "Successfully Interviewed" of 13,719 records. The other 2,877 are refusals (1,096), not located (808), not tracked (778), household deaths (176) and moved abroad (19). So the filter drops one interviewed household, not 2,878 records with bad data.
- **Reproduced:** 10,841 records with w5_wgt > 0; Σw = 18.670 m households; Σw × hhsize = 56.52 m people.
- **Fix:** "10,841 of the 10,842 successfully interviewed households (the file holds 13,719 household records, including non-respondents)".

**M6. NCR acts known only through secondary sources.** `01_introduction.tex:26-29`; `02_model.tex:135`; `appendix_b_register.tex:91`.
- **Two NCR acts are cited only through other parties:**
  - the "formal notification to the industry" (BNPL not credit at inception, but possibly incidental credit when default fees are levied), via Business Day;
  - the "formal instruction to disallow the live processing of BNPL data", via FINASA.
- **The quotes are accurate [FT].** The thesis flags the first as "Press reports describe" (plural, although one report is cited).
- **Fix:** cite the NCR documents if they can be obtained. Otherwise keep the hedges and make "Press reports" singular.

### LOW-MED

**L1. Hayashi & Routh: "disproportionately liquidity-constrained".** `02_model.tex:230-231`.
- **What the paper says [FT, §III p. 9]:** "BNPL users are significantly more likely to face financial constraints than BNPL nonusers". It never uses the word "liquidity-constrained". Its 11 indicators mix credit and liquidity ("most indicators are related to both constraints", p. 8).
- **The liquidity indicator does differ:** lacking three months' expenses, 51% vs 28% (Chart 2, p. 10).
- **Fix:** "BNPL users are more likely to face financial constraints, including lacking three months' expenses". 01:141-143 is fine as written.

**L2. Pattern-oriented modelling cited only to Grimm et al. (2020).** `03_calibration.tex:326`; `01_introduction.tex:127-128`.
- **What the 2020 update offers [FT]:** it adds the element "Purpose and patterns".
- **The problem:** it also has a section headed "ODD is not clearly linked to pattern-oriented modelling" and names Grimm et al. (2005, *Science* 310) as "the primary publication on POM". It does not discuss keeping fitting patterns separate from validation patterns.
- **Fix:** add Grimm et al. (2005) for POM, or a later POM reference that sets out the patterns workflow; keep the 2020 paper for the ODD element.

**L3. FinScope claims rest on the questionnaire, not the cited Pocket Guide.** `03_calibration.tex:132-134`; `03:235`.
- **The 13% figure** is supported by the Pocket Guide, p. 19: Banked 68 / SASSA card only 13 / Unbanked 19; "only 13 % (or 5.3 million) grant recipients who have one SASSA card only".
- **Two claims rest on the questionnaire alone:**
  - that the banking question counts a grant card as an account, from Q.F1 ("SASSA CARD … USED FOR GRANT PAYMENTS IS A BANK ACCOUNT");
  - "repayable within 31 days", from Q.G13 ("a short-term loan repayable within 31 days after take up").
- **Fix:** cite the FinScope SA 2019 questionnaire (Q.F1, Q.G13), in the note or as its own entry.

**L4. UK equivalence-scale statement without a source.** `appendix_b_specification.tex:86-90`.
- **The Australian sentence** is supported by `abs_income_2019_20`, which is not cited at that sentence. The ABS text says: "assigns a value of 1 to the household head … For a lone person household, equivalised income is equal to actual income".
- **The UK sentence** ("sets a couple's equivalised income equal to its income") is correct but appears in no cited source. ONS states it in *The effects of taxes and benefits on household income, technical report: FYE 2019* (25 Jun 2020): "rescaled so that a two adult household equivalence value is 1.0".
- **Fix:** cite that ONS report for the UK sentence, and `abs_income_2019_20` for the Australian one.

**L5. Regulation 23A excludes incidental credit (missing caveat).** `05_policy.tex:11-13`; `02_model.tex:143-147`.
- **What the regulation says:** 23A(2)(e): "These Regulations … do not apply to … (e) an incidental credit agreement".
- **Why it matters:** the NCR's reported position is that BNPL may become incidental credit (01:28-29). Screening BNPL under Reg 23A is therefore a policy analogue, not current law.
- **Fix:** add one sentence in Section 5.

### LOW

**N1. DCASA, `01:29-31`.** Source: "more than two million BNPL records were submitted during May. However, these are not yet being displayed … while the appropriate reporting and classification framework is finalised". In the source, "while finalised" goes with non-display, not with submission. Reword.

**N2. `appendix_b_register.tex:91`, "not displayed … before the 2026 arrangements".** DCASA and FINASA describe July and April 2026, not the period before. Write "as of July 2026", or add the Business Day COO quote ("The traditional reporting framework did not accommodate BNPL data").

**N3. FINASA, `02_model.tex:158`, "preliminary score reductions reported".** The source says "could reduce … potentially negatively affecting roughly a quarter". These are projections. Write "projected". `01:33-34` is fine.

**N4. Business Day, `01:27`, "Credit Bureau Association".** The article spells it "Credit Bureaus Association". The thesis spelling is the body's real name; keep it.

**N5. TransUnion CPS, `01:11-13`.**
- **Source:** Fig. 3, p. 2: "Expect to be unable to pay at least one of their current bills and loans in full", 36%.
- **Optional:** add "in full".
- **Sample:** an online panel, "results are unweighted" (p. 9).

**N6. TransUnion CIR, `03:444-446`, 57%.** The figure is verbatim in the release [FT]. It comes from the same unweighted online panel, which is worth a clause, because it is compared with model adoption.

**N7. ASIC, `01:183-185`.**
- **Source, p. 4:** "21% of buy now pay later users who were surveyed missed a payment in the last 12 months". This is supported.
- **Regulatory status, same page:** BNPL providers "are generally considered not to be regulated under the National Consumer Credit Protection Act 2009 (National Credit Act). However … regulated as credit under the … ASIC Act 2001".
- **Fix:** "generally sat outside … though regulated as credit under the ASIC Act". REP 672 is an "industry update", not a "review" (REP 600 was the review).

**N8. CFPB stacking share (`04:86-87`, `03:437`, `tab_bnpl_on_checks:18`, `tab_stacking:7`).** Supported. Table 4, p. 18: 31.7% (2021) and 32.6% (2022), per year, simultaneous meaning a second loan within 42 days at a different firm. Footnote 24, p. 17: "likely an undercount". "United States borrowers" means borrowers at six large firms; optionally say so.

**N9. HomeChoice 2024 IAR, `generated/tab_bnpl_on_checks.tex:7`.**
- **Thesis:** "average spending of R7,000 per customer".
- **Source, PDF p. 18, in the PJN/BNPL passage:** "Frequency is up to 2.12 per annum, average spending is up 21% to 7 000". There is no "R", and no "per customer".
- **Fix:** add "(denominator not stated)".

**N10. Weaver IAR volume band (`tab_bnpl_on_checks:19-21`).** Reproduces: 7.1 bn / 3.7 m / 1.4391 = R1,333, and (13.1 bn / 9.4 m) × 4.4 / 1.4391 = R4,261.
- **Caveats:**
  - 3.7 m is cumulative sign-ups, set against FY2025 GMV.
  - The R7.1 bn "at our retailer partners" may include PayStretch.
  - The R992 mean purchase uses a different deflator (1.4047) from the band (1.4391).
- **Fix:** state both formulas and both deflators in the note.

**N11. Low-and-grow policy, `02_model.tex:276`.** `homechoice2024ir` supports it as group-wide credit strategy, not as a BNPL rule (PDF p. 40). This is fine as cited, because the row does not claim more.

**N12. Payflex, "25% at checkout" (`02:280`, `register:103`).** The terms (cl. 1.1.7) give four instalments, the first upfront and the rest "every two weeks for six weeks". The equal 25% split is on payflex.co.za/how-it-works/. Add that page or drop "25%". The fee clauses (1.1.5, 7.1, 8.2, 8.5) and the absence of a maximum order value (cl. 4.4) are verified verbatim.

**N13. Short-term 60% (`tab:credit-terms`, 03:235).** 5% a month applies to a first loan; repeat loans in the same calendar year are capped at 3% a month (GN R1080 Table A item 5). Say "first-loan maximum".

**N14. CCMR 14.21% (`01:7`).** This is pooled by the author from Table 21 (credit facilities) and Table 23 (unsecured) on p. 29. All bands reproduce exactly (71.63 / 8.24 / 3.59 / 2.32 / 1.76 / 12.45). The CCMR never prints the pooled figure. Say "computed from Tables 21 and 23".

**N15. Other CCMR checks.**
- R392.0 bn = credit facilities 223.578 + unsecured 165.745 + short-term 2.667 (Table 1.6, p. 5). Name the three categories in the table note.
- 65.83% "≤1 Month" (Table 6.2, p. 17) covers quarterly-return filers only; most short-term lenders are excluded. Add a caveat.

**N16. LMD conversions (`03:265-269`, `register:37-41`).**
- **Re-employment:** 11.6% a quarter (Table 2.1a, p. 15) gives 1.87% a tick only with 6.52 ticks per quarter; with exactly 6.5 it gives 1.88%.
- **Separation band:** 0.54–1.17% combines the narrow minimum (3.5%, Q3→Q4 2017) with the broad maximum (7.4%, Q4 2017→Q1 2018, which ends in 2018).
- **QLFS versus NIDS unemployment:** LMD Table 2.2 (p. 105) gives the QLFS 2017 rate as 27.5%; the NIDS figure (1,113/5,783 = 19.2%) is the thesis's own.
- **Fix:** state the conversion, and give both unemployment numbers at 03:269.

**N17. CPI (`appendix_d:272`).** The 2025 rate used, 3.22, is computed from index averages (102.5/99.3); Stats SA prints 3.2. "Stats SA annual averages" is therefore slightly loose. All other numbers reproduce (5.0%, 107.5, 71.4, 6.9 / 6.0 / 4.4, and the World Bank's 7.04 / 6.08 / 4.36).

**N18. Hamill et al.**
- **Supported:** `01:122-124` and `appendix_c:291-294`. §6.1: promotions "could potentially escalate customer indebtedness"; "the fractions of accounts with missed payments remain approximately constant".
- **Middle-income peak (§5):** a stylised fact reproduced from Kincses (2010), measured as card balance-to-income.
- **Note:** the balance effect is small (£3,846 to £3,909).

**N19. Cardaci, `01:109-111`.** The abstract says "paving the way for a financial crisis", not a "banking crisis". "Collateralised debt" is supported: "collateralised consumption loans and mortgages"; "home equity extraction" [ABS].

**N20. Madeira.** Madeira describes a "heterogeneous agents model", but it is listed under "Agent-based models" (`01:105-117`). Consider "heterogeneous-agent".

**N21. Comer & Loerch, and Alizadeh & Cioffi-Revilla.** Neither tests a fixed order. They justify a robustness arm, which is how the register now uses them.

**N22. deHaan et al., "larger increases among heavier users" (`01:39`).** Supported in the working paper's §4.4 ("significantly larger for high-intensity users", where high intensity means more BNPL providers). It was not confirmed in the published version, which was blocked. "Users of more BNPL providers" is more exact.

**N23. Keys & Wang (`01:165`, `app_a:36`, `register:75`).** Supported verbatim: "29% of accounts regularly make payments at or near the minimum"; "At least 22% of near-minimum payers (and 9% of all accounts) respond … consistent with anchoring". The 29% is a sample share (about a quarter of the US general-purpose card market).

**N24. Kuchler & Pagel.** The paper concerns self-set paydown plans, not contractual instalments. "Motivated by" is right; do not say more.

**N25. Meier & Sprenger, "predicts".** The paper reports a correlation. Fine in the statistical sense.

**N26. Hundenborn et al., 0.66 (Table 1, p. 3).** Verified. That it is person-weighted is inferred from N_weighted = 54.9 m and is not stated in the paper.

**N27. Norton Rose.** The quote is verbatim, but the source says "BNPL models", not "interest-free" ones. "Takes the same view" is acceptable.

**Verified with no issue:**
- `sarb_fsr_2026_1`, read by me. Box 4, p. 25: "This perceived affordability, together with the ability to hold multiple concurrent BNPL obligations, increases the risk of over-indebtedness"; approval "based on less rigorous credit checks, rather than the full credit assessments that characterise traditional unsecured credit agreements"; footnote 5: "providers often argue that these products fall outside the NCA because they do not charge explicit interest or upfront fees". This supports `01:17-24`.
- `ncr_cbm_2017`, read by me:
  - p. 2: "39.3%, comprising of 21.7% of consumers in three months or more in arrears, 11.4% … adverse listings, and 6.2% … judgments".
  - p. 8, Definitions: "Impaired record: A record on which a consumer and/or any of the accounts, are either classified as three or more payments or months in arrears, or which has an 'adverse listing', or that reflects a judgment or administration order".
  - p. 1: bureaus receive data "from credit providers, courts and utility service providers".
  - This supports `02:196-198`, `03:347-353` and `register:89`.
- `sarb_mpc_2017_03`, p. 9: "keep the repurchase rate unchanged at 7.0% per annum".
- `sa_nca_2005` s.81(2).
- Reg 23A, Table 1, p. 19: every band and the two hand checks (R881.00 and R1,505.38) reproduce.
- GN R1080 Table A: every rate in `tab:credit-terms`.
- Community Survey: 3.3, printed p. 59.
- Inequality Trends: Table B3, p. 165, 0.67 for 2015.
- Woolard: para 4.42, p. 49, verbatim (£1,000).
- ONS: £30,500. ABS: $959 → 0.481.
- ASIC: Table 2, p. 10, A$2,000.
- Di Maggio et al.: both claims [FT], pp. 2 and 8–9.
- D'Orazio & Giulioni, Yun & Moon, Granovetter [ABS], Grimm et al. (2006/2020) for ODD, Windrum et al.
- PayJustNow: an individually assigned purchase limit, and default charges capped at 25%.
- Payflex limits FAQ, verbatim.

---

## (c) Mechanical and formatting findings

**Integrity**

1. **Keys and warnings.**
   - 52 distinct keys are cited (main.aux), and all 52 are in main.bib.
   - The blg reports "You've used 52 entries" and `warning$ -- 0`. main.log has no "Citation … undefined" lines; its "undefined" lines are acronym-package info messages.
2. **Uncited entries** (6, which do not print under BibTeX): `cfpb2025market`, `ncr_ccmr_2025` (no URL), `payjustnow_limits`, `sa_bnpl_basket_2026` (still marked % VERIFY), `weaver2025results`, `worldbank_gini_zaf`.
3. **No duplicates.**
   - No duplicate entries.
   - No work is cited under two keys. Distinct pairs: `cfpb2025bnpl` and `cfpb2025market`; `weaver2025iar` and `weaver2025results`; `statssa_cpi` and `statssa_cpi_history`.
   - Year suffixes are correct: NCR 2017a = CCMR and 2017b = CBM; RSA 2015a = rate caps and 2015b = affordability (ordered by title, as agsm does); Stats SA 2026a = CPI and 2026b = CPI history.

**Rendering, from main.pdf and main.bbl**

4. **No DOI prints for any article.** agsm ignores the `doi` field, so journal articles carry neither a DOI nor a link, while web sources carry URLs. Hayashi & Routh (no pages) cannot be located from the list at all. Add DOIs, for example via `url = {https://doi.org/...}`, or use a Harvard style that prints DOIs.
5. **Double brackets from acronym first-use plus `\citeyearpar`.**
   - `01:39`: "The Consumer Financial Protection Bureau (CFPB) (2025) documents".
   - `01:183`: "The Australian Securities and Investments Commission (ASIC) review (2020) found" (and REP 672 is not a review).
   - `01:181-182`: "the Financial Conduct Authority (FCA)'s approach … (Financial Conduct Authority, 2026)".
   - Fix with `\acused` plus `\citet`, or by moving the citation to `\citep` at the end of the clause.
6. **The year detaches from the name** at `03:252`: "informed by Woolard's illustrative stacked exposure (2021)". Use "Woolard's~\citeyearpar{woolard2021} illustrative …".
7. **"Windrum, Fagiolo and Moneta" is hard-coded** at `01:127`, where agsm prints "Windrum et al." elsewhere (03:327 and Table 1), and other three-author works use "et al.". Use `\citet`.
8. **The one direct quotation has no page.** The Credit Bureau Monitor quote at `02_model.tex:197` and `appendix_b_register.tex:89` is verbatim, but it lacks the page. Add p. 8 (Definitions).
9. **Sentence-casing has broken some capitals.** "wave 5" (NIDS), "table B1" (CPI history) and "first quarter, March 2017" print in lower case. "Buy now pay later" is lower case in ASIC and DCASA but braced title case in CFPB, Wang, Hayashi, Di Maggio and Ackert. Brace the proper nouns or apply one convention throughout.
10. **Mixed title typography.**
    - `@techreport` titles print plain: CS 2016, LMD, CFPB, the IARs.
    - Comparable `@misc` works print in quotes: IES 2022/23, NIDS, FinScope datasets, provider terms.
    - No standalone work is italicised, which is the usual Harvard convention.
    - The SARB FSR also prints a redundant type: "Financial Stability Review, first edition 2026, Review".
11. **The access-date convention is non-standard.** Each entry prints "Accessed … Available at: URL" in that order; the usual form is "Available at: URL (Accessed: date)". The list is consistent, so this is only a convention point.
12. **Access dates are inconsistent or missing in two entries.**
    - `cfpb2025bnpl` prints "Accessed 29 September 2026" but has `lastchecked = 10 November 2026`.
    - `nids_w5_2018` has a URL but no access date.
13. **`statssa_cs_2016`** prints a note on HTTP 404 and the archive (unusual but informative). The archive URL uses http, not https.
14. **URLs that have moved or carry caveats.**
    - `nortonrose_bnpl_sa` now redirects to /en-africa/.
    - `businessday_bnpl_2026` is paywalled; say so in the entry.
    - The Payflex and PayJustNow terms pages changed after the access date; consider Wayback snapshots.
15. **Cited by year only.** The NCA and the regulations are cited as "(Republic of South Africa, 2005, 2015b)", which gives a reader no means to tell the Act from the regulations without the list. Consider naming the instruments in the text, as SA legal citation usually does.
16. **Wrong annotes.** These do not print, but the bib records reasoning in them:
    - `statssa_cs_2016`: "p. 68" should be printed p. 59.
    - `payflex_terms`: "automated credit assessment" is not in the terms (cl. 11.6 says "may seek information from any credit bureau").
    - `finscope2019`: banked share 82.4% against 82.8% in the thesis (donor share against imputed share).
    - `fca_ps26_1`: overstates PS26/1 on s.66A (see M3).
    - `transunion_cps_sa_2025`: `month = oct` is the PDF creation date; the public release was 13 Jan 2026.

---

## (d) Uncited claims (chapters 1–3 and 5–6) that need a source or a hedge

| Location | Claim | Suggested support |
|---|---|---|
| 02_model.tex:183-184 | BNPL is paid first, "an assumption based on platforms debiting a card automatically" | The Payflex and PayJustNow terms (card debit) or the CFPB report ("automatic repayment requirements", p. 2) |
| 03_calibration.tex:219-220 | "The NIDS non-food aggregate already includes clothing-account, hire-purchase and vehicle payments" | NIDS W5 questionnaire / derived-variable documentation (expenditure module) |
| 03_calibration.tex:268-269 | "NIDS records a lower unemployment rate than the QLFS" | Give both rates: QLFS 27.5% (LMD Table 2.2, p. 105) and NIDS 19.2% (own) |
| 03_calibration.tex:145 | "FinScope records one adult's holdings" | FinScope methodology / questionnaire |
| 03_calibration.tex:304-305 | "new accounts replenish the CCMR book" | CCMR Table 5.1 (credit granted per quarter) |
| 03_calibration.tex:369-370 | "underreporting may explain part of the gap" | A survey-debt underreporting source, or mark it as conjecture |
| 01_introduction.tex:32 | "no statutory commencement date has been confirmed" | DCASA ("the NCR is expected to issue guidance"), or rephrase as "no published NCR instrument sets a date" |
| 05_policy.tex:39-40 | "a bureau reporting with a lag would not show" (same-tick agreements) | A SACRRA monthly-submission source, or present it as an assumption |
| appendix_b_specification.tex:89-90 | The UK scale sets a couple's equivalised income equal to its income | ONS technical report FYE 2019 (see L4) |
| main.tex:106-107 (abstract) | "Bureau reporting of BNPL is reportedly due from 2027" | No citation is needed in an abstract, but align the wording with M1 |

No other uncited factual claims about the world were found in chapters 1–3 and 5–6. Statements such as "We found no South African study …" and "which no jurisdiction we found imposes" are the author's own search claims and are acceptable as worded.
