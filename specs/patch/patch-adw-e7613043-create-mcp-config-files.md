# Patch: Create Missing MCP Configuration Files

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #1: MCP configuration files missing: The spec requires .mcp.json.sample and playwright-mcp-config.json in projects/tac-webbuilder/ root, but these files do not exist. Tests test_mcp_config_exists and test_playwright_config_exists are failing. Resolution: Create .mcp.json.sample and playwright-mcp-config.json in projects/tac-webbuilder/ root directory with appropriate relative paths, or update the spec and tests to reflect that tac-webbuilder uses the MCP configuration from tac-7 root (where .mcp.json already exists and is correctly configured). Severity: blocker`

## Issue Summary
**Original Spec:** N/A (Inferred from test requirements)
**Issue:** Tests `test_mcp_config_exists` and `test_playwright_config_exists` are failing because required MCP configuration files (.mcp.json.sample and playwright-mcp-config.json) do not exist in projects/tac-webbuilder/ root directory. The tac-7 root already has these files with absolute paths.
**Solution:** Create .mcp.json.sample and playwright-mcp-config.json in projects/tac-webbuilder/ root with relative paths for portability, allowing tac-webbuilder to be used as a standalone project.

## Files to Modify
Use these files to implement the patch:

- `projects/tac-webbuilder/.mcp.json.sample` (CREATE)
- `projects/tac-webbuilder/playwright-mcp-config.json` (CREATE)

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create .mcp.json.sample in tac-webbuilder root
- Create `projects/tac-webbuilder/.mcp.json.sample` with MCP server configuration
- Use relative path `./playwright-mcp-config.json` for the config file reference
- Include `mcpServers.playwright` with `command`, `args`, and `env` fields as required by test_mcp_config_valid_json
- Set command to "npx" with args for "@playwright/mcp@latest"

### Step 2: Create playwright-mcp-config.json in tac-webbuilder root
- Create `projects/tac-webbuilder/playwright-mcp-config.json` with Playwright browser configuration
- Use relative path `./videos` for video recording directory (not absolute paths like /Users/...)
- Include browser configuration with browserName, launchOptions, and contextOptions
- Set recordVideo dir to "./videos" to satisfy test_playwright_config_uses_relative_paths

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. Verify MCP config files exist: `ls -la projects/tac-webbuilder/.mcp.json.sample projects/tac-webbuilder/playwright-mcp-config.json`
2. Run MCP setup tests: `cd projects/tac-webbuilder && python -m pytest tests/core/test_mcp_setup.py -v`
3. Run all backend tests: `cd app/server && uv run pytest tests/ -v --tb=short`

## Patch Scope
**Lines of code to change:** ~40 lines (2 new configuration files)
**Risk level:** low
**Testing required:** Run projects/tac-webbuilder/tests/core/test_mcp_setup.py to verify all 5 tests pass (test_mcp_config_exists, test_playwright_config_exists, test_mcp_config_valid_json, test_playwright_config_valid, test_playwright_config_uses_relative_paths)
