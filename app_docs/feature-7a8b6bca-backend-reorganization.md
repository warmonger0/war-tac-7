# Backend Structure Reorganization

**ADW ID:** 7a8b6bca
**Date:** 2025-11-10
**Specification:** specs/issue-41-adw-7a8b6bca-sdlc_planner-reorganize-backend-structure.md

## Overview

This chore completed the backend reorganization by finalizing the migration from `interfaces/web/` to `app/server/`. The work focused on fixing the entry point (`main.py`), updating the startup script to use the correct entry point, and updating the MCP configuration path to match the new directory structure.

## What Was Built

This reorganization finalized three key components:

- **Proper entry point**: Updated `main.py` to correctly import and expose the FastAPI app
- **Aligned startup script**: Modified `start_webbuilder.sh` to use the proper entry point with reload enabled
- **Updated MCP configuration**: Fixed the path reference in `.mcp.json` to point to the current tree directory

## Technical Implementation

### Files Modified

- `app/server/main.py`: Replaced placeholder logging code with proper FastAPI app import and uvicorn entry point
- `scripts/start_webbuilder.sh`: Changed from `uvicorn server:app` to `uvicorn main:app` with reload flag added
- `.mcp.json`: Updated playwright MCP server config path from previous tree (`b5e84e34`) to current tree (`7a8b6bca`)
- `specs/patch/patch-adw-7a8b6bca-fix-main-import.md`: Added patch specification documenting the import fix

### Key Changes

**Entry Point Transformation (`app/server/main.py`)**:
- Removed 21 lines of placeholder logging code
- Added clean entry point that imports `app` from `server` module
- Configured uvicorn to run with `server:app` (not `main:app` as originally planned, to maintain consistency with the import pattern)
- Added proper `if __name__ == "__main__"` guard with uvicorn configuration

**Startup Script Enhancement (`scripts/start_webbuilder.sh`)**:
- Updated command from `uv run python -m uvicorn server:app` to `uv run uvicorn main:app`
- Added `--reload` flag for development convenience
- Maintained correct working directory (`app/server`) and host/port settings

**MCP Configuration Update (`.mcp.json`)**:
- Updated the playwright MCP server config path to reflect the current tree directory
- Changed from `/Users/Warmonger0/tac/tac-7/trees/b5e84e34/...` to `/Users/Warmonger0/tac/tac-7/trees/7a8b6bca/...`

## How to Use

### Starting the Backend

Use the startup script from the project root:

```bash
./scripts/start_webbuilder.sh
```

This will:
1. Change to the `app/server` directory
2. Start uvicorn with the FastAPI app
3. Enable hot reload for development
4. Serve on `http://0.0.0.0:8002`

### Alternative Direct Start

You can also run uvicorn directly from the `app/server` directory:

```bash
cd app/server
uv run uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

### Importing the App

The FastAPI app can be imported in Python code:

```python
from server import app  # When inside app/server/
# or
from app.server.server import app  # From project root
```

## Configuration

No configuration changes are required. The backend continues to:
- Listen on port 8002
- Use the same FastAPI app structure
- Support hot reload in development mode

## Testing

### Verify Entry Point

```bash
cd app/server
python3 -c "from main import app; print('✅ main.py import successful')"
python3 -c "from server import app; print('✅ server.py import successful')"
```

### Test Server Health

```bash
# Start the server
./scripts/start_webbuilder.sh &

# Wait for startup
sleep 3

# Check health endpoint
curl http://localhost:8002/health

# Stop the server
pkill -f uvicorn
```

### Run Backend Tests

```bash
cd app/server
uv run pytest tests/ -v
```

## Notes

### Migration Context

This work completed the backend reorganization that was ~80% done:
- The `interfaces/web/` directory was already removed in previous commits
- Files had been moved to `app/server/` structure
- Core modules were properly placed in `app/server/core/`
- All imports had been updated to use `from core.*` pattern

This final phase focused on fixing the entry point and startup mechanism to ensure the reorganized backend could actually run.

### Import Pattern Consistency

The entry point uses:
```python
from server import app  # Relative import within app/server/
```

This is consistent with other modules in `app/server/` that use relative imports like `from core.data_models import ...`.

### Startup Script Strategy

The startup script runs `uvicorn main:app` which:
1. Loads `app/server/main.py`
2. Which imports from `server` module (relative import)
3. Which loads the FastAPI app instance

This provides a clean separation where `main.py` is the entry point but `server.py` contains the actual app definition.

### Routes Organization

Per the investigation in the specification, routes were kept inline in `server.py` rather than extracted to a separate `app/server/routes/` directory. With only ~8 endpoints and ~391 lines total, the monolithic structure remains maintainable for this codebase.
