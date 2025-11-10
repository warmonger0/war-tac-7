# Playwright MCP Integration

**ADW ID:** ba7c9f28
**Date:** 2025-11-10
**Specification:** specs/issue-28-adw-ba7c9f28-sdlc_planner-playwright-mcp-integration.md

## Overview

This feature integrates the Playwright Model Context Protocol (MCP) server into tac-webbuilder, enabling automated browser automation and end-to-end (E2E) testing capabilities for all generated web applications. The integration provides zero-touch testing infrastructure that is automatically included in all project templates (React-Vite, Next.js, Vanilla JS) and can be seamlessly integrated into existing projects.

## What Was Built

- **Root-level MCP configuration files** - Core `.mcp.json.sample` and `playwright-mcp-config.json` files with proper relative paths
- **Template integration** - MCP configuration files added to all three project templates (React-Vite, Next.js, Vanilla JS)
- **Scaffolding script enhancements** - `setup_new_project.sh` automatically copies MCP configuration for immediate use in new projects
- **Integration script enhancements** - `integrate_existing.sh` detects and adds MCP configuration to existing projects
- **Comprehensive documentation** - `docs/playwright-mcp.md` with setup, configuration, troubleshooting, and best practices
- **Updated project documentation** - README, architecture, examples, and troubleshooting docs all reference MCP capabilities
- **Validation tests** - Python tests in `app/server/tests/core/test_mcp_setup.py` and `app/server/tests/templates/test_mcp_in_templates.py`
- **E2E test specification** - `.claude/commands/e2e/test_playwright_mcp_integration.md` to validate the entire integration
- **Conditional documentation rules** - Updated `.claude/commands/conditional_docs.md` to reference MCP documentation

## Technical Implementation

### Files Modified

- `scripts/setup_new_project.sh`: Added MCP configuration copying step and videos directory creation
- `scripts/integrate_existing.sh`: Added MCP setup section with detection, file copying, and .gitignore updates
- `.gitignore`: Added `.mcp.json` and `videos/` patterns
- `templates/new_webapp/react-vite/.gitignore`: Added MCP-specific ignore patterns
- `templates/new_webapp/nextjs/.gitignore`: Added MCP-specific ignore patterns
- `templates/new_webapp/vanilla/.gitignore`: Added MCP-specific ignore patterns
- `templates/template_structure.json`: Added `.mcp.json.sample` and `playwright-mcp-config.json` to all template definitions
- `README.md`: Added Playwright MCP Integration section with setup instructions and capabilities overview
- `docs/architecture.md`: Added MCP to system architecture
- `docs/examples.md`: Added examples leveraging Playwright MCP
- `docs/troubleshooting.md`: Added MCP-specific troubleshooting section
- `.claude/commands/conditional_docs.md`: Added conditional documentation rules for MCP-related work
- `playwright-mcp-config.json`: Updated video directory path configuration

### Files Created

- `templates/new_webapp/react-vite/.mcp.json.sample`: MCP server configuration for React-Vite template
- `templates/new_webapp/react-vite/playwright-mcp-config.json`: Playwright browser settings for React-Vite template
- `templates/new_webapp/nextjs/.mcp.json.sample`: MCP server configuration for Next.js template
- `templates/new_webapp/nextjs/playwright-mcp-config.json`: Playwright browser settings for Next.js template
- `templates/new_webapp/vanilla/.mcp.json.sample`: MCP server configuration for Vanilla JS template
- `templates/new_webapp/vanilla/playwright-mcp-config.json`: Playwright browser settings for Vanilla JS template
- `docs/playwright-mcp.md`: Comprehensive MCP integration documentation
- `app/server/tests/core/test_mcp_setup.py`: Tests validating root-level MCP configuration
- `app/server/tests/templates/test_mcp_in_templates.py`: Tests validating MCP presence in all templates
- `.claude/commands/e2e/test_playwright_mcp_integration.md`: E2E test specification for validating MCP integration

### Key Changes

- **Relative path strategy**: All template configurations use relative paths (`./videos`, `./playwright-mcp-config.json`) to ensure portability across different project locations
- **Automatic setup in new projects**: `setup_new_project.sh` copies `.mcp.json.sample` as `.mcp.json` (removing the `.sample` suffix) for immediate usability
- **Detection for existing projects**: `integrate_existing.sh` checks if MCP configuration already exists before copying to avoid overwriting custom configurations
- **Consistent browser settings**: All templates use chromium in headless mode with 1920x1080 viewport and video recording enabled
- **Comprehensive .gitignore patterns**: Both `.mcp.json` (instance-specific config) and `videos/` (large recording files) are excluded from version control

## How to Use

### For New Projects

When creating a new project, MCP configuration is automatically included:

