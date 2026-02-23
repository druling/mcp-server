import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Slack prompts with the MCP server."""

    @mcp.prompt()
    async def slack_guide() -> str:
        return """Guide for using Slack API for team collaboration:
        
        Slack integration provides comprehensive messaging and collaboration features:
        - Send and read messages in channels
        - Create and manage canvases
        - Get user and channel information
        
        Key capabilities:
        1. Channels: Get list of channels, channel info
        2. Users: Get list of users in workspace
        3. Messaging: Send messages, read messages, reply to threads
        4. Block Messages: Send rich formatted messages with Block Kit
        5. Canvases: Create collaborative documents
        6. Threads: Get thread replies and permalinks
        
        Message options:
        - Send as user or bot
        - Reply to threads
        - Attach files
        - Hide link previews
        - Use Block Kit for rich formatting
        
        Best practices:
        - Use threads for organized conversations
        - Leverage Block Kit for interactive messages
        - Set appropriate canvas access levels
        """
