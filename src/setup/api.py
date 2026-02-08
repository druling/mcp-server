from fastapi import FastAPI
from src.app.heatlh_check.api import router as health_routes


def register_routes(app: FastAPI):
    app.include_router(health_routes)
