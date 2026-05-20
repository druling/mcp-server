import json
import logging
from typing import Annotated, Optional, Dict, Any
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import IntegrationAppClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class PosthogServer(BaseMCPServer):
    """MCP Server for PostHog."""

    name: str = "posthog"
    category: str = "PostHog"
    description: str = "PostHog integration for product analytics, feature flags, and user tracking."
    scope: str = "posthog_access_key"
    client_service = IntegrationAppClient()
    base_url = "/posthog"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_projects_output = mcp_output(
            description="List of projects in the PostHog organization",
            examples=[''])
        @self._mcp.tool(
            description="List all projects in the PostHog organization.",
            meta=mcp_meta("list_projects"),
            structured_output=True
        )
        async def list_projects() -> list_projects_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        list_events_output = mcp_output(
            description="List of events for the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List events for a PostHog project.",
            meta=mcp_meta("list_events"),
            structured_output=True
        )
        async def list_events(
            project_id: Annotated[str, Field(description="PostHog project ID")],
            event: Annotated[Optional[str], Field(description="Filter by event name")] = None,
            distinct_id: Annotated[Optional[str], Field(description="Filter by user distinct ID")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of events")] = 100,
            after: Annotated[Optional[str], Field(description="Filter events after this ISO timestamp")] = None,
            before: Annotated[Optional[str], Field(description="Filter events before this ISO timestamp")] = None
        ) -> list_events_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/",
                data={"project_id": project_id, "event": event, "distinct_id": distinct_id, "limit": limit, "after": after, "before": before},
                context=context
            )
            return [json.dumps(response.data)]

        list_persons_output = mcp_output(
            description="List of persons (users) for the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List persons (users) for a PostHog project.",
            meta=mcp_meta("list_persons"),
            structured_output=True
        )
        async def list_persons(
            project_id: Annotated[str, Field(description="PostHog project ID")],
            search: Annotated[Optional[str], Field(description="Search term for persons")] = None,
            distinct_id: Annotated[Optional[str], Field(description="Filter by distinct ID")] = None,
            limit: Annotated[Optional[int], Field(description="Maximum number of persons")] = 100
        ) -> list_persons_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/persons/",
                data={"project_id": project_id, "search": search, "distinct_id": distinct_id, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        list_feature_flags_output = mcp_output(
            description="List of feature flags for the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List feature flags for a PostHog project.",
            meta=mcp_meta("list_feature_flags"),
            structured_output=True
        )
        async def list_feature_flags(
            project_id: Annotated[str, Field(description="PostHog project ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of feature flags")] = 100
        ) -> list_feature_flags_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/feature-flags/",
                data={"project_id": project_id, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        list_insights_output = mcp_output(
            description="List of insights/charts for the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List insights and saved charts for a PostHog project.",
            meta=mcp_meta("list_insights"),
            structured_output=True
        )
        async def list_insights(
            project_id: Annotated[str, Field(description="PostHog project ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of insights")] = 20
        ) -> list_insights_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/insights/",
                data={"project_id": project_id, "limit": limit},
                context=context
            )
            return [json.dumps(response.data)]

        list_cohorts_output = mcp_output(
            description="List of cohorts for the specified project",
            examples=[''])
        @self._mcp.tool(
            description="List cohorts for a PostHog project.",
            meta=mcp_meta("list_cohorts"),
            structured_output=True
        )
        async def list_cohorts(
            project_id: Annotated[str, Field(description="PostHog project ID")]
        ) -> list_cohorts_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/cohorts/",
                data={"project_id": project_id},
                context=context
            )
            return [json.dumps(response.data)]

        capture_event_output = mcp_output(
            description="Confirmation of event capture",
            examples=[''])
        @self._mcp.tool(
            description="Capture a custom event in PostHog.",
            meta=mcp_meta("capture_event"),
            structured_output=True
        )
        async def capture_event(
            project_api_key: Annotated[str, Field(description="PostHog project API key")],
            distinct_id: Annotated[str, Field(description="User distinct ID")],
            event: Annotated[str, Field(description="Event name")],
            properties: Annotated[Optional[Dict[str, Any]], Field(description="Event properties")] = None
        ) -> capture_event_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/events/capture/",
                data={"project_api_key": project_api_key, "distinct_id": distinct_id, "event": event, "properties": properties},
                context=context
            )
            return [json.dumps(response.data)]

        query_output = mcp_output(
            description="Query results from PostHog",
            examples=[''])
        @self._mcp.tool(
            description="Execute a HogQL or insight query in PostHog.",
            meta=mcp_meta("query"),
            structured_output=True
        )
        async def query(
            project_id: Annotated[str, Field(description="PostHog project ID")],
            query: Annotated[Dict[str, Any], Field(description="Query object (HogQL or insight query)")]
        ) -> query_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/query/",
                data={"project_id": project_id, "query": query},
                context=context
            )
            return [json.dumps(response.data)]
