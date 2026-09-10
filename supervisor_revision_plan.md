# Supervisor Revision Plan — CONTENT

Plan date: 2026-09-08. Revised 2026-09-09. Scope: **content and writing only.**

Restructuring is out of scope and already planned in `SOL_PLAN_REFORMAT.md`, which states its own
dependency: "Before any rewrite begins, Opus's supervisor-driven edits must be complete." **This
plan runs first.** It therefore writes into the **current** file layout using the **current**
labels, so the document compiles and reads correctly throughout. §9 lists what is handed over.

Reference paper: `Davids_duRand_Georg_Koziol_Schasfoort_2021_Covid.pdf` (SSRN 3663320). Its
pseudocode and table-note conventions are used here; its section order is `SOL_PLAN_REFORMAT.md`'s
business.

**Status: NOT STARTED.** On completion, add a dated `APPLIED` banner recording what was done and
anything that went beyond this list, per the precedent in `literature_2_fix.md`, and add both plans
to `OVERVIEW.md` §8 "Companion documents", which currently indexes neither.

---

## 0. Constraints

### 0.1 Supervisor decisions

Approved: the umbrella RQ rewrite; algorithm floats excluded from the word count; cool-off and
facility cap cut from the body; no standalone Discussion and Limitations section.

Cutting the cap overrides a "protect this" entry at `scratchpad/SCOPE_REDUCTION.md` §2.5. Deliberate;
recorded, not reopened. Runs survive in `results/raw/rq3.parquet`.

### 0.2 Word budget — this plan supersedes the earlier projections

Three live budgets disagree: `SCOPE_REDUCTION.md` §5 targets 9,300; `SOL_PLAN_REFORMAT.md` targets
9,500 max and declares SCOPE_REDUCTION stale; this plan projects below. **Precedence: use
`SOL_PLAN_REFORMAT.md`'s 9,500 ceiling.** It also caps the body at five figures — §6 adds ~5 new
ones, so confirm that cap with the restructure agent rather than breaching it silently.

Body prose now (excluding comments, tables, figures, TikZ, algorithm floats): **6,206**.

| Change | § | Δ |
|---|---|---|
| Ch3 construction mechanics → variables appendix | 2 | −370 |
| Ch6 dissolved | 7 | −400 |
| Four levers → three scenarios | 4 | −150 |
| Ch2 Ch1-duplication deleted | 1 | −150 |
| Cell-donor: figure + body paragraph | 3 | +80 |
| Notation prose (if it goes in the body — see §5) | 5 | +80 |
| Framing rewrite, in place | 1 | ~0 |
| **Subtotal** | | **~5,296** |
| Results (existing skeleton budget) | | +3,300 |
| Conclusion — **target total**, absorbing Ch6 §6.6 and the existing `07_conclusion.tex` §7.4 | | 800 |
| Abstract (~300, currently a TODO) — **confirm whether it counts** | | +300? |

Projection **~9,400–9,700**. The headroom is thin and possibly negative if the abstract counts.
Settle that question in step 1.

⚠️ **The word count cannot be checked meaningfully by this plan.** `05_results.tex` and
`07_conclusion.tex` §§7.1–7.3 are pure comment skeletons; the +3,300 and +800 are unwritten. A count
run at the end of this plan lands near 5,300 and proves nothing. Record the subtotal, hand the
budget to whoever writes Results.

### 0.3 Regulatory facts, verified 2026-09-08

**All trade press or an industry statement. None is a primary source.**

