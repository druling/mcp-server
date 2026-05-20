import json
import logging
from typing import Annotated, Optional
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class LinearServer(BaseMCPServer):
    """MCP Server for Linear."""

    name: str = "linear"
    category: str = "Linear"
    description: str = "Linear integration for engineering issue tracking, project management, and team workflows."
    scope: str = "linear_access_key"
    client_service = IntegrationAppClient()
    base_url = "/linear"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_issues_output = mcp_output(
            description="List of Linear issues with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List Linear issues, optionally filtered by team.",
            meta=mcp_meta("list_issues"),
            structured_output=True
        )
        async def list_issues(
            team_id: Annotated[Optional[str], Field(description="Filter by team ID")] = None,
            first: Annotated[Optional[int], Field(description="Number of issues to fetch")] = 50,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_issues_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/",
                data={"team_id": team_id, "first": first, "after": after},
                context=context
            )
            return [json.dumps(response.data)]

        get_issue_output = mcp_output(
            description="Detailed information about a specific Linear issue",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Linear issue by ID.",
            meta=mcp_meta("get_issue"),
            structured_output=True
        )
        async def get_issue(
            issue_id: Annotated[str, Field(description="Issue ID")]
        ) -> get_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/get/",
                data={"issue_id": issue_id},
                context=context
            )
            return [json.dumps(response.data)]

        create_issue_output = mcp_output(
            description="Created issue details with ID and URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Linear issue.",
            meta=mcp_meta("create_issue"),
            structured_output=True
        )
        async def create_issue(
            title: Annotated[str, Field(description="Issue title")],
            team_id: Annotated[str, Field(description="Team ID the issue belongs to")],
            description: Annotated[Optional[str], Field(description="Issue description in markdown")] = None,
            assignee_id: Annotated[Optional[str], Field(description="Assignee user ID")] = None,
            priority: Annotated[Optional[int], Field(description="Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)")] = None,
            state_id: Annotated[Optional[str], Field(description="Workflow state ID")] = None
        ) -> create_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/create/",
                data={"title": title, "team_id": team_id, "description": description, "assignee_id": assignee_id, "priority": priority, "state_id": state_id},
                context=context
            )
            return [json.dumps(response.data)]

        update_issue_output = mcp_output(
            description="Updated issue details",
            examples=[''])
        @self._mcp.tool(
            description="Update an existing Linear issue.",
            meta=mcp_meta("update_issue"),
            structured_output=True
        )
        async def update_issue(
            issue_id: Annotated[str, Field(description="Issue ID to update")],
            title: Annotated[Optional[str], Field(description="New issue title")] = None,
            description: Annotated[Optional[str], Field(description="New issue description")] = None,
            assignee_id: Annotated[Optional[str], Field(description="New assignee user ID")] = None,
            priority: Annotated[Optional[int], Field(description="New priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)")] = None,
            state_id: Annotated[Optional[str], Field(description="New workflow state ID")] = None
        ) -> update_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/update/",
                data={"issue_id": issue_id, "title": title, "description": description, "assignee_id": assignee_id, "priority": priority, "state_id": state_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_teams_output = mcp_output(
            description="List of all teams in the Linear workspace",
            examples=[''])
        @self._mcp.tool(
            description="List all teams in the Linear workspace.",
            meta=mcp_meta("list_teams"),
            structured_output=True
        )
        async def list_teams() -> list_teams_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/teams/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_projects_output = mcp_output(
            description="List of all Linear projects with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all Linear projects.",
            meta=mcp_meta("list_projects"),
            structured_output=True
        )
        async def list_projects(
            first: Annotated[Optional[int], Field(description="Number of projects to fetch")] = 50,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_projects_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/",
                data={"first": first, "after": after},
                context=context
            )
            return [json.dumps(response.data)]

        list_users_output = mcp_output(
            description="List of all users in the Linear workspace",
            examples=[''])
        @self._mcp.tool(
            description="List all users in the Linear workspace.",
            meta=mcp_meta("list_users"),
            structured_output=True
        )
        async def list_users() -> list_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_viewer_output = mcp_output(
            description="Authenticated Linear user details",
            examples=[''])
        @self._mcp.tool(
            description="Get the currently authenticated Linear user.",
            meta=mcp_meta("get_viewer"),
            structured_output=True
        )
        async def get_viewer() -> get_viewer_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/viewer/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_workflow_states_output = mcp_output(
            description="List of workflow states, optionally filtered by team",
            examples=[''])
        @self._mcp.tool(
            description="List Linear workflow states, optionally filtered by team.",
            meta=mcp_meta("list_workflow_states"),
            structured_output=True
        )
        async def list_workflow_states(
            team_id: Annotated[Optional[str], Field(description="Filter by team ID")] = None
        ) -> list_workflow_states_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/workflow-states/",
                data={"team_id": team_id},
                context=context
            )
            return [json.dumps(response.data)]
