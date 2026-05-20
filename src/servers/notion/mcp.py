import json
import logging
from typing import Annotated, Optional, Any, Dict, List
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class NotionServer(BaseMCPServer):
    """MCP Server for Notion."""

    name: str = "notion"
    category: str = "Notion"
    description: str = "Notion integration for workspace collaboration and knowledge management."
    scope: str = "notion_access_key"
    client_service = IntegrationAppClient()
    base_url = "/notion"

    def _register_prompts(self) -> None:
        """Register all Notion prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Notion tools with the MCP server."""

        search_output = mcp_output(
            description="Search results from Notion workspace",
            examples=[''])
        @self._mcp.tool(
            description="Search Notion workspace for pages and databases.",
            meta=mcp_meta("search"),
            structured_output=True
        )
        async def search(
            query: Annotated[Optional[str], Field(description="Search query")] = "",
            filter_type: Annotated[Optional[str], Field(description="Filter type: page or database")] = None,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = 10
        ) -> search_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/search/",
                data={
                    "query": query,
                    "filter_type": filter_type,
                    "page_size": page_size,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_database_output = mcp_output(
            description="Database schema and properties",
            examples=[''])
        @self._mcp.tool(
            description="Get Notion database details and schema.",
            meta=mcp_meta("get_database"),
            structured_output=True
        )
        async def get_database(
            database_id: Annotated[str, Field(description="Database ID")]
        ) -> get_database_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/database/",
                data={"database_id": database_id},
                context=context
            )
            return [json.dumps(response.data)]

        query_database_output = mcp_output(
            description="Database query results with filtered and sorted pages",
            examples=[''])
        @self._mcp.tool(
            description="Query a Notion database with filters and sorts.",
            meta=mcp_meta("query_database"),
            structured_output=True
        )
        async def query_database(
            database_id: Annotated[str, Field(description="Database ID")],
            filter: Annotated[Optional[Dict[str, Any]], Field(description="Filter object for query")] = None,
            sorts: Annotated[Optional[List[Dict[str, Any]]], Field(description="Sort configuration")] = None,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = 100
        ) -> query_database_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/database/query/",
                data={
                    "database_id": database_id,
                    "filter": filter,
                    "sorts": sorts,
                    "page_size": page_size,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_page_output = mcp_output(
            description="Page details with properties and content",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a Notion page.",
            meta=mcp_meta("get_page"),
            structured_output=True
        )
        async def get_page(
            page_id: Annotated[str, Field(description="Page ID")]
        ) -> get_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/page/",
                data={"page_id": page_id},
                context=context
            )
            return [json.dumps(response.data)]

        create_page_output = mcp_output(
            description="Created page details with ID and properties",
            examples=[''])
        @self._mcp.tool(
            description="Create a new page in Notion.",
            meta=mcp_meta("create_page"),
            structured_output=True
        )
        async def create_page(
            parent: Annotated[Dict[str, Any], Field(description="Parent object (database_id or page_id)")],
            properties: Annotated[Dict[str, Any], Field(description="Page properties")],
            children: Annotated[Optional[List[Dict[str, Any]]], Field(description="Child blocks content")] = None
        ) -> create_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/page/create/",
                data={
                    "parent": parent,
                    "properties": properties,
                    "children": children,
                },
                context=context
            )
            return [json.dumps(response.data)]

        update_page_output = mcp_output(
            description="Updated page details",
            examples=[''])
        @self._mcp.tool(
            description="Update properties of a Notion page.",
            meta=mcp_meta("update_page"),
            structured_output=True
        )
        async def update_page(
            page_id: Annotated[str, Field(description="Page ID")],
            properties: Annotated[Dict[str, Any], Field(description="Properties to update")]
        ) -> update_page_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/page/update/",
                data={
                    "page_id": page_id,
                    "properties": properties,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_block_children_output = mcp_output(
            description="List of child blocks for the specified block",
            examples=[''])
        @self._mcp.tool(
            description="Get children blocks of a Notion block or page.",
            meta=mcp_meta("get_block_children"),
            structured_output=True
        )
        async def get_block_children(
            block_id: Annotated[str, Field(description="Block or page ID")],
            page_size: Annotated[Optional[int], Field(description="Number of blocks per page")] = 100
        ) -> get_block_children_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/blocks/children/",
                data={
                    "block_id": block_id,
                    "page_size": page_size,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_users_output = mcp_output(
            description="List of users in the Notion workspace",
            examples=[''])
        @self._mcp.tool(
            description="Get list of users in the Notion workspace.",
            meta=mcp_meta("get_users"),
            structured_output=True
        )
        async def get_users() -> get_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]
