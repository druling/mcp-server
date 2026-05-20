import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all Jira prompts with the MCP server."""

    @mcp.prompt()
    async def jira_guide() -> str:
        return """Guide for using Jira API for project and issue management:

        Jira integration enables comprehensive project tracking and issue management:
        - Search and filter issues using JQL (Jira Query Language)
        - Create, update, and track issues across projects
        - Manage workflows and transitions
        - Collaborate with comments and assignees

        Key capabilities:
        1. Projects: List all projects, get project details
        2. Issues: Search with JQL, get issue details, create and update issues
        3. Workflow: Get available transitions, transition issues to new status
        4. Collaboration: Add comments, assign users
        5. Users: Search and list Jira users

        JQL examples:
        - 'project = PROJ AND status = Open'
        - 'assignee = currentUser() AND status != Done'
        - 'created >= -7d ORDER BY created DESC'

        Best practices:
        - Use JQL for precise issue filtering
        - Check available transitions before transitioning issues
        - Specify fields parameter to reduce response size
        - Use pagination (start_at, max_results) for large result sets
        """
