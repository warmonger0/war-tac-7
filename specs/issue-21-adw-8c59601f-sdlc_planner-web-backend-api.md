# Feature: Web Backend API for tac-webbuilder

## Metadata
issue_number: `21`
adw_id: `8c59601f`
issue_json: `{"number":21,"title":"web-backend","body":"# 🎯 ISSUE 4: tac-webbuilder - Web UI Backend API\n\n## Overview\nBuild FastAPI backend server to power the web interface for submitting requests and monitoring workflows.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory.\n\n## Dependencies\n**Requires**: Issue 2 (NL Processing & Issue Formatter) to be completed\n\n## Tasks\n\n### 1. FastAPI Server Setup\n**File**: `interfaces/web/server.py`\n\n```python\nfrom fastapi import FastAPI, WebSocket\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI(title=\"tac-webbuilder API\")\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\"http://localhost:5174\"],\n    allow_credentials=True,\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)\n```\n\n### 2. API Routes\n**File**: `interfaces/web/routes/requests.py`\n\n```python\nfrom fastapi import APIRouter, HTTPException\nfrom pydantic import BaseModel\n\nrouter = APIRouter(prefix=\"/api\")\n\nclass SubmitRequest(BaseModel):\n    nl_input: str\n    project_path: str | None = None\n    auto_post: bool = False\n\n@router.post(\"/request\")\nasync def submit_request(req: SubmitRequest):\n    \"\"\"\n    Submit NL request.\n    Returns: request_id for tracking\n    \"\"\"\n\n@router.get(\"/preview/{request_id}\")\nasync def get_preview(request_id: str):\n    \"\"\"\n    Get formatted issue preview.\n    Returns: GitHubIssue object\n    \"\"\"\n\n@router.post(\"/confirm/{request_id}\")\nasync def confirm_and_post(request_id: str):\n    \"\"\"\n    Confirm and post issue to GitHub.\n    Returns: issue_number, github_url\n    \"\"\"\n```\n\n**File**: `interfaces/web/routes/workflows.py`\n\n```python\n@router.get(\"/workflows\")\nasync def list_workflows():\n    \"\"\"\n    List active ADW workflows.\n    Returns: List of workflows with status\n    \"\"\"\n\n@router.get(\"/workflows/{adw_id}\")\nasync def get_workflow_status(adw_id: str):\n    \"\"\"\n    Get detailed status of specific workflow.\n    Returns: ADWState with progress info\n    \"\"\"\n```\n\n**File**: `interfaces/web/routes/projects.py`\n\n```python\n@router.get(\"/projects\")\nasync def list_projects():\n    \"\"\"\n    List configured projects.\n    Returns: Project list with context\n    \"\"\"\n\n@router.post(\"/projects\")\nasync def add_project(path: str):\n    \"\"\"\n    Add new project and analyze it.\n    Returns: ProjectContext\n    \"\"\"\n\n@router.get(\"/projects/{project_id}/context\")\nasync def get_project_context(project_id: str):\n    \"\"\"\n    Get detected context for project.\n    Returns: ProjectContext with framework, stack, etc.\n    \"\"\"\n```\n\n**File**: `interfaces/web/routes/history.py`\n\n```python\n@router.get(\"/history\")\nasync def get_history(limit: int = 20):\n    \"\"\"\n    Get request history.\n    Returns: List of past requests with status\n    \"\"\"\n```\n\n### 3. WebSocket for Real-time Updates\n**File**: `interfaces/web/websocket.py`\n\n```python\nfrom fastapi import WebSocket, WebSocketDisconnect\n\nclass ConnectionManager:\n    def __init__(self):\n        self.active_connections: list[WebSocket] = []\n\n    async def broadcast(self, message: dict):\n        \"\"\"Broadcast workflow updates to all clients.\"\"\"\n\nmanager = ConnectionManager()\n\n@app.websocket(\"/ws\")\nasync def websocket_endpoint(websocket: WebSocket):\n    \"\"\"\n    WebSocket for real-time workflow updates.\n\n    Messages:\n    - workflow_started: {adw_id, issue_number}\n    - workflow_progress: {adw_id, phase, status}\n    - workflow_completed: {adw_id, pr_url}\n    \"\"\"\n```\n\n### 4. Request State Management\n**File**: `interfaces/web/state.py`\n\n```python\nfrom uuid import uuid4\nimport json\n\nclass RequestState:\n    \"\"\"Manage in-progress requests before GitHub posting.\"\"\"\n\n    def __init__(self):\n        self.pending_requests: dict[str, dict] = {}\n\n    def create_request(\n        self,\n        nl_input: str,\n        project_context: ProjectContext\n    ) -> str:\n        \"\"\"\n        Create new request, generate preview.\n        Returns: request_id\n        \"\"\"\n\n    def get_preview(self, request_id: str) -> GitHubIssue:\n        \"\"\"Get formatted issue for preview.\"\"\"\n\n    def confirm_and_post(self, request_id: str) -> int:\n        \"\"\"Post to GitHub and return issue_number.\"\"\"\n```\n\n### 5. Workflow Monitor\n**File**: `interfaces/web/workflow_monitor.py`\n\n```python\nimport os\nfrom pathlib import Path\n\ndef list_active_workflows() -> list[dict]:\n    \"\"\"\n    Scan agents/ directory for active workflows.\n    Returns: List of ADWState objects\n    \"\"\"\n\ndef get_workflow_status(adw_id: str) -> dict:\n    \"\"\"\n    Read ADWState and agent logs.\n    Returns: Detailed status with phase progress\n    \"\"\"\n\ndef watch_workflow_changes():\n    \"\"\"\n    Monitor agents/ directory for changes.\n    Broadcast updates via WebSocket.\n    \"\"\"\n```\n\n### 6. Startup Script\n**File**: `scripts/start_web.sh`\n\n```bash\n#!/bin/bash\ncd \"$(dirname \"$0\")/..\"\n\n# Start backend\necho \"🚀 Starting web backend on port 8002...\"\nuv run uvicorn interfaces.web.server:app \\\n    --host 0.0.0.0 \\\n    --port 8002 \\\n    --reload\n\n# Note: Frontend started separately in Issue 5\n```\n\n## Dependencies (Python)\nAdd to `pyproject.toml`:\n```toml\nfastapi = \"^0.115.0\"\nuvicorn = \"^0.32.0\"\nwebsockets = \"^13.0\"\n```\n\n## Test Cases\nCreate `tests/interfaces/test_web_api.py`:\n\n```python\nfrom fastapi.testclient import TestClient\n\ndef test_submit_request():\n    \"\"\"Test POST /api/request\"\"\"\n\ndef test_preview_endpoint():\n    \"\"\"Test GET /api/preview/{id}\"\"\"\n\ndef test_confirm_and_post():\n    \"\"\"Test POST /api/confirm/{id}\"\"\"\n\ndef test_list_workflows():\n    \"\"\"Test GET /api/workflows\"\"\"\n\ndef test_websocket_connection():\n    \"\"\"Test WebSocket connectivity\"\"\"\n```\n\n## Success Criteria\n- ✅ FastAPI server runs on port 8002\n- ✅ All API endpoints functional\n- ✅ WebSocket broadcasts workflow updates\n- ✅ Request state properly managed\n- ✅ CORS configured for frontend\n- ✅ All tests pass\n\n## API Documentation\nFastAPI auto-generates docs at:\n- http://localhost:8002/docs (Swagger UI)\n- http://localhost:8002/redoc (ReDoc)\n\n## Next Issue\nAfter this completes:\n- **Issue 5**: Web UI - Frontend Dashboard\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`interface`, `web-backend`, `api`, `webbuilder`\n"}`

## Feature Description
Build a comprehensive FastAPI backend server that powers the web interface for the tac-webbuilder system. The API will provide endpoints for submitting natural language requests, monitoring ADW workflow execution, managing project contexts, and tracking request history. It includes WebSocket support for real-time workflow updates and integrates with the existing NL processing infrastructure from Issue #14.

## User Story
As a tac-webbuilder user accessing the web interface
I want a robust backend API that processes my requests and provides real-time workflow updates
So that I can submit natural language requests via a web UI and monitor their execution status without using the CLI

## Problem Statement
The tac-webbuilder currently has CLI support (Issue #16) and core NL processing capabilities (Issue #14), but lacks a web-accessible API layer. Users who prefer web interfaces over command-line tools need a REST API with WebSocket support to submit requests, preview generated GitHub issues, track workflow execution, and manage project configurations through a browser-based interface.

## Solution Statement
Implement a FastAPI-based backend server on port 8002 that provides:
- RESTful endpoints for request submission, issue preview, and GitHub posting
- WebSocket connections for real-time workflow status updates
- Project management endpoints for context detection and configuration
- History tracking endpoints for past requests
- Workflow monitoring endpoints for active ADW executions
- Request state management for preview-before-post workflow
- CORS middleware configured for frontend integration
- Auto-generated OpenAPI documentation

## Relevant Files
Use these files to implement the feature:

**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`

