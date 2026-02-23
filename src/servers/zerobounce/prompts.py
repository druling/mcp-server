import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all ZeroBounce prompts with the MCP server."""

    @mcp.prompt()
    async def zerobounce_guide() -> str:
        return """Guide for using ZeroBounce API for email validation:
        
        ZeroBounce provides professional email validation and verification:
        - Validate email addresses for deliverability
        - Check for spam traps and disposable emails
        - Get email quality scores
        
        Key capabilities:
        1. Email Validation: Check if an email is valid and deliverable
        2. Deliverability Check: Verify email inbox exists
        3. Risk Assessment: Identify risky or invalid emails
        
        Validation results:
        - Valid: Email is deliverable
        - Invalid: Email does not exist
        - Catch-all: Domain accepts all emails
        - Unknown: Unable to verify
        - Spamtrap: Known spam trap
        - Abuse: Abuse/complaint email
        - Do not mail: Should not send emails
        
        Best practices:
        - Validate emails before adding to campaigns
        - Check validation status regularly
        - Remove invalid emails from lists
        - Note: Email validation consumes credits
        """
