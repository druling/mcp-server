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
class ApifyServer(BaseMCPServer):
    """MCP Server for Apify."""

    name: str = "apify"
    category: str = "Apify"
    description: str = "Apify integration for web scraping and browser automation."
    scope: str = "apify_access_key"
    client_service = IntegrationAppClient()
    base_url = "/apify"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_actors_output = mcp_output(
            description="List of available Apify actors",
            examples=[''])
        @self._mcp.tool(
            description="List available Apify actors.",
            meta=mcp_meta("list_actors"),
            structured_output=True
        )
        async def list_actors(
            my: Annotated[Optional[bool], Field(description="Return only actors owned by the user")] = True,
            limit: Annotated[Optional[int], Field(description="Maximum number of actors to return")] = 20,
            offset: Annotated[Optional[int], Field(description="Offset for pagination")] = 0
        ) -> list_actors_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/actors/",
                data={"my": my, "limit": limit, "offset": offset},
                context=context
            )
            return [json.dumps(response.data)]

        run_actor_output = mcp_output(
            description="Run details including run ID and status",
            examples=[''])
        @self._mcp.tool(
            description="Run an Apify actor with optional input.",
            meta=mcp_meta("run_actor"),
            structured_output=True
        )
        async def run_actor(
            actor_id: Annotated[str, Field(description="Actor ID or name")],
            run_input: Annotated[Optional[Dict[str, Any]], Field(description="Input data for the actor")] = None,
            memory_mbytes: Annotated[Optional[int], Field(description="Memory limit in MB")] = None,
            timeout_secs: Annotated[Optional[int], Field(description="Timeout in seconds")] = None
        ) -> run_actor_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/actors/run/",
                data={"actor_id": actor_id, "run_input": run_input, "memory_mbytes": memory_mbytes, "timeout_secs": timeout_secs},
                context=context
            )
            return [json.dumps(response.data)]

        get_actor_runs_output = mcp_output(
            description="List of runs for the specified actor",
            examples=[''])
        @self._mcp.tool(
            description="Get runs for an Apify actor.",
            meta=mcp_meta("get_actor_runs"),
            structured_output=True
        )
        async def get_actor_runs(
            actor_id: Annotated[str, Field(description="Actor ID or name")],
            limit: Annotated[Optional[int], Field(description="Maximum number of runs to return")] = 20,
            offset: Annotated[Optional[int], Field(description="Offset for pagination")] = 0,
            status: Annotated[Optional[str], Field(description="Filter by status (RUNNING, SUCCEEDED, FAILED)")] = None
        ) -> get_actor_runs_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/actors/runs/",
                data={"actor_id": actor_id, "limit": limit, "offset": offset, "status": status},
                context=context
            )
            return [json.dumps(response.data)]

        get_run_output = mcp_output(
            description="Details of a specific actor run including status and dataset ID",
            examples=[''])
        @self._mcp.tool(
            description="Get details of a specific Apify actor run.",
            meta=mcp_meta("get_run"),
            structured_output=True
        )
        async def get_run(
            actor_id: Annotated[str, Field(description="Actor ID or name")],
            run_id: Annotated[str, Field(description="Run ID")]
        ) -> get_run_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/runs/get/",
                data={"actor_id": actor_id, "run_id": run_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_dataset_items_output = mcp_output(
            description="Items from the specified dataset",
            examples=[''])
        @self._mcp.tool(
            description="Get items from an Apify dataset.",
            meta=mcp_meta("get_dataset_items"),
            structured_output=True
        )
        async def get_dataset_items(
            dataset_id: Annotated[str, Field(description="Dataset ID")],
            limit: Annotated[Optional[int], Field(description="Maximum number of items to return")] = 100,
            offset: Annotated[Optional[int], Field(description="Offset for pagination")] = 0,
            format: Annotated[Optional[str], Field(description="Output format (json, csv, xml)")] = "json"
        ) -> get_dataset_items_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/datasets/items/",
                data={"dataset_id": dataset_id, "limit": limit, "offset": offset, "format": format},
                context=context
            )
            return [json.dumps(response.data)]

        get_store_record_output = mcp_output(
            description="Record value from the key-value store",
            examples=[''])
        @self._mcp.tool(
            description="Get a record from an Apify key-value store.",
            meta=mcp_meta("get_store_record"),
            structured_output=True
        )
        async def get_store_record(
            store_id: Annotated[str, Field(description="Key-value store ID")],
            record_key: Annotated[str, Field(description="Record key")]
        ) -> get_store_record_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/key-value-stores/records/get/",
                data={"store_id": store_id, "record_key": record_key},
                context=context
            )
            return [json.dumps(response.data)]
