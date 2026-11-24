#!/usr/bin/env python3
"""Mechanical style, voice and terminology checks for the thesis.

Reads the rules in rules.tsv (beside this file) and reports every hit as file:line. It also
finds near-repeated sentences, reports sentence length, and checks the word caps. It needs
only the standard library.

    python3 .claude/skills/style-check/check_style.py                 # whole thesis, new hits only
    python3 .claude/skills/style-check/check_style.py --since HEAD    # only lines changed since a git ref
    python3 .claude/skills/style-check/check_style.py FILE ...        # named .tex files
    python3 .claude/skills/style-check/check_style.py --all           # include hits accepted in baseline.tsv
    python3 .claude/skills/style-check/check_style.py --text draft.tex  # a draft passage not yet in the thesis
    python3 .claude/skills/style-check/check_style.py --update-baseline # accept every current hit

A hit listed in baseline.tsv was reviewed and accepted (a legitimate other meaning, a quoted
source category, a table label). The default run hides those, so a clean run means "nothing new".
Exit status is 1 when an ERROR-level hit is new or a word cap is broken.

The script finds patterns. It cannot judge voice, framing or whether a point already has a home:
SKILL.md lists the reading checks that follow it.
"""

from __future__ import annotations

import argparse
import bisect
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
THESIS = ROOT / "thesis"
CHAPTERS = THESIS / "chapters"
RULES = HERE / "rules.tsv"
BASELINE = HERE / "baseline.tsv"

BODY_CAP = 10_000  # chapters 1 to 6 under notebooks/scripts/wc_prose.py
ABSTRACT_CAP = 300  # UCT limit
LONG_SENTENCE = 45  # words
REPEAT_MIN_WORDS = 12
REPEAT_JACCARD = 0.6

# Environments whose contents are not prose.
SKIP_ENVS = ("tikzpicture", "algorithmic", "equation", "equation*", "align", "align*", "verbatim")

SCOPES = {
    "all": r".*",
    "abstract": r"^main\.tex$",
    "front": r"^(main\.tex|01_|06_)",  # abstract, introduction, conclusion
    "body": r"^(main\.tex|0[1-6]_)",  # abstract and Sections 1 to 6
    "sections": r"^0[1-6]_",  # Sections 1 to 6 without the abstract
    "prose": r"^(main\.tex|0[1-6]_|appendix_)",  # everything hand-written
    "notpolicy": r"^(main\.tex|0[12346]_|appendix_)",  # "scenario" is reserved for Section 5
    "nomodelapp": r"^(main\.tex|0[1-6]_|appendix_[abc])",  # not Appendices D to G, which say "agent"
    "generated": r"^generated/",
}


def default_files() -> list[Path]:
    return [THESIS / "main.tex", *sorted(CHAPTERS.glob("*.tex")), *sorted((CHAPTERS / "generated").glob("*.tex"))]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(CHAPTERS))
    except ValueError:
        return path.name


def clean_line(line: str) -> str:
    """Blank what is not prose but keep the line's length roughly meaningful for reading."""
    line = re.sub(r"(?<!\\)%.*", "", line)
    line = re.sub(r"\\(label|ref|eqref|autoref|input|include|includegraphics|url|href|bibliography\w*|usepackage|acro|newcommand|renewcommand)\*?(\[[^\]]*\])*\{[^}]*\}", " ", line)
    line = re.sub(r"\\cite\w*\*?(\[[^\]]*\])*\{[^}]*\}", " CITE ", line)
    line = re.sub(r"\\texttt\{[^}]*\}", " CODE ", line)
    line = re.sub(r"\\acs?p?\{([^}]*)\}", r"\1", line)
    line = re.sub(r"\$[^$]*\$", " MATH ", line)
    return line


