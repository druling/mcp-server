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
class HunterServer(BaseMCPServer):
    """MCP Server for Hunter."""

    name: str = "hunter"
    category: str = "Hunter"
    description: str = "Hunter integration for email finding and verification."
    scope: str = "hunter_access"
    client_service = IntegrationAppClient()
    base_url = "/hunter"

    def _register_prompts(self) -> None:
        """Register all Hunter prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Hunter tools with the MCP server."""

        get_contact_info_output = mcp_output(
            description="List of contacts with verified email addresses, name, job title, company, and confidence score",
            examples=[''])
        @self._mcp.tool(
            description="Find and verify contact information using Hunter's email finder.",
            meta=mcp_meta("get_contact_info"),
            structured_output=True
        )
        async def get_contact_info(
            domain: Annotated[Optional[str], Field(description="Company domain")] = None,
            first_name: Annotated[Optional[str], Field(description="Contact's first name")] = None,
            last_name: Annotated[Optional[str], Field(description="Contact's last name")] = None,
            email: Annotated[Optional[str], Field(description="Email address to verify")] = None,
            job_title: Annotated[Optional[str], Field(description="Contact's job title")] = None,
            company: Annotated[Optional[str], Field(description="Company name")] = None,
            linkedin: Annotated[Optional[str], Field(description="LinkedIn profile URL")] = None,
            per_page: Annotated[Optional[int], Field(description="Number of contacts per page")] = 10
        ) -> get_contact_info_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/contacts/",
                data={
                    "domain": domain,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "job_title": job_title,
                    "company": company,
                    "linkedin": linkedin,
                    "per_page": per_page
                },
                context=context
            )
            return [json.dumps(response.data)]
