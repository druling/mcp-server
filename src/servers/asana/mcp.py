import json
import logging
from typing import Annotated, Optional, List
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class AsanaServer(BaseMCPServer):
    """MCP Server for Asana."""

    name: str = "asana"
    category: str = "Asana"
    description: str = "Asana integration for project and task management across teams and workspaces."
    scope: str = "asana_access_key"
    client_service = IntegrationAppClient()
    base_url = "/asana"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        get_me_output = mcp_output(
            description="Authenticated Asana user profile",
            examples=[''])
        @self._mcp.tool(
            description="Get the current authenticated Asana user.",
            meta=mcp_meta("get_me"),
            structured_output=True
        )
        async def get_me() -> get_me_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/me/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_workspaces_output = mcp_output(
            description="List of workspaces the user belongs to",
            examples=[''])
        @self._mcp.tool(
            description="List all Asana workspaces the authenticated user belongs to.",
            meta=mcp_meta("list_workspaces"),
            structured_output=True
        )
        async def list_workspaces() -> list_workspaces_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/workspaces/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_projects_output = mcp_output(
            description="List of Asana projects",
            examples=[''])
        @self._mcp.tool(
            description="List Asana projects, optionally filtered by workspace or team.",
            meta=mcp_meta("list_projects"),
            structured_output=True
        )
        async def list_projects(
            workspace: Annotated[Optional[str], Field(description="Workspace GID to filter by")] = None,
            team: Annotated[Optional[str], Field(description="Team GID to filter by")] = None,
            archived: Annotated[Optional[bool], Field(description="Include archived projects")] = False
        ) -> list_projects_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/",
                data={"workspace": workspace, "team": team, "archived": archived},
                context=context
            )
            return [json.dumps(response.data)]

        get_project_output = mcp_output(
            description="Detailed information about a specific Asana project",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Asana project by GID.",
            meta=mcp_meta("get_project"),
            structured_output=True
        )
        async def get_project(
            project_gid: Annotated[str, Field(description="Project GID")]
        ) -> get_project_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/get/",
                data={"project_gid": project_gid},
                context=context
            )
            return [json.dumps(response.data)]

        list_tasks_output = mcp_output(
            description="List of Asana tasks matching the criteria",
            examples=[''])
        @self._mcp.tool(
            description="List Asana tasks, filtered by project, assignee, or workspace.",
            meta=mcp_meta("list_tasks"),
            structured_output=True
        )
        async def list_tasks(
            project: Annotated[Optional[str], Field(description="Project GID to filter by")] = None,
            assignee: Annotated[Optional[str], Field(description="Assignee GID or 'me'")] = None,
            workspace: Annotated[Optional[str], Field(description="Workspace GID")] = None,
            completed_since: Annotated[Optional[str], Field(description="Filter tasks completed after this ISO timestamp")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of tasks")] = 50
        ) -> list_tasks_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tasks/",
                data={"project": project, "assignee": assignee, "workspace": workspace, "completed_since": completed_since, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_task_output = mcp_output(
            description="Detailed information about a specific Asana task",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Asana task by GID.",
            meta=mcp_meta("get_task"),
            structured_output=True
        )
        async def get_task(
            task_gid: Annotated[str, Field(description="Task GID")]
        ) -> get_task_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tasks/get/",
                data={"task_gid": task_gid},
                context=context
            )
            return [json.dumps(response.data)]

        create_task_output = mcp_output(
            description="Created task details with GID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Asana task.",
            meta=mcp_meta("create_task"),
            structured_output=True
        )
        async def create_task(
            name: Annotated[str, Field(description="Task name")],
            workspace: Annotated[Optional[str], Field(description="Workspace GID")] = None,
            projects: Annotated[Optional[List[str]], Field(description="List of project GIDs to add the task to")] = None,
            assignee: Annotated[Optional[str], Field(description="Assignee GID or 'me'")] = None,
            notes: Annotated[Optional[str], Field(description="Task notes/description")] = None,
            due_on: Annotated[Optional[str], Field(description="Due date as YYYY-MM-DD")] = None
        ) -> create_task_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tasks/create/",
                data={"name": name, "workspace": workspace, "projects": projects, "assignee": assignee, "notes": notes, "due_on": due_on},
                context=context
            )
            return [json.dumps(response.data)]

        update_task_output = mcp_output(
            description="Updated task details",
            examples=[''])
        @self._mcp.tool(
            description="Update an existing Asana task.",
            meta=mcp_meta("update_task"),
            structured_output=True
        )
        async def update_task(
            task_gid: Annotated[str, Field(description="Task GID to update")],
            name: Annotated[Optional[str], Field(description="New task name")] = None,
            completed: Annotated[Optional[bool], Field(description="Mark task as completed")] = None,
            assignee: Annotated[Optional[str], Field(description="New assignee GID")] = None,
            notes: Annotated[Optional[str], Field(description="New task notes")] = None,
            due_on: Annotated[Optional[str], Field(description="New due date as YYYY-MM-DD")] = None
        ) -> update_task_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tasks/update/",
                data={"task_gid": task_gid, "name": name, "completed": completed, "assignee": assignee, "notes": notes, "due_on": due_on},
                context=context
            )
            return [json.dumps(response.data)]

        list_sections_output = mcp_output(
            description="List of sections in the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List sections in an Asana project.",
            meta=mcp_meta("list_sections"),
            structured_output=True
        )
        async def list_sections(
            project_gid: Annotated[str, Field(description="Project GID")]
        ) -> list_sections_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/sections/",
                data={"project_gid": project_gid},
                context=context
            )
            return [json.dumps(response.data)]

        list_users_output = mcp_output(
            description="List of Asana users in the workspace",
            examples=[''])
        @self._mcp.tool(
            description="List users in an Asana workspace.",
            meta=mcp_meta("list_users"),
            structured_output=True
        )
        async def list_users(
            workspace: Annotated[Optional[str], Field(description="Workspace GID to filter by")] = None
        ) -> list_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={"workspace": workspace},
                context=context
            )
            return [json.dumps(response.data)]

        add_task_to_project_output = mcp_output(
            description="Confirmation of task added to project",
            examples=[''])
        @self._mcp.tool(
            description="Add an Asana task to a project.",
            meta=mcp_meta("add_task_to_project"),
            structured_output=True
        )
        async def add_task_to_project(
            task_gid: Annotated[str, Field(description="Task GID")],
            project_gid: Annotated[str, Field(description="Project GID to add task to")],
            insert_before: Annotated[Optional[str], Field(description="Task GID to insert before")] = None
        ) -> add_task_to_project_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tasks/add-project/",
                data={"task_gid": task_gid, "project_gid": project_gid, "insert_before": insert_before},
                context=context
            )
            return [json.dumps(response.data)]
