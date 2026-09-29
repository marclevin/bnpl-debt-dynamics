import math, pandas as pd, numpy as np
from pathlib import Path
RAW = Path("results/raw")
rq0, rq2, eff, rob = (pd.read_parquet(RAW / f"{n}.parquet") for n in ("rq0","rq2","effect","robustness"))
L = lambda df, l: df[df.label==l]
def par(a,b,col,scale=1.0):
    x=a.set_index("seed")[col]; y=b.set_index("seed")[col]; z=(x-y.reindex(x.index))*scale
    return f"{z.mean():+.3f} ± {z.std(ddof=1)/math.sqrt(len(z)):.3f}"
print("eff ref b0 vs off refused", par(L(eff,"eff_ref_b0.0"),L(eff,"eff_ref_off"),"trad_refused_gate"))
off,b0,b1=(L(rq0,l) for l in ("baseline_no_bnpl","bnpl_on_beta0","bnpl_on_beta1"))
for nm,a in (("b0",b0),("b1",b1)):
    print(nm,"trad_debt_final Rm", par(a,off,"trad_debt_final",1e-6), "| mean levels", a.trad_debt_final.mean()/1e6, off.trad_debt_final.mean()/1e6,
          "| interest rel", (a.trad_interest_total.mean()/off.trad_interest_total.mean()-1)*100)
    x=a.set_index("seed").trad_interest_total; y=off.set_index("seed").trad_interest_total
    z=(x/y-1)*100; print("   interest % paired", z.mean(), z.std(ddof=1)/math.sqrt(20))
print("\nsteps between adjacent access levels (paired)")
steps=[]
for b in sorted(rq2.beta.unique()):
    acc = sorted(rq2[rq2.beta==b].bnpl_access_rate.unique())
    out=[]
    for lo,hi in zip(acc[:-1],acc[1:]):
        x=rq2[(rq2.beta==b)&(rq2.bnpl_access_rate==hi)].set_index("seed").default_rate_final
        y=rq2[(rq2.beta==b)&(rq2.bnpl_access_rate==lo)].set_index("seed").default_rate_final
        z=(x-y.reindex(x.index))*100; m,s=z.mean(),z.std(ddof=1)/math.sqrt(len(z))
        out.append(f"{m:+.2f}±{s:.2f}{'*' if abs(m)>2*s else ''}"); steps.append((b,m,s))
    print(b, out)
m=np.array([s[1] for s in steps]); se=np.array([s[2] for s in steps])
print("all steps: min %.2f max %.2f median %.2f; se range %.2f-%.2f; n detectable %d of %d"%(m.min(),m.max(),np.median(m),se.min(),se.max(),(abs(m)>2*se).sum(),len(m)))
mb=np.array([s[1] for s in steps if s[0]>0]); print("beta>0 steps: min %.2f max %.2f median %.2f"%(mb.min(),mb.max(),np.median(mb)))