| Fact | Source |
|---|---|
| NCR ordered BNPL providers to report payment behaviour to bureaus **from February 2027** | timeslive.co.za/news/business/2026-08-15-bnpl-users-face-new-credit-scrutiny/ ; businessday.co.za/business-times/business/2026-08-15-bnpl-users-face-new-credit-scrutiny/ |
| MoA with SACRRA and the Credit Bureaus Association; a BNPL subcommittee sets the format | same |
| NCR position: BNPL agreements are **not credit agreements at inception**, but **may be incidental credit agreements** where default charges are levied | same |
| NCR earlier **disallowed live processing** of BNPL data pending assessment | finasa.org.za/post/statement-from-fintech-association-of-south-africa-on-buy-now-pay-later-bnpl-reporting-and-regula |
| A major bureau: BNPL data under current scoring models would **cut scores significantly per product**, affecting **~a quarter of credit-active consumers** | same |
| SARB: BNPL contributes to over-indebtedness via multiple simultaneous obligations under fewer affordability checks | businessday.co.za/business-times/2026-06-13-buy-now-pay-later-industry-pushes-for-formal-regulation/ |

URLs recorded per the `literature_2_fix.md` convention so nothing needs re-searching.

**Fallback if step 1 finds no primary source.** The whole reframing turns on the February 2027 date,
and §1 propagates to five files. Do not stall:

- **Safe on two corroborating press reports**, cited as dated press reports of an NCR statement: that
  the NCR has announced a reporting requirement, the MoA parties, and the incidental-credit position.
- **Must be dropped or hedged if only trade press survives**: the specific February 2027 commencement.
  Fall back to "announced, commencement not yet gazetted" — which survives either outcome, so **write
  §1 in that hedged form first** and tighten to the date only once a primary source is in hand. This
  makes step 2 non-blocking.

---

## 1. Framing

Hybrid: over-indebtedness motivates, the mandate is the question.

> South Africa already carries a large over-indebted population, assessed under a residual-income
> statute that has never been able to see BNPL. A new credit channel was added outside the statute,
> and it is now required to report to the bureaus. This thesis asks whether adding the channel was
> benign, and what the reporting requirement is likely to achieve.

**Approved umbrella RQ:**

> In a household population already carrying substantial credit distress, what does the addition of
> a BNPL lending channel outside the affordability and reporting regime do to that distress, and
> what is the mandated extension of credit-bureau reporting to BNPL likely to achieve?

**Scope the claim at the point it is made, not 30 pages later.** The model answers the *affordability
channel* of that question only (see the limitation below). Put one scoping clause directly under the
RQ in `01_introduction.tex` §1.2, in the abstract, and in `05_results.tex` §5.3's framing. Then the
Submodel 10 passage elaborates rather than retracts. The RQ wording itself stands.

Propagate the RQ to: `01_introduction.tex` §1.2, `04_design.tex` §4.1, `05_results.tex` section
titles, `07_conclusion.tex`, and the abstract.

- [ ] `01_introduction.tex` §1.1 — rewrite, ~600 → ~600. Order: (1) SA over-indebtedness + NCA/Reg 23A;
      (2) BNPL outside it, current ¶2 retensed to past/present-perfect; (3) **NEW** the reporting
      requirement, the MoA, the incidental-credit position; (4) deHaan/CFPB unchanged; (5) contribution,
      reframed pre- vs post-mandate.
- [ ] `01_introduction.tex` §1.2 — new umbrella RQ + the scoping clause.
- [ ] `02_literature.tex` **§2.2** (`sec:lit-bnpl`) — delete the ~150 words duplicating Ch1 (deHaan
      10.6m, CFPB 63/32). *Not §2.4 — that is the regulatory subsection.*
- [ ] `02_literature.tex` **§2.4** (`sec:lit-regulatory`) — retense the "invisibility is structural"
      sentence (now *more* true); add the mandate and the SARB over-indebtedness citation.
- [ ] `04_design.tex` Submodel 10 — retense; add the scoring-channel limitation (below); **fix the
      stale switch name**: the body says `\texttt{bureau\_visibility}`, the code is
      `bnpl_bureau_visible` (`config.py:411`).

### The scoring-channel limitation

