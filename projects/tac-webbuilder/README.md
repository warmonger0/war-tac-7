# tac-webbuilder

Natural language interface for tac-7 AI Developer Workflows (ADW).

## Overview

`tac-webbuilder` is a tool within the tac-7 repository that enables users to interact with AI Developer Workflows using natural language. Instead of manually creating GitHub issues with specific markdown formatting and understanding ADW workflow syntax, users can describe what they want to build in plain language, and tac-webbuilder handles the translation to properly formatted GitHub issues and workflow triggers.

### Available Interfaces

1. **CLI Interface** - Interactive terminal-based interface with rich formatting
2. **Web Backend API** - FastAPI REST API with WebSocket support for programmatic access

**Note:** A web frontend UI (browser-based interface) is planned but not yet implemented. The current web backend API can be consumed by any HTTP client or used to build a custom frontend.

## Project Structure

```
tac-webbuilder/
├── README.md                 # This file
├── pyproject.toml           # Python project configuration
├── uv.lock                  # Locked dependency versions
├── config.yaml              # YAML configuration (from config.yaml.sample)
├── config.yaml.sample       # YAML configuration template
├── .env                     # Environment variables (from .env.sample)
├── .env.sample              # Environment variables template
├── .gitignore               # Git ignore patterns
├── core/                    # Core configuration and utilities
│   ├── __init__.py
│   └── config.py           # Pydantic-based configuration management
├── interfaces/              # User-facing interfaces
│   ├── cli/                # Command-line interface (IMPLEMENTED)
│   │   ├── __init__.py
│   │   ├── __main__.py     # CLI entry point
│   │   ├── main.py         # Main CLI logic
│   │   ├── commands.py     # Command implementations
│   │   ├── interactive.py  # Interactive mode
│   │   ├── config_manager.py # CLI configuration
│   │   ├── history.py      # Request history tracking
│   │   └── output.py       # Output formatting
│   └── web/                # Web backend API (IMPLEMENTED)
│       ├── __init__.py
│       ├── server.py       # FastAPI application
│       ├── models.py       # Pydantic models
│       ├── state.py        # Request state management
│       ├── websocket.py    # WebSocket manager
│       ├── workflow_monitor.py # ADW monitoring
│       └── routes/         # API route modules
│           ├── __init__.py
│           ├── requests.py # Request submission
│           ├── workflows.py # Workflow monitoring
│           ├── projects.py # Project management
│           └── history.py  # History endpoints
├── adws/                    # AI Developer Workflows (copied from tac-7)
│   ├── adw_modules/        # Core ADW modules
│   │   ├── agent.py        # Agent execution
│   │   ├── workflow_ops.py # Workflow operations
│   │   ├── git_ops.py      # Git operations
│   │   ├── github.py       # GitHub API integration
│   │   ├── worktree_ops.py # Git worktree management
│   │   ├── state.py        # Workflow state
│   │   ├── data_types.py   # Data type definitions
│   │   ├── utils.py        # Utility functions
│   │   └── r2_uploader.py  # R2 artifact uploads
│   ├── adw_*_iso.py        # Workflow scripts
│   │   ├── adw_sdlc_iso.py # Full SDLC workflow
│   │   ├── adw_sdlc_zte_iso.py # Zero-test-error SDLC
│   │   ├── adw_plan_build_test_iso.py
│   │   ├── adw_plan_build_iso.py
│   │   ├── adw_build_iso.py
│   │   ├── adw_test_iso.py
│   │   ├── adw_review_iso.py
│   │   ├── adw_ship_iso.py
│   │   ├── adw_document_iso.py
│   │   └── adw_patch_iso.py
│   ├── adw_triggers/       # Automation triggers
│   │   ├── trigger_webhook.py # Webhook trigger
│   │   └── trigger_cron.py    # Scheduled trigger
│   ├── adw_tests/          # Test utilities
│   └── README.md           # Complete ADW documentation
├── .claude/                 # Claude Code configuration
│   ├── commands/           # Slash commands
│   │   ├── e2e/           # E2E test commands
│   │   │   ├── test_cli_interface.md
│   │   │   └── test_web_api.md
│   │   └── ... (setup, test, feature commands)
│   ├── hooks/              # Git hooks
│   └── settings.json       # Claude settings
├── templates/               # Issue and workflow templates
│   └── issue_template.md  # GitHub issue template
├── docs/                    # Documentation
│   ├── api/                # API documentation
│   │   └── nl-processing.md # NL processing API reference
│   ├── guides/             # Usage guides
│   │   └── nl-processing-guide.md # NL processing usage guide
│   ├── architecture/       # Architecture documentation
│   │   └── nl-processing-architecture.md # System architecture
│   └── playwright-mcp.md  # Playwright MCP integration guide
├── examples/                # Example code
│   └── nl-processing/      # NL processing examples
│       ├── README.md       # Examples overview
│       ├── basic_usage.py  # Basic usage example
│       ├── advanced_usage.py # Advanced usage example
│       ├── edge_cases.py   # Edge cases example
│       ├── example_inputs.json # Sample inputs
│       └── example_outputs.json # Sample outputs
├── scripts/                 # Utility scripts
│   ├── setup.sh            # Initial setup script
│   ├── start_cli.sh        # Start CLI interface
│   ├── start_web.sh        # Start web backend API
│   └── validate_adw.py     # ADW validation
├── tests/                   # Test suite
│   ├── conftest.py         # Pytest configuration
│   ├── test_config.py      # Configuration tests
│   ├── core/               # Core module tests
│   │   └── test_mcp_setup.py
│   └── interfaces/         # Interface tests
│       ├── test_cli_main.py
│       ├── test_commands.py
│       ├── test_interactive.py
│       ├── test_config_manager.py
│       ├── test_history.py
│       ├── test_output.py
│       └── web/            # Web API tests
│           ├── test_server.py
│           ├── test_models.py
│           ├── test_state.py
│           ├── test_requests_routes.py
│           └── test_workflows_routes.py
├── logs/                    # Runtime logs (gitignored)
├── agents/                  # Agent execution artifacts (gitignored)
└── trees/                   # Worktree isolation (gitignored)
```

