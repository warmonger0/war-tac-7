# Patch: Remove Template System Tests

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #3: 11 tests are skipped: All template-related tests in test_mcp_in_templates.py are skipped because the template directories and MCP files don't exist. Tests are: test_react_vite_has_mcp, test_nextjs_has_mcp, test_vanilla_has_mcp, test_templates_have_mcp_gitignore, and 3 test_template_mcp_configs_valid_json variants. Resolution: Once the architectural decision is made (create templates vs. acknowledge tac-webbuilder doesn't need them), either implement the template system with MCP configs or remove/modify these tests to match the actual architecture. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-18-adw-e7613043-sdlc_planner-playwright-mcp-integration.md (deleted)
**Issue:** 11 tests in test_mcp_in_templates.py are skipped because the template system (templates/new_webapp/react-vite, nextjs, vanilla) doesn't exist and was never implemented. These tests were written based on the original Issue #18 spec which described a template scaffolding system, but tac-webbuilder's actual architecture is a natural language interface for ADW workflows, not a project scaffolding tool.
**Solution:** Remove the template-related test file entirely and update documentation to reflect that tac-webbuilder doesn't include a template system. The MCP integration exists at the root level for tac-webbuilder itself, which is correct.

## Files to Modify
Use these files to implement the patch:

- `projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py` - Delete this file entirely
- `projects/tac-webbuilder/README.md` - Remove references to templates/ directory if any exist in the project structure diagram

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Remove template tests file
- Delete `projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py`
- This removes all 11 skipped tests related to non-existent template system

### Step 2: Clean up empty test directory
- Check if `projects/tac-webbuilder/tests/templates/` directory is empty
- If empty, remove the `tests/templates/` directory entirely

### Step 3: Update README project structure
- Read `projects/tac-webbuilder/README.md`
- Review the Project Structure section
- Remove or clarify any references to `templates/` directory that suggest it contains webapp scaffolding templates
- Ensure the structure reflects that `templates/` only contains issue/workflow templates, not webapp project templates

## Validation
Execute every command to validate the patch is complete with zero regressions.

```bash
# Verify template tests file is removed
cd /Users/Warmonger0/tac/tac-7/trees/e7613043/projects/tac-webbuilder
test ! -f tests/templates/test_mcp_in_templates.py && echo "✓ Template tests removed" || echo "✗ File still exists"

# Run all remaining tests to ensure no regressions
cd /Users/Warmonger0/tac/tac-7/trees/e7613043/projects/tac-webbuilder
uv run pytest tests/ -v

# Verify no skipped tests remain (only MCP setup tests should run)
cd /Users/Warmonger0/tac/tac-7/trees/e7613043/projects/tac-webbuilder
uv run pytest tests/ -v | grep -E "(SKIPPED|PASSED|FAILED)"

# Run MCP setup tests specifically to ensure they still pass
cd /Users/Warmonger0/tac/tac-7/trees/e7613043/projects/tac-webbuilder
uv run pytest tests/core/test_mcp_setup.py -v
```

## Patch Scope
**Lines of code to change:** ~205 (delete entire test file) + ~3 (README clarification)
**Risk level:** low
**Testing required:** Verify all remaining tests pass and no skipped tests remain in the test suite
