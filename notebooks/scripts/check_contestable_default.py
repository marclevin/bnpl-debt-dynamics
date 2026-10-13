"""Examiner hole H3 (2026-10-13): default excluding households that default regardless.

About 3.6% of agents have surveyed income below their food and rent (committed spending)
from the start, and about 96% of them default in every arm (defaulter_credit.json). This
script measures default among the OTHER households, the "contestable" rate, and the BNPL
and bureau-visibility effects on it, so the effects can be stated relative to the part of
default that the experiments can move.

Reruns, with agent-level default recorded:
* the three blocks pooled for the beta = 1 BNPL effect, and the four for beta = 0, exactly as
  in build_results_tables.derived_numbers: rq0 (seeds 10,000-10,019), the access sweep at full
  against zero access (30,000-), the threshold control (60,000-, beta = 0 only) and the
  effect-sensitivity reference (70,000-);
* the RQ3 benchmark and bureau arms at beta 0 and 1 (seeds 80,000-80,099);
* the single-tick shock arm of the effect suite, off and on (hole H4, seeds 70,000-70,019).
Each run's population-wide default rate is checked against results/raw/*.parquet, so the
rerun is the published run. Writes results/summary/contestable_default.json.

    PYTHONPATH=. .venv/bin/python notebooks/scripts/check_contestable_default.py
"""
import json
import sys
import warnings
from pathlib import Path

import pandas as pd
from joblib import Parallel, delayed

