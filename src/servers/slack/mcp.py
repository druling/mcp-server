import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from src.servers.google.gmail import outputs
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class SlackServer(BaseMCPServer):
    """MCP Server for Slack."""

    name: str = "slack"
    category: str = "Slack"
    description: str = "Slack integration for messaging and team collaboration."
    scope: str = "slack_access"
    backend_service = BackendClient()
    base_url = "/slack"

    def _register_prompts(self) -> None:
        """Register all Slack prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Slack tools with the MCP server."""

        @self._mcp.tool(
            description="Read all emails in the user's Gmail account.",
            meta=mcp_meta("read_emails"),
            structured_output=True
        )
        async def read_emails(
                query: Annotated[str, Field(description="Search query to filter emails (e.g., 'from:name@example.com' or 'subject:meeting')")],
                max_results: Annotated[int, Field(description="Maximum number of emails to retrieve")] = 10
        ) -> outputs.ListGmailRead:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/read/",
                data={
                "query": query,
                "max_results": max_results
            }, context=context)

            result: list[outputs.GmailRead] = response.data
            return outputs.ListGmailRead(result=result)
