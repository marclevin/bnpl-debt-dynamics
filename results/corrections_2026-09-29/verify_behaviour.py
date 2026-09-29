"""Small deterministic examples that establish what the model actually does.

Run from the repository root:

    PYTHONPATH=. .venv/bin/python results/corrections_2026-09-29/verify_behaviour.py

The script uses only interfaces that exist both before and after the corrections, so the
same file documents the original behaviour (git tag pre-correction-2026-09-29) and the
corrected behaviour. Its two outputs are stored next to it.

Every example is one household with a hand-set balance sheet, no income shock, no payment
friction and no peer influence, so nothing in it is random except platform routing, which
is examined separately.
"""

from __future__ import annotations

import warnings
from collections import Counter
from dataclasses import replace

from simulation.config import MONTHLY_TO_TICK, ParamSet
from simulation.model import BNPLModel

warnings.simplefilter("ignore", FutureWarning)

CHI = MONTHLY_TO_TICK


def household(
    *,
    income_tick: float,
    committed_tick: float,
    discretionary_tick: float = 0.0,
    d_trad: float = 0.0,
    service_tick: float = 0.0,
    apr: float = 0.26,
    savings: float = 0.0,
    min_payer: bool = False,
    seed: int = 1,
    **params,
):
    """One household with a hand-set balance sheet inside an otherwise ordinary model."""
    base = dict(
        seed=seed, n_agents=1, n_ticks=8, burn_in=0, shock_prob=0.0, payment_friction=0.0,
        q_base=0.0, beta=0.0, bnpl_enabled=True, n_platforms=4,
    )
    base.update(params)
    model = BNPLModel(ParamSet(**base))
    agent = next(iter(model.agents))
    agent.rec = replace(
        agent.rec,
        income_source="GRANT",  # exempt from the income shock
        n_earners=0,
        income_tick=income_tick,
        income_wage_tick=0.0,
        committed_tick=committed_tick,
        discretionary_tick=discretionary_tick,
        discretionary_monthly=discretionary_tick / CHI,
        income_monthly=income_tick / CHI,
        banked=True,
    )
    agent.is_wage_household = False
    agent.income_monthly = income_tick / CHI
    agent.bnpl_eligible = base["bnpl_enabled"]
    agent.is_min_payer = min_payer
    agent.d_trad = d_trad
    agent.scheduled_service_tick = service_tick
    agent.apr_annual = apr
    agent.savings = savings
    for pl in model.platforms:
        pl.rolling_limits[agent.agent_id] = base.get("bnpl_limit_income_multiple", 0.10) * agent.income_monthly
    return model, agent


def loans(model, agent):
    return {pl.platform_id: [(round(l.principal, 2), l.remaining, round(l.arrears, 2)) for l in pl.loans.get(agent.agent_id, [])]
            for pl in model.platforms if pl.loans.get(agent.agent_id)}


def rule(title):
    print("\n" + "=" * 88 + f"\n{title}\n" + "=" * 88)


# --------------------------------------------------------------------------------------
rule("1. TRADITIONAL INTEREST AND PAYMENT ACCOUNTING")
print("Balance R1,000 at 26% a year (1% a tick), instalment R100 a tick, income ample.")
print("Correct accounting: 1000 + 10 interest - 100 paid = 910 after one tick.")
m, a = household(income_tick=5000, committed_tick=1000, d_trad=1000, service_tick=100, bnpl_enabled=False)
for t in range(3):
    before = a.d_trad
    m.step()
    print(f"  tick {t}: balance {before:9.2f} -> {a.d_trad:9.2f}   interest charged {a.interest_charged_tick:6.2f}"
          f"   arrears {a.arrears_trad:6.2f}   savings {a.savings:8.2f}")
print("Life of the loan: R1,000 amortised over 12 ticks at 1% a tick (instalment R88.85).")
m, a = household(income_tick=5000, committed_tick=1000, d_trad=1000, service_tick=88.85, bnpl_enabled=False, n_ticks=40)
paid_total, t = 0.0, 0
while a.d_trad > 0.005 and t < 40:
    s0 = a.savings
    m.step()
    paid_total += (s0 + 5000 - 1000) - a.savings
    t += 1
