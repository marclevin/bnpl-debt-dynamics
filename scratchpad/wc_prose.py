"""Count body prose words per chapter file, under the department's counting rule.

Counted: running prose, headings, inline maths (one token each), footnotes.
Not counted: comments, tables, figures, TikZ, algorithm floats, display maths, citations,
labels and cross-reference commands.

    ./env/python.exe scratchpad/wc_prose.py            # every body file in main.tex order
    ./env/python.exe scratchpad/wc_prose.py FILE ...   # named files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHAPTERS = Path(__file__).resolve().parents[1] / "thesis" / "chapters"
FLOATS = "table|table\\*|figure|figure\\*|longtable|tabular|tabularx|tikzpicture|algorithm|algorithmic|equation|equation\\*|align|align\\*"


def prose_words(tex: str) -> int:
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    tex = re.sub(rf"\\begin\{{({FLOATS})\}}.*?\\end\{{\1\}}", " ", tex, flags=re.S)
    tex = re.sub(r"\\\[.*?\\\]", " ", tex, flags=re.S)
    tex = re.sub(r"\\(cite\w*|ref|eqref|autoref|label|input|include|vspace|hspace)\*?(\[[^\]]*\])*\{[^}]*\}", " ", tex)
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


if __name__ == "__main__":
    files = [Path(a) for a in sys.argv[1:]] or body_files()
    total = 0
    for f in files:
        n = prose_words(f.read_text(encoding="utf-8"))
        total += n
        print(f"{n:6d}  {f.name}")
    print(f"{total:6d}  TOTAL")
