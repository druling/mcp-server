import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all Hunter prompts with the MCP server."""

    @mcp.prompt()
    async def hunter_guide() -> str:
        return """Guide for using Hunter API for email finding and verification:
        
        Hunter helps you find and verify professional email addresses:
        - Find email addresses associated with a domain
        - Verify email deliverability
        - Get contact information with confidence scores
        
        Key capabilities:
        1. Email Finder: Find email addresses by domain, name, and company
        2. Email Verification: Check if an email address is valid and deliverable
        3. Contact Search: Find contacts with LinkedIn profiles and job titles
        
        Best practices:
        - Use domain and name for more accurate results
        - Check confidence scores before using email addresses
        - Combine with LinkedIn profiles for better matching
        """
