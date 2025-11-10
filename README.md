# tac-webbuilder

Build web applications with natural language using the ADW (Autonomous Development Workflow) system.

## What is tac-webbuilder?

tac-webbuilder is a natural language interface for web development that transforms your feature requests into working code. It provides:

- 🗣️ **Natural Language Interface** - Describe features in plain English
- 🤖 **Automated Implementation** - ADW workflow handles planning, coding, testing, and review
- 🎨 **Project Templates** - Start new projects with React, Next.js, or Vanilla JavaScript
- 🔗 **Existing Code Integration** - Add ADW to any existing web application
- 💻 **Dual Interface** - Use CLI for speed or Web UI for visualization
- ✅ **Complete Automation** - From feature request to merged PR

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ or Bun
- uv (Python package manager)
- GitHub CLI (`gh`)
- Git

### Installation

```bash
cd /path/to/tac-webbuilder
uv sync
cp .env.sample .env
# Edit .env and add your API keys
```

### Configuration

Add to `.env`:

```env
# Required
ANTHROPIC_API_KEY=your-anthropic-key
GITHUB_TOKEN=your-github-token

# Optional
GITHUB_REPO_URL=https://github.com/owner/repo
API_URL=http://localhost:8002
LOG_LEVEL=INFO
```

Get GitHub token:
```bash
gh auth login
gh auth token
```

### Use the CLI

```bash
# Interactive mode
./scripts/start_cli.sh interactive

# Direct request
./scripts/start_cli.sh request "Add dark mode toggle"

# Create new project from template
./scripts/start_cli.sh new my-app --framework react-vite

# Integrate into existing app
./scripts/start_cli.sh integrate /path/to/existing/app
```

### Use the Web UI

```bash
# Start both backend and frontend
./scripts/start_web_full.sh

# Or start separately:
# Terminal 1: Backend
./scripts/start_web_backend.sh

# Terminal 2: Frontend
./scripts/start_web_frontend.sh
```

