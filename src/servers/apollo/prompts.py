import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Apollo prompts with the MCP server."""

    @mcp.prompt()
    async def apollo_guide() -> str:
        return f"Guide for accessing contact and company data with Apollo API..."
