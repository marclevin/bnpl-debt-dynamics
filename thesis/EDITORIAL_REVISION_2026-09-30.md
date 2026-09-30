# Editorial revision of 2026-09-30

Starting version: commit `3b79e3c` on `claude/charming-albattani-bb0gqn`. No simulation code,
empirical input, generated table or result was changed. Every number in the prose was checked
against `thesis/chapters/generated/` or `results/summary/results_numbers.json`.

## Word count

Counted with `scratchpad/wc_prose.py` (the project's existing convention) and reported by
`scratchpad/wc_report.py`. Counted: running prose and headings, with inline maths as one token.
Not counted: comments, tables, figures, TikZ, algorithms, display maths, citations, labels and
cross-references, the cover page, the declaration, the acronym list and the appendices.

| | Before | After |
|---|---:|---:|
| Body prose, Sections 1–6 | 9,653 | 9,741 |
| Abstract | 257 | 256 |
| **Body prose + abstract** | **9,910** | **9,997** |
| Captions and table/figure notes in the body (separate) | 3,550 | 3,550 |
| Appendix prose (excluded) | 5,776 | 5,757 |
| Appendix captions and notes (excluded) | 1,478 | 1,478 |

The caption and note count is unchanged, so no prose was moved into floats.

## Open issues for the author

1. **Submodel 12, "0.10 is conservative on either reading".** Expressing Woolard's £1,000 as a
   share of *equivalised* income (39%) overstates it relative to *household* income, so the
   Woolard-implied per-platform limit on household income is below 0.10. On that reading 0.10
   is at or above the benchmark, which is conservative only if "conservative" means "does not
   understate BNPL capacity". Confirm the intended sense or reword.
2. **Pattern 1 falsification condition.** The pre-specified condition treats a fall in
   traditional interest as falsifying the lender-choice hierarchy, but Section 4.1 shows the fall
   arises *from* that hierarchy (BNPL first, so a smaller traditional book). The thesis reports
   the result under the condition as specified; consider saying explicitly in Section 3.5 that
   the condition, in hindsight, conflates the two.
3. **"About 100 more refusals" with both switches (Section 5).** The figure is recorded in
   `results/corrections_2026-09-29/CORRECTIONS.md` but not in `tab_switches` or
   `results_numbers.json`. Add it to the generated outputs at the next table build.
4. **Front matter.** The declaration wording and title-page layout remain provisional
   (TODO comments in `main.tex`).
5. **Submodel table layout.** Longtable can break only between rows, and several rows are tall,
   so pages 16–18 are partly empty. A landscape page or a wider rule column would fix it.
