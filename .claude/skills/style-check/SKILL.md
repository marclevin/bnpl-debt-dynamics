---
name: style-check
description: Check or write thesis prose so that it matches Marc's voice, the supervisor's three style guides and the thesis's fixed terminology. Use before finishing any edit to thesis/**/*.tex (body, abstract, captions, table notes, appendices), when reviewing a draft passage from any assistant, when a new term, group, arm or measure is introduced, and whenever asked for a style, voice, consistency, tautology or AI-writing check.
---

# Style check

This skill checks new thesis text against the existing voice and the term ledger. It has two
parts: a script that finds patterns, and a reading pass for what a pattern cannot find (a new
thing with three names, a point made twice, a claim with the wrong scope). Run both.

Files beside this one:

| File | Holds |
|---|---|
| `check_style.py` | The mechanical checks, word caps, repeated sentences, sentence length |
| `rules.tsv` | The patterns, one per line, with the message shown for each |
| `baseline.tsv` | Hits already reviewed and accepted in the current text |
| `terms.md` | The term ledger and the fixed sentences. **Read it before writing anything** |
| `guides.md` | The rules of the three style guides, and where the thesis departs from them on purpose |

## Procedure

### 1. Before writing

1. Read `terms.md`. Read the paragraph before and after the place you will edit.
2. Find the point's home. Grep the thesis for the claim and its number. If it is already made
   somewhere, edit it there or cite that section; do not make it a second time.
3. Check the word budget: `python3 notebooks/scripts/wc_prose.py`. The body (Sections 1 to 6)
   has a cap of 10,000 words; tables, figures, captions, display maths, citations, the abstract,
   front matter, bibliography and appendices are not counted. The abstract has its own limit
   of 300. Plan additions so that at least 50 words stay spare.

### 2. After writing: the script

```
python3 .claude/skills/style-check/check_style.py --since HEAD     # lines changed since the last commit
python3 .claude/skills/style-check/check_style.py --text draft.tex  # a passage not yet in the thesis
python3 .claude/skills/style-check/check_style.py                   # the whole thesis, new hits only
```

- **ERROR**: the thesis has none of these. Fix every one.
- **WARN**: read the hit. Fix it, or decide it is legitimate (a cited source's own word, a table
  label, a second established meaning). Never accept a hit only to make the run clean.
- `repeat`: two sentences share most of their words. Keep one; make the other a pointer.
- `long-sentence`: over 45 words. Split it unless it is a list.
- Headings are checked like prose: no question as a heading, no "robustness".
- When every remaining hit is legitimate, run `--update-baseline` and commit `baseline.tsv` with
  the text.

### 3. After writing: the reading pass

Read the new text aloud against the paragraph before it. Then answer each question.

**Terms**
1. Does every model object, group, measure, arm and rule carry its `terms.md` name, including
   in captions, table rows, figure labels and `%` comments?
2. Is anything new named? List every noun phrase the new text uses for it and grep the thesis
   for each. There must be exactly one, defined in one sentence at first use, added to
   `terms.md`, given drift patterns in `rules.tsv`, and used identically at every later mention
   (text, table rows, captions, `tab:experiments`, the register).
3. Does any word now mean two things in the same section ("short", "cap", "screen", "reference",
   "threshold", "run")? If so, use the full name each time.
4. Is each symbol named at its first use in the section?

**Framing**
5. Does each result use the fixed sentence for its kind (`terms.md`, "Fixed sentences")?
6. Is every claim scoped the way the thesis scopes claims: "in the model", "within two years",
   "depends on", "follows from the rules"? No modal hedges, no causal claims about real
   households, no recommendations.
7. Does each limitation sit once, at the claim it limits?
8. If a headline number or its wording changed, is it identical in the abstract, the
   introduction, the body and the conclusion, and in the `%` comments?

**Voice**
9. One claim per sentence, subject first, a plain verb, about 20 words. Things as subjects: the
   model, the lender, the platforms, the arm, the effect.
10. Present tense for the model and its results. Past tense for what the author did when
    building it and for facts about the world. "Would" for what better data would show.
11. Active. "We" only for the author's own choices ("we fit", "we report", "we found no").
12. Model rules stated as facts: "A household defaults when ...", never "we assume that".
13. Order: what is done, then why, then the alternative, then the pointer to a sensitivity run
    or appendix.
14. Connectives inside the sentence: "so", "because", "therefore", "but", "while". No opener
    words. No signposting sentence that only announces the next one.
15. Paragraphs open on their claim and stop when it is made. No closing sentence that restates
    the paragraph.

