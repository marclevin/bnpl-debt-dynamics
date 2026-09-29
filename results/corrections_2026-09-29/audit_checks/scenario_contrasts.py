import math, pandas as pd, numpy as np
rq3 = pd.read_parquet("results/raw/rq3.parquet")
L = lambda l: rq3[rq3.label==l]
def unp(a,b,col,scale=1.0):
    x,y=a[col],b[col]; return f"{(x.mean()-y.mean())*scale:+.3f} ± {math.sqrt(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))*scale:.3f}"
def relvol(a,b):
    x,y=a.bnpl_volume_cumulative,b.bnpl_volume_cumulative
    r=x.mean()/y.mean(); se=r*math.sqrt(x.var(ddof=1)/len(x)/x.mean()**2+y.var(ddof=1)/len(y)/y.mean()**2)
    return f"{(r-1)*100:+.1f} ± {se*100:.1f}%"
for b in ("0.0","1.0"):
    ben=L(f"rq3_kcool0_b{b}")
    for k in ("bureau","afford","both"):
        a=L(f"rq3_{k}_b{b}")
        print(b,k,"default",unp(a,ben,"default_rate_final",100),"vol",relvol(a,ben),"refused",unp(a,ben,"trad_refused_gate"),"(",round(a.trad_refused_gate.mean()),round(ben.trad_refused_gate.mean()),")",
              "lend",unp(a,ben,"trad_granted_value",1e-6),"hold",unp(a,ben,"bnpl_adoption_final",100), "arrears90", unp(a,ben,"active_90_plus_final",100) if "active_90_plus_final" in a else "")
