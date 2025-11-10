# E2E Test: Playwright MCP Integration

## User Story
As a developer using tac-webbuilder, I want to verify that the Playwright MCP integration works correctly so that I can confidently use browser automation and E2E testing capabilities in my projects.

## Prerequisites
- Project scaffolded with one of the templates (react-vite, nextjs, or vanilla)
- MCP configuration files present (.mcp.json.sample, playwright-mcp-config.json)
- Node.js and npm installed

## Test Steps

### Step 1: Verify MCP Configuration Files Exist
**Action**: Check for MCP configuration files in the project
**Expected**: 
- `.mcp.json.sample` exists in project root
- `playwright-mcp-config.json` exists in project root
- Both files are valid JSON

**Validation**:
```bash
test -f .mcp.json.sample && echo "✓ .mcp.json.sample exists"
test -f playwright-mcp-config.json && echo "✓ playwright-mcp-config.json exists"
python3 -m json.tool .mcp.json.sample > /dev/null && echo "✓ .mcp.json.sample is valid JSON"
python3 -m json.tool playwright-mcp-config.json > /dev/null && echo "✓ playwright-mcp-config.json is valid JSON"
```

### Step 2: Verify .gitignore Contains MCP Patterns
**Action**: Check .gitignore for MCP-specific patterns
**Expected**: 
- `.mcp.json` is in .gitignore
- `videos/` is in .gitignore

**Validation**:
```bash
grep -q "\.mcp\.json" .gitignore && echo "✓ .gitignore includes .mcp.json"
grep -q "videos/" .gitignore && echo "✓ .gitignore includes videos/"
```

### Step 3: Verify MCP Configuration Structure
**Action**: Validate MCP configuration references Playwright correctly
**Expected**:
- .mcp.json.sample contains mcpServers.playwright configuration
- Configuration references ./playwright-mcp-config.json
- Playwright config uses relative path for video directory (./videos)

**Validation**:
```bash
# Check MCP config references playwright-mcp-config.json
grep -q '"./playwright-mcp-config.json"' .mcp.json.sample && echo "✓ MCP config uses relative path"

# Check playwright config uses relative video path
grep -q '"./videos"' playwright-mcp-config.json && echo "✓ Playwright uses relative video path"
```

### Step 4: Copy .mcp.json.sample to .mcp.json
**Action**: Create the active MCP configuration
**Expected**: .mcp.json is created from .mcp.json.sample

**Validation**:
```bash
cp .mcp.json.sample .mcp.json
test -f .mcp.json && echo "✓ .mcp.json created"
```

### Step 5: Verify Playwright MCP Server Can Start
**Action**: Attempt to verify Playwright MCP is available
**Expected**: npx @playwright/mcp@latest is accessible

**Validation**:
```bash
npx @playwright/mcp@latest --version 2>&1 | head -n 1
```

**Note**: This step verifies the MCP server package is available. The actual server will be started by Claude Code.

### Step 6: Test Browser Automation (via Playwright MCP)
**Action**: Use Playwright MCP to navigate to a test page
**Expected**:
- Playwright MCP server responds to commands
- Browser can be launched (chromium)
- Screenshot can be captured
- Video recording is configured

**Test Request**: "Use Playwright MCP to navigate to https://example.com and take a screenshot"

**Expected Behavior**:
1. Playwright MCP server starts successfully
2. Browser launches (chromium in headless mode)
3. Page navigation succeeds
4. Screenshot is captured
5. Screenshot file is saved

**Capture Screenshot**: Save the screenshot to verify visual output

### Step 7: Verify Video Directory Creation
**Action**: Check that the videos directory exists or can be created
**Expected**: videos/ directory exists

**Validation**:
```bash
mkdir -p videos
test -d videos && echo "✓ videos/ directory exists"
```

### Step 8: Validate Configuration Consistency
**Action**: Verify template configurations match expectations
**Expected**:
- browserName is "chromium"
- headless is true
- viewport is 1920x1080
- video size is 1920x1080

**Validation**:
```bash
# Check browser settings
grep -q '"chromium"' playwright-mcp-config.json && echo "✓ Browser is chromium"
grep -q '"headless": true' playwright-mcp-config.json && echo "✓ Headless mode enabled"
grep -q '"width": 1920' playwright-mcp-config.json && echo "✓ Viewport width correct"
```

## Success Criteria

✅ All MCP configuration files exist and are valid JSON
✅ .gitignore contains MCP-specific patterns
✅ Configuration uses relative paths (not absolute)
✅ .mcp.json can be created from .mcp.json.sample
✅ Playwright MCP package is accessible
✅ Browser automation works (navigation and screenshot capture)
✅ Video recording directory exists
✅ Configuration values match expected defaults

## Output Format

Provide a summary report:

```
Playwright MCP Integration Test Results
========================================

Configuration Files: ✓ PASS / ✗ FAIL
.gitignore Patterns: ✓ PASS / ✗ FAIL
Path Configuration: ✓ PASS / ✗ FAIL
MCP Server Availability: ✓ PASS / ✗ FAIL
Browser Automation: ✓ PASS / ✗ FAIL
Video Directory: ✓ PASS / ✗ FAIL
Configuration Consistency: ✓ PASS / ✗ FAIL

Overall Result: ✓ ALL TESTS PASSED / ✗ SOME TESTS FAILED

[Detailed explanation of any failures]
```

## Cleanup

After test completion:
- Videos can be deleted from videos/ directory
- .mcp.json can remain for further testing
- Screenshots captured during testing can be reviewed

## Notes

- This test validates the MCP integration infrastructure only
- Full E2E testing of application features requires a running application
- Browser automation depends on Playwright browsers being installed
- The test can be run in any project created from tac-webbuilder templates
