import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all PostHog prompts with the MCP server."""

    @mcp.prompt()
    async def posthog_guide() -> str:
        return """Guide for using PostHog API for product analytics:

        PostHog is an open-source product analytics platform:
        - Track events and user behavior
        - Manage feature flags and experiments
        - Query analytics data with HogQL

        Key capabilities:
        1. Projects: List all projects in the organization
        2. Events: List and capture events for a project
        3. Persons: List and search users (persons)
        4. Feature Flags: List all feature flags
        5. Insights: List saved charts and insights
        6. Cohorts: List user cohorts
        7. Query: Execute HogQL or insight queries

        Best practices:
        - Always specify project_id when accessing project-scoped data
        - Use distinct_id consistently for user identification
        - Use after/before for time-range filtering on events
        """
