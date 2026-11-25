"""D19 (supervisor, 2026-11-24): the BNPL effect by household group, under the wage-income
screen and on a redrawn population.

The effect at beta = 0 is carried by the households short from the start (income_tick <
committed_tick, Section 3.5). The supervisor asked for two checks: an arm in which platforms
lend only to households with surveyed labour-market income, on the seeds of
tab:baseline-arms, and the main comparison rerun with a new population draw in each
replicate. This script reruns, with household-level default recorded,

* the rq0 arms `baseline_no_bnpl` and `bnpl_on_beta0` (seeds 10,000-10,019; the benchmark);
* the wage-income screen arm `screen_b0.0` (the same seeds; results/raw/screen.parquet);
* the redrawn population, `redraw_off` and `redraw_b0.0` (seeds 110,000-110,099, one
  population draw per replicate; results/raw/redraw.parquet),

checks every run's default against results/raw, and writes results/summary/effect_split.json:
the effect on default during the run (new defaults after the start, as a share of all
households, as in tab:baseline-arms) for all households and for the households short and not
short from the start, with paired standard errors; who the screen leaves out; and how the
redrawn populations vary. It also records what NIDS's w5_hhwage, the variable the screen uses,
is made of. Rates are fractions, as in results_numbers.json; build_results_tables.py writes
tab:effect-split from this file.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_effect_split.py
"""
from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

warnings.simplefilter("ignore")
from simulation import experiments as ex  # noqa: E402
from simulation.config import NIDS_HHDERIVED, NIDS_INDDERIVED, POPULATION_PARQUET  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "results" / "raw"
OUT = ROOT / "results" / "summary" / "effect_split.json"
RQ0_ARMS = ("baseline_no_bnpl", "bnpl_on_beta0")
#: The eight individual labour-market components of indderived (monthly), tested against w5_hhwage.
WAGE_PARTS = ["fwag", "cwag", "swag", "prof", "extr", "bonu", "cheq", "help"]


def one(params) -> dict:
    """One run, with default during the run split by group and the lender's grants recorded."""
    warnings.simplefilter("ignore")  # Mesa's seed deprecation, in each worker
    from simulation.lender import TraditionalLender
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    agents = list(m.agents)
    n = len(agents)
    short = {a.agent_id for a in agents if a.income_tick < a.committed_tick}
    start = {a.agent_id for a in agents if a.defaulted}
    at_risk = short - start
    granted: set[int] = set()
    original = TraditionalLender.apply

    # As in check_short_group_lending.py: a wrapper that records grants and changes nothing.
    def apply(self, agent, amount):
        got = original(self, agent, amount)
        if agent.agent_id in at_risk and amount > 0 and got > 0:
            granted.add(agent.agent_id)
        return got

    TraditionalLender.apply = apply
    try:
        summary = m.run()
    finally:
        TraditionalLender.apply = original
    end = {a.agent_id for a in agents if a.defaulted}
    assert start <= end, "default is absorbing"
    new = end - start
    assert len(new) == round(summary["new_default_rate_final"] * n)
    row = {
        "label": params.label, "seed": params.seed, "population_seed": params.population_seed,
        "shock_prob": params.shock_prob, "n_agents": n,
        "default_rate_final": summary["default_rate_final"],
        "new_default_rate_final": summary["new_default_rate_final"],
        "n_bnpl_eligible": summary["n_bnpl_eligible"],
        "n_short": len(short), "n_short_at_risk": len(at_risk),
        "new_default_short": len(new & short) / n,
        "new_default_other": len(new - short) / n,
    }
    if params.population_seed is None:  # the canonical population: keep who is who
        row["_at_risk"] = sorted(at_risk)
        row["_granted"] = sorted(granted)
        row["_new_at_risk"] = sorted(new & at_risk)
        row["_wage"] = sorted(r.agent_id for r in m.records if r.income_wage_tick > 0)
        row["_banked"] = sorted(r.agent_id for r in m.records if r.banked)
    return row


def arms() -> list:
    out = [p for p in ex.rq0_baseline(20) if p.label in RQ0_ARMS]
    out += ex.wage_screen(20)
    out += ex.population_redraw(20)
    return out


