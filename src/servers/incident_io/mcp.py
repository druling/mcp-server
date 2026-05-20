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
class IncidentIoServer(BaseMCPServer):
    """MCP Server for incident.io."""

    name: str = "incident_io"
    category: str = "Incident.io"
    description: str = "incident.io integration for incident management, alerts, escalations, and on-call scheduling."
    scope: str = "incident_io_access_key"
    client_service = IntegrationAppClient()
    base_url = "/incident_io"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_incidents_output = mcp_output(
            description="List of incidents with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all incidents in incident.io.",
            meta=mcp_meta("list_incidents"),
            structured_output=True
        )
        async def list_incidents(
            page_size: Annotated[Optional[int], Field(description="Number of incidents per page")] = 25,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None,
            status: Annotated[Optional[str], Field(description="Filter by status")] = None
        ) -> list_incidents_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/incidents/",
                data={"page_size": page_size, "after": after, "status": status},
                context=context
            )
            return [json.dumps(response.data)]

        get_incident_output = mcp_output(
            description="Detailed information about a specific incident",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific incident.io incident by ID.",
            meta=mcp_meta("get_incident"),
            structured_output=True
        )
        async def get_incident(
            incident_id: Annotated[str, Field(description="Incident ID")]
        ) -> get_incident_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/incidents/get/",
                data={"incident_id": incident_id},
                context=context
            )
            return [json.dumps(response.data)]

        create_incident_output = mcp_output(
            description="Created incident details with ID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new incident in incident.io.",
            meta=mcp_meta("create_incident"),
            structured_output=True
        )
        async def create_incident(
            name: Annotated[str, Field(description="Incident name")],
            severity_id: Annotated[str, Field(description="Severity ID (use list_severities to get valid IDs)")],
            incident_type_id: Annotated[Optional[str], Field(description="Incident type ID")] = None,
            summary: Annotated[Optional[str], Field(description="Incident summary")] = None,
            mode: Annotated[Optional[str], Field(description="Incident mode (real or test)")] = "real",
            visibility: Annotated[Optional[str], Field(description="Visibility (public or private)")] = "public"
        ) -> create_incident_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/incidents/create/",
                data={"name": name, "severity_id": severity_id, "incident_type_id": incident_type_id, "summary": summary, "mode": mode, "visibility": visibility},
                context=context
            )
            return [json.dumps(response.data)]

        edit_incident_output = mcp_output(
            description="Updated incident details",
            examples=[''])
        @self._mcp.tool(
            description="Edit an existing incident.io incident.",
            meta=mcp_meta("edit_incident"),
            structured_output=True
        )
        async def edit_incident(
            incident_id: Annotated[str, Field(description="Incident ID to edit")],
            name: Annotated[Optional[str], Field(description="New incident name")] = None,
            severity_id: Annotated[Optional[str], Field(description="New severity ID")] = None,
            summary: Annotated[Optional[str], Field(description="New incident summary")] = None
        ) -> edit_incident_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/incidents/edit/",
                data={"incident_id": incident_id, "name": name, "severity_id": severity_id, "summary": summary},
                context=context
            )
            return [json.dumps(response.data)]

        list_severities_output = mcp_output(
            description="List of available incident severities",
            examples=[''])
        @self._mcp.tool(
            description="List all incident severity levels in incident.io.",
            meta=mcp_meta("list_severities"),
            structured_output=True
        )
        async def list_severities() -> list_severities_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/severities/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_alerts_output = mcp_output(
            description="List of alerts with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all alerts in incident.io.",
            meta=mcp_meta("list_alerts"),
            structured_output=True
        )
        async def list_alerts(
            page_size: Annotated[Optional[int], Field(description="Number of alerts per page")] = 25,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_alerts_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/alerts/",
                data={"page_size": page_size, "after": after},
                context=context
            )
            return [json.dumps(response.data)]

        list_escalations_output = mcp_output(
            description="List of escalations with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List all escalations in incident.io.",
            meta=mcp_meta("list_escalations"),
            structured_output=True
        )
        async def list_escalations(
            page_size: Annotated[Optional[int], Field(description="Number of escalations per page")] = 25,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_escalations_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/escalations/",
                data={"page_size": page_size, "after": after},
                context=context
            )
            return [json.dumps(response.data)]

        list_follow_ups_output = mcp_output(
            description="List of follow-up actions",
            examples=[''])
        @self._mcp.tool(
            description="List follow-up actions in incident.io, optionally filtered by incident.",
            meta=mcp_meta("list_follow_ups"),
            structured_output=True
        )
        async def list_follow_ups(
            incident_id: Annotated[Optional[str], Field(description="Filter by incident ID")] = None
        ) -> list_follow_ups_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/follow-ups/",
                data={"incident_id": incident_id},
                context=context
            )
            return [json.dumps(response.data)]

        list_users_output = mcp_output(
            description="List of users in incident.io",
            examples=[''])
        @self._mcp.tool(
            description="List users in incident.io.",
            meta=mcp_meta("list_users"),
            structured_output=True
        )
        async def list_users(
            page_size: Annotated[Optional[int], Field(description="Number of users per page")] = 25,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={"page_size": page_size, "after": after},
                context=context
            )
            return [json.dumps(response.data)]

        list_schedules_output = mcp_output(
            description="List of on-call schedules",
            examples=[''])
        @self._mcp.tool(
            description="List on-call schedules in incident.io.",
            meta=mcp_meta("list_schedules"),
            structured_output=True
        )
        async def list_schedules(
            page_size: Annotated[Optional[int], Field(description="Number of schedules per page")] = 25,
            after: Annotated[Optional[str], Field(description="Cursor for next page")] = None
        ) -> list_schedules_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/schedules/",
                data={"page_size": page_size, "after": after},
                context=context
            )
            return [json.dumps(response.data)]
