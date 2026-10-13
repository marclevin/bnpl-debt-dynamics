"""Examiner hole H1 (2026-10-13): what does the lender's test see under bureau visibility?

With `bnpl_bureau_visible=True` the traditional lender adds `Platform.obligations()` to the
obligations in the Regulation 23A test. That is one instalment per live agreement PLUS the
loan's arrears, and arrears include late fees. Arrears stay on the loan until paid, and the
lender scales the whole amount by 26/12 as if it fell due every month. This script measures
how much of the visible BNPL obligation is arrears and fees rather than live instalments.

Reruns the RQ3 bureau arm (seeds 80,000-80,019, beta 0 and 1) and records, after burn-in:

* at every application the lender assesses (defaulted households excluded, since the bureau
  refuses them before the test): the live-instalment and arrears parts of the visible BNPL
  obligation, summed (value-weighted), overall and by income quintile;
* the same split over the stock of non-defaulted households at the end of each tick, and over
  every holder including defaulted households, whom the lender never assesses (the bureau
  refuses them before the test, and they no longer seek credit);
* the share of the visible obligation that is the live instalment of an agreement opened in
  the same tick (on the shortfall path BNPL is drawn before the traditional application);
* the refusals the visible BNPL obligation causes ("bureau-induced": the test fails with BNPL
  added but passes on traditional service alone), how many of those households carry BNPL
  arrears, and how many would pass if only live instalments were shown. The last is a
  one-decision counterfactual inside the run, not a rerun without arrears.

Instrumented by patching `TraditionalLender.apply` in each worker and stepping the model by
hand; the model code is unchanged. Writes results/summary/bureau_visible_split.json.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_bureau_visible_split.py
"""
import json
import warnings
from collections import Counter
from pathlib import Path

from joblib import Parallel, delayed

warnings.simplefilter("ignore")
from simulation.experiments import calibrated  # noqa: E402

QUINTILES = ("Q1", "Q2", "Q3", "Q4", "Q5")
SEEDS = range(80_000, 80_020)


def split(agent):
    """(live instalments, arrears incl. fees) per tick across platforms: Platform.obligations."""
    live = arrears = 0.0
    for p in agent.model.platforms:
        for loan in p.loans.get(agent.agent_id, ()):
            if loan.remaining > 0:
                live += loan.instalment
            arrears += loan.arrears
    return live, arrears


def one(params):
    from simulation.affordability import nca_gate
    from simulation.config import MONTHLY_TO_TICK
    from simulation.lender import TraditionalLender, new_loan_instalment
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    burn = params.burn_in
    c = Counter()

    orig_apply = TraditionalLender.apply

    def apply_hook(self, agent, amount):
        if amount > 0 and m.tick >= burn and not self.bureau.is_defaulted(agent.agent_id):
            q = agent.rec.income_quintile
            live, arr = split(agent)
            # Live instalments on agreements opened this tick: on the shortfall path the
            # household draws BNPL first and applies to the lender for the remainder.
            same = sum(loan.instalment for p in m.platforms
                       for loan in p.loans.get(agent.agent_id, ())
                       if loan.remaining > 0 and loan.opened_tick == m.tick)
            # Platform.obligations() is what the bureau adds; check the split reproduces it.
            assert abs(live + arr - agent.bnpl_obligations_per_tick()) < 1e-6
            for key in ("all", q):
                c[f"app_n_{key}"] += 1
                c[f"app_live_{key}"] += live
                c[f"app_arrears_{key}"] += arr
                c[f"app_live_same_tick_{key}"] += same
                c[f"app_with_bnpl_{key}"] += (live + arr) > 0
                c[f"app_with_arrears_{key}"] += arr > 0
            trad = agent.scheduled_service_tick / MONTHLY_TO_TICK
            inst = new_loan_instalment(amount)
            ok_full = nca_gate(agent.income_monthly, trad + (live + arr) / MONTHLY_TO_TICK, inst)
            ok_trad = nca_gate(agent.income_monthly, trad, inst)
            ok_live = nca_gate(agent.income_monthly, trad + live / MONTHLY_TO_TICK, inst)
            if not ok_full:
                for key in ("all", q):
                    c[f"refused_{key}"] += 1
                    if ok_trad:
                        c[f"bureau_refused_{key}"] += 1
                        c[f"bureau_refused_with_arrears_{key}"] += arr > 0
                        c[f"bureau_refused_pass_live_only_{key}"] += ok_live
            granted = orig_apply(self, agent, amount)
            # The replicated test must agree with the lender's own decision.
            c["gate_mismatch"] += (granted > 0) != ok_full
            return granted
        return orig_apply(self, agent, amount)

    def stock():
        # Called after each completed tick, whose index is m.tick - 1.
        if m.tick - 1 < burn:
            return
        for a in m.agents:
            live, arr = split(a)
            if live + arr <= 0:
                continue
            for key in ("all", a.rec.income_quintile):
                # Every holder, defaulted or not: the measure a probe on the stock gives.
                c[f"stockall_live_{key}"] += live
                c[f"stockall_arrears_{key}"] += arr
                c[f"stockall_arrears_defaulted_{key}"] += arr if a.defaulted else 0.0
            if a.defaulted:
                continue
            for key in ("all", a.rec.income_quintile):
                c[f"stock_live_{key}"] += live
                c[f"stock_arrears_{key}"] += arr
                c[f"stock_holders_{key}"] += 1
                c[f"stock_holders_arrears_{key}"] += arr > 0

    TraditionalLender.apply = apply_hook
    try:
        # The loop of BNPLModel.run, with the stock read after every tick.
        for _ in range(params.n_ticks):
            m.step()
            stock()
    finally:
        TraditionalLender.apply = orig_apply
    return dict(c)


