import json
import logging
from typing import Annotated, Optional, Dict
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import Output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GoogleDocsServer(BaseMCPServer):
    """MCP Server for Google Docs"""

    name: str = "google_docs"
    category: str = "Google Docs"
    description: str = "Google Docs integration for reading and managing documents in Google Drive."
    scope: str = "google_docs_access"
    backend_service = BackendClient()
    base_url = "/google/docs"

    def _register_prompts(self) -> None:
        """Register all Google Docs prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Google Docs tools with the MCP server."""

        @self._mcp.tool(
            description="Read a Google Doc document by ID or URL.",
            meta=mcp_meta("read_document"),
            structured_output=True
        )
        async def read_document(
            document_id: Annotated[Optional[str], Field(description="The ID of the document to read")] = None,
            document_url: Annotated[Optional[str], Field(description="The URL of the document to read")] = None,
            tabs: Annotated[Optional[list[str]], Field(description="List of tab IDs to read (optional)")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/read/",
                data={
                    "document_id": document_id,
                    "document_url": document_url,
                    "tabs": tabs
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Create a new Google Doc document.",
            meta=mcp_meta("create_document"),
            structured_output=True
        )
        async def create_document(
            title: Annotated[str, Field(description="Title of the new document")],
            content: Annotated[Optional[str], Field(description="Initial content for the document")] = "",
            format_type: Annotated[Optional[str], Field(description="Format type: 'plain_text' or 'html'")] = "plain_text",
            folder_id: Annotated[Optional[str], Field(description="Google Drive folder ID to create the document in")] = None,
            mark_as_public: Annotated[Optional[bool], Field(description="Whether to make the document publicly accessible")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create/",
                data={
                    "title": title,
                    "content": content,
                    "format_type": format_type,
                    "folder_id": folder_id,
                    "mark_as_public": mark_as_public
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Update an existing Google Doc document with new content.",
            meta=mcp_meta("update_document"),
            structured_output=True
        )
        async def update_document(
            content: Annotated[str, Field(description="Content to add to the document")],
            document_id: Annotated[Optional[str], Field(description="The ID of the document to update")] = None,
            document_url: Annotated[Optional[str], Field(description="The URL of the document to update")] = None,
            format_type: Annotated[Optional[str], Field(description="Format type: 'plain_text' or 'html'")] = "plain_text",
            upsert_start: Annotated[Optional[bool], Field(description="Whether to insert content at the start (True) or end (False)")] = True
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/update/",
                data={
                    "document_id": document_id,
                    "document_url": document_url,
                    "content": content,
                    "format_type": format_type,
                    "upsert_start": upsert_start
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="List all tabs in a Google Doc document.",
            meta=mcp_meta("list_document_tabs"),
            structured_output=True
        )
        async def list_document_tabs(
            document_id: Annotated[Optional[str], Field(description="The ID of the document")] = None,
            document_url: Annotated[Optional[str], Field(description="The URL of the document")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/list_tabs/",
                data={
                    "document_id": document_id,
                    "document_url": document_url
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Create a new document from a template with placeholder replacements.",
            meta=mcp_meta("create_from_template"),
            structured_output=True
        )
        async def create_from_template(
            document_name: Annotated[str, Field(description="Name for the new document")],
            template_id: Annotated[Optional[str], Field(description="The ID of the template document")] = None,
            template_url: Annotated[Optional[str], Field(description="The URL of the template document")] = None,
            placeholders: Annotated[Optional[Dict[str, str]], Field(description="Dictionary of placeholder replacements (e.g., {'{{name}}': 'John Doe'})")] = None,
            folder_id: Annotated[Optional[str], Field(description="Google Drive folder ID to create the document in")] = None,
            make_public: Annotated[Optional[bool], Field(description="Whether to make the document publicly accessible")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create_from_template/",
                data={
                    "template_id": template_id,
                    "template_url": template_url,
                    "placeholders": placeholders or {},
                    "document_name": document_name,
                    "folder_id": folder_id,
                    "make_public": make_public
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Find all placeholders in a Google Doc template.",
            meta=mcp_meta("find_placeholders"),
            structured_output=True
        )
        async def find_placeholders(
            template_id: Annotated[Optional[str], Field(description="The ID of the template document")] = None,
            template_url: Annotated[Optional[str], Field(description="The URL of the template document")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/find_placeholders/",
                data={
                    "template_id": template_id,
                    "template_url": template_url
                },
                context=context
            )
            return [json.dumps(response.data)]
