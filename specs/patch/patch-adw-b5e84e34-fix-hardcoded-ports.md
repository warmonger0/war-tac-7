# Patch: Fix Hardcoded Ports in Vite Configuration

## Metadata
adw_id: `b5e84e34`
review_change_request: `Issue #1: vite.config.ts has hardcoded port 5174 for frontend and proxy target http://localhost:8002 for backend. The .ports.env specifies FRONTEND_PORT=9213 and BACKEND_PORT=9113 (via VITE_BACKEND_URL=http://localhost:9113), but these environment variables are not being used in the vite configuration. Resolution: Update vite.config.ts to use environment variables: port should use process.env.FRONTEND_PORT || 9213, and proxy target should use process.env.VITE_BACKEND_URL || 'http://localhost:9113'. Alternatively, update vite.config.ts to dynamically read from .ports.env file. Severity: blocker`

## Issue Summary
**Original Spec:** Not provided
**Issue:** The vite.config.ts file has hardcoded port 5174 for the frontend server and hardcoded proxy target http://localhost:8002 for the backend, but .ports.env specifies FRONTEND_PORT=9213 and BACKEND_PORT=9113. The configuration does not read from environment variables.
**Solution:** Update vite.config.ts to read from .ports.env file and use those values for the server port and proxy targets with appropriate fallback values.

## Files to Modify
Use these files to implement the patch:

- `app/client/vite.config.ts` - Update to use environment variables from .ports.env for port and proxy configuration

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Install dotenv package for loading .ports.env
- Add dotenv as a dev dependency: `cd app/client && bun add -d dotenv`
- This allows reading environment variables from .ports.env file

### Step 2: Update vite.config.ts to load and use environment variables
- Import dotenv and load variables from ../../.ports.env (relative to app/client)
- Replace hardcoded port 5174 with `parseInt(process.env.FRONTEND_PORT || '9213')`
- Replace hardcoded proxy target 'http://localhost:8002' with `process.env.VITE_BACKEND_URL || 'http://localhost:9113'`
- Replace hardcoded WebSocket target 'ws://localhost:8002' with the backend URL converted to ws:// protocol
- Ensure proper type handling (port must be a number, URLs must be strings)

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. **TypeScript Type Check**: `cd app/client && bun tsc --noEmit`
   - Ensures no type errors introduced by the configuration changes

2. **Frontend Build**: `cd app/client && bun run build`
   - Verifies that the build process completes successfully with the new configuration

3. **Manual Port Verification**: Start the dev server with `cd app/client && bun run dev` and verify it starts on port 9213

4. **Python Syntax Check**: `cd app/server && uv run python -m py_compile server.py main.py core/*.py`
   - Ensures no regressions in backend code

5. **All Backend Tests**: `cd app/server && uv run pytest tests/ -v --tb=short`
   - Ensures no regressions in backend functionality

## Patch Scope
**Lines of code to change:** ~8 lines (3 lines added for dotenv import/config, 3 lines modified for port/proxy values)
**Risk level:** low
**Testing required:** TypeScript compilation, frontend build, dev server startup on correct port, full backend test suite
