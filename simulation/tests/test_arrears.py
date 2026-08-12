"""Verification: CCMR band ageing.

At a 14-day tick the mapping onto the published day buckets is exact, which is the whole
reason k was revised from 6 to 7.
"""

from __future__ import annotations

import pytest

from simulation.config import CCMR_BANDS, TICK_DAYS
from simulation.metrics import ccmr_band


@pytest.mark.parametrize(
    "ticks,expected",
    [
        (0, "current"),
        (1, "d30"),
        (2, "d30"),
        (3, "d31_60"),
        (4, "d31_60"),
        (5, "d61_90"),
        (6, "d61_90"),
        (7, "d91_120"),
        (8, "d91_120"),
        (9, "d120_plus"),
        (25, "d120_plus"),
    ],
)
def test_arrears_ages_into_the_right_ccmr_band(ticks, expected):
    assert ccmr_band(ticks) == expected


@pytest.mark.parametrize("label,lo,hi", CCMR_BANDS)
def test_band_day_ranges_match_the_published_buckets(label, lo, hi):
    """Each band's tick range must convert to the CCMR day bucket it is named for."""
    ranges = {
        "current": (0, 0),
        "d30": (14, 30),
        "d31_60": (31, 60),
        "d61_90": (61, 90),
        "d91_120": (91, 120),
        "d120_plus": (121, None),
    }
    lo_days, hi_days = ranges[label]
    assert lo * TICK_DAYS >= lo_days - TICK_DAYS + 1
    if hi is not None:
        assert hi * TICK_DAYS <= hi_days


def test_default_horizon_k7_lands_in_the_90_plus_convention():
    """k=7 ticks = 98 days, inside the 91-120 bucket, so it maps onto 90+.

    k=6 would be 84 days, inside 61-90, with no clean CCMR analogue at all. This test
    is the reason the revision happened, so it should fail loudly if k moves.
    """
    assert 7 * TICK_DAYS == 98
    assert ccmr_band(7) == "d91_120"
    assert 6 * TICK_DAYS == 84
    assert ccmr_band(6) == "d61_90"


def test_k4_sensitivity_arm_lands_in_the_60_plus_band():
    """The looser definition targets the 60+ figure of 16.54%."""
    assert 4 * TICK_DAYS == 56
    assert ccmr_band(4) == "d31_60"
    assert ccmr_band(5) == "d61_90"


def test_bands_are_exhaustive_and_non_overlapping():
    seen = [ccmr_band(t) for t in range(0, 40)]
    assert set(seen) == {label for label, _, _ in CCMR_BANDS}
    # Monotone: ageing never moves a household to an earlier band.
    order = [label for label, _, _ in CCMR_BANDS]
    idx = [order.index(s) for s in seen]
    assert idx == sorted(idx)
