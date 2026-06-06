import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Ashby prompts with the MCP server."""

    @mcp.prompt()
    async def ashby_guide() -> str:
        return """Guide for using Ashby API for recruiting and hiring management:

        Ashby is an all-in-one recruiting platform for managing candidates and jobs:
        - Search and manage candidates across pipeline stages
        - Track job postings and applications
        - Access user and department data

        Key capabilities:
        1. Candidates: List, search, get, and create candidates
        2. Jobs: List and view open job postings
        3. Applications: List and view applications
        4. Users: List hiring team members
        5. Departments: List departments

        Best practices:
        - Search candidates by email for deduplication
        - Use cursor-based pagination for large datasets
        - Combine candidate search with application data for full pipeline view
        """