print(f"  balance cleared after {t} ticks; paid to the lender {paid_total:.2f} (contract: 12 ticks, 1066.19)")
print(f"  scheduled service still shown to the gate after the balance cleared: {a.scheduled_service_tick:.2f} a tick")
print(f"  total_debt() with balance {a.d_trad:.2f} and arrears {a.arrears_trad:.2f}: {a.total_debt():.2f}")
print("Arrears inside total debt: balance R1,000, instalment R100, income too low to pay it.")
m, a = household(income_tick=1000, committed_tick=1000, d_trad=1000, service_tick=100, bnpl_enabled=False,
                 amount_rule="shortfall")
a.defaulted = True  # blocks borrowing so the instalment simply goes unpaid
m.step()
print(f"  after one unpaid tick: d_trad {a.d_trad:.2f}, arrears {a.arrears_trad:.2f}, total_debt() {a.total_debt():.2f}"
      f"   (owed to the lender: {a.d_trad:.2f})")

# --------------------------------------------------------------------------------------
rule("2. SHORTFALL COVERAGE: BNPL FIRST, THEN THE TRADITIONAL LENDER")
print("Income R3,000 a tick, committed R3,000, no savings, instalment R200 due: shortfall R200.")
print("Discretionary budget large enough that the BNPL share of the request is not capped.")
for label, kw in [("traditional credit only (BNPL disabled)", dict(bnpl_enabled=False)),
                  ("BNPL enabled", dict(bnpl_enabled=True))]:
    m, a = household(income_tick=3000, committed_tick=3000, discretionary_tick=2000,
                     d_trad=4000, service_tick=200, apr=0.0, **kw)
    m.step()
    h = m.history[-1]
    print(f"  {label}:")
    print(f"     traditional applications {m.lender.n_applications}, granted value {m.lender.value_granted:.2f}")
    print(f"     BNPL agreements {loans(m, a)}")
    print(f"     distressed this tick: {a.distress_streak == 1};  traditional arrears {a.arrears_trad:.2f};"
          f"  balance {a.d_trad:.2f};  savings {a.savings:.2f}")

# --------------------------------------------------------------------------------------
rule("3. INSTALMENT TIMING ON THE TWO BORROWING PATHS")
print("Contract: 25% at checkout, then 25% at each of the NEXT three ticks.")
print("Shortfall path (same household as example 2, BNPL enabled):")
m, a = household(income_tick=3000, committed_tick=3000, discretionary_tick=2000,
                 d_trad=4000, service_tick=200, apr=0.0)
m.step()
print(f"  end of the origination tick: agreements (principal, instalments remaining, arrears) {loans(m, a)}")
print("Want-driven path (purchase probability 1, income ample, no debt):")
m, a = household(income_tick=3000, committed_tick=1000, discretionary_tick=500, q_base=1.0, bnpl_purchase_cv=0.0001)
m.step()
print(f"  end of the origination tick: {loans(m, a)}")
a_q = m.params
m.params = replace(m.params, q_base=0.0)
m.step()
print(f"  end of the next tick:        {loans(m, a)}")

# --------------------------------------------------------------------------------------
rule("4. WHAT THE CAP COUNTS AND WHICH DRAWS IT BLOCKS")
for cap in (1, 2, 3):
    agreements, platforms = Counter(), Counter()
    for seed in range(200):
        m, a = household(income_tick=30000, committed_tick=1000, discretionary_tick=500, stacking_cap=cap,
                         bnpl_limit_income_multiple=1.0, seed=seed)
        for i in range(40):
            a._bnpl_draw(100.0)
        agreements[sum(len(pl.loans.get(a.agent_id, [])) for pl in m.platforms)] += 1
        platforms[a.stacking_depth()] += 1
    print(f"  cap {cap}: 40 requests of R100 in one tick, ample limits, 200 seeds -> platforms owed "
          f"{dict(sorted(platforms.items()))}; open agreements {dict(sorted(agreements.items()))}")
