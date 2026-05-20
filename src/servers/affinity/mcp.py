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
class AffinityServer(BaseMCPServer):
    """MCP Server for Affinity."""

    name: str = "affinity"
    category: str = "Affinity"
    description: str = "Affinity CRM integration for relationship intelligence and deal tracking."
    scope: str = "affinity_access_key"
    client_service = IntegrationAppClient()
    base_url = "/affinity"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        get_persons_output = mcp_output(
            description="List of persons matching the search criteria",
            examples=[''])
        @self._mcp.tool(
            description="Search or list all persons in Affinity.",
            meta=mcp_meta("get_persons"),
            structured_output=True
        )
        async def get_persons(
            term: Annotated[Optional[str], Field(description="Search term to filter persons")] = None,
            with_interaction_dates: Annotated[Optional[bool], Field(description="Include interaction dates")] = False,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = None,
            page_token: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> get_persons_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/persons/",
                data={"term": term, "with_interaction_dates": with_interaction_dates, "page_size": page_size, "page_token": page_token},
                context=context
            )
            return [json.dumps(response.data)]

        get_person_output = mcp_output(
            description="Detailed information about a specific person",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific person by ID.",
            meta=mcp_meta("get_person"),
            structured_output=True
        )
        async def get_person(
            person_id: Annotated[int, Field(description="Person ID")]
        ) -> get_person_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/persons/get/",
                data={"person_id": person_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_organizations_output = mcp_output(
            description="List of organizations matching the search criteria",
            examples=[''])
        @self._mcp.tool(
            description="Search or list all organizations in Affinity.",
            meta=mcp_meta("get_organizations"),
            structured_output=True
        )
        async def get_organizations(
            term: Annotated[Optional[str], Field(description="Search term to filter organizations")] = None,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = None,
            page_token: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> get_organizations_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/organizations/",
                data={"term": term, "page_size": page_size, "page_token": page_token},
                context=context
            )
            return [json.dumps(response.data)]

        get_organization_output = mcp_output(
            description="Detailed information about a specific organization",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific organization by ID.",
            meta=mcp_meta("get_organization"),
            structured_output=True
        )
        async def get_organization(
            organization_id: Annotated[int, Field(description="Organization ID")]
        ) -> get_organization_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/organizations/get/",
                data={"organization_id": organization_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_lists_output = mcp_output(
            description="All Affinity lists with ID and name",
            examples=[''])
        @self._mcp.tool(
            description="Get all Affinity lists.",
            meta=mcp_meta("get_lists"),
            structured_output=True
        )
        async def get_lists() -> get_lists_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/lists/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_list_entries_output = mcp_output(
            description="All entries in the specified list",
            examples=[''])
        @self._mcp.tool(
            description="Get all entries in an Affinity list.",
            meta=mcp_meta("get_list_entries"),
            structured_output=True
        )
        async def get_list_entries(
            list_id: Annotated[int, Field(description="List ID")],
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = None,
            page_token: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> get_list_entries_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/lists/entries/",
                data={"list_id": list_id, "page_size": page_size, "page_token": page_token},
                context=context
            )
            return [json.dumps(response.data)]

        get_notes_output = mcp_output(
            description="Notes filtered by entity type",
            examples=[''])
        @self._mcp.tool(
            description="List notes in Affinity, optionally filtered by entity.",
            meta=mcp_meta("get_notes"),
            structured_output=True
        )
        async def get_notes(
            person_id: Annotated[Optional[int], Field(description="Filter by person ID")] = None,
            organization_id: Annotated[Optional[int], Field(description="Filter by organization ID")] = None,
            opportunity_id: Annotated[Optional[int], Field(description="Filter by opportunity ID")] = None,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = None,
            page_token: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> get_notes_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/notes/",
                data={"person_id": person_id, "organization_id": organization_id, "opportunity_id": opportunity_id, "page_size": page_size, "page_token": page_token},
                context=context
            )
            return [json.dumps(response.data)]

        create_note_output = mcp_output(
            description="Created note details",
            examples=[''])
        @self._mcp.tool(
            description="Create a note in Affinity attached to one or more entities.",
            meta=mcp_meta("create_note"),
            structured_output=True
        )
        async def create_note(
            content: Annotated[str, Field(description="Note content")],
            person_ids: Annotated[Optional[List[int]], Field(description="Person IDs to attach note to")] = None,
            organization_ids: Annotated[Optional[List[int]], Field(description="Organization IDs to attach note to")] = None,
            opportunity_ids: Annotated[Optional[List[int]], Field(description="Opportunity IDs to attach note to")] = None
        ) -> create_note_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/notes/create/",
                data={"content": content, "person_ids": person_ids, "organization_ids": organization_ids, "opportunity_ids": opportunity_ids},
                context=context
            )
            return [json.dumps(response.data)]

        get_opportunities_output = mcp_output(
            description="List of opportunities matching the search criteria",
            examples=[''])
        @self._mcp.tool(
            description="Search or list all opportunities in Affinity.",
            meta=mcp_meta("get_opportunities"),
            structured_output=True
        )
        async def get_opportunities(
            term: Annotated[Optional[str], Field(description="Search term to filter opportunities")] = None,
            page_size: Annotated[Optional[int], Field(description="Number of results per page")] = None,
            page_token: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> get_opportunities_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/opportunities/",
                data={"term": term, "page_size": page_size, "page_token": page_token},
                context=context
            )
            return [json.dumps(response.data)]

        get_field_values_output = mcp_output(
            description="Custom field values for the specified entity",
            examples=[''])
        @self._mcp.tool(
            description="Get custom field values for an Affinity entity.",
            meta=mcp_meta("get_field_values"),
            structured_output=True
        )
        async def get_field_values(
            person_id: Annotated[Optional[int], Field(description="Person ID")] = None,
            organization_id: Annotated[Optional[int], Field(description="Organization ID")] = None,
            opportunity_id: Annotated[Optional[int], Field(description="Opportunity ID")] = None
        ) -> get_field_values_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/field-values/",
                data={"person_id": person_id, "organization_id": organization_id, "opportunity_id": opportunity_id},
                context=context
            )
            return [json.dumps(response.data)]
