"""
Test result data structures.

TestOutcome  – pass/fail/error/skip enum for a single test case.
TestCase     – result for one individual test.
TestResults  – aggregated results for a full test-suite run.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone


class TestOutcome(str, enum.Enum):
    """Outcome of a single test case execution."""

    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


@dataclass
class TestCase:
    """Result for a single test case."""

    name: str
    outcome: TestOutcome
    duration_ms: float = 0.0
    # Failure message / traceback (populated when outcome is FAILED or ERROR).
    message: str = ""


@dataclass
class TestResults:
    """
    Aggregated results from a single test-suite run.

    Produced by TestRunner.run() and consumed by:
      - FaultLocalizer (to compute coverage-based suspiciousness)
      - RepairOrchestrator (to decide whether a patch is valid)
    """

    test_cases: list[TestCase] = field(default_factory=list)
    run_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    # Raw output from the test runner (stdout + stderr).
    raw_output: str = ""

    # ── Computed properties ───────────────────────────────────────────────────

    @property
    def passed(self) -> int:
        return sum(1 for t in self.test_cases if t.outcome == TestOutcome.PASSED)

    @property
    def failed(self) -> int:
        return sum(1 for t in self.test_cases if t.outcome == TestOutcome.FAILED)

    @property
    def errors(self) -> int:
        return sum(1 for t in self.test_cases if t.outcome == TestOutcome.ERROR)

    @property
    def skipped(self) -> int:
        return sum(1 for t in self.test_cases if t.outcome == TestOutcome.SKIPPED)

    @property
    def total(self) -> int:
        return len(self.test_cases)

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.errors == 0

    def failing_tests(self) -> list[TestCase]:
        """Return only the failed and errored test cases."""
        return [t for t in self.test_cases if t.outcome in (TestOutcome.FAILED, TestOutcome.ERROR)]

    def __str__(self) -> str:
        return (
            f"TestResults({self.passed} passed, {self.failed} failed, "
            f"{self.errors} errors, {self.skipped} skipped)"
        )

