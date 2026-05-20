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
class GhostServer(BaseMCPServer):
    """MCP Server for Ghost."""

    name: str = "ghost"
    category: str = "Ghost"
    description: str = "Ghost CMS integration for managing blog posts, pages, members, and tags."
    scope: str = "ghost_access_key"
    client_service = IntegrationAppClient()
    base_url = "/ghost"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_posts_output = mcp_output(
            description="List of Ghost posts with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List posts in Ghost CMS.",
            meta=mcp_meta("list_posts"),
            structured_output=True
        )
        async def list_posts(
            limit: Annotated[Optional[int], Field(description="Maximum number of posts")] = 15,
            page: Annotated[Optional[int], Field(description="Page number")] = 1,
            status: Annotated[Optional[str], Field(description="Filter by status (published, draft, scheduled, all)")] = "all"
        ) -> list_posts_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/posts/",
                data={"limit": limit, "page": page, "status": status},
                context=context
            )
            return [json.dumps(response.data)]

        get_post_output = mcp_output(
            description="Detailed information about a specific Ghost post",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Ghost post by ID.",
            meta=mcp_meta("get_post"),
            structured_output=True
        )
        async def get_post(
            post_id: Annotated[str, Field(description="Post ID")]
        ) -> get_post_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/posts/get/",
                data={"post_id": post_id},
                context=context
            )
            return [json.dumps(response.data)]

        create_post_output = mcp_output(
            description="Created post details with ID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new post in Ghost CMS.",
            meta=mcp_meta("create_post"),
            structured_output=True
        )
        async def create_post(
            title: Annotated[str, Field(description="Post title")],
            html: Annotated[Optional[str], Field(description="Post content as HTML")] = None,
            status: Annotated[Optional[str], Field(description="Post status (draft, published)")] = "draft",
            tags: Annotated[Optional[List], Field(description="List of tag objects with name or slug")] = None
        ) -> create_post_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/posts/create/",
                data={"title": title, "html": html, "status": status, "tags": tags},
                context=context
            )
            return [json.dumps(response.data)]

        update_post_output = mcp_output(
            description="Updated post details",
            examples=[''])
        @self._mcp.tool(
            description="Update an existing Ghost post.",
            meta=mcp_meta("update_post"),
            structured_output=True
        )
        async def update_post(
            post_id: Annotated[str, Field(description="Post ID to update")],
            updated_at: Annotated[str, Field(description="Current updated_at value for conflict detection (ISO timestamp)")],
            title: Annotated[Optional[str], Field(description="New post title")] = None,
            html: Annotated[Optional[str], Field(description="New post content as HTML")] = None,
            status: Annotated[Optional[str], Field(description="New post status")] = None
        ) -> update_post_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/posts/update/",
                data={"post_id": post_id, "updated_at": updated_at, "title": title, "html": html, "status": status},
                context=context
            )
            return [json.dumps(response.data)]

        list_pages_output = mcp_output(
            description="List of Ghost pages",
            examples=[''])
        @self._mcp.tool(
            description="List pages in Ghost CMS.",
            meta=mcp_meta("list_pages"),
            structured_output=True
        )
        async def list_pages(
            limit: Annotated[Optional[int], Field(description="Maximum number of pages")] = 15,
            page: Annotated[Optional[int], Field(description="Page number")] = 1
        ) -> list_pages_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/pages/",
                data={"limit": limit, "page": page},
                context=context
            )
            return [json.dumps(response.data)]

        list_members_output = mcp_output(
            description="List of Ghost members/subscribers",
            examples=[''])
        @self._mcp.tool(
            description="List members/subscribers in Ghost.",
            meta=mcp_meta("list_members"),
            structured_output=True
        )
        async def list_members(
            limit: Annotated[Optional[int], Field(description="Maximum number of members")] = 15,
            page: Annotated[Optional[int], Field(description="Page number")] = 1,
            filter: Annotated[Optional[str], Field(description="Filter expression (e.g. status:free)")] = None
        ) -> list_members_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/members/",
                data={"limit": limit, "page": page, "filter": filter},
                context=context
            )
            return [json.dumps(response.data)]

        list_tags_output = mcp_output(
            description="List of Ghost tags",
            examples=[''])
        @self._mcp.tool(
            description="List tags in Ghost CMS.",
            meta=mcp_meta("list_tags"),
            structured_output=True
        )
        async def list_tags(
            limit: Annotated[Optional[int], Field(description="Maximum number of tags")] = 50,
            page: Annotated[Optional[int], Field(description="Page number")] = 1
        ) -> list_tags_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/tags/",
                data={"limit": limit, "page": page},
                context=context
            )
            return [json.dumps(response.data)]

        get_site_output = mcp_output(
            description="Ghost site configuration and metadata",
            examples=[''])
        @self._mcp.tool(
            description="Get Ghost site information.",
            meta=mcp_meta("get_site"),
            structured_output=True
        )
        async def get_site() -> get_site_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/site/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]
