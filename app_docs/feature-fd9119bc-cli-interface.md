# CLI Interface Specification for tac-webbuilder

**ADW ID:** fd9119bc
**Date:** 2025-11-09
**Specification:** specs/issue-16-adw-fd9119bc-sdlc_planner-cli-interface.md

## Overview

This feature documents the specification for an interactive command-line interface (CLI) for the tac-webbuilder system. The CLI will enable developers to submit natural language requests for GitHub issue creation, manage ADW workflow configurations, track request history, and integrate ADW into existing or new projects through both interactive and direct command modes.

## What Was Built

This change establishes the complete specification for the CLI interface feature, including:

- Specification document defining CLI architecture and implementation plan
- Configuration updates for isolated ADW tree execution environment
- Detailed implementation tasks across 13 phases
- Comprehensive testing strategy with unit and E2E test requirements
- Integration patterns with existing core modules

## Technical Implementation

### Files Modified

- `specs/issue-16-adw-fd9119bc-sdlc_planner-cli-interface.md`: Complete CLI interface specification with architecture, implementation plan, testing strategy, and validation commands
- `.mcp.json`: Updated Playwright MCP config path from `e2bbe1a5` tree to `fd9119bc` tree for isolated execution environment
- `playwright-mcp-config.json`: Updated video recording directory path from `e2bbe1a5` tree to `fd9119bc` tree

### Key Changes

- **Comprehensive CLI Specification**: Defined complete architecture using Typer (CLI framework), questionary (interactive prompts), and rich (terminal formatting) libraries
- **13-Phase Implementation Plan**: Structured approach from dependency installation through documentation and validation
- **Command Structure**: Six main commands defined - `request`, `interactive`, `history`, `config`, `integrate`, and `new`
- **Integration Strategy**: Clear integration points with existing tac-webbuilder core modules and main application's NL processing system
- **Testing Framework**: Unit tests, edge cases, and E2E test structure for comprehensive validation
- **Tree Isolation**: Updated MCP configuration to ensure ADW execution in isolated tree environment (fd9119bc)

## How to Use

### Understanding the Specification

This specification document serves as the complete blueprint for implementing the CLI interface. It should be referenced when:

1. **Planning Implementation**: Review the 13 step-by-step tasks in implementation order
2. **Understanding Architecture**: Review the CLI structure, command handlers, and integration points
3. **Writing Tests**: Reference the Testing Strategy section for unit test requirements and edge cases
4. **Validating Implementation**: Execute all validation commands listed in the Validation Commands section

### Key Specification Sections

- **Feature Description**: High-level overview of CLI capabilities
- **Implementation Plan**: Three phases - Foundation, Core Implementation, and Integration
- **Step by Step Tasks**: 13 ordered tasks from dependency installation to validation
- **Testing Strategy**: Unit tests, edge cases, and E2E test requirements
- **Acceptance Criteria**: Success metrics for the completed feature
- **Validation Commands**: Complete list of commands to validate implementation

### CLI Commands (Once Implemented)

The specification defines these commands:

```bash
# Interactive mode (guided workflow)
webbuilder interactive

# Direct request submission
webbuilder request "Add user authentication"

# Auto-post without confirmation
webbuilder request "Add dark mode" --auto-post

# View request history
webbuilder history

# Manage configuration
webbuilder config set auto_post true
webbuilder config get auto_post
webbuilder config list

# Future: Create new project
webbuilder new my-app --framework react-vite

# Future: Integrate ADW into existing project
webbuilder integrate /path/to/project
```

## Configuration

### Required Environment Variables

The CLI will require these environment variables (once implemented):

- `ANTHROPIC_API_KEY`: For NL processing integration
- `GITHUB_REPO_URL`: Target repository for issue creation
- `WEBBUILDER_CONFIG` (optional): Custom config file path

### CLI-Specific Configuration

The specification defines these configuration options:

- `auto_post`: Skip confirmation prompts (default: false)
- `default_project_path`: Default project path for requests
- History storage: `~/.webbuilder/history.json`

### Tree Isolation Configuration

The MCP configuration has been updated to ensure ADW execution occurs in an isolated tree environment:

- Working directory: `/Users/Warmonger0/tac/tac-7/trees/fd9119bc`
- Video recording directory: `/Users/Warmonger0/tac/tac-7/trees/fd9119bc/videos`
- This ensures clean separation between ADW workflow iterations

## Testing

### Test Structure

The specification defines comprehensive testing requirements:

**Unit Tests** (to be implemented in `tests/interfaces/`):
- `test_output.py`: Rich formatting functions
- `test_config_manager.py`: Configuration get/set/list operations
- `test_history.py`: History tracking and persistence
- `test_cli_main.py`: Command handlers and routing
- `test_interactive.py`: Interactive mode with mocked prompts

**Edge Cases to Cover**:
- Missing environment variables
- Missing or unauthenticated GitHub CLI
- Invalid project paths
- Corrupted history file
- Network errors during GitHub operations
- User cancellation in interactive mode
- Concurrent history file access

**E2E Test** (to be created in `.claude/commands/e2e/test_cli_interface.md`):
- CLI launch and help text
- History command with empty history
- Config list command
- Interactive mode prompt display

### Validation Commands

Once implemented, run these commands to validate:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# Run all CLI unit tests
uv run pytest tests/interfaces/ -v

# Ensure no regressions
uv run pytest -v

# Test CLI help
uv run python -m interfaces.cli --help

# Test individual command help
uv run python -m interfaces.cli request --help
uv run python -m interfaces.cli interactive --help
uv run python -m interfaces.cli history --help
uv run python -m interfaces.cli config --help

# Test commands
uv run python -m interfaces.cli config list
uv run python -m interfaces.cli history

# Test convenience script
./scripts/start_cli.sh --help
```

## Notes

### Design Rationale

**Typer Framework**: Chosen for automatic help generation, type hints support, and seamless rich integration

**Questionary**: Selected for interactive prompts with excellent UX (arrow key navigation, validation)

**Rich Library**: Provides professional terminal output with tables, panels, and progress indicators

**JSON-based History**: Simple, human-readable format for debugging and extension

**Integration Strategy**: Leverages existing Pydantic configuration system and ADW workflow patterns

### Implementation Approach

The specification defines a 13-task sequential implementation:

1. **Foundation** (Tasks 1-2): Dependencies and package structure
2. **Core Utilities** (Tasks 3-5): Output formatting, configuration, history tracking
3. **Command Handlers** (Tasks 6-7): Request processing and interactive mode
4. **CLI Entry Points** (Tasks 8-10): Main CLI, module entry, convenience script
5. **Testing & Documentation** (Tasks 11-13): E2E tests, documentation, validation

### Future Extensibility

The specification plans for future enhancements:

- **Project Templates**: `new` command for scaffolding web app projects
- **ADW Integration**: `integrate` command for existing codebases
- **Status Monitoring**: Real-time ADW workflow execution tracking
- **Workflow Management**: List and trigger specific ADW workflows
- **Shell Completion**: Autocomplete for bash/zsh/fish
- **Plugins**: Third-party CLI extensions

### Dependencies

The CLI will integrate with:

- **Existing tac-webbuilder**: `core/config.py`, `adws/adw_modules/`
- **Main Application** (future): `app/server/core/nl_processor.py`, `app/server/core/project_detector.py`, `app/server/core/github_poster.py`

### Success Metrics

- CLI execution time < 1s for synchronous commands
- Clear, actionable error messages for all failure modes
- Zero breaking changes to existing functionality
- Test coverage >80% for all CLI code
- Complete auto-generated help documentation
