"""
RepairService – business logic for repair run lifecycle management.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repair_run import RepairRun, RepairStatus


class RepairService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create_run(self, *, issue_id: str) -> RepairRun:
        """Create a new RepairRun in PENDING state."""
        run = RepairRun(issue_id=issue_id, status=RepairStatus.PENDING)
        self._db.add(run)
        await self._db.commit()
        await self._db.refresh(run)
        # TODO: dispatch run to the background orchestrator task queue.
        return run

    async def get_run(self, run_id: str) -> RepairRun | None:
        """Return a RepairRun by primary key, or None if not found."""
        result = await self._db.execute(
            select(RepairRun).where(RepairRun.id == run_id)
        )
        return result.scalar_one_or_none()

    async def list_runs(self) -> list[RepairRun]:
        """Return all repair runs ordered by start time."""
        result = await self._db.execute(
            select(RepairRun).order_by(RepairRun.started_at.desc())
        )
        return list(result.scalars().all())

    async def update_status(
        self,
        run_id: str,
        status: RepairStatus,
    ) -> RepairRun | None:
        """Update the status of an existing run."""
        run = await self.get_run(run_id)
        if run is None:
            return None
        run.status = status
        await self._db.commit()
        await self._db.refresh(run)
        return run

