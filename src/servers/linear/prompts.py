import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Linear prompts with the MCP server."""

    @mcp.prompt()
    async def linear_guide() -> str:
        return """Guide for using Linear API for engineering project management:

        Linear is a project management tool for engineering teams:
        - Track issues, projects, and sprints
        - Manage team workflows and states
        - Assign and prioritize work

        Key capabilities:
        1. Issues: List, view, create, and update issues
        2. Teams: List all teams in the workspace
        3. Projects: List and track projects
        4. Users: List team members
        5. Viewer: Get the authenticated user
        6. Workflow States: View issue states per team

        Best practices:
        - Always get teams first to get team_id for creating issues
        - Use list_workflow_states to find valid state_id values
        - Priority values: 0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low
        - Use cursor pagination (after parameter) for large issue lists
        """
