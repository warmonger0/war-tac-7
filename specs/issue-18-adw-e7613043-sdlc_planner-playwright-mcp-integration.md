# Feature: Playwright MCP Integration

## Metadata
issue_number: `18`
adw_id: `e7613043`
issue_json: `{"number":18,"title":"Playwright MCP Integration","body":"# 🎯 ISSUE 7: tac-webbuilder - Playwright MCP Integration\n\n## Overview\nIntegrate the Playwright Model Context Protocol (MCP) server into tac-webbuilder to enable browser automation and E2E testing capabilities for all generated web applications.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory unless otherwise specified (e.g., copying from tac-7).\n\n## Dependencies\n**Requires**: Issue 1 (Project Foundation) to be completed\n\n## Tasks\n\n### 1. Copy MCP Configuration Files\nCopy MCP configuration from `/Users/Warmonger0/tac/tac-7`:\n\n**Files to copy**:\n- `.mcp.json.sample` → `tac-webbuilder/.mcp.json.sample`\n- `playwright-mcp-config.json` → `tac-webbuilder/playwright-mcp-config.json`\n\n**File**: `tac-webbuilder/.mcp.json.sample`\n```json\n{\n  \"mcpServers\": {\n    \"playwright\": {\n      \"command\": \"npx\",\n      \"args\": [\n        \"@playwright/mcp@latest\",\n        \"--isolated\",\n        \"--config\",\n        \"./playwright-mcp-config.json\"\n      ]\n    }\n  }\n}\n```\n\n**File**: `tac-webbuilder/playwright-mcp-config.json`\n```json\n{\n  \"browser\": {\n    \"browserName\": \"chromium\",\n    \"launchOptions\": {\n      \"headless\": true\n    },\n    \"contextOptions\": {\n      \"recordVideo\": {\n        \"dir\": \"./videos\",\n        \"size\": {\n          \"width\": 1920,\n          \"height\": 1080\n        }\n      },\n      \"viewport\": {\n        \"width\": 1920,\n        \"height\": 1080\n      }\n    }\n  }\n}\n```\n\n### 2. Update Template Projects with MCP\n**For each template** (`react-vite`, `nextjs`, `vanilla`):\n\nAdd to template structure:\n- `.mcp.json.sample` - MCP server configuration\n- `playwright-mcp-config.json` - Playwright-specific settings\n- `videos/` directory in `.gitignore`\n\n**File**: `templates/new_webapp/{template}/.gitignore` (add):\n```\n# MCP\n.mcp.json\nvideos/\n```\n\n### 3. Add MCP Setup to Integration Script\n**File**: `scripts/integrate_existing.sh` (update)\n\nAdd MCP setup step:\n```bash\n# Copy MCP configuration\necho \"📦 Setting up Playwright MCP...\"\ncp .mcp.json.sample .mcp.json\ncp playwright-mcp-config.json \"$PROJECT_PATH/\"\n\n# Add to .gitignore\nif ! grep -q \"\\.mcp\\.json\" \"$PROJECT_PATH/.gitignore\"; then\n    echo \".mcp.json\" >> \"$PROJECT_PATH/.gitignore\"\n    echo \"videos/\" >> \"$PROJECT_PATH/.gitignore\"\nfi\n```\n\n### 4. Update New Project Scaffolding\n**File**: `scripts/setup_new_project.sh` (update)\n\nAdd MCP configuration step after template copy:\n```bash\n# Set up MCP\necho \"🎭 Configuring Playwright MCP...\"\ncp .mcp.json.sample \"$PROJECT_PATH/.mcp.json\"\ncp playwright-mcp-config.json \"$PROJECT_PATH/\"\n```\n\n### 5. Add MCP to ADW Commands\nUpdate slash commands to leverage Playwright MCP:\n\n**File**: `.claude/commands/test_e2e.md` (copy from tac-7)\n```markdown\nRun E2E tests using Playwright MCP.\n\nSteps:\n1. Use Playwright MCP to navigate to the application\n2. Test critical user flows\n3. Capture screenshots and videos for failures\n4. Generate test report\n```\n\n**File**: `.claude/commands/review.md` (copy from tac-7)\n```markdown\nVisual review of the application using Playwright MCP.\n\nSteps:\n1. Launch application in Playwright browser\n2. Navigate through key pages\n3. Take screenshots at various viewport sizes\n4. Check for visual regressions\n5. Upload screenshots to comments\n```\n\n### 6. Documentation for MCP Usage\n**File**: `docs/playwright-mcp.md`\n\n```markdown\n# Playwright MCP Integration\n\n## What is Playwright MCP?\n\nThe Playwright Model Context Protocol (MCP) server enables Claude Code to:\n- Control browsers programmatically\n- Run E2E tests automatically\n- Capture screenshots and videos\n- Validate visual appearance\n- Test user interactions\n\n## Setup\n\n### 1. Configure MCP\n```bash\n# Copy sample configuration\ncp .mcp.json.sample .mcp.json\n```\n\n### 2. Install Playwright\n```bash\nnpm install -D playwright\nnpx playwright install chromium\n```\n\n### 3. Verify Setup\nThe Playwright MCP server will automatically start when Claude Code runs.\n\n## Usage\n\n### In ADW Workflows\n\nADW workflows automatically use Playwright MCP for:\n- **Testing Phase**: E2E test execution\n- **Review Phase**: Visual validation with screenshots\n- **Documentation Phase**: Capturing UI examples\n\n### Manual Testing\n\nUse `/test_e2e` command to run tests on demand.\n\n### Visual Review\n\nUse `/review` command to capture screenshots for review.\n\n## Configuration\n\n### Browser Settings\nEdit `playwright-mcp-config.json`:\n\n```json\n{\n  \"browser\": {\n    \"browserName\": \"chromium\",  // or \"firefox\", \"webkit\"\n    \"launchOptions\": {\n      \"headless\": true,  // Set to false for debugging\n      \"slowMo\": 0        // Milliseconds to slow down operations\n    }\n  }\n}\n```\n\n### Video Recording\nVideos are saved to `./videos/` directory when tests run.\n\nTo disable video recording:\n```json\n{\n  \"contextOptions\": {\n    \"recordVideo\": null\n  }\n}\n```\n\n### Viewport Size\nDefault: 1920x1080\n\nTo change:\n```json\n{\n  \"contextOptions\": {\n    \"viewport\": {\n      \"width\": 1280,\n      \"height\": 720\n    }\n  }\n}\n```\n\n## Troubleshooting\n\n### MCP Server Won't Start\n- Ensure Node.js is installed\n- Run `npx @playwright/mcp@latest --version` to verify\n- Check `.mcp.json` syntax is valid\n\n### Browser Launch Fails\n- Run `npx playwright install chromium`\n- Check system dependencies: `npx playwright install-deps`\n\n### Videos Not Recording\n- Ensure `videos/` directory exists\n- Check `recordVideo` config in `playwright-mcp-config.json`\n- Verify disk space available\n\n## Best Practices\n\n### 1. Headless Mode\nKeep `headless: true` for CI/CD and automated workflows.\nUse `headless: false` only for local debugging.\n\n### 2. Video Storage\nVideos can be large. Add to `.gitignore`:\n```\nvideos/\n```\n\n### 3. Screenshot Organization\nStore screenshots in `logs/screenshots/` for easy access.\n\n### 4. Test Stability\nUse proper waits and selectors to avoid flaky tests:\n```typescript\n// Good: Wait for element\nawait page.waitForSelector('[data-testid=\"submit-button\"]');\n\n// Bad: Hard-coded timeout\nawait page.waitForTimeout(5000);\n```\n\n## Examples\n\nSee `docs/examples.md` for example test requests that leverage Playwright MCP.\n```\n\n### 7. Update Foundation Issue\n**File**: `issue-1-foundation.md` (update)\n\nAdd to \"Copy ADW System from tac-7\" section:\n```markdown\n- `.mcp.json.sample` → `.mcp.json.sample`\n- `playwright-mcp-config.json` → `playwright-mcp-config.json`\n```\n\nAdd to .gitignore:\n```markdown\n.mcp.json\nvideos/\n```\n\n### 8. Update Templates Issue\n**File**: `issue-6-templates-docs.md` (update)\n\nAdd to each template structure:\n```markdown\n├── .mcp.json.sample\n├── playwright-mcp-config.json\n```\n\nAdd to \"Framework-Specific Notes\":\n```markdown\n### Playwright MCP Setup\nAll templates include:\n- `.mcp.json.sample` for MCP server configuration\n- `playwright-mcp-config.json` for browser settings\n- E2E test commands in `.claude/commands/`\n```\n\n## Testing\n\n### Test MCP Installation\n**File**: `tests/core/test_mcp_setup.py`\n\n```python\ndef test_mcp_config_exists():\n    \"\"\"Verify .mcp.json.sample exists.\"\"\"\n\ndef test_playwright_config_exists():\n    \"\"\"Verify playwright-mcp-config.json exists.\"\"\"\n\ndef test_mcp_config_valid_json():\n    \"\"\"Verify .mcp.json.sample is valid JSON.\"\"\"\n\ndef test_playwright_config_valid():\n    \"\"\"Verify playwright-mcp-config.json is valid.\"\"\"\n```\n\n### Test Template Integration\n**File**: `tests/templates/test_mcp_in_templates.py`\n\n```python\ndef test_react_vite_has_mcp():\n    \"\"\"Verify React-Vite template includes MCP config.\"\"\"\n\ndef test_nextjs_has_mcp():\n    \"\"\"Verify Next.js template includes MCP config.\"\"\"\n\ndef test_new_project_includes_mcp():\n    \"\"\"Verify scaffolding includes MCP setup.\"\"\"\n```\n\n## Success Criteria\n- ✅ `.mcp.json.sample` and `playwright-mcp-config.json` copied to tac-webbuilder\n- ✅ All templates include MCP configuration\n- ✅ Integration script sets up MCP for existing projects\n- ✅ New project scaffolding includes MCP\n- ✅ E2E and review commands copied from tac-7\n- ✅ Documentation explains MCP usage\n- ✅ `.gitignore` excludes `.mcp.json` and `videos/`\n- ✅ All tests pass\n\n## Benefits\n\n### For New Projects\n- E2E testing ready out-of-the-box\n- Visual review capabilities from day one\n- No manual Playwright setup needed\n\n### For Existing Projects\n- Easy integration via `webbuilder integrate`\n- Consistent testing across all projects\n- Automated visual validation\n\n### For ADW Workflows\n- Automated E2E test execution\n- Screenshot-based code review\n- Video recordings of test failures\n- Higher quality deliverables\n\n## Next Issue\nThis can run in parallel with other issues. No blocking dependencies.\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`infrastructure`, `testing`, `playwright`, `mcp`, `webbuilder`\n"}`

## Feature Description
Integrate the Playwright Model Context Protocol (MCP) server into the tac-webbuilder project to enable browser automation and end-to-end testing capabilities for all web applications generated by tac-webbuilder. This integration will copy MCP configuration files from the parent tac-7 repository, embed them into template projects (React-Vite, Next.js, Vanilla), update scaffolding scripts to include MCP setup, create ADW slash commands for E2E testing and visual review, add comprehensive documentation for MCP usage, and ensure proper gitignore configuration to exclude generated artifacts. The feature establishes a foundation for automated browser testing that can be used during the ADW workflow testing phases.

## User Story
As a tac-webbuilder user
I want Playwright MCP automatically configured in my generated web applications
So that I can run end-to-end tests and visual reviews using Claude Code's browser automation capabilities without manual setup

## Problem Statement
Web applications generated by tac-webbuilder currently lack browser automation and E2E testing infrastructure. Developers must manually install and configure Playwright, set up MCP servers, create test commands, and integrate with ADW workflows. This creates friction for testing, reduces confidence in deployments, and makes visual validation cumbersome. Without standardized E2E test infrastructure, each project has different testing approaches, and ADW workflows cannot automatically validate UI functionality or capture visual artifacts for code review.

## Solution Statement
Copy the proven Playwright MCP configuration from the parent tac-7 repository (which already uses Playwright MCP successfully) into tac-webbuilder, embed it into all template projects so new applications get E2E testing out-of-the-box, update scaffolding scripts to configure MCP during project setup, create reusable ADW slash commands for running E2E tests and visual reviews, and provide comprehensive documentation explaining MCP usage, configuration options, and troubleshooting. This approach leverages existing working infrastructure and ensures consistency across all tac-webbuilder generated projects.

## Relevant Files
Use these files to implement the feature:

- **/.mcp.json.sample** - Source MCP server configuration from tac-7 root; will be copied to tac-webbuilder
- **/playwright-mcp-config.json** - Source Playwright configuration from tac-7 root with absolute paths; needs modification for relative paths in tac-webbuilder
- **/.claude/commands/test_e2e.md** - E2E test runner command in tac-7; will be used as reference for tac-webbuilder commands
- **/.claude/commands/e2e/test_basic_query.md** - Example E2E test format; reference for understanding test structure
- **/projects/tac-webbuilder/.gitignore** - tac-webbuilder gitignore; needs updates to exclude MCP artifacts
- **/projects/tac-webbuilder/README.md** - tac-webbuilder documentation; needs MCP integration section
- **/projects/tac-webbuilder/scripts/** - Scaffolding scripts directory; needs MCP setup integration
- **/projects/tac-webbuilder/templates/** - Template projects directory; needs MCP files embedded
- **/projects/tac-webbuilder/.claude/commands/** - ADW commands directory; needs test_e2e.md and review.md
- **/app_docs/feature-1afd9aba-project-structure-adw-integration.md** - MCP configuration patterns and absolute path management reference

### New Files

The following new files will be created:

- **projects/tac-webbuilder/.mcp.json.sample** - MCP server configuration for tac-webbuilder (copied and modified from tac-7 root)
- **projects/tac-webbuilder/playwright-mcp-config.json** - Playwright browser configuration with relative paths for videos directory
- **projects/tac-webbuilder/.claude/commands/test_e2e.md** - E2E test runner command adapted for tac-webbuilder
- **projects/tac-webbuilder/.claude/commands/review.md** - Visual review command using Playwright to capture screenshots
- **projects/tac-webbuilder/.claude/commands/e2e/** - Directory for E2E test specifications
- **projects/tac-webbuilder/docs/playwright-mcp.md** - Comprehensive MCP usage documentation
- **projects/tac-webbuilder/templates/new_webapp/react-vite/.mcp.json.sample** - MCP config for React-Vite template
- **projects/tac-webbuilder/templates/new_webapp/react-vite/playwright-mcp-config.json** - Playwright config for React-Vite template
- **projects/tac-webbuilder/templates/new_webapp/nextjs/.mcp.json.sample** - MCP config for Next.js template
- **projects/tac-webbuilder/templates/new_webapp/nextjs/playwright-mcp-config.json** - Playwright config for Next.js template
- **projects/tac-webbuilder/templates/new_webapp/vanilla/.mcp.json.sample** - MCP config for Vanilla template
- **projects/tac-webbuilder/templates/new_webapp/vanilla/playwright-mcp-config.json** - Playwright config for Vanilla template
- **projects/tac-webbuilder/tests/core/test_mcp_setup.py** - Unit tests verifying MCP configuration files exist and are valid
- **projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py** - Unit tests verifying templates include MCP configuration

## Implementation Plan

### Phase 1: Foundation
Copy MCP configuration files from tac-7 root to tac-webbuilder, modifying absolute paths to relative paths since tac-webbuilder templates don't use worktree isolation. Update tac-webbuilder's .gitignore to exclude .mcp.json (active config) and videos/ directory. Create docs/ directory structure if it doesn't exist for documentation files.

### Phase 2: Core Implementation
Embed MCP configuration files into all three template projects (react-vite, nextjs, vanilla) and update their .gitignore files to exclude MCP artifacts. Create ADW slash commands (test_e2e.md and review.md) adapted from tac-7 patterns. Write comprehensive MCP documentation explaining setup, configuration, troubleshooting, and best practices. Update tac-webbuilder README with MCP integration overview.

### Phase 3: Integration
Update scaffolding scripts (if they exist, otherwise create setup instructions in README) to copy MCP configuration during project initialization. Create comprehensive pytest tests to verify MCP files exist, contain valid JSON, and are properly embedded in all templates. Update any existing issue specifications or documentation that references template structure to include MCP files.

## Step by Step Tasks

### 1. Copy and Adapt MCP Configuration Files to tac-webbuilder Root
- Read `/.mcp.json.sample` to understand structure
- Read `/playwright-mcp-config.json` to understand Playwright settings
- Read `/app_docs/feature-1afd9aba-project-structure-adw-integration.md` to understand absolute vs relative path strategy
- Create `projects/tac-webbuilder/.mcp.json.sample` with relative path to playwright-mcp-config.json
- Create `projects/tac-webbuilder/playwright-mcp-config.json` with relative path `./videos` instead of absolute path
- Verify JSON syntax is valid in both files

### 2. Update tac-webbuilder .gitignore
- Read `projects/tac-webbuilder/.gitignore` to understand current exclusions
- Add section comment `# MCP`
- Add `.mcp.json` (exclude active config, keep .sample tracked)
- Add `videos/` (exclude video recordings)
- Ensure no duplicate entries exist

