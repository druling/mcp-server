import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Firecrawl prompts with the MCP server."""

    @mcp.prompt()
    async def firecrawl_guide() -> str:
        return """Guide for using Firecrawl API for web scraping and data extraction:
        
        Firecrawl provides powerful web scraping capabilities:
        - Scrape single web pages for content and data extraction
        - Crawl entire websites with depth control
        - Search job listings from various job boards
        
        Key features:
        1. Scrape: Extract content from a single URL with stealth mode support
        2. Crawl: Recursively crawl websites starting from a root URL
        3. Job Search: Find job listings from job boards like Indeed and LinkedIn
        
        Options:
        - Stealth mode to avoid bot detection
        - Mobile user agent support
        - Custom browser actions
        - Link extraction
        - Raw HTML retrieval
        """
