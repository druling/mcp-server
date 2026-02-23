import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Apollo prompts with the MCP server."""

    @mcp.prompt()
    async def apollo_guide() -> str:
        return """Guide for using Apollo API to find contacts and companies:
        
        Apollo is a sales intelligence platform that helps you:
        - Search for companies by name, industry, size, and location
        - Find contact information including email addresses and phone numbers
        - Get company details and enrichment data
        
        Key capabilities:
        1. Search Companies: Find companies matching specific criteria
        2. Get Company by Domain: Retrieve detailed company information
        3. Get Contact Info: Find and verify contact details for prospects
        
        Best practices:
        - Use specific search criteria to narrow down results
        - Combine multiple filters for more accurate results
        - Verify contact information before use
        """
