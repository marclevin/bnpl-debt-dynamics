# Fix pass, 2026-11-11: shared brief for every editing agent

The author asked for a comprehensive fix pass on the thesis after six audits (reports A to F in
this folder), and for language that is academic and free of AI-prose patterns. You apply the
audit findings that fall in YOUR files. An orchestrator reviews every diff afterwards.

## Hard rules

1. Edit only the files your prompt assigns. Never edit `thesis/chapters/generated/`, `notebooks/`,
   `simulation/`, `results/`, `docs/`, or (unless assigned) `thesis/main.bib`. If a finding needs a
   change in a generated table, the parameter register, a figure or a file you do not own, do not
   make it: list it under "For the orchestrator" in your final message, with the exact old and new
   text.
2. No git commands. Do not run latexmk or any build, any simulation, or any script other than the
   word counter: `python3 notebooks/scripts/wc_prose.py` (run from the repo root).
3. Word cap. The body is capped at 10,000 words and sits at 9,991. Your prompt gives a cap for each
   body file you own; finish at or below it. Check with the word counter before you finish and
   report the count. Appendices are not counted, but keep them tight.
4. No new numbers, facts or claims except those this brief supplies. Every number in the thesis is
   traceable to a generated table or a results/summary file. The LaTeX comments that name each
   number's source must be kept, and updated when you change a number.
5. Do not reword the research questions (01_introduction.tex, the quote block and the enumerate).
   Do not restructure the introduction, literature review or abstract; sentence-level fixes only.
   Do not add experiments, arms or results. A finding that needs a rerun, a design decision or new
   literature beyond what this brief names goes under "Left for the author", untouched.
6. Preserve LaTeX: labels, \ref targets, \ac{} acronym commands, \citep/\citet keys, table and
   figure environments, and the tilde ties. Do not change a label name. Check braces balance.
7. Where an audit finding is wrong, a matter of taste, or already handled by the text, skip it and
   say so in one line. Apply every HIGH and MED finding in your files unless a rule above or a
   decision below says otherwise; apply LOW findings where the fix is clearly right and costs no
   words.

## Voice (the author's own; this outranks any rewrite an audit report suggests)

- Short declarative sentences, one claim each, plain verbs, academic register. Present tense for
  what the model does and what the tables show.
- "We" is the authorial voice. "Detectable" means beyond two standard errors and is the house term;
  never write "significant" for it.
- A number comes with one standard error and a table or section reference. A limitation is stated
  once, where the claim is made.
