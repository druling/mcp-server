import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Slides prompts with the MCP server."""

    @mcp.prompt()
    async def google_slides_guide() -> str:
        return f"Guide for managing presentations with Google Slides API..."
