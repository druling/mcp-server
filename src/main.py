import contextlib
import logging
import signal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from requests import Request

from src.core.exceptions import BaseError
from src.setup.api import register_routes
from src.setup.mcp import mount_mcp_servers, MCP_PATH
from src.core.middleware import InternalAuthMiddleware, RequestIDMiddleware, ExceptionHandlers

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

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Combined lifespan to manage MCP session managers."""
    logger.info("Druling MCP Server application starting up...")
    async with contextlib.AsyncExitStack() as stack:
        for server in MCP_PATH.values():
            await stack.enter_async_context(server.mcp.session_manager.run())
        yield
    logger.info("Druling MCP Server application shutting down...")


app = FastAPI(
    title="Druling MCP Server",
    description="Druling MCP Server",
    version="1.0.0",
    lifespan=lifespan,
)

# Register REST API routes
register_routes(app)

# Mount MCP servers
mount_mcp_servers(app)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(InternalAuthMiddleware)
app.add_middleware(RequestIDMiddleware)

@app.exception_handler(BaseError)
async def global_exception_handler(request: Request, exc: BaseError):
    return await ExceptionHandlers.handle_base_error(request, exc)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return await ExceptionHandlers.handle_global_exception(request, exc)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await ExceptionHandlers.handle_http_exception(request, exc)
