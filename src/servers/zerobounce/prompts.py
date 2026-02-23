import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Zerobounce prompts with the MCP server."""

    @mcp.prompt()
    async def zerobounce_guide() -> str:
        return f"Guide for email validation and verification with Zerobounce API..."