The model implements bureau visibility as **affordability-input** visibility: BNPL balances enter the
Reg 23A calculation at the lender's gate. The requirement's principal channel appears to be
**credit-score** visibility, and **the model has no credit score.** The near-null result is a statement
about the affordability channel only, and is **silent on** — not evidence against — the scoring
channel. ~150 words at Submodel 10, picked up in the Conclusion's extensions. *Owned here; §7's table
points at it and does not restate it.*

### Carry the incidental-credit position to where it bites

Not just an intro fact. Submodel 14 levies late fees (ZAR 125.74/tick, capped at 188.61) — under the
NCR position, such a product **may already be** an incidental credit agreement. That partly undercuts
Submodel 12's premise ("a light automated screen, deliberately not Regulation 23A") and recasts
Scenario 2 from "new regulation" to "clarification of law that may already apply."

- [ ] Two sentences at Submodel 12/14: state the position, and why the model still treats the screen
      as light (no provider currently applies Reg 23A, whatever the classification).

### Bibliography

- [ ] `ncr_bnpl_reporting_2026` — primary source wanted (NCR releases, SACRRA, Gazette); press
      fallback per §0.3.
- [ ] `finasa_bnpl_2026`, `sarb_fsr_bnpl` — locate the Financial Stability Review itself.
- [ ] Retire nothing. `nortonrose_bnpl_sa`, `transunion_cps_sa_2025` stay, cited as **pre-mandate**.

---

## 2. Variable construction appendix

New hand-written file `thesis/chapters/appendix_d_variables.tex` (letter provisional).

**The NIDS field names already exist** — `scratchpad/DECISIONS.md` §II.4 "Variable map" gives exact
columns (`income_monthly` ← `w5_hhincome`, `expenditure_committed` ← `w5_expf` + `w5_rentexpend`,
`liquid_savings` ← `w5_f_ass`, `d_trad` ← `w5_f_deb`, plus the FinScope `F1`/`G10`–`G14` rules), and
`household_agent.md` repeats it. So this is **relocation and expansion, not research**, and the
diagnostic numbers are already in `03_data.tex` — do not re-derive them, move them.

⚠️ **But the two copies contradict each other**, which is the actual justification for a generator:
`household_agent.md:60` derives `expenditure_discretionary` as `w5_expnf − w5_rentexpend`, while
`DECISIONS.md` §II.4 and `03_data.tex` both say rent is **not** subtracted. **Resolve against
`simulation/population.py`, and say which was wrong.**

Template per variable: **source fields** → **formula** → **missing-data treatment** →
**transformations** → **diagnostics**.

Cover, in order: `income_monthly` (the one the supervisor named); `income_wage_tick` and the
dominant-component rule; `n_earners`; `committed_tick` incl. the imputed-rent exclusion;
`discretionary_tick` incl. **the double-count disclosure**; `liquid_savings`; `d_trad` incl. the
holder-mean counterfactual; `income_quintile` (**also a matching key** → §3); the three-step
amortisation moved from body §3.3; `nca_capacity_monthly`; tick scaling (12/26, stated once,
formally); deflation.

**~1,400 words, free.**

### The generator — specify the split, or it clobbers the prose

`generate_param_register.py` works because `config.py` exposes a declarative `parameter_register()`.
`population.py` exposes no equivalent, and the field names are spread across `p0_backbone.ipynb`.
A script scraping notebook cells is the brittle middle option. **Choose explicitly:**

- **(a) Hand-write the appendix**, citing module and cell per row. Sufficient for a document submitted
  once; the citation is what makes it checkable. **Default.**
- **(b) Add a declarative field map to `population.py` first**, then generate from it — same shape as
  the precedent. Only if drift protection is genuinely wanted.

Either way: **generated table in its own `\input`ed file, prose in a hand file.** A generator that
emits the whole appendix destroys the argument on every rerun.

- [ ] `03_data.tex` §3.1 — bullet list → two sentences + pointer (−120).
- [ ] `03_data.tex` §3.3 — amortisation mechanics move out (−250).

