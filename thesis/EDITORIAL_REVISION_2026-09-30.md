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
| Body prose, Sections 1–6 | 9,653 | 9,742 |
| Abstract | 257 | 256 |
| **Body prose + abstract** | **9,910** | **9,998** |
| Captions and table/figure notes in the body (separate) | 3,550 | 3,550 |
| Appendix prose (excluded) | 5,776 | 5,757 |
| Appendix captions and notes (excluded) | 1,478 | 1,478 |

The caption and note count is unchanged, so no prose was moved into floats.

## Resolved in the follow-up pass

- Submodel 12: the unclear clause "0.10 is conservative on either reading" is removed; the
  factual statement that both equivalised shares overstate the limit is kept.
- Pattern 1: Section 3.5 now says that the pre-specified condition conflates two effects,
  because the fall in traditional interest comes from the smaller book that the lender-choice
  rule produces.
- Branch check: the revision sits directly on the latest `main` (`3b79e3c`); `corrected-model`
  points at the same commit and `six-section-restructure` is an older ancestor.

## Open issues for the author

1. **Front matter.** The declaration wording and title-page layout remain provisional
   (TODO comments in `main.tex`).
2. **Submodel table layout.** Longtable can break only between rows, and several rows are tall,
   so pages 16–18 are partly empty. A landscape page or a wider rule column would fix it.
