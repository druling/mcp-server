import json
import logging
from typing import Annotated, Optional, Dict
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GoogleSlideServer(BaseMCPServer):
    """MCP Server for Google Slides."""

    name: str = "google_slides"
    category: str = "Google Slides"
    description: str = "Google Slides integration for managing presentations."
    scope: str = "google_slides_access"
    backend_service = BackendClient()
    base_url = "/google/slides"

    def _register_prompts(self) -> None:
        """Register all Google Slides prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Google Slides tools with the MCP server."""

        read_slides_output = mcp_output(
            description="List of slides with text content, notes, and thumbnail image URLs",
            examples=[''])
        @self._mcp.tool(
            description="Read slides from a Google Slides presentation.",
            meta=mcp_meta("read_slides"),
            structured_output=True
        )
        async def read_slides(
            presentation_id: Annotated[Optional[str], Field(description="The ID of the presentation to read")] = None,
            presentation_url: Annotated[Optional[str], Field(description="The URL of the presentation to read")] = None,
            index_start: Annotated[Optional[int], Field(description="Starting slide index (inclusive)")] = None,
            index_end: Annotated[Optional[int], Field(description="Ending slide index (inclusive)")] = None,
            thumbnail_size: Annotated[Optional[str], Field(description="Size of thumbnails: 'SMALL', 'MEDIUM', 'LARGE'")] = "LARGE"
        ) -> read_slides_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/read/",
                data={
                    "presentation_id": presentation_id,
                    "presentation_url": presentation_url,
                    "index_start": index_start,
                    "index_end": index_end,
                    "thumbnail_size": thumbnail_size
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_from_template_output = mcp_output(
            description="New presentation details created from template, including presentation ID and URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a presentation from a template with placeholder replacements.",
            meta=mcp_meta("create_from_template"),
            structured_output=True
        )
        async def create_from_template(
            new_title: Annotated[str, Field(description="Title for the new presentation")],
            template_id: Annotated[Optional[str], Field(description="The ID of the template presentation")] = None,
            template_url: Annotated[Optional[str], Field(description="The URL of the template presentation")] = None,
            replacements: Annotated[Optional[Dict[str, str]], Field(description="Dictionary of placeholder replacements (e.g., {'{{title}}': 'My Title'})")] = None
        ) -> create_from_template_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create_from_template/",
                data={
                    "template_id": template_id,
                    "template_url": template_url,
                    "replacements": replacements or {},
                    "new_title": new_title
                },
                context=context
            )
            return [json.dumps(response.data)]

        find_placeholders_output = mcp_output(
            description="List of all placeholder strings found in the template presentation",
            examples=[''])
        @self._mcp.tool(
            description="Find all placeholders in a Google Slides template.",
            meta=mcp_meta("find_placeholders"),
            structured_output=True
        )
        async def find_placeholders(
            template_id: Annotated[Optional[str], Field(description="The ID of the template presentation")] = None,
            template_url: Annotated[Optional[str], Field(description="The URL of the template presentation")] = None
        ) -> find_placeholders_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/find_placeholders/",
                data={
                    "template_id": template_id,
                    "template_url": template_url
                },
                context=context
            )
            return [json.dumps(response.data)]
