import json
import logging
from typing import Annotated, Optional, List
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import Output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class GmailServer(BaseMCPServer):
    """MCP Server for Gmail."""

    name: str = "gmail"
    category: str = "Gmail"
    description: str = "Gmail integration for reading emails and performing actions on Gmail accounts."
    scope: str = "gmail_access"
    backend_service = BackendClient()
    base_url = "/google/gmail"

    def _register_prompts(self) -> None:
        """Register all Gmail prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Gmail tools with the MCP server."""

        @self._mcp.tool(
            description="Read emails in the user's Gmail account with optional search filters.",
            meta=mcp_meta("read_emails"),
            structured_output=True
        )
        async def read_emails(
            query: Annotated[Optional[str], Field(description="Search query to filter emails (e.g., 'from:name@example.com' or 'subject:meeting')")] = None,
            max_results: Annotated[Optional[int], Field(description="Maximum number of emails to retrieve")] = 10
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/read/",
                data={
                    "query": query,
                    "max_results": max_results
                },
                context=context
            )
            return [json.dumps(item) for item in response.data]

        @self._mcp.tool(
            description="Send an email or create a draft. Can also reply to an existing thread.",
            meta=mcp_meta("send_email"),
            structured_output=True
        )
        async def send_email(
            to: Annotated[str, Field(description="Recipient email address")],
            subject: Annotated[str, Field(description="Email subject")],
            body: Annotated[Optional[str], Field(description="Plain text body of the email")] = None,
            html_body: Annotated[Optional[str], Field(description="HTML body of the email")] = None,
            send_as: Annotated[Optional[str], Field(description="Email address to send from (if delegated)")] = None,
            sender_name: Annotated[Optional[str], Field(description="Display name for the sender")] = None,
            reply_email: Annotated[Optional[str], Field(description="Reply-to email address")] = None,
            attachments: Annotated[Optional[List[str]], Field(description="List of attachment URLs or file paths")] = None,
            thread_id: Annotated[Optional[str], Field(description="Thread ID to reply to (for replies)")] = None,
            save_as_draft: Annotated[Optional[bool], Field(description="Save as draft instead of sending")] = False,
            is_reply: Annotated[Optional[bool], Field(description="Whether this is a reply to an existing email")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/send/",
                data={
                    "to": to,
                    "subject": subject,
                    "body": body,
                    "html_body": html_body,
                    "send_as": send_as,
                    "sender_name": sender_name,
                    "reply_email": reply_email,
                    "attachments": attachments,
                    "thread_id": thread_id,
                    "save_as_draft": save_as_draft,
                    "is_reply": is_reply
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Update an email (mark as read, add/remove labels).",
            meta=mcp_meta("update_email"),
            structured_output=True
        )
        async def update_email(
            message_id: Annotated[str, Field(description="ID of the message to update")],
            mark_as_read: Annotated[Optional[bool], Field(description="Mark the email as read")] = False,
            add_labels: Annotated[Optional[List[str]], Field(description="List of label IDs to add")] = None,
            remove_labels: Annotated[Optional[List[str]], Field(description="List of label IDs to remove")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/update/",
                data={
                    "message_id": message_id,
                    "mark_as_read": mark_as_read,
                    "add_labels": add_labels or [],
                    "remove_labels": remove_labels or []
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Create a draft email without sending it.",
            meta=mcp_meta("create_draft"),
            structured_output=True
        )
        async def create_draft(
            to: Annotated[str, Field(description="Recipient email address")],
            subject: Annotated[str, Field(description="Email subject")],
            body: Annotated[Optional[str], Field(description="Plain text body of the email")] = None,
            html_body: Annotated[Optional[str], Field(description="HTML body of the email")] = None,
            send_as: Annotated[Optional[str], Field(description="Email address to send from (if delegated)")] = None,
            sender_name: Annotated[Optional[str], Field(description="Display name for the sender")] = None,
            reply_email: Annotated[Optional[str], Field(description="Reply-to email address")] = None,
            attachments: Annotated[Optional[List[str]], Field(description="List of attachment URLs or file paths")] = None,
            thread_id: Annotated[Optional[str], Field(description="Thread ID to attach to")] = None
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create_draft/",
                data={
                    "to": to,
                    "subject": subject,
                    "body": body,
                    "html_body": html_body,
                    "send_as": send_as,
                    "sender_name": sender_name,
                    "reply_email": reply_email,
                    "attachments": attachments,
                    "thread_id": thread_id
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Forward an email to another recipient.",
            meta=mcp_meta("forward_email"),
            structured_output=True
        )
        async def forward_email(
            to: Annotated[str, Field(description="Recipient email address")],
            subject: Annotated[str, Field(description="Email subject")],
            body: Annotated[Optional[str], Field(description="Additional message to add")] = None,
            html_body: Annotated[Optional[str], Field(description="HTML body of the email")] = None,
            send_as: Annotated[Optional[str], Field(description="Email address to send from (if delegated)")] = None,
            sender_name: Annotated[Optional[str], Field(description="Display name for the sender")] = None,
            reply_email: Annotated[Optional[str], Field(description="Reply-to email address")] = None,
            attachments: Annotated[Optional[List[str]], Field(description="List of attachment URLs or file paths")] = None,
            thread_id: Annotated[Optional[str], Field(description="Thread ID to forward")] = None,
            save_as_draft: Annotated[Optional[bool], Field(description="Save as draft instead of sending")] = False
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/forward/",
                data={
                    "to": to,
                    "subject": subject,
                    "body": body,
                    "html_body": html_body,
                    "send_as": send_as,
                    "sender_name": sender_name,
                    "reply_email": reply_email,
                    "attachments": attachments,
                    "thread_id": thread_id,
                    "save_as_draft": save_as_draft
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Create a new label in Gmail.",
            meta=mcp_meta("create_label"),
            structured_output=True
        )
        async def create_label(
            label_name: Annotated[str, Field(description="Name of the new label")],
            label_list_visibility: Annotated[Optional[str], Field(description="Visibility in label list: 'labelShow', 'labelShowIfUnread', 'labelHide'")] = "labelShow",
            message_list_visibility: Annotated[Optional[str], Field(description="Visibility in message list: 'show', 'hide'")] = "show"
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/create_label/",
                data={
                    "label_name": label_name,
                    "label_list_visibility": label_list_visibility,
                    "message_list_visibility": message_list_visibility
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Archive an email (remove from inbox).",
            meta=mcp_meta("archive_email"),
            structured_output=True
        )
        async def archive_email(
            message_id: Annotated[str, Field(description="ID of the message to archive")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/archive_email/",
                data={"message_id": message_id},
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Move an email to trash.",
            meta=mcp_meta("trash_email"),
            structured_output=True
        )
        async def trash_email(
            message_id: Annotated[str, Field(description="ID of the message to trash")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/trash/",
                data={"message_id": message_id},
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Star an email.",
            meta=mcp_meta("star_email"),
            structured_output=True
        )
        async def star_email(
            message_id: Annotated[str, Field(description="ID of the message to star")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/start/",
                data={"message_id": message_id},
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Unstar an email.",
            meta=mcp_meta("unstar_email"),
            structured_output=True
        )
        async def unstar_email(
            message_id: Annotated[str, Field(description="ID of the message to unstar")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/unstart/",
                data={"message_id": message_id},
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="Get an attachment from an email.",
            meta=mcp_meta("get_attachment"),
            structured_output=True
        )
        async def get_attachment(
            message_id: Annotated[str, Field(description="ID of the message containing the attachment")],
            attachment_id: Annotated[str, Field(description="ID of the attachment to retrieve")]
        ) -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/get_attachment/",
                data={
                    "message_id": message_id,
                    "attachment_id": attachment_id
                },
                context=context
            )
            return [json.dumps(response.data)]

        @self._mcp.tool(
            description="List all labels in Gmail account.",
            meta=mcp_meta("list_labels"),
            structured_output=True
        )
        async def list_labels() -> Output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/list_labels/",
                data={},
                context=context
            )
            return [json.dumps(item) for item in response.data]