def check_against_raw(df: pd.DataFrame) -> int:
    """Every rerun must reproduce its stored row."""
    n = 0
    for suite in ("rq0", "screen", "redraw"):
        raw = pd.read_parquet(RAW / f"{suite}.parquet")
        m = df.merge(raw[["label", "seed", "default_rate_final", "new_default_rate_final", "shock_prob"]],
                     on=["label", "seed"], suffixes=("", "_raw"))
        for c in ("default_rate_final", "new_default_rate_final", "shock_prob"):
            assert (m[c] == m[f"{c}_raw"]).all(), (suite, c)
        n += len(m)
    return n


def paired(df: pd.DataFrame, on: str, off: str, col: str) -> tuple[float, float, float]:
    """on - off seed by seed: mean, paired standard error, SD of the differences."""
    x = df[df.label == on].set_index("seed")[col]
    y = df[df.label == off].set_index("seed")[col]
    assert sorted(x.index) == sorted(y.index), (on, off)
    d = (x - y.reindex(x.index)).astype(float)
    return float(d.mean()), float(d.std(ddof=1) / math.sqrt(len(d))), float(d.std(ddof=1))


def spread(s: pd.Series) -> dict:
    return {"mean": float(s.mean()), "sd": float(s.std(ddof=1)), "min": float(s.min()), "max": float(s.max())}


def hhwage_components() -> dict:
    """What w5_hhwage is: compared, household by household, with sums of member income."""
    cols = ["w5_hhid"] + [f"w5_{c}" for c in WAGE_PARTS]
    ind = pd.read_stata(NIDS_INDDERIVED, columns=cols, convert_categoricals=False)
    for c in WAGE_PARTS:
        ind[f"w5_{c}"] = pd.to_numeric(ind[f"w5_{c}"], errors="coerce")
    sums = ind.groupby("w5_hhid")[[f"w5_{c}" for c in WAGE_PARTS]].sum(min_count=1).fillna(0.0)
    hh = pd.read_csv(NIDS_HHDERIVED, usecols=["w5_hhid", "w5_hhwage", "w5_hhincome_flg"])
    m = hh.merge(sums, left_on="w5_hhid", right_index=True, how="left").fillna(
        {f"w5_{c}": 0.0 for c in WAGE_PARTS})
    known = m[m.w5_hhwage.notna()]

    def matches(parts: list[str]) -> int:
        tot = known[[f"w5_{c}" for c in parts]].sum(axis=1)
        return int(np.isclose(tot, known.w5_hhwage, rtol=0, atol=0.5).sum())

    member_total = m[[f"w5_{c}" for c in WAGE_PARTS]].sum(axis=1)
    all8 = known[[f"w5_{c}" for c in WAGE_PARTS]].sum(axis=1)
    matched = pd.read_parquet(ROOT / "data/processed/synthetic_population_matched.parquet", columns=["w5_hhid"])
    pop = pd.read_parquet(POPULATION_PARQUET, columns=["source_w5_hhid", "income_source"])
    missing = m[m.w5_hhwage.isna() & (member_total > 0)]
    return {
        "_note": ("w5_hhwage (hhderived) against the sum over household members of eight indderived "
                  "monthly components: fwag (primary and secondary jobs), cwag (casual work), swag "
                  "(self-employment), prof (profit share), extr (piece-rate), bonu (bonuses), cheq "
                  "(13th cheque) and help (helping friends). Match: within R0.50."),
        "households": int(len(m)),
        "households_with_hhwage": int(len(known)),
        "match_all_eight": matches(WAGE_PARTS),
        "match_all_eight_max_abs_diff": float((all8 - known.w5_hhwage).abs().max()),
        "match_without_self_employment": matches([c for c in WAGE_PARTS if c != "swag"]),
        "match_jobs_casual_self_employment_only": matches(["fwag", "cwag", "swag"]),
        "missing_hhwage_with_member_labour_income": int(len(missing)),
        "missing_hhwage_with_member_labour_income_income_flag": missing.w5_hhincome_flg.value_counts().to_dict(),
        "missing_hhwage_with_member_labour_income_in_matched": int(missing.w5_hhid.isin(matched.w5_hhid).sum()),
        "agents_from_those_households": int(pop.source_w5_hhid.isin(missing.w5_hhid).sum()),
        "agents_from_those_households_income_source": pop[pop.source_w5_hhid.isin(missing.w5_hhid)]
        .income_source.value_counts().to_dict(),
        "_missing_ids": sorted(int(i) for i in missing.w5_hhid),
    }


