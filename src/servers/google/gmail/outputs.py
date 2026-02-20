from typing import Optional
from pydantic import BaseModel, Field

# Pydantic models for structured output
class GmailRead(BaseModel):
    id: str = Field(description="Unique identifier for the email")
    subject: str = Field(description="Subject of the email")
    sender: str = Field(description="Email address of the sender")
    recipient: str = Field(description="Email address of the recipient")
    date: str = Field(description="Date when the email was received")
    snippet: str = Field(description="Short preview of the email content")
    body: Optional[str] = Field(default=None, description="Full body content of the email")

class ListGmailRead(BaseModel):
    result: list[GmailRead] = Field(description="List of workflow components")