---

## 3. Cell-donor matching

The supervisor asked for the **explanation** to be expanded and a figure added. An appendix alone
satisfies the letter of that but not the place it was raised.

- [ ] **Put `fig:cell-donor` in body §3.2** — figures are free, so it costs nothing — plus ~80 words
      naming **A4** (whole-vector transfer, because stacking is a joint phenomenon), **P1**
      (urban/rural not matched on → attenuation) and **P4** (vintage direction). Strengthen the
      existing "single donor preserves the joint distribution" sentence, currently the only trace of
      A4 in the body.
- [ ] Full catalogue → new file `thesis/chapters/appendix_e_matching.tex`.

Provenance for most of the below is already in `DECISIONS.md` §II.2/§II.5/§II.6 and
`appendix_a_rationale.tex` — cite it, don't re-derive.

**Part A — The procedure, formally.** Cells $c=(q,p)$ over quintile × province, $|C|=45$. For NIDS
record $i$ in cell $c$, draw donor $d$ with probability $w_d/\sum_{d'\in c} w_{d'}$ on `HH_WEIGHT16`;
copy the **entire six-flag vector**. Seed 42. ≥30 donors per cell, `province_fallback_draws = 0` —
currently unreported. *Use the §5 notation; do not invent a second symbol for the cell.*

**Part B — The figure.**

**Part C — Credible when:**
**A1 Cell sufficiency** — conditional on quintile × province the six flags are independent of
everything else that matters. Load-bearing; these are the two strongest inclusion correlates in *both*
instruments. **A2 Common support** — verified, ≥30 donors, zero fallbacks. **A3 Population
comparability.** **A4 Joint-structure preservation** — one donor, six flags, so the imputed joint
distribution is a real household's. **A5 Weight-proportional draw** — reproduces weighted cell
marginals in expectation; `tab:imputation_errors` passes at ≤1.8pp.

**Part D — Problematic when:**
**P1 Within-cell heterogeneity** — urban/rural above all, not matched on; between-cell variation
reproduced, within-cell suppressed, so the eligible population is more homogeneous than the real one
and concentration of exposure is likely *understated*. **P2 Small-cell donor reuse** — draws with
replacement from pools near the 30-donor floor; **report the realised max donor-use count** (new).
**P3 Matching-key measurement error** — banded FinScope income, midpoint quintiles, boundary
misassignment; bounded by the 2.4pp deflation test. **P4 Vintage** — 2019 flags on a 2017 population,
banked share rising, so the 82.8% ceiling is plausibly **too generous**; direction known, magnitude
not. **P5 Group B validation is near-tautological** — marginals reproduced *by construction*. **P6 The
joint distribution is never externally validated.**

**Part E — What would actually break the results.** P4 moves the eligibility ceiling and adoption
levels; P1 moves the *distribution* of exposure, which matters for by-quintile reporting; P2/P3 are
second-order; P5/P6 bound what the validation record claims, not what the model does.

### P5 has a root cause the caption cannot reach

`03_data.tex` §3.5 reports "eighteen diagnostic validation checks … seventeen tests satisfy target
tolerances." Seven are Group B (construction checks) and four are Group E resample fidelity against
the same source, so the headline is ~6 genuinely external checks dressed as 17.

- [ ] Restructure that sentence to report **construction checks and external checks as separate
      counts, with the external count as the headline.** One sentence of body prose; it is the root of
      the standing "validation is internal" problem, and a `tab:validation` note leaves it standing.

### The figure — `fig:cell-donor`

TikZ, matching `fig:visibility`'s style — no new package. Must convey three things prose does badly:

1. **The cell is the unit** — matching happens inside the 5 × 9 grid, never across it.
2. **The draw is weight-proportional** — depict donors at different sizes.
3. **The whole vector moves together** — six flags, one donor.

