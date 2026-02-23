import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Workflow Component prompts with the MCP server."""

    @mcp.prompt()
    async def workflow_component_guide(workflow_type: str = "general") -> str:
        """Get a comprehensive guide for workflow components."""
        return f"Guide for creating {workflow_type} workflow components..."
