import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Task Scheduler prompts with the MCP server."""

    @mcp.prompt()
    async def task_scheduler_guide(task_type: str = "general") -> str:
        """Get a comprehensive guide for task scheduling."""
        return f"Guide for scheduling and managing {task_type} tasks..."
