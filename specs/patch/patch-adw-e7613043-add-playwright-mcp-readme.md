# Patch: Add Playwright MCP Integration Section to README

## Metadata
adw_id: `e7613043`
review_change_request: `Issue #6: README not updated: The spec requires updating projects/tac-webbuilder/README.md with a 'Playwright MCP Integration' section. While the README exists, it contains no mention of Playwright MCP integration. Resolution: Add a section to the README explaining Playwright MCP integration capabilities and referencing the detailed documentation. Severity: blocker`

## Issue Summary
**Original Spec:** N/A (deleted spec file)
**Issue:** The README at projects/tac-webbuilder/README.md lacks a Playwright MCP Integration section, despite comprehensive Playwright MCP documentation existing at docs/playwright-mcp.md
**Solution:** Add a new "Playwright MCP Integration" section to the README that explains capabilities and references the detailed documentation

## Files to Modify
Use these files to implement the patch:

- `projects/tac-webbuilder/README.md` - Add Playwright MCP Integration section

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add Playwright MCP Integration section to README
- Insert new section after "AI Developer Workflows (ADW)" section (after line 167)
- Include overview of Playwright MCP capabilities (browser control, E2E testing, screenshots)
- Reference the detailed documentation at docs/playwright-mcp.md
- Keep content concise and focused on key capabilities
- Use consistent markdown formatting with existing README structure

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. **Verify README contains Playwright MCP section**
   ```bash
   grep -n "Playwright MCP" projects/tac-webbuilder/README.md
   ```

2. **Verify documentation link is correct**
   ```bash
   test -f projects/tac-webbuilder/docs/playwright-mcp.md && echo "Documentation file exists"
   ```

3. **Validate markdown formatting**
   ```bash
   cd projects/tac-webbuilder && npx markdownlint-cli2 README.md || echo "No markdown linter available - manual review required"
   ```

## Patch Scope
**Lines of code to change:** ~15-20 lines
**Risk level:** low
**Testing required:** Manual verification that README section is present and documentation link is valid