- Forbidden: em dashes and en dashes used as punctuation (number ranges keep their existing form);
  sentence openers "However,", "Moreover,", "Furthermore,", "Notably,", "Importantly,",
  "Interestingly,", "Additionally,"; "X, not Y" and "not X but Y" as a rhetorical device;
  colon-then-reveal sentences; announcing sentences ("It is worth noting that", "This section
  shows"); padded lists of three; vague quantifiers where the tabulated number exists; the words
  delve, crucial, landscape, nuanced, leverage, underscore, highlight, robust (as filler), pivotal,
  key (as an adjective of emphasis), shed light, in order to.
- British/South African spelling. Percentage-point changes are "points" in the text.
- An audit report's suggested rewrite is a starting point. Rewrite it in this voice if it does not
  already match; compare with untouched sentences nearby before you finish.

## Decisions already made (apply these exactly where they touch your files)

D1. Stale labour figures (03_calibration.tex about lines 269-275; appendix_c_supplementary.tex about
    line 114). Correct values from results/summary/defaulter_credit.json: employment at the final
    tick is 0.2% below its starting level; 13.6% of the members employed at the start are out of
    work at the final tick; household income is 14.9% above its start in Q1, 5.3% below in Q4,
    5.8% below in Q5 (the largest fall) and 3.9% lower in total.

D2. Platform count. Section 4.3 must report that, of the 20 contrasts of two to six platforms
    against one across the four values of beta, two exceed two standard errors (two platforms at
    beta = 0, +0.22 +/- 0.10 points; five platforms at beta = 0.3, +0.22 +/- 0.11), about what
    chance gives, with no rising pattern. Source: nmax_minus_n1_beta* in results_numbers.json and
    Table tab:stacking-full. The abstract, the RQ2 answer (4.7) and the conclusion say default
    "shows no systematic rise with the number of platforms" in place of "no detectable rise".

D3. Starting stock (03_calibration.tex about lines 48-50 and 59-60). The number of households
    placed in default at the start is the same in every arm of a seed block. They are the same
    households in the baseline, injection and scenario arms. In arms that change access or a
    repayment parameter a few of them differ (7 of 318 on one seed in the access arms, up to 24
    under a different minimum payment), because eligibility and the repayment archetype are drawn
    from the same stream before arrears are placed. Reword the two claims accordingly, briefly; the
    exception for the 56-day threshold stays.

D4. The bureau and BNPL default (02_model.tex, the credit bureau bullet about lines 75-76, and
    wherever the benchmark's information structure is summarised). In the benchmark the bureau does
    not record BNPL balances or instalments, but default is recorded whatever caused it, so a
    household that defaults on BNPL alone is shown in default and gets no further credit from the
    lender or any platform. Say so in one sentence where the bureau is introduced.

D5. Abstract, last sentence. Bureau visibility raises default and also the share short of food and
    rent, so it leaves households worse off on both measures. Only for screening is the welfare
    reading open: default falls, slightly more households are short of food and rent without peer
    influence, and the runs record no amount unpaid. Rewrite so that "neither result shows whether
    households are better off" is no longer claimed of visibility.

D6. What the headline effect is (new, verified; source results/summary/short_group_lending.json,
    notebooks/scripts/check_short_group_lending.py, seeds 10,000-10,019, beta = 0). Of the 120
    households whose surveyed income is below food and rent and who do not start in default, the
    traditional lender's Regulation 23A test never grants a loan to 55 and lends to 65. Without
    BNPL none of the 55 defaults during the run, because they hold no debt: they go short of food
    and rent instead. With BNPL the platforms lend to them and 46 of the 55 default (45.75 on
    average). Among the 65 the lender lends to, 57 default with or without BNPL (56.7 in both
    arms). The 55 therefore account for 0.92 of the 1.08-point effect of Table tab:baseline-arms.
    The group also makes 2,623 of the lender's 2,796 refusals without BNPL and 817 of the 970 with.
    Consequences for the text:
    - Section 4.1 states this in three or four sentences and says plainly that this part of the
      effect follows from the rules: a household with no debt cannot default, and the platforms'
      screen does not compare income with living costs. It also says, in one sentence with a
      pointer to Appendix app:calibration, that the effect depends on counting BNPL arrears as
      default: under the earlier rule, which did not, it was -0.10 +/- 0.06 points.
    - Section 3.5 (the paragraph on the 120) may carry the 55/65 split in one sentence or leave it
      to 4.1; do not state it twice.
    - Section 5 says once, where screening's effect in Q1 is explained, that the offset is close to
      mechanical: screening applies to BNPL requests the test that already keeps these households
      from the lender.
    - The conclusion's "to whom the platforms' light screen lends where the Regulation 23A test
      would not" is correct and stays.
    - The abstract and introduction keep their existing claims about this group but must not
      present the concentration as a discovery; "most of them households whose surveyed income
      does not cover food and rent, which the lender's test refuses" is the kind of wording wanted.
    The examiner report's H3 (the "tenor" reading) is wrong for this group; ignore it.

D7. Default threshold wording. The concept is "more than 90 days past due"; the model's threshold is
    seven ticks, 98 days. Replace "91 or more days behind" with "more than 90 days behind". "98
    days" is used only where the tick threshold itself is the subject.

D8. "Default" is the outcome and nothing else. For parameter settings write "reference values" or
    "reference parameters" (for example "The reference values are q_base = 0.05 and beta = 0").

D9. Terms. "Baseline" is the run without BNPL; "benchmark" is the run with BNPL and no regulatory
    change. Never swap them. Model households are "households" (keep "agents" only in Section 2's
    entity description, Table tab:agent-mapping and the pseudocode). "Platforms" are the model's;
    "providers" are real firms. "Switch" for bureau visibility and screening; "lever" only for the
    cooling-off window and the platform cap. "Sensitivity", not "robustness arm", in prose. Define
    at first use, in a clause and inside the word cap: light screen, stacking, arm, seed block,
    shortfall (income and savings short of committed expenditure plus payments due), shortfall
    path.

D10. Peer influence. That volume and stacking rise with beta is how beta is defined, so do not
    frame it as a result or the flat default response as a surprise ("although", "yet"). State
    that beta acts only on want-driven purchases, so the flat response is what the shortfall
    mechanism implies, and that the sweep confirms it within its power.

D11. Bureau visibility under peer influence. Do not imply peer influence removes the effect. The
    estimates at the two values of beta do not differ detectably (-0.09 +/- 0.08), so say the rise
    is detectable at beta = 0 and not at beta = 0.3, and that the two do not differ detectably.

D12. "Pre-registered" is too strong: the reporting rule was "fixed before the runs". "Flat" for the
    beta response becomes "no detectable slope".

D13. Section 3 contradictions. (a) Pattern 3: at the start Q4 already has the highest
    debt-to-income (1.19), so the peak is present at the start too; what changes over the run is
    that Q1's ratio collapses from 0.81 to 0.08 as its debt is written off. Reword; the verdict
    "we do not count Pattern 3 as evidence" stays. (b) Section 3.3: name the two ceilings (the
    statutory rate ceiling overstates payments; the direction of the error from the Regulation 23A
    payment cap, the product allocation and the horizons is unknown). (c) The provenance note
    "every swept input is also assumed" is false for kappa (derived), the minimum-payer share
    (imported) and k; say that sourced inputs are also swept where the source may not transfer.
    (d) The final-tick 90+ share is 13.84% on the calibration seeds (1,000-1,019) and 14.16% on
    seeds 10,000-10,019; say which seeds at each. (e) "About 0.9 of the 1.08-point effect" is on
    the Table tab:baseline-arms block and "+0.11 +/- 0.07" is pooled over four blocks; say so, so
    the parts are not read as summing.

D14. Two conventions for the CCMR 91-120 day band (03_calibration.tex). The write-off derivation
    lets half the band age out each tick (0.88%); the flow check uses 14/30 of it (0.82%). Disclose
    in one clause at the flow check that the derivation's convention differs and would give 0.0660
    on the 30-day convention. Put any longer note in Appendix C's calibration subsection.

D15. Undisclosed model behaviour, text only: (a) payment friction applies whether or not the
    household has the cash for the full instalment (02_model.tex and Table tab:submodels say
    "affordable"); (b) once behind, a household with the cash to pay still pays nothing with
    probability 0.72 each tick, so a run of bad draws can carry a solvent household to default;
    state this implication once, in Section 3.4 where persistence is introduced or in the Index of
    Limitations in Appendix C; (c) the peer signal and the holding and stacking measures count the
    frozen BNPL balances of defaulted households until write-off (Section 4.3 already says this of
    holding and stacking; add the peer signal in Section 2's peer-influence paragraph in a clause).

D16. References (each agent fixes the in-text side in its own files; only the agent assigned
    main.bib edits entries).
    - February 2027: the Business Day report attributes to the NCR an order that providers begin
      reporting from February 2027; an industry executive is the source for records appearing on
      profiles from then. The abstract's "reportedly due from 2027" becomes consistent with records
      already being submitted in 2026 (for example "is reportedly to be mandatory from 2027").
    - Wang (2026) is cited for CFPB data; cite cfpb2025bnpl for the subprime and deep-subprime
      shares of originations.
    - Ackert et al.: the experiment is between-subject. Do not write that participants "chose the
      two equally often" or "more often finance with BNPL than with a card"; say that participants
      offered interest-free BNPL were at least as willing to finance the purchase as those offered
      a credit card, unless the report quotes a more exact reading.
    - Hayashi and Routh do not call users "liquidity-constrained"; use "financially constrained".
    - The 14-day cooling-off figure is not in FCA PS26/1. If the correct source cannot be verified
      and added by the agent that owns main.bib, describe the window without attributing 14 days to
      PS26/1.
    - The CBM quotation takes its page: \citep[p.~8]{ncr_cbm_2017}.
    - Double brackets from an acronym's first use beside an author-year citation: reword so the
      rendered text does not read "(CFPB) (2025)" or "(FCA)'s", for example by using \acs or by
      spelling the body out once earlier in the sentence.
    - "Windrum, Fagiolo and Moneta" hard-coded beside a year citation becomes \citet.
    - NIDS 13,719: the records dropped are mostly households not interviewed in Wave 5, so say that
      10,841 of the 13,719 household records have reported income, a valid size and a positive
      weight, without implying 2,878 had bad data.
    - Uncited factual claims flagged in report C section (d): add a hedge ("we assume", "in the
      survey's definition") or point to the appendix that documents the construction. Do not
      invent a citation.

D17. Supplementary appendix. The Sobol sentence "within 0.03 of zero (95% bootstrap bound)" becomes
    "upper 95% bound at most 0.021" in line with Section 4.6. Where a contrast sits at exactly two
    standard errors as printed, say "at the two-standard-error threshold". Reconcile 41% (Section 5)
    with 40.5% (Appendix C) by giving the same rounding in both.

## Final message format

1. Files edited, with the word count of each body file against its cap.
2. Findings applied: a count by report and severity, and a list of any HIGH or MED finding you did
   NOT apply, each with a one-line reason.
3. "For the orchestrator": exact old/new text for anything in a generated table, the register, a
   figure, the bibliography or another agent's file.
4. "Left for the author": findings that need a decision, a rerun or new literature.
Keep it factual and short. Do not describe your process.
