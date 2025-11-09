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
