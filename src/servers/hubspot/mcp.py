import json
import logging
from typing import Annotated, Optional, List, Dict, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class HubspotServer(BaseMCPServer):
    """MCP Server for HubSpot."""

    name: str = "hubspot"
    category: str = "HubSpot"
    description: str = "HubSpot integration for CRM and marketing automation."
    scope: str = "hubspot_access"
    backend_service = BackendClient()
    base_url = "/hubspot"

    def _register_prompts(self) -> None:
        """Register all HubSpot prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all HubSpot tools with the MCP server."""

        get_properties_output = mcp_output(
            description="List of property definitions for the object type with name, label, and field type",
            examples=[''])
        @self._mcp.tool(
            description="Get properties for a HubSpot object type (contacts, companies, deals, etc.).",
            meta=mcp_meta("get_properties"),
            structured_output=True
        )
        async def get_properties(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")]
        ) -> get_properties_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/properties/",
                data={"object_type": object_type},
                context=context
            )
            return [json.dumps(response.data)]

        get_pipelines_output = mcp_output(
            description="List of pipelines with stages, IDs, and pipeline configuration",
            examples=[''])
        @self._mcp.tool(
            description="Get pipelines for a HubSpot object type.",
            meta=mcp_meta("get_pipelines"),
            structured_output=True
        )
        async def get_pipelines(
            object_type: Annotated[str, Field(description="Object type (e.g., 'deals', 'tickets')")]
        ) -> get_pipelines_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/pipelines/",
                data={"object_type": object_type},
                context=context
            )
            return [json.dumps(response.data)]

        get_lists_output = mcp_output(
            description="List of HubSpot lists with list ID, name, and membership criteria",
            examples=[''])
        @self._mcp.tool(
            description="Get lists for a HubSpot object type.",
            meta=mcp_meta("get_lists"),
            structured_output=True
        )
        async def get_lists(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies')")]
        ) -> get_lists_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/lists/",
                data={"object_type": object_type},
                context=context
            )
            return [json.dumps(response.data)]

        get_records_output = mcp_output(
            description="List of records with requested property values and record IDs",
            examples=[''])
        @self._mcp.tool(
            description="Get records from HubSpot with specified properties.",
            meta=mcp_meta("get_records"),
            structured_output=True
        )
        async def get_records(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            properties: Annotated[List[str], Field(description="List of property names to retrieve")],
            limit: Annotated[Optional[int], Field(description="Maximum number of records to retrieve")] = 250
        ) -> get_records_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/records/",
                data={
                    "object_type": object_type,
                    "properties": properties,
                    "limit": limit
                },
                context=context
            )
            return [json.dumps(response.data)]

        search_records_output = mcp_output(
            description="List of records matching the filter criteria with requested property values",
            examples=[''])
        @self._mcp.tool(
            description="Search for records in HubSpot with filters.",
            meta=mcp_meta("search_records"),
            structured_output=True
        )
        async def search_records(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            properties: Annotated[List[str], Field(description="List of property names to retrieve")],
            filters: Annotated[Optional[Dict[str, Any]], Field(description="Filter criteria as key-value pairs")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of records to retrieve")] = 200
        ) -> search_records_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/records/search/",
                data={
                    "object_type": object_type,
                    "properties": properties,
                    "filters": filters,
                    "limit": limit
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_record_output = mcp_output(
            description="Created record details including the new record ID and its properties",
            examples=[''])
        @self._mcp.tool(
            description="Create a new record in HubSpot.",
            meta=mcp_meta("create_record"),
            structured_output=True
        )
        async def create_record(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            properties: Annotated[Dict[str, Any], Field(description="Properties for the new record")]
        ) -> create_record_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/records/create/",
                data={
                    "object_type": object_type,
                    "properties": properties
                },
                context=context
            )
            return [json.dumps(response.data)]

        update_record_output = mcp_output(
            description="Updated record details including the record ID and modified properties",
            examples=[''])
        @self._mcp.tool(
            description="Update an existing record in HubSpot.",
            meta=mcp_meta("update_record"),
            structured_output=True
        )
        async def update_record(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            object_id: Annotated[str, Field(description="ID of the record to update")],
            properties: Annotated[Dict[str, Any], Field(description="Properties to update")]
        ) -> update_record_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/records/update/",
                data={
                    "object_type": object_type,
                    "object_id": object_id,
                    "properties": properties
                },
                context=context
            )
            return [json.dumps(response.data)]

        send_marketing_email_output = mcp_output(
            description="Confirmation of the sent marketing email including delivery status",
            examples=[''])
        @self._mcp.tool(
            description="Send a marketing email through HubSpot.",
            meta=mcp_meta("send_marketing_email"),
            structured_output=True
        )
        async def send_marketing_email(
            email_id: Annotated[str, Field(description="HubSpot email template ID")],
            to: Annotated[str, Field(description="Recipient email address")],
            bcc: Annotated[Optional[str], Field(description="BCC email address")] = None,
            cc: Annotated[Optional[str], Field(description="CC email address")] = None,
            from_email: Annotated[Optional[str], Field(description="Sender email address")] = None,
            reply_to: Annotated[Optional[str], Field(description="Reply-to email address")] = None
        ) -> send_marketing_email_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/email/send/",
                data={
                    "email_id": email_id,
                    "to": to,
                    "bcc": bcc,
                    "cc": cc,
                    "from_email": from_email,
                    "reply_to": reply_to
                },
                context=context
            )
            return [json.dumps(response.data)]
