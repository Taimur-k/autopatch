"""
SQLAlchemy ORM model for ToolCall.

Records every tool/function invocation the orchestrator makes during a run,
useful for debugging and auditing.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ToolCall(Base):
    """Audit log of a single tool call made during a repair run."""

    __tablename__ = "tool_calls"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    run_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("repair_runs.id"), nullable=False
    )
    # Pipeline stage during which this tool was called.
    stage: Mapped[str] = mapped_column(String(100), nullable=False)
    # Name of the tool / function.
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # JSON-serialised input arguments.
    input_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON-serialised output / result.
    output_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    run: Mapped["RepairRun"] = relationship("RepairRun", back_populates="tool_calls")  # noqa: F821

    def __repr__(self) -> str:
        return f"<ToolCall id={self.id!r} name={self.name!r} stage={self.stage!r}>"

