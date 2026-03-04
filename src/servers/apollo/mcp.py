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
class ApolloServer(BaseMCPServer):
    """MCP Server for Apollo."""

    name: str = "apollo"
    category: str = "Apollo"
    description: str = "Apollo integration for accessing contact and company data."
    scope: str = "apollo_access"
    client_service = IntegrationAppClient()
    base_url = "/apollo"

    def _register_prompts(self) -> None:
        """Register all Apollo prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Apollo tools with the MCP server."""

        search_companies_output = mcp_output(
            description="List of companies matching the search criteria with name, domain, industry, size, and location",
            examples=[''])
        @self._mcp.tool(
            description="Search for companies in Apollo by name, keyword, size, location, or industry.",
            meta=mcp_meta("search_companies"),
            structured_output=True
        )
        async def search_companies(
            name: Annotated[Optional[str], Field(description="Company name to search for")] = None,
            keyword: Annotated[Optional[str], Field(description="Keyword to search in company descriptions")] = None,
            size_range: Annotated[Optional[str], Field(description="Company size range (e.g., '1-10', '11-50')")] = None,
            location: Annotated[Optional[str], Field(description="Company location")] = None,
            industry: Annotated[Optional[str], Field(description="Company industry")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of companies to retrieve")] = 10
        ) -> search_companies_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/companies/search/",
                data={
                    "name": name,
                    "keyword": keyword,
                    "size_range": size_range,
                    "location": location,
                    "industry": industry,
                    "limit": limit
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_company_by_domain_output = mcp_output(
            description="Company profile with name, industry, size, location, revenue, and employee count",
            examples=[''])
        @self._mcp.tool(
            description="Get company information by domain name.",
            meta=mcp_meta("get_company_by_domain"),
            structured_output=True
        )
        async def get_company_by_domain(
            domain: Annotated[str, Field(description="Company domain (e.g., 'example.com')")]
        ) -> get_company_by_domain_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/company/domain/",
                data={"domain": domain},
                context=context
            )
            return [json.dumps(response.data)]

        get_contact_info_output = mcp_output(
            description="List of contacts with name, email, job title, company, LinkedIn profile, and phone number",
            examples=[''])
        @self._mcp.tool(
            description="Get contact information from Apollo by domain, name, job title, or LinkedIn profile.",
            meta=mcp_meta("get_contact_info"),
            structured_output=True
        )
        async def get_contact_info(
            domain: Annotated[Optional[str], Field(description="Company domain")] = None,
            first_name: Annotated[Optional[str], Field(description="Contact's first name")] = None,
            last_name: Annotated[Optional[str], Field(description="Contact's last name")] = None,
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
                    "job_title": job_title,
                    "company": company,
                    "linkedin": linkedin,
                    "per_page": per_page
                },
                context=context
            )
            return [json.dumps(response.data)]
