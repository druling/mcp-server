import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Confluence prompts with the MCP server."""

    @mcp.prompt()
    async def confluence_guide() -> str:
        return """Guide for using Confluence API for documentation and knowledge management:

        Confluence integration supports wiki-style documentation and collaboration:
        - Organize content in spaces and pages
        - Create and update pages with rich content
        - Search using CQL (Confluence Query Language)
        - Manage comments and attachments

        Key capabilities:
        1. Spaces: List spaces, get space details
        2. Pages: Create, read, update pages with hierarchy
        3. Search: Use CQL to find content across Confluence
        4. Comments: View and add comments to pages
        5. Attachments: List page attachments
        6. Navigation: Get child pages and page hierarchy

        CQL examples:
        - 'type=page AND space=DOCS'
        - 'title ~ "user guide" AND lastModified >= now("-7d")'
        - 'creator = currentUser() ORDER BY created DESC'

        Page management:
        - Use version_number when updating pages (required)
        - Specify parent_id to create child pages
        - Set representation to 'storage' for HTML or 'wiki' for wiki markup

        Best practices:
        - Use expand parameter to get page body and metadata
        - Use pagination (start, limit) for large result sets
        - Search with CQL for precise content discovery
        """
