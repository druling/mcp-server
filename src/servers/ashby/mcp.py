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
class AshbyServer(BaseMCPServer):
    """MCP Server for Ashby."""

    name: str = "ashby"
    category: str = "Ashby"
    description: str = "Ashby integration for recruiting and applicant tracking."
    scope: str = "ashby_access_key"
    client_service = IntegrationAppClient()
    base_url = "/ashby"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_candidates_output = mcp_output(
            description="List of candidates with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all candidates in Ashby.",
            meta=mcp_meta("list_candidates"),
            structured_output=True
        )
        async def list_candidates(
            cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of candidates")] = 100
        ) -> list_candidates_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/candidates/",
                data={"cursor": cursor, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_candidate_output = mcp_output(
            description="Detailed information about a specific candidate",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific candidate by ID.",
            meta=mcp_meta("get_candidate"),
            structured_output=True
        )
        async def get_candidate(
            candidate_id: Annotated[str, Field(description="Candidate ID")]
        ) -> get_candidate_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/candidates/get/",
                data={"candidate_id": candidate_id},
                context=context
            )
            return [json.dumps(response.data)]

        search_candidates_output = mcp_output(
            description="Candidates matching the search criteria",
            examples=[''])
        @self._mcp.tool(
            description="Search candidates by email or name.",
            meta=mcp_meta("search_candidates"),
            structured_output=True
        )
        async def search_candidates(
            email: Annotated[Optional[str], Field(description="Email address to search")] = None,
            name: Annotated[Optional[str], Field(description="Name to search")] = None
        ) -> search_candidates_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/candidates/search/",
                data={"email": email, "name": name},
                context=context
            )
            return [json.dumps(response.data)]

        create_candidate_output = mcp_output(
            description="Created candidate details with ID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new candidate in Ashby.",
            meta=mcp_meta("create_candidate"),
            structured_output=True
        )
        async def create_candidate(
            name: Annotated[str, Field(description="Candidate full name")],
            email: Annotated[Optional[str], Field(description="Candidate email address")] = None,
            phone_number: Annotated[Optional[str], Field(description="Candidate phone number")] = None
        ) -> create_candidate_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/candidates/create/",
                data={"name": name, "email": email, "phone_number": phone_number},
                context=context
            )
            return [json.dumps(response.data)]

        list_jobs_output = mcp_output(
            description="List of all job postings",
            examples=[''])
        @self._mcp.tool(
            description="List all jobs in Ashby.",
            meta=mcp_meta("list_jobs"),
            structured_output=True
        )
        async def list_jobs(
            cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of jobs")] = 100
        ) -> list_jobs_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/jobs/",
                data={"cursor": cursor, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_job_output = mcp_output(
            description="Detailed information about a specific job",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific job by ID.",
            meta=mcp_meta("get_job"),
            structured_output=True
        )
        async def get_job(
            job_id: Annotated[str, Field(description="Job ID")]
        ) -> get_job_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/jobs/get/",
                data={"job_id": job_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_applications_output = mcp_output(
            description="List of applications with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all applications in Ashby.",
            meta=mcp_meta("list_applications"),
            structured_output=True
        )
        async def list_applications(
            cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of applications")] = 100
        ) -> list_applications_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/applications/",
                data={"cursor": cursor, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_application_output = mcp_output(
            description="Detailed information about a specific application",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific application by ID.",
            meta=mcp_meta("get_application"),
            structured_output=True
        )
        async def get_application(
            application_id: Annotated[str, Field(description="Application ID")]
        ) -> get_application_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/applications/get/",
                data={"application_id": application_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_users_output = mcp_output(
            description="List of users in Ashby",
            examples=[''])
        @self._mcp.tool(
            description="List all users in Ashby.",
            meta=mcp_meta("list_users"),
            structured_output=True
        )
        async def list_users() -> list_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_departments_output = mcp_output(
            description="List of departments in Ashby",
            examples=[''])
        @self._mcp.tool(
            description="List all departments in Ashby.",
            meta=mcp_meta("list_departments"),
            structured_output=True
        )
        async def list_departments() -> list_departments_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/departments/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]
