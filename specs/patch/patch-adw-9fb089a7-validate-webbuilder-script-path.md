# Patch: Validate Webbuilder Script Points to Correct Application

## Metadata
adw_id: `9fb089a7`
review_change_request: `Issue #2: The start_webbuilder_ui.sh script now points to /app/client/ which contains the Natural Language SQL Interface application (main.ts), not the webbuilder application. This creates a naming mismatch where a script called 'start_webbuilder_ui' actually starts the SQL interface. Resolution: Either rename the script to reflect what it actually starts, or point it to the correct webbuilder application location once issue #1 is resolved. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-38-adw-9fb089a7-sdlc_planner-move-frontend-application.md
**Issue:** The start_webbuilder_ui.sh script must point to the webbuilder React application (App.tsx with WorkflowDashboard), not the SQL Interface (main.ts). Current staged changes show the script points to `projects/tac-webbuilder/app/client` which contains the correct webbuilder application, resolving the concern.
**Solution:** Verify the staged changes are correct by confirming `projects/tac-webbuilder/app/client` contains the webbuilder React application (App.tsx, WorkflowDashboard, RequestForm components), not the SQL interface. Add validation to ensure the script launches the correct application.

## Files to Modify
Use these files to implement the patch:

- `scripts/start_webbuilder_ui.sh` - Already points to correct location, verify and add validation
- `projects/tac-webbuilder/app/client/src/App.tsx` - Verify this is the webbuilder app (already staged)

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify current script configuration
- Read `scripts/start_webbuilder_ui.sh` to confirm it points to `projects/tac-webbuilder/app/client`
- Confirm the path is correct (not pointing to `app/client` which has the SQL interface)

### Step 2: Validate target directory contains webbuilder React app
- Verify `projects/tac-webbuilder/app/client/src/App.tsx` exists
- Confirm it imports WorkflowDashboard and RequestForm components
- Verify it's NOT the SQL interface (which has main.ts instead of main.tsx)

### Step 3: Confirm SQL interface location is separate
- Verify `app/client/src/main.ts` contains the SQL interface code
- Confirm it's a vanilla TypeScript app (not React)
- Ensure there's no confusion between the two applications

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. `cat scripts/start_webbuilder_ui.sh | grep "cd"` - Verify script points to projects/tac-webbuilder/app/client
2. `test -f projects/tac-webbuilder/app/client/src/App.tsx` - Verify webbuilder React app exists
3. `grep -q "WorkflowDashboard" projects/tac-webbuilder/app/client/src/App.tsx` - Verify it's the webbuilder app
4. `test -f app/client/src/main.ts` - Verify SQL interface is separate
5. `grep -q "processQuery" app/client/src/main.ts` - Verify main.ts is SQL interface
6. `cd projects/tac-webbuilder/app/client && npm run build` - Verify webbuilder builds successfully
7. `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Verify backend syntax (zero regressions)
8. `cd app/server && uv run pytest tests/ -v --tb=short` - Verify all backend tests pass (zero regressions)

## Patch Scope
**Lines of code to change:** 0 (validation only - staged changes already correct)
**Risk level:** low
**Testing required:** Path validation, build verification, backend regression tests
