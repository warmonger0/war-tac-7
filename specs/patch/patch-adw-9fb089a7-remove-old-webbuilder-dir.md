# Patch: Remove Old Webbuilder Client Directory

## Metadata
adw_id: `9fb089a7`
review_change_request: `Issue #1: The old directory /app/webbuilder/client/ still exists with all original files intact. The spec explicitly requires in Step 5: 'Verify /app/webbuilder/client/ is completely empty' and 'Remove the empty /app/webbuilder/client/ directory'. The validation commands also include 'test ! -d app/webbuilder/client' to verify the old directory is removed. Resolution: Remove the /app/webbuilder/client/ directory completely using 'rm -rf app/webbuilder/client/' or 'git rm -r app/webbuilder/client/' if tracked by git. Verify removal with 'test ! -d app/webbuilder/client'. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-38-adw-9fb089a7-sdlc_planner-move-frontend-application.md
**Issue:** The old directory `/app/webbuilder/client/` still exists with all original files intact after the frontend was moved to `/projects/tac-webbuilder/app/client/`. The spec explicitly requires this directory to be removed, and validation includes checking that it no longer exists.
**Solution:** Remove the `/app/webbuilder/client/` directory completely since it's untracked by git and contains duplicate files from before the move.

## Files to Modify
Use these files to implement the patch:

- `app/webbuilder/client/` - Remove this entire directory and all contents

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Verify old directory exists and is untracked
- Check that `/app/webbuilder/client/` exists
- Confirm it's untracked by git (not part of git history)
- Verify new directory `/projects/tac-webbuilder/app/client/` has all required files

### Step 2: Remove old webbuilder client directory
- Execute `rm -rf app/webbuilder/client/` to completely remove the old directory
- Verify removal was successful

### Step 3: Remove empty parent directory if needed
- Check if `app/webbuilder/` is now empty
- If empty, remove `app/webbuilder/` directory as well

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. `test ! -d app/webbuilder/client && echo "Old directory removed" || echo "ERROR: Old directory still exists"` - Verify old directory is removed
2. `test -d projects/tac-webbuilder/app/client && echo "New directory exists" || echo "ERROR: New directory missing"` - Verify new directory exists
3. `find projects/tac-webbuilder/app/client -type f | wc -l` - Verify new directory has files (should be 24+)
4. `cd projects/tac-webbuilder/app/client && npm run build` - Verify frontend builds successfully from new location
5. `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Verify backend syntax (zero regressions)
6. `cd app/server && uv run pytest tests/ -v --tb=short` - Verify all backend tests pass (zero regressions)

## Patch Scope
**Lines of code to change:** 0 (directory removal only)
**Risk level:** low
**Testing required:** Verify new location works correctly, verify old location is removed, verify no regressions in backend tests
