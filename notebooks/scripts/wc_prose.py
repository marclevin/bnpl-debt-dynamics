"""Count body prose words per chapter file, under the department's counting rule.

Counted: running prose, headings, inline maths (one token each), footnotes.
Not counted: comments, tables, figures, TikZ, algorithm floats, display maths, citations,
labels and cross-reference commands.

--floats reports, separately, the words in the captions and notes of the body's tables and
figures: every \\caption and \\tabnote argument, and the note row (the \\multicolumn before
\\toprule) of a longtable, in the body files and the generated tables they \\input. Cell contents
are not counted. The same rule applies inside them: inline maths one token, citations and
cross-reference commands none.

    python3 notebooks/scripts/wc_prose.py            # every body file in main.tex order
    python3 notebooks/scripts/wc_prose.py FILE ...   # named files
    python3 notebooks/scripts/wc_prose.py --floats   # captions and notes of the body's floats
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[2] / "thesis" / "chapters"
FLOATS = "table|table\\*|figure|figure\\*|longtable|tabular|tabularx|tikzpicture|algorithm|algorithmic|equation|equation\\*|align|align\\*"


def prose_words(tex: str) -> int:
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    tex = re.sub(rf"\\begin\{{({FLOATS})\}}.*?\\end\{{\1\}}", " ", tex, flags=re.S)
    tex = re.sub(r"\\\[.*?\\\]", " ", tex, flags=re.S)
    tex = re.sub(r"\\(cite\w*|ref|eqref|autoref|label|input|include|vspace|hspace|needspace)\*?(\[[^\]]*\])*\{[^}]*\}", " ", tex)
    tex = re.sub(r"\$[^$]*\$", " M ", tex)
    tex = re.sub(r"\\(begin|end)\{[^}]*\}", " ", tex)
    tex = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", tex)
    tex = re.sub(r"[{}~\\]", " ", tex)
    return sum(1 for w in tex.split() if re.search(r"[A-Za-z0-9]", w))


def body_files() -> list[Path]:
    main = (CHAPTERS.parent / "main.tex").read_text(encoding="utf-8")
    main = re.sub(r"(?<!\\)%.*", "", main)
    body = main.split(r"\appendix")[0]
    return [CHAPTERS.parent / f"{m}.tex" for m in re.findall(r"\\input\{([^}]+)\}", body)]


def braced(tex: str, start: int) -> tuple[str, int]:
    """The balanced {...} argument whose opening brace is at or after start, and the index after it."""
    i = tex.index("{", start)
    depth = 0
    for j in range(i, len(tex)):
        if tex[j] == "{" and tex[j - 1] != "\\":
            depth += 1
        elif tex[j] == "}" and tex[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return tex[i + 1 : j], j + 1
    raise ValueError("unbalanced braces")


def float_texts(tex: str) -> list[str]:
    """Captions and notes: \\caption{..}, \\tabnote{..}, and a longtable's \\multicolumn note row."""
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    out = []
    for m in re.finditer(r"\\(caption|tabnote)(\[[^\]]*\])?(?=\{)", tex):
        out.append(braced(tex, m.end())[0])
    for m in re.finditer(r"\\begin\{longtable\}", tex):
        head = tex[m.end() : tex.index(r"\toprule", m.end())]
        for mc in re.finditer(r"\\multicolumn", head):
            _, k = braced(head, mc.end())  # column count
            _, k = braced(head, k)  # column spec
            out.append(braced(head, k)[0])
    return out


def float_words(files: list[Path]) -> None:
    total = 0
    for f in files:
        tex = f.read_text(encoding="utf-8")
        own = sum(prose_words(t) for t in float_texts(tex))
        live = re.sub(r"(?<!\\)%.*", "", tex)
        gen = [CHAPTERS.parent / f"{g}.tex" for g in re.findall(r"\\input\{([^}]+)\}", live)]
        inp = sum(prose_words(t) for g in gen for t in float_texts(g.read_text(encoding="utf-8")))
        total += own + inp
        print(f"{own + inp:6d}  {f.name} (captions and notes; {inp} of them in {len(gen)} generated tables)")
    print(f"{total:6d}  TOTAL captions and notes")


if __name__ == "__main__":
    if sys.argv[1:] == ["--floats"]:
        float_words(body_files())
        sys.exit()
    files = [Path(a) for a in sys.argv[1:]] or body_files()
    total = 0
    for f in files:
        n = prose_words(f.read_text(encoding="utf-8"))
        total += n
        print(f"{n:6d}  {f.name}")
    print(f"{total:6d}  TOTAL")
