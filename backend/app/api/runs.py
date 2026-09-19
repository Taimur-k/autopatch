"""
Repair Runs API router.

POST /api/repair-runs                           – Start a new repair run
GET  /api/repair-runs/{run_id}                  – Get run summary
GET  /api/repair-runs/{run_id}/timeline         – Get pipeline timeline events
GET  /api/repair-runs/{run_id}/fault-locations  – Get fault localisation results
GET  /api/repair-runs/{run_id}/patches          – Get candidate patches
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.repair_run import RepairStage, RepairStatus
from app.services.repair_service import RepairService

router = APIRouter(prefix="/repair-runs", tags=["Repair Runs"])


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class RepairRunCreate(BaseModel):
    issue_id: str


class RepairRunResponse(BaseModel):
    id: str
    issue_id: str
    status: RepairStatus
    current_stage: RepairStage
    started_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class TimelineEvent(BaseModel):
    timestamp: datetime
    stage: str
    message: str
    metadata: dict | None = None


class FaultLocation(BaseModel):
    file: str
    line: int
    function: str | None
    suspiciousness_score: float


class PatchCandidateResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    id: str
    description: str
    diff: str
    model_score: float
    test_status: str
    final_score: float


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=RepairRunResponse, status_code=201)
async def create_repair_run(
    payload: RepairRunCreate,
    db: AsyncSession = Depends(get_db),
) -> RepairRunResponse:
    """Create and queue a new repair run for the given issue."""
    service = RepairService(db)
    run = await service.create_run(issue_id=payload.issue_id)
    return RepairRunResponse.model_validate(run)


@router.get("/{run_id}", response_model=RepairRunResponse)
async def get_repair_run(
    run_id: str,
    db: AsyncSession = Depends(get_db),
) -> RepairRunResponse:
    """Retrieve summary for a single repair run."""
    service = RepairService(db)
    run = await service.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Repair run '{run_id}' not found.")
    return RepairRunResponse.model_validate(run)


@router.get("/{run_id}/timeline", response_model=list[TimelineEvent])
async def get_timeline(run_id: str) -> list[TimelineEvent]:
    """Return ordered pipeline timeline events (mock data for now)."""
    now = datetime.now(timezone.utc)
    return [
        TimelineEvent(timestamp=now, stage="INITIALIZING", message="Cloning repository…"),
        TimelineEvent(timestamp=now, stage="RUNNING_TESTS", message="Running test suite — 26 tests found."),
        TimelineEvent(timestamp=now, stage="LOCALIZING_FAULT", message="Applying Ochiai fault localisation…"),
        TimelineEvent(timestamp=now, stage="RETRIEVING_CONTEXT", message="Fetching relevant code context."),
        TimelineEvent(timestamp=now, stage="GENERATING_PATCH", message="Generating 3 candidate patches."),
        TimelineEvent(timestamp=now, stage="VALIDATING_PATCH", message="Validating patches against test suite."),
        TimelineEvent(timestamp=now, stage="RANKING_PATCH", message="Ranking patches by score."),
        TimelineEvent(timestamp=now, stage="COMPLETED", message="Best patch selected. Ready for review."),
    ]


@router.get("/{run_id}/fault-locations", response_model=list[FaultLocation])
async def get_fault_locations(run_id: str) -> list[FaultLocation]:
    """Return fault localisation results (mock data for now)."""
    return [
        FaultLocation(file="src/parser.py", line=42, function="parse_expression", suspiciousness_score=0.91),
        FaultLocation(file="src/service.py", line=88, function="process_request", suspiciousness_score=0.82),
        FaultLocation(file="src/api.py", line=31, function="handle_input", suspiciousness_score=0.71),
        FaultLocation(file="src/utils.py", line=17, function="validate", suspiciousness_score=0.55),
    ]


@router.get("/{run_id}/patches", response_model=list[PatchCandidateResponse])
async def get_patches(run_id: str) -> list[PatchCandidateResponse]:
    """Return candidate patches generated for this run (mock data for now)."""
    return [
        PatchCandidateResponse(
            id="patch-1",
            description="Fix off-by-one error in parse_expression boundary check.",
            diff='--- a/src/parser.py\n+++ b/src/parser.py\n@@ -40,7 +40,7 @@\n     if index >= len(tokens):\n-        raise IndexError("index out of range")\n+        return None\n',
            model_score=0.88,
            test_status="PASSED",
            final_score=0.91,
        ),
        PatchCandidateResponse(
            id="patch-2",
            description="Add guard clause to process_request for None input.",
            diff='--- a/src/service.py\n+++ b/src/service.py\n@@ -86,6 +86,8 @@\n def process_request(req):\n+    if req is None:\n+        return {}\n     data = req.data\n',
            model_score=0.74,
            test_status="FAILED",
            final_score=0.62,
        ),
        PatchCandidateResponse(
            id="patch-3",
            description="Initialise default value before conditional assignment.",
            diff='--- a/src/utils.py\n+++ b/src/utils.py\n@@ -15,6 +15,7 @@\n def validate(value):\n+    result = None\n     if value:\n         result = value.strip()\n',
            model_score=0.61,
            test_status="PASSED",
            final_score=0.70,
        ),
    ]

