# Patch: Create Missing MCP Unit Tests

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #5: Unit tests not created: The spec requires creating tests/core/test_mcp_setup.py and tests/templates/test_mcp_in_templates.py with 5+ tests each. These test files do not exist. Resolution: Create the pytest test files as specified in the spec to verify MCP configuration. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-18-adw-e7613043-sdlc_planner-playwright-mcp-integration.md (deleted, restored from git)
**Issue:** The specification requires creating two test files (`tests/core/test_mcp_setup.py` and `tests/templates/test_mcp_in_templates.py`) with 5+ tests each to verify MCP configuration, but these files were not created during implementation.
**Solution:** Create both pytest test files with comprehensive test coverage for MCP configuration validation, including tests for file existence, JSON validity, and template integration.

## Files to Modify
Use these files to implement the patch:

- **projects/tac-webbuilder/tests/core/** (directory to create)
- **projects/tac-webbuilder/tests/core/test_mcp_setup.py** (new file)
- **projects/tac-webbuilder/tests/templates/** (directory to create)
- **projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py** (new file)

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create test directory structure
- Create `projects/tac-webbuilder/tests/core/` directory
- Create `projects/tac-webbuilder/tests/core/__init__.py` empty file
- Create `projects/tac-webbuilder/tests/templates/` directory
- Create `projects/tac-webbuilder/tests/templates/__init__.py` empty file

### Step 2: Create test_mcp_setup.py with 5+ tests
- Create `projects/tac-webbuilder/tests/core/test_mcp_setup.py`
- Implement `test_mcp_config_exists()` to verify `.mcp.json.sample` exists in tac-webbuilder root
- Implement `test_playwright_config_exists()` to verify `playwright-mcp-config.json` exists in tac-webbuilder root
- Implement `test_mcp_config_valid_json()` to parse and validate `.mcp.json.sample` is valid JSON with required structure
- Implement `test_playwright_config_valid()` to parse and validate `playwright-mcp-config.json` is valid JSON with required structure
- Implement `test_playwright_config_uses_relative_paths()` to verify videos directory uses relative path `./videos` not absolute path
- Use pytest framework and pathlib for path operations
- Use json module for validation
- All tests should have descriptive docstrings

### Step 3: Create test_mcp_in_templates.py with 5+ tests
- Create `projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py`
- Implement `test_react_vite_has_mcp()` to verify React-Vite template includes both `.mcp.json.sample` and `playwright-mcp-config.json`
- Implement `test_nextjs_has_mcp()` to verify Next.js template includes both MCP files
- Implement `test_vanilla_has_mcp()` to verify Vanilla template includes both MCP files
- Implement `test_templates_have_mcp_gitignore()` to verify all templates exclude `.mcp.json` and `videos/` in .gitignore
- Implement `test_template_mcp_configs_valid_json()` to parse all template MCP files and verify valid JSON
- Use pytest framework with proper imports
- Use parametrized tests where appropriate for testing multiple templates
- All tests should have descriptive docstrings

### Step 4: Run tests to verify implementation
- Execute `cd projects/tac-webbuilder && pytest tests/core/test_mcp_setup.py -v`
- Execute `cd projects/tac-webbuilder && pytest tests/templates/test_mcp_in_templates.py -v`
- Verify all tests pass or fail gracefully with clear error messages
- If tests fail due to missing MCP files, that's expected and tests are working correctly

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. `ls -la projects/tac-webbuilder/tests/core/test_mcp_setup.py` - Verify test file exists
2. `ls -la projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py` - Verify test file exists
3. `cd projects/tac-webbuilder && python -m py_compile tests/core/test_mcp_setup.py` - Verify Python syntax is valid
4. `cd projects/tac-webbuilder && python -m py_compile tests/templates/test_mcp_in_templates.py` - Verify Python syntax is valid
5. `cd projects/tac-webbuilder && pytest tests/core/test_mcp_setup.py -v --collect-only` - Verify at least 5 tests collected
6. `cd projects/tac-webbuilder && pytest tests/templates/test_mcp_in_templates.py -v --collect-only` - Verify at least 5 tests collected
7. `cd projects/tac-webbuilder && pytest tests/ -v` - Run all tests to ensure no regressions

## Patch Scope
**Lines of code to change:** ~150 lines (75 per test file)
**Risk level:** low
**Testing required:** The patch creates test files, so the validation is self-contained. Tests will verify MCP configuration exists and is valid.
