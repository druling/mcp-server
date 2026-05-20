import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Affinity prompts with the MCP server."""

    @mcp.prompt()
    async def affinity_guide() -> str:
        return """Guide for using Affinity CRM API for relationship intelligence:

        Affinity helps teams track and manage their relationships and deals:
        - Search and manage persons and organizations
        - Track opportunities through lists
        - Add notes and field values to entities

        Key capabilities:
        1. Persons: Search/list persons, get person details
        2. Organizations: Search/list organizations, get organization details
        3. Lists: View all lists and their entries (deals, opportunities)
        4. Notes: Retrieve and create notes on persons, organizations, or opportunities
        5. Field Values: Read custom field values on any entity
        6. Opportunities: Search and list opportunities

        Best practices:
        - Use term parameter for search queries
        - Use page_token for cursor-based pagination
        - Attach notes to multiple entity types at once when relevant
        """
