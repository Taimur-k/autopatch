"""
SQLAlchemy ORM model for RepairRun.

A RepairRun represents one full execution of the AutoPatch pipeline
for a given issue.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RepairStatus(str, enum.Enum):
    """High-level lifecycle status of a repair run."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class RepairStage(str, enum.Enum):
    """Fine-grained pipeline stage the orchestrator is currently in."""

    INITIALIZING = "INITIALIZING"
    RUNNING_TESTS = "RUNNING_TESTS"
    LOCALIZING_FAULT = "LOCALIZING_FAULT"
    RETRIEVING_CONTEXT = "RETRIEVING_CONTEXT"
    GENERATING_PATCH = "GENERATING_PATCH"
    VALIDATING_PATCH = "VALIDATING_PATCH"
    RANKING_PATCH = "RANKING_PATCH"
    COMPLETED = "COMPLETED"


class RepairRun(Base):
    """One full AutoPatch repair pipeline execution."""

    __tablename__ = "repair_runs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    issue_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("issues.id"), nullable=False
    )
    status: Mapped[RepairStatus] = mapped_column(
        Enum(RepairStatus), default=RepairStatus.PENDING, nullable=False
    )
    current_stage: Mapped[RepairStage] = mapped_column(
        Enum(RepairStage), default=RepairStage.INITIALIZING, nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    issue: Mapped["Issue"] = relationship("Issue", back_populates="repair_runs")  # noqa: F821
    patches: Mapped[list["PatchCandidate"]] = relationship(  # noqa: F821
        "PatchCandidate", back_populates="run", cascade="all, delete-orphan"
    )
    tool_calls: Mapped[list["ToolCall"]] = relationship(  # noqa: F821
        "ToolCall", back_populates="run", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<RepairRun id={self.id!r} status={self.status}>"

