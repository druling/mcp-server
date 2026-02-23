from typing import Optional, List
from pydantic import BaseModel, Field


class SlideContent(BaseModel):
    """Structure for slide content"""
    slide_id: str = Field(description="ID of the slide")
    index: int = Field(description="Index of the slide in the presentation")
    content: str = Field(description="Text content of the slide")
    thumbnail: Optional[str] = Field(default=None, description="URL to the slide thumbnail")


class PresentationRead(BaseModel):
    """Structure for presentation read response"""
    presentation_id: str = Field(description="ID of the presentation")
    title: str = Field(description="Title of the presentation")
    slides: List[SlideContent] = Field(description="List of slides in the presentation")


class PresentationCreate(BaseModel):
    """Structure for presentation creation response"""
    presentation_id: str = Field(description="ID of the created presentation")
    presentation_url: str = Field(description="URL to view the presentation")


class PlaceholderList(BaseModel):
    """Structure for placeholders in a presentation"""
    placeholders: List[str] = Field(description="List of placeholders found in the presentation")

