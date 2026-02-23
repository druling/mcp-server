import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Google Sheets prompts with the MCP server."""

    @mcp.prompt()
    async def google_sheets_guide() -> str:
        return f"Guide for managing spreadsheets and data with Google Sheets API..."
