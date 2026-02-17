from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/conversation',
    tags=['conversation']
)


@router.post("")
async def conversation(request: ChatRequest):
    """Process a text conversation with modern LangChain integration"""
    pass
