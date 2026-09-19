"""
Heuristic patch ranker (stub implementation).

Implements PatchRanker by computing a final_score from available signals:
model_score and test_status. More sophisticated features (code smell metrics,
AST complexity, semantic similarity) can be added later.
"""

from __future__ import annotations

from app.repair.base import PatchCandidate, PatchRanker

# Weight of model_score vs test bonus in final_score calculation.
_MODEL_WEIGHT = 0.6
_TEST_BONUS = 0.4   # Added when patch passes tests.


class HeuristicPatchRanker(PatchRanker):
    """
    Ranks patches using a simple weighted combination of:
      - model_score   (from the LLM's self-assessed confidence)
      - test_bonus    (whether the patch passes the test suite)

    final_score = model_score * MODEL_WEIGHT + test_bonus * TEST_WEIGHT

    TODO: Extend with richer features:
      - Edit distance from the fault location
      - AST complexity delta
      - Code naturalness score (n-gram language model)
      - Human preference data (RLHF)
    """

    async def rank(self, candidates: list[PatchCandidate]) -> list[PatchCandidate]:
        """Compute final_score for each candidate and sort descending."""
        for patch in candidates:
            test_bonus = _TEST_BONUS if patch.test_status == "PASSED" else 0.0
            patch.final_score = patch.model_score * _MODEL_WEIGHT + test_bonus

        return sorted(candidates, key=lambda p: p.final_score, reverse=True)

