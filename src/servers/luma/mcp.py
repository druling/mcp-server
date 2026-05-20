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
class LumaServer(BaseMCPServer):
    """MCP Server for Luma."""

    name: str = "luma"
    category: str = "Luma"
    description: str = "Luma integration for event creation, management, and attendee tracking."
    scope: str = "luma_access_key"
    client_service = IntegrationAppClient()
    base_url = "/luma"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        get_self_output = mcp_output(
            description="Authenticated Luma user profile",
            examples=[''])
        @self._mcp.tool(
            description="Get the current authenticated Luma user.",
            meta=mcp_meta("get_self"),
            structured_output=True
        )
        async def get_self() -> get_self_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/user/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_calendar_output = mcp_output(
            description="Current Luma calendar details",
            examples=[''])
        @self._mcp.tool(
            description="Get the current Luma calendar details.",
            meta=mcp_meta("get_calendar"),
            structured_output=True
        )
        async def get_calendar() -> get_calendar_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calendar/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_events_output = mcp_output(
            description="List of events with pagination",
            examples=[''])
        @self._mcp.tool(
            description="List events in the Luma calendar.",
            meta=mcp_meta("list_events"),
            structured_output=True
        )
        async def list_events(
            after: Annotated[Optional[str], Field(description="Filter events after this ISO timestamp")] = None,
            before: Annotated[Optional[str], Field(description="Filter events before this ISO timestamp")] = None,
            pagination_cursor: Annotated[Optional[str], Field(description="Cursor for next page")] = None,
            pagination_limit: Annotated[Optional[int], Field(description="Maximum number of events")] = 50
        ) -> list_events_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/",
                data={"after": after, "before": before, "pagination_cursor": pagination_cursor, "pagination_limit": pagination_limit},
                context=context
            )
            return [json.dumps(response.data)]

        get_event_output = mcp_output(
            description="Detailed information about a specific Luma event",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Luma event by API ID.",
            meta=mcp_meta("get_event"),
            structured_output=True
        )
        async def get_event(
            event_api_id: Annotated[str, Field(description="Event API ID")]
        ) -> get_event_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/get/",
                data={"event_api_id": event_api_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_event_guests_output = mcp_output(
            description="List of guests for the specified event",
            examples=[''])
        @self._mcp.tool(
            description="Get guests for a specific Luma event.",
            meta=mcp_meta("get_event_guests"),
            structured_output=True
        )
        async def get_event_guests(
            event_api_id: Annotated[str, Field(description="Event API ID")],
            pagination_cursor: Annotated[Optional[str], Field(description="Cursor for next page")] = None,
            pagination_limit: Annotated[Optional[int], Field(description="Maximum number of guests")] = 100
        ) -> get_event_guests_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/guests/",
                data={"event_api_id": event_api_id, "pagination_cursor": pagination_cursor, "pagination_limit": pagination_limit},
                context=context
            )
            return [json.dumps(response.data)]

        create_event_output = mcp_output(
            description="Created event details with API ID",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Luma event.",
            meta=mcp_meta("create_event"),
            structured_output=True
        )
        async def create_event(
            name: Annotated[str, Field(description="Event name")],
            start_at: Annotated[str, Field(description="Start time as ISO 8601 timestamp")],
            end_at: Annotated[Optional[str], Field(description="End time as ISO 8601 timestamp")] = None,
            description: Annotated[Optional[str], Field(description="Event description")] = None,
            cover_url: Annotated[Optional[str], Field(description="URL of the cover image")] = None
        ) -> create_event_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/create/",
                data={"name": name, "start_at": start_at, "end_at": end_at, "description": description, "cover_url": cover_url},
                context=context
            )
            return [json.dumps(response.data)]

        add_guests_output = mcp_output(
            description="Confirmation of guests added to the event",
            examples=[''])
        @self._mcp.tool(
            description="Add guests to a Luma event.",
            meta=mcp_meta("add_guests"),
            structured_output=True
        )
        async def add_guests(
            event_api_id: Annotated[str, Field(description="Event API ID")],
            guests: Annotated[List[Dict[str, Any]], Field(description="List of guest objects with email and optional name")]
        ) -> add_guests_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/guests/add/",
                data={"event_api_id": event_api_id, "guests": guests},
                context=context
            )
            return [json.dumps(response.data)]

        list_people_output = mcp_output(
            description="List of people in the Luma calendar",
            examples=[''])
        @self._mcp.tool(
            description="List people in the Luma calendar.",
            meta=mcp_meta("list_people"),
            structured_output=True
        )
        async def list_people(
            pagination_cursor: Annotated[Optional[str], Field(description="Cursor for next page")] = None,
            pagination_limit: Annotated[Optional[int], Field(description="Maximum number of people")] = 100
        ) -> list_people_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/people/",
                data={"pagination_cursor": pagination_cursor, "pagination_limit": pagination_limit},
                context=context
            )
            return [json.dumps(response.data)]
