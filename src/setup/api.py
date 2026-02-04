from fastapi import FastAPI
from src.app.health_check.api import router as health_routes
from src.app.llm_model.api import router as llm_routes
from src.app.conversation.api import router as llm_query_routes
from src.app.llm_pricing.api import router as llm_pricing_routes
from src.app.asset_conversation.api.asset import router as asset_conversation_routes
from src.app.asset_conversation.api.pdf import router as pdf_conversation_routes



def register_routes(app: FastAPI):
    app.include_router(health_routes)
    app.include_router(llm_routes)
    app.include_router(llm_pricing_routes)
    app.include_router(llm_query_routes)
    app.include_router(asset_conversation_routes)
    app.include_router(pdf_conversation_routes)
