# Patch: Restore Webbuilder React Application

## Metadata
adw_id: `9fb089a7`
review_change_request: `Issue #1: The webbuilder React application (with App.tsx, WorkflowDashboard, RequestForm components) was deleted from /app/webbuilder/client/ but was not moved to /projects/tac-webbuilder/app/client/ as specified in the original issue. The application no longer exists in the codebase. Resolution: Restore the webbuilder React application files from git history and move them to the correct location at /projects/tac-webbuilder/app/client/, then update the startup script to point to that location. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-38-adw-9fb089a7-sdlc_planner-move-frontend-application.md
**Issue:** The webbuilder React application was deleted in commit 8fcaeca instead of being moved. The application files (App.tsx, WorkflowDashboard, RequestForm, and 21 other files) need to be restored from commit e1b9359 and placed in the correct location at /projects/tac-webbuilder/app/client/.
**Solution:** Use git to restore all 24 frontend files from commit e1b9359, create the target directory structure, move files to /projects/tac-webbuilder/app/client/, and update startup scripts to reference the new location.

## Files to Modify
Use these files to implement the patch:

- `projects/tac-webbuilder/app/client/` - Create directory and restore all 24 frontend files
- `scripts/start_webbuilder_ui.sh` - Update to point to /projects/tac-webbuilder/app/client/

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create target directory structure
- Create the directory `/projects/tac-webbuilder/app/client/`
- Verify the directory is created successfully

### Step 2: Restore webbuilder React application from git history
- Checkout all 24 files from commit e1b9359 where they existed at path `app/webbuilder/client/`
- Files to restore:
  - index.html, package.json, package-lock.json, postcss.config.js
  - tailwind.config.js, tsconfig.json, tsconfig.node.json, vite.config.ts
  - src/App.tsx, src/main.tsx, src/style.css, src/types.ts
  - src/api/client.ts
  - src/components/ConfirmDialog.tsx, HistoryView.tsx, IssuePreview.tsx
  - src/components/ProgressBar.tsx, RequestForm.tsx, RoutesView.tsx
  - src/components/StatusBadge.tsx, TabBar.tsx, WorkflowCard.tsx, WorkflowDashboard.tsx
  - src/hooks/useWebSocket.ts
- Move restored files to `/projects/tac-webbuilder/app/client/`

### Step 3: Update startup script
- Edit `scripts/start_webbuilder_ui.sh` to change path from `../app/client` to `../projects/tac-webbuilder/app/client`
- Update echo message to reflect correct location

### Step 4: Install dependencies
- Navigate to `/projects/tac-webbuilder/app/client/`
- Run `npm install` to install all frontend dependencies

### Step 5: Verify file count and structure
- Count files in `/projects/tac-webbuilder/app/client/` (should be 24+ files)
- Verify all React components exist in src/components/
- Verify src/App.tsx exists and contains WorkflowDashboard reference

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. `ls -la projects/tac-webbuilder/app/client/` - Verify directory exists with files
2. `find projects/tac-webbuilder/app/client -type f | wc -l` - Verify file count (should be 24+)
3. `test -f projects/tac-webbuilder/app/client/src/App.tsx` - Verify App.tsx exists
4. `test -f projects/tac-webbuilder/app/client/src/components/WorkflowDashboard.tsx` - Verify WorkflowDashboard exists
5. `test -f projects/tac-webbuilder/app/client/src/components/RequestForm.tsx` - Verify RequestForm exists
6. `grep -q "projects/tac-webbuilder/app/client" scripts/start_webbuilder_ui.sh` - Verify startup script updated
7. `cd projects/tac-webbuilder/app/client && npm run build` - Verify frontend builds successfully
8. `cd app/server && uv run python -m py_compile server.py main.py core/*.py` - Verify backend syntax (zero regressions)
9. `cd app/server && uv run pytest tests/ -v --tb=short` - Verify all backend tests pass (zero regressions)

## Patch Scope
**Lines of code to change:** ~2500 (24 files restored, 1 script updated)
**Risk level:** medium
**Testing required:** Frontend build validation, backend regression tests, startup script verification
