"""
Issues API router.

POST /api/issues              – Create a new issue
GET  /api/issues/{issue_id}   – Retrieve an issue by ID
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.issue_service import IssueService

router = APIRouter(prefix="/issues", tags=["Issues"])


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class IssueCreate(BaseModel):
    title: str
    description: str
    repository_url: str
    github_issue_url: str | None = None


class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    repository_url: str
    github_issue_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=IssueResponse, status_code=201)
async def create_issue(
    payload: IssueCreate,
    db: AsyncSession = Depends(get_db),
) -> IssueResponse:
    """Create a new issue and persist it to the database."""
    service = IssueService(db)
    issue = await service.create(
        title=payload.title,
        description=payload.description,
        repository_url=payload.repository_url,
        github_issue_url=payload.github_issue_url,
    )
    return IssueResponse.model_validate(issue)


@router.get("/{issue_id}", response_model=IssueResponse)
async def get_issue(
    issue_id: str,
    db: AsyncSession = Depends(get_db),
) -> IssueResponse:
    """Retrieve a single issue by its ID."""
    service = IssueService(db)
    issue = await service.get(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail=f"Issue '{issue_id}' not found.")
    return IssueResponse.model_validate(issue)