## Architecture

### Relationship to tac-7

tac-webbuilder lives within the tac-7 repository under `projects/` but maintains its own:
- Directory structure and codebase
- Configuration system (YAML + environment variables)
- Python virtual environment (managed by `uv`)
- Complete copy of the ADW system for independent evolution

This architecture allows tac-webbuilder to leverage tac-7's proven ADW infrastructure while developing as an independent tool with its own roadmap.

## Prerequisites

- **Python 3.10+**: Required for running tac-webbuilder
- **uv**: Python package manager - [Install uv](https://github.com/astral-sh/uv)
- **gh** (optional): GitHub CLI for authentication - [Install gh](https://cli.github.com/)
- **claude** (optional): Claude Code CLI for workflow execution - [Install Claude Code](https://docs.claude.com/)

## Quick Start

### 1. Initial Setup

Run the setup script to configure your environment:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
bash scripts/setup.sh
```

This script will:
- Check for required tools
- Create `.env` and `config.yaml` from sample files
- Install Python dependencies
- Verify GitHub authentication

### 2. Configuration

#### Option A: YAML Configuration (Recommended)

Edit `config.yaml` with your settings:

```yaml
github:
  default_repo: "yourusername/your-repo"
  auto_post: false

adw:
  default_workflow: "adw_sdlc_iso"
  default_model_set: "base"

interfaces:
  cli:
    enabled: true
  web:
    enabled: true
    port: 5174
```

#### Option B: Environment Variables

Edit `.env` with your credentials:

```bash
TWB_GITHUB_REPO_URL="https://github.com/yourusername/your-repo"
TWB_GITHUB_PAT="ghp_xxxxxxxxxxxx"
TWB_CLAUDE_API_KEY="sk-ant-xxxxxxxxxxxx"
```

**Note:** Environment variables override YAML settings.

### 3. Verify Installation

Test that configuration loads correctly:

```bash
uv run python -c "from core.config import load_config; config = load_config(); print('Config loaded successfully!')"
```

Test that ADW modules are importable:

```bash
uv run python -c "from adws.adw_modules.agent import Agent; print('ADW modules loaded successfully!')"
```

### 4. Choose Your Interface

tac-webbuilder provides two interfaces for interacting with AI Developer Workflows:

#### Option A: CLI Interface (Terminal)

Start the interactive CLI:

```bash
./scripts/start_cli.sh
```

Or run one-off commands:

```bash
# Submit a request
uv run python -m interfaces.cli submit "Add dark mode to settings page" --project /path/to/project

# View history
uv run python -m interfaces.cli history

# Check status of workflows
uv run python -m interfaces.cli status
```

See [CLI Interface Documentation](#cli-interface) for full details.

#### Option B: Web Backend API (Programmatic)

Start the FastAPI backend server:

```bash
./scripts/start_web.sh
```

Access the API at:
- **API Documentation**: http://localhost:8002/docs (Swagger UI)
- **API Base**: http://localhost:8002
- **WebSocket**: ws://localhost:8002/ws

See [Web Backend API Documentation](#web-backend-api) for full details.

**Note:** A web frontend UI is planned but not yet implemented. The web backend provides a REST API that can be consumed by any HTTP client or used to build a custom frontend.

## Natural Language Processing

tac-webbuilder includes a powerful Natural Language (NL) Processing system that converts plain English descriptions into structured GitHub issues with automatic ADW workflow recommendations. This is the core feature that enables you to simply describe what you want, and the system handles the rest.

### How It Works

1. **Intent Analysis**: The system uses Claude API to understand your request type (feature, bug, or chore)
2. **Requirement Extraction**: Breaks down your description into actionable technical requirements
3. **Project Detection**: Analyzes your project structure to determine frameworks, tools, and complexity
4. **Issue Generation**: Creates properly formatted GitHub issues with appropriate ADW workflows
5. **GitHub Integration**: Posts issues directly to GitHub with preview and confirmation

### Quick Example

```python
import asyncio
from app.server.core.nl_processor import process_request
from app.server.core.project_detector import detect_project_context
from app.server.core.github_poster import GitHubPoster

async def main():
    # Detect your project context
    context = detect_project_context("/path/to/your/project")

    # Process natural language request
    issue = await process_request(
        "Add a dark mode toggle to the settings page",
        context
    )

    # Post to GitHub
    poster = GitHubPoster()
    issue_number = poster.post_issue(issue, confirm=True)
    print(f"Created issue #{issue_number}")

asyncio.run(main())
```

### Supported Project Types

The system automatically detects and adapts to:

- **Frontend**: React, Vue, Next.js, Angular, Svelte
- **Backend**: FastAPI, Django, Flask, Express, NestJS
- **Build Tools**: Vite, Webpack, TypeScript, Docker
- **Package Managers**: npm, yarn, pnpm, bun, pip, uv, poetry

### Workflow Recommendations

The system automatically recommends ADW workflows based on issue type and project complexity:

| Issue Type | Complexity | Workflow | Model Set |
|------------|-----------|----------|-----------|
| Feature | Low | `adw_sdlc_iso` | `base` |
| Feature | Medium | `adw_plan_build_test_iso` | `base` |
| Feature | High | `adw_plan_build_test_iso` | `heavy` |
| Bug | Any | `adw_plan_build_test_iso` | `base` |
| Chore | Any | `adw_sdlc_iso` | `base` |

### Setup Requirements

1. **Set ANTHROPIC_API_KEY**:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
   ```

2. **Authenticate with GitHub CLI** (for posting issues):
   ```bash
   gh auth login
   ```

### Documentation

- **[API Reference](docs/api/nl-processing.md)** - Complete API documentation for all NL processing modules
- **[Usage Guide](docs/guides/nl-processing-guide.md)** - Step-by-step guide with examples and best practices
- **[Architecture](docs/architecture/nl-processing-architecture.md)** - System design and component diagrams
- **[Examples](examples/nl-processing/README.md)** - Working code examples and edge cases

### Example Inputs

Here are some example natural language inputs the system can process:

**Feature Requests:**
```
"Add a dark mode toggle to the settings page"
"Implement user authentication with JWT tokens"
"Build a real-time chat feature with WebSockets"
```

**Bug Reports:**
```
"Login button doesn't respond when clicked"
"Dashboard page loads slowly (5+ seconds)"
"User passwords are stored in plain text"
```

**Chores:**
```
"Update API documentation for authentication endpoints"
"Refactor user service to use dependency injection"
"Add unit tests for authentication service"
```

### Try It Out

Run the basic example:
```bash
cd examples/nl-processing
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
python basic_usage.py
```

This will:
1. Detect project context
2. Process a sample natural language request
3. Display the generated GitHub issue
4. Optionally post to GitHub

## Configuration

### Configuration Precedence

1. **Environment Variables** (highest priority)
2. **config.yaml** file
3. **Default values** (lowest priority)

### Environment Variable Naming

All environment variables use the prefix `TWB_` (tac-webbuilder):

- GitHub: `TWB_GITHUB_*`
- Claude: `TWB_CLAUDE_*`
- ADW: `TWB_ADW_*`
- Interfaces: `TWB_INTERFACES__WEB__PORT` (note double underscore for nesting)

### Required Configuration

At minimum, you need:

- `TWB_GITHUB_PAT` or `github.pat` in config.yaml
- `TWB_GITHUB_DEFAULT_REPO` or `github.default_repo` in config.yaml
- `TWB_CLAUDE_API_KEY` or `claude.api_key` in config.yaml

## AI Developer Workflows (ADW)

tac-webbuilder includes a complete copy of tac-7's ADW system. For comprehensive documentation on ADW concepts, workflows, and usage, see:

- [ADW README](adws/README.md) - Complete ADW documentation within this project
- [tac-7 ADW README](/Users/Warmonger0/tac/tac-7/adws/README.md) - Original tac-7 documentation

### Available Workflows

- `adw_sdlc_iso` - Full SDLC workflow (plan → build → test → document → ship)
- `adw_sdlc_zte_iso` - Zero-test-error SDLC workflow
- `adw_plan_build_test_iso` - Plan, build, and test workflow
- `adw_plan_build_iso` - Plan and build workflow
- `adw_build_iso` - Build only
- And more - see [ADW README](adws/README.md)

## CLI Interface

tac-webbuilder provides a command-line interface for terminal-based interaction with AI Developer Workflows. The CLI supports both interactive mode and one-off commands.

### Quick Start

Start the interactive CLI:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_cli.sh
```

Or run commands directly:

```bash
# Submit a request
uv run python -m interfaces.cli submit "Add dark mode toggle to settings" --project /path/to/project

# View request history
uv run python -m interfaces.cli history

# Check workflow status
uv run python -m interfaces.cli status

# Show configuration
uv run python -m interfaces.cli config
```

### Interactive Mode

The interactive CLI provides a conversational interface:

```bash
$ ./scripts/start_cli.sh

Welcome to tac-webbuilder CLI!
Connected to: yourusername/your-repo

> What would you like to build?
Add a dark mode toggle to the settings page

> Project path (or press Enter for current directory):
/Users/me/projects/my-app

[Analyzing project...]
[Generating GitHub issue...]

Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title: Add dark mode toggle to settings page

## Description
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> Post to GitHub? [y/N]: y

✓ Issue created: #42
✓ ADW workflow triggered
Monitor progress at: http://localhost:8002/api/workflows/adw-abc123
```

### Features

- **Interactive mode**: Conversational interface for submitting requests
- **Command mode**: Run one-off commands without interaction
- **Request history**: View past requests and their status
- **Configuration management**: View and update CLI settings
- **Workflow monitoring**: Check status of running ADW workflows
- **Project context**: Automatic detection of project type and tech stack
- **Rich output**: Color-coded, formatted output using Rich library

### Configuration

Configure the CLI via `config.yaml`:

```yaml
interfaces:
  cli:
    enabled: true
    auto_confirm: false  # Auto-post to GitHub without confirmation
    default_project: "/path/to/default/project"
    history_limit: 50    # Number of history items to keep
```

Or via environment variables:

```bash
TWB_INTERFACES__CLI__ENABLED=true
TWB_INTERFACES__CLI__AUTO_CONFIRM=false
TWB_INTERFACES__CLI__DEFAULT_PROJECT=/path/to/project
```

### Testing

Run CLI tests:

```bash
# Run all CLI tests
uv run pytest tests/interfaces/test_cli_main.py -v

# Test specific features
uv run pytest tests/interfaces/test_commands.py -v
uv run pytest tests/interfaces/test_interactive.py -v
uv run pytest tests/interfaces/test_history.py -v
```

### Troubleshooting

#### Command Not Found

Make sure you're in the correct directory and the virtual environment is activated:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_cli.sh
```

#### Configuration Errors

Check that your configuration is valid:

```bash
uv run python -m interfaces.cli config
```

## Web Backend API

tac-webbuilder provides a FastAPI-based web backend that powers the web interface with REST API endpoints and WebSocket support for real-time updates.

### Quick Start

Start the web backend server:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_web.sh
```

The API will be available at:
- **API Base**: http://localhost:8002
- **API Documentation**: http://localhost:8002/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8002/redoc (ReDoc)
- **Health Check**: http://localhost:8002/api/health
- **WebSocket**: ws://localhost:8002/ws

### Configuration

Configure the web backend via environment variables or config.yaml:

```bash
# Environment variables
TWB_WEB_BACKEND_HOST=0.0.0.0          # Listen address (default: 0.0.0.0)
TWB_WEB_BACKEND_PORT=8002             # API port (default: 8002)
TWB_FRONTEND_ORIGIN=http://localhost:5174  # CORS allowed origin
```

```yaml
# config.yaml
interfaces:
  web:
    enabled: true
    port: 5174  # Frontend port (backend runs on 8002)
```

### API Endpoints

#### Health & Info
- `GET /api/health` - Health check endpoint
- `GET /` - API root with links to documentation

#### Requests (Issue Creation)
- `POST /api/request` - Submit NL request and get preview
- `GET /api/preview/{request_id}` - Get formatted GitHub issue preview
- `POST /api/confirm/{request_id}` - Confirm and post issue to GitHub

#### Workflows (ADW Monitoring)
- `GET /api/workflows` - List active ADW workflows
- `GET /api/workflows/{adw_id}` - Get detailed workflow status and logs

#### Projects (Context Detection)
- `GET /api/projects` - List configured projects
- `POST /api/projects` - Add new project and detect context
- `GET /api/projects/{project_id}/context` - Get project context

#### History
- `GET /api/history` - Get request history with pagination

### API Usage Examples

#### Submit a Request
```bash
curl -X POST http://localhost:8002/api/request \
  -H "Content-Type: application/json" \
  -d '{
    "nl_input": "Add a dark mode toggle to the settings page",
    "project_path": "/path/to/project"
  }'
```

**Response:**
```json
{
  "request_id": "abc-123",
  "github_issue": {
    "title": "Add a dark mode toggle to the settings page",
    "body": "## Description\n...",
    "labels": ["tac-webbuilder", "enhancement"]
  },
  "project_context": {
    "project_name": "my-project",
    "language": "Python",
    "framework": "FastAPI"
  }
}
```

#### List Workflows
```bash
curl http://localhost:8002/api/workflows
```

**Response:**
```json
{
  "workflows": [
    {
      "adw_id": "adw-xyz",
      "issue_number": 42,
      "current_phase": "build",
      "status": "running",
      "started_at": "2025-11-09T10:00:00",
      "pr_url": null
    }
  ],
  "total_count": 1
}
```

#### Add a Project
```bash
curl -X POST http://localhost:8002/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/Users/me/projects/my-app"
  }'
```

**Response:**
```json
{
  "project_path": "/Users/me/projects/my-app",
  "project_name": "my-app",
  "framework": "React",
  "language": "TypeScript",
  "tech_stack": ["Node.js"],
  "build_tools": ["npm"],
  "test_frameworks": ["vitest"],
  "has_git": true,
  "repo_url": "https://github.com/user/my-app"
}
```

### WebSocket Real-time Updates

Connect to the WebSocket endpoint for real-time workflow updates:

```javascript
const ws = new WebSocket('ws://localhost:8002/ws');

ws.onopen = () => {
  console.log('Connected to tac-webbuilder API');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message.type, message.data);

  switch (message.type) {
    case 'workflow_started':
      console.log('Workflow started:', message.data.adw_id);
      break;
    case 'workflow_progress':
      console.log('Progress:', message.data.phase, message.data.status);
      break;
    case 'workflow_completed':
      console.log('PR created:', message.data.pr_url);
      break;
  }
};
```

**Message Types:**
- `workflow_started` - New workflow execution began
- `workflow_progress` - Phase progress update
- `workflow_completed` - Workflow finished successfully
- `workflow_failed` - Workflow encountered an error

### Testing the API

#### Unit Tests
```bash
# Run web API tests
uv run pytest tests/interfaces/web/ -v

