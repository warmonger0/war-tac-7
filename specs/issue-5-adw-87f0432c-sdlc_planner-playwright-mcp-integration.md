# Feature: Playwright MCP Integration

## Metadata
issue_number: `5`
adw_id: `87f0432c`
issue_json: `{"number":5,"title":"7-playwright-mcp","body":"# 🎯 ISSUE 7: tac-webbuilder - Playwright MCP Integration\n\n## Overview\nIntegrate the Playwright Model Context Protocol (MCP) server into tac-webbuilder to enable browser automation and E2E testing capabilities for all generated web applications.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory unless otherwise specified (e.g., copying from tac-7).\n\n## Dependencies\n**Requires**: Issue 1 (Project Foundation) to be completed\n\n## Tasks\n\n### 1. Copy MCP Configuration Files\nCopy MCP configuration from `/Users/Warmonger0/tac/tac-7`:\n\n**Files to copy**:\n- `.mcp.json.sample` → `tac-webbuilder/.mcp.json.sample`\n- `playwright-mcp-config.json` → `tac-webbuilder/playwright-mcp-config.json`\n\n**File**: `tac-webbuilder/.mcp.json.sample`\n```json\n{\n  \"mcpServers\": {\n    \"playwright\": {\n      \"command\": \"npx\",\n      \"args\": [\n        \"@playwright/mcp@latest\",\n        \"--isolated\",\n        \"--config\",\n        \"./playwright-mcp-config.json\"\n      ]\n    }\n  }\n}\n```\n\n**File**: `tac-webbuilder/playwright-mcp-config.json`\n```json\n{\n  \"browser\": {\n    \"browserName\": \"chromium\",\n    \"launchOptions\": {\n      \"headless\": true\n    },\n    \"contextOptions\": {\n      \"recordVideo\": {\n        \"dir\": \"./videos\",\n        \"size\": {\n          \"width\": 1920,\n          \"height\": 1080\n        }\n      },\n      \"viewport\": {\n        \"width\": 1920,\n        \"height\": 1080\n      }\n    }\n  }\n}\n```\n\n### 2. Update Template Projects with MCP\n**For each template** (`react-vite`, `nextjs`, `vanilla`):\n\nAdd to template structure:\n- `.mcp.json.sample` - MCP server configuration\n- `playwright-mcp-config.json` - Playwright-specific settings\n- `videos/` directory in `.gitignore`\n\n**File**: `templates/new_webapp/{template}/.gitignore` (add):\n```\n# MCP\n.mcp.json\nvideos/\n```\n\n### 3. Add MCP Setup to Integration Script\n**File**: `scripts/integrate_existing.sh` (update)\n\nAdd MCP setup step:\n```bash\n# Copy MCP configuration\necho \"📦 Setting up Playwright MCP...\"\ncp .mcp.json.sample .mcp.json\ncp playwright-mcp-config.json \"$PROJECT_PATH/\"\n\n# Add to .gitignore\nif ! grep -q \"\\.mcp\\.json\" \"$PROJECT_PATH/.gitignore\"; then\n    echo \".mcp.json\" >> \"$PROJECT_PATH/.gitignore\"\n    echo \"videos/\" >> \"$PROJECT_PATH/.gitignore\"\nfi\n```\n\n### 4. Update New Project Scaffolding\n**File**: `scripts/setup_new_project.sh` (update)\n\nAdd MCP configuration step after template copy:\n```bash\n# Set up MCP\necho \"🎭 Configuring Playwright MCP...\"\ncp .mcp.json.sample \"$PROJECT_PATH/.mcp.json\"\ncp playwright-mcp-config.json \"$PROJECT_PATH/\"\n```\n\n### 5. Add MCP to ADW Commands\nUpdate slash commands to leverage Playwright MCP:\n\n**File**: `.claude/commands/test_e2e.md` (copy from tac-7)\n```markdown\nRun E2E tests using Playwright MCP.\n\nSteps:\n1. Use Playwright MCP to navigate to the application\n2. Test critical user flows\n3. Capture screenshots and videos for failures\n4. Generate test report\n```\n\n**File**: `.claude/commands/review.md` (copy from tac-7)\n```markdown\nVisual review of the application using Playwright MCP.\n\nSteps:\n1. Launch application in Playwright browser\n2. Navigate through key pages\n3. Take screenshots at various viewport sizes\n4. Check for visual regressions\n5. Upload screenshots to comments\n```\n\n### 6. Documentation for MCP Usage\n**File**: `docs/playwright-mcp.md`\n\n```markdown\n# Playwright MCP Integration\n\n## What is Playwright MCP?\n\nThe Playwright Model Context Protocol (MCP) server enables Claude Code to:\n- Control browsers programmatically\n- Run E2E tests automatically\n- Capture screenshots and videos\n- Validate visual appearance\n- Test user interactions\n\n## Setup\n\n### 1. Configure MCP\n```bash\n# Copy sample configuration\ncp .mcp.json.sample .mcp.json\n```\n\n### 2. Install Playwright\n```bash\nnpm install -D playwright\nnpx playwright install chromium\n```\n\n### 3. Verify Setup\nThe Playwright MCP server will automatically start when Claude Code runs.\n\n## Usage\n\n### In ADW Workflows\n\nADW workflows automatically use Playwright MCP for:\n- **Testing Phase**: E2E test execution\n- **Review Phase**: Visual validation with screenshots\n- **Documentation Phase**: Capturing UI examples\n\n### Manual Testing\n\nUse `/test_e2e` command to run tests on demand.\n\n### Visual Review\n\nUse `/review` command to capture screenshots for review.\n\n## Configuration\n\n### Browser Settings\nEdit `playwright-mcp-config.json`:\n\n```json\n{\n  \"browser\": {\n    \"browserName\": \"chromium\",  // or \"firefox\", \"webkit\"\n    \"launchOptions\": {\n      \"headless\": true,  // Set to false for debugging\n      \"slowMo\": 0        // Milliseconds to slow down operations\n    }\n  }\n}\n```\n\n### Video Recording\nVideos are saved to `./videos/` directory when tests run.\n\nTo disable video recording:\n```json\n{\n  \"contextOptions\": {\n    \"recordVideo\": null\n  }\n}\n```\n\n### Viewport Size\nDefault: 1920x1080\n\nTo change:\n```json\n{\n  \"contextOptions\": {\n    \"viewport\": {\n      \"width\": 1280,\n      \"height\": 720\n    }\n  }\n}\n```\n\n## Troubleshooting\n\n### MCP Server Won't Start\n- Ensure Node.js is installed\n- Run `npx @playwright/mcp@latest --version` to verify\n- Check `.mcp.json` syntax is valid\n\n### Browser Launch Fails\n- Run `npx playwright install chromium`\n- Check system dependencies: `npx playwright install-deps`\n\n### Videos Not Recording\n- Ensure `videos/` directory exists\n- Check `recordVideo` config in `playwright-mcp-config.json`\n- Verify disk space available\n\n## Best Practices\n\n### 1. Headless Mode\nKeep `headless: true` for CI/CD and automated workflows.\nUse `headless: false` only for local debugging.\n\n### 2. Video Storage\nVideos can be large. Add to `.gitignore`:\n```\nvideos/\n```\n\n### 3. Screenshot Organization\nStore screenshots in `logs/screenshots/` for easy access.\n\n### 4. Test Stability\nUse proper waits and selectors to avoid flaky tests:\n```typescript\n// Good: Wait for element\nawait page.waitForSelector('[data-testid=\"submit-button\"]');\n\n// Bad: Hard-coded timeout\nawait page.waitForTimeout(5000);\n```\n\n## Examples\n\nSee `docs/examples.md` for example test requests that leverage Playwright MCP.\n```\n\n### 7. Update Foundation Issue\n**File**: `issue-1-foundation.md` (update)\n\nAdd to \"Copy ADW System from tac-7\" section:\n```markdown\n- `.mcp.json.sample` → `.mcp.json.sample`\n- `playwright-mcp-config.json` → `playwright-mcp-config.json`\n```\n\nAdd to .gitignore:\n```markdown\n.mcp.json\nvideos/\n```\n\n### 8. Update Templates Issue\n**File**: `issue-6-templates-docs.md` (update)\n\nAdd to each template structure:\n```markdown\n├── .mcp.json.sample\n├── playwright-mcp-config.json\n```\n\nAdd to \"Framework-Specific Notes\":\n```markdown\n### Playwright MCP Setup\nAll templates include:\n- `.mcp.json.sample` for MCP server configuration\n- `playwright-mcp-config.json` for browser settings\n- E2E test commands in `.claude/commands/`\n```\n\n## Testing\n\n### Test MCP Installation\n**File**: `tests/core/test_mcp_setup.py`\n\n```python\ndef test_mcp_config_exists():\n    \"\"\"Verify .mcp.json.sample exists.\"\"\"\n\ndef test_playwright_config_exists():\n    \"\"\"Verify playwright-mcp-config.json exists.\"\"\"\n\ndef test_mcp_config_valid_json():\n    \"\"\"Verify .mcp.json.sample is valid JSON.\"\"\"\n\ndef test_playwright_config_valid():\n    \"\"\"Verify playwright-mcp-config.json is valid.\"\"\"\n```\n\n### Test Template Integration\n**File**: `tests/templates/test_mcp_in_templates.py`\n\n```python\ndef test_react_vite_has_mcp():\n    \"\"\"Verify React-Vite template includes MCP config.\"\"\"\n\ndef test_nextjs_has_mcp():\n    \"\"\"Verify Next.js template includes MCP config.\"\"\"\n\ndef test_new_project_includes_mcp():\n    \"\"\"Verify scaffolding includes MCP setup.\"\"\"\n```\n\n## Success Criteria\n- ✅ `.mcp.json.sample` and `playwright-mcp-config.json` copied to tac-webbuilder\n- ✅ All templates include MCP configuration\n- ✅ Integration script sets up MCP for existing projects\n- ✅ New project scaffolding includes MCP\n- ✅ E2E and review commands copied from tac-7\n- ✅ Documentation explains MCP usage\n- ✅ `.gitignore` excludes `.mcp.json` and `videos/`\n- ✅ All tests pass\n\n## Benefits\n\n### For New Projects\n- E2E testing ready out-of-the-box\n- Visual review capabilities from day one\n- No manual Playwright setup needed\n\n### For Existing Projects\n- Easy integration via `webbuilder integrate`\n- Consistent testing across all projects\n- Automated visual validation\n\n### For ADW Workflows\n- Automated E2E test execution\n- Screenshot-based code review\n- Video recordings of test failures\n- Higher quality deliverables\n\n## Next Issue\nThis can run in parallel with other issues. No blocking dependencies.\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`infrastructure`, `testing`, `playwright`, `mcp`, `webbuilder`\n"}`

## Feature Description
This feature integrates the Playwright Model Context Protocol (MCP) server into the Natural Language SQL Interface application to enable automated browser testing and end-to-end (E2E) validation. The integration provides programmatic browser control for testing user flows, capturing screenshots, recording videos, and validating application behavior without manual intervention.

The Playwright MCP server acts as a bridge between Claude Code (AI assistant) and browser automation tools, allowing the application to run comprehensive E2E tests automatically. This ensures that natural language queries, data uploads, result displays, and all user interactions work correctly across the entire application stack.

## User Story
As a developer
I want automated E2E testing using Playwright MCP
So that I can validate user workflows, catch regressions early, and ensure the application functions correctly without manual browser testing

## Problem Statement
The current application lacks automated end-to-end testing capabilities. Manual testing is time-consuming, error-prone, and inconsistent. Without automated E2E tests:
- Regressions go undetected until users report issues
- Complex user workflows (query input, file upload, result display) require manual validation
- Visual regressions and UI issues are not systematically caught
- Integration between frontend and backend cannot be verified automatically
- Quality assurance relies entirely on manual testing, slowing development velocity

## Solution Statement
Integrate the Playwright Model Context Protocol (MCP) server to enable programmatic browser automation. The solution includes:
1. MCP configuration files (`.mcp.json` and `playwright-mcp-config.json`) for Playwright setup
2. Browser automation capabilities through Claude Code commands
3. E2E test infrastructure with screenshot capture and video recording
4. Automated test execution integrated into development workflows
5. Comprehensive documentation for using Playwright MCP

This provides developers with automated testing tools that validate user workflows, capture visual evidence of functionality, and ensure code quality through systematic E2E validation.

## Relevant Files
Use these files to implement the feature:

- `.mcp.json` (existing) - Current MCP server configuration that needs to be converted to a sample template
  - Already exists at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/.mcp.json`
  - Contains Playwright MCP server configuration with proper command and arguments
  - Will be used as the source for creating `.mcp.json.sample`

