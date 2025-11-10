# Playwright MCP Integration

## What is Playwright MCP?

The Playwright Model Context Protocol (MCP) server enables Claude Code to:
- Control browsers programmatically
- Run E2E tests automatically
- Capture screenshots and videos
- Validate visual appearance
- Test user interactions

## Setup

### 1. Configure MCP
```bash
# Copy sample configuration
cp .mcp.json.sample .mcp.json
```

### 2. Install Playwright
```bash
npm install -D playwright
npx playwright install chromium
```

### 3. Verify Setup
The Playwright MCP server will automatically start when Claude Code runs.

## Usage

### In ADW Workflows

ADW workflows automatically use Playwright MCP for:
- **Testing Phase**: E2E test execution
- **Review Phase**: Visual validation with screenshots
- **Documentation Phase**: Capturing UI examples

### Manual Testing

Use `/test_e2e` command to run tests on demand.

### Visual Review

Use `/review` command to capture screenshots for review.

## Configuration

### Browser Settings
Edit `playwright-mcp-config.json`:

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "headless": true,
      "slowMo": 0
    }
  }
}
```

**Browser Options:**
- `browserName`: Choose `"chromium"`, `"firefox"`, or `"webkit"`
- `headless`: Set to `true` for CI/CD, `false` for debugging
- `slowMo`: Milliseconds to slow down operations (useful for debugging)

### Video Recording
Videos are saved to `./videos/` directory when tests run.

**Default Configuration:**
```json
{
  "browser": {
    "contextOptions": {
      "recordVideo": {
        "dir": "./videos",
        "size": {
          "width": 1920,
          "height": 1080
        }
      }
    }
  }
}
```

**To disable video recording:**
```json
{
  "browser": {
    "contextOptions": {
      "recordVideo": null
    }
  }
}
```

### Viewport Size
Default: 1920x1080

**To change viewport:**
```json
{
  "browser": {
    "contextOptions": {
      "viewport": {
        "width": 1280,
        "height": 720
      }
    }
  }
}
```

## Troubleshooting

### MCP Server Won't Start
**Symptoms:** MCP server fails to initialize or Claude Code can't connect to Playwright.

**Solutions:**
- Ensure Node.js is installed: `node --version`
- Verify Playwright MCP package: `npx @playwright/mcp@latest --version`
- Check `.mcp.json` syntax is valid JSON
- Review error logs in Claude Code output
- Try running manually: `npx @playwright/mcp@latest --config ./playwright-mcp-config.json`

### Browser Launch Fails
**Symptoms:** Browser doesn't open or crashes on launch.

**Solutions:**
- Install browser binaries: `npx playwright install chromium`
- Install system dependencies: `npx playwright install-deps`
- Check available disk space (browsers need ~500MB)
- Verify permissions on browser install directory
- Try a different browser: change `browserName` to `"firefox"` or `"webkit"`

### Videos Not Recording
**Symptoms:** No video files appear in `videos/` directory after tests.

**Solutions:**
- Ensure `videos/` directory exists: `mkdir -p videos`
- Check `recordVideo` config in `playwright-mcp-config.json` is not `null`
- Verify disk space available (videos can be large)
- Check write permissions on `videos/` directory
- Ensure path is relative: use `"./videos"` not absolute path

### Tests Are Flaky
**Symptoms:** Tests pass sometimes and fail other times.

**Solutions:**
- Add proper waits for dynamic content
- Use `waitForSelector` instead of hard-coded timeouts
- Increase timeout values for slow operations
- Check network conditions and API response times
- Use stable selectors (data-testid attributes)

## Best Practices

### 1. Headless Mode
**Production/CI:**
```json
{
  "browser": {
    "launchOptions": {
      "headless": true
    }
  }
}
```

**Local Debugging:**
```json
{
  "browser": {
    "launchOptions": {
      "headless": false,
      "slowMo": 100
    }
  }
}
```

Keep `headless: true` for CI/CD and automated workflows.
Use `headless: false` only for local debugging.

### 2. Video Storage
Videos can be large. Add to `.gitignore`:
```
videos/
```

**Recommended practices:**
- Delete old videos regularly to save disk space
- Only record videos for failed tests in CI
- Use lower resolution for CI: `1280x720` instead of `1920x1080`
- Consider using screenshots for quick validation instead of full videos

### 3. Screenshot Organization
Store screenshots in `logs/screenshots/` for easy access.

**Naming convention:**
```
logs/screenshots/YYYY-MM-DD_HH-MM-SS_test-name.png
```

### 4. Test Stability
Use proper waits and selectors to avoid flaky tests:

**Good practices:**
```typescript
// Good: Wait for element
await page.waitForSelector('[data-testid="submit-button"]');

