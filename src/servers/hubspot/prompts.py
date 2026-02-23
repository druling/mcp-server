import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Hubspot prompts with the MCP server."""

    @mcp.prompt()
    async def hubspot_guide() -> str:
        return f"Guide for CRM and marketing automation with Hubspot API..."
