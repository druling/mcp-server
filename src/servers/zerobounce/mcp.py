import json
import logging
from typing import Annotated
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import Output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class ZerobounceServer(BaseMCPServer):
    """MCP Server for Zerobounce."""

    name: str = "zerobounce"
    category: str = "Zerobounce"
    description: str = "Zerobounce integration for email validation and verification."
    scope: str = "zerobounce_access"
    backend_service = BackendClient()
    base_url = "/zerobounce"

    def _register_prompts(self) -> None:
        """Register all Zerobounce prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Zerobounce tools with the MCP server."""

        @self._mcp.tool(
            description="Validate an email address to check if it's valid and deliverable.",
            meta=mcp_meta("validate_email"),
            structured_output=True
        )
        async def validate_email(
            email: Annotated[str, Field(description="Email address to validate")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/validate/",
                data={"email": email},
                context=context
            )
            return [json.dumps(response.data)]