### 3. Create docs/ Directory and MCP Documentation
- Check if `projects/tac-webbuilder/docs/` exists; create if not
- Create `projects/tac-webbuilder/docs/playwright-mcp.md` with comprehensive documentation covering:
  - What is Playwright MCP and its capabilities
  - Setup instructions (3 steps: copy config, install playwright, verify)
  - Usage in ADW workflows (testing, review, documentation phases)
  - Configuration options (browser settings, video recording, viewport)
  - Troubleshooting common issues (server won't start, browser fails, videos not recording)
  - Best practices (headless mode, video storage, screenshot organization, test stability)

### 4. Embed MCP Configuration in React-Vite Template
- Create `projects/tac-webbuilder/templates/new_webapp/react-vite/.mcp.json.sample`
- Create `projects/tac-webbuilder/templates/new_webapp/react-vite/playwright-mcp-config.json`
- Read `projects/tac-webbuilder/templates/new_webapp/react-vite/.gitignore`
- Add MCP exclusions to React-Vite template .gitignore (`.mcp.json` and `videos/`)

### 5. Embed MCP Configuration in Next.js Template
- Create `projects/tac-webbuilder/templates/new_webapp/nextjs/.mcp.json.sample`
- Create `projects/tac-webbuilder/templates/new_webapp/nextjs/playwright-mcp-config.json`
- Read `projects/tac-webbuilder/templates/new_webapp/nextjs/.gitignore` if it exists
- Add MCP exclusions to Next.js template .gitignore (`.mcp.json` and `videos/`)

### 6. Embed MCP Configuration in Vanilla Template
- Create `projects/tac-webbuilder/templates/new_webapp/vanilla/.mcp.json.sample`
- Create `projects/tac-webbuilder/templates/new_webapp/vanilla/playwright-mcp-config.json`
- Read `projects/tac-webbuilder/templates/new_webapp/vanilla/.gitignore` if it exists
- Add MCP exclusions to Vanilla template .gitignore (`.mcp.json` and `videos/`)

### 7. Create ADW E2E Test Command
- Check if `projects/tac-webbuilder/.claude/commands/e2e/` exists; create if not
- Read `/.claude/commands/test_e2e.md` as reference
- Create `projects/tac-webbuilder/.claude/commands/test_e2e.md` adapted for tac-webbuilder context
- Command should reference MCP server usage, screenshot capture, and test execution patterns
- Remove any tac-7 specific paths or references

### 8. Create ADW Visual Review Command
- Create `projects/tac-webbuilder/.claude/commands/review.md` for visual validation
- Command should use Playwright MCP to:
  - Launch application in browser
  - Navigate through key pages
  - Capture screenshots at different viewport sizes
  - Identify visual regressions
  - Upload screenshots for review comments

### 9. Update tac-webbuilder README with MCP Overview
- Read `projects/tac-webbuilder/README.md` to understand current structure
- Add section "Playwright MCP Integration" after main feature list or in appropriate location
- Include brief overview of capabilities (browser automation, E2E tests, screenshots)
- Reference detailed documentation at `docs/playwright-mcp.md`
- Add quick start commands (copy .mcp.json.sample, install playwright)

### 10. Create Unit Tests for MCP Configuration Validation
- Create `projects/tac-webbuilder/tests/core/test_mcp_setup.py`
- Implement `test_mcp_config_exists()` to verify `.mcp.json.sample` exists in tac-webbuilder root
- Implement `test_playwright_config_exists()` to verify `playwright-mcp-config.json` exists in tac-webbuilder root
- Implement `test_mcp_config_valid_json()` to parse and validate .mcp.json.sample structure
- Implement `test_playwright_config_valid()` to parse and validate playwright-mcp-config.json structure
- Tests should use pytest and standard library json module

### 11. Create Unit Tests for Template MCP Integration
- Create `projects/tac-webbuilder/tests/templates/test_mcp_in_templates.py`
- Implement `test_react_vite_has_mcp()` to verify React-Vite template includes both MCP files
- Implement `test_nextjs_has_mcp()` to verify Next.js template includes both MCP files
- Implement `test_vanilla_has_mcp()` to verify Vanilla template includes both MCP files
- Implement `test_templates_have_mcp_gitignore()` to verify all templates exclude MCP artifacts
- Tests should verify file existence and valid JSON structure

### 12. Verify Template Directory Structure
- Read `projects/tac-webbuilder/templates/new_webapp/react-vite/` structure
- Read `projects/tac-webbuilder/templates/new_webapp/nextjs/` structure
- Read `projects/tac-webbuilder/templates/new_webapp/vanilla/` structure
- Document any template-specific considerations in implementation notes

### 13. Check for Scaffolding Scripts
- Check if `projects/tac-webbuilder/scripts/setup_new_project.sh` exists
- Check if `projects/tac-webbuilder/scripts/integrate_existing.sh` exists
- If scripts exist, read them to understand project setup flow
- If scripts exist, add MCP configuration copying steps:
  - Copy .mcp.json.sample to .mcp.json in new project
  - Copy playwright-mcp-config.json to new project
  - Add .mcp.json and videos/ to project .gitignore
- If scripts don't exist, document manual setup steps in README or docs/playwright-mcp.md

### 14. Update Scaffolding Scripts (if they exist)
- Update `projects/tac-webbuilder/scripts/setup_new_project.sh` with MCP setup section
- Add echo message: "🎭 Configuring Playwright MCP..."
- Copy MCP files to new project directory
- Update `projects/tac-webbuilder/scripts/integrate_existing.sh` with MCP setup section
- Add echo message: "📦 Setting up Playwright MCP..."
- Add gitignore entries if not present

### 15. Create E2E Test Examples
- Create example E2E test in `projects/tac-webbuilder/.claude/commands/e2e/` directory
- Consider creating a basic template validation test (e.g., test that a newly generated project loads correctly)
- Reference `/.claude/commands/e2e/test_basic_query.md` format for consistency
- Keep examples simple and focused on validating template generation

### 16. Validate MCP Configuration Paths
- Verify all playwright-mcp-config.json files use relative path `./videos`
- Verify all .mcp.json.sample files reference relative path `./playwright-mcp-config.json`
- Test that paths work from template directories when templates are copied to new locations
- Ensure no absolute paths from tac-7 worktree environment leak into tac-webbuilder

### 17. Create Videos Directory in tac-webbuilder Root
- Create `projects/tac-webbuilder/videos/` directory (or ensure it's created on first run)
- Add .gitkeep file if directory should be tracked empty, or let it be created dynamically
- Verify directory is excluded in .gitignore

### 18. Document ADW Workflow Integration Points
- Update `projects/tac-webbuilder/docs/playwright-mcp.md` with section on ADW integration
- Explain how test_e2e command is used during ADW testing phase
- Explain how review command is used during ADW review phase
- Document expected screenshot locations and naming conventions

### 19. Run All Tests to Verify Implementation
- Run `cd projects/tac-webbuilder && pytest tests/core/test_mcp_setup.py -v` to verify MCP config files
- Run `cd projects/tac-webbuilder && pytest tests/templates/test_mcp_in_templates.py -v` to verify template integration
- Verify all tests pass with zero failures
- Fix any issues discovered during testing

### 20. Validation Commands Execution
- Execute all commands in the Validation Commands section to ensure zero regressions
- Verify tac-webbuilder project structure is correct
- Verify all templates include MCP configuration
- Verify documentation is comprehensive and accurate
- Verify tests provide adequate coverage

## Testing Strategy

### Unit Tests

#### MCP Configuration Tests (`tests/core/test_mcp_setup.py`)
- `test_mcp_config_exists()`: Verify `.mcp.json.sample` exists at tac-webbuilder root
- `test_playwright_config_exists()`: Verify `playwright-mcp-config.json` exists at tac-webbuilder root
- `test_mcp_config_valid_json()`: Parse .mcp.json.sample and verify structure (mcpServers.playwright.command, args)
- `test_playwright_config_valid()`: Parse playwright-mcp-config.json and verify structure (browser.browserName, launchOptions, contextOptions)
- `test_playwright_config_uses_relative_paths()`: Verify videos directory path is relative `./videos` not absolute

#### Template Integration Tests (`tests/templates/test_mcp_in_templates.py`)
- `test_react_vite_has_mcp()`: Verify both MCP files exist in react-vite template directory
- `test_nextjs_has_mcp()`: Verify both MCP files exist in nextjs template directory
- `test_vanilla_has_mcp()`: Verify both MCP files exist in vanilla template directory
- `test_templates_have_mcp_gitignore()`: Verify all templates exclude `.mcp.json` and `videos/` in .gitignore
- `test_template_mcp_configs_valid_json()`: Parse all template MCP files and verify valid JSON

### Edge Cases

#### Path Resolution
- Verify relative paths work when templates are copied to different directories
- Test that `./playwright-mcp-config.json` reference resolves correctly from .mcp.json.sample
- Test that `./videos` directory path resolves correctly from playwright-mcp-config.json

#### File Existence
- Test behavior when .mcp.json.sample already exists in target directory (should overwrite or skip?)
- Test behavior when videos/ directory already exists (should be fine, gitignored)
- Test behavior when user has custom .mcp.json (sample should not overwrite active config)

#### JSON Validity
- Test that all MCP JSON files parse without syntax errors
- Test that required fields are present in configurations
- Test that relative paths don't contain invalid characters

#### Gitignore Integration
- Test that .mcp.json is properly excluded (active config)
- Test that .mcp.json.sample is NOT excluded (sample should be tracked)
- Test that videos/ directory is excluded
- Test that no duplicate gitignore entries are created

#### Template Isolation
- Verify each template has independent MCP configuration (not symlinked)
- Verify changes to one template don't affect others
- Verify template configs work when copied to new project locations

## Acceptance Criteria

- `.mcp.json.sample` file exists in `projects/tac-webbuilder/` root directory with relative path to Playwright config
- `playwright-mcp-config.json` file exists in `projects/tac-webbuilder/` root directory with relative `./videos` path
- All three template directories (react-vite, nextjs, vanilla) contain both `.mcp.json.sample` and `playwright-mcp-config.json` files
- All template .gitignore files exclude `.mcp.json` and `videos/` directory
- `projects/tac-webbuilder/.gitignore` excludes `.mcp.json` and `videos/` directory
- `projects/tac-webbuilder/.claude/commands/test_e2e.md` exists with E2E test runner instructions
- `projects/tac-webbuilder/.claude/commands/review.md` exists with visual review instructions
- `projects/tac-webbuilder/docs/playwright-mcp.md` exists with comprehensive MCP documentation (setup, usage, configuration, troubleshooting)
- `projects/tac-webbuilder/README.md` includes overview section about Playwright MCP integration
- `tests/core/test_mcp_setup.py` exists with 5+ tests verifying MCP configuration
- `tests/templates/test_mcp_in_templates.py` exists with 5+ tests verifying template integration
- All pytest tests pass with zero failures
- All MCP JSON configuration files contain valid JSON (no syntax errors)
- All MCP configurations use relative paths (no absolute paths from tac-7 environment)
- Scaffolding scripts (if present) include MCP setup steps with appropriate echo messages
- Documentation clearly explains how to configure, use, and troubleshoot Playwright MCP

## Validation Commands

Execute every command to validate the feature works correctly with zero regressions.

- `cd projects/tac-webbuilder && pytest tests/core/test_mcp_setup.py -v` - Verify MCP configuration files exist and are valid
- `cd projects/tac-webbuilder && pytest tests/templates/test_mcp_in_templates.py -v` - Verify all templates include MCP configuration
- `cd projects/tac-webbuilder && pytest -v` - Run all tac-webbuilder tests to ensure zero regressions
- `ls -la projects/tac-webbuilder/.mcp.json.sample projects/tac-webbuilder/playwright-mcp-config.json` - Verify root MCP files exist
- `ls -la projects/tac-webbuilder/templates/new_webapp/react-vite/.mcp.json.sample projects/tac-webbuilder/templates/new_webapp/react-vite/playwright-mcp-config.json` - Verify React-Vite template has MCP files
- `ls -la projects/tac-webbuilder/templates/new_webapp/nextjs/.mcp.json.sample projects/tac-webbuilder/templates/new_webapp/nextjs/playwright-mcp-config.json` - Verify Next.js template has MCP files
- `ls -la projects/tac-webbuilder/templates/new_webapp/vanilla/.mcp.json.sample projects/tac-webbuilder/templates/new_webapp/vanilla/playwright-mcp-config.json` - Verify Vanilla template has MCP files
- `cat projects/tac-webbuilder/.mcp.json.sample | python -m json.tool` - Validate .mcp.json.sample is valid JSON
- `cat projects/tac-webbuilder/playwright-mcp-config.json | python -m json.tool` - Validate playwright-mcp-config.json is valid JSON
- `grep -q ".mcp.json" projects/tac-webbuilder/.gitignore && echo "Found" || echo "Missing"` - Verify .mcp.json is gitignored
- `grep -q "videos/" projects/tac-webbuilder/.gitignore && echo "Found" || echo "Missing"` - Verify videos/ is gitignored
- `ls -la projects/tac-webbuilder/.claude/commands/test_e2e.md` - Verify E2E test command exists
- `ls -la projects/tac-webbuilder/.claude/commands/review.md` - Verify review command exists
- `ls -la projects/tac-webbuilder/docs/playwright-mcp.md` - Verify MCP documentation exists
- `wc -l projects/tac-webbuilder/docs/playwright-mcp.md` - Verify documentation is comprehensive (should be 100+ lines)

## Notes

### MCP Configuration Path Strategy
The tac-7 root repository uses absolute paths in MCP configurations because it operates with worktree isolation where each ADW execution runs in a separate `trees/{adw_id}/` directory. However, tac-webbuilder is a project template system that generates new projects in arbitrary locations, so it must use relative paths. When copying configurations from tac-7 to tac-webbuilder, replace absolute paths with relative equivalents:

- `.mcp.json`: Change `"--config", "/absolute/path/playwright-mcp-config.json"` to `"--config", "./playwright-mcp-config.json"`
- `playwright-mcp-config.json`: Change `"dir": "/absolute/path/videos"` to `"dir": "./videos"`

### Template vs Root Configuration
Both tac-webbuilder root and all template directories should include MCP configuration files. The root configuration is used when developing tac-webbuilder itself (for testing the templates). The template configurations are embedded in generated projects so users get E2E testing capabilities out-of-the-box.

### Video Storage Considerations
Playwright can generate large video files (several MB per test run). The `videos/` directory is gitignored to prevent committing these artifacts. Users should be informed in documentation that video storage can grow over time and they should periodically clean up old videos. Consider documenting this in the troubleshooting section of `docs/playwright-mcp.md`.

### ADW Workflow Integration
The `test_e2e.md` and `review.md` commands integrate with ADW workflows during the testing and review phases. When ADW runs these commands, screenshots and videos are captured to the `agents/{adw_id}/{agent_name}/img/` directory (as defined in test_e2e.md). This provides visual artifacts for code review and regression testing.

### Playwright Installation Note
Playwright requires a separate installation step (`npx playwright install chromium`) to download browser binaries. This should be documented clearly in `docs/playwright-mcp.md` setup instructions. Consider adding a note in tac-webbuilder README that users must run this command before E2E tests will work.

### No Python Dependencies Required
This feature is purely configuration-based and requires no Python package additions to tac-webbuilder. Playwright MCP runs as a separate Node.js process via npx, and the MCP server is started automatically by Claude Code when it reads the .mcp.json configuration.