Plus a small third panel showing the rejected per-flag alternative (six arrows, six donors), which
makes A4 visual. That panel *is* the "intuition" the supervisor asked for.

---

## 4. Interventions → scenarios

`experiments.py:198` already runs `for b in (0.0, 1.0)` crossed with every lever, so present the set
as it actually is — **2 × 3, not a 4-row list**:

| | Benchmark | Bureau visibility | Mandatory affordability screening |
|---|---|---|---|
| **β = 0** | pre-mandate status quo | the reporting requirement | FCA PS26/1 analogue |
| **β > 0** | + peer effects | | |

That makes the plan's own question — *does the answer to bureau visibility and screening depend on
whether adoption is socially transmitted?* — the **axis of the table** rather than a sentence about
it, and makes the anti-circularity requirement structural instead of a reporting habit.

**No re-running, no code change.** All arms exist in `results/raw/rq3.parquet`.

- [ ] Each scenario gets the **same outcome panel as the benchmark** (default, arrears, adoption,
      by-quintile), not a Δ column against it. The `05_results.tex` skeleton still says "Table, all
      four levers ranked by effect" — that is the old shape; rewrite it.
- [ ] Cool-off and cap cut entirely from the body; detail tables → `appendix_c_supplementary.tex`.
- [ ] `04_design.tex` Submodel 15 — "Intervention levers" → "Scenario switches"; three switches;
      delete the four-item enumerate. `tab:submodels` row 15 retitled.
- [ ] `01_introduction.tex` RQ3 — "interventions" → "scenarios". *Owned here, not in §1.*

### The Conclusion's policy argument must be reground

⚠️ The current skeleton argues "the three instruments regulators propose are the three that don't
work, and the one that works is proposed nowhere" — that depends entirely on the cap. But the
obvious replacement ("the harm is that a household holds several at once") **was also demonstrated by
the cap**. Two null scenarios do not establish *why* they are null.

- [ ] Ground the claim on **RQ2 evidence that stays in the body**: emergent 2+ facility shares against
      the CFPB's 32%, the single-platform arm producing exactly zero stacking, and default rising with
      platform count. The two null scenarios are then *corroboration*, not the argument.
- [ ] `07_conclusion.tex` §7.3 — rewrite accordingly. Numbers and prior wording: `STATUS.md` §6.

*Note for the user, not a reopening: cutting cool-off also removes the only lever × peer-effect
interaction (−33% where β > 0), which is the one result giving the newly-added peer scenario a policy
consequence. One appendix table row would preserve it.*

---

## 5. Pseudocode

Free of the word limit. Convention from the reference: a master algorithm dispatching to
sub-algorithms; unnumbered lines; a prose sentence before each; notation carried from the body; two
appendices split by phase.

### Notation table — build it FIRST

Needed by §3 (Part A) as well as here; §3 otherwise invents $c=(q,p)$ for the object this table calls
$\mathcal{G}, g$. Two symbol systems for one construct is the failure mode.

Sets script, cardinality upper, elements lower: $\mathcal{H},H,h$ households (5,000);
$\mathcal{P},P,p$ platforms (4); $\mathcal{G},g$ reference groups (quintile × province);
$t\in[1,T]$, $T=52$; $y_h,y^w_h$ income and wage component; $e^c_h,e^d_h$ committed and discretionary;
$a_h(t)$ savings; $D_h(t),B_{h,p}(t)$ traditional debt and BNPL balance; $s_h(t)$ scheduled service;
$\rho_h$ Reg 23A capacity; $\alpha_h(t)$ arrears band; $\delta_h(t)$ distressed ticks, default at
$k=7$; $q_h(t),\beta,s_g(t)$ propensity, peer weight, adoption share; $\lambda,\kappa$ rolling limit
and purchase ratio; $\mathbb{1}^{\text{bur}},\mathbb{1}^{\text{aff}}$ scenario switches.

