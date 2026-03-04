import json
import logging
from typing import Annotated
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

        read_emails_output = mcp_output(
            description="List of Jira issues matching the search query with key, summary, status, and assignee",
            examples=[''])
        @self._mcp.tool(
            description="Read all emails in the user's Gmail account.",
            meta=mcp_meta("read_emails"),
            structured_output=True
        )
        async def read_emails(
                query: Annotated[str, Field(description="Search query to filter emails (e.g., 'from:name@example.com' or 'subject:meeting')")],
                max_results: Annotated[int, Field(description="Maximum number of emails to retrieve")] = 10
        ) -> read_emails_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/read/",
                data={
                "query": query,
                "max_results": max_results
            }, context=context)
            return [json.dumps(item) for item in response.data]
