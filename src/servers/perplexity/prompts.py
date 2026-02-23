import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Perplexity prompts with the MCP server."""

    @mcp.prompt()
    async def perplexity_guide() -> str:
        return """Guide for using Perplexity API for AI-powered search:
        
        Perplexity provides AI-powered search and research capabilities:
        - Reserve credits for API usage
        - Access advanced AI search features
        - Get comprehensive research results
        
        Key features:
        1. Credit Reservation: Reserve credits before making API calls
        2. AI Search: Leverage AI for intelligent search results
        3. Research: Get comprehensive answers with sources
        
        Usage:
        - Reserve credits before starting research tasks
        - Use for complex information retrieval
        - Get cited sources with answers
        """
