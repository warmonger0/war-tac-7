# Natural Language SQL Interface

A web application that converts natural language queries to SQL using AI, built with FastAPI and Vite + TypeScript.

## Features

- 🗣️ Natural language to SQL conversion using OpenAI or Anthropic
- 📁 Drag-and-drop file upload (.csv and .json)
- 📊 Interactive table results display
- 🔒 SQL injection protection
- ⚡ Fast development with Vite and uv

## Prerequisites

- Python 3.10+
- uv (Python package manager)
- Node.js 18+
- Bun (or your preferred npm tool: npm, yarn, etc.)
- OpenAI API key and/or Anthropic API key

## Setup

### 1. Install Dependencies

```bash
# Backend
cd app/server
uv sync --all-extras

# Frontend
cd app/client
bun install
```

### 2. Environment Configuration

Set up your API keys in the server directory:

```bash
cp .env.sample .env
# Edit .env and add your API keys
```


```bash
cd app/server
cp .env.sample .env
# Edit .env and add your API keys
```

## Quick Start

Use the provided script to start both services:

```bash
./scripts/start.sh
```

Press `Ctrl+C` to stop both services.

The script will:
- Check that `.env` exists in `app/server/`
- Start the backend on http://localhost:8000
- Start the frontend on http://localhost:5173
- Handle graceful shutdown when you exit

## Manual Start (Alternative)

### Backend
```bash
cd app/server
# .env is loaded automatically by python-dotenv
uv run python server.py
```

### Frontend
```bash
cd app/client
bun run dev
```

## Usage

1. **Upload Data**: Click "Upload" to open the modal
   - Use sample data buttons for quick testing
   - Or drag and drop your own .csv or .json files
   - Uploading a file with the same name will overwrite the existing table
2. **Query Your Data**: Type a natural language query like "Show me all users who signed up last week"
   - Press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux) to run the query
3. **View Results**: See the generated SQL and results in a table format
4. **Manage Tables**: Click the × button on any table to remove it

## Development

### Backend Commands
```bash
cd app/server
uv run python server.py      # Start server with hot reload
uv run pytest               # Run tests
uv add <package>            # Add package to project
uv remove <package>         # Remove package from project
uv sync --all-extras        # Sync all extras
```

### Frontend Commands
```bash
cd app/client
bun run dev                 # Start dev server
bun run build              # Build for production
bun run preview            # Preview production build
```

## Playwright MCP Integration

The application integrates the Playwright Model Context Protocol (MCP) server to enable automated browser testing and end-to-end (E2E) validation. Playwright MCP acts as a bridge between Claude Code (AI assistant) and browser automation tools, allowing comprehensive E2E tests to run automatically.

### What is Playwright MCP?

Playwright MCP provides:
- **Browser Automation**: Programmatic control of browsers for testing user workflows
- **Screenshot Capture**: Visual evidence of functionality and UI state
- **Video Recording**: Recordings of test executions for debugging
- **E2E Testing**: Automated validation of complete user journeys

### Setup

#### 1. Copy MCP Configuration

Create your local MCP configuration from the sample:

```bash
cp .mcp.json.sample .mcp.json
```

The `.mcp.json` file is user-specific and excluded from git. It configures the Playwright MCP server with the following settings:
- Command: `npx @playwright/mcp@latest`
- Isolated mode: Ensures clean browser sessions
- Config path: `./playwright-mcp-config.json`

#### 2. Install Playwright

Install Playwright and the required browser:

```bash
npm install -D playwright
npx playwright install chromium
```

#### 3. Verify Setup

The Playwright MCP server will automatically start when Claude Code runs. You can verify by checking that `.mcp.json` exists and is valid JSON.

### Configuration

#### Browser Settings

Edit `playwright-mcp-config.json` to customize browser behavior:

```json
{
  "browser": {
    "browserName": "chromium",  // Options: "chromium", "firefox", "webkit"
    "launchOptions": {
      "headless": true,  // Set to false for debugging
      "slowMo": 0        // Milliseconds to slow down operations
    }
  }
}
```

#### Video Recording

Videos are automatically recorded during test execution and saved to the `./videos/` directory. Each test creates a separate video file.

To disable video recording, edit `playwright-mcp-config.json`:

