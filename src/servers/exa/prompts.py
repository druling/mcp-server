import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Exa prompts with the MCP server."""

    @mcp.prompt()
    async def exa_guide() -> str:
        return """Guide for using Exa API for web search and content discovery:

        Exa is a neural search engine that helps you find and retrieve web content:
        - Semantic search across the web with quality filtering
        - Find similar content based on a URL
        - Retrieve full content, highlights, and summaries

        Key capabilities:
        1. Search: Neural web search with domain filtering and date ranges
        2. Find Similar: Discover content similar to a given URL
        3. Get Contents: Retrieve full text, highlights, or summaries by content IDs

        Search options:
        - Domain filtering (include/exclude specific domains)
        - Date range filtering (start/end published dates)
        - Autoprompt enhancement for better queries
        - Search type: auto, keyword, or neural

        Best practices:
        - Use autoprompt for natural language queries
        - Filter by domains for focused results
        - Request text/highlights only when needed to reduce response size
        - Use find_similar to discover related content from a known good URL
        """
