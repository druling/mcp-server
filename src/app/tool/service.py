import logging

from src.core.exceptions.BaseError import BaseError

logger = logging.getLogger(__name__)


class LLMConversationService:
    async def llm_service(self, request):
        """Get LLM service based on provider and model"""
        try:
            pass
        except Exception as e:
            raise BaseError(f"Error getting LLM service: {e}")

    async def conversation(self, request):
        """Process a text conversation with modern LangChain integration"""
        try:
            llm_service = await self.llm_service(request)
            return await llm_service.process()
        except Exception as e:
            logger.error(f"Error processing conversation: {e}")
            raise BaseError("Error while processing conversation", original_exception=e)
