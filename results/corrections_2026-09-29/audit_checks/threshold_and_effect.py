import math, pandas as pd, numpy as np
from pathlib import Path
RAW = Path("results/raw")
rq0, rq2, rq2t, eff = (pd.read_parquet(RAW / f"{n}.parquet") for n in ("rq0","rq2","rq2t","effect"))
L = lambda df, l: df[df.label==l]
s = lambda df: df.set_index("seed").default_rate_final*100
print("== B2 threshold: rise(a1-a0) under g0.3 less rise under g0.0, paired seeds 60000")
for sg in ("0.05","0.1","0.2","0.3","0.4"):
    r3 = s(L(rq2t,f"rq2t_a1.0_s{sg}_g0.3")) - s(L(rq2t,f"rq2t_a0.0_s{sg}_g0.3"))
    r0 = s(L(rq2t,f"rq2t_a1.0_s{sg}_g0.0")) - s(L(rq2t,f"rq2t_a0.0_s{sg}_g0.0"))
    z = r3 - r0
    print(sg, f"rule {r3.mean():+.2f}±{r3.std(ddof=1)/math.sqrt(20):.2f}  control {r0.mean():+.2f}±{r0.std(ddof=1)/math.sqrt(20):.2f}  diff {z.mean():+.2f}±{z.std(ddof=1)/math.sqrt(20):.2f}")
print("\n== B10 identical lambda arms at beta 0?")
a, b = L(eff,"eff_limit0.25_b0.0").set_index("seed"), L(eff,"eff_limit1.0_b0.0").set_index("seed")
num = [c for c in a.columns if a[c].dtype.kind in "fi" and c not in ("lambda","bnpl_limit_months","limit_months")]
diff = [c for c in num if not np.allclose(a[c].values, b.reindex(a.index)[c].values, equal_nan=True)]
print("columns that differ:", diff)
a1, b1 = L(eff,"eff_limit0.25_b1.0").set_index("seed"), L(eff,"eff_limit1.0_b1.0").set_index("seed")
print("b1 default identical:", np.allclose(a1.default_rate_final, b1.reindex(a1.index).default_rate_final))
print("\n== effect at beta0 per setting (paired vs matching off arm)")
offs = {l for l in eff.label.unique() if l.endswith("_off") and l!="eff_want_off_b0.0"}
rows=[]
for l in sorted(eff.label.unique()):
    if not l.endswith("_b0.0") or l=="eff_want_off_b0.0": continue
    stem = l[:-5]
    cand = [stem+"_off", stem.replace("_uncapped","")+"_off", "eff_ref_off"]
    off = next(c for c in cand if c in offs)
    z = s(L(eff,l)) - s(L(eff,off)); z1 = s(L(eff,stem+"_b1.0")) - s(L(eff,off))
    rows.append((stem, off, z.mean(), z.std(ddof=1)/math.sqrt(20), z1.mean(), z1.std(ddof=1)/math.sqrt(20)))
for r in rows: print(f"{r[0]:38s} {r[1]:28s} b0 {r[2]:+.2f}±{r[3]:.2f} {'*' if abs(r[2])>2*r[3] else ' '}  b1 {r[4]:+.2f}±{r[5]:.2f} {'*' if abs(r[4])>2*r[5] else ' '}")
