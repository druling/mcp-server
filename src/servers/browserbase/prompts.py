import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Browserbase prompts with the MCP server."""

    @mcp.prompt()
    async def browserbase_guide() -> str:
        return """Guide for using Browserbase API for cloud browser automation:

        Browserbase provides cloud-hosted browsers for automation and scraping:
        - Create and manage browser sessions
        - Monitor session status and recordings
        - Access session logs for debugging

        Key capabilities:
        1. Projects: List and view projects
        2. Sessions: Create, list, view, and stop browser sessions
        3. Recordings: Retrieve session recordings for replay
        4. Logs: Access session logs for debugging

        Best practices:
        - Always specify project_id when creating sessions
        - Stop sessions when done to avoid resource waste
        - Check session status before accessing recordings
        - Use session logs to debug automation failures
        """
