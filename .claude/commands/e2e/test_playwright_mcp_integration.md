# E2E Test: Playwright MCP Integration

Test Playwright MCP browser automation integration to validate that the MCP server is properly configured and can control browsers for E2E testing.

## User Story

As a developer
I want Playwright MCP to be properly integrated
So that I can use browser automation for E2E testing without manual browser interaction

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial page load
3. **Verify** the page loads successfully (status code 200 or page content visible)
4. **Verify** the browser window is visible and responsive
5. **Verify** the page title is present (any title is acceptable for this test)
6. **Verify** the viewport is set to 1920x1080 as configured in `playwright-mcp-config.json`
7. Take a screenshot of the full page
8. **Verify** screenshot files are created successfully
9. **Verify** MCP server responds to browser commands without errors
10. Close the browser cleanly

## Success Criteria
- Playwright MCP server starts without errors
- Browser launches successfully in headless mode
- Navigation to application URL works
- Page loads and renders content
- Screenshots are captured and saved correctly
- MCP server responds to all browser automation commands
- Browser closes cleanly without hanging
- No MCP communication errors occur
- 2 screenshots are taken