**Existing Files to Reference**:
- `README.md` - Project documentation and structure understanding
- `core/data_models.py` - Existing Pydantic models (GitHubIssue, ProjectContext, etc.). Will be extended with new web API models
- `core/nl_processor.py` - Natural language processing orchestration. Will be integrated into request endpoints
- `core/project_detector.py` - Project context detection logic. Will be used by project endpoints
- `core/github_poster.py` - GitHub CLI integration for posting issues. Will be used by confirm endpoint
- `core/issue_formatter.py` - Issue template formatting. Will be used for preview generation
- `adws/adw_modules/workflow_ops.py` - Workflow state management. Reference for workflow monitoring
- `adws/adw_modules/agent.py` - Agent execution patterns. Reference for understanding workflow states
- `interfaces/cli/history.py` - History tracking implementation. Will be referenced for API history endpoint
- `interfaces/cli/config_manager.py` - Configuration management. Will be referenced for project configuration

**Reference from Main Application**:
Since this is a separate tac-webbuilder project, reference the main application's API patterns:
- `app/server/server.py` - FastAPI server setup patterns, CORS configuration, error handling
- `app/server/main.py` - Server entry point patterns
- `app/server/core/data_models.py` - Pydantic model patterns

**Documentation**:
- `.claude/commands/conditional_docs.md` - Conditional documentation guide
- `.claude/commands/test_e2e.md` - E2E test execution patterns
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure

