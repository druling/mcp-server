from fastapi import APIRouter
import logging

from src.app.tool.service import ToolService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/tool',
    tags=['tool']
)
tool_service = ToolService()

@router.get("/all")
async def all():
    """Process a text conversation with modern LangChain integration"""
    return tool_service.all()

@router.get("/{tool_name}")
async def get_service_tools(tool_name: str):
    """Get tools for a specific service"""
    return tool_service.get_service_tools(tool_name)