```json
{
  "contextOptions": {
    "recordVideo": null
  }
}
```

#### Viewport Size

Default viewport is 1920x1080. To customize:

```json
{
  "contextOptions": {
    "viewport": {
      "width": 1280,
      "height": 720
    }
  }
}
```

### Running E2E Tests

#### Using Claude Code CLI

Run E2E tests using the `/test_e2e` command:

```bash
claude /test_e2e .claude/commands/e2e/test_basic_query.md
```

This will:
1. Launch the Playwright browser
2. Navigate to the application
3. Execute test steps defined in the test file
4. Capture screenshots at key points
5. Generate a test report with results

#### Available Tests

E2E test files are located in `.claude/commands/e2e/`:
- `test_basic_query.md` - Tests natural language query functionality
- `test_playwright_mcp_integration.md` - Validates MCP integration

#### Test Output

Test results include:
- **Status**: `passed` or `failed`
- **Screenshots**: Saved to `agents/<adw_id>/<agent_name>/img/<test_name>/`
- **Video**: Saved to `videos/` directory
- **Error Details**: Detailed failure information if test fails

### Troubleshooting

#### MCP Server Won't Start

**Symptoms**: Claude Code reports MCP server connection errors

**Solutions**:
- Verify Node.js is installed: `node --version`
- Test MCP installation: `npx @playwright/mcp@latest --version`
- Check `.mcp.json` syntax with `cat .mcp.json | jq .`
- Ensure `playwright-mcp-config.json` exists in repository root

#### Browser Launch Fails

**Symptoms**: Tests fail with "Browser not found" or "Failed to launch browser"

**Solutions**:
- Install Playwright browsers: `npx playwright install chromium`
- Install system dependencies: `npx playwright install-deps`
- Check available browsers: `npx playwright list-browsers`

#### Videos Not Recording

**Symptoms**: No video files appear in `videos/` directory after tests

**Solutions**:
- Verify `videos/` directory exists: `mkdir -p videos`
- Check `recordVideo` config in `playwright-mcp-config.json`
- Ensure sufficient disk space: `df -h`
- Check file permissions: `ls -la videos/`

#### Screenshot Path Issues

**Symptoms**: Screenshots fail to save or appear in wrong location

**Solutions**:
- Ensure agent directory structure exists
- Check absolute paths are used when moving screenshots
- Verify write permissions on target directory

### Best Practices

#### 1. Headless Mode

- **Production/CI**: Keep `headless: true` for automated workflows
- **Debugging**: Use `headless: false` to watch tests execute

#### 2. Video Storage

Videos can be large files. Best practices:
- Keep videos excluded from git (already in `.gitignore`)
- Review videos after test failures for debugging
- Delete old videos periodically to save disk space

#### 3. Screenshot Organization

Screenshots are organized by:
- ADW ID (workflow run identifier)
- Agent name (e.g., `test_e2e`)
- Test name (e.g., `basic_query`)

This structure ensures screenshots don't conflict across test runs.

#### 4. Test Stability

Write stable tests using proper waits and selectors:

```typescript
// Good: Wait for element
await page.waitForSelector('[data-testid="submit-button"]');

// Bad: Hard-coded timeout
await page.waitForTimeout(5000);
```

### Writing New E2E Tests

To create a new E2E test:

1. Create a test file in `.claude/commands/e2e/`:
   ```markdown
   # E2E Test: [Test Name]

   ## User Story
   As a [user role]
   I want [goal]
   So that [benefit]

   ## Test Steps
   1. Navigate to the `Application URL`
   2. **Verify** [condition]
   3. Take a screenshot
   ...

   ## Success Criteria
   - [Criterion 1]
   - [Criterion 2]
   ```

2. Run the test:
   ```bash
   claude /test_e2e .claude/commands/e2e/your_test.md
   ```

3. Review results in the generated JSON output

For examples, see existing tests in `.claude/commands/e2e/`.

## Project Structure

```
.
├── app/                    # Main application
│   ├── client/             # Vite + TypeScript frontend
│   └── server/             # FastAPI backend
│
├── adws/                   # AI Developer Workflow (ADW) - GitHub issue automation system
├── scripts/                # Utility scripts (start.sh, stop_apps.sh)
├── specs/                  # Feature specifications
├── ai_docs/                # AI/LLM documentation
├── agents/                 # Agent execution logging
└── logs/                   # Structured session logs
```

