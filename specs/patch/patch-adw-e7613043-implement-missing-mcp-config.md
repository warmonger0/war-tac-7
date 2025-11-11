# Patch: Implement Missing MCP Configuration Files

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #7: Git history shows only spec addition: The git commit log shows 'sdlc_planner: feature: add playwright MCP spec' as the most recent commit. This indicates only the spec file was added, with no implementation work completed. Resolution: Implement all the tasks described in the spec file, or clarify that this is a planning-only commit and implementation will follow. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-18-adw-e7613043-sdlc_planner-playwright-mcp-integration.md (deleted)
**Issue:** The Playwright MCP integration spec was added but critical implementation files are missing. While documentation (docs/playwright-mcp.md), tests (tests/core/test_mcp_setup.py, tests/templates/test_mcp_in_templates.py), and README updates were completed, the core MCP configuration files (.mcp.json.sample and playwright-mcp-config.json) were never created in the tac-webbuilder root directory. The tests reference these files but they don't exist, causing test failures.
**Solution:** Copy and adapt MCP configuration files from tac-7 root to tac-webbuilder root, update .gitignore, and verify all tests pass. This completes the blocked implementation tasks from the original spec.

## Files to Modify

**Files to create:**
- `projects/tac-webbuilder/.mcp.json.sample` - MCP server configuration
- `projects/tac-webbuilder/playwright-mcp-config.json` - Playwright browser configuration

**Files to modify:**
- `projects/tac-webbuilder/.gitignore` - Add MCP exclusions

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Copy MCP configuration from tac-7 root to tac-webbuilder
- Read `.mcp.json.sample` from tac-7 root to understand structure
- Read `playwright-mcp-config.json` from tac-7 root to understand Playwright settings
- Create `projects/tac-webbuilder/.mcp.json.sample` with the same MCP server configuration (relative path to playwright config)
- Create `projects/tac-webbuilder/playwright-mcp-config.json` with relative video directory path (`./videos`)
- Verify both files contain valid JSON syntax

### Step 2: Update tac-webbuilder .gitignore
- Read `projects/tac-webbuilder/.gitignore` current contents
- Add section comment `# MCP` if not already present
- Add `.mcp.json` exclusion (exclude active config, keep .sample tracked)
- Add `videos/` exclusion (exclude video recordings)
- Ensure no duplicate entries exist

### Step 3: Validate implementation with existing tests
- Run `cd projects/tac-webbuilder && uv run pytest tests/core/test_mcp_setup.py -v` to verify MCP config files exist and are valid
- Run `cd projects/tac-webbuilder && uv run pytest tests/templates/test_mcp_in_templates.py -v` to verify template integration (expected to fail since templates don't have MCP files yet, but should not fail on root config validation)
- Verify all config file existence and JSON validation tests pass

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. **Verify MCP config files exist:**
   ```bash
   ls -la projects/tac-webbuilder/.mcp.json.sample projects/tac-webbuilder/playwright-mcp-config.json
   ```

2. **Verify JSON validity:**
   ```bash
   cd projects/tac-webbuilder && cat .mcp.json.sample | python -m json.tool > /dev/null && echo "Valid JSON"
   cd projects/tac-webbuilder && cat playwright-mcp-config.json | python -m json.tool > /dev/null && echo "Valid JSON"
   ```

3. **Run MCP setup tests:**
   ```bash
   cd projects/tac-webbuilder && uv run pytest tests/core/test_mcp_setup.py -v
   ```

4. **Verify gitignore updated:**
   ```bash
   cd projects/tac-webbuilder && grep -E "^\.mcp\.json$|^videos/$" .gitignore
   ```

## Patch Scope
**Lines of code to change:** ~50 lines (2 new config files + gitignore updates)
**Risk level:** low
**Testing required:** Pytest tests already exist and validate the configuration files. All test_mcp_setup.py tests must pass.
