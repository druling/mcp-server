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
class ConfluenceServer(BaseMCPServer):
    """MCP Server for Confluence."""

    name: str = "confluence"
    category: str = "Confluence"
    description: str = "Confluence integration for managing wiki pages and documentation."
    scope: str = "confluence_access"
    client_service = IntegrationAppClient()
    base_url = "/atlassian/confluence"

    def _register_prompts(self) -> None:
        """Register all Confluence prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Confluence tools with the MCP server."""

        get_spaces_output = mcp_output(
            description="List of Confluence spaces with key, name, and type",
            examples=[''])
        @self._mcp.tool(
            description="Get list of Confluence spaces.",
            meta=mcp_meta("get_spaces"),
            structured_output=True
        )
        async def get_spaces(
            space_type: Annotated[Optional[str], Field(description="Space type filter (global, personal)")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of spaces to retrieve")] = 25,
            start: Annotated[Optional[int], Field(description="Starting index for pagination")] = 0
        ) -> get_spaces_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/spaces/",
                data={
                    "space_type": space_type,
                    "limit": limit,
                    "start": start,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_space_output = mcp_output(
            description="Detailed information about a specific Confluence space",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Confluence space.",
            meta=mcp_meta("get_space"),
            structured_output=True
        )
        async def get_space(
            space_key: Annotated[str, Field(description="Space key")]
        ) -> get_space_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/spaces/get/",
                data={"space_key": space_key},
                context=context
            )
            return [json.dumps(response.data)]

        get_pages_output = mcp_output(
            description="List of pages in the specified Confluence space",
            examples=[''])
        @self._mcp.tool(
            description="Get pages in a Confluence space.",
            meta=mcp_meta("get_pages"),
            structured_output=True
        )
        async def get_pages(
            space_key: Annotated[str, Field(description="Space key")],
            limit: Annotated[Optional[int], Field(description="Maximum number of pages to retrieve")] = 25,
            start: Annotated[Optional[int], Field(description="Starting index for pagination")] = 0,
            expand: Annotated[Optional[List[str]], Field(description="List of expansion properties")] = None
        ) -> get_pages_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/",
                data={
                    "space_key": space_key,
                    "limit": limit,
                    "start": start,
                    "expand": expand,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_page_output = mcp_output(
            description="Detailed information about a specific Confluence page",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Confluence page.",
            meta=mcp_meta("get_page"),
            structured_output=True
        )
        async def get_page(
            page_id: Annotated[str, Field(description="Page ID")],
            expand: Annotated[Optional[str], Field(description="Expansion properties (e.g., 'body.storage')")] = "body.storage"
        ) -> get_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/get/",
                data={
                    "page_id": page_id,
                    "expand": expand,
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_page_output = mcp_output(
            description="Created page details with ID and URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Confluence page.",
            meta=mcp_meta("create_page"),
            structured_output=True
        )
        async def create_page(
            space_key: Annotated[str, Field(description="Space key")],
            title: Annotated[str, Field(description="Page title")],
            body: Annotated[Optional[str], Field(description="Page content body")] = "",
            parent_id: Annotated[Optional[str], Field(description="Parent page ID")] = None,
            representation: Annotated[Optional[str], Field(description="Body representation format (storage, wiki)")] = "storage"
        ) -> create_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/create/",
                data={
                    "space_key": space_key,
                    "title": title,
                    "body": body,
                    "parent_id": parent_id,
                    "representation": representation,
                },
                context=context
            )
            return [json.dumps(response.data)]

        update_page_output = mcp_output(
            description="Updated page details",
            examples=[''])
        @self._mcp.tool(
            description="Update a Confluence page.",
            meta=mcp_meta("update_page"),
            structured_output=True
        )
        async def update_page(
            page_id: Annotated[str, Field(description="Page ID")],
            title: Annotated[str, Field(description="Page title")],
            version_number: Annotated[int, Field(description="Current version number (required for updates)")],
            body: Annotated[Optional[str], Field(description="Page content body")] = "",
            representation: Annotated[Optional[str], Field(description="Body representation format (storage, wiki)")] = "storage"
        ) -> update_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/update/",
                data={
                    "page_id": page_id,
                    "title": title,
                    "body": body,
                    "version_number": version_number,
                    "representation": representation,
                },
                context=context
            )
            return [json.dumps(response.data)]

        search_content_output = mcp_output(
            description="Search results from Confluence",
            examples=[''])
        @self._mcp.tool(
            description="Search Confluence content using CQL (Confluence Query Language).",
            meta=mcp_meta("search_content"),
            structured_output=True
        )
        async def search_content(
            cql: Annotated[str, Field(description="CQL query string")],
            limit: Annotated[Optional[int], Field(description="Maximum number of results")] = 25,
            start: Annotated[Optional[int], Field(description="Starting index for pagination")] = 0,
            expand: Annotated[Optional[List[str]], Field(description="List of expansion properties")] = None
        ) -> search_content_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/search/",
                data={
                    "cql": cql,
                    "limit": limit,
                    "start": start,
                    "expand": expand,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_page_children_output = mcp_output(
            description="List of child pages",
            examples=[''])
        @self._mcp.tool(
            description="Get child pages of a Confluence page.",
            meta=mcp_meta("get_page_children"),
            structured_output=True
        )
        async def get_page_children(
            page_id: Annotated[str, Field(description="Page ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of children to retrieve")] = 25,
            start: Annotated[Optional[int], Field(description="Starting index for pagination")] = 0
        ) -> get_page_children_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/children/",
                data={
                    "page_id": page_id,
                    "limit": limit,
                    "start": start,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_comments_output = mcp_output(
            description="List of comments on the page",
            examples=[''])
        @self._mcp.tool(
            description="Get comments on a Confluence page.",
            meta=mcp_meta("get_comments"),
            structured_output=True
        )
        async def get_comments(
            page_id: Annotated[str, Field(description="Page ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of comments to retrieve")] = 25
        ) -> get_comments_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/comments/",
                data={
                    "page_id": page_id,
                    "limit": limit,
                },
                context=context
            )
            return [json.dumps(response.data)]

        add_comment_output = mcp_output(
            description="Created comment details",
            examples=[''])
        @self._mcp.tool(
            description="Add a comment to a Confluence page.",
            meta=mcp_meta("add_comment"),
            structured_output=True
        )
        async def add_comment(
            page_id: Annotated[str, Field(description="Page ID")],
            comment_body: Annotated[str, Field(description="Comment text")],
            representation: Annotated[Optional[str], Field(description="Body representation format (storage, wiki)")] = "storage"
        ) -> add_comment_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/comments/add/",
                data={
                    "page_id": page_id,
                    "comment_body": comment_body,
                    "representation": representation,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_attachments_output = mcp_output(
            description="List of attachments on the page",
            examples=[''])
        @self._mcp.tool(
            description="Get attachments on a Confluence page.",
            meta=mcp_meta("get_attachments"),
            structured_output=True
        )
        async def get_attachments(
            page_id: Annotated[str, Field(description="Page ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of attachments to retrieve")] = 25
        ) -> get_attachments_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/attachments/",
                data={
                    "page_id": page_id,
                    "limit": limit,
                },
                context=context
            )
            return [json.dumps(response.data)]
