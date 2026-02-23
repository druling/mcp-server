import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Docs prompts with the MCP server."""

    @mcp.prompt()
    async def google_docs_guide() -> str:
        return f"Guide for reading and managing documents with Google Docs API..."
