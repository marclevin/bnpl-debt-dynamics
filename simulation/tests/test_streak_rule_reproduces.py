"""Verification: the old distress rule reproduces commit 6b0a4c7 bit for bit.

The fixture holds `summarise_run` rows produced at 6b0a4c7, before the arrears-based rule
(issue #92) was added. With `distress_rule="streak"` and the old baseline switches, every
numeric output must be identical. Keys added since are ignored; no stored key may change.
"""

from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import pytest

from simulation.batch import run_one
from simulation.config import ParamSet

FIXTURE = Path(__file__).parent / "fixtures" / "streak_rule_6b0a4c7.json"

#: The 6b0a4c7 baseline: labour flows, the derived separation rate, friction 0.09.
OLD_BASE = dict(n_agents=400, labour_flows=True, shock_prob=0.00446, payment_friction=0.09)

ARMS = {
    "off": dict(bnpl_enabled=False),
    "beta0": dict(bnpl_enabled=True, beta=0.0),
    "beta1": dict(bnpl_enabled=True, beta=1.0),
    "funded": dict(bnpl_enabled=True, beta=1.0, committed_shortfall_funded=True),
    "relief": dict(bnpl_enabled=True, beta=1.0, committed_shortfall_funded=True,
                   committed_shortfall_clears_distress=True),
    "k4": dict(bnpl_enabled=True, beta=1.0, k_default=4),
    "single_tick": dict(bnpl_enabled=True, beta=1.0, shock_persistent=False),
    "bureau": dict(bnpl_enabled=True, beta=1.0, bnpl_bureau_visible=True),
}


def arm_params(name: str, seed: int) -> ParamSet:
    kw = {**OLD_BASE, **ARMS[name], "seed": seed, "label": name}
    # Explicit, so the test still pins the old rule after the baseline default changes.
    if "distress_rule" in ParamSet.__dataclass_fields__:
        kw["distress_rule"] = "streak"
    return ParamSet(**kw)


@pytest.mark.parametrize("key", sorted(json.loads(FIXTURE.read_text())) if FIXTURE.exists() else [])
def test_streak_rule_reproduces_6b0a4c7(key):
    stored = json.loads(FIXTURE.read_text())[key]
    name, seed = key.split("/")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        now = run_one(arm_params(name, int(seed)))
    for k, v in stored.items():
        assert k in now, f"{key}: output {k} disappeared"
        w = now[k]
        assert (isinstance(w, float) and math.isnan(w) and math.isnan(v)) or w == v, (
            f"{key}: {k} was {v!r}, now {w!r}"
        )
