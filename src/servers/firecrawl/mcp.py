import json
import logging
from typing import Annotated, Optional, List, Dict, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class FirecrawlServer(BaseMCPServer):
    """MCP Server for Firecrawl."""

    name: str = "firecrawl"
    category: str = "Firecrawl"
    description: str = "Firecrawl integration for web scraping and data extraction."
    scope: str = "firecrawl_access"
    client_service = IntegrationAppClient()
    base_url = "/firecrawl"

    def _register_prompts(self) -> None:
        """Register all Firecrawl prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Firecrawl tools with the MCP server."""

        scrape_output = mcp_output(
            description="Scraped page content including markdown text, HTML, metadata, and extracted links",
            examples=[''])
        @self._mcp.tool(
            description="Scrape a single web page to extract content, text, and links.",
            meta=mcp_meta("scrape"),
            structured_output=True
        )
        async def scrape(
            url: Annotated[str, Field(description="URL to scrape")],
            timeout: Annotated[Optional[int], Field(description="Timeout in seconds")] = None,
            stealth: Annotated[Optional[bool], Field(description="Use stealth mode to avoid detection")] = False,
            actions: Annotated[Optional[List[Dict[str, Any]]], Field(description="Browser actions to perform")] = None,
            mobile: Annotated[Optional[bool], Field(description="Use mobile user agent")] = False,
            all_links: Annotated[Optional[bool], Field(description="Extract all links from the page")] = True,
            raw_html: Annotated[Optional[bool], Field(description="Include raw HTML in response")] = False
        ) -> scrape_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/scrape/",
                data={
                    "url": url,
                    "timeout": timeout,
                    "stealth": stealth,
                    "actions": actions,
                    "mobile": mobile,
                    "all_links": all_links,
                    "raw_html": raw_html
                },
                context=context
            )
            return [json.dumps(response.data)]

        crawl_output = mcp_output(
            description="List of scraped pages with URL, content, and links from the crawled website",
            examples=[''])
        @self._mcp.tool(
            description="Crawl a website to scrape multiple pages starting from a root URL.",
            meta=mcp_meta("crawl"),
            structured_output=True
        )
        async def crawl(
            url: Annotated[str, Field(description="Root URL to start crawling from")],
            depth: Annotated[Optional[int], Field(description="Maximum crawl depth")] = 1,
            allow_external: Annotated[Optional[bool], Field(description="Allow crawling external links")] = True
        ) -> crawl_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/crawl/",
                data={
                    "url": url,
                    "depth": depth,
                    "allow_external": allow_external
                },
                context=context
            )
            return [json.dumps(response.data)]

        search_jobs_output = mcp_output(
            description="List of job listings with title, company, location, description, and application URL",
            examples=[''])
        @self._mcp.tool(
            description="Search for job listings from various sources.",
            meta=mcp_meta("search_jobs"),
            structured_output=True
        )
        async def search_jobs(
            source: Annotated[str, Field(description="Job board source (e.g., 'indeed', 'linkedin')")],
            keyword: Annotated[str, Field(description="Job search keyword or title")],
            location: Annotated[str, Field(description="Job location")],
            max_jobs: Annotated[Optional[int], Field(description="Maximum number of jobs to retrieve")] = 30
        ) -> search_jobs_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/jobs/search/",
                data={
                    "source": source,
                    "keyword": keyword,
                    "location": location,
                    "max_jobs": max_jobs
                },
                context=context
            )
            return [json.dumps(response.data)]
