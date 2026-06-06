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
class CalServer(BaseMCPServer):
    """MCP Server for Cal.com."""

    name: str = "cal"
    category: str = "Cal"
    description: str = "Cal.com integration for scheduling, bookings, and calendar management."
    scope: str = "cal_access_key"
    client_service = IntegrationAppClient()
    base_url = "/cal"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        get_me_output = mcp_output(
            description="Authenticated user profile details",
            examples=[''])
        @self._mcp.tool(
            description="Get the current authenticated Cal.com user profile.",
            meta=mcp_meta("get_me"),
            structured_output=True
        )
        async def get_me() -> get_me_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/me/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_event_types_output = mcp_output(
            description="List of event types for the user",
            examples=[''])
        @self._mcp.tool(
            description="Get all Cal.com event types, optionally for a specific username.",
            meta=mcp_meta("get_event_types"),
            structured_output=True
        )
        async def get_event_types(
            username: Annotated[Optional[str], Field(description="Username to filter event types")] = None
        ) -> get_event_types_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/event-types/",
                data={"username": username},
                context=context
            )
            return [json.dumps(response.data)]

        get_event_type_output = mcp_output(
            description="Detailed information about a specific event type",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Cal.com event type by ID.",
            meta=mcp_meta("get_event_type"),
            structured_output=True
        )
        async def get_event_type(
            event_type_id: Annotated[int, Field(description="Event type ID")]
        ) -> get_event_type_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/event-types/get/",
                data={"event_type_id": event_type_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_bookings_output = mcp_output(
            description="List of bookings with pagination",
            examples=[''])
        @self._mcp.tool(
            description="Get all Cal.com bookings with optional status filter.",
            meta=mcp_meta("get_bookings"),
            structured_output=True
        )
        async def get_bookings(
            status: Annotated[Optional[str], Field(description="Filter by status (upcoming, past, cancelled)")] = None,
            cursor: Annotated[Optional[int], Field(description="Pagination cursor")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of bookings")] = 10
        ) -> get_bookings_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/bookings/",
                data={"status": status, "cursor": cursor, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_booking_output = mcp_output(
            description="Detailed information about a specific booking",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Cal.com booking by UID.",
            meta=mcp_meta("get_booking"),
            structured_output=True
        )
        async def get_booking(
            booking_uid: Annotated[str, Field(description="Booking UID")]
        ) -> get_booking_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/bookings/get/",
                data={"booking_uid": booking_uid},
                context=context
            )
            return [json.dumps(response.data)]

        get_schedules_output = mcp_output(
            description="List of availability schedules",
            examples=[''])
        @self._mcp.tool(
            description="Get all Cal.com availability schedules.",
            meta=mcp_meta("get_schedules"),
            structured_output=True
        )
        async def get_schedules() -> get_schedules_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/schedules/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_schedule_output = mcp_output(
            description="Detailed information about a specific schedule",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Cal.com schedule by ID.",
            meta=mcp_meta("get_schedule"),
            structured_output=True
        )
        async def get_schedule(
            schedule_id: Annotated[int, Field(description="Schedule ID")]
        ) -> get_schedule_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/schedules/get/",
                data={"schedule_id": schedule_id},
                context=context
            )
            return [json.dumps(response.data)]

        cancel_booking_output = mcp_output(
            description="Confirmation of booking cancellation",
            examples=[''])
        @self._mcp.tool(
            description="Cancel a Cal.com booking by UID.",
            meta=mcp_meta("cancel_booking"),
            structured_output=True
        )
        async def cancel_booking(
            booking_uid: Annotated[str, Field(description="Booking UID to cancel")],
            cancellation_reason: Annotated[Optional[str], Field(description="Reason for cancellation")] = None
        ) -> cancel_booking_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/bookings/cancel/",
                data={"booking_uid": booking_uid, "cancellation_reason": cancellation_reason},
                context=context
            )
            return [json.dumps(response.data)]
