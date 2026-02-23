import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Similarweb prompts with the MCP server."""

    @mcp.prompt()
    async def similarweb_guide() -> str:
        return f"Guide for website analytics and market intelligence with Similarweb API..."
