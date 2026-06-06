import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all GitHub prompts with the MCP server."""

    @mcp.prompt()
    async def github_guide() -> str:
        return """Guide for using GitHub API for repository and collaboration workflows:

        GitHub integration supports repository discovery and software collaboration:
        - Get authenticated user details
        - List and inspect repositories
        - Search repositories and issues
        - Read file content from repositories
        - Work with issues, pull requests, and commits

        Key capabilities:
        1. User: Get current authenticated user
        2. Repositories: List repos, get repo details, search repos
        3. Issues: List issues, get issue details, create issues, search issues
        4. Pull Requests: List pull requests by state
        5. Code: Read file content and list commits

        Best practices:
        - Use small page sizes for broad queries, then paginate
        - Filter issues and PRs by state when possible
        - Provide explicit owner and repo for deterministic results
        """