### New Files
The following files will be created to implement the web backend API:

**Core Server**:
- `interfaces/web/__init__.py` - Web interface package initialization
- `interfaces/web/server.py` - Main FastAPI application with middleware and router registration
- `interfaces/web/state.py` - Request state management for preview-before-post workflow
- `interfaces/web/websocket.py` - WebSocket connection manager for real-time updates
- `interfaces/web/workflow_monitor.py` - ADW workflow status monitoring and file system watching

**API Routes**:
- `interfaces/web/routes/__init__.py` - Routes package initialization
- `interfaces/web/routes/requests.py` - Request submission, preview, and confirmation endpoints
- `interfaces/web/routes/workflows.py` - Workflow listing and status endpoints
- `interfaces/web/routes/projects.py` - Project management and context endpoints
- `interfaces/web/routes/history.py` - Request history endpoints

**Data Models**:
- `interfaces/web/models.py` - Pydantic models specific to web API (request/response schemas)

**Scripts**:
- `scripts/start_web.sh` - Convenience script to start the web backend server

**Tests**:
- `tests/interfaces/web/__init__.py` - Web API test package initialization
- `tests/interfaces/web/test_server.py` - Server initialization and middleware tests
- `tests/interfaces/web/test_requests_routes.py` - Tests for request-related endpoints
- `tests/interfaces/web/test_workflows_routes.py` - Tests for workflow endpoints
- `tests/interfaces/web/test_projects_routes.py` - Tests for project endpoints
- `tests/interfaces/web/test_history_routes.py` - Tests for history endpoints
- `tests/interfaces/web/test_websocket.py` - WebSocket connection and broadcast tests
- `tests/interfaces/web/test_state.py` - Request state management tests
- `tests/interfaces/web/test_workflow_monitor.py` - Workflow monitoring tests

**E2E Test**:
- `.claude/commands/e2e/test_web_api.md` - End-to-end test for web API functionality

## Implementation Plan
### Phase 1: Foundation
Set up the FastAPI server infrastructure with proper CORS configuration, error handling, and middleware. Install required dependencies (fastapi, uvicorn, websockets) and create the web interface package structure. Establish patterns for route organization, request/response models, and error handling that will be consistent across all API endpoints. Define core Pydantic models for API requests and responses.