def main() -> None:
    ps = arms()
    df = pd.DataFrame(Parallel(n_jobs=-2)(delayed(one)(p) for p in ps))
    assert check_against_raw(df) == len(df), "a rerun is missing from results/raw"
    df["new_default_all"] = df.new_default_rate_final
    assert np.allclose(df.new_default_short + df.new_default_other, df.new_default_all, rtol=0, atol=1e-12)

    out: dict = {"_note": (
        "D19 (2026-11-24). Default during the run: households that enter default after the start, "
        "as a share of all households (fractions; x100 for points), so the two groups sum to all. "
        "Short from the start: surveyed income below committed expenditure (income_tick < "
        "committed_tick). Benchmark and screen: seeds 10,000-10,019, each paired by seed with "
        "baseline_no_bnpl of results/raw/rq0.parquet. Redrawn population: seeds 110,000-110,099, "
        "one population draw per replicate shared by its BNPL-off and BNPL-on runs, paired by draw. "
        "se: paired standard error; sd: SD of the per-seed (per-draw) differences. "
        "Script: notebooks/scripts/check_effect_split.py.")}
    out["n_runs_checked_against_raw"] = len(df)

    rows = {"bench": ("bnpl_on_beta0", "baseline_no_bnpl"), "screen": ("screen_b0.0", "baseline_no_bnpl"),
            "redraw": ("redraw_b0.0", "redraw_off"), "screen_less_bench": ("screen_b0.0", "bnpl_on_beta0")}
    for key, (on, off) in rows.items():
        for g in ("all", "short", "other"):
            d, se, sd = paired(df, on, off, f"new_default_{g}")
            out[f"{key}_{g}"], out[f"{key}_{g}_se"], out[f"{key}_{g}_sd"] = d, se, sd
        out[f"{key}_n"] = int((df.label == on).sum())

    # --- the canonical population: who the screen leaves out --------------------------------
    can = df[df.population_seed.isna()]
    first = can.iloc[0]
    for c in ("_at_risk", "_wage", "_banked"):
        assert all(r == first[c] for r in can[c]), f"{c} differs between seeds"
    at_risk, wage, banked = set(first["_at_risk"]), set(first["_wage"]), set(first["_banked"])
    pop = pd.read_parquet(POPULATION_PARQUET, columns=["agent_id", "source_w5_hhid"]).set_index("agent_id")
    from simulation.population import build_records

    short_ids = {r.agent_id for r in build_records()[0] if r.income_tick < r.committed_tick}
    short_n = int(first["n_short"])
    assert len(short_ids) == short_n and at_risk <= short_ids
    srcs = lambda ids: int(pop.loc[sorted(ids), "source_w5_hhid"].nunique())  # noqa: E731
    out.update(
        short_n=short_n, short_sources=srcs(short_ids),
        short_at_risk=len(at_risk), short_at_risk_sources=srcs(at_risk),
        short_at_risk_banked=len(at_risk & banked), short_at_risk_banked_wage=len(at_risk & banked & wage),
        short_at_risk_wage=len(at_risk & wage),
    )
    # The lent-to split is the lender's grants in the no-BNPL run, seed by seed, as in
    # check_short_group_lending.py; it moves by a household on some seeds (55 or 56 never lent
    # to), so every count below is a mean over the 20 seeds.
    by_seed = {lab: can[can.label == lab].set_index("seed") for lab in
               ("baseline_no_bnpl", "bnpl_on_beta0", "screen_b0.0")}
    split = []
    for seed, off_row in by_seed["baseline_no_bnpl"].iterrows():
        lent = set(off_row["_granted"])
        never = at_risk - lent
        r = {"seed": seed}
        for name, ids in (("never_lent", never), ("lent", lent)):
            r[name] = len(ids)
            r[f"{name}_banked"] = len(ids & banked)
            r[f"{name}_wage"] = len(ids & wage)
            r[f"{name}_banked_wage"] = len(ids & banked & wage)
            r[f"{name}_sources"] = srcs(ids)
            for lab, tag in (("baseline_no_bnpl", "off"), ("bnpl_on_beta0", "bench"), ("screen_b0.0", "screen")):
                r[f"{name}_default_{tag}"] = len(set(by_seed[lab].loc[seed, "_new_at_risk"]) & ids)
        split.append(r)
    split = pd.DataFrame(split)
    for c in split.columns.drop("seed"):
        out[c] = float(split[c].mean())
        if c.startswith(("never_lent", "lent")) and split[c].nunique() > 1:
            out[f"{c}_min"], out[f"{c}_max"] = int(split[c].min()), int(split[c].max())
    grants = [set(g) for g in by_seed["baseline_no_bnpl"]["_granted"]]
    never_every = at_risk - set.union(*grants)  # never lent to on any of the 20 seeds
    out["never_lent_every_seed"] = len(never_every)
    out["never_lent_every_seed_wage"] = len(never_every & wage)
    out["never_lent_every_seed_sources"] = srcs(never_every)
    out["lent_every_seed"] = len(set.intersection(*grants))
    for lab, tag in (("baseline_no_bnpl", "off"), ("bnpl_on_beta0", "bench"), ("screen_b0.0", "screen")):
        out[f"eligible_{tag}"] = float(by_seed[lab].n_bnpl_eligible.mean())
    # The lending split must be the one short_group_lending.json reports.
    sgl = json.loads((ROOT / "results/summary/short_group_lending.json").read_text())["summary"]
    assert len(at_risk) == sgl["at_risk"]["mean"]
    for mine, theirs in (("lent", "lent_to"), ("never_lent", "never_lent_to"),
                         ("never_lent_default_bench", "never_default_on"),
                         ("never_lent_default_off", "never_default_off"),
                         ("lent_default_bench", "lent_to_default_on"),
                         ("lent_default_off", "lent_to_default_off")):
        assert abs(out[mine] - sgl[theirs]["mean"]) < 1e-9, (mine, out[mine], sgl[theirs]["mean"])

    # --- the redrawn populations --------------------------------------------------------------
    red_off = df[df.label == "redraw_off"]
    out["redraw_seeds"] = [int(red_off.seed.min()), int(red_off.seed.max())]
    out["redraw_short_n"] = spread(red_off.n_short)
    out["redraw_short_at_risk"] = spread(red_off.n_short_at_risk)
    out["redraw_baseline_new_default"] = spread(red_off.new_default_rate_final)
    out["redraw_baseline_default"] = spread(red_off.default_rate_final)
    out["redraw_separation_rate"] = spread(red_off.shock_prob)
    out["canonical_separation_rate"] = float(ex.DERIVED_SHOCK_PROB)
    out["canonical_baseline_new_default"] = float(by_seed["baseline_no_bnpl"].new_default_rate_final.mean())
    out["effect_sd_rq0_seeds"] = out["bench_all_sd"]
    out["effect_sd_redraws"] = out["redraw_all_sd"]
    out["w5_hhwage"] = hhwage_components()
    missing = set(out["w5_hhwage"].pop("_missing_ids"))
    hh_of = pop.source_w5_hhid
    out["w5_hhwage"]["agents_from_those_households_short"] = int(hh_of.loc[sorted(short_ids)].isin(missing).sum())
    out["w5_hhwage"]["agents_from_those_households_at_risk"] = int(hh_of.loc[sorted(at_risk)].isin(missing).sum())
    out["w5_hhwage"]["agents_from_those_households_never_lent_every_seed"] = int(
        hh_of.loc[sorted(never_every)].isin(missing).sum())

    ints = ["seed", "n_short", "n_short_at_risk", "n_bnpl_eligible"]
    floats = ["shock_prob", "default_rate_final", "new_default_rate_final", "new_default_short",
              "new_default_other"]
    out["per_run"] = [
        {"label": r["label"], **{c: int(r[c]) for c in ints},
         "population_seed": None if pd.isna(r["population_seed"]) else int(r["population_seed"]),
         **{c: float(r[c]) for c in floats}}
        for _, r in df.iterrows()
    ]
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    for k, v in out.items():
        if k != "per_run":
            print(k, round(v, 6) if isinstance(v, float) else v)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
