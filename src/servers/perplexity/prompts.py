import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Perplexity prompts with the MCP server."""

    @mcp.prompt()
    async def perplexity_guide() -> str:
        return f"Guide for AI-powered search and research with Perplexity API..."
