from fastapi import FastAPI
from src.app.heatlh_check.api import router as health_routes
from src.app.auth.api import router as auth_routes


def register_routes(app: FastAPI):
    app.include_router(health_routes)
    app.include_router(auth_routes)
