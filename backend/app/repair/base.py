"""
Abstract base classes for the repair engine.

RepairGenerator  – generates candidate patches from code context + fault info.
PatchRanker      – ranks a list of candidate patches.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PatchCandidate:
    """
    An in-memory representation of a candidate patch.

    This is distinct from the SQLAlchemy ORM model (models/patch.py);
    the orchestrator works with these lightweight dataclasses and the
    service layer persists them to the database.
    """

    id: str
    description: str
    diff: str
    model_score: float = 0.0
    test_status: str = "PENDING"
    final_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class RepairGenerator(ABC):
    """
    Abstract base class for patch generation engines.

    Implement this to add LLM-based, template-based, or genetic
    program repair generators.
    """

    @abstractmethod
    async def generate(
        self,
        code_context: str,
        fault_locations: list[Any],
        max_patches: int = 5,
    ) -> list[PatchCandidate]:
        """
        Generate candidate patches for the given fault locations.

        Args:
            code_context:    Relevant source code retrieved around the fault.
            fault_locations: Ranked list of FaultLocation objects.
            max_patches:     Maximum number of patches to generate.

        Returns:
            List of PatchCandidate objects (unvalidated).
        """
        ...


class PatchRanker(ABC):
    """
    Abstract base class for patch ranking strategies.

    Implement this to add ML-based, heuristic, or human-in-the-loop
    patch rankers.
    """

    @abstractmethod
    async def rank(
        self, candidates: list[PatchCandidate]
    ) -> list[PatchCandidate]:
        """
        Rank patches from best to worst and return the sorted list.

        Args:
            candidates: Unranked list of PatchCandidate objects.

        Returns:
            The same list sorted by final_score descending.
        """
        ...

