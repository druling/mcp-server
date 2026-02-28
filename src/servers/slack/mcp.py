import json
import logging
from typing import Annotated, Optional, List
from dataclasses import dataclass

from pydantic import Field

from src.clients.backend.client import BackendClient
from src.core.outputs import mcp_output
from src.core.service import BaseMCPServer
from src.core.utils.mcp_tool_meta import mcp_meta
from .prompts import prompts

logger = logging.getLogger(__name__)


@dataclass
class SlackServer(BaseMCPServer):
    """MCP Server for Slack."""

    name: str = "slack"
    category: str = "Slack"
    description: str = "Slack integration for messaging and team collaboration."
    scope: str = "slack_access"
    backend_service = BackendClient()
    base_url = "/slack"

    def _register_prompts(self) -> None:
        """Register all Slack prompts with the MCP server."""
        prompts(self._mcp, self.get_context)

    def _register_tools(self) -> None:
        """Register all Slack tools with the MCP server."""

        get_channels_output = mcp_output(
            description="List of all workspace channels with channel ID, name, topic, and member count",
            examples=[''])
        @self._mcp.tool(
            description="Get list of all channels in the workspace.",
            meta=mcp_meta("get_channels"),
            structured_output=True
        )
        async def get_channels() -> get_channels_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/channels/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        get_users_output = mcp_output(
            description="List of all workspace users with user ID, name, email, and profile information",
            examples=[''])
        @self._mcp.tool(
            description="Get list of all users in the workspace.",
            meta=mcp_meta("get_users"),
            structured_output=True
        )
        async def get_users() -> get_users_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/users/",
                data={},
                context=context
            )
            return [json.dumps(response.data)]

        send_message_output = mcp_output(
            description="Confirmation of the sent message including message timestamp and channel ID",
            examples=[''])
        @self._mcp.tool(
            description="Send a message to a Slack channel or user.",
            meta=mcp_meta("send_message"),
            structured_output=True
        )
        async def send_message(
            channel: Annotated[str, Field(description="Channel ID or name to send message to")],
            text: Annotated[str, Field(description="Message text to send")],
            thread: Annotated[Optional[str], Field(description="Thread timestamp to reply to")] = None,
            as_user: Annotated[Optional[bool], Field(description="Send as the authenticated user")] = False,
            hide_preview: Annotated[Optional[bool], Field(description="Hide link previews")] = False,
            file_urls: Annotated[Optional[List[str]], Field(description="List of file URLs to attach")] = None
        ) -> send_message_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/message/send/",
                data={
                    "channel": channel,
                    "text": text,
                    "thread": thread,
                    "as_user": as_user,
                    "hide_preview": hide_preview,
                    "file_urls": file_urls
                },
                context=context
            )
            return [json.dumps(response.data)]

        send_block_message_output = mcp_output(
            description="Confirmation of the sent block message including message timestamp and channel ID",
            examples=[''])
        @self._mcp.tool(
            description="Send a block message with rich formatting to Slack.",
            meta=mcp_meta("send_block_message"),
            structured_output=True
        )
        async def send_block_message(
            channel: Annotated[str, Field(description="Channel ID or name to send message to")],
            block_json: Annotated[str, Field(description="Block Kit JSON for rich formatting")],
            description: Annotated[Optional[str], Field(description="Fallback text description")] = None,
            thread: Annotated[Optional[str], Field(description="Thread timestamp to reply to")] = None,
            as_user: Annotated[Optional[bool], Field(description="Send as the authenticated user")] = False
        ) -> send_block_message_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/message/send-block/",
                data={
                    "channel": channel,
                    "block_json": block_json,
                    "description": description,
                    "thread": thread,
                    "as_user": as_user
                },
                context=context
            )
            return [json.dumps(response.data)]

        read_messages_output = mcp_output(
            description="List of messages from the channel with text, sender, timestamp, and thread info",
            examples=[''])
        @self._mcp.tool(
            description="Read messages from a Slack channel.",
            meta=mcp_meta("read_messages"),
            structured_output=True
        )
        async def read_messages(
            channel: Annotated[str, Field(description="Channel ID or name to read messages from")],
            limit: Annotated[Optional[int], Field(description="Maximum number of messages to retrieve")] = 100
        ) -> read_messages_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/message/read/",
                data={
                    "channel": channel,
                    "limit": limit
                },
                context=context
            )
            return [json.dumps(response.data)]

        conversation_replies_output = mcp_output(
            description="List of replies in the thread with text, sender, and timestamp",
            examples=[''])
        @self._mcp.tool(
            description="Get replies to a thread in Slack.",
            meta=mcp_meta("conversation_replies"),
            structured_output=True
        )
        async def conversation_replies(
            channel: Annotated[str, Field(description="Channel ID or name")],
            thread_ts: Annotated[str, Field(description="Thread timestamp")],
            limit: Annotated[Optional[int], Field(description="Maximum number of replies to retrieve")] = 100
        ) -> conversation_replies_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/thread/replies/",
                data={
                    "channel": channel,
                    "thread_ts": thread_ts,
                    "limit": limit
                },
                context=context
            )
            return [json.dumps(response.data)]

        create_canvas_output = mcp_output(
            description="Created canvas details including canvas ID, title, and URL",
            examples=[''])
        @self._mcp.tool(
            description="Create a Slack canvas for collaborative content.",
            meta=mcp_meta("create_canvas"),
            structured_output=True
        )
        async def create_canvas(
            channel: Annotated[str, Field(description="Channel ID to create canvas in")],
            title: Annotated[str, Field(description="Canvas title")],
            content: Annotated[str, Field(description="Canvas content")]
        ) -> create_canvas_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/canvas/create/",
                data={
                    "channel": channel,
                    "title": title,
                    "content": content
                },
                context=context
            )
            return [json.dumps(response.data)]

        set_canvas_access_output = mcp_output(
            description="Confirmation of updated canvas access permissions",
            examples=[''])
        @self._mcp.tool(
            description="Set access permissions for a Slack canvas.",
            meta=mcp_meta("set_canvas_access"),
            structured_output=True
        )
        async def set_canvas_access(
            canvas_id: Annotated[str, Field(description="Canvas ID")],
            channel_ids: Annotated[List[str], Field(description="List of channel IDs to grant access")],
            access_level: Annotated[Optional[str], Field(description="Access level: 'read' or 'write'")] = "read"
        ) -> set_canvas_access_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/canvas/access/",
                data={
                    "canvas_id": canvas_id,
                    "channel_ids": channel_ids,
                    "access_level": access_level
                },
                context=context
            )
            return [json.dumps(response.data)]

        channel_info_output = mcp_output(
            description="Channel details including ID, name, topic, purpose, member count, and creation date",
            examples=[''])
        @self._mcp.tool(
            description="Get information about a Slack channel.",
            meta=mcp_meta("channel_info"),
            structured_output=True
        )
        async def channel_info(
            channel: Annotated[str, Field(description="Channel ID or name")]
        ) -> channel_info_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/channel/info/",
                data={"channel": channel},
                context=context
            )
            return [json.dumps(response.data)]

        get_thread_link_output = mcp_output(
            description="Permalink URL to the specified message thread",
            examples=[''])
        @self._mcp.tool(
            description="Get a permalink to a specific message thread.",
            meta=mcp_meta("get_thread_link"),
            structured_output=True
        )
        async def get_thread_link(
            channel_id: Annotated[str, Field(description="Channel ID")],
            message_ts: Annotated[str, Field(description="Message timestamp")]
        ) -> get_thread_link_output:
            context = self.get_context()
            response = self.backend_service.post(
                f"{self.base_url}/thread/link/",
                data={
                    "channel_id": channel_id,
                    "message_ts": message_ts
                },
                context=context
            )
            return [json.dumps(response.data)]
