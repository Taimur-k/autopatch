"""
RepositoryService – business logic for repository registration and lookup.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(
        self,
        *,
        name: str,
        url: str,
        default_branch: str = "main",
    ) -> Repository:
        """Register a new repository."""
        repo = Repository(name=name, url=url, default_branch=default_branch)
        self._db.add(repo)
        await self._db.commit()
        await self._db.refresh(repo)
        return repo

    async def get(self, repo_id: str) -> Repository | None:
        """Return a Repository by primary key, or None if not found."""
        result = await self._db.execute(
            select(Repository).where(Repository.id == repo_id)
        )
        return result.scalar_one_or_none()

    async def get_by_url(self, url: str) -> Repository | None:
        """Return a Repository by its URL."""
        result = await self._db.execute(
            select(Repository).where(Repository.url == url)
        )
        return result.scalar_one_or_none()

    async def set_local_path(self, repo_id: str, path: str) -> Repository | None:
        """Record the local filesystem clone path for a repository."""
        repo = await self.get(repo_id)
        if repo is None:
            return None
        repo.local_path = path
        await self._db.commit()
        await self._db.refresh(repo)
        return repo

