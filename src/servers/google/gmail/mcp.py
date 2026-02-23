import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from src.servers.google.gmail import outputs
from src.servers.google.gmail.prompts import gmail_prompts

logger = logging.getLogger(__name__)


@dataclass
class GmailMCPServer(BaseMCPServer):
    """MCP Server for Gmail."""

    name: str = "gmail"
    category: str = "Gmail"
    description: str = "Gmail integration for reading emails and performing actions on Gmail accounts."
    scope: str = "gmail_access"
    backend_service = BackendClient()
    base_url = "/google/gmail"

    def _register_prompts(self) -> None:
        """Register all gmail prompts with the MCP server."""
        gmail_prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all gmail tools with the MCP server."""

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
