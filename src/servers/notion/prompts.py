import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Notion prompts with the MCP server."""

    @mcp.prompt()
    async def notion_guide() -> str:
        return """Guide for using Notion API for workspace collaboration:

        Notion integration enables you to work with workspaces, databases, and pages:
        - Search across all workspace content
        - Query and manage databases
        - Create, read, and update pages
        - Work with blocks and content structure

        Key capabilities:
        1. Search: Find pages, databases, and content across workspace
        2. Databases: Get database schema, query with filters and sorts
        3. Pages: Create, read, update pages with properties
        4. Blocks: Retrieve block children for content hierarchy
        5. Users: List workspace users

        Database queries:
        - Apply filters to narrow results
        - Sort by properties
        - Control page size for pagination

        Page operations:
        - Create pages with parent and properties
        - Update page properties
        - Add children blocks for rich content

        Best practices:
        - Use search with filter_type (page/database) for targeted results
        - Query databases with specific filters to reduce data transfer
        - Structure page properties according to database schema
        """
