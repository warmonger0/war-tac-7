# Integration Cleanup

**ADW ID:** 23bd15ec
**Date:** 2025-11-10
**Specification:** specs/issue-49-adw-23bd15ec-sdlc_planner-integration-cleanup.md

## Overview

This feature completes Wave 1 integration by providing a unified full-stack startup experience for the TAC-7 application. It introduces a single command to start both backend and frontend services with automatic health checking, updates documentation to reflect the new architecture, and cleans up deprecated directories.

## What Was Built

- **Full Stack Startup Script** - New `scripts/start_full.sh` that orchestrates both backend and frontend startup with health checking
- **Enhanced Documentation** - Updated README.md Quick Start section with clearer instructions and architecture diagram
- **Configuration Update** - Updated `.mcp.json` with correct worktree path

## Technical Implementation

### Files Modified

- `scripts/start_full.sh`: New unified startup script with process management, health checking, and graceful shutdown
- `README.md`: Updated Quick Start section with full-stack command and architecture overview
- `.mcp.json`: Updated playwright-mcp-config path to reference current worktree (23bd15ec)

### Key Changes

- **Process Management**: Implements proper cleanup handlers with `trap` to ensure both backend and frontend processes terminate cleanly on interrupt
- **Health Checking**: Adds robust health check loop (10 attempts) against backend `/api/health` endpoint before starting frontend
- **User Experience**: Provides clear status messages during startup and displays all relevant URLs (backend, frontend, API docs)
- **Documentation Clarity**: Reorganized Quick Start to highlight the recommended full-stack approach while preserving separate startup options
- **Architecture Visibility**: Added clear directory structure showing `app/client/` (React+Vite) and `app/server/` (FastAPI)

## How to Use

### Starting the Full Stack

1. Run the full stack startup script:
   ```bash
   ./scripts/start_full.sh
   ```

2. Wait for the startup messages confirming both services are ready:
   - Backend: http://localhost:8002
   - Frontend: http://localhost:5174
   - API Docs: http://localhost:8002/docs

3. Open http://localhost:5174 in your browser to access the frontend

4. Press Ctrl+C to stop all services cleanly

### Starting Services Separately

If you prefer to run services in separate terminals:

**Terminal 1 - Backend:**
```bash
./scripts/start_webbuilder.sh
```

**Terminal 2 - Frontend:**
```bash
./scripts/start_client.sh
```

## Configuration

No additional configuration required. The script automatically:
- Detects the project directory
- Uses correct port numbers (8002 for backend, 5174 for frontend)
- Waits for backend health check before starting frontend
- Handles cleanup of both processes on exit

## Testing

To verify the integration:

```bash
# Start full stack
./scripts/start_full.sh &

# Wait for startup
sleep 5

# Test backend
curl -f http://localhost:8002/api/health

# Test frontend
curl -f -I http://localhost:5174

# Stop services
pkill -f "uvicorn|node.*vite"
```

## Notes

- The health check endpoint is `/api/health` (not `/health` as initially specified)
- Backend runs on port 8002 with uvicorn from `app/server`
- Frontend runs on port 5174 with Vite dev server from `app/client`
- The script uses relative paths and works from any directory
- Cleanup handler ensures no orphaned processes on exit
- The deprecated `app/webbuilder/` directory was already removed in a previous commit
