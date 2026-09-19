"""
Tests for the repair engine (generator and ranker).
"""

from __future__ import annotations

import pytest

from app.repair.base import PatchCandidate
from app.repair.generator import LLMRepairGenerator
from app.repair.ranker import HeuristicPatchRanker


@pytest.fixture
def generator() -> LLMRepairGenerator:
    return LLMRepairGenerator()


@pytest.fixture
def ranker() -> HeuristicPatchRanker:
    return HeuristicPatchRanker()


# ── Generator tests ───────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_generator_returns_list(generator: LLMRepairGenerator) -> None:
    results = await generator.generate(code_context="", fault_locations=[], max_patches=3)
    assert isinstance(results, list)


@pytest.mark.anyio
async def test_generator_respects_max_patches(generator: LLMRepairGenerator) -> None:
    results = await generator.generate(code_context="", fault_locations=[], max_patches=2)
    assert len(results) <= 2


@pytest.mark.anyio
async def test_generator_returns_patch_candidates(generator: LLMRepairGenerator) -> None:
    results = await generator.generate(code_context="", fault_locations=[], max_patches=5)
    for patch in results:
        assert isinstance(patch, PatchCandidate)
        assert patch.id
        assert patch.diff


# ── Ranker tests ──────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_ranker_sorts_by_final_score(ranker: HeuristicPatchRanker) -> None:
    candidates = [
        PatchCandidate(id="a", description="A", diff="", model_score=0.5, test_status="PASSED"),
        PatchCandidate(id="b", description="B", diff="", model_score=0.9, test_status="PASSED"),
        PatchCandidate(id="c", description="C", diff="", model_score=0.3, test_status="FAILED"),
    ]
    ranked = await ranker.rank(candidates)
    scores = [p.final_score for p in ranked]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.anyio
async def test_ranker_passed_beats_failed(ranker: HeuristicPatchRanker) -> None:
    """A patch that passes tests should rank above one that fails, even with lower model_score."""
    candidates = [
        PatchCandidate(id="pass", description="", diff="", model_score=0.5, test_status="PASSED"),
        PatchCandidate(id="fail", description="", diff="", model_score=0.6, test_status="FAILED"),
    ]
    ranked = await ranker.rank(candidates)
    assert ranked[0].id == "pass"


@pytest.mark.anyio
async def test_ranker_empty_list(ranker: HeuristicPatchRanker) -> None:
    ranked = await ranker.rank([])
    assert ranked == []

