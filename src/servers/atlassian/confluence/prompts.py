import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Confluence prompts with the MCP server."""

    @mcp.prompt()
    async def confluence_guide() -> str:
        return f"Guide for managing wiki pages and documentation with Confluence API..."
