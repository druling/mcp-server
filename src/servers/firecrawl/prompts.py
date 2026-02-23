import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Firecrawl prompts with the MCP server."""

    @mcp.prompt()
    async def firecrawl_guide() -> str:
        return f"Guide for web scraping and data extraction with Firecrawl API..."