### Phase 2: Core Implementation
Implement the API route modules in this order:
1. **Request State Management** - Build the in-memory state manager for handling preview-before-post workflow
2. **Request Routes** - Implement endpoints for submitting requests, generating previews, and posting to GitHub
3. **Project Routes** - Implement endpoints for project detection, listing, and context retrieval
4. **History Routes** - Implement endpoint for retrieving request history
5. **Workflow Routes** - Implement workflow monitoring endpoints that read from agents/ directory
6. **WebSocket Manager** - Build WebSocket connection manager with broadcast capabilities
7. **Workflow Monitor** - Implement file system watching for agent directory changes and WebSocket broadcasting

### Phase 3: Integration
Connect the web API to existing tac-webbuilder infrastructure:
- Integrate with core NL processing modules (nl_processor, project_detector, github_poster)
- Connect to CLI history tracking system for unified history
- Implement workflow monitoring by reading ADW agent state files
- Set up proper error handling with meaningful HTTP status codes
- Configure CORS for frontend (port 5174)
- Create startup script for easy server launching
- Add comprehensive logging for debugging

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Install Dependencies and Update Project Configuration
- Navigate to `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`
- Add fastapi, uvicorn[standard], and websockets to `pyproject.toml` dependencies
- Run `uv sync` to install new dependencies
- Verify dependencies are properly installed by importing them in a test script

### Task 2: Create Web Interface Package Structure
- Create directory: `interfaces/web/`
- Create directory: `interfaces/web/routes/`
- Initialize `interfaces/web/__init__.py` with package exports
- Initialize `interfaces/web/routes/__init__.py`
- Set up basic package structure

### Task 3: Define Web API Data Models
- Create `interfaces/web/models.py`
- Define Pydantic models for API requests/responses:
  - `SubmitRequestModel` (nl_input, project_path, auto_post)
  - `RequestPreviewResponse` (request_id, github_issue, project_context)
  - `ConfirmResponse` (issue_number, github_url, workflow_info)
  - `WorkflowStatusResponse` (adw_id, phase, status, logs)
  - `WorkflowListResponse` (workflows list with summary info)
  - `ProjectListResponse` (projects with context summaries)
  - `HistoryResponse` (request history list)
- Import and reuse existing models from `core/data_models.py` where applicable (GitHubIssue, ProjectContext)
- Add comprehensive docstrings and field descriptions
- Write unit tests in `tests/interfaces/web/test_models.py` (if complex validation logic exists)

### Task 4: Implement Request State Manager
- Create `interfaces/web/state.py`
- Implement `RequestState` class:
  - `pending_requests: dict[str, dict]` for in-memory storage
  - `create_request(nl_input, project_context)` - generate UUID, store request, return request_id
  - `get_request(request_id)` - retrieve pending request
  - `get_preview(request_id)` - get formatted GitHub issue
  - `confirm_and_post(request_id)` - post to GitHub and remove from pending
  - `cleanup_old_requests()` - remove requests older than 24 hours
- Integrate with `core/nl_processor.py` for issue generation
- Integrate with `core/github_poster.py` for GitHub posting
- Add error handling for missing requests
- Write unit tests in `tests/interfaces/web/test_state.py`

### Task 5: Implement Request Routes
- Create `interfaces/web/routes/requests.py`
- Create APIRouter with prefix "/api"
- Implement endpoints:
  - `POST /api/request` - Accept SubmitRequestModel, validate project_path, call state.create_request(), return request_id
  - `GET /api/preview/{request_id}` - Get preview from state manager, return GitHubIssue
  - `POST /api/confirm/{request_id}` - Call state.confirm_and_post(), return issue number and URL
- Add request validation (check for required env vars, validate paths)
- Add error handling with appropriate HTTP status codes
- Add logging for all operations
- Write tests in `tests/interfaces/web/test_requests_routes.py` using TestClient

### Task 6: Implement Workflow Monitor
- Create `interfaces/web/workflow_monitor.py`
- Implement functions:
  - `list_active_workflows()` - scan agents/ directory, read ADW state files, return workflow summaries
  - `get_workflow_status(adw_id)` - read specific agent directory, parse logs, return detailed status
  - `parse_adw_state(adw_state_file)` - parse ADW state JSON files
  - `get_agent_logs(adw_id)` - read agent log files
