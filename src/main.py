import contextlib
import logging
import signal

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.servers.druling.workflow.mcp import WorkflowMCPServer
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

# Initialize MCP servers
workflow_server = WorkflowMCPServer()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Combined lifespan to manage MCP session managers."""
    logger.info("Druling MCP Server application starting up...")
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(workflow_server.mcp.session_manager.run())
        # Add more MCP servers here as needed:
        # await stack.enter_async_context(another_server.mcp.session_manager.run())
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

# Mount MCP servers (use streamable_http_app() from server, not mcp, to include middleware)
app.mount("/workflow", workflow_server.streamable_http_app())

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
