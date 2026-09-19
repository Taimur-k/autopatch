"""
Ochiai fault localiser.

The Ochiai coefficient is a spectrum-based fault localisation (SBFL) metric.
For each program element e, given:
    ef = number of failing tests that execute e
    ep = number of passing tests that execute e
    nf = number of failing tests that do NOT execute e

The Ochiai suspiciousness score is:

    ochiai(e) = ef / sqrt((ef + nf) * (ef + ep))

Reference:
    Abreu et al., "An Evaluation of Similarity Coefficients for Software
    Fault Localization", PRDC 2006.

Current implementation: returns placeholder data.
Replace the body of `localize` with real coverage-matrix computation.
"""

from __future__ import annotations

import math
from typing import Any

from app.fault_localization.base import FaultLocalizer, FaultLocation


class OchiaiFaultLocalizer(FaultLocalizer):
    """
    SBFL fault localiser using the Ochiai similarity coefficient.

    To implement:
    1. Parse the test-coverage matrix produced by coverage.py or pytest-cov.
    2. For each executable statement, compute ef, ep, nf counts.
    3. Apply the Ochiai formula and sort descending.
    """

    @staticmethod
    def ochiai_score(ef: int, ep: int, nf: int) -> float:
        """
        Compute the Ochiai suspiciousness score for a single program element.

        Args:
            ef: Failing tests that execute this element.
            ep: Passing tests that execute this element.
            nf: Failing tests that do NOT execute this element.

        Returns:
            Float in [0, 1]; returns 0.0 when denominator is zero.
        """
        denominator = math.sqrt((ef + nf) * (ef + ep))
        if denominator == 0.0:
            return 0.0
        return ef / denominator

    async def localize(
        self,
        repository: str,
        test_results: Any,
    ) -> list[FaultLocation]:
        """
        Localise faults using the Ochiai coefficient.

        TODO: Replace placeholder data with real coverage-matrix analysis.
              Steps:
              1. Run `pytest --cov=<src> --cov-report=json` inside repository.
              2. Parse coverage.json to build the coverage matrix.
              3. Compute ochiai_score() for every executed statement.
              4. Return sorted FaultLocation list.
        """
        # ── Placeholder: return mock fault locations ───────────────────────
        return [
            FaultLocation(
                file="src/parser.py",
                line=42,
                function="parse_expression",
                suspiciousness_score=self.ochiai_score(ef=8, ep=1, nf=2),
            ),
            FaultLocation(
                file="src/service.py",
                line=88,
                function="process_request",
                suspiciousness_score=self.ochiai_score(ef=7, ep=2, nf=3),
            ),
            FaultLocation(
                file="src/api.py",
                line=31,
                function="handle_input",
                suspiciousness_score=self.ochiai_score(ef=6, ep=3, nf=4),
            ),
            FaultLocation(
                file="src/utils.py",
                line=17,
                function="validate",
                suspiciousness_score=self.ochiai_score(ef=4, ep=5, nf=6),
            ),
        ]