def summarise(tot: Counter) -> dict:
    out = {}
    for key in ("all", *QUINTILES):
        app_obl = tot[f"app_live_{key}"] + tot[f"app_arrears_{key}"]
        stock_obl = tot[f"stock_live_{key}"] + tot[f"stock_arrears_{key}"]
        br = tot[f"bureau_refused_{key}"]
        out[key] = {
            # Value-weighted share of the visible BNPL obligation that is arrears and fees.
            "arrears_share_at_application": tot[f"app_arrears_{key}"] / app_obl if app_obl else None,
            "live_opened_same_tick_share_at_application": tot[f"app_live_same_tick_{key}"] / app_obl
            if app_obl else None,
            "arrears_share_stock": tot[f"stock_arrears_{key}"] / stock_obl if stock_obl else None,
            "arrears_share_stock_incl_defaulted": tot[f"stockall_arrears_{key}"]
            / (tot[f"stockall_arrears_{key}"] + tot[f"stockall_live_{key}"])
            if tot[f"stockall_arrears_{key}"] + tot[f"stockall_live_{key}"] else None,
            "arrears_held_by_defaulted_share": tot[f"stockall_arrears_defaulted_{key}"]
            / tot[f"stockall_arrears_{key}"] if tot[f"stockall_arrears_{key}"] else None,
            "applications": tot[f"app_n_{key}"],
            "applications_with_bnpl_share": tot[f"app_with_bnpl_{key}"] / tot[f"app_n_{key}"]
            if tot[f"app_n_{key}"] else None,
            "applications_with_arrears_share": tot[f"app_with_arrears_{key}"] / tot[f"app_n_{key}"]
            if tot[f"app_n_{key}"] else None,
            "holders_with_arrears_share_stock": tot[f"stock_holders_arrears_{key}"]
            / tot[f"stock_holders_{key}"] if tot[f"stock_holders_{key}"] else None,
            "gate_refusals": tot[f"refused_{key}"],
            "bureau_induced_refusals": br,
            "bureau_induced_share_of_refusals": br / tot[f"refused_{key}"] if tot[f"refused_{key}"] else None,
            "bureau_induced_with_arrears_share": tot[f"bureau_refused_with_arrears_{key}"] / br if br else None,
            "bureau_induced_pass_if_live_only_share": tot[f"bureau_refused_pass_live_only_{key}"] / br
            if br else None,
        }
    return out


if __name__ == "__main__":
    out = {"_note": (
        "RQ3 bureau arm (bnpl_bureau_visible=True), seeds 80,000-80,019, post-burn-in (tick >= 12). "
        "arrears_share_*: value-weighted share of the visible BNPL obligation (Platform.obligations) "
        "that is arrears including late fees, at the lender's applications (non-defaulted applicants) "
        "and over the end-of-tick stock of non-defaulted holders, or of every holder (incl_defaulted). "
        "live_opened_same_tick: share that is the instalment of an agreement opened in the same tick. "
        "bureau_induced: the gate fails with "
        "BNPL added and passes on traditional service alone; pass_if_live_only: it would pass if only "
        "live instalments were shown (one-decision counterfactual). Script: "
        "notebooks/scripts/check_bureau_visible_split.py.")}
    for b in (0.0, 1.0):
        ps = [calibrated(bnpl_enabled=True, beta=b, bnpl_bureau_visible=True,
                         label=f"rq3s_bureau_b{b}").replace(seed=s) for s in SEEDS]
        rows = Parallel(n_jobs=-2)(delayed(one)(p) for p in ps)
        tot = Counter()
        for r in rows:
            tot.update(r)
        assert tot["gate_mismatch"] == 0, tot["gate_mismatch"]
        out[f"beta{int(b)}"] = summarise(tot)
        for key in ("all", *QUINTILES):
            d = out[f"beta{int(b)}"][key]
            print(f"beta={b} {key}: arrears share at application "
                  f"{d['arrears_share_at_application']:.3f}, stock {d['arrears_share_stock']:.3f} "
                  f"(incl. defaulted {d['arrears_share_stock_incl_defaulted']:.3f}); "
                  f"bureau-induced refusals {d['bureau_induced_refusals']}, with arrears "
                  f"{d['bureau_induced_with_arrears_share']}, pass if live only "
                  f"{d['bureau_induced_pass_if_live_only_share']}")
    dest = Path("results/summary/bureau_visible_split.json")
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest}")