**Placement rule:** every symbol here is used only by the pseudocode. Put the table in the body
**only if** `04_design.tex` §4.2's step list and Submodels 9/12/14 are re-expressed in these symbols. Otherwise it
belongs beside the algorithms and costs no body words. Decide once, then apply.

### Algorithms

The algorithms are the **normative statement** of the pipeline; appendices D and E point at them
rather than restating the steps in prose.

*Initialisation* — 1 master; 2 build the survey backbone; 3 **cell-donor match** (also §3 Part A —
write once, reference twice); 4 construct debt service (amortise → horizon → Reg 23A cap); 5 resample
to 5,000. Sources: `p0_backbone.ipynb`, `p2_finscope_match.ipynb`, `population.py`, `p3_resample.ipynb`.
`household_agent.md`'s P1–P5 phase diagram is the existing skeleton — reuse it.

*Main loop* — 6 main simulation; 7 household tick; 8 **Reg 23A gate** with the $\mathbb{1}^{\text{bur}}$
branch; 9 **BNPL origination and routing** with the $\mathbb{1}^{\text{aff}}$ branch; 10 repayment,
arrears, default; 11 peer-influence update. Algorithms 8 and 9 are where the scenarios appear as
branches — a reader should be able to point at the exact line the requirement changes. Say so.

⚠️ **Resolve the tick-order discrepancy before writing Algorithm 7.** `DECISIONS.md` D0 gives a
**six**-step order with its ABM anchors; `THESIS_GUIDE.md` §6 gives **seven**, inserting peer
observation at position 6. Verify against `model.py` and cite D0 as design intent; otherwise the
pseudocode silently picks one.

### LaTeX

```latex
\usepackage{caption}      % REQUIRED — main.tex does not currently load it
\usepackage{algorithm}    % load AFTER float; both patch the float mechanism
\usepackage{algpseudocode}
\algrenewcommand\alglinenumber[1]{}
\captionsetup[algorithm]{labelsep=space}
```

- [ ] Verify each algorithm against `model.py`, `agents.py`, `bnpl.py`, `lender.py`,
      `affordability.py`. Pseudocode contradicting the implementation is worse than none.

---

## 6. Self-contained tables and figures

Caption = **short title only**; a `\footnotesize` note between title and body doing four things: what
is shown, symbol definitions, sample/replicate count, scenario.

```latex
\newcommand{\tabnote}[1]{\par\vspace{2pt}{\footnotesize #1}\par\vspace{4pt}}
```

⚠️ **`\tabnote` cannot go between caption and body in a `longtable`** — `tab:design-concepts`,
`tab:submodels` and `tab:further-caveats` put `\caption{...}\\` inside the table body, where an
intervening `\par` is a syntax error. For those three use
`\multicolumn{n}{p{\linewidth}}{\footnotesize …}\\` before `\midrule`.

⚠️ **`tab:param-register` must be edited through `generate_param_register.py`**, not in
`appendix_b_register.tex` — that file is machine-generated and says so on line 1. The caption is a
string literal in the script (~lines 85–89). A hand edit is reverted on the next run.

| Float | Needs |
|---|---|
| `tab:imputation_errors` | "Synthetic" (weighted) vs "Agents" (unweighted 5,000); vintages; ≤3pp tolerance |
| `tab:credit-terms` | APRs are statutory **maxima not realised rates** + the upward bias; define "horizon"; the two NIDS $n$ values |
| `tab:validation` | provenance of every tolerance; define groups A–E; Group B is a construction check |
| `tab:agent-mapping` | 12/26 applies to flow rows only; point to the variables appendix |
| `tab:patterns` | which is the calibration target vs plausibility checks |
| `tab:ccmr` | "account basis" vs the model's household unit |
| `tab:design-concepts` | ODD design concepts; "Source" = literature grounding; "None" = choice with no anchor. **Also receives the 6.5 exclusions — see §7** |
| `tab:submodels` | point at the **existing** sourced/derived/assumed definition in `tab:param-register`'s generated caption; do not write a second copy |
| `fig:inclusion-fidelity`, `tab:param-register` | restructure to title + note |
| `fig:pop-fidelity` | resample seed; unweighted agents vs weighted source |
| `fig:visibility` | title "Information structure of the model"; note carries legend + Submodel refs |

