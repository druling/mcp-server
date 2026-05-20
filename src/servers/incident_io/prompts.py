import logging

logger = logging.getLogger(__name__)


def prompts(mcp, ctx) -> None:
    """Register all incident.io prompts with the MCP server."""

    @mcp.prompt()
    async def incident_io_guide() -> str:
        return """Guide for using incident.io API for incident management:

        incident.io is an incident management platform for on-call and response:
        - Create, track, and resolve incidents
        - Manage alerts and escalations
        - Track follow-up actions and schedules

        Key capabilities:
        1. Incidents: List, view, create, and edit incidents
        2. Severities: List severity levels
        3. Alerts: View and manage alerts
        4. Escalations: View escalation policies
        5. Follow-ups: Track post-incident actions
        6. Users: List team members
        7. Schedules: View on-call schedules

        Best practices:
        - Use list_severities to get valid severity_id before creating incidents
        - Set mode to 'real' for production incidents, 'test' for drills
        - Set visibility to 'public' or 'private' based on sensitivity
        - Use after cursor for paginating through large incident histories
        """
