import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Workflow Run prompts with the MCP server."""

    @mcp.prompt()
    async def workflow_run_guide(workflow_type: str = "general") -> str:
        """Get a comprehensive guide for workflow runs."""
        return f"Guide for monitoring and managing {workflow_type} workflow runs..."
