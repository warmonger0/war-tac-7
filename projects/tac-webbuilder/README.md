# tac-webbuilder

Natural language interface for tac-7 AI Developer Workflows (ADW).

## Overview

`tac-webbuilder` is a tool within the tac-7 repository that enables users to interact with AI Developer Workflows using natural language. Instead of manually creating GitHub issues with specific markdown formatting and understanding ADW workflow syntax, users can describe what they want to build in plain language, and tac-webbuilder handles the translation to properly formatted GitHub issues and workflow triggers.

## Project Structure

```
tac-webbuilder/
├── README.md                 # This file
├── pyproject.toml           # Python project configuration
├── config.yaml.sample       # YAML configuration template
├── .env.sample              # Environment variables template
├── .gitignore               # Git ignore patterns
├── core/                    # Core configuration and utilities
│   ├── __init__.py
│   └── config.py           # Pydantic-based configuration management
├── interfaces/              # User-facing interfaces
│   ├── cli/                # Command-line interface (future)
│   └── web/                # Web interface (future)
├── adws/                    # AI Developer Workflows (copied from tac-7)
│   ├── adw_modules/        # Core ADW modules
│   ├── adw_*_iso.py        # Workflow scripts
│   ├── adw_triggers/       # Automation triggers
│   ├── adw_tests/          # Test utilities
│   └── README.md           # Complete ADW documentation
├── .claude/                 # Claude Code configuration
│   ├── commands/           # Slash commands
│   ├── hooks/              # Git hooks
│   └── settings.json       # Claude settings
├── templates/               # Issue and workflow templates
├── scripts/                 # Utility scripts
│   └── setup.sh            # Initial setup script
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

## Future Roadmap

tac-webbuilder is being developed in phases:

1. **✓ Issue 1 (Current)**: Project foundation and ADW integration
2. **Issue 2**: Natural language processing - Convert user input to GitHub issues
3. **Issue 3**: CLI interface - Terminal-based interactions
4. **Issue 4**: Web backend API - REST API for the web interface
5. **Issue 5**: Web frontend UI - Browser-based interface
6. **Issue 6**: Template system - Reusable templates for common workflows

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
