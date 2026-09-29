import math, pandas as pd, numpy as np
from pathlib import Path
RAW = Path("results/raw")
rq0, rq1, rq2, rq2t, rq3, rob, eff = (pd.read_parquet(RAW / f"{n}.parquet") for n in ("rq0","rq1","rq2","rq2t","rq3","robustness","effect"))

def unp(a, b, col, scale=1.0):
    x, y = a[col], b[col]
    return (x.mean()-y.mean())*scale, math.sqrt(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))*scale
def par(a, b, col, scale=1.0):
    x = a.set_index("seed")[col]; y = b.set_index("seed")[col]
    assert sorted(x.index)==sorted(y.index)
    z = (x-y.reindex(x.index))*scale
    return z.mean(), z.std(ddof=1)/math.sqrt(len(z))
L = lambda df, l: df[df.label==l]
print("cols with refus/lend:", [c for c in rq3.columns if "refus" in c or "trad" in c or "lend" in c or "grant" in c])
print("seeds per label rq3:"); print(rq3.groupby("label").seed.agg(["min","max","count"]))

f = lambda t: f"{t[0]:+.3f} ± {t[1]:.3f}"
print("\n== A1: both less screening (unpaired)")
for b in ("0.0","1.0"):
    a, s = L(rq3,f"rq3_both_b{b}"), L(rq3,f"rq3_afford_b{b}")
    print(b, "refused", f(unp(a,s,"trad_refused_gate")), "| lending Rm", f(unp(a,s,"trad_granted_value",1e-6)),
          "| holding pp", f(unp(a,s,"bnpl_adoption_final",100)), "| default pp", f(unp(a,s,"default_rate_final",100)))
    print("   means refused", a.trad_refused_gate.mean(), s.trad_refused_gate.mean())
    ben = L(rq3,f"rq3_kcool0_b{b}")
    print("   both vs benchmark default", f(unp(a,ben,"default_rate_final",100)))

print("\n== A2/B11: refusals and lending, BNPL on vs off")
print("eff want_off b0 vs ref_off: refused", f(par(L(eff,"eff_want_off_b0.0"),L(eff,"eff_ref_off"),"trad_refused_gate")),
      "lending", f(par(L(eff,"eff_want_off_b0.0"),L(eff,"eff_ref_off"),"trad_granted_value",1e-6)))
print("eff labels:", sorted(eff.label.unique()))
print("rq0 b0 vs off: refused", f(par(L(rq0,"bnpl_on_beta0"),L(rq0,"baseline_no_bnpl"),"trad_refused_gate")),
      "lending", f(par(L(rq0,"bnpl_on_beta0"),L(rq0,"baseline_no_bnpl"),"trad_granted_value",1e-6)))
print("rq0 b1 vs off: refused", f(par(L(rq0,"bnpl_on_beta1"),L(rq0,"baseline_no_bnpl"),"trad_refused_gate")),
      "lending", f(par(L(rq0,"bnpl_on_beta1"),L(rq0,"baseline_no_bnpl"),"trad_granted_value",1e-6)))

print("\n== B5: paired beta1 - beta0 by block (default pp)")
for k in ("kcool0","bureau","afford","both"):
    print(k, f(par(L(rq3,f"rq3_{k}_b1.0"),L(rq3,f"rq3_{k}_b0.0"),"default_rate_final",100)))

print("\n== A4: lever-by-beta DiD (paired within block, then unpaired across blocks where needed)")
def did(lever, ben_block_label):
    x1 = L(rq3,f"rq3_{lever}_b1.0").set_index("seed").default_rate_final
    x0 = L(rq3,f"rq3_{lever}_b0.0").set_index("seed").default_rate_final
    d_l = (x1-x0)*100
    b1 = L(rq3,"rq3_kcool0_b1.0").set_index("seed").default_rate_final
    b0 = L(rq3,"rq3_kcool0_b0.0").set_index("seed").default_rate_final
    d_b = (b1-b0)*100
    if sorted(d_l.index)==sorted(d_b.index):
        z = d_l - d_b.reindex(d_l.index); return z.mean(), z.std(ddof=1)/math.sqrt(len(z)), "paired"
    return d_l.mean()-d_b.mean(), math.sqrt(d_l.var(ddof=1)/len(d_l)+d_b.var(ddof=1)/len(d_b)), "unpaired"
for lv in ("cap1","cap2","cap3","kcool1","kcool2","kcool3","kcool4","bureau","afford","both"):
    m,s,k = did(lv,None); print(lv, f"{m:+.2f} ± {s:.2f}", k, "t=%.1f"%(m/s))
print("holding at b1:", {k: round(L(rq3,f"rq3_{k}_b1.0").bnpl_adoption_final.mean()*100,1) for k in ("kcool0","afford","cap1","cap2","kcool4")})