## API Endpoints

- `POST /api/upload` - Upload CSV/JSON file
- `POST /api/query` - Process natural language query
- `GET /api/schema` - Get database schema
- `POST /api/insights` - Generate column insights
- `GET /api/health` - Health check

## Security

### SQL Injection Protection

The application implements comprehensive SQL injection protection through multiple layers:

1. **Centralized Security Module** (`core/sql_security.py`):
   - Identifier validation for table and column names
   - Safe query execution with parameterized queries
   - Proper escaping for identifiers using SQLite's square bracket notation
   - Dangerous operation detection and blocking

2. **Input Validation**:
   - All table and column names are validated against a whitelist pattern
   - SQL keywords cannot be used as identifiers
   - File names are sanitized before creating tables
   - User queries are validated for dangerous operations

3. **Query Execution Safety**:
   - Parameterized queries used wherever possible
   - Identifiers (table/column names) are properly escaped
   - Multiple statement execution is blocked
   - SQL comments are not allowed in queries

4. **Protected Operations**:
   - File uploads with malicious names are sanitized
   - Natural language queries cannot inject SQL
   - Table deletion uses validated identifiers
   - Data insights generation validates all inputs

### Security Best Practices for Development

When adding new SQL functionality:
1. Always use the `sql_security` module functions
2. Never concatenate user input directly into SQL strings
3. Use `execute_query_safely()` for all database operations
4. Validate all identifiers with `validate_identifier()`
5. For DDL operations, use `allow_ddl=True` explicitly

### Testing Security

Run the comprehensive security tests:
```bash
cd app/server
uv run pytest tests/test_sql_injection.py -v
```


### Additional Security Features

- CORS configured for local development only
- File upload validation (CSV and JSON only)
- Comprehensive error logging without exposing sensitive data
- Database operations are isolated with proper connection handling

## AI Developer Workflow (ADW)

The ADW system is a comprehensive automation framework that integrates GitHub issues with Claude Code CLI to classify issues, generate implementation plans, and automatically create pull requests. ADW processes GitHub issues by classifying them as `/chore`, `/bug`, or `/feature` commands and then implementing solutions autonomously.

### Prerequisites

Before using ADW, ensure you have the following installed and configured:

- **GitHub CLI**: `brew install gh` (macOS) or equivalent for your OS
- **Claude Code CLI**: Install from [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- **Python with uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **GitHub authentication**: `gh auth login`

### Environment Variables

Set these environment variables before running ADW:

```bash
export GITHUB_REPO_URL="https://github.com/owner/repository"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export CLAUDE_CODE_PATH="/path/to/claude"  # Optional, defaults to "claude"
export GITHUB_PAT="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Optional, only if using different account than 'gh auth login'
```

### Usage Modes

ADW supports three main operation modes:

#### 1. Manual Processing
Process a single GitHub issue manually (in isolated worktree):
```bash
cd adws/
uv run adw_plan_build_iso.py <issue-number>
```

#### 2. Automated Monitoring
Continuously monitor GitHub for new issues (polls every 20 seconds):
```bash
cd adws/
uv run trigger_cron.py
```

#### 3. Webhook Server
Start a webhook server for real-time GitHub event processing:
```bash
cd adws/
uv run trigger_webhook.py
```

### How ADW Works

1. **Issue Classification**: Analyzes GitHub issues and determines type (`/chore`, `/bug`, `/feature`)
2. **Planning**: Generates detailed implementation plans using Claude Code CLI
3. **Implementation**: Executes the plan by making code changes, running tests, and ensuring quality
4. **Integration**: Creates git commits and pull requests with semantic commit messages

### For More Information

For detailed technical documentation, configuration options, and troubleshooting, see [`adws/README.md`](adws/README.md).

## Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (requires 3.12+)
- Verify API keys are set: `echo $OPENAI_API_KEY`

**Frontend errors:**
- Clear node_modules: `rm -rf node_modules && bun install`
- Check Node version: `node --version` (requires 18+)

**CORS issues:**
- Ensure backend is running on port 8000
- Check vite.config.ts proxy settings