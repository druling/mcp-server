import logging

logger = logging.getLogger(__name__)

def prompts(mcp, ctx) -> None:
    """Register all HubSpot prompts with the MCP server."""

    @mcp.prompt()
    async def hubspot_guide() -> str:
        return """Guide for using HubSpot API for CRM and marketing automation:
        
        HubSpot provides comprehensive CRM and marketing automation capabilities:
        - Manage contacts, companies, deals, and other CRM objects
        - Access properties, pipelines, and lists
        - Send marketing emails
        
        Key capabilities:
        1. Properties: Get available properties for any object type
        2. Pipelines: Manage deal and ticket pipelines
        3. Lists: Access and manage contact/company lists
        4. Records: Create, read, update, and search CRM records
        5. Marketing Emails: Send template-based emails
        
        Supported object types:
        - contacts: People in your CRM
        - companies: Organizations
        - deals: Sales opportunities
        - tickets: Customer service tickets
        - tasks, notes, calls, emails, meetings
        - products, line_items, quotes
        
        Best practices:
        - Get properties first to know available fields
        - Use search with filters for targeted queries
        - Batch operations for better performance
        - Use pipelines to organize deals and tickets
        """
