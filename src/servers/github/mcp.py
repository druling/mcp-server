import json
import logging
from typing import Annotated, Optional, List
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GithubServer(BaseMCPServer):
    """MCP Server for GitHub."""

    name: str = "github"
    category: str = "GitHub"
    description: str = "GitHub integration for repositories, issues, pull requests, and commits."
    scope: str = "github_access_key"
    client_service = IntegrationAppClient()
    base_url = "/github"

    def _register_prompts(self) -> None:
        """Register all GitHub prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all GitHub tools with the MCP server."""

        get_authenticated_user_output = mcp_output(
            description="Authenticated GitHub user profile details",
            examples=[''])
        @self._mcp.tool(
            description="Get the authenticated GitHub user.",
            meta=mcp_meta("get_authenticated_user"),
            structured_output=True
        )
        async def get_authenticated_user() -> get_authenticated_user_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/user/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_repos_output = mcp_output(
            description="List of repositories with pagination metadata",
            examples=[''])
        @self._mcp.tool(
            description="List repositories for the authenticated user.",
            meta=mcp_meta("list_repos"),
            structured_output=True
        )
        async def list_repos(
            visibility: Annotated[Optional[str], Field(description="Repository visibility: all, public, or private")] = "all",
            per_page: Annotated[Optional[int], Field(description="Maximum number of repositories per page")] = 30,
            page: Annotated[Optional[int], Field(description="Page number for pagination")] = 1
        ) -> list_repos_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/repos/",
                data={
                    "visibility": visibility,
                    "per_page": per_page,
                    "page": page,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_repo_output = mcp_output(
            description="Repository details for the requested owner and repository name",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific repository.",
            meta=mcp_meta("get_repo"),
            structured_output=True
        )
        async def get_repo(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")]
        ) -> get_repo_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/repo/",
                data={
                    "owner": owner,
                    "repo": repo,
                },
                context=context
            )
            return [json.dumps(response.data)]

        list_issues_output = mcp_output(
            description="List of issues in the specified repository",
            examples=[''])
        @self._mcp.tool(
            description="List issues for a repository.",
            meta=mcp_meta("list_issues"),
            structured_output=True
        )
        async def list_issues(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            state: Annotated[Optional[str], Field(description="Issue state: open, closed, or all")] = "open",
            per_page: Annotated[Optional[int], Field(description="Maximum number of issues per page")] = 30,
            page: Annotated[Optional[int], Field(description="Page number for pagination")] = 1
        ) -> list_issues_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "state": state,
                    "per_page": per_page,
                    "page": page,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_issue_output = mcp_output(
            description="Details for a specific issue in a repository",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific issue.",
            meta=mcp_meta("get_issue"),
            structured_output=True
        )
        async def get_issue(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            issue_number: Annotated[int, Field(description="Issue number")]
        ) -> get_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/get/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "issue_number": issue_number,
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_issue_output = mcp_output(
            description="Created issue details including number, state, and URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a new issue in a repository.",
            meta=mcp_meta("create_issue"),
            structured_output=True
        )
        async def create_issue(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            title: Annotated[str, Field(description="Issue title")],
            body: Annotated[Optional[str], Field(description="Issue description/body")] = None,
            labels: Annotated[Optional[List[str]], Field(description="List of labels")] = None,
            assignees: Annotated[Optional[List[str]], Field(description="List of assignees")]=None
        ) -> create_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/create/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "title": title,
                    "body": body,
                    "labels": labels,
                    "assignees": assignees,
                },
                context=context
            )
            return [json.dumps(response.data)]

        list_pull_requests_output = mcp_output(
            description="List of pull requests in the specified repository",
            examples=[''])
        @self._mcp.tool(
            description="List pull requests for a repository.",
            meta=mcp_meta("list_pull_requests"),
            structured_output=True
        )
        async def list_pull_requests(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            state: Annotated[Optional[str], Field(description="Pull request state: open, closed, or all")] = "open",
            per_page: Annotated[Optional[int], Field(description="Maximum number of pull requests per page")] = 30,
            page: Annotated[Optional[int], Field(description="Page number for pagination")] = 1
        ) -> list_pull_requests_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pulls/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "state": state,
                    "per_page": per_page,
                    "page": page,
                },
                context=context
            )
            return [json.dumps(response.data)]

        search_repositories_output = mcp_output(
            description="Repository search results matching the query",
            examples=[''])
        @self._mcp.tool(
            description="Search public repositories on GitHub.",
            meta=mcp_meta("search_repositories"),
            structured_output=True
        )
        async def search_repositories(
            query: Annotated[str, Field(description="Search query for repositories")],
            per_page: Annotated[Optional[int], Field(description="Maximum number of repositories to return")] = 30
        ) -> search_repositories_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/search/repos/",
                data={
                    "query": query,
                    "per_page": per_page,
                },
                context=context
            )
            return [json.dumps(response.data)]

        search_issues_output = mcp_output(
            description="Issue search results matching the query",
            examples=[''])
        @self._mcp.tool(
            description="Search issues on GitHub.",
            meta=mcp_meta("search_issues"),
            structured_output=True
        )
        async def search_issues(
            query: Annotated[str, Field(description="Search query for issues")],
            per_page: Annotated[Optional[int], Field(description="Maximum number of issues to return")] = 30
        ) -> search_issues_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/search/issues/",
                data={
                    "query": query,
                    "per_page": per_page,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_file_content_output = mcp_output(
            description="File content and metadata from the specified repository path",
            examples=[''])
        @self._mcp.tool(
            description="Get repository file content by path.",
            meta=mcp_meta("get_file_content"),
            structured_output=True
        )
        async def get_file_content(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            path: Annotated[str, Field(description="Path to file in repository")],
            ref: Annotated[Optional[str], Field(description="Git reference (branch, tag, or commit SHA)")] = None
        ) -> get_file_content_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/file/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "path": path,
                    "ref": ref,
                },
                context=context
            )
            return [json.dumps(response.data)]

        list_commits_output = mcp_output(
            description="List of commits from the specified repository",
            examples=[''])
        @self._mcp.tool(
            description="List commits for a repository.",
            meta=mcp_meta("list_commits"),
            structured_output=True
        )
        async def list_commits(
            owner: Annotated[str, Field(description="Repository owner")],
            repo: Annotated[str, Field(description="Repository name")],
            sha: Annotated[Optional[str], Field(description="Branch name or commit SHA to start listing from")] = None,
            per_page: Annotated[Optional[int], Field(description="Maximum number of commits to return")] = 30
        ) -> list_commits_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/commits/",
                data={
                    "owner": owner,
                    "repo": repo,
                    "sha": sha,
                    "per_page": per_page,
                },
                context=context
            )
            return [json.dumps(response.data)]
