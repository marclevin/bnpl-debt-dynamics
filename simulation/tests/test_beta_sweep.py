"""Verification: the Milestone 2 beta sweep suite (issues #97 and #98)."""

from __future__ import annotations

from simulation.experiments import BETA_SWEEP_GRID, BETA_SWEEP_REPS, SUITES, beta_sweep, calibrated


def test_the_sweep_runs_the_pre_registered_grid_and_a_paired_no_bnpl_arm():
    sets = beta_sweep(reps=1)  # the replicate count is pre-registered, not taken from --reps
    labels = {p.label for p in sets}
    assert labels == {"rqb_off", *(f"rqb_b{b}" for b in BETA_SWEEP_GRID)}
    assert BETA_SWEEP_GRID[0] == 0.0 and max(BETA_SWEEP_GRID) == 0.30
    assert len(sets) == BETA_SWEEP_REPS * (len(BETA_SWEEP_GRID) + 1)
    seeds = {lab: sorted(p.seed for p in sets if p.label == lab) for lab in labels}
    assert len({tuple(s) for s in seeds.values()}) == 1  # every arm on the same seeds
    assert "rqb" in SUITES


def test_the_beta_zero_arm_is_the_ordinary_beta_zero_baseline():
    arm = next(p for p in beta_sweep(1) if p.label == "rqb_b0.0")
    assert arm == calibrated(bnpl_enabled=True, beta=0.0, label="rqb_b0.0", seed=arm.seed)
    assert arm.distress_rule == "arrears"
