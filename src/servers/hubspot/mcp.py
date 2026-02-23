import logging
from typing import Annotated, Optional, List, Dict, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from . import outputs
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class HubspotServer(BaseMCPServer):
    """MCP Server for Hubspot."""

    name: str = "hubspot"
    category: str = "Hubspot"
    description: str = "Hubspot integration for CRM and marketing automation."
    scope: str = "hubspot_access"
    backend_service = BackendClient()
    base_url = "/hubspot"

    def _register_prompts(self) -> None:
        """Register all Hubspot prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Hubspot tools with the MCP server."""

        @self._mcp.tool(
            description="Get properties for a HubSpot object type (contacts, companies, deals, etc.).",
            meta=mcp_meta("get_properties"),
            structured_output=True
        )
        async def get_properties(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")]
        ) -> outputs.PropertyList:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/properties/",
                data={"object_type": object_type},
                context=context
            )
            return outputs.PropertyList(**response.data)

        @self._mcp.tool(
            description="Get pipelines for a HubSpot object type.",
            meta=mcp_meta("get_pipelines"),
            structured_output=True
        )
        async def get_pipelines(
            object_type: Annotated[str, Field(description="Object type (e.g., 'deals', 'tickets')")]
        ) -> outputs.PipelineList:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/pipelines/",
                data={"object_type": object_type},
                context=context
            )
            return outputs.PipelineList(**response.data)

        @self._mcp.tool(
            description="Get lists for a HubSpot object type.",
            meta=mcp_meta("get_lists"),
            structured_output=True
        )
        async def get_lists(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies')")]
        ) -> outputs.Lists:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/lists/",
                data={"object_type": object_type},
                context=context
            )
            return outputs.Lists(**response.data)

        @self._mcp.tool(
            description="Get records from HubSpot with specified properties.",
            meta=mcp_meta("get_records"),
            structured_output=True
        )
        async def get_records(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            properties: Annotated[List[str], Field(description="List of property names to retrieve")],
            limit: Annotated[Optional[int], Field(description="Maximum number of records to retrieve")] = 250
        ) -> outputs.RecordList:
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
            return outputs.RecordList(**response.data)

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
        ) -> outputs.RecordList:
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
            return outputs.RecordList(**response.data)

        @self._mcp.tool(
            description="Create a new record in HubSpot.",
            meta=mcp_meta("create_record"),
            structured_output=True
        )
        async def create_record(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            properties: Annotated[Dict[str, Any], Field(description="Properties for the new record")]
        ) -> outputs.RecordResult:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/records/create/",
                data={
                    "object_type": object_type,
                    "properties": properties
                },
                context=context
            )
            return outputs.RecordResult(success=True, **response.data)

        @self._mcp.tool(
            description="Update an existing record in HubSpot.",
            meta=mcp_meta("update_record"),
            structured_output=True
        )
        async def update_record(
            object_type: Annotated[str, Field(description="Object type (e.g., 'contacts', 'companies', 'deals')")],
            object_id: Annotated[str, Field(description="ID of the record to update")],
            properties: Annotated[Dict[str, Any], Field(description="Properties to update")]
        ) -> outputs.RecordResult:
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
            return outputs.RecordResult(success=True, **response.data)

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
        ) -> outputs.EmailResult:
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
            return outputs.EmailResult(success=True, **response.data)