**New Results/Scenario floats (~6 tables, 5 figures)** — these belong to whoever writes Results, but
the rule is set here: every note states replicate count and seed scheme; the noise floor (0.33pp;
below ~0.67pp is noise); which scenario each column is; that access rates are shares of the **banked
subpopulation** (82.8% ceiling), not all households; and that **β = 0 is the control arm**.

**Sign-off test:** read each float with the body covered. Any unexplained symbol, subsample, scenario
or transformation means the note is incomplete.

---

## 7. Dissolve Discussion and Limitations

Verified against the reference: it has no limitations section *and* no limitations discussion in the
conclusion. Caveats sit **inline at the point of the assumption**; the conclusion is findings →
policy insights → extensions. `SOL_PLAN_REFORMAT.md` says the same. So Ch6's 947 words are
**redistributed, not deleted** — content work, no file moves.

**Single-source rule, or this multiplies caveats instead of relocating them:** each caveat is argued
in **exactly one** named place and pointed at everywhere else. Before writing any of the rows below,
check `tab:further-caveats`, `tab:submodels` and `appendix_a_rationale.tex` — several flags already
exist there (row 4 "structural assumption with no anchor located", row 6 the minimum fraction, row 8
"no local calibration data"). **Budget for the argument, not for restating the flag.**

| Ch6 § | Destination | Words |
|---|---|---|
| 6.1 Calibrated not validated | `04_design.tex` §4.5, where the two parameters are fitted | ~200 |
| 6.2 Validation targets uneven | `04_design.tex` §4.1, after the patterns table | ~180 |
| 6.3 Behavioural parameters imported | `04_design.tex` Submodels 6, 8, 11 | ~150 |
| 6.4 One rule has no anchor | `04_design.tex` Submodel 4 | ~90 |
| 6.5 exclusions | **`tab:design-concepts`** — the ODD protocol puts exclusions there, and three are already rows. A free float, so ~120 of the 550 costs nothing | ~0 |
| 6.5 interpretation | `05_results.tex` §5.2, beside the negative result it explains | ~130 |
| 6.6 How results should be read | `07_conclusion.tex`, penultimate paragraph — **keep intact** | ~130 |

`tab:further-caveats` also gains the demoted headings as rows, each pointing at where it is now
argued — one table indexing every limitation in the thesis.

- [ ] **Fix the caveat count once, here, at the end** — not in §6. Today: `06_discussion.tex` says
      "seven", `appendix_c_supplementary.tex:45` says "nine", the table has nine rows. After this
      section the chapter sentence is gone and the table is **nine + the demoted rows**. Also retarget
      `appendix_c_supplementary.tex:46` ("The five that do are argued in Section~\ref{ch:discussion}"),
      which will otherwise point at an emptied file.
- [ ] Empty `06_discussion.tex` to a pointer comment. **Do not delete it** — `main.tex` still
      `\input`s it; deletion is the restructure agent's job.

### ⚠️ The `sec:lim-*` labels break here, not at the restructure

All six are declared in `06_discussion.tex`. **Five** are referenced from outside it (not six):

| Label | Referenced from |
|---|---|
| `sec:lim-transfer` | `02_literature.tex:100`, `07_conclusion.tex:67` |
| `sec:lim-validation` | `04_design.tex:19,30`, `05_results.tex:85` |
| `sec:lim-structural` | `05_results.tex:76`, `07_conclusion.tex:58` |
| `sec:lim-reading` | `07_conclusion.tex:47` |
| `sec:lim-calibration` | `appendix_b_specification.tex:18` |
| `sec:lim-amount` | *nowhere — safe to drop* |

