# Patch: Restore Original Frontend from Backup

## Metadata
adw_id: `b5e84e34`
review_change_request: `Issue #2: The spec explicitly requested moving files from /app/webbuilder/client/ to /app/client/ (a file reorganization task), but the implementation completely replaced the app/client directory with a new React+Tailwind frontend application. The original app/client was backed up to app/client.backup, and the /app/webbuilder/client directory was emptied, but the content that was supposed to be moved is not present in the new app/client. Resolution: The implementation should have performed a simple 'mv' operation to relocate existing files, not create a new application. To fix: restore app/client.backup to app/client, then properly move the webbuilder frontend files to the correct location per spec. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-38-adw-b5e84e34-sdlc_planner-move-frontend-app.md
**Issue:** The implementation created a new React+Tailwind application instead of performing a simple file move operation. The original webbuilder frontend files (Vite + React with Tailwind) were backed up to `app/client.backup/` instead of being placed in `app/client/`. The `/app/webbuilder/client/` directory was emptied as expected, but the wrong content ended up in the target location.
**Solution:** Remove the incorrectly created React app from `app/client/`, restore the original webbuilder frontend files from `app/client.backup/` to `app/client/`, and verify the frontend works correctly.

## Files to Modify
Use these files to implement the patch:

- `app/client/` - Remove entire directory (incorrect React app)
- `app/client.backup/` - Source of original webbuilder frontend files
- No other files need modification - all scripts and documentation were already updated correctly

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Remove incorrect React application
- Delete the entire `app/client/` directory that contains the wrong React+Tailwind app
- Verify deletion with `ls app/client/` (should error or show empty)

### Step 2: Restore original webbuilder frontend
- Move `app/client.backup/` to `app/client/` to restore the original webbuilder files
- Use `mv app/client.backup app/client` command
- Verify the restored directory contains the correct files (index.html, package.json with "webbuilder-ui" name, src/ directory, etc.)

### Step 3: Verify frontend structure and dependencies
- Confirm `app/client/package.json` has name "webbuilder-ui" (not "client")
- Confirm `app/client/` contains all expected files: index.html, vite.config.ts, tailwind.config.js, postcss.config.js, tsconfig.json, src/ directory
- Verify node_modules exists and is populated
- Run `npm install` if needed to ensure dependencies are up to date

## Validation
Execute every command to validate the patch is complete with zero regressions.

- `ls -la app/client/` - Verify client directory exists with correct structure
- `ls -la app/client/src/` - Verify src directory with React components
- `find app/client -type f | wc -l` - Count files (should be ~5880 files)
- `test -f app/client/package.json && grep -q "webbuilder-ui" app/client/package.json && echo "Correct package.json"` - Verify correct package.json
- `test -f app/client/index.html && echo "index.html exists"` - Verify index.html
- `test -f app/client/tailwind.config.js && echo "tailwind.config.js exists"` - Verify Tailwind config
- `test -f app/client/postcss.config.js && echo "postcss.config.js exists"` - Verify PostCSS config
- `test ! -d app/client.backup && echo "Backup directory removed"` - Verify backup directory no longer exists
- `cd app/server && uv run pytest` - Run server tests to validate zero regressions

## Patch Scope
**Lines of code to change:** 0 (file system operations only)
**Risk level:** low (simple restore operation, original files preserved in backup)
**Testing required:** Verify directory structure, file count, and server tests pass