# With coverage
uv run pytest tests/interfaces/web/ --cov=interfaces.web
```

#### E2E Tests
```bash
# Follow the E2E test guide
cat .claude/commands/e2e/test_web_api.md

# Or run individual curl commands
curl http://localhost:8002/api/health
```

### Troubleshooting

#### Port Already in Use
```bash
# Kill process on port 8002
lsof -ti:8002 | xargs kill -9

# Or use the startup script (it handles this automatically)
./scripts/start_web.sh
```

#### CORS Errors
Make sure your frontend origin is configured:
```bash
export TWB_FRONTEND_ORIGIN=http://localhost:5174
./scripts/start_web.sh
```

#### WebSocket Connection Refused
Check that the server is running and accessible:
```bash
curl http://localhost:8002/api/health
```

### Development

The web API is built with:
- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server with WebSocket support
- **Pydantic**: Data validation and serialization
- **WebSockets**: Real-time bidirectional communication

Project structure:
```
interfaces/web/
├── server.py           # Main FastAPI application
├── models.py           # Pydantic request/response models
├── state.py            # Request state management
├── websocket.py        # WebSocket connection manager
├── workflow_monitor.py # ADW workflow monitoring
└── routes/
    ├── requests.py     # Request submission routes
    ├── workflows.py    # Workflow monitoring routes
    ├── projects.py     # Project management routes
    └── history.py      # Request history routes
