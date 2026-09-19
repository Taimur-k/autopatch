"""
FastAPI application factory.

Mounts all API routers, configures CORS middleware, and initialises the
database on startup.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, issues, repositories, runs
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[type-arg]
    """Run startup and shutdown tasks."""
    await init_db()
    yield
    # Shutdown logic goes here (e.g. close external connections).


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="AutoPatch API",
        description="AI-powered automated program repair system.",
        version=settings.APP_VERSION,
        lifespan=lifespan,
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(health.router, prefix="/api")
    app.include_router(issues.router, prefix="/api")
    app.include_router(runs.router, prefix="/api")
    app.include_router(repositories.router, prefix="/api")

    return app


app = create_app()

