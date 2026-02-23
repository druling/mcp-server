import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Hunter prompts with the MCP server."""

    @mcp.prompt()
    async def hunter_guide() -> str:
        return f"Guide for email finding and verification with Hunter API..."
