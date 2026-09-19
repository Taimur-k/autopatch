"""
Code retrieval interfaces.

CodeRetriever  – abstract base class for code search strategies.
SimpleCodeRetriever  – stub implementation using filesystem walks.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CodeRetriever(ABC):
    """
    Abstract base class for code retrieval components.

    Implementations should return relevant source-code snippets
    around the identified fault locations so the repair engine
    has enough context to generate accurate patches.
    """

    @abstractmethod
    async def retrieve(
        self,
        repository: str,
        fault_locations: list[Any],
        context_lines: int = 20,
    ) -> str:
        """
        Retrieve code context around the given fault locations.

        Args:
            repository:      Local filesystem path to the cloned repository.
            fault_locations: List of FaultLocation objects.
            context_lines:   Number of lines of context to include around
                             each fault location.

        Returns:
            A single formatted string containing all relevant code snippets,
            suitable for inclusion in an LLM prompt.
        """
        ...


class SimpleCodeRetriever(CodeRetriever):
    """
    Stub code retriever that reads lines from the filesystem.

    TODO: Replace with a smarter retriever that uses:
      - Tree-sitter AST parsing to extract whole function bodies.
      - Embedding-based semantic search across the codebase.
      - Call-graph analysis to include caller/callee context.
    """

    async def retrieve(
        self,
        repository: str,
        fault_locations: list[Any],
        context_lines: int = 20,
    ) -> str:
        """
        Return placeholder context string.

        Replace this body with real file-reading logic.
        """
        if not fault_locations:
            return ""

        # ── Placeholder ────────────────────────────────────────────────────
        parts: list[str] = []
        for loc in fault_locations:
            file_path = getattr(loc, "file", "unknown")
            line = getattr(loc, "line", 0)
            func = getattr(loc, "function", None)
            parts.append(
                f"# {file_path} (line {line}"
                + (f", function: {func}" if func else "")
                + ")\n"
                + "# [source code will be loaded here]\n"
            )
        return "\n".join(parts)