- [ ] Re-declare each surviving label at its new home so inbound references keep resolving.
- [ ] **`sec:lim-structural` is the hard one:** 6.5 splits across two files, but
      `07_conclusion.tex:58` wants the **exclusions** half and `05_results.tex:76` wants the
      **interpretation** half. One label cannot serve both. Split it — e.g. `sec:exclusions` and
      `sec:no-cascade` — and retarget each reference explicitly. A blind rename produces references
      that compile and point at the wrong place.

---

## 8. Execution order

Organised by **file pass**, not by item — `04_design.tex` and `07_conclusion.tex` are otherwise each
opened four or five times.

**Step 1 — Prerequisites (independent, run together).**
- [ ] Primary sources for the mandate / SARB / FINASA. Non-blocking: write §1 hedged per §0.3.
- [ ] Resolve the `expenditure_discretionary` contradiction against `population.py` (§2).
- [ ] Compute max donor-use count and per-cell pool sizes (§3, P2).
- [ ] Confirm whether the abstract counts toward the limit (§0.2).
- [ ] Resolve the six-vs-seven tick-order discrepancy against `model.py` (§5).
- [ ] Preamble: add `caption`, `algorithm` (after `float`), `algpseudocode`, `\tabnote`. **Stub
      `appendix_d_variables.tex` and `appendix_e_matching.tex` and `\input` them now**, so one
      smoke-test compile covers the final preamble and float structure.
- [ ] Write the **notation table** (§5) — §3 depends on it.

**Step 2 — `01_introduction.tex` + `02_literature.tex`, one pass.** §1's framing, the RQ and its
scoping clause, the §2.2 deletion, the §2.4 retensing, RQ3's "scenarios" rewording, the bib entries.

**Step 3 — `03_data.tex`, one pass.** §2's two compressions, §3's body paragraph and figure, the
17/18 validation-headline fix.

**Step 4 — Appendices D and E.** Variables (hand-written per §2a) and matching + TikZ figure.

**Step 5 — `04_design.tex`, one pass.** Submodel 10 retense + scoring limitation + switch-name fix;
Submodels 12/14 incidental-credit sentences; Submodel 15 → scenario switches; `tab:submodels` row 15;
**all four §7 caveat destinations**; the notation table if it goes in the body.

**Step 6 — Pseudocode appendices**, then verify each algorithm against its module.

**Step 7 — `05_results.tex` + `07_conclusion.tex`, one pass.** §4's scenario table shape and skeleton
rewrite; 6.5's interpretation; 6.6; the reground policy argument; the extensions paragraph.

**Step 8 — Floats and labels.** §6's audit on the ~13 existing floats; the `longtable` and generator
routing; §7's `sec:lim-*` re-declaration and split; the caveat count.

**Step 9 — Recompile.** `grep main.log` for undefined references — it must come back empty. Record
the prose subtotal (expect ~5,300) and hand the 9,500 ceiling to whoever writes Results. Do **not**
report a word-count pass; the two largest chapters are unwritten.

Commit at the end of each step — edits have silently reverted in this repo before.

---

## 9. Handed to `SOL_PLAN_REFORMAT.md`

That document already specifies the target structure, the four moves, and a file-level
implementation map. Not restated here. What this plan leaves it:

- `06_discussion.tex` emptied but still `\input`ed — delete the file and the input together.
- Two new appendix files at the end of `main.tex`; letters provisional, reorder freely.
- All content written against **current** labels; the rename map is theirs.
- The `sec:lim-*` labels are **already resolved by §7**, including the `sec:lim-structural` split.
  Do not re-derive them — but do re-run `grep -rn "sec:lim-" thesis/chapters/*.tex` to confirm.
- Its own five-figure body cap conflicts with the ~5 new Results figures (§0.2). Settle it.
