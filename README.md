# Druling MCP Server

## Install all dependencies
- Run `pip install -r requirements-dev.txt`

## How to run app using Docker with PostgreSQL
- Install Docker Desktop
- Run `docker compose up --build`
- Run `docker compose down` to stop all services

## How to run locally without postgres or docker
- In database/core.py change the DATABASE_URL to sqlite
- Run `make run`

## How to run tests
- Run `pytest` to run all tests

---

## How to Add a New MCP Server

MCP (Model Context Protocol) servers provide tools and prompts for AI integrations. Follow these steps to add a new MCP server:

### Step 1: Create the MCP Server Directory

Create a new directory under `src/servers/` for your MCP server:

```
src/servers/<provider>/<service>/
    __init__.py
    mcp.py
    outputs.py
    prompts.py
```

For example, to add a new "calendar" service under Google:
```
src/servers/google/calendar/
    __init__.py
    mcp.py
    outputs.py
    prompts.py
```

### Step 2: Define Output Models (`outputs.py`)

Create Pydantic models for your tool outputs:

### Step 3: Define Prompts (`prompts.py`)

Create prompts for your MCP server (optional):

### Step 4: Create the MCP Server (`mcp.py`)

Create the MCP server class by extending `BaseMCPServer`:

### Step 5: Register the MCP Server

Update `src/setup/mcp.py` to register your new MCP server:

```python
from src.servers.google.calendar.mcp import CalendarMCPServer

# Add to existing imports and initializations
calendar_server = CalendarMCPServer()

MCP_PATH = {
    # ...existing servers...
    "calendar": calendar_server,
}
```

The server will automatically:
- Be mounted at `/<server_name>` (e.g., `/calendar`)
- Have session management handled by the lifespan context
- Include authentication and context middleware

---

## How to Add a New REST API

REST APIs are used for standard HTTP endpoints. Follow these steps to add a new API:

### Step 1: Create the API Directory

Create a new directory under `src/app/` for your API:

```
src/app/<feature>/
    __init__.py
    api.py
```

For example, to add a "users" API:
```
src/app/users/
    __init__.py
    api.py
```

### Step 2: Create the API Router (`api.py`)

Create the FastAPI router with your endpoints:

### Step 3: Register the API Router

Update `src/setup/api.py` to include your new router:

---

## Project Structure Overview

```
src/
├── main.py                 # FastAPI app entry point
├── setup/
│   ├── api.py              # REST API route registration
│   └── mcp.py              # MCP server registration
├── app/                    # REST API endpoints
│   ├── health_check/
│   ├── auth/
│   └── <your_api>/
├── servers/                # MCP servers
│   ├── google/
│   │   ├── gmail/
│   │   ├── drive/
│   │   └── <your_service>/
│   ├── druling/
│   └── <your_provider>/
├── core/
│   ├── service/            # Base MCP server class
│   ├── middleware/         # Auth and context middleware
│   ├── exceptions/         # Custom exceptions
│   └── utils/              # Utility functions
└── clients/
    └── backend/            # Backend API client
```

---

## Key Concepts

### MCP Server
- Extends `BaseMCPServer` from `src.core.service`
- Provides tools (functions) and prompts for AI agents
- Uses `@self._mcp.tool()` decorator to register tools
- Uses `mcp_meta()` for tool metadata
- Access user context via `self.get_context()`

### REST API
- Uses FastAPI's `APIRouter`
- Registered via `app.include_router()`
- Standard REST conventions with proper status codes

### Backend Client
- Use `BackendClient` from `src.clients.backend.client` to call backend services
- Supports `get()`, `post()`, `put()`, `delete()` methods
- Pass `context` for authenticated requests