class Doc:
    """One .tex file as cleaned, flattened prose with a map back to line numbers."""

    def __init__(self, path: Path, raw: str | None = None, plain: bool = False):
        self.path = path
        self.name = rel(path)
        raw = path.read_text(encoding="utf-8") if raw is None else raw
        lines = raw.split("\n")
        if self.name == "main.tex" and not plain:
            lines = self._abstract_only(lines)
        out, skip = [], None
        for line in lines:
            c = line if plain else clean_line(line)
            if skip:
                if re.search(r"\\end\{" + re.escape(skip) + r"\}", c):
                    skip = None
                out.append("")
                continue
            m = re.search(r"\\begin\{(" + "|".join(re.escape(e) for e in SKIP_ENVS) + r")\}", c)
            if m and not re.search(r"\\end\{" + re.escape(m.group(1)) + r"\}", c):
                skip = m.group(1)
                out.append("")
                continue
            out.append(c)
        self.lines = out
        self.starts, pos = [], 0
        for c in out:
            self.starts.append(pos)
            pos += len(c) + 1
        # Newlines become spaces (same length), so a phrase split over two lines still matches.
        # An empty line stays visible as a run of two or more spaces: a paragraph break.
        self.flat = " ".join(out)

    @staticmethod
    def _abstract_only(lines: list[str]) -> list[str]:
        keep, inside = [], False
        for line in lines:
            if re.match(r"\\section\*\{Abstract\}", line):
                inside = True
                keep.append("")
                continue
            if inside and re.match(r"\\section\*\{", line):
                inside = False
            keep.append(line if inside else "")
        return keep

    def line_of(self, offset: int) -> int:
        return bisect.bisect_right(self.starts, offset)

    def context(self, start: int, end: int, pad: int = 45) -> str:
        s = self.flat[max(0, start - pad) : min(len(self.flat), end + pad)]
        return re.sub(r"\s+", " ", s).strip()

    def sentences(self) -> list[tuple[int, str]]:
        """(line, sentence) for running prose: LaTeX commands dropped, table rows skipped."""
        out = []
        for m in re.finditer(r"[^.?!]+(?:[.?!](?!\s)[^.?!]*)*[.?!]", self.flat):
            s = m.group(0)
            if "&" in s or "\\\\" in s:
                continue
            words = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)
            words = re.sub(r"[{}~\\]", " ", words)
            words = re.sub(r"\s+", " ", words).strip()
            lead = len(s) - len(s.lstrip())
            out.append((self.line_of(m.start() + lead), words))
        return out


def load_rules() -> list[dict]:
    rules = []
    for n, row in enumerate(RULES.read_text(encoding="utf-8").split("\n"), 1):
        if not row.strip() or row.startswith("#"):
            continue
        parts = row.split("\t")
        if len(parts) != 6:
            sys.exit(f"rules.tsv line {n}: expected 6 tab-separated fields, found {len(parts)}")
        rid, sev, scope, flags, pattern, msg = (p.strip() for p in parts)
        if scope not in SCOPES:
            sys.exit(f"rules.tsv line {n}: unknown scope {scope!r}")
        if sev not in ("ERROR", "WARN"):
            sys.exit(f"rules.tsv line {n}: severity must be ERROR or WARN")
        try:
            rx = re.compile(pattern, 0 if "c" in flags else re.I)
        except re.error as e:
            sys.exit(f"rules.tsv line {n}: bad regex ({e})")
        rules.append({"id": rid, "sev": sev, "scope": re.compile(SCOPES[scope]), "rx": rx, "msg": msg})
    return rules


def changed_lines(ref: str, files: list[Path]) -> dict[str, set[int]]:
    """Line numbers added or changed in the working tree since a git ref, per file."""
    out: dict[str, set[int]] = {}
    diff = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "-U0", ref, "--", *[str(f) for f in files]],
        capture_output=True, text=True, check=True,
    ).stdout
    cur = None
    for line in diff.split("\n"):
        if line.startswith("+++ b/"):
            cur = rel(ROOT / line[6:])
            out.setdefault(cur, set())
        elif line.startswith("@@") and cur is not None:
            m = re.search(r"\+(\d+)(?:,(\d+))?", line)
            start, count = int(m.group(1)), int(m.group(2) or 1)
            out[cur].update(range(start, start + count))
    untracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--others", "--exclude-standard", "--", *[str(f) for f in files]],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    for u in untracked:
        p = ROOT / u
        out[rel(p)] = set(range(1, len(p.read_text(encoding="utf-8").split("\n")) + 1))
    return out


def key(rid: str, name: str, ctx: str) -> str:
    return f"{rid}\t{name}\t{ctx}"


def shingles(s: str) -> set[tuple[str, ...]]:
    w = re.findall(r"[a-z0-9.]+", s.lower())
    return {tuple(w[i : i + 3]) for i in range(len(w) - 2)}


def find_repeats(docs: list[Doc]) -> list[tuple[str, int, str, int, str, float]]:
    items = []
    for d in docs:
        if d.name.startswith("generated/"):
            continue
        for line, s in d.sentences():
            if len(s.split()) >= REPEAT_MIN_WORDS:
                items.append((d.name, line, s, shingles(s)))
    hits = []
    for i in range(len(items)):
        a = items[i]
        for j in range(i + 1, len(items)):
            b = items[j]
            if not a[3] or not b[3]:
                continue
            inter = len(a[3] & b[3])
            if inter and inter / len(a[3] | b[3]) >= REPEAT_JACCARD:
                hits.append((a[0], a[1], b[0], b[1], a[2], inter / len(a[3] | b[3])))
    return hits


