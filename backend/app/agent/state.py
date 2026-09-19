"""
Agent state definitions.

RepairStage  – fine-grained pipeline stage enum.
RepairState  – immutable snapshot of the orchestrator's current state,
               passed between pipeline steps.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


class RepairStage(str, enum.Enum):
    """Ordered pipeline stages for the AutoPatch repair orchestrator."""

    INITIALIZING = "INITIALIZING"
    RUNNING_TESTS = "RUNNING_TESTS"
    LOCALIZING_FAULT = "LOCALIZING_FAULT"
    RETRIEVING_CONTEXT = "RETRIEVING_CONTEXT"
    GENERATING_PATCH = "GENERATING_PATCH"
    VALIDATING_PATCH = "VALIDATING_PATCH"
    RANKING_PATCH = "RANKING_PATCH"
    COMPLETED = "COMPLETED"


# Ordered list of stages for progress tracking.
STAGE_ORDER: list[RepairStage] = [
    RepairStage.INITIALIZING,
    RepairStage.RUNNING_TESTS,
    RepairStage.LOCALIZING_FAULT,
    RepairStage.RETRIEVING_CONTEXT,
    RepairStage.GENERATING_PATCH,
    RepairStage.VALIDATING_PATCH,
    RepairStage.RANKING_PATCH,
    RepairStage.COMPLETED,
]


@dataclass
class TimelineEntry:
    """A single timestamped event emitted by the orchestrator."""

    stage: RepairStage
    message: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RepairState:
    """
    Mutable state object threaded through the repair pipeline.

    Each pipeline step receives this object, mutates it, and returns it.
    """

    run_id: str
    issue_id: str

    # Repository info
    repository_url: str = ""
    local_repo_path: str = ""

    # Current pipeline position
    current_stage: RepairStage = RepairStage.INITIALIZING

    # Test results (populated after RUNNING_TESTS)
    test_results: Any = None

    # Fault locations (populated after LOCALIZING_FAULT)
    fault_locations: list[Any] = field(default_factory=list)

    # Retrieved code context (populated after RETRIEVING_CONTEXT)
    code_context: str = ""

    # Generated patches (populated after GENERATING_PATCH)
    patch_candidates: list[Any] = field(default_factory=list)

    # Best patch selected after ranking
    best_patch: Any = None

    # Full ordered timeline of events
    timeline: list[TimelineEntry] = field(default_factory=list)

    def emit(self, message: str, **metadata: Any) -> None:
        """Add a timestamped event to the timeline."""
        self.timeline.append(
            TimelineEntry(
                stage=self.current_stage,
                message=message,
                metadata=metadata,
            )
        )

