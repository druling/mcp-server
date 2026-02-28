import json
import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GoogleMeetServer(BaseMCPServer):
    """MCP Server for Google Meet."""

    name: str = "google_meet"
    category: str = "Google Meet"
    description: str = "Google Meet integration for managing video meetings and conferences."
    scope: str = "google_meet_access"
    backend_service = BackendClient()
    base_url = "/google/meet"

    def _register_prompts(self) -> None:
        """Register all Google Meet prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Google Meet tools with the MCP server."""

        read_emails_output = mcp_output(
            description="List of Google Meet meetings matching the search query with title, date, and participants",
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
            response = self.backend_service.post(
                f"{self.base_url}/read/",
                data={
                "query": query,
                "max_results": max_results
            }, context=context)
            return [json.dumps(item) for item in response.data]