def word_caps() -> list[str]:
    problems = []
    spec = importlib.util.spec_from_file_location("wc_prose", ROOT / "notebooks" / "scripts" / "wc_prose.py")
    wc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wc)
    total = sum(wc.prose_words(f.read_text(encoding="utf-8")) for f in wc.body_files())
    main = (THESIS / "main.tex").read_text(encoding="utf-8")
    m = re.search(r"\\section\*\{Abstract\}(.*?)\\section\*\{", main, flags=re.S)
    abstract = wc.prose_words(m.group(1)) if m else 0
    print(f"words: body {total:,} of {BODY_CAP:,} ({BODY_CAP - total:,} spare); abstract {abstract} of {ABSTRACT_CAP}")
    if total > BODY_CAP:
        problems.append(f"body is {total - BODY_CAP} words over the {BODY_CAP:,} cap")
    if abstract > ABSTRACT_CAP:
        problems.append(f"abstract is {abstract - ABSTRACT_CAP} words over the {ABSTRACT_CAP} limit")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--since", metavar="REF", help="report only hits on lines changed since this git ref")
    ap.add_argument("--all", action="store_true", help="include hits accepted in baseline.tsv")
    ap.add_argument("--update-baseline", action="store_true", help="write every current hit to baseline.tsv")
    ap.add_argument("--text", type=Path, help="check a plain-text or LaTeX draft passage as if it were body prose")
    ap.add_argument("--no-repeats", action="store_true", help="skip the repeated-sentence search")
    ap.add_argument("--stats", action="store_true", help="print sentence-length figures per file")
    args = ap.parse_args()

    rules = load_rules()
    if args.text:
        d = Doc(args.text, raw=args.text.read_text(encoding="utf-8"))
        d.name = "01_draft:" + args.text.name  # scoped as body prose
        docs = [d]
    else:
        docs = [Doc(f) for f in (args.files or default_files())]
    only = changed_lines(args.since, [d.path for d in docs]) if args.since else None
    accepted = set()
    if BASELINE.exists() and not args.all and not args.update_baseline and not args.text:
        accepted = {r for r in BASELINE.read_text(encoding="utf-8").split("\n") if r and not r.startswith("#")}

    found: list[tuple[str, str, int, str, str, str]] = []  # sev, file, line, rule, msg, ctx
    for d in docs:
        for r in rules:
            if not r["scope"].search(d.name):
                continue
            for m in r["rx"].finditer(d.flat):
                s = m.start(1) if m.groups() and m.group(1) is not None else m.start()
                e = m.end(1) if m.groups() and m.group(1) is not None else m.end()
                found.append((r["sev"], d.name, d.line_of(s), r["id"], r["msg"], d.context(s, e)))
        if not d.name.startswith("generated/"):
            for line, s in d.sentences():
                n = len(s.split())
                if n > LONG_SENTENCE:
                    found.append(("WARN", d.name, line, "long-sentence", f"{n} words; the voice runs at about 20", s[:90]))

    repeats = [] if args.no_repeats else find_repeats(docs)
    for a_name, a_line, b_name, b_line, s, j in repeats:
        found.append(("WARN", a_name, a_line, "repeat", f"near-repeat of {b_name}:{b_line} (overlap {j:.2f}); one home per point", s[:90]))

    if args.update_baseline:
        rows = sorted({key(rid, name, ctx) for _, name, _, rid, _, ctx in found})
        BASELINE.write_text(
            "# Hits reviewed and accepted. One per line: rule, file, context. Rebuilt by --update-baseline.\n"
            + "\n".join(rows) + "\n", encoding="utf-8")
        print(f"baseline.tsv: {len(rows)} accepted hits")
        return 0

    shown = []
    for sev, name, line, rid, msg, ctx in found:
        if key(rid, name, ctx) in accepted:
            continue
        if only is not None and line not in only.get(name, set()):
            continue
        shown.append((sev, name, line, rid, msg, ctx))
    shown.sort(key=lambda h: (h[0] != "ERROR", h[1], h[2]))
    for sev, name, line, rid, msg, ctx in shown:
        print(f"{sev:5s} {name}:{line}  [{rid}] {msg}\n        ... {ctx} ...")

    if args.stats:
        for d in docs:
            lens = [len(s.split()) for _, s in d.sentences() if len(s.split()) >= 4]
            if lens and not d.name.startswith("generated/"):
                lens.sort()
                print(f"stats {d.name}: {len(lens)} sentences, mean {sum(lens) / len(lens):.1f} words, median {lens[len(lens) // 2]}, longest {lens[-1]}")

    if args.text:
        n = sum(len(s.split()) for _, s in docs[0].sentences())
        print(f"words in the passage: about {n} (the body has a cap; run notebooks/scripts/wc_prose.py for the exact count)")
    problems = [] if args.text else word_caps()
    for p in problems:
        print(f"ERROR {p}")
    errors = sum(1 for h in shown if h[0] == "ERROR") + len(problems)
    warns = sum(1 for h in shown if h[0] == "WARN")
    hidden = len(found) - len(shown)
    print(f"{errors} errors, {warns} warnings to review" + (f" ({hidden} accepted or outside the changed lines)" if hidden else ""))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