```

## Playwright MCP Integration

tac-webbuilder includes Playwright Model Context Protocol (MCP) integration that enables Claude Code to control browsers programmatically for testing and validation.

### Key Capabilities

- **Browser Control**: Navigate, interact with elements, and test workflows automatically
- **E2E Testing**: Run end-to-end tests with real browser automation
- **Visual Validation**: Capture screenshots and videos for review
- **Multi-Browser Support**: Test with Chromium, Firefox, or WebKit
- **ADW Integration**: Automatically used in ADW workflow testing and review phases

### Quick Start

```bash
# Copy MCP configuration
cp .mcp.json.sample .mcp.json

# Install Playwright
npm install -D playwright
npx playwright install chromium
```

The Playwright MCP server will start automatically when Claude Code runs.

### Documentation

For comprehensive documentation on configuration, usage, troubleshooting, and best practices, see [Playwright MCP Documentation](docs/playwright-mcp.md).

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=core --cov=interfaces

# Run specific test file
uv run pytest tests/test_config.py -v
```

### Adding Dependencies

```bash
# Add a production dependency
uv add package-name

# Add a development dependency
uv add --dev package-name
```

### Project Layout

- `core/` - Configuration management and shared utilities
- `interfaces/` - User-facing interfaces (CLI and web)
- `adws/` - Complete ADW system (modules, scripts, triggers, tests)
- `templates/` - Issue and workflow templates
- `scripts/` - Utility scripts for setup and maintenance
- `tests/` - Test suite