- Reference `adws/adw_modules/workflow_ops.py` for ADW state structure
- Handle missing/corrupted state files gracefully
- Add caching to avoid excessive file system reads
- Write tests in `tests/interfaces/web/test_workflow_monitor.py`

### Task 7: Implement Workflow Routes
- Create `interfaces/web/routes/workflows.py`
- Create APIRouter with prefix "/api"
- Implement endpoints:
  - `GET /api/workflows` - Call workflow_monitor.list_active_workflows(), return list
  - `GET /api/workflows/{adw_id}` - Call workflow_monitor.get_workflow_status(adw_id), return detailed status
- Add error handling for missing workflows (404)
- Add query parameters for filtering (status, limit)
- Add logging
- Write tests in `tests/interfaces/web/test_workflows_routes.py`

### Task 8: Implement Project Routes
- Create `interfaces/web/routes/projects.py`
- Create APIRouter with prefix "/api"
- Implement endpoints:
  - `GET /api/projects` - List configured projects (read from config or scan common locations)
  - `POST /api/projects` - Accept project path, call detect_project_context(), save to config, return ProjectContext
  - `GET /api/projects/{project_id}/context` - Get cached project context
- Integrate with `core/project_detector.py` for context detection
- Store project configurations in a JSON file or extend existing config system
- Add path validation (ensure project exists)
- Write tests in `tests/interfaces/web/test_projects_routes.py`

### Task 9: Implement History Routes
- Create `interfaces/web/routes/history.py`
- Create APIRouter with prefix "/api"
- Implement endpoint:
  - `GET /api/history` - Read from CLI history system (interfaces/cli/history.py), return recent requests
  - Support query parameters: limit (default 20), offset for pagination
- Integrate with existing `interfaces/cli/history.py` RequestHistory class
- Add filtering options (by project, by date range)
- Write tests in `tests/interfaces/web/test_history_routes.py`

### Task 10: Implement WebSocket Manager
- Create `interfaces/web/websocket.py`
- Implement `ConnectionManager` class:
  - `active_connections: list[WebSocket]` - track connected clients
  - `connect(websocket)` - add websocket to connections
  - `disconnect(websocket)` - remove websocket from connections
  - `broadcast(message)` - send message to all connected clients
  - `send_to_client(websocket, message)` - send message to specific client
- Implement `/ws` endpoint that:
  - Accepts WebSocket connections
  - Keeps connection alive with periodic pings
  - Handles disconnections gracefully
- Define message format: `{"type": "workflow_started|workflow_progress|workflow_completed", "data": {...}}`
- Add error handling for connection failures
- Write tests in `tests/interfaces/web/test_websocket.py`

### Task 11: Integrate Workflow Monitor with WebSocket
- Update `interfaces/web/workflow_monitor.py`
- Add function `watch_workflow_changes(connection_manager)`:
  - Use file system watcher (watchdog library or polling) to monitor agents/ directory
  - When changes detected, parse updates and broadcast via WebSocket
  - Handle file creation, modification events
- Alternatively, implement polling mechanism that checks for changes every 2-5 seconds
- Broadcast workflow status changes to all connected WebSocket clients
- Add start/stop controls for the watcher
- Update tests to verify WebSocket integration

### Task 12: Implement Main FastAPI Application
- Create `interfaces/web/server.py`
- Initialize FastAPI app with title "tac-webbuilder API", version "1.0.0"
- Add CORS middleware:
  - allow_origins: ["http://localhost:5174"] (configurable via env var)
  - allow_credentials: True
  - allow_methods: ["*"]
  - allow_headers: ["*"]
- Register all routers:
  - Include requests router
  - Include workflows router
  - Include projects router
  - Include history router
