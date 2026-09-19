"""
Repository management interfaces.

RepositoryManager  – abstract base class for cloning, resetting, and
                     querying local repositories.
LocalRepositoryManager  – stub implementation using subprocess git calls.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RepoInfo:
    """Metadata about a locally cloned repository."""

    path: str
    url: str
    branch: str
    commit_sha: str


class RepositoryManager(ABC):
    """
    Abstract base class for repository lifecycle management.

    Implementations should handle cloning, branch checkout,
    patch application, and clean-up.
    """

    @abstractmethod
    async def clone(self, url: str, destination: str, branch: str = "main") -> RepoInfo:
        """Clone a remote repository to a local destination."""
        ...

    @abstractmethod
    async def apply_patch(self, repo_path: str, diff: str) -> None:
        """Apply a unified diff patch to the repository working tree."""
        ...

    @abstractmethod
    async def revert_patch(self, repo_path: str) -> None:
        """Revert all uncommitted changes in the working tree."""
        ...

    @abstractmethod
    async def get_info(self, repo_path: str) -> RepoInfo:
        """Return metadata about the repository at the given path."""
        ...


class LocalRepositoryManager(RepositoryManager):
    """
    Manages repositories on the local filesystem using git subprocess calls.

    TODO: Implement each method using asyncio.create_subprocess_exec
          to run git commands without blocking the event loop.
    """

    async def clone(self, url: str, destination: str, branch: str = "main") -> RepoInfo:
        """TODO: Run `git clone --branch <branch> <url> <destination>`."""
        return RepoInfo(path=destination, url=url, branch=branch, commit_sha="placeholder-sha")

    async def apply_patch(self, repo_path: str, diff: str) -> None:
        """TODO: Write diff to a temp file and run `git apply <file>`."""
        pass

    async def revert_patch(self, repo_path: str) -> None:
        """TODO: Run `git checkout -- .` to discard working-tree changes."""
        pass

    async def get_info(self, repo_path: str) -> RepoInfo:
        """TODO: Run `git remote get-url origin` and `git rev-parse HEAD`."""
        return RepoInfo(
            path=repo_path,
            url="",
            branch="main",
            commit_sha="placeholder-sha",
        )

