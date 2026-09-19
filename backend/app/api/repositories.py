"""
Repositories API router.

POST /api/repositories              – Register a repository
GET  /api/repositories/{repo_id}    – Retrieve a repository by ID
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.repository_service import RepositoryService

router = APIRouter(prefix="/repositories", tags=["Repositories"])


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class RepositoryCreate(BaseModel):
    name: str
    url: str
    default_branch: str = "main"


class RepositoryResponse(BaseModel):
    id: str
    name: str
    url: str
    local_path: str | None
    default_branch: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=RepositoryResponse, status_code=201)
async def create_repository(
    payload: RepositoryCreate,
    db: AsyncSession = Depends(get_db),
) -> RepositoryResponse:
    """Register a new repository."""
    service = RepositoryService(db)
    repo = await service.create(
        name=payload.name,
        url=payload.url,
        default_branch=payload.default_branch,
    )
    return RepositoryResponse.model_validate(repo)


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
) -> RepositoryResponse:
    """Retrieve a repository by ID."""
    service = RepositoryService(db)
    repo = await service.get(repo_id)
    if repo is None:
        raise HTTPException(status_code=404, detail=f"Repository '{repo_id}' not found.")
    return RepositoryResponse.model_validate(repo)

