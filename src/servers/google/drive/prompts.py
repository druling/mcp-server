import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Drive prompts with the MCP server."""

    @mcp.prompt()
    async def google_drive_guide() -> str:
        return f"Guide for managing files and folders with Google Drive API..."