// Good: Wait for network idle
await page.waitForLoadState('networkidle');

// Good: Wait for specific element state
await page.waitForSelector('button:not([disabled])');
```

**Bad practices:**
```typescript
// Bad: Hard-coded timeout
await page.waitForTimeout(5000);

// Bad: Fragile CSS selector
await page.click('.container > div:nth-child(3) > button');

// Bad: Assuming immediate availability
await page.click('#submit'); // Might not be ready yet
```

### 5. Selector Strategies

**Priority order:**
1. **data-testid attributes** (most stable)
   ```typescript
   await page.click('[data-testid="login-button"]');
   ```

2. **Semantic roles and labels** (accessible and stable)
   ```typescript
   await page.click('button:has-text("Login")');
   await page.getByRole('button', { name: 'Login' });
   ```

3. **IDs** (stable but may change)
   ```typescript
   await page.click('#login-btn');
   ```

4. **CSS classes** (least stable, avoid if possible)
   ```typescript
   await page.click('.btn-primary'); // Only if no better option
   ```

### 6. Error Handling

Always add error context to make debugging easier:

```typescript
try {
  await page.click('[data-testid="submit-button"]');
} catch (error) {
  // Take screenshot on error
  await page.screenshot({ path: 'logs/error-screenshot.png' });
  throw new Error(`Failed to click submit button: ${error.message}`);
}
```

### 7. Performance Optimization

**Reuse browser contexts:**
```json
{
  "browser": {
    "launchOptions": {
      "headless": true
    },
    "reuseExistingContext": true
  }
}
```

**Disable unnecessary features for CI:**
```json
{
  "browser": {
    "launchOptions": {
      "headless": true,
      "args": [
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-gpu"
      ]
    }
  }
}
```

## Examples

### Basic Navigation Test
```typescript
// Navigate to application
await page.goto('http://localhost:3000');

// Wait for page load
await page.waitForLoadState('domcontentloaded');

// Verify title
const title = await page.title();
expect(title).toContain('My App');
```

### Form Interaction Test
```typescript
// Fill form fields
await page.fill('[data-testid="username"]', 'testuser');
await page.fill('[data-testid="password"]', 'password123');

// Submit form
await page.click('[data-testid="login-button"]');

// Wait for navigation
await page.waitForURL('**/dashboard');

// Verify success
await expect(page.getByText('Welcome, testuser')).toBeVisible();
```

### Visual Regression Test
```typescript
// Navigate to page
await page.goto('http://localhost:3000/about');

// Wait for images to load
await page.waitForLoadState('networkidle');

// Take screenshot
await page.screenshot({
  path: 'logs/screenshots/about-page.png',
  fullPage: true
});

// Compare with baseline (requires additional tooling)
```

### Mobile Viewport Test
```typescript
// Set mobile viewport
await page.setViewportSize({ width: 375, height: 667 });

// Test mobile navigation
await page.click('[data-testid="mobile-menu-toggle"]');
await expect(page.getByRole('navigation')).toBeVisible();
```

## Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [ADW Workflow Documentation](../README.md)

## Integration with tac-webbuilder

All templates generated by tac-webbuilder include Playwright MCP configuration out-of-the-box:
- React-Vite template
- Next.js template
- Vanilla JavaScript template

Simply copy `.mcp.json.sample` to `.mcp.json` and install Playwright to get started with E2E testing.
