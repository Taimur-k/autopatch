"""
GitHub API client interfaces.

GitHubClient  – abstract base class for GitHub operations.
GitHubAPIClient  – stub implementation that will use the GitHub REST API.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PullRequest:
    """Represents a created GitHub pull request."""

    number: int
    url: str
    title: str
    branch: str


class GitHubClient(ABC):
    """
    Abstract base class for GitHub integration.

    Implement this to support pull-request creation, issue commenting,
    and repository metadata retrieval via the GitHub REST API.
    """

    @abstractmethod
    async def create_pull_request(
        self,
        *,
        repo: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> PullRequest:
        """
        Create a pull request on GitHub.

        Args:
            repo:         Full repository name, e.g. "owner/repo".
            title:        PR title.
            body:         PR description (Markdown).
            head_branch:  Branch containing the patch.
            base_branch:  Target branch (usually "main" or "master").

        Returns:
            PullRequest with the PR number and URL.
        """
        ...

    @abstractmethod
    async def comment_on_issue(
        self,
        *,
        repo: str,
        issue_number: int,
        body: str,
    ) -> None:
        """Post a comment on a GitHub issue."""
        ...


class GitHubAPIClient(GitHubClient):
    """
    GitHub REST API client using httpx.

    TODO: Implement each method using httpx.AsyncClient with the
          GITHUB_TOKEN from settings for authentication.
          Base URL: https://api.github.com
    """

    async def create_pull_request(
        self,
        *,
        repo: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> PullRequest:
        """TODO: POST /repos/{repo}/pulls"""
        return PullRequest(
            number=0,
            url=f"https://github.com/{repo}/pull/0",
            title=title,
            branch=head_branch,
        )

    async def comment_on_issue(
        self,
        *,
        repo: str,
        issue_number: int,
        body: str,
    ) -> None:
        """TODO: POST /repos/{repo}/issues/{issue_number}/comments"""
        pass