Then open [http://localhost:5174](http://localhost:5174) in your browser.

## Features

### Natural Language Requests

Describe what you want to build in plain English:

**Authentication:**
```
Add user authentication with:
- Email/password signup and login
- OAuth providers (Google, GitHub)
- Password reset via email
- Session management with JWT
- Protected routes
```

**UI Components:**
```
Add a dark mode toggle that:
- Switches between light and dark themes
- Persists preference in localStorage
- Includes smooth transitions
- Updates all components
```

**Data Features:**
```
Create an analytics dashboard with:
- Line chart for user growth
- Bar chart for revenue
- Real-time updates via WebSocket
- Export to CSV
```

See [docs/examples.md](docs/examples.md) for 30+ more examples.

### Automatic Implementation

ADW workflow handles:

1. **Planning** - Analyzes request and creates technical specification
2. **Implementation** - Writes code following best practices
3. **Testing** - Generates and runs unit and E2E tests
4. **Review** - Creates pull request with description
5. **Documentation** - Updates relevant docs
6. **Merge** - Auto-merges after successful review (optional)

### Dual Interface

**CLI Interface:**
- Fast workflow for developers
- Interactive and non-interactive modes
- Request history management
- Configuration commands
- Scriptable and automatable

**Web UI:**
- Visual, user-friendly interface
- Real-time workflow monitoring
- Issue preview before posting
- Request history with filtering
- WebSocket live updates

### Project Templates

Start new projects with pre-configured templates:

**React + Vite:**
- React 18 with TypeScript
- Vite for fast development
- Vitest for testing
- ESLint and proper tooling
- ADW pre-configured

**Next.js:**
- Next.js 14 with App Router
- Server and Client Components
- API routes ready
- Jest for testing
- ADW pre-configured

**Vanilla JavaScript:**
- Plain HTML/CSS/JS
- No build step
- Simple structure
- Great for learning
- ADW-ready

**Create a new project:**
```bash
./scripts/setup_new_project.sh my-app react-vite
cd /Users/Warmonger0/tac/my-app
npm run dev
```

### Existing Codebase Integration

Integrate ADW into any existing web application:

```bash
./scripts/integrate_existing.sh /path/to/your/app
```

This will:
- Detect your framework automatically
- Create GitHub issue with integration plan
- Let ADW implement integration
- Add `.claude/` configuration
- Set up environment variables
- Create project-specific slash commands

Supports: React, Next.js, Vue, Svelte, FastAPI, Express, Django, Flask, and more.

See [templates/existing_webapp/integration_guide.md](templates/existing_webapp/integration_guide.md) for details.

## Architecture

```
┌─────────────┐     ┌─────────────┐
│     CLI     │     │   Web UI    │
│  (Python)   │     │   (React)   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └───────┬───────────┘
               │
        ┌──────▼──────┐
        │  Backend    │
        │  (FastAPI)  │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
┌───▼───┐  ┌──▼──┐  ┌────▼────┐
│GitHub │  │ ADW │  │ Project │
│  API  │  │     │  │Detection│
└───────┘  └─────┘  └─────────┘
```

### Components

- **CLI** - Command-line interface for developers
- **Web UI** - React + TypeScript + Vite frontend
- **Backend** - FastAPI server with WebSocket support
- **NL Processor** - Natural language parsing and analysis
- **GitHub Poster** - Issue creation and management
- **Project Detector** - Framework and structure detection
- **ADW Integration** - Workflow triggering and monitoring

See [docs/architecture.md](docs/architecture.md) for detailed architecture.

## Documentation

- **[CLI Reference](docs/cli.md)** - Complete CLI command reference
- **[Web UI Guide](docs/web-ui.md)** - Using the web interface
- **[API Documentation](docs/api.md)** - Backend API reference
- **[Architecture](docs/architecture.md)** - System design and data flow
- **[Example Requests](docs/examples.md)** - 30+ example natural language requests
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions
- **[Integration Guide](templates/existing_webapp/integration_guide.md)** - Integrate into existing projects
- **[ADW Workflows](adws/README.md)** - ADW system documentation

## Project Structure

```
.
├── app/
│   ├── client/              # React + Vite frontend
│   │   ├── src/
│   │   │   ├── components/  # UI components
│   │   │   ├── api/         # API client
│   │   │   └── App.tsx      # Main app
│   │   └── package.json
│   │
│   └── server/              # FastAPI backend
│       ├── core/
│       │   ├── nl_processor.py      # Natural language processing
│       │   ├── github_poster.py     # GitHub integration
│       │   ├── project_detector.py  # Framework detection
│       │   └── workflow_manager.py  # ADW workflow management
│       ├── routers/         # API endpoints
│       ├── models/          # Data models
│       └── main.py          # FastAPI app
│
├── templates/               # Project templates
│   ├── new_webapp/
│   │   ├── react-vite/     # React + Vite template
│   │   ├── nextjs/         # Next.js template
│   │   └── vanilla/        # Vanilla JS template
│   ├── existing_webapp/
│   │   └── integration_guide.md
│   └── template_structure.json
│
├── scripts/                 # Utility scripts
│   ├── setup_new_project.sh        # Create new project
│   ├── integrate_existing.sh       # Integrate into existing
│   ├── start_cli.sh                # Start CLI
│   ├── start_web_full.sh           # Start full web stack
│   ├── start_web_backend.sh        # Start backend only
│   └── start_web_frontend.sh       # Start frontend only
│
├── docs/                    # Documentation
│   ├── cli.md              # CLI reference
│   ├── web-ui.md           # Web UI guide
│   ├── api.md              # API reference
│   ├── architecture.md     # System architecture
│   ├── examples.md         # Example requests
│   └── troubleshooting.md  # Troubleshooting guide
│
├── adws/                    # ADW workflow system
├── specs/                   # Feature specifications
├── tests/                   # Test suite
└── .claude/                 # Claude Code configuration
```

## API Endpoints

**Request Management:**
- `POST /api/request` - Create a new feature request
- `POST /api/preview` - Preview issue without posting
- `POST /api/confirm` - Confirm and post previewed issue
- `GET /api/history` - Get request history

**Project Detection:**
- `POST /api/detect` - Detect project framework and structure
- `GET /api/repos` - List accessible GitHub repositories

**Workflow Management:**
- `GET /api/workflow/{issue_number}` - Get workflow status
- `POST /api/workflow/{issue_number}/cancel` - Cancel workflow

**WebSocket:**
- `ws://localhost:8002/ws` - Real-time updates

See [docs/api.md](docs/api.md) for complete API reference with examples.

## CLI Commands

```bash
# Create a request
./scripts/start_cli.sh request "Add feature X"

# Interactive mode
./scripts/start_cli.sh interactive

# View history
./scripts/start_cli.sh history
./scripts/start_cli.sh history --limit 10 --filter react

# Configuration
./scripts/start_cli.sh config set default_repo owner/repo
./scripts/start_cli.sh config list

# New project from template
./scripts/start_cli.sh new myapp --framework react-vite

# Integrate into existing project
./scripts/start_cli.sh integrate /path/to/app
```

See [docs/cli.md](docs/cli.md) for complete CLI reference.

## ADW Workflows

The ADW (Autonomous Development Workflow) system automates the entire development lifecycle:

### Supported Workflows

- `adw_sdlc_zte_iso` - Full SDLC with zero-touch execution
- `adw_plan_build_test_iso` - Plan, build, and test workflow
- `adw_sdlc_iso` - Standard SDLC workflow

### Workflow Selection

ADW automatically selects the appropriate workflow based on:
- Issue complexity (low, medium, high)
- Issue type (feature, bug, chore)
- Project structure and size
- Test coverage requirements

### Monitoring Workflows

**Via Web UI:**
- Real-time progress updates
- Stage indicators (planning → implementing → testing → review)
- Live log streaming
- Error notifications

**Via CLI:**
```bash
# Check workflow status
./scripts/start_cli.sh workflow status <issue-number>

# View workflow logs
./scripts/start_cli.sh workflow logs <issue-number>
```

See [adws/README.md](adws/README.md) for detailed ADW documentation.

## Testing

### Run All Tests

```bash
cd app/server
uv run pytest -v
```

### Test Specific Modules

```bash
# Natural language processing
uv run pytest tests/core/test_nl_processor.py -v

# Project detection
uv run pytest tests/core/test_project_detector.py -v

# GitHub integration
uv run pytest tests/core/test_github_poster.py -v

# Template scaffolding
uv run pytest tests/templates/ -v
```

### Frontend Tests

```bash
cd app/client
bun test
bun run test:ui
```

## Example Workflows

### 1. Create New App and Add Features

```bash
# Create new React app
./scripts/setup_new_project.sh my-dashboard react-vite

# Navigate to app
cd /Users/Warmonger0/tac/my-dashboard

# Add authentication feature
cd /path/to/tac-webbuilder
./scripts/start_cli.sh request "Add user authentication with email/password" \
  --repo myorg/my-dashboard

# Add dashboard
./scripts/start_cli.sh request "Create analytics dashboard with charts" \
  --repo myorg/my-dashboard
```

### 2. Integrate ADW into Existing App

```bash
# Integrate ADW
./scripts/integrate_existing.sh ~/projects/existing-app

# Wait for integration PR
# Review and merge PR

# Now use natural language for features
./scripts/start_cli.sh request "Add dark mode" \
  --project ~/projects/existing-app
```

### 3. Use Web UI for Team Collaboration

```bash
# Start web UI
./scripts/start_web_full.sh

# Team members can:
# - Create requests via web form
# - Monitor workflow progress
# - View request history
# - Share request links
# - Get desktop notifications
```

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Must be 3.10+

# Check dependencies
cd app/server && uv sync

# Check environment variables
cat .env | grep -E "ANTHROPIC_API_KEY|GITHUB_TOKEN"
```

**GitHub authentication failed:**
```bash
# Authenticate with GitHub CLI
gh auth login

# Get token for .env
gh auth token
```

**Cannot create project from template:**
```bash
# Verify templates exist
ls -la templates/new_webapp/

# Check permissions
chmod +x scripts/setup_new_project.sh

# Try with full path
./scripts/setup_new_project.sh myapp react-vite /full/path
```

**ADW workflow not triggering:**
- Check issue has correct labels
- Verify webhook is configured
- Ensure repository has GitHub remote
- Check ADW system is running

See [docs/troubleshooting.md](docs/troubleshooting.md) for comprehensive troubleshooting.

## Security

### Best Practices

- **API Keys** - Never commit `.env` files
- **GitHub Token** - Use tokens with minimal required permissions
- **CORS** - Configured for local development only
- **Input Validation** - All inputs validated before processing
- **SQL Injection** - Parameterized queries and validation
- **Rate Limiting** - API endpoints are rate-limited

### Production Considerations

- Use environment-specific API keys
- Enable HTTPS for all communications
- Configure CORS for production domains
- Set up proper logging and monitoring
- Use secrets management (not .env files)
- Enable GitHub webhook authentication

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

Or use tac-webbuilder itself to contribute:
```bash
./scripts/start_cli.sh request "Add feature Y to tac-webbuilder" \
  --repo owner/tac-webbuilder
```

## Related Projects

- **[tac-7](https://github.com/owner/tac-7)** - Original ADW workflow implementation
- **[Claude Code](https://claude.com/claude-code)** - AI-powered coding assistant
- **[Anthropic](https://www.anthropic.com)** - Claude AI provider

## License

[Your License Here]

## Support

- **Documentation** - See [docs/](docs/) directory
- **Issues** - [GitHub Issues](https://github.com/owner/tac-webbuilder/issues)
- **Examples** - [docs/examples.md](docs/examples.md)
- **Troubleshooting** - [docs/troubleshooting.md](docs/troubleshooting.md)

---

**Built with ❤️ using Claude Code and ADW workflows**
