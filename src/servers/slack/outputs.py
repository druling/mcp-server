from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class Channel(BaseModel):
    """Slack channel"""
    id: str = Field(description="Channel ID")
    name: str = Field(description="Channel name")
    is_channel: Optional[bool] = Field(default=None, description="Whether it's a channel")
    is_private: Optional[bool] = Field(default=None, description="Whether it's private")
    is_member: Optional[bool] = Field(default=None, description="Whether user is a member")


class ChannelList(BaseModel):
    """List of channels"""
    channels: List[Channel] = Field(description="List of channels")
    count: int = Field(description="Total number of channels")


class User(BaseModel):
    """Slack user"""
    id: str = Field(description="User ID")
    name: str = Field(description="User name")
    real_name: Optional[str] = Field(default=None, description="Real name")
    email: Optional[str] = Field(default=None, description="Email address")
    is_bot: Optional[bool] = Field(default=None, description="Whether it's a bot")


class UserList(BaseModel):
    """List of users"""
    users: List[User] = Field(description="List of users")
    count: int = Field(description="Total number of users")


class Message(BaseModel):
    """Slack message"""
    ts: str = Field(description="Message timestamp")
    text: str = Field(description="Message text")
    user: Optional[str] = Field(default=None, description="User ID")
    channel: Optional[str] = Field(default=None, description="Channel ID")
    thread_ts: Optional[str] = Field(default=None, description="Thread timestamp")


class MessageList(BaseModel):
    """List of messages"""
    messages: List[Message] = Field(description="List of messages")
    count: int = Field(description="Total number of messages")


class MessageResult(BaseModel):
    """Result of sending a message"""
    success: bool = Field(description="Whether the message was sent successfully")
    ts: Optional[str] = Field(default=None, description="Message timestamp")
    channel: Optional[str] = Field(default=None, description="Channel ID")
    message: Optional[str] = Field(default=None, description="Status message")


class CanvasResult(BaseModel):
    """Result of canvas operation"""
    success: bool = Field(description="Whether the operation was successful")
    canvas_id: Optional[str] = Field(default=None, description="Canvas ID")
    message: Optional[str] = Field(default=None, description="Status message")


class ChannelInfo(BaseModel):
    """Slack channel information"""
    id: str = Field(description="Channel ID")
    name: str = Field(description="Channel name")
    topic: Optional[str] = Field(default=None, description="Channel topic")
    purpose: Optional[str] = Field(default=None, description="Channel purpose")
    is_private: Optional[bool] = Field(default=None, description="Whether it's private")
    num_members: Optional[int] = Field(default=None, description="Number of members")


class ThreadLink(BaseModel):
    """Thread link"""
    link: str = Field(description="Thread permalink")