- Add WebSocket endpoint
- Add health check endpoint: `GET /api/health` (return server status, version)
- Add startup event handler to initialize state manager and start workflow watcher
- Add shutdown event handler to cleanup resources
- Add global exception handler for unhandled errors
- Configure logging (match main app's logging format)
- Write tests in `tests/interfaces/web/test_server.py`

### Task 13: Create Server Startup Script
- Create `scripts/start_web.sh`
- Add shebang and navigate to project root
- Check for required environment variables (ANTHROPIC_API_KEY, GITHUB_REPO_URL)
- Kill any existing process on port 8002
- Execute `uv run uvicorn interfaces.web.server:app --host 0.0.0.0 --port 8002 --reload`
- Add colored output for status messages
- Make script executable with `chmod +x`
- Test script execution

### Task 14: Create E2E Test File
- Create `.claude/commands/e2e/test_web_api.md`
- Define test steps to validate:
  - Server starts successfully on port 8002
  - Health endpoint returns 200 OK
  - API documentation is accessible at /docs
  - Submit request endpoint creates a request and returns request_id
  - Preview endpoint returns formatted GitHub issue
  - Workflows endpoint lists active workflows (may be empty)
  - History endpoint returns request history
  - WebSocket connection can be established
  - WebSocket receives broadcast messages (if workflow running)
- Structure test similar to existing E2E tests
- Include user story and success criteria
- Specify validation steps with HTTP requests and response assertions

### Task 15: Update Project Documentation
- Update `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/README.md`
- Add "Web Backend API" section with:
  - Overview of the web API
  - Installation and setup instructions
  - Starting the server (using start_web.sh)
  - API endpoint documentation (or link to /docs)
  - WebSocket usage examples
  - Environment variable requirements
  - Port configuration (8002)
  - Troubleshooting section
- Add API endpoint reference table with all routes
- Include example curl commands for testing endpoints

### Task 16: Run Validation Commands
Execute all validation commands to ensure zero regressions and complete functionality:
- Run all web API tests
- Run all existing tests to ensure no regressions
- Start the web server and verify it runs without errors
- Access API documentation at http://localhost:8002/docs
- Execute the E2E test
- Verify WebSocket connectivity
- Test server startup script

## Testing Strategy
### Unit Tests
- **Data Models** (`test_models.py`): Test Pydantic model validation, field defaults, serialization
- **Request State Manager** (`test_state.py`): Test request creation, retrieval, confirmation, cleanup, error cases
- **Request Routes** (`test_requests_routes.py`): Test all endpoints with TestClient, mock dependencies (NL processor, GitHub poster)
- **Workflow Routes** (`test_workflows_routes.py`): Test workflow listing and status retrieval, mock file system reads
- **Project Routes** (`test_projects_routes.py`): Test project detection and listing, mock project_detector
- **History Routes** (`test_history_routes.py`): Test history retrieval, pagination, filtering
- **WebSocket** (`test_websocket.py`): Test connection, disconnection, broadcast, message format
- **Workflow Monitor** (`test_workflow_monitor.py`): Test file parsing, workflow status extraction, agent log reading
- **Server** (`test_server.py`): Test app initialization, CORS, router registration, health check, startup/shutdown

All tests should use FastAPI's TestClient, mock external dependencies (file system, GitHub CLI, NL processing), and ensure fast, deterministic execution.

### Edge Cases
- Missing required environment variables (ANTHROPIC_API_KEY, GITHUB_REPO_URL)
- Invalid request_id in preview/confirm endpoints (should return 404)
- Invalid project_path (non-existent directory)
- Malformed ADW state files in agents/ directory
- No active workflows (empty list)
- WebSocket disconnection during broadcast
- Concurrent request submissions
- Very old pending requests (>24 hours)
- agents/ directory doesn't exist
- GitHub CLI not installed or not authenticated
- Network errors during GitHub posting
- CORS preflight requests from frontend
- Large request history (pagination)
- Invalid JSON in state files
- WebSocket connection refused

## Acceptance Criteria
- FastAPI server starts successfully on port 8002 with `./scripts/start_web.sh`
- Health check endpoint returns 200 OK with server status
- Request submission endpoint accepts NL input and returns request_id
- Preview endpoint returns formatted GitHub issue for valid request_id
- Confirm endpoint posts to GitHub and returns issue number and URL
- Workflow endpoints return list of active workflows and detailed status
- Project endpoints allow adding projects and retrieving context
- History endpoint returns past requests with pagination
- WebSocket endpoint accepts connections and broadcasts messages
- CORS is properly configured for frontend (port 5174)
- API documentation is auto-generated and accessible at /docs and /redoc
- All unit tests pass with >80% coverage
- E2E test validates API functionality end-to-end
- No regressions in existing tac-webbuilder functionality
- Server handles errors gracefully with appropriate HTTP status codes
- Logging provides clear debugging information
- Server can be stopped and restarted without issues

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

```bash
# Navigate to tac-webbuilder project
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# Run web API unit tests
uv run pytest tests/interfaces/web/ -v

# Run all tests to ensure no regressions
uv run pytest -v

# Start the web backend server
./scripts/start_web.sh &
sleep 5

# Test health endpoint
curl http://localhost:8002/api/health

# Test API documentation
curl http://localhost:8002/docs
curl http://localhost:8002/redoc

# Stop the server
pkill -f "uvicorn interfaces.web.server:app"

# Read and execute E2E test
# Read .claude/commands/test_e2e.md, then read and execute .claude/commands/e2e/test_web_api.md
```

## Notes

### Design Decisions
1. **FastAPI Framework**: Chosen for automatic OpenAPI documentation, Pydantic integration, WebSocket support, and excellent async performance
2. **Port 8002**: Separate port from main app (8000) to avoid conflicts, allows both systems to run simultaneously
3. **In-Memory State Management**: Pending requests stored in memory for simplicity, can be migrated to Redis/database if persistence needed
4. **WebSocket for Real-time Updates**: Provides instant feedback to users when workflows progress through phases
5. **Router Organization**: Routes organized by domain (requests, workflows, projects, history) for maintainability
6. **CORS Configuration**: Frontend on 5174 to avoid conflicts with main app on 5173
7. **Reuse Core Modules**: Leverages existing NL processing, project detection, and GitHub posting from core modules
8. **File-based Workflow Monitoring**: Reads ADW state from agents/ directory, aligns with existing ADW architecture

### Implementation Notes
- This web API is the backend for the tac-webbuilder web UI (to be built in Issue 5)
- The API provides the same functionality as the CLI but optimized for HTTP/WebSocket protocols
- Request state management allows preview-before-post workflow, giving users control before GitHub posting
- Workflow monitoring requires access to agents/ directory where ADW executions are logged
- History endpoint integrates with CLI history system for unified tracking across interfaces
- Error handling should provide clear, actionable messages with appropriate HTTP status codes
- Security: Validate all user inputs, sanitize file paths, check for path traversal attacks
- Performance: Consider caching for workflow status and project context to reduce file system reads

### Integration Points
- **NL Processing** (Issue #14): Uses core/nl_processor.py for converting NL to GitHub issues
- **CLI Interface** (Issue #16): Shares history tracking system with CLI
- **ADW System**: Reads workflow state from agents/ directory, integrates with ADW execution model
- **GitHub Integration**: Uses core/github_poster.py for posting issues via gh CLI
- **Web Frontend** (Issue #5): This API will be consumed by the web dashboard

### Future Extensibility
This web API foundation enables future enhancements:
- **Authentication/Authorization**: Add user accounts and API keys for multi-user support
- **Database Integration**: Migrate from in-memory state to PostgreSQL/SQLite for persistence
- **Advanced Workflow Control**: Add endpoints to pause, resume, cancel workflows
- **Webhook Integration**: Receive GitHub webhook events for workflow updates
- **Rate Limiting**: Add rate limiting middleware for production deployment
- **Metrics/Analytics**: Track API usage, request patterns, workflow success rates
- **Multi-project Support**: Manage multiple projects simultaneously with project switching
- **Template Management**: API for managing custom issue templates

### Required Environment Variables
- `ANTHROPIC_API_KEY` - For NL processing (required)
- `GITHUB_REPO_URL` - Target repository for issue creation (required)
- `WEB_BACKEND_PORT` - Override default port 8002 (optional)
- `FRONTEND_PORT` - Frontend port for CORS (default 5174, optional)

### Security Considerations
- **Input Validation**: All user inputs must be validated (paths, request IDs, project paths)
- **Path Traversal**: Prevent directory traversal attacks when accessing agent directories
- **CORS**: Restrict to frontend origin only, avoid wildcard in production
- **Rate Limiting**: Consider adding rate limiting to prevent abuse (future enhancement)
- **Authentication**: Consider adding API authentication for production (future enhancement)
- **Secrets**: Never expose API keys or sensitive data in responses or logs

### Key Metrics for Success
- API response time < 500ms for all endpoints (excluding NL processing which may take 2-3s)
- WebSocket latency < 100ms for broadcast messages
- Zero crashes or unhandled exceptions during normal operation
- Clear error messages for all failure modes
- Test coverage >80% for all new API code
- Complete OpenAPI documentation auto-generated by FastAPI
- Server startup time < 5 seconds
