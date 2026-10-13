"""Lead-editor check (2026-10-07): what share of defaulters hold any credit when they default?

Default (Submodel 7) is seven consecutive distressed ticks, and distress includes an unpaid
committed-expenditure (food and rent) shortfall, so a household with no debt can default.
Reruns the rq0 arms on their own seeds (10,000-10,019) and records, at the tick each
household defaults, whether it owes traditional debt or BNPL, and whether it held traditional
debt at initialisation. Also records the unemployment path and (2026-10-13, examiner hole H2)
the income path by quintile with BNPL off. Writes results/summary/defaulter_credit.json
(Sections 3.4 and 3.5 of the thesis).

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_defaulter_credit.py
"""
import json
import warnings
from pathlib import Path
from collections import Counter

from joblib import Parallel, delayed

warnings.simplefilter("ignore")
from simulation.config import MONTHLY_TO_TICK  # noqa: E402
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
        # Why the defaulting streak was distressed (added 2026-10-12): every tick had a
        # food or rent shortfall, none did (unmet debt service only), or a mix.
        k = a.distress_streak
        c["streak_all_committed"] += a.committed_in_streak == k
        c["streak_no_committed"] += a.committed_in_streak == 0
        c["income_below_committed"] += a.income_tick < a.committed_tick
        # Added 2026-10-12 (second review): an earner out of work when the household defaults.
        c["unemployed_at_default"] += a.is_wage_household and a.n_unemployed > 0
        return orig(self, aid)

    cls.record_default = hook
    try:
        m.run()
    finally:
        cls.record_default = orig
    c["n"] = len(agents)
    c["n_income_below_committed"] = sum(a.income_tick < a.committed_tick for a in agents.values())
    return dict(c)


def unemployment_path(params):
    """Share of the earners employed at the start who are out of work at ticks 12, 26 and 52.

    Without labour flows every earner starts employed and the share out of work rises
    towards its steady state (46% at the earlier fitted rate). With labour flows (the
    baseline from 2026-10-12) employment is constant in expectation."""
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    flows = params.labour_flows
    pool = [a for a in m.agents if a.rec.n_earners > 0 and (flows or a.is_wage_household)]
    earners = sum(a.rec.n_earners for a in pool)
    out = {}
    for t in range(1, 53):
        m.step()
        if t in (12, 26, 52):
            out[f"earners_out_of_work_t{t}"] = sum(a.n_unemployed for a in pool) / earners
            # Employment relative to the start: starting earners still in work plus hires.
            out[f"employment_index_t{t}"] = sum(
                a.rec.n_earners - a.n_unemployed + a.n_hired for a in m.agents) / sum(
                a.rec.n_earners for a in m.agents)
    out["households_with_earner_out_t52"] = sum(a.n_unemployed > 0 for a in pool) / len(m.agents)
    return out


QUINTILES = ("Q1", "Q2", "Q3", "Q4", "Q5")


def realised_income(a) -> float:
    """Income received in the tick just stepped: Submodel 1 with labour flows, as in
    HouseholdAgent.step (surveyed income, less the wage share of members out of work, plus
    the hire wage of jobseekers in work, floored at zero)."""
    income = a.income_tick
    n = a.rec.n_earners
    if a.n_unemployed and n:
        income -= a.rec.income_wage_tick * (a.n_unemployed / n)
    income += a.n_hired * a.rec.hire_wage_tick
    return max(income, 0.0)


def income_path(params):
    """Examiner hole H2 (added 2026-10-13): labour flows hold employment constant, not income.

    Records aggregate household income at ticks 1, 12, 26 and 52 relative to surveyed income
    at the start, overall and by income quintile; employment by quintile relative to the
    start; and, per quintile, the expected wage lost when an earner separates (the household
    wage component over its earners, averaged over earners) against the wage a hired
    jobseeker brings (the quintile median take-home pay)."""
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    agents = list(m.agents)
    groups = {"all": agents, **{q: [a for a in agents if a.rec.income_quintile == q]
                                for q in QUINTILES}}
    start = {k: sum(a.income_tick for a in g) for k, g in groups.items()}
    emp0 = {k: sum(a.rec.n_earners for a in g) for k, g in groups.items()}
    out = {}
    for k, g in groups.items():
        earners = sum(a.rec.n_earners for a in g)
        out[f"earners_{k}"] = earners
        out[f"jobseekers_{k}"] = sum(a.rec.n_jobseekers for a in g)
        # Monthly 2017 Rands: tick amounts over MONTHLY_TO_TICK.
        out[f"lost_wage_per_earner_monthly_{k}"] = (
            sum(a.rec.income_wage_tick for a in g if a.rec.n_earners) / earners / MONTHLY_TO_TICK
            if earners else 0.0)
        js = [a for a in g if a.rec.n_jobseekers]
        out[f"hire_wage_monthly_{k}"] = (
            sum(a.rec.hire_wage_tick * a.rec.n_jobseekers for a in js)
            / sum(a.rec.n_jobseekers for a in js) / MONTHLY_TO_TICK if js else 0.0)
    for t in range(1, 53):
        m.step()
        if t in (1, 12, 26, 52):
            for k, g in groups.items():
                out[f"income_rel_t{t}_{k}"] = sum(realised_income(a) for a in g) / start[k] - 1.0
                out[f"employment_rel_t{t}_{k}"] = sum(
                    a.rec.n_earners - a.n_unemployed + a.n_hired for a in g) / emp0[k] - 1.0
    return out


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
                     "held_traditional_at_start": tot["started_with_debt"] / d,
                     "streak_all_committed": tot["streak_all_committed"] / d,
                     "streak_no_committed": tot["streak_no_committed"] / d,
                     "income_below_committed": tot["income_below_committed"] / d,
                     "unemployed_at_default": tot["unemployed_at_default"] / d,
                     "income_below_committed_share_of_agents": tot["n_income_below_committed"] / tot["n"],
                     "income_below_committed_who_default": tot["income_below_committed"]
                     / tot["n_income_below_committed"]}
        print(
            f"{name}: default rate {d / tot['n']:.4f}; of defaulters: owe any credit "
            f"{tot['owes_any'] / d:.3f}, owe traditional {tot['owes_trad'] / d:.3f}, "
            f"held traditional debt at start {tot['started_with_debt'] / d:.3f}"
        )
    for name, kw in (("unemployment path, baseline with labour flows", {}),
                     ("unemployment path, earlier fitted shock 0.016, no flows",
                      dict(shock_prob=0.016, labour_flows=False)),
                     ("unemployment path, QLFS upper bound 0.0117, no flows",
                      dict(shock_prob=0.0117, labour_flows=False))):
        ps = [calibrated(bnpl_enabled=False, label=name).replace(seed=10_000 + i, **kw)
              for i in range(20)]
        rows = Parallel(n_jobs=-2)(delayed(unemployment_path)(p) for p in ps)
        out[name] = {k: sum(r[k] for r in rows) / len(rows) for k in rows[0]}
        print(name, {k: round(v, 3) for k, v in out[name].items()})
    name = "income path, baseline with labour flows"
    ps = [calibrated(bnpl_enabled=False, label=name).replace(seed=10_000 + i) for i in range(20)]
    rows = Parallel(n_jobs=-2)(delayed(income_path)(p) for p in ps)
    out[name] = {k: sum(r[k] for r in rows) / len(rows) for k in rows[0]}
    print(name, {k: round(v, 3) for k, v in out[name].items() if k.startswith("income_rel_t52")})
    dest = Path("results/summary/defaulter_credit.json")
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest}")