- `playwright-mcp-config.json` (existing) - Current Playwright configuration with browser settings
  - Already exists at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/playwright-mcp-config.json`
  - Contains browser type (chromium), headless mode settings, video recording configuration
  - Needs path adjustments to use relative paths instead of absolute paths

- `.gitignore` (existing) - Git ignore file that needs MCP-related exclusions
  - Located at root of repository
  - Needs to exclude `.mcp.json` (user-specific config) and `videos/` (generated recordings)

- `.claude/commands/test_e2e.md` (existing) - E2E test runner command
  - Already exists at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/.claude/commands/test_e2e.md`
  - Provides instructions for executing E2E tests using Playwright MCP
  - Defines test execution workflow, screenshot capture, and result reporting

- `.claude/commands/e2e/test_basic_query.md` (existing) - Example E2E test for basic query functionality
  - Already exists at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/.claude/commands/e2e/test_basic_query.md`
  - Demonstrates test structure with user story, test steps, and success criteria
  - Will serve as template for creating new E2E test in this feature

- `README.md` (existing) - Project documentation that needs MCP documentation section
  - Located at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/README.md`
  - Contains project overview, setup instructions, and development workflows
  - Needs new section explaining Playwright MCP integration and usage

### New Files

- `.mcp.json.sample` - Sample MCP configuration template for users to copy
  - Will be created at root of repository
  - Contains Playwright MCP server configuration with relative paths
  - Users copy this to `.mcp.json` and customize as needed

