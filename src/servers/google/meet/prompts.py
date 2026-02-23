import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Meet prompts with the MCP server."""

    @mcp.prompt()
    async def google_meet_guide() -> str:
        return f"Guide for managing video meetings and conferences with Google Meet API..."
