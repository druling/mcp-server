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
class GongServer(BaseMCPServer):
    """MCP Server for Gong."""

    name: str = "gong"
    category: str = "Gong"
    description: str = "Gong integration for sales intelligence and conversation analytics."
    scope: str = "gong_access"
    client_service = IntegrationAppClient()
    base_url = "/gong"

    def _register_prompts(self) -> None:
        """Register all Gong prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Gong tools with the MCP server."""

        get_calls_output = mcp_output(
            description="List of calls with metadata and pagination cursor",
            examples=[''])
        @self._mcp.tool(
            description="Get list of Gong calls with optional date filtering.",
            meta=mcp_meta("get_calls"),
            structured_output=True
        )
        async def get_calls(
            from_date_time: Annotated[Optional[str], Field(description="Start datetime (ISO format)")] = None,
            to_date_time: Annotated[Optional[str], Field(description="End datetime (ISO format)")] = None,
            cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None
        ) -> get_calls_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calls/",
                data={
                    "from_date_time": from_date_time,
                    "to_date_time": to_date_time,
                    "cursor": cursor,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_call_output = mcp_output(
            description="Detailed information about a specific call",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Gong call.",
            meta=mcp_meta("get_call"),
            structured_output=True
        )
        async def get_call(
            call_id: Annotated[str, Field(description="Call ID")]
        ) -> get_call_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calls/get/",
                data={"call_id": call_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_call_transcripts_output = mcp_output(
            description="Transcripts for the requested calls",
            examples=[''])
        @self._mcp.tool(
            description="Get transcripts for multiple Gong calls.",
            meta=mcp_meta("get_call_transcripts"),
            structured_output=True
        )
        async def get_call_transcripts(
            call_ids: Annotated[List[str], Field(description="List of call IDs")]
        ) -> get_call_transcripts_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calls/transcripts/",
                data={"call_ids": call_ids},
                context=context
            )
            return [json.dumps(response.data)]

        get_extensive_calls_output = mcp_output(
            description="Extensive call data with detailed metadata and insights",
            examples=[''])
        @self._mcp.tool(
            description="Get extensive call data with detailed insights.",
            meta=mcp_meta("get_extensive_calls"),
            structured_output=True
        )
        async def get_extensive_calls(
            call_ids: Annotated[Optional[List[str]], Field(description="List of specific call IDs")] = None,
            from_date_time: Annotated[Optional[str], Field(description="Start datetime (ISO format)")] = None,
            to_date_time: Annotated[Optional[str], Field(description="End datetime (ISO format)")] = None
        ) -> get_extensive_calls_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calls/extensive/",
                data={
                    "call_ids": call_ids,
                    "from_date_time": from_date_time,
                    "to_date_time": to_date_time,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_call_stats_output = mcp_output(
            description="Aggregated call statistics for specified time period and users",
            examples=[''])
        @self._mcp.tool(
            description="Get call statistics and analytics.",
            meta=mcp_meta("get_call_stats"),
            structured_output=True
        )
        async def get_call_stats(
            from_date_time: Annotated[Optional[str], Field(description="Start datetime (ISO format)")] = None,
            to_date_time: Annotated[Optional[str], Field(description="End datetime (ISO format)")] = None,
            user_ids: Annotated[Optional[List[str]], Field(description="List of user IDs to filter by")] = None
        ) -> get_call_stats_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/calls/stats/",
                data={
                    "from_date_time": from_date_time,
                    "to_date_time": to_date_time,
                    "user_ids": user_ids,
                },
                context=context
            )
            return [json.dumps(response.data)]

        get_users_output = mcp_output(
            description="List of Gong users with optional avatars",
            examples=[''])
        @self._mcp.tool(
            description="Get list of users in Gong workspace.",
            meta=mcp_meta("get_users"),
            structured_output=True
        )
        async def get_users(
            cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
            include_avatars: Annotated[Optional[bool], Field(description="Include user avatar URLs")] = False
        ) -> get_users_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/users/",
                data={
                    "cursor": cursor,
                    "include_avatars": include_avatars,
                },
                context=context
            )
            return [json.dumps(response.data)]
