import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Parallel Markets prompts with the MCP server."""

    @mcp.prompt()
    async def parallel_guide() -> str:
        return """Guide for using Parallel Markets API for investor accreditation and identity:

        Parallel Markets provides identity and accreditation verification for financial platforms:
        - Verify investor accreditation status
        - Access individual and business identity records
        - Monitor token and API connection info

        Key capabilities:
        1. Token: Get current API token and connection info
        2. Accreditations: List and view accreditation records
        3. Individuals: List and view individual identity records
        4. Businesses: List and view business entity records

        Best practices:
        - Use starting_after cursor for paginating through large record sets
        - Check accreditation status before allowing investor actions
        - Combine individual and accreditation data for full investor profiles
        """