m, a = household(income_tick=30000, committed_tick=1000, stacking_cap=2, bnpl_limit_income_multiple=1.0, seed=3)
m.platforms[0].request(a.agent_id, 100.0)
m.platforms[1].request(a.agent_id, 100.0)
print(f"  cap 2, household already owes platforms 0 and 1: a further draw of R100 finances {a._bnpl_draw(100.0):.2f}"
      "  (a draw on a platform already in use is refused too)")

# --------------------------------------------------------------------------------------
rule("5. PLATFORM ROUTING")
first = Counter()
for seed in range(2000):
    m, a = household(income_tick=30000, committed_tick=1000, bnpl_limit_income_multiple=1.0, seed=seed)
    a._bnpl_draw(100.0)
    first[next(pl.platform_id for pl in m.platforms if pl.has_balance(a.agent_id))] += 1
print(f"  platform that receives a first request, 2,000 seeds: {dict(sorted(first.items()))}")
second_new = 0
for seed in range(2000):
    m, a = household(income_tick=30000, committed_tick=1000, bnpl_limit_income_multiple=1.0, seed=seed)
    a._bnpl_draw(100.0)
    a._bnpl_draw(100.0)
    second_new += a.stacking_depth() == 2
print(f"  second request lands on a different platform although the first has headroom: {second_new / 2000:.3f}"
      "   (uniform routing over 4 platforms implies 0.750)")
m, a = household(income_tick=3000, committed_tick=1000, bnpl_limit_income_multiple=0.10, seed=5)
got = a._bnpl_draw(2000.0)
print(f"  one request of R2,000 against per-platform limits of R{0.10 * a.income_monthly:.0f}: financed {got:.2f}, split {loans(m, a)}")

# --------------------------------------------------------------------------------------
rule("6. WHAT EACH AFFORDABILITY GATE OBSERVES")
m, a = household(income_tick=3000, committed_tick=1000, d_trad=4000, service_tick=200, apr=0.0,
                 bnpl_limit_income_multiple=1.0)
m.platforms[0].request(a.agent_id, 400.0)
m.platforms[1].request(a.agent_id, 800.0)
print(f"  household: traditional instalment R200 a tick; BNPL instalments R100 (platform 0) and R200 (platform 1) a tick")
for visible in (False, True):
    m.bureau.bnpl_visible = visible
    print(f"  traditional lender, bureau visibility {visible!s:5}: monthly service it sees = "
          f"{m.bureau.visible_monthly_service(a):8.2f}   (traditional alone {200 / CHI:.2f}; with BNPL {(200 + 300) / CHI:.2f})")
print("  screening gate on a new BNPL request: tested below with income that admits the request only if"
      " BNPL on other platforms is NOT counted")
from simulation.affordability import nca_max_service
room = nca_max_service(a.income_monthly)
m.params = replace(m.params, bnpl_affordability_check=True, bnpl_bureau_visible=False)
m.bureau.bnpl_visible = False
trad_only = 200 / CHI
with_bnpl = (200 + 300) / CHI
probe = (room - trad_only) * CHI * 4 * 0.98          # fits if only traditional service is counted
fits_if_bnpl_counted = (probe / 4) / CHI <= room - with_bnpl
res = a._bnpl_draw(probe)
print(f"     Reg 23A room {room:.2f} a month; request R{probe:.2f} fits against traditional service alone, "
      f"and against traditional plus BNPL: {fits_if_bnpl_counted}")
print(f"     financed with the bureau switch OFF: {res:.2f}  -> the screening gate "
      f"{'counts' if res == 0 else 'does not count'} BNPL held on other platforms")
m2, a2 = household(income_tick=3000, committed_tick=1000)
a2.n_unemployed = 1
print(f"  income used by both gates: agent.income_monthly = {a2.income_monthly:.2f}, fixed at initialisation"
      " (not reduced while a member is unemployed)")
