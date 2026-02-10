import logging

logger = logging.getLogger(__name__)

def workflow_prompts(mcp, ctx) -> None:
    """Register all workflow prompts with the MCP server."""

    @mcp.prompt()
    async def workflow_creation_guide(workflow_type: str = "general") -> str:
        """Get a comprehensive guide for creating workflows."""
        try:
            user_ctx = ctx
            logger.info(f"Getting workflow creation guide for user: {user_ctx.user_id}")
        except ValueError:
            logger.info("Getting workflow creation guide (no user context)")

        return f"Guide for creating {workflow_type} workflows..."

    @mcp.prompt()
    async def workflow_troubleshooting(error_type: str = "", workflow_id: str = "") -> str:
        """Get troubleshooting guidance for workflow errors."""
        return f"Troubleshooting guide for error: {error_type}, workflow: {workflow_id}"

    @mcp.prompt()
    async def workflow_optimization() -> str:
        """Get optimization suggestions for improving workflow performance and reliability."""
        return "Optimization suggestions for workflows..."
