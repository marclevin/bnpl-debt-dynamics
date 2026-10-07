"""Lead-editor check (2026-10-07): what share of defaulters hold any credit when they default?

Default (Submodel 7) is seven consecutive distressed ticks, and distress includes an unpaid
committed-expenditure (food and rent) shortfall, so a household with no debt can default.
Reruns the rq0 arms on their own seeds (10,000-10,019) and records, at the tick each
household defaults, whether it owes traditional debt or BNPL, and whether it held traditional
debt at initialisation. Writes results/summary/defaulter_credit.json (Section 2.3 of the thesis).

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_defaulter_credit.py
"""
import json
import warnings
from pathlib import Path
from collections import Counter

from joblib import Parallel, delayed

warnings.simplefilter("ignore")
from simulation.experiments import calibrated  # noqa: E402


def one(params):
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    agents = {a.agent_id: a for a in m.agents}
    c = Counter()
    cls = type(m.bureau)  # slotted class: patch the method on the class, per worker
    orig = cls.record_default

    def hook(self, aid):
        a = agents[aid]
        owes_trad = a.d_trad > 0
        owes_bnpl = a.bnpl_outstanding() > 0
        c["defaults"] += 1
        c["owes_any"] += owes_trad or owes_bnpl
        c["owes_trad"] += owes_trad
        c["started_with_debt"] += a.rec.d_trad > 0
        return orig(self, aid)

    cls.record_default = hook
    try:
        m.run()
    finally:
        cls.record_default = orig
    c["n"] = len(agents)
    return dict(c)


if __name__ == "__main__":
    arms = {
        "no BNPL": dict(bnpl_enabled=False),
        "BNPL beta=0": dict(bnpl_enabled=True, beta=0.0),
        "BNPL beta=1": dict(bnpl_enabled=True, beta=1.0),
    }
    out = {}
    for name, kw in arms.items():
        ps = [calibrated(**kw, label=name).replace(seed=10_000 + i) for i in range(20)]
        rows = Parallel(n_jobs=-2)(delayed(one)(p) for p in ps)
        tot = Counter()
        for r in rows:
            tot.update(r)
        d = tot["defaults"]
        out[name] = {"default_rate": d / tot["n"], "owe_any_credit": tot["owes_any"] / d,
                     "owe_traditional": tot["owes_trad"] / d,
                     "held_traditional_at_start": tot["started_with_debt"] / d}
        print(
            f"{name}: default rate {d / tot['n']:.4f}; of defaulters: owe any credit "
            f"{tot['owes_any'] / d:.3f}, owe traditional {tot['owes_trad'] / d:.3f}, "
            f"held traditional debt at start {tot['started_with_debt'] / d:.3f}"
        )
    dest = Path("results/summary/defaulter_credit.json")
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest}")
