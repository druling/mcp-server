import json
import logging
from typing import Annotated, Optional
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import Output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GoogleDriveServer(BaseMCPServer):
    """MCP Server for Google Drive."""

    name: str = "google_drive"
    category: str = "Google Drive"
    description: str = "Google Drive integration for managing files and folders in Google Drive."
    scope: str = "google_drive_access"
    backend_service = BackendClient()
    base_url = "/google/drive"

    def _register_prompts(self) -> None:
        """Register all Google Drive prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Google Drive tools with the MCP server."""

        @self._mcp.tool(
            description="Search for files in Google Drive using a query.",
            meta=mcp_meta("search_files"),
            structured_output=True
        )
        async def search_files(
            query: Annotated[str, Field(description="Search query (e.g., 'name contains \"document\"' or 'mimeType=\"application/pdf\"')")],
            max_results: Annotated[Optional[int], Field(description="Maximum number of results to return")] = 100
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/search/",
                data={
                    "query": query,
                    "max_results": max_results
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Copy a file in Google Drive.",
            meta=mcp_meta("copy_file"),
            structured_output=True
        )
        async def copy_file(
            new_title: Annotated[str, Field(description="Title for the copied file")],
            file_id: Annotated[Optional[str], Field(description="The ID of the file to copy")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file to copy")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/copy/",
                data={
                    "file_id": file_id,
                    "file_url": file_url,
                    "new_title": new_title
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Create a new folder in Google Drive.",
            meta=mcp_meta("create_folder"),
            structured_output=True
        )
        async def create_folder(
            folder_name: Annotated[str, Field(description="Name of the new folder")],
            parent_folder_id: Annotated[Optional[str], Field(description="ID of the parent folder (optional)")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/folder/create/",
                data={
                    "folder_name": folder_name,
                    "parent_folder_id": parent_folder_id
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Move a file to a different folder in Google Drive.",
            meta=mcp_meta("move_file"),
            structured_output=True
        )
        async def move_file(
            destination_folder_id: Annotated[str, Field(description="ID of the destination folder")],
            file_id: Annotated[Optional[str], Field(description="The ID of the file to move")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file to move")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/move/",
                data={
                    "file_id": file_id,
                    "file_url": file_url,
                    "destination_folder_id": destination_folder_id
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Upload a plain text file to Google Drive.",
            meta=mcp_meta("upload_file"),
            structured_output=True
        )
        async def upload_file(
            file_name: Annotated[str, Field(description="Name of the file to create")],
            file_content: Annotated[Optional[str], Field(description="Content of the file")] = "",
            parent_folder_id: Annotated[Optional[str], Field(description="ID of the parent folder (optional)")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/upload/",
                data={
                    "file_name": file_name,
                    "file_content": file_content,
                    "parent_folder_id": parent_folder_id
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Change sharing permissions for a file in Google Drive.",
            meta=mcp_meta("change_permissions"),
            structured_output=True
        )
        async def change_permissions(
            file_id: Annotated[Optional[str], Field(description="The ID of the file")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file")] = None,
            permission_type: Annotated[Optional[str], Field(description="Type of permission: 'anyone', 'user', 'group', 'domain'")] = "anyone",
            permission_role: Annotated[Optional[str], Field(description="Role: 'reader', 'writer', 'commenter'")] = "reader",
            email_address: Annotated[Optional[str], Field(description="Email address for user/group permissions")] = None,
            domain: Annotated[Optional[str], Field(description="Domain for domain permissions")] = None,
            send_notification: Annotated[Optional[bool], Field(description="Whether to send notification email")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/permissions/",
                data={
                    "file_id": file_id,
                    "file_url": file_url,
                    "permission_type": permission_type,
                    "permission_role": permission_role,
                    "email_address": email_address,
                    "domain": domain,
                    "send_notification": send_notification
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Rename a file in Google Drive.",
            meta=mcp_meta("rename_file"),
            structured_output=True
        )
        async def rename_file(
            new_name: Annotated[str, Field(description="New name for the file")],
            file_id: Annotated[Optional[str], Field(description="The ID of the file to rename")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file to rename")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/rename/",
                data={
                    "file_id": file_id,
                    "file_url": file_url,
                    "new_name": new_name
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Get a file from Google Drive (download).",
            meta=mcp_meta("get_file"),
            structured_output=True
        )
        async def get_file(
            file_id: Annotated[Optional[str], Field(description="The ID of the file to get")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file to get")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/file/",
                data={
                    "file_id": file_id,
                    "file_url": file_url
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="List contents of a folder in Google Drive.",
            meta=mcp_meta("list_folder_contents"),
            structured_output=True
        )
        async def list_folder_contents(
            folder_id: Annotated[Optional[str], Field(description="The ID of the folder")] = None,
            folder_url: Annotated[Optional[str], Field(description="The URL of the folder")] = None,
            recursive: Annotated[Optional[bool], Field(description="Whether to list contents recursively")] = False,
            only_drive_link: Annotated[Optional[bool], Field(description="Return only Drive links")] = False,
            only_doc_link: Annotated[Optional[bool], Field(description="Return only Doc links")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/folder/contents/",
                data={
                    "folder_id": folder_id,
                    "folder_url": folder_url,
                    "recursive": recursive,
                    "only_drive_link": only_drive_link,
                    "only_doc_link": only_doc_link
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Delete a file or folder from Google Drive.",
            meta=mcp_meta("delete_file"),
            structured_output=True
        )
        async def delete_file(
            file_id: Annotated[Optional[str], Field(description="The ID of the file to delete")] = None,
            file_url: Annotated[Optional[str], Field(description="The URL of the file to delete")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/delete/",
                data={
                    "file_id": file_id,
                    "file_url": file_url
                },
                context=context
            )
            return [json.dumps(response.data)]
