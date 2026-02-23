import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Similarweb prompts with the MCP server."""

    @mcp.prompt()
    async def similarweb_guide() -> str:
        return """Guide for using Similarweb API for website analytics:
        
        Similarweb provides comprehensive website analytics and market intelligence:
        - Get traffic statistics for any website
        - Analyze competitor performance
        - Understand traffic sources and audience demographics
        
        Key capabilities:
        1. Company Info by Domain: Get detailed website analytics
        2. Traffic Analysis: Monthly visits, bounce rate, time on site
        3. Rankings: Global and country-specific website rankings
        4. Traffic Sources: Direct, search, social, referral breakdown
        
        Use cases:
        - Competitive analysis
        - Market research
        - Lead qualification
        - Partnership opportunities
        """
