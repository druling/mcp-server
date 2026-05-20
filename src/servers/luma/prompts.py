import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Luma prompts with the MCP server."""

    @mcp.prompt()
    async def luma_guide() -> str:
        return """Guide for using Luma API for event management:

        Luma is an event management platform for hosting and tracking events:
        - Create and manage events with guest lists
        - Track attendees and RSVPs
        - Manage calendar and people

        Key capabilities:
        1. User: Get authenticated user profile
        2. Calendar: Get calendar details
        3. Events: List, view, and create events
        4. Guests: View and add guests to events
        5. People: Browse your network of contacts

        Best practices:
        - Use after/before timestamps for date-range filtering on events
        - Use pagination_cursor for paginating through large lists
        - When adding guests, provide email and name in the guests list
        """
