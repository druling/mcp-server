import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Asana prompts with the MCP server."""

    @mcp.prompt()
    async def asana_guide() -> str:
        return """Guide for using Asana API for project and task management:

        Asana is a work management platform for tracking tasks and projects:
        - Manage tasks across projects and workspaces
        - Assign and track work for team members
        - Organize work with sections and projects

        Key capabilities:
        1. Me: Get the authenticated user profile
        2. Workspaces: List all accessible workspaces
        3. Projects: List and view projects
        4. Tasks: List, view, create, and update tasks
        5. Sections: List sections within a project
        6. Users: List workspace members
        7. Add Task to Project: Move tasks between projects

        Best practices:
        - Get workspaces first to get workspace GID
        - Filter tasks by project for better performance
        - Use due_on as YYYY-MM-DD format
        - Task GIDs are stable identifiers — save them for future lookups
        """