- `.claude/commands/e2e/test_playwright_mcp_integration.md` - E2E test validating MCP integration
  - Will be created to validate Playwright MCP functionality
  - Tests browser automation, screenshot capture, and basic navigation
  - Ensures MCP server is properly configured and operational

## Implementation Plan

### Phase 1: Foundation
Create the MCP configuration infrastructure by converting existing configuration files into sample templates. This includes:
- Converting `.mcp.json` to `.mcp.json.sample` with relative paths
- Updating `playwright-mcp-config.json` to use relative paths for video recording
- Updating `.gitignore` to exclude user-specific MCP files and generated videos
- Creating E2E test directory structure for organizing tests

### Phase 2: Core Implementation
Implement the E2E testing infrastructure and documentation:
- Create E2E test file that validates Playwright MCP integration
- Update README.md with comprehensive MCP documentation section
- Document MCP setup, configuration, and usage patterns
- Provide troubleshooting guidance for common MCP issues

### Phase 3: Integration
Ensure MCP integration works seamlessly with existing workflows:
- Validate existing `.claude/commands/test_e2e.md` works with new configuration
- Test E2E workflow end-to-end with sample application
- Verify screenshot capture and video recording function correctly
- Document validation process and acceptance criteria

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Create MCP Configuration Sample Template
- Read existing `.mcp.json` file at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/.mcp.json`
- Create `.mcp.json.sample` in repository root with same configuration
- Update config path from absolute to relative: `./playwright-mcp-config.json`
- Add comments explaining the purpose of each configuration option

### 2. Update Playwright Configuration
- Read existing `playwright-mcp-config.json` at `/Users/Warmonger0/tac/tac-7/trees/87f0432c/playwright-mcp-config.json`
- Update video recording directory from absolute path to relative: `./videos`
- Ensure viewport and browser settings are appropriate for testing
- Validate JSON syntax is correct

### 3. Update .gitignore
- Read current `.gitignore` file
- Add `.mcp.json` to exclude user-specific MCP configuration
- Add `videos/` to exclude generated video recordings from git
- Add comment explaining why these files are excluded

### 4. Create E2E Test for MCP Integration
- Read `.claude/commands/test_e2e.md` to understand test runner expectations
- Read `.claude/commands/e2e/test_basic_query.md` for test structure reference
- Create `.claude/commands/e2e/test_playwright_mcp_integration.md` with:
  - User story validating Playwright MCP browser automation
  - Test steps: Navigate to app, verify page loads, take screenshot, verify elements exist
  - Success criteria: Browser launches, navigation works, screenshots captured, MCP responds
- Test should validate core MCP functionality without testing application-specific features

### 5. Update README.md with MCP Documentation
- Read current `README.md` file
- Add new section "Playwright MCP Integration" after "Development" section
- Document what Playwright MCP is and why it's valuable
- Explain setup steps: copying `.mcp.json.sample` to `.mcp.json`
- Document how to run E2E tests using `/test_e2e` command
- Add troubleshooting section for common MCP issues:
  - MCP server won't start
  - Browser launch fails
  - Videos not recording
  - Screenshot path issues
- Include configuration examples for customizing browser settings
- Link to `.claude/commands/e2e/` directory for example tests

### 6. Run Validation Commands
- Execute all validation commands listed in "Validation Commands" section
- Ensure server tests pass with zero regressions
- Ensure client type checking passes with zero errors
- Ensure client build completes successfully
- Read and execute new E2E test to validate MCP integration works

## Testing Strategy

### Unit Tests
No unit tests required for this feature as it only adds configuration files and documentation. The feature is validated through:
- E2E test execution validating MCP server functionality
- Manual verification of configuration file formats
- Build process validation ensuring no breaking changes

### Edge Cases
- **MCP server fails to start**: E2E test should fail gracefully and report error
- **Browser installation missing**: Test should detect missing Playwright browser and report clear error
- **Invalid configuration paths**: Relative paths should work from repository root
- **Video recording fails**: Test should still complete even if video recording fails
- **Screenshot directory doesn't exist**: Test should create directory or report clear error

## Acceptance Criteria
- `.mcp.json.sample` exists in repository root with valid Playwright MCP configuration
- `playwright-mcp-config.json` uses relative paths for video recording (`./videos`)
- `.gitignore` excludes `.mcp.json` and `videos/` directory
- `.claude/commands/e2e/test_playwright_mcp_integration.md` E2E test file exists and validates MCP functionality
- README.md includes comprehensive "Playwright MCP Integration" section with:
  - Setup instructions for copying `.mcp.json.sample`
  - Usage documentation for running E2E tests
  - Configuration examples for customizing browser settings
  - Troubleshooting guide for common issues
- All existing tests pass without regression
- Client build completes successfully
- New E2E test executes and validates MCP integration works correctly

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Read `.claude/commands/test_e2e.md` to understand how to execute E2E tests, then read and execute `.claude/commands/e2e/test_playwright_mcp_integration.md` to validate Playwright MCP integration works correctly. This will test browser automation, screenshot capture, and navigation.

- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- `cat .mcp.json.sample` - Verify sample MCP config file exists and has correct format
- `cat playwright-mcp-config.json | grep './videos'` - Verify video path is relative
- `grep -E '(\.mcp\.json|videos/)' .gitignore` - Verify gitignore excludes MCP files
- `test -f .claude/commands/e2e/test_playwright_mcp_integration.md` - Verify E2E test file exists

## Notes
- The existing `.mcp.json` file should NOT be committed to git - only `.mcp.json.sample` should be committed
- Users will manually copy `.mcp.json.sample` to `.mcp.json` when setting up their local environment
- Video recordings can be large files - ensure they are excluded from git via `.gitignore`
- The E2E test should validate MCP functionality without testing application-specific features (those are covered by existing E2E tests like `test_basic_query.md`)
- Playwright browsers must be installed locally: `npx playwright install chromium`
- MCP server automatically starts when Claude Code detects `.mcp.json` configuration
- Screenshots are saved to `agents/<adw_id>/<agent_name>/img/` directory structure for organization
- This feature enables future E2E tests to be written more easily by providing the infrastructure
