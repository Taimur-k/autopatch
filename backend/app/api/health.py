"""
Health-check endpoint.

GET /api/health  →  200 OK with version and status information.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter(tags=["Health"])

_started_at = datetime.now(timezone.utc)


class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    timestamp: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return API health status and version information."""
    now = datetime.now(timezone.utc)
    uptime = (now - _started_at).total_seconds()
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        uptime_seconds=uptime,
        timestamp=now,
    )

