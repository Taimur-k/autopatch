"""
IssueService – business logic for creating and retrieving issues.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.issue import Issue


class IssueService:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(
        self,
        *,
        title: str,
        description: str,
        repository_url: str,
        github_issue_url: str | None = None,
    ) -> Issue:
        """Persist a new Issue and return it."""
        issue = Issue(
            title=title,
            description=description,
            repository_url=repository_url,
            github_issue_url=github_issue_url,
        )
        self._db.add(issue)
        await self._db.commit()
        await self._db.refresh(issue)
        return issue

    async def get(self, issue_id: str) -> Issue | None:
        """Return an Issue by primary key, or None if not found."""
        result = await self._db.execute(
            select(Issue).where(Issue.id == issue_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Issue]:
        """Return all issues ordered by creation date."""
        result = await self._db.execute(
            select(Issue).order_by(Issue.created_at.desc())
        )
        return list(result.scalars().all())