```bash
./scripts/setup_new_project.sh my-project react-vite
cd my-project

# MCP is already configured - just install Playwright browsers
npx playwright install chromium
```

### For Existing Projects

Add MCP integration to an existing project:

```bash
./scripts/integrate_existing.sh /path/to/existing/project

# Follow the integration request provided by the script
# MCP configuration files will be copied automatically
```

### Using Playwright MCP

The Playwright MCP server enables Claude Code to:

1. **Run E2E tests automatically**: Use `/test_e2e` command for automated test execution
2. **Capture screenshots**: Use `/review` command for visual validation with screenshots
3. **Record test videos**: Failed tests automatically save videos to the `videos/` directory
4. **Validate user flows**: Test critical user interactions programmatically
5. **Check visual regressions**: Compare screenshots across different viewport sizes

### Configuration

Edit `playwright-mcp-config.json` to customize:

- **Browser type**: Change `browserName` from "chromium" to "firefox" or "webkit"
- **Headless mode**: Set `headless: false` for debugging (default: `true`)
- **Viewport size**: Adjust `width` and `height` (default: 1920x1080)
- **Video recording**: Set `recordVideo: null` to disable (default: enabled)

See [docs/playwright-mcp.md](../docs/playwright-mcp.md) for detailed configuration options.

## Testing

### Unit Tests

```bash
# Validate MCP setup in project root
cd app/server && uv run pytest tests/core/test_mcp_setup.py -v

# Validate MCP presence in all templates
cd app/server && uv run pytest tests/templates/test_mcp_in_templates.py -v
```

### E2E Test

```bash
# Run comprehensive MCP integration test
# Read and execute .claude/commands/e2e/test_playwright_mcp_integration.md
```

### Manual Validation

```bash
# Verify configuration files exist
test -f .mcp.json.sample && echo "✅ Root config exists"
test -f playwright-mcp-config.json && echo "✅ Playwright config exists"

# Validate JSON syntax
python3 -m json.tool .mcp.json.sample > /dev/null && echo "✅ Valid JSON"

# Check .gitignore patterns
grep -q "\.mcp\.json" .gitignore && echo "✅ .gitignore updated"
grep -q "videos/" .gitignore && echo "✅ videos/ ignored"

# Verify all templates have MCP files
for template in react-vite nextjs vanilla; do
  test -f "templates/new_webapp/$template/.mcp.json.sample" && echo "✅ $template has MCP"
done
```

## Notes

### Integration with ADW Workflows

Playwright MCP enables zero-touch testing in ADW workflows:

- **Testing Phase**: ADW automatically tests implemented features with E2E tests
- **Review Phase**: ADW captures screenshots for visual validation
- **Documentation Phase**: ADW generates UI examples with automated screenshots

This ensures higher quality deliverables with minimal manual intervention.

### Path Resolution Strategy

The implementation uses **relative paths in templates** (`./videos`, `./playwright-mcp-config.json`) to ensure portability. When ADW creates worktrees for isolated execution, these paths should be updated to absolute paths specific to that worktree (see `app_docs/feature-1afd9aba-project-structure-adw-integration.md`).

### Video Storage Considerations

Playwright video recordings can be large (multiple MB per test). The `.gitignore` patterns ensure videos are never committed to repositories. Best practices:

- Clean up old videos periodically
- Consider adding videos to CI/CD artifact storage
- Disable video recording in development if disk space is limited

### Template Consistency

All three templates (React-Vite, Next.js, Vanilla JS) receive **identical MCP configuration files**, ensuring consistent E2E testing capabilities regardless of framework choice. The only framework-specific differences are in package dependencies.

### Security Note

The `.mcp.json` file may contain instance-specific configuration and should not be committed to version control. Always copy from `.mcp.json.sample` and customize as needed.

## Future Enhancements

Potential extensions in future issues:

- Add configuration presets for multiple browsers (Firefox, WebKit)
- Implement visual regression testing with screenshot diffing
- Add performance testing capabilities with Lighthouse integration
- Create reusable test utilities for common patterns (auth flows, form submission, etc.)
- Integrate with CI/CD pipelines for automated testing on every commit
- Add mobile viewport presets for responsive testing
- Implement parallel test execution for faster feedback

## Related Documentation

- [docs/playwright-mcp.md](../docs/playwright-mcp.md) - Comprehensive MCP documentation with setup, configuration, troubleshooting
- [docs/architecture.md](../docs/architecture.md) - System architecture including MCP integration
- [docs/examples.md](../docs/examples.md) - Example requests leveraging Playwright MCP
- [docs/troubleshooting.md](../docs/troubleshooting.md) - MCP-specific troubleshooting section
- [app_docs/feature-1afd9aba-project-structure-adw-integration.md](feature-1afd9aba-project-structure-adw-integration.md) - MCP configuration path patterns for worktree isolation
