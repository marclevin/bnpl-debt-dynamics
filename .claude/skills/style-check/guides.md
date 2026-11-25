# The supervisor's three style guides, as they apply to this thesis

The PDFs sit at the repository root (`cochrane.pdf`, `bellemare.pdf`, `Session 5.pdf`; not in
git; `pdftotext -layout` reads them). They were applied in the style pass of 2026-11-16
(`30281f2`, PR #106). Read a guide itself only when a rule here is unclear.

- **Cochrane**, *Writing Tips for Ph.D. Students*: organisation and sentence-level writing.
- **Bellemare**, *How to Write Applied Papers in Economics*: what each part of the paper must contain.
- **Langenmayr**, *Academic Writing 1, Session 5*: the introduction (Keith Head's formula,
  Claudia Sahm's structure).

## Organisation

1. **One central contribution, stated up front** (Cochrane). Newspaper order, not joke order:
   the finding first, the background after. No travelogue of the search.
2. **Nothing before the main result that the reader does not need to understand it** (Cochrane).
3. **First say what you do, then explain it, then compare it with alternatives** (Cochrane), at
   the level of the section, the paragraph and the sentence.
4. **Say it once.** A finding appears once in the abstract, once in the introduction and once in
   the body. "In other words" is a sign of trouble. Each point has one home; other places cite it.
5. **No previews, no recalls** (Cochrane). "As we will see" and "recall that" mean the order is wrong.
6. **Appendices hold** the general versions, the rejected alternatives and the extra sensitivity
   runs. The body summarises them in a sentence.

## Introduction (Langenmayr, Head, Bellemare)

The order in this thesis: Background (hook and gap), Research Questions, Approach and Findings,
Related Literature by theme, Contribution (three), a short roadmap.

1. The hook is about the world, never "a large literature has studied".
2. The question is understandable from the hook alone. The contributions make sense only against
   the antecedents.
3. Most of the introduction is about this thesis, not about the literature.
4. Literature is told as a story by theme, not as "X found Y" lists. Each theme here ends with
   "The model takes from this evidence ...". Cite the closest studies and those that deserve
   priority; leave out the rest.
5. Never trash prior work. Say what this thesis adds. Neutral tone, facts only.
6. Up to three contributions, the finding first and the tools after.
7. A roadmap specific to this thesis, at most a sentence per section.
8. Do not overpromise (Bellemare).
9. As little jargon as possible: a parent should follow most of it.

## Abstract

1. Concrete: say what was found, not what was looked for (Cochrane).
2. No literature in the abstract (Cochrane).
3. Readable by a non-economist (Bellemare).
4. UCT limit 300 words. Current order: context, question, the model's rules, the result, who it
   falls on, the nulls, the two switches, the validation misses, how to read the results.

## Results

1. Start with the main result. No warm-up exercises (Cochrane).
2. Every important number carries a standard error (Cochrane). Two to three significant digits.
3. Give the economic size, not only whether it is detectable (Cochrane).
4. Say what drives each number (Cochrane, on identification): here, which households and which
   rule.
5. Admit what the design cannot show, and claim nothing beyond it (Bellemare). Say which
   mechanisms cannot be tested and why.
6. Check heterogeneity before reporting "no effect" (Bellemare).
7. Present tense for results (Cochrane, Bellemare).

## Conclusion

1. Short. Do not restate all the findings (Cochrane).
2. The summary differs from the abstract (Bellemare).
3. Limitations, then implications, without claims the results do not support.
4. No speculation, no list of plans. Strike "I leave x for future research" (Cochrane). This
   thesis says what better data "would show".

## Tables and figures

1. A self-contained caption or note, so a skimming reader needs no hunt through the text
   (Cochrane). Define every symbol in the note.
2. No number in a table that the text does not discuss (Cochrane).
3. Sensible units, the same number of decimals in a column, plain-English row names (Bellemare).
4. Label axes; no line styles that vanish in print (Cochrane).

## Sentences (Cochrane)

1. Active voice. Search for "is" and "are" to find the passives.
2. Subject, verb, object. Few clauses, nothing left hanging.
3. Short plain words: "use" not "utilize", "several" not "diverse".
4. Concrete, not abstract.
5. Delete everything before "that": "It should be noted that", "It is easy to show that".
6. Clothe the naked "this".
7. No adjectives for your own work. No double adjectives.
8. State the model; do not "assume" it. "Consumers have power utility." Keep "assumption" for
   claims about the real world.
9. "In which" for a model, "where" for a place.
10. Spell out authors' names.
11. Remind the reader of a Greek letter's name when it comes back.
12. No footnotes for asides: in the text or out.
13. One direction is enough: no "(down)".
14. Keep the tense consistent within a paragraph.
15. Do not overuse italics.

## Where this thesis departs from the guides on purpose

Do not "fix" these.

| Guide says | The thesis does | Why |
|---|---|---|
| "I" for a sole author (Cochrane) | "we" and "our" | Decided 2026-11-16. Do not reopen |
| No roadmap needed (Cochrane) | A short roadmap | Bellemare and Langenmayr ask for one |
| Abstract of 100 to 150 words (Cochrane) | Up to 300 | UCT's limit; the abstract names the validation misses |
| Literature after the contribution (Cochrane), antecedents before value-added (Head) | Findings, then literature by theme, then contribution | Langenmayr's "My alternative" order |
| A separate limitations section (Bellemare) | Each limit stated once, where the claim is made, and the conclusion's second paragraph | The voice: a caveat sits at its claim |
| Future research section (Bellemare) | What better data "would show", in the conclusion | Cochrane |
| Stars or p-values are usual | Estimate, one standard error, "detectable" beyond two | Section 3.1 convention |
| Sources named in the text | The source of every number sits in a `%` comment under its paragraph | Keeps prose short; the comments are checked by `check_results_tables.py` |