## Roadmap & Status

tac-webbuilder has been developed in phases:

1. **✓ Issue 1 - COMPLETED**: Project foundation and ADW integration
2. **✓ Issue 2 - COMPLETED**: Natural language processing - Convert user input to GitHub issues
3. **✓ Issue 3 - COMPLETED**: CLI interface - Terminal-based interactions
4. **✓ Issue 4 - COMPLETED**: Web backend API - REST API for the web interface
5. **Issue 5 - PLANNED**: Web frontend UI - Browser-based interface (React/Vue/Svelte)
6. **✓ Issue 6 - COMPLETED**: Template system - Reusable templates for common workflows
7. **✓ Issue 7 - COMPLETED**: Playwright MCP Integration - Browser automation for testing
8. **✓ Issue 8 - COMPLETED**: Environment setup and configuration documentation

### Current Status

**Implemented Features:**
- ✅ Core configuration system (YAML + env variables)
- ✅ CLI interface with interactive mode
- ✅ Web backend API (FastAPI + WebSocket)
- ✅ Natural language request processing
- ✅ GitHub issue creation and preview
- ✅ ADW workflow monitoring
- ✅ Project context detection
- ✅ Request history tracking
- ✅ Playwright MCP integration
- ✅ Comprehensive test suite

**Not Yet Implemented:**
- ❌ Web frontend UI (planned for future development)
- ❌ Mobile interface

## Troubleshooting

### Configuration Not Loading

```bash
# Check that config file exists
ls -la config.yaml

# Verify environment variables
env | grep TWB_

# Test configuration loading
uv run python -c "from core.config import load_config; config = load_config(); print(config)"
```

### ADW Modules Import Errors

```bash
# Verify ADW modules were copied correctly
ls -la adws/adw_modules/

# Test imports
uv run python -c "from adws.adw_modules.agent import Agent; print('Success')"
```

### GitHub Authentication Issues

```bash
# Check gh authentication
gh auth status

# Re-authenticate if needed
gh auth login
```

## Contributing

tac-webbuilder follows the same development workflow as tac-7:

1. Create a GitHub issue describing the feature or bug
2. Use ADW workflows to implement the feature
3. Follow the test-driven development approach
4. Submit PRs with comprehensive documentation

## License

Same license as tac-7.

## Links

- [tac-7 Main README](/Users/Warmonger0/tac/tac-7/README.md)
- [ADW Documentation](adws/README.md)
- [Claude Code Documentation](https://docs.claude.com/)