warnings.simplefilter("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from results_common import delta, paired_diff  # noqa: E402

from simulation import experiments as ex  # noqa: E402

QUINTILES = ("Q1", "Q2", "Q3", "Q4", "Q5")


def one(params):
    from simulation.model import BNPLModel

    m = BNPLModel(params)
    m.run()
    row = {"label": params.label, "seed": params.seed, "beta": params.beta,
           "bnpl_access_rate": params.bnpl_access_rate, "gamma": params.gamma,
           "sigma_theta": params.sigma_theta}
    agents = list(m.agents)
    struct = [a for a in agents if a.income_tick < a.committed_tick]
    other = [a for a in agents if not a.income_tick < a.committed_tick]
    row["n_agents"] = len(agents)
    row["default_rate_final"] = sum(a.defaulted for a in agents) / len(agents)
    row["n_struct"] = len(struct)
    row["struct_default_rate"] = sum(a.defaulted for a in struct) / len(struct)
    row["contestable_default_rate"] = sum(a.defaulted for a in other) / len(other)
    # Contestable defaults as points of the whole population, for the decomposition.
    row["contestable_default_pop"] = sum(a.defaulted for a in other) / len(agents)
    for q in QUINTILES:
        oq = [a for a in other if a.rec.income_quintile == q]
        row[f"contestable_default_rate_{q}"] = sum(a.defaulted for a in oq) / len(oq)
    return row


def arms():
    out = list(ex.rq0_baseline(20))
    out += [p for p in ex.rq2_surface(20)
            if p.beta in (0.0, 1.0) and p.bnpl_access_rate in (0.0, 1.0)]
    thr = [p for p in ex.rq2_threshold(20) if p.label.startswith("rq2t_a") and p.gamma == 0]
    smin = min(p.sigma_theta for p in thr)
    out += [p for p in thr if p.sigma_theta == smin and p.bnpl_access_rate in (0.0, 1.0)]
    out += [p for p in ex.effect_robustness(20)
            if p.label in ("eff_ref_off", "eff_ref_b0.0", "eff_ref_b1.0")
            or p.label.startswith("eff_shock_single_tick_")]
    out += [p for p in ex.rq3_scenarios(20) if "_bench_" in p.label or "_bureau_" in p.label]
    return out


def check_against_raw(df: pd.DataFrame) -> int:
    """Every rerun must reproduce the published population default rate."""
    n = 0
    for suite in ("rq0", "rq2", "rq2t", "effect", "rq3s"):
        raw = pd.read_parquet(f"results/raw/{suite}.parquet")
        m = df.merge(raw[["label", "seed", "default_rate_final"]], on=["label", "seed"],
                     suffixes=("", "_raw"))
        assert (abs(m.default_rate_final - m.default_rate_final_raw) < 1e-12).all(), suite
        n += len(m)
    return n


def pooled(blocks: dict) -> tuple[float, float]:
    w = {k: 1.0 / se**2 for k, (_, se) in blocks.items()}
    est = sum(w[k] * blocks[k][0] for k in blocks) / sum(w.values())
    return est, (1.0 / sum(w.values())) ** 0.5


if __name__ == "__main__":
    ps = arms()
    df = pd.DataFrame(Parallel(n_jobs=-2)(delayed(one)(p) for p in ps))
    assert check_against_raw(df) == len(df), "a rerun is missing from results/raw"

    def lab(x):
        return df[df.label == x]

    rq2 = df[df.label.str.startswith("rq2_")]
    thr = df[df.label.str.startswith("rq2t_")]
    out = {"_note": (
        "Contestable default: default among households whose surveyed income covers food and "
        "rent at the start (a.income_tick >= a.committed_tick). Effects in percentage points "
        "of that rate, as fractions; pooled by inverse variance over the blocks of "
        "build_results_tables.derived_numbers. Script: notebooks/scripts/check_contestable_default.py.")}
    out["n_runs_checked_against_raw"] = len(df)
    base = lab("baseline_no_bnpl")
    out["baseline_default_rate"] = base.default_rate_final.mean()
    out["baseline_contestable_default_rate"] = base.contestable_default_rate.mean()
    out["baseline_contestable_default_pop"] = base.contestable_default_pop.mean()
    out["struct_share_of_agents"] = base.n_struct.mean() / 5000
    out["struct_default_rate_baseline"] = base.struct_default_rate.mean()
    for q in QUINTILES:
        out[f"baseline_contestable_default_rate_{q}"] = base[f"contestable_default_rate_{q}"].mean()

    col = "contestable_default_rate"
    for b, keys in ((0, ("rq0", "access", "threshold_control", "effect")), (1, ("rq0", "access", "effect"))):
        blocks = {
            "rq0": delta(lab(f"bnpl_on_beta{b}"), base, col),
            "access": delta(rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 1.0)],
                            rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 0.0)], col),
            "threshold_control": delta(thr[thr.bnpl_access_rate == 1.0],
                                       thr[thr.bnpl_access_rate == 0.0], col),
            "effect": paired_diff(lab(f"eff_ref_b{b}.0"), lab("eff_ref_off"), col),
        }
        blocks = {k: blocks[k] for k in keys}
        est, se = pooled(blocks)
        # The same pooling on the population rate, which must reproduce results_numbers.json.
        pop = {
            "rq0": delta(lab(f"bnpl_on_beta{b}"), base, "default_rate_final"),
            "access": delta(rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 1.0)],
                            rq2[(rq2.beta == b) & (rq2.bnpl_access_rate == 0.0)], "default_rate_final"),
            "threshold_control": delta(thr[thr.bnpl_access_rate == 1.0],
                                       thr[thr.bnpl_access_rate == 0.0], "default_rate_final"),
            "effect": paired_diff(lab(f"eff_ref_b{b}.0"), lab("eff_ref_off"), "default_rate_final"),
        }
        pest, pse = pooled({k: pop[k] for k in keys})
        out[f"beta{b}_effect_pooled_population"] = pest
        out[f"beta{b}_effect_pooled_population_se"] = pse
        out[f"beta{b}_effect_pooled_contestable"] = est
        out[f"beta{b}_effect_pooled_contestable_se"] = se
        out[f"beta{b}_effect_relative_to_contestable_baseline"] = est / out["baseline_contestable_default_rate"]
        out[f"beta{b}_effect_relative_to_full_baseline"] = pest / out["baseline_default_rate"]
        for k, (d, s) in blocks.items():
            out[f"beta{b}_effect_contestable_{k}"], out[f"beta{b}_effect_contestable_{k}_se"] = d, s

    for b in (0.0, 1.0):
        bench, bur = lab(f"rq3s_bench_b{b}"), lab(f"rq3s_bureau_b{b}")
        tag = f"b{int(b)}"
        out[f"rq3s_bench_default_{tag}"] = bench.default_rate_final.mean()
        out[f"rq3s_bench_contestable_{tag}"] = bench[col].mean()
        d, s = paired_diff(bur, bench, "default_rate_final")
        out[f"rq3s_bureau_diff_population_{tag}"], out[f"rq3s_bureau_diff_population_{tag}_se"] = d, s
        d, s = paired_diff(bur, bench, col)
        out[f"rq3s_bureau_diff_contestable_{tag}"], out[f"rq3s_bureau_diff_contestable_{tag}_se"] = d, s
        out[f"rq3s_bureau_relative_to_contestable_bench_{tag}"] = d / bench[col].mean()
        out[f"rq3s_bureau_relative_to_full_bench_{tag}"] = (
            out[f"rq3s_bureau_diff_population_{tag}"] / bench.default_rate_final.mean())

    # Examiner hole H4: the single-tick arm (no hires, wage households only) against the
    # reference, both on the effect block (70,000-70,019).
    for name in ("ref", "shock_single_tick"):
        off = lab(f"eff_{name}_off")
        out[f"eff_{name}_off_default"] = off.default_rate_final.mean()
        out[f"eff_{name}_off_struct_default_rate"] = off.struct_default_rate.mean()
        out[f"eff_{name}_off_contestable"] = off[col].mean()
        out[f"eff_{name}_off_contestable_pop"] = off.contestable_default_pop.mean()
        for b in (0, 1):
            d, s_ = paired_diff(lab(f"eff_{name}_b{b}.0"), off, col)
            out[f"eff_{name}_effect_contestable_b{b}"], out[f"eff_{name}_effect_contestable_b{b}_se"] = d, s_
    out["single_tick_removes_contestable_share"] = 1.0 - (
        out["eff_shock_single_tick_off_contestable"] / out["eff_ref_off_contestable"])

    dest = Path("results/summary/contestable_default.json")
    dest.write_text(json.dumps(out, indent=2))
    for k, v in out.items():
        print(k, round(v, 5) if isinstance(v, float) else v)
    print(f"wrote {dest}")
