import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Cal.com prompts with the MCP server."""

    @mcp.prompt()
    async def cal_guide() -> str:
        return """Guide for using Cal.com API for scheduling and booking management:

        Cal.com is an open scheduling platform for managing bookings and availability:
        - View and manage event types and schedules
        - Access bookings and their statuses
        - Cancel bookings when needed

        Key capabilities:
        1. Profile: Get authenticated user profile
        2. Event Types: List and view event types by username
        3. Bookings: List, view, and cancel bookings
        4. Schedules: View availability schedules

        Best practices:
        - Use status filter when listing bookings (upcoming, past, cancelled)
        - Use cursor pagination for large booking histories
        - Check event_type_id before cancelling bookings
        """