**Tautology and repetition**
16. Does any sentence say what the sentence before it said? Does any clause restate its own
    main clause ("lends to them, extending credit to these households")?
17. Does any sentence only define a word by itself, or state what the table beside it already
    shows without adding the reading of it?
18. Is the same finding stated twice in one section? Is a definition restated instead of cited?
    (A number may recur as a reference point: "of the 1.08 points".)
19. Could the paragraph lose its first or last sentence and say the same? Then cut it.

**Numbers**
20. Every estimate has its standard error and a table or section reference, and a `%` comment
    beneath the paragraph naming the file and key it came from. Counts of households ("55",
    "46 of the 55") carry no standard error.
21. Typed numbers match `results/summary/`:
    `PYTHONPATH=. .venv/bin/python notebooks/scripts/check_results_tables.py`.
    Generated tables are never edited by hand: change `build_results_tables.py` and rebuild.
22. Two decimals for model outputs; two or three significant digits for standard errors; the
    abstract rounds and drops the standard error.

**Balance**
23. Has the edit added more than the point needs? Compare the word count before and after.
    A new result earns about two to four sentences in the body.
24. Has it cut something a later section relies on? Grep for references to what was removed.

### 4. Report

List what was found as `file:line`, the rule or question it failed, and the fix made. Say
plainly if anything was left and why.

## The voice in one page

Sections 1 to 6 at `81e6ee9` are the reference. Mean sentence length is 18 to 24 words by
section; the median is about 20.

**It sounds like this.**

- "A household defaults when its arrears age reaches seven ticks."
- "Enabling BNPL raises it by `$1.08 \pm 0.11$` points at `$\beta=0$` and `$1.12 \pm 0.11$` at
  `$\beta=0.3$`."
- "Without BNPL none of the 55 defaults; they go short of food and rent instead."
- "We found no South African provider that publishes a limit, so λ is an assumption."
- "Two in 20 is about what chance gives."
- "Whether screening leaves households better off is open."

**It never does this.**

| Habit | Instead |
|---|---|
| Em dashes; a dash between words | A full stop, a comma, "and" |
| "However,", "Moreover,", "Notably,", "Importantly," | Join with "but" or "so", or start with the subject |
| "It is important to note that", "It should be noted" | Say the thing |
| "This shows", "This means" | "This rule shows", "Seven ticks means" |
| "X, not Y" and "not only X but Y" as a flourish | State X |
| A sentence that announces the next, or sums up the last | Cut it |
| Three-part lists for rhythm; paired adjectives | The one item that matters |
| "significant", "robust", "striking", "crucial", "key", "novel" | The number, and "detectable" |
| "may", "might", "could", "suggests", "appears" about a model result | State it, scoped "in the model" |
| "several", "many", "substantially", "roughly" | The tabulated number; "about" is the only approximator |
| "we assume" for a model rule | State the rule; "is an assumption" when no source gives the value |
| "as discussed above", "as we will see", "recall that" | "(Section~\ref{...})" after the claim |
| Rhetorical questions, footnotes, italics for emphasis, contractions | None |
| A closing moral ("This underlines the importance of ...") | End on the last fact |
| Synonyms for variety | The same word every time |

**Structure it keeps.**

- A caveat is stated once, at the claim. The conclusion's second paragraph collects the main ones.
- A null result is reported with its estimate, its standard error and what the design could
  have detected.
- The experiments show which assumptions an effect depends on. They do not identify mechanisms.
- The thesis recommends nothing. It says what the model gives and what is open.
- Captions are noun phrases with no full stop. Table notes are "Label: definition." fragments
  that carry seeds, units and pairing, so the table reads alone.
- Provenance of every number lives in a `%` comment under its paragraph.

## Decisions that are closed

Do not reopen these, and do not flag them as defects.

- "We" and "our" on a sole-authored thesis.
- The research questions keep their wording (Marc, 2026-11-11). "Affordability screening",
  "peer adoption" and "population default" survive inside them for that reason.
- The main estimate is the redrawn population's `$1.13 \pm 0.06$` points (Marc, 2026-11-25, on the
  supervisor's advice); the pooled fixed-population `$1.03 \pm 0.06$` is reported beside it.
- No stars, no p-values; "detectable" means beyond two standard errors.
- The departures from the guides listed at the end of `guides.md`.

## Keeping the skill current

- A term the thesis settles on goes into `terms.md` and `rules.tsv` in the same commit as the text.
- A rule that fires on approved text is wrong: narrow its pattern; do not bury it in the baseline.
- After any edit to the thesis, rebuild the baseline only once the remaining hits have been read.
- If Marc corrects a wording, record the correction here or in `terms.md`, with the date.
