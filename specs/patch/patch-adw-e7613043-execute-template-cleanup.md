# Patch: Execute Template System Cleanup

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #2: Template system doesn't exist: The spec requires embedding MCP configs in templates/new_webapp/{react-vite,nextjs,vanilla} directories, but templates/new_webapp/ doesn't exist. tac-webbuilder/templates/ only contains issue_template.md. This indicates the spec was written for a different type of project. Resolution: The architectural mismatch is acknowledged in patch spec patch-adw-e7613043-remove-template-references.md. Either create the template system, or update the implementation to reflect tac-webbuilder's actual architecture as an ADW workflow tool rather than a web app scaffolding system. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-18-adw-e7613043-sdlc_planner-playwright-mcp-integration.md (deleted)
**Issue:** The original spec assumed tac-webbuilder has a web application template system (templates/new_webapp/react-vite, nextjs, vanilla) when it's actually a natural language interface tool for ADW workflows, not a web app scaffolding system. MCP configuration files were incorrectly created in projects/tac-webbuilder/ when they should only exist in tac-7 root.
**Solution:** Execute the cleanup plan from patch-adw-e7613043-remove-template-references.md: unstage and delete MCP files from projects/tac-webbuilder/, verify they exist correctly in tac-7 root, and ensure tac-webbuilder architecture is properly reflected.

## Files to Modify
Use these files to implement the patch:

- `projects/tac-webbuilder/.mcp.json.sample` (unstage and delete)
- `projects/tac-webbuilder/playwright-mcp-config.json` (unstage and delete)

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Unstage and remove MCP files from tac-webbuilder
- Run `git reset HEAD projects/tac-webbuilder/.mcp.json.sample` to unstage
- Run `git reset HEAD projects/tac-webbuilder/playwright-mcp-config.json` to unstage
- Delete `projects/tac-webbuilder/.mcp.json.sample`
- Delete `projects/tac-webbuilder/playwright-mcp-config.json`

### Step 2: Verify MCP files exist correctly in tac-7 root
- Confirm `.mcp.json.sample` exists in tac-7 root (not in projects/tac-webbuilder)
- Confirm `playwright-mcp-config.json` exists in tac-7 root (not in projects/tac-webbuilder)
- These files are correctly placed for tac-7 and should remain there

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. **Verify MCP files removed from tac-webbuilder:**
   ```bash
   test ! -f projects/tac-webbuilder/.mcp.json.sample && test ! -f projects/tac-webbuilder/playwright-mcp-config.json && echo "PASS: MCP files correctly removed from tac-webbuilder" || echo "FAIL: MCP files still exist in tac-webbuilder"
   ```

2. **Verify MCP files exist in tac-7 root:**
   ```bash
   test -f .mcp.json.sample && test -f playwright-mcp-config.json && echo "PASS: MCP files correctly placed in tac-7 root" || echo "FAIL: MCP files missing from tac-7 root"
   ```

3. **Verify git status shows no staged MCP files:**
   ```bash
   git status --short | grep -E "^(A|M).*\.mcp|playwright-mcp-config" && echo "FAIL: MCP files still staged" || echo "PASS: No MCP files staged"
   ```

4. **Verify templates structure matches reality:**
   ```bash
   test -d projects/tac-webbuilder/templates/new_webapp && echo "FAIL: new_webapp directory should not exist" || echo "PASS: templates/ only contains issue_template.md"
   ```

5. **Run backend tests:**
   ```bash
   cd app/server && uv run pytest tests/ -v --tb=short
   ```

## Patch Scope
**Lines of code to change:** 0 (only removing incorrectly placed files and unstaging changes)
**Risk level:** low (removing files that were created based on incorrect spec assumptions)
**Testing required:** Verify MCP files remain in tac-7 root and are removed from tac-webbuilder; confirm tac-webbuilder architecture is understood correctly (it's a CLI/web interface for ADW, not a web app scaffolding tool with templates)
