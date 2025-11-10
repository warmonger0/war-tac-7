# Patch: Fix Frontend Port Environment Variable

## Metadata
adw_id: `9fb089a7`
review_change_request: `Issue #3: The Vite server starts on port 5173 instead of the expected port 5174. The vite.config.ts reads process.env.FRONTEND_PORT but the start_webbuilder_ui.sh script doesn't export this environment variable before running 'npm run dev'. Resolution: Update scripts/start_webbuilder_ui.sh to source .ports.env (if exists) or export FRONTEND_PORT=5174 before running npm run dev. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-38-adw-9fb089a7-sdlc_planner-move-frontend-application.md
**Issue:** The Vite development server starts on the default port 5173 instead of the expected port 5174 because the `start_webbuilder_ui.sh` script doesn't export the `FRONTEND_PORT` environment variable that `vite.config.ts` expects to read from `process.env.FRONTEND_PORT`.
**Solution:** Update `scripts/start_webbuilder_ui.sh` to source the `.ports.env` file (if it exists) or explicitly export `FRONTEND_PORT=5174` before running `npm run dev`, ensuring the Vite server uses the correct port.

## Files to Modify

- `scripts/start_webbuilder_ui.sh` - Add environment variable sourcing/export before npm run dev

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update start_webbuilder_ui.sh to export FRONTEND_PORT
- Source `.ports.env` if it exists at the project root
- Fallback to explicitly exporting `FRONTEND_PORT=5174` if `.ports.env` doesn't exist
- Add the environment setup before the `npm run dev` command
- Ensure the script sources from the project root directory (two levels up from scripts/)

### Step 2: Verify the .ports.env file contents
- Confirm `.ports.env` contains `FRONTEND_PORT` definition
- The file currently defines `FRONTEND_PORT=9204` but the script should handle both sourcing this file and providing a fallback

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. `cat scripts/start_webbuilder_ui.sh` - Verify the script sources .ports.env or exports FRONTEND_PORT
2. `cat .ports.env` - Verify .ports.env contains FRONTEND_PORT definition
3. `./scripts/start_webbuilder_ui.sh &` - Start the frontend in background
4. `sleep 5` - Wait for server to start
5. `curl -s http://localhost:9204 | head -n 5` - Verify frontend serves on the port defined in .ports.env (9204)
6. `pkill -f vite` - Stop the Vite server
7. `cd projects/tac-webbuilder/app/client && npm run build` - Verify frontend builds successfully

## Patch Scope
**Lines of code to change:** 3-5 lines
**Risk level:** low
**Testing required:** Verify frontend starts on correct port (9204 from .ports.env) and can still be accessed via browser
