import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Ghost prompts with the MCP server."""

    @mcp.prompt()
    async def ghost_guide() -> str:
        return """Guide for using Ghost Admin API for content management:

        Ghost is a headless CMS and publishing platform:
        - Create and manage blog posts and pages
        - Manage members and subscriptions
        - Organize content with tags

        Key capabilities:
        1. Posts: List, view, create, and update posts
        2. Pages: List static pages
        3. Members: View and manage newsletter subscribers
        4. Tags: Browse content tags
        5. Site: Get site configuration

        Best practices:
        - Use status filter when listing posts (published, draft, scheduled)
        - Always include updated_at when updating a post for conflict detection
        - Use limit/page for paginating through content lists
        - Tags can be provided as objects with name or slug
        """
