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
class BrowserbaseServer(BaseMCPServer):
    """MCP Server for Browserbase."""

    name: str = "browserbase"
    category: str = "Browserbase"
    description: str = "Browserbase integration for cloud browser sessions and web automation."
    scope: str = "browserbase_access_key"
    client_service = IntegrationAppClient()
    base_url = "/browserbase"

    def _register_prompts(self) -> None:
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:

        list_projects_output = mcp_output(
            description="List of Browserbase projects",
            examples=[''])
        @self._mcp.tool(
            description="List all Browserbase projects.",
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

        get_project_output = mcp_output(
            description="Detailed information about a specific Browserbase project",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Browserbase project by ID.",
            meta=mcp_meta("get_project"),
            structured_output=True
        )
        async def get_project(
            project_id: Annotated[str, Field(description="Project ID")]
        ) -> get_project_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/projects/get/",
                data={"project_id": project_id},
                context=context
            )
            return [json.dumps(response.data)]

        create_session_output = mcp_output(
            description="Created session details including session ID and connect URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a new Browserbase browser session.",
            meta=mcp_meta("create_session"),
            structured_output=True
        )
        async def create_session(
            project_id: Annotated[str, Field(description="Project ID for the session")],
            browser_settings: Annotated[Optional[Dict[str, Any]], Field(description="Browser configuration settings")] = None,
            timeout: Annotated[Optional[int], Field(description="Session timeout in seconds")] = None
        ) -> create_session_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/create/",
                data={"project_id": project_id, "browser_settings": browser_settings, "timeout": timeout},
                context=context
            )
            return [json.dumps(response.data)]

        list_sessions_output = mcp_output(
            description="List of browser sessions",
            examples=[''])
        @self._mcp.tool(
            description="List Browserbase sessions, optionally filtered by project or status.",
            meta=mcp_meta("list_sessions"),
            structured_output=True
        )
        async def list_sessions(
            project_id: Annotated[Optional[str], Field(description="Filter by project ID")] = None,
            status: Annotated[Optional[str], Field(description="Filter by status (RUNNING, COMPLETED, ERROR)")] = None
        ) -> list_sessions_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/",
                data={"project_id": project_id, "status": status},
                context=context
            )
            return [json.dumps(response.data)]

        get_session_output = mcp_output(
            description="Detailed information about a specific browser session",
            examples=[''])
        @self._mcp.tool(
            description="Get a specific Browserbase session by ID.",
            meta=mcp_meta("get_session"),
            structured_output=True
        )
        async def get_session(
            session_id: Annotated[str, Field(description="Session ID")]
        ) -> get_session_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/get/",
                data={"session_id": session_id},
                context=context
            )
            return [json.dumps(response.data)]

        stop_session_output = mcp_output(
            description="Confirmation of session stop",
            examples=[''])
        @self._mcp.tool(
            description="Stop a running Browserbase session.",
            meta=mcp_meta("stop_session"),
            structured_output=True
        )
        async def stop_session(
            session_id: Annotated[str, Field(description="Session ID to stop")]
        ) -> stop_session_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/stop/",
                data={"session_id": session_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_session_recording_output = mcp_output(
            description="Recording data for the specified session",
            examples=[''])
        @self._mcp.tool(
            description="Get the recording for a Browserbase session.",
            meta=mcp_meta("get_session_recording"),
            structured_output=True
        )
        async def get_session_recording(
            session_id: Annotated[str, Field(description="Session ID")]
        ) -> get_session_recording_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/recording/",
                data={"session_id": session_id},
                context=context
            )
            return [json.dumps(response.data)]

        get_session_logs_output = mcp_output(
            description="Log entries for the specified session",
            examples=[''])
        @self._mcp.tool(
            description="Get the logs for a Browserbase session.",
            meta=mcp_meta("get_session_logs"),
            structured_output=True
        )
        async def get_session_logs(
            session_id: Annotated[str, Field(description="Session ID")]
        ) -> get_session_logs_output:
            context = self.get_context()
            response = self.client_service.post(
                f"{self.base_url}/sessions/logs/",
                data={"session_id": session_id},
                context=context
            )
            return [json.dumps(response.data)]
