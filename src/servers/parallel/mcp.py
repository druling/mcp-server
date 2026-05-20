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
class ParallelServer(BaseMCPServer):
    """MCP Server for Parallel Markets."""

    name: str = "parallel"
    category: str = "Parallel"
    description: str = "Parallel Markets integration for investor accreditation and identity verification."
    scope: str = "parallel_access_key"
    client_service = IntegrationAppClient()
    base_url = "/parallel"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        get_token_info_output = mcp_output(
            description="Current API token info and connected account details",
            examples=[''])
        @self._mcp.tool(
            description="Get info about the current Parallel Markets API token.",
            meta=mcp_meta("get_token_info"),
            structured_output=True
        )
        async def get_token_info() -> get_token_info_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/token/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_accreditations_output = mcp_output(
            description="List of accreditation records with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List accreditation records from Parallel Markets.",
            meta=mcp_meta("list_accreditations"),
            structured_output=True
        )
        async def list_accreditations(
            limit: Annotated[Optional[int], Field(description="Maximum number of records")] = 20,
            starting_after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_accreditations_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/accreditations/",
                data={"limit": limit, "starting_after": starting_after},
                context=context
            )
            return [json.dumps(response.data)]

        get_accreditation_output = mcp_output(
            description="Detailed information about a specific accreditation record",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific accreditation record by ID.",
            meta=mcp_meta("get_accreditation"),
            structured_output=True
        )
        async def get_accreditation(
            accreditation_id: Annotated[str, Field(description="Accreditation ID")]
        ) -> get_accreditation_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/accreditations/get/",
                data={"accreditation_id": accreditation_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_individuals_output = mcp_output(
            description="List of individual identity records with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List individual identity records from Parallel Markets.",
            meta=mcp_meta("list_individuals"),
            structured_output=True
        )
        async def list_individuals(
            limit: Annotated[Optional[int], Field(description="Maximum number of records")] = 20,
            starting_after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_individuals_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/individuals/",
                data={"limit": limit, "starting_after": starting_after},
                context=context
            )
            return [json.dumps(response.data)]

        get_individual_output = mcp_output(
            description="Detailed information about a specific individual",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific individual identity record by ID.",
            meta=mcp_meta("get_individual"),
            structured_output=True
        )
        async def get_individual(
            individual_id: Annotated[str, Field(description="Individual ID")]
        ) -> get_individual_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/individuals/get/",
                data={"individual_id": individual_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_businesses_output = mcp_output(
            description="List of business entity records with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List business entity records from Parallel Markets.",
            meta=mcp_meta("list_businesses"),
            structured_output=True
        )
        async def list_businesses(
            limit: Annotated[Optional[int], Field(description="Maximum number of records")] = 20,
            starting_after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_businesses_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/businesses/",
                data={"limit": limit, "starting_after": starting_after},
                context=context
            )
            return [json.dumps(response.data)]

        get_business_output = mcp_output(
            description="Detailed information about a specific business entity",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific business entity record by ID.",
            meta=mcp_meta("get_business"),
            structured_output=True
        )
        async def get_business(
            business_id: Annotated[str, Field(description="Business entity ID")]
        ) -> get_business_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/businesses/get/",
                data={"business_id": business_id},
                context=context
            )
            return [json.dumps(response.data)]
