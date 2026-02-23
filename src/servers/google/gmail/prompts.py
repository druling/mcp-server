import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Gmail prompts with the MCP server."""

    @mcp.prompt()
    async def gmail_guide() -> str:
        return f"Guide for creating sending emails with Gmail API..."
