"""
Abstract base class for fault localisers.

Implement this interface to add new fault localisation algorithms
(e.g. Ochiai, Tarantula, SBFL, MBFL, LLM-based).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class FaultLocation:
    """
    A single suspicious code location returned by a fault localiser.

    Attributes:
        file:                  Relative path to the source file.
        line:                  1-based line number of the suspicious statement.
        function:              Name of the enclosing function / method (optional).
        suspiciousness_score:  Float in [0, 1]; higher = more suspicious.
    """

    file: str
    line: int
    function: str | None
    suspiciousness_score: float

    def __str__(self) -> str:
        location = f"{self.file}:{self.line}"
        if self.function:
            location += f" ({self.function})"
        return f"{location}  score={self.suspiciousness_score:.3f}"


class FaultLocalizer(ABC):
    """
    Abstract base class for fault localisation components.

    All fault localisation algorithms must implement this interface so
    that the orchestrator can swap them without code changes.
    """

    @abstractmethod
    async def localize(
        self,
        repository: str,
        test_results: Any,
    ) -> list[FaultLocation]:
        """
        Identify suspicious code locations given a repository and test results.

        Args:
            repository:   Local filesystem path to the cloned repository.
            test_results: Output of the test runner (TestResults instance).

        Returns:
            A list of FaultLocation objects sorted by suspiciousness_score
            descending (most suspicious first).
        """
        ...

