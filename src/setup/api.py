from fastapi import FastAPI
from src.app.heatlh_check.api import router as health_routes
from src.app.tool.api import router as tool_routes


def register_routes(app: FastAPI):
    app.include_router(health_routes)
    app.include_router(tool_routes)
