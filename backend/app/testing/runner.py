"""
Test runner interfaces.

TestRunner  – abstract base class for test execution backends.
PytestRunner  – stub implementation that will invoke pytest as a subprocess.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.testing.results import TestCase, TestOutcome, TestResults


class TestRunner(ABC):
    """
    Abstract base class for test execution engines.

    Implement this to support different test frameworks (pytest, unittest,
    Maven, Gradle, cargo test, etc.).
    """

    @abstractmethod
    async def run(self, repository_path: str) -> TestResults:
        """
        Execute the test suite at the given repository path.

        Args:
            repository_path: Absolute filesystem path to the repository root.

        Returns:
            TestResults with per-test outcomes and raw output.
        """
        ...


class PytestRunner(TestRunner):
    """
    Runs pytest as a subprocess and parses its JSON output.

    TODO: Implement with subprocess / asyncio.create_subprocess_exec:
      1. Run: pytest --tb=short --json-report --json-report-file=- <repo_path>
      2. Parse JSON report into TestResults.
      3. Handle timeouts and subprocess errors gracefully.
    """

    async def run(self, repository_path: str) -> TestResults:
        """
        Return placeholder TestResults.

        Replace this body with a real subprocess call to pytest.
        """
        # ── Placeholder results ────────────────────────────────────────────
        return TestResults(
            test_cases=[
                TestCase(name="test_parse_simple", outcome=TestOutcome.PASSED, duration_ms=12.3),
                TestCase(name="test_parse_empty", outcome=TestOutcome.PASSED, duration_ms=5.1),
                TestCase(name="test_parse_nested", outcome=TestOutcome.PASSED, duration_ms=18.7),
                TestCase(name="test_parse_boundary", outcome=TestOutcome.FAILED, duration_ms=8.2, message="IndexError: list index out of range"),
                TestCase(name="test_service_none_input", outcome=TestOutcome.FAILED, duration_ms=3.4, message="AttributeError: 'NoneType' object has no attribute 'data'"),
                TestCase(name="test_validate_empty", outcome=TestOutcome.PASSED, duration_ms=2.1),
                TestCase(name="test_health_endpoint", outcome=TestOutcome.PASSED, duration_ms=45.0),
            ],
            raw_output="[placeholder] pytest output will appear here.",
        )

