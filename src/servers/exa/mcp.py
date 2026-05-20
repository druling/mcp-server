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
class ExaServer(BaseMCPServer):
    """MCP Server for Exa."""

    name: str = "exa"
    category: str = "Exa"
    description: str = "Exa integration for neural web search and content discovery."
    scope: str = "exa_access_key"
    client_service = IntegrationAppClient()
    base_url = "/exa"

    def _register_prompts(self) -> None:
        """Register all Exa prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Exa tools with the MCP server."""

        search_output = mcp_output(
            description="Search results with URLs, titles, and optional content",
            examples=[''])
        @self._mcp.tool(
            description="Search the web using Exa's neural search engine.",
            meta=mcp_meta("search"),
            structured_output=True
        )
        async def search(
            query: Annotated[str, Field(description="Search query")],
            num_results: Annotated[Optional[int], Field(description="Number of results to return")] = 10,
            use_autoprompt: Annotated[Optional[bool], Field(description="Enhance query with autoprompt")] = False,
            type: Annotated[Optional[str], Field(description="Search type: auto, keyword, or neural")] = "auto",
            include_domains: Annotated[Optional[List[str]], Field(description="List of domains to include")] = None,
            exclude_domains: Annotated[Optional[List[str]], Field(description="List of domains to exclude")] = None,
            start_published_date: Annotated[Optional[str], Field(description="Start date for published content (ISO format)")] = None,
            end_published_date: Annotated[Optional[str], Field(description="End date for published content (ISO format)")] = None,
            include_text: Annotated[Optional[bool], Field(description="Include full text content in results")] = False
        ) -> search_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/search/",
                data={
                    "query": query,
                    "num_results": num_results,
                    "use_autoprompt": use_autoprompt,
                    "type": type,
                    "include_domains": include_domains,
                    "exclude_domains": exclude_domains,
                    "start_published_date": start_published_date,
                    "end_published_date": end_published_date,
                    "include_text": include_text,
                },
                context=context
            )
            return [json.dumps(response.data)]

        find_similar_output = mcp_output(
            description="Similar content results based on the provided URL",
            examples=[''])
        @self._mcp.tool(
            description="Find content similar to a given URL.",
            meta=mcp_meta("find_similar"),
            structured_output=True
        )
        async def find_similar(
            url: Annotated[str, Field(description="URL to find similar content for")],
            num_results: Annotated[Optional[int], Field(description="Number of results to return")] = 10,
            include_domains: Annotated[Optional[List[str]], Field(description="List of domains to include")] = None,
            exclude_domains: Annotated[Optional[List[str]], Field(description="List of domains to exclude")] = None,
            include_text: Annotated[Optional[bool], Field(description="Include full text content in results")] = False
        ) -> find_similar_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/find-similar/",
                data={
                    "url": url,
                    "num_results": num_results,
                    "include_domains": include_domains,
                    "exclude_domains": exclude_domains,
                    "include_text": include_text,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_contents_output = mcp_output(
            description="Full content, highlights, or summaries for the requested IDs",
            examples=[''])
        @self._mcp.tool(
            description="Get full content for specific Exa search result IDs.",
            meta=mcp_meta("get_contents"),
            structured_output=True
        )
        async def get_contents(
            ids: Annotated[List[str], Field(description="List of content IDs to retrieve")],
            text: Annotated[Optional[bool], Field(description="Include full text content")] = True,
            highlights: Annotated[Optional[bool], Field(description="Include content highlights")] = False,
            summary: Annotated[Optional[bool], Field(description="Include content summary")] = False
        ) -> get_contents_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/contents/",
                data={
                    "ids": ids,
                    "text": text,
                    "highlights": highlights,
                    "summary": summary,
                },
                context=context
            )
            return [json.dumps(response.data)]
