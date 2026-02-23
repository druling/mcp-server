import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Slack prompts with the MCP server."""

    @mcp.prompt()
    async def slack_guide() -> str:
        return f"Guide for messaging and team collaboration with Slack API..."
