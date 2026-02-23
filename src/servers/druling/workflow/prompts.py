import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Workflow prompts with the MCP server."""

    @mcp.prompt()
    async def workflow_creation_guide(workflow_type: str = "general") -> str:
        """Get a comprehensive guide for creating workflows."""
        return f"Guide for creating {workflow_type} workflows..."
