"""Word counts for the thesis under the project's convention (scratchpad/wc_prose.py),
plus float captions and notes counted separately. Run from the repository root."""
import re, sys
from pathlib import Path
sys.path.insert(0, 'scratchpad')
from wc_prose import prose_words

T = Path('thesis'); CH = T / 'chapters'

def expand(tex):
    # inline \input{chapters/generated/...} so body tables are attributed to their chapter
    return re.sub(r"\\input\{(chapters/generated/[^}]+)\}",
                  lambda m: (T / (m.group(1) + '.tex')).read_text(), tex)

def balanced(tex, start):
    depth = 0
    for i in range(start, len(tex)):
        if tex[i] == '{': depth += 1
        elif tex[i] == '}':
            depth -= 1
            if depth == 0: return tex[start+1:i]
    return ''

def float_text(tex):
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    out = []
    for cmd in ('caption', 'tabnote'):
        for m in re.finditer(r"\\" + cmd + r"\{", tex):
            out.append(balanced(tex, m.end() - 1))
    # longtable notes: \multicolumn{n}{p{..}}{\footnotesize ...}
    for m in re.finditer(r"\\multicolumn\{\d+\}\{p\{[^}]*\}\}\{", tex):
        out.append(balanced(tex, m.end() - 1))
    return ' '.join(out)

def floats_words(tex):
    return prose_words(re.sub(r"\\(begin|end)\{[^}]*\}", " ", float_text(tex)))

main = (T / 'main.tex').read_text()
body_files = re.findall(r"\\input\{([^}]+)\}", re.sub(r"(?<!\\)%.*", "", main.split(r"\appendix")[0]))
app_files = re.findall(r"\\input\{([^}]+)\}", re.sub(r"(?<!\\)%.*", "", main.split(r"\appendix")[1]))
abstract = main[main.index(r'\section*{Abstract}'):main.index(r'\acresetall')]

tot_p = tot_f = 0
for f in body_files:
    tex = expand((T / f'{f}.tex').read_text())
    p, fl = prose_words(tex), floats_words(tex)
    tot_p += p; tot_f += fl
    print(f"{Path(f).name:32s} prose {p:6d}   captions+notes {fl:5d}")
print(f"{'BODY':32s} prose {tot_p:6d}   captions+notes {tot_f:5d}")
a = prose_words(abstract)
print(f"abstract {a};  body prose + abstract {tot_p + a}")
ap = af = 0
for f in app_files:
    tex = (T / f'{f}.tex').read_text()
    tex = re.sub(r"\\input\{(chapters/[^}]+)\}", lambda m: expand((T / (m.group(1) + '.tex')).read_text()), tex)
    tex = expand(tex)
    ap += prose_words(tex); af += floats_words(tex)
print(f"appendices: prose {ap}, captions+notes {af} (excluded from the cap)")
