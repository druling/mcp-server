import logging
import signal
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.setup.api import register_routes

load_dotenv()
logger = logging.getLogger("mcp_server")

# Global shutdown flag
shutdown_event = False


def signal_handler(signum, frame):
    global shutdown_event
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event = True


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Druling MCP Server application starting up...")
    yield
    # Shutdown
    logger.info("Druling MCP Server application shutting down...")


app = FastAPI(
    title="Druling MCP Server",
    description="Druling MCP Server",
    version="1.0.0",
    lifespan=lifespan,
)

register_routes(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
