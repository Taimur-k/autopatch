"""
Tests for OchiaiFaultLocalizer.
"""

from __future__ import annotations

import math

import pytest

from app.fault_localization.base import FaultLocation
from app.fault_localization.ochiai import OchiaiFaultLocalizer


@pytest.fixture
def localizer() -> OchiaiFaultLocalizer:
    return OchiaiFaultLocalizer()


def test_ochiai_score_known_values() -> None:
    """Verify the Ochiai formula against a hand-computed example."""
    # ef=8, ep=1, nf=2  →  8 / sqrt(10 * 9) = 8 / sqrt(90)
    score = OchiaiFaultLocalizer.ochiai_score(ef=8, ep=1, nf=2)
    expected = 8 / math.sqrt(10 * 9)
    assert abs(score - expected) < 1e-9


def test_ochiai_score_zero_denominator() -> None:
    """Score should be 0.0 when denominator is zero (no executions at all)."""
    score = OchiaiFaultLocalizer.ochiai_score(ef=0, ep=0, nf=0)
    assert score == 0.0


def test_ochiai_score_all_failing() -> None:
    """Element executed by all failing tests and no passing tests → score = 1.0."""
    score = OchiaiFaultLocalizer.ochiai_score(ef=5, ep=0, nf=0)
    assert abs(score - 1.0) < 1e-9


@pytest.mark.anyio
async def test_localize_returns_list(localizer: OchiaiFaultLocalizer) -> None:
    """localize() should return a non-empty list of FaultLocation objects."""
    results = await localizer.localize(repository="/fake/repo", test_results=None)
    assert isinstance(results, list)
    assert len(results) > 0


@pytest.mark.anyio
async def test_localize_returns_fault_locations(localizer: OchiaiFaultLocalizer) -> None:
    """Every item returned should be a FaultLocation."""
    results = await localizer.localize(repository="/fake/repo", test_results=None)
    for loc in results:
        assert isinstance(loc, FaultLocation)


@pytest.mark.anyio
async def test_localize_scores_in_range(localizer: OchiaiFaultLocalizer) -> None:
    """All suspiciousness scores should be in [0, 1]."""
    results = await localizer.localize(repository="/fake/repo", test_results=None)
    for loc in results:
        assert 0.0 <= loc.suspiciousness_score <= 1.0

