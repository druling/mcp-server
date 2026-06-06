import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Gong prompts with the MCP server."""

    @mcp.prompt()
    async def gong_guide() -> str:
        return """Guide for using Gong API for sales intelligence and call analytics:

        Gong provides AI-powered insights from customer conversations:
        - Access call recordings and transcripts
        - Analyze conversation data and statistics
        - Track sales team performance and engagement

        Key capabilities:
        1. Calls: List calls with date filtering and pagination
        2. Call Details: Get individual call information
        3. Transcripts: Retrieve call transcripts for analysis
        4. Extensive Call Data: Access detailed call metadata and insights
        5. Call Stats: Aggregate statistics by date and user
        6. Users: List Gong workspace users

        Call filtering:
        - Filter by date range (from_date_time, to_date_time)
        - Use cursor for pagination through large result sets
        - Request specific call_ids for batch operations

        Best practices:
        - Use date filters to limit scope and improve performance
        - Fetch transcripts in batches using call_ids list
        - Request extensive data only when detailed analysis is needed
        - Use call stats for reporting and performance tracking
        """
