# Natural Language SQL Interface

A web application that converts natural language queries to SQL using AI, built with FastAPI and Vite + TypeScript.

## Features

- 🗣️ Natural language to SQL conversion using OpenAI or Anthropic
- 📁 Drag-and-drop file upload (.csv and .json)
- 📊 Interactive table results display
- 🔒 SQL injection protection
- ⚡ Fast development with Vite and uv
- 🤖 Natural language to GitHub issue generation (NEW)

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

## Natural Language to GitHub Issue Generation

The application now includes a powerful feature for converting natural language requests into structured GitHub issues with appropriate ADW workflow triggers.

### Features

- **Intent Analysis**: Automatically classifies requests as feature, bug, or chore
- **Requirement Extraction**: Extracts technical requirements from natural language
- **Project Context Detection**: Analyzes project structure to detect framework, tech stack, and complexity
- **Smart Workflow Selection**: Recommends appropriate ADW workflow and model set based on complexity
- **GitHub CLI Integration**: Posts issues directly to GitHub with preview and confirmation

### Required Environment Variables

```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxx"  # Required for NL processing
export GITHUB_REPO_URL="owner/repo"      # Optional, defaults to current repo
```

### Required Setup

Install GitHub CLI and authenticate:
```bash
brew install gh              # macOS
# or: sudo apt install gh    # Linux
# or: choco install gh       # Windows

gh auth login
```

### Usage Examples

#### Python API

```python
from core.nl_processor import process_request
from core.project_detector import detect_project_context
from core.github_poster import GitHubPoster

# Detect project context
context = detect_project_context("/path/to/project")

# Process natural language request
issue = await process_request("Add dark mode to my app", context)

# Post to GitHub (with confirmation)
poster = GitHubPoster()
issue_number = poster.post_issue(issue, confirm=True)
```

#### Project Context Detection

The system automatically detects:
- **Framework**: React, Vue, Next.js, Angular, Svelte, FastAPI, Django, Flask, Express, NestJS
- **Build Tools**: Vite, Webpack, Rollup, TypeScript, Babel, Docker
- **Package Manager**: npm, yarn, pnpm, bun, pip, uv, poetry, pipenv
- **Complexity**: Low, medium, or high based on project structure
- **Git Status**: Whether the project has git initialized

#### Workflow Recommendations

The system automatically recommends workflows based on issue type and complexity:

| Issue Type | Complexity | Workflow | Model Set |
|------------|-----------|----------|-----------|
| Feature | Low | `adw_sdlc_iso` | `base` |
| Feature | Medium | `adw_plan_build_test_iso` | `base` |
| Feature | High | `adw_plan_build_test_iso` | `heavy` |
| Bug | Any | `adw_plan_build_test_iso` | `base` |
| Chore | Any | `adw_sdlc_iso` | `base` |

### Module Documentation

#### Core Modules

1. **`core/nl_processor.py`**: Natural language processing using Claude API
   - `analyze_intent()`: Analyzes user intent and classifies issue type
   - `extract_requirements()`: Extracts technical requirements
   - `process_request()`: Main orchestration function

2. **`core/issue_formatter.py`**: Issue template formatting
   - `create_feature_issue_body()`: Formats feature issues
   - `create_bug_issue_body()`: Formats bug reports
   - `create_chore_issue_body()`: Formats chore tasks

3. **`core/project_detector.py`**: Project context detection
   - `detect_project_context()`: Analyzes project structure
   - `detect_framework()`: Identifies frontend framework
   - `detect_backend()`: Identifies backend framework
   - `calculate_complexity()`: Calculates project complexity

4. **`core/github_poster.py`**: GitHub CLI integration
   - `GitHubPoster.post_issue()`: Posts issue with preview
   - `GitHubPoster.format_preview()`: Rich terminal preview
   - `GitHubPoster.get_repo_info()`: Repository information

### Testing

Run the comprehensive test suite:

```bash
cd app/server

# Run all NL-to-issue tests
uv run pytest tests/core/test_nl_processor.py -v
uv run pytest tests/core/test_issue_formatter.py -v
uv run pytest tests/core/test_project_detector.py -v
uv run pytest tests/core/test_github_poster.py -v

# Run integration tests
uv run pytest tests/test_nl_workflow_integration.py -v

# Run all tests
uv run pytest
```

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