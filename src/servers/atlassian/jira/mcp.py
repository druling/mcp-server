import json
import logging
from typing import Annotated, Optional, List, Dict, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class JiraServer(BaseMCPServer):
    """MCP Server for Jira."""

    name: str = "jira"
    category: str = "Jira"
    description: str = "Jira integration for managing issues, projects, and workflows."
    scope: str = "jira_access"
    client_service = IntegrationAppClient()
    base_url = "/atlassian/jira"

    def _register_prompts(self) -> None:
        """Register all Jira prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Jira tools with the MCP server."""

        get_projects_output = mcp_output(
            description="List of Jira projects with key, name, and metadata",
            examples=[''])
        @self._mcp.tool(
            description="Get list of all Jira projects.",
            meta=mcp_meta("get_projects"),
            structured_output=True
        )
        async def get_projects(
            max_results: Annotated[Optional[int], Field(description="Maximum number of projects to retrieve")] = 50
        ) -> get_projects_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/",
                data={"max_results": max_results},
                context=context
            )
            return [json.dumps(response.data)]

        get_project_output = mcp_output(
            description="Detailed information about a specific Jira project",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Jira project.",
            meta=mcp_meta("get_project"),
            structured_output=True
        )
        async def get_project(
            project_key: Annotated[str, Field(description="Project key")]
        ) -> get_project_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/get/",
                data={"project_key": project_key},
                context=context
            )
            return [json.dumps(response.data)]

        search_issues_output = mcp_output(
            description="List of Jira issues matching the JQL query",
            examples=[''])
        @self._mcp.tool(
            description="Search Jira issues using JQL (Jira Query Language).",
            meta=mcp_meta("search_issues"),
            structured_output=True
        )
        async def search_issues(
            jql: Annotated[str, Field(description="JQL query string (e.g., 'project = PROJ AND status = Open')")],
            fields: Annotated[Optional[List[str]], Field(description="List of fields to return")] = None,
            max_results: Annotated[Optional[int], Field(description="Maximum number of issues to retrieve")] = 50,
            start_at: Annotated[Optional[int], Field(description="Starting index for pagination")] = 0
        ) -> search_issues_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/search/",
                data={
                    "jql": jql,
                    "fields": fields,
                    "max_results": max_results,
                    "start_at": start_at,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_issue_output = mcp_output(
            description="Detailed information about a specific Jira issue",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Jira issue.",
            meta=mcp_meta("get_issue"),
            structured_output=True
        )
        async def get_issue(
            issue_key: Annotated[str, Field(description="Issue key (e.g., 'PROJ-123')")],
            fields: Annotated[Optional[List[str]], Field(description="List of fields to return")] = None
        ) -> get_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/get/",
                data={
                    "issue_key": issue_key,
                    "fields": fields,
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_issue_output = mcp_output(
            description="Created issue details with key and ID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Jira issue.",
            meta=mcp_meta("create_issue"),
            structured_output=True
        )
        async def create_issue(
            project_key: Annotated[str, Field(description="Project key")],
            summary: Annotated[str, Field(description="Issue summary/title")],
            issue_type: Annotated[Optional[str], Field(description="Issue type (Task, Bug, Story, etc.)")] = "Task",
            description: Annotated[Optional[str], Field(description="Issue description")] = None,
            assignee_id: Annotated[Optional[str], Field(description="Assignee user ID")] = None,
            priority: Annotated[Optional[str], Field(description="Priority (Highest, High, Medium, Low, Lowest)")] = None,
            labels: Annotated[Optional[List[str]], Field(description="List of labels")] = None
        ) -> create_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/create/",
                data={
                    "project_key": project_key,
                    "summary": summary,
                    "issue_type": issue_type,
                    "description": description,
                    "assignee_id": assignee_id,
                    "priority": priority,
                    "labels": labels,
                },
                context=context
            )
            return [json.dumps(response.data)]

        update_issue_output = mcp_output(
            description="Confirmation of issue update",
            examples=[''])
        @self._mcp.tool(
            description="Update a Jira issue.",
            meta=mcp_meta("update_issue"),
            structured_output=True
        )
        async def update_issue(
            issue_key: Annotated[str, Field(description="Issue key")],
            fields: Annotated[Dict[str, Any], Field(description="Fields to update")]
        ) -> update_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/update/",
                data={
                    "issue_key": issue_key,
                    "fields": fields,
                },
                context=context
            )
            return [json.dumps(response.data)]

        add_comment_output = mcp_output(
            description="Created comment details",
            examples=[''])
        @self._mcp.tool(
            description="Add a comment to a Jira issue.",
            meta=mcp_meta("add_comment"),
            structured_output=True
        )
        async def add_comment(
            issue_key: Annotated[str, Field(description="Issue key")],
            comment: Annotated[str, Field(description="Comment text")]
        ) -> add_comment_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/comment/",
                data={
                    "issue_key": issue_key,
                    "comment": comment,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_transitions_output = mcp_output(
            description="Available transitions for the issue",
            examples=[''])
        @self._mcp.tool(
            description="Get available transitions for a Jira issue.",
            meta=mcp_meta("get_transitions"),
            structured_output=True
        )
        async def get_transitions(
            issue_key: Annotated[str, Field(description="Issue key")]
        ) -> get_transitions_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/transitions/",
                data={"issue_key": issue_key},
                context=context
            )
            return [json.dumps(response.data)]

        transition_issue_output = mcp_output(
            description="Confirmation of issue transition",
            examples=[''])
        @self._mcp.tool(
            description="Transition a Jira issue to a new status.",
            meta=mcp_meta("transition_issue"),
            structured_output=True
        )
        async def transition_issue(
            issue_key: Annotated[str, Field(description="Issue key")],
            transition_id: Annotated[str, Field(description="Transition ID")]
        ) -> transition_issue_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/issues/transition/",
                data={
                    "issue_key": issue_key,
                    "transition_id": transition_id,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_users_output = mcp_output(
            description="List of Jira users",
            examples=[''])
        @self._mcp.tool(
            description="Get list of Jira users.",
            meta=mcp_meta("get_users"),
            structured_output=True
        )
        async def get_users(
            query: Annotated[Optional[str], Field(description="Search query for users")] = None,
            max_results: Annotated[Optional[int], Field(description="Maximum number of users to retrieve")] = 50
        ) -> get_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={
                    "query": query,
                    "max_results": max_results,
                },
                context=context
            )
            return [json.dumps(response.data)]
