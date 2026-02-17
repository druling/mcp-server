from fastapi import APIRouter
import logging

from src.app.tool.service import ToolService
from src.core.api.responses import ResponseFactory

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/tool',
    tags=['tool']
)
tool_service = ToolService()

@router.get("/all")
async def all():
    """Get all tools"""
    tools = tool_service.all()
    return ResponseFactory.success(tools)

@router.get("/{tool_name}")
async def get_service_tools(tool_name: str):
    """Get details of a specific tool by name"""
    tool_details = tool_service.get_service_tools(tool_name)
    return ResponseFactory.success(tool_details)
