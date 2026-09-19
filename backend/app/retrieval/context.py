"""
Context builder.

Assembles multiple code snippets and metadata into a single formatted
string suitable for use in an LLM prompt.
"""

from __future__ import annotations

from typing import Any


class ContextBuilder:
    """
    Constructs a structured context document from code snippets,
    fault locations, and test information.

    Usage::

        builder = ContextBuilder()
        builder.add_issue(title="NullPointerException in login", description="…")
        builder.add_fault_location(file="auth.py", line=42, snippet="…")
        builder.add_test_failure(name="test_login", output="…")
        context = builder.build()
    """

    def __init__(self) -> None:
        self._sections: list[str] = []

    def add_issue(self, title: str, description: str) -> "ContextBuilder":
        """Add the bug report / issue section."""
        self._sections.append(
            f"## Issue: {title}\n\n{description}"
        )
        return self

    def add_fault_location(
        self,
        file: str,
        line: int,
        snippet: str,
        score: float | None = None,
    ) -> "ContextBuilder":
        """Add a suspicious code location with its source snippet."""
        header = f"## Suspicious Location: {file}:{line}"
        if score is not None:
            header += f"  (score={score:.3f})"
        self._sections.append(f"{header}\n\n```python\n{snippet}\n```")
        return self

    def add_test_failure(self, name: str, output: str) -> "ContextBuilder":
        """Add a failing test and its output."""
        self._sections.append(
            f"## Failing Test: {name}\n\n```\n{output}\n```"
        )
        return self

    def add_raw(self, content: str) -> "ContextBuilder":
        """Add an arbitrary section of text."""
        self._sections.append(content)
        return self

    def build(self) -> str:
        """Return the fully assembled context string."""
        return "\n\n---\n\n".join(self._sections)

