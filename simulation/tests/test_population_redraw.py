"""Verification: the wage-income screen and the redrawn population (D19, 2026-11-24).

  * with both new fields at their defaults a run reproduces a stored rq0 row exactly;
  * the P3 step, moved into population.py, reproduces the canonical population with P3's seed;
  * under the screen no household without wage income is eligible, and the eligibility draw
    consumes the same random numbers as the benchmark's, so the arm pairs by seed;
  * population draws differ between seeds and repeat on one seed.
"""

from __future__ import annotations

import math
import warnings

import pandas as pd
import pytest

from simulation.config import MATCHED_PARQUET, POPULATION_PARQUET, RESULTS_RAW, ParamSet
from simulation.experiments import DERIVED_SHOCK_PROB, calibrated, population_redraw
from simulation.model import BNPLModel
from simulation.population import (
    P3_SEED,
    load_population_frame,
    resample_population,
    stationary_separation_rate,
)

RQ0 = RESULTS_RAW / "rq0.parquet"
needs_data = pytest.mark.skipif(
    not (POPULATION_PARQUET.exists() and MATCHED_PARQUET.exists()), reason="data/processed not built"
)


def _model(**kw) -> BNPLModel:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return BNPLModel(calibrated(**kw))


def test_defaults_are_off():
    p = ParamSet()
    assert p.population_seed is None and p.bnpl_wage_income_screen is False
    assert calibrated().population_seed is None and calibrated().bnpl_wage_income_screen is False


@pytest.mark.skipif(not RQ0.exists(), reason="results/raw/rq0.parquet not present")
def test_defaults_reproduce_a_stored_rq0_row():
    from simulation.batch import run_one

    stored = pd.read_parquet(RQ0)
    row = stored[(stored.label == "bnpl_on_beta0") & (stored.seed == 10_000)].iloc[0]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        now = run_one(calibrated(bnpl_enabled=True, beta=0.0, label="bnpl_on_beta0", seed=10_000,
                                 population_seed=None, bnpl_wage_income_screen=False))
    assert now["default_rate_final"] == row["default_rate_final"]
    assert now["new_default_rate_final"] == row["new_default_rate_final"]
    # Every stored output, not only default, is reproduced exactly.
    for k, v in row.items():
        assert k in now, f"output {k} disappeared"
        w = now[k]
        if isinstance(v, float) and math.isnan(v):
            assert isinstance(w, float) and math.isnan(w), k
        else:
            assert w == v, f"{k}: stored {v!r}, now {w!r}"


@needs_data
def test_p3_step_reproduces_the_canonical_population():
    canonical = pd.read_parquet(POPULATION_PARQUET)
    pd.testing.assert_frame_equal(resample_population(P3_SEED), canonical, check_exact=True)
    # ...and so does the full frame built from it, joins, hire wages and APRs included.
    pd.testing.assert_frame_equal(load_population_frame(P3_SEED), load_population_frame(),
                                  check_exact=True)
    assert round(stationary_separation_rate(ParamSet().shock_exit_prob, P3_SEED), 5) == DERIVED_SHOCK_PROB


@needs_data
def test_screen_keeps_only_wage_households_and_the_benchmark_stream():
    bench = _model(bnpl_enabled=True, beta=0.0, seed=10_003)
    screen = _model(bnpl_enabled=True, beta=0.0, seed=10_003, bnpl_wage_income_screen=True)
    # The eligibility draw, and the minimum-payer draw after it, used the same numbers.
    assert bench.rng.getstate() == screen.rng.getstate()
    wage = {r.agent_id for r in bench.records if r.income_wage_tick > 0}
    elig_b = {a.agent_id for a in bench.agents if a.bnpl_eligible}
    elig_s = {a.agent_id for a in screen.agents if a.bnpl_eligible}
    assert elig_s == elig_b & wage
    assert all(a.rec.income_wage_tick > 0 for a in screen.agents if a.bnpl_eligible)
    assert 0 < len(elig_s) < len(elig_b)
    assert screen.n_bnpl_eligible == len(elig_s)
    # The peer-share denominators count the screened set.
    for g, members in screen.groups.items():
        assert screen.group_eligible[g] == sum(1 for i in members if i in elig_s)
    # Nothing else about the households changed.
    assert [a.is_min_payer for a in bench.agents] == [a.is_min_payer for a in screen.agents]


@needs_data
def test_population_draws_differ_between_seeds_and_repeat_on_one():
    a1, a2, b = resample_population(110_000), resample_population(110_000), resample_population(110_001)
    pd.testing.assert_frame_equal(a1, a2, check_exact=True)
    assert not a1.source_w5_hhid.equals(b.source_w5_hhid)
    m1 = _model(bnpl_enabled=False, seed=110_000, population_seed=110_000)
    m2 = _model(bnpl_enabled=False, seed=110_000, population_seed=110_000)
    m3 = _model(bnpl_enabled=False, seed=110_000, population_seed=110_001)
    assert m1.records == m2.records
    assert m1.records != m3.records


@needs_data
def test_redraw_suite_pairs_arms_and_derives_the_separation_rate_per_draw():
    sets = population_redraw(20)
    assert len(sets) == 200
    exit_prob = ParamSet().shock_exit_prob
    for off, on in zip(sets[::2], sets[1::2]):
        assert (off.seed, off.population_seed, off.shock_prob) == (on.seed, on.population_seed, on.shock_prob)
        assert off.seed == off.population_seed and not off.bnpl_enabled and on.bnpl_enabled
        assert off.shock_prob == round(stationary_separation_rate(exit_prob, off.seed), 5)
    assert sorted({p.seed for p in sets}) == list(range(110_000, 110_100))
    assert len({p.shock_prob for p in sets}) > 1
