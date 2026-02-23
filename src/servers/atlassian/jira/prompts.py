import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Jira prompts with the MCP server."""

    @mcp.prompt()
    async def jira_guide() -> str:
        return f"Guide for managing issues, projects, and workflows with Jira API..."
