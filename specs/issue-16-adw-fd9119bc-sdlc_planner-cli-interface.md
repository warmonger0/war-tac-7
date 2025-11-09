# Feature: CLI Interface for tac-webbuilder

## Metadata
issue_number: `16`
adw_id: `fd9119bc`
issue_json: `{"number":16,"title":"CLI Interface","body":"# 🎯 ISSUE 3: tac-webbuilder - CLI Interface\n\n## Overview\nBuild an interactive CLI for submitting natural language requests and managing the webbuilder system.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory.\n\n## Dependencies\n**Requires**: Issue 2 (NL Processing & Issue Formatter) to be completed\n\n## Tasks\n\n### 1. CLI Entry Point\n**File**: `interfaces/cli/main.py`\n\nUse **Typer** for CLI framework:\n```python\nimport typer\nfrom rich.console import Console\n\napp = typer.Typer()\nconsole = Console()\n\n@app.command()\ndef request(\n    nl_input: str,\n    project: str = typer.Option(None, help=\"Target project path\"),\n    auto_post: bool = typer.Option(False, help=\"Skip confirmation\")\n):\n    \"\"\"Submit a natural language request.\"\"\"\n\n@app.command()\ndef interactive():\n    \"\"\"Start interactive mode.\"\"\"\n\n@app.command()\ndef integrate(path: str):\n    \"\"\"Integrate ADW into existing codebase.\"\"\"\n\n@app.command()\ndef new(\n    name: str,\n    framework: str = typer.Option(\"react-vite\")\n):\n    \"\"\"Create new web app project.\"\"\"\n\n@app.command()\ndef config(action: str, key: str, value: str = None):\n    \"\"\"Manage configuration (set/get).\"\"\"\n\n@app.command()\ndef history(limit: int = 10):\n    \"\"\"View past requests and their status.\"\"\"\n```\n\n### 2. Interactive Mode\n**File**: `interfaces/cli/interactive.py`\n\nUse **questionary** for interactive prompts:\n```python\nimport questionary\n\ndef run_interactive_mode():\n    \"\"\"\n    Flow:\n    1. Ask: New project or existing codebase?\n    2. If new: Select framework template\n    3. If existing: Get path and analyze\n    4. Prompt for feature request\n    5. Generate issue preview\n    6. Confirm and post\n    7. Display GitHub issue URL\n    \"\"\"\n\n    mode = questionary.select(\n        \"What would you like to do?\",\n        choices=[\n            \"Submit a request for existing project\",\n            \"Create new web app\",\n            \"Integrate ADW into existing codebase\",\n            \"View history\"\n        ]\n    ).ask()\n```\n\n### 3. Request Handler\n**File**: `interfaces/cli/commands.py`\n\n```python\nfrom core.nl_processor import process_request\nfrom core.github_poster import GitHubPoster\nfrom core.project_detector import detect_project_context\n\ndef handle_request(\n    nl_input: str,\n    project_path: str,\n    auto_post: bool\n):\n    \"\"\"\n    1. Detect project context\n    2. Process NL request\n    3. Format GitHub issue\n    4. Show preview (if not auto_post)\n    5. Post to GitHub\n    6. Display issue URL and workflow info\n    \"\"\"\n```\n\n### 4. History Tracking\n**File**: `interfaces/cli/history.py`\n\n```python\nimport json\nfrom pathlib import Path\n\nclass RequestHistory:\n    def __init__(self, history_file: Path):\n        self.history_file = history_file\n\n    def add_request(\n        self,\n        nl_input: str,\n        issue_number: int,\n        project: str,\n        timestamp: str\n    ):\n        \"\"\"Save request to history.\"\"\"\n\n    def get_recent(self, limit: int = 10) -> list[dict]:\n        \"\"\"Get recent requests.\"\"\"\n\n    def display(self):\n        \"\"\"Display history in rich table.\"\"\"\n```\n\n**History file**: `~/.webbuilder/history.json`\n\n### 5. Configuration Commands\n**File**: `interfaces/cli/config_manager.py`\n\n```python\ndef get_config(key: str) -> str:\n    \"\"\"Get configuration value.\"\"\"\n\ndef set_config(key: str, value: str):\n    \"\"\"Set configuration value.\"\"\"\n\ndef list_config():\n    \"\"\"Display all configuration.\"\"\"\n```\n\n### 6. Rich Output Formatting\nUse **Rich** for beautiful terminal output:\n- Progress spinners during NL processing\n- Formatted tables for history\n- Syntax highlighted issue preview\n- Success/error panels\n\n## Dependencies (Python)\nAdd to `pyproject.toml`:\n```toml\ntyper = \"^0.15.0\"\nquestionary = \"^2.0.0\"\nrich = \"^13.0.0\"\n```\n\n## Scripts\n**File**: `scripts/start_cli.sh`\n```bash\n#!/bin/bash\ncd \"$(dirname \"$0\")/..\"\nuv run python -m interfaces.cli.main \"$@\"\n```\n\n## Test Cases\nCreate `tests/interfaces/test_cli.py`:\n```python\ndef test_request_command():\n    \"\"\"Test basic request submission.\"\"\"\n\ndef test_interactive_mode():\n    \"\"\"Test interactive flow.\"\"\"\n\ndef test_history_tracking():\n    \"\"\"Test history is saved and displayed.\"\"\"\n\ndef test_config_management():\n    \"\"\"Test get/set config.\"\"\"\n```\n\n## Success Criteria\n- ✅ CLI accepts natural language requests\n- ✅ Interactive mode guides users through workflow\n- ✅ History tracks all requests\n- ✅ Configuration can be managed via CLI\n- ✅ Rich formatting makes output beautiful\n- ✅ All tests pass\n\n## Example Usage\n```bash\n# Interactive mode\nwebbuilder interactive\n\n# Direct request\nwebbuilder request \"Add user authentication\"\n\n# With auto-post\nwebbuilder request \"Add dark mode\" --auto-post\n\n# View history\nwebbuilder history\n\n# Configure\nwebbuilder config set auto_post true\n```\n\n## Next Issues\nCan run in parallel with Issue 4. After both 3 and 5 complete:\n- **Issue 6**: Project Templates & Documentation\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`interface`, `cli`, `webbuilder`\n"}`

## Feature Description
Build a comprehensive interactive command-line interface (CLI) for the tac-webbuilder system that allows users to submit natural language requests for GitHub issue creation, manage ADW workflow configurations, track request history, and integrate ADW into existing or new projects. The CLI will provide both interactive and command-line modes, with rich terminal formatting for an enhanced user experience.

## User Story
As a developer using tac-webbuilder
I want to submit natural language requests and manage workflows via a CLI
So that I can efficiently generate GitHub issues and manage ADW workflows without needing to use the web interface or manual API calls

## Problem Statement
Currently, the tac-webbuilder system has robust natural language processing and GitHub issue generation capabilities (implemented in Issue #14), but lacks a user-friendly interface for developers to interact with these features. Users need a convenient command-line tool that allows them to submit requests, view history, manage configurations, and integrate ADW into their projects without writing custom Python code or scripts.

## Solution Statement
Implement a Typer-based CLI application with rich terminal formatting that provides:
- Direct command execution for quick requests
- Interactive mode with questionary prompts for guided workflows
- History tracking of all requests with status updates
- Configuration management for user preferences
- Project integration commands for setting up ADW in new or existing codebases
- Beautiful terminal output using the rich library

## Relevant Files
Use these files to implement the feature:

**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`

**Existing Files to Reference**:
- `core/config.py` - Existing Pydantic-based configuration system with YAML support. Will be extended for CLI-specific settings
- `adws/adw_modules/agent.py` - Claude Code CLI execution patterns. Reference for understanding ADW workflow execution
- `adws/adw_modules/github.py` - GitHub operations module. Reference for issue fetching and posting patterns
- `adws/adw_modules/workflow_ops.py` - Workflow orchestration logic. Reference for understanding available ADW workflows
- `tests/test_config.py` - Existing test patterns for configuration. Extend for CLI configuration tests
- `pyproject.toml` - Project dependencies. Will be updated to add typer, questionary, and rich
- `README.md` - Project documentation. Will be updated with CLI usage examples

**Context from Main Application**:
Since the tac-webbuilder will eventually integrate with the main application's NL processing capabilities:
- Reference: `app/server/core/nl_processor.py` (from main app) - Natural language processing patterns
- Reference: `app/server/core/project_detector.py` (from main app) - Project context detection patterns
- Reference: `app/server/core/github_poster.py` (from main app) - GitHub posting with rich preview patterns
- Reference: `app/server/core/issue_formatter.py` (from main app) - Issue formatting templates

**Documentation**:
- `.claude/commands/conditional_docs.md` - Conditional documentation guide
- `.claude/commands/test_e2e.md` - E2E test execution patterns
- `.claude/commands/e2e/test_basic_query.md` - Example E2E test structure

### New Files
The following files will be created to implement the CLI feature:

**CLI Implementation**:
- `interfaces/cli/main.py` - Main CLI entry point with Typer commands
- `interfaces/cli/__main__.py` - Python module entry point for `python -m interfaces.cli`
- `interfaces/cli/commands.py` - Command handlers for request processing
- `interfaces/cli/interactive.py` - Interactive mode implementation with questionary
- `interfaces/cli/history.py` - Request history tracking and display
- `interfaces/cli/config_manager.py` - Configuration management commands
- `interfaces/cli/output.py` - Rich terminal output formatting utilities

**Scripts**:
- `scripts/start_cli.sh` - Convenience script to launch CLI

**Tests**:
- `tests/interfaces/__init__.py` - Test package initialization
- `tests/interfaces/test_cli_main.py` - Tests for main CLI commands
- `tests/interfaces/test_interactive.py` - Tests for interactive mode
- `tests/interfaces/test_history.py` - Tests for history tracking
- `tests/interfaces/test_config_manager.py` - Tests for configuration management
- `tests/interfaces/test_output.py` - Tests for output formatting

**E2E Test**:
- `.claude/commands/e2e/test_cli_interface.md` - End-to-end test for CLI functionality

## Implementation Plan
### Phase 1: Foundation
Set up the CLI infrastructure with Typer framework, rich terminal formatting, and basic command structure. Install required dependencies (typer, questionary, rich) and create the CLI package structure with proper module initialization. Establish patterns for command handlers, error handling, and output formatting that will be consistent across all CLI commands.

### Phase 2: Core Implementation
Implement the five main CLI commands:
1. **request** - Process natural language requests and create GitHub issues
2. **interactive** - Launch interactive mode with questionary prompts
3. **history** - Display request history with rich table formatting
4. **config** - Manage configuration (get/set/list)
5. **integrate** - Set up ADW in existing projects (placeholder for future)

Integrate with existing core modules (from main app's NL processing system) to leverage natural language processing, project detection, and GitHub posting capabilities. Build request history tracking system with JSON-based persistent storage.

### Phase 3: Integration
Connect the CLI to the existing tac-webbuilder core infrastructure:
- Use the existing config.py for configuration management
- Integrate with ADW workflow execution patterns from adws/adw_modules
- Ensure CLI respects existing configuration files and environment variables
- Add comprehensive error handling for missing dependencies (gh CLI, API keys)
- Create convenience scripts for easy CLI access

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Install Dependencies and Update Project Configuration
- Add typer, questionary, and rich to `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/pyproject.toml` dependencies
- Run `uv sync` to install new dependencies
- Verify dependencies are properly installed

### Task 2: Create CLI Package Structure
- Create directory: `interfaces/cli/`
- Initialize `interfaces/cli/__init__.py` with package exports
- Create `interfaces/cli/__main__.py` for `python -m interfaces.cli` entry point
- Set up basic package structure

### Task 3: Implement Output Formatting Utilities
- Create `interfaces/cli/output.py`
- Implement console initialization with rich.Console
- Add spinner/progress indicators for async operations
- Add panel formatting for success/error messages
- Add table formatting for history display
- Create functions for: show_error(), show_success(), show_info(), show_panel(), create_table()
- Write unit tests in `tests/interfaces/test_output.py`

### Task 4: Implement Configuration Manager
- Create `interfaces/cli/config_manager.py`
- Implement get_config(), set_config(), list_config() functions
- Integrate with existing `core/config.py` for configuration loading
- Support CLI-specific configuration (e.g., auto_post, default_project_path)
- Add rich table formatting for config listing
- Write unit tests in `tests/interfaces/test_config_manager.py`

### Task 5: Implement History Tracking System
- Create `interfaces/cli/history.py`
- Implement RequestHistory class with JSON-based persistence
- Store history in `~/.webbuilder/history.json`
- Implement add_request(), get_recent(), display() methods
- Add rich table formatting for history display with columns: Timestamp, Request, Issue #, Project, Status
- Handle history file creation if it doesn't exist
- Write unit tests in `tests/interfaces/test_history.py`

### Task 6: Implement Request Command Handler
- Create `interfaces/cli/commands.py`
- Implement handle_request() function that:
  - Accepts nl_input, project_path, auto_post parameters
  - Validates required environment variables (ANTHROPIC_API_KEY, GITHUB_REPO_URL)
  - Detects project context using patterns from app/server/core/project_detector.py
  - Processes NL request (stub for now, will integrate with core modules)
  - Shows rich preview of generated issue
  - Confirms with user if not auto_post
  - Posts to GitHub (stub for now)
  - Saves to history
  - Displays success message with issue URL
- Add error handling for missing dependencies
- Write unit tests in `tests/interfaces/test_cli_main.py`

### Task 7: Implement Interactive Mode
- Create `interfaces/cli/interactive.py`
- Implement run_interactive_mode() function with questionary prompts:
  - Main menu: Submit request / Create new project / Integrate ADW / View history
  - For "Submit request": prompt for project path, then NL request
  - For "View history": call history.display()
  - For "Create new project" and "Integrate ADW": show "Coming soon" message
- Add project path validation
- Add confirmation prompts before posting to GitHub
- Implement graceful cancellation handling
- Write unit tests in `tests/interfaces/test_interactive.py` using unittest.mock for questionary

### Task 8: Implement Main CLI Entry Point
- Create `interfaces/cli/main.py`
- Set up Typer app with rich console
- Implement commands:
  - `request` - Call handle_request() from commands.py
  - `interactive` - Call run_interactive_mode() from interactive.py
  - `history` - Display history with optional limit parameter
  - `config` - Manage configuration (get/set/list actions)
  - `integrate` - Placeholder for future ADW integration
  - `new` - Placeholder for future project creation
- Add proper docstrings for CLI help text
- Implement version command showing tac-webbuilder version
- Add error handling and user-friendly error messages

### Task 9: Implement Python Module Entry Point
- Create `interfaces/cli/__main__.py`
- Import and call main() from main.py
- Ensure `python -m interfaces.cli` works correctly

### Task 10: Create Convenience Launch Script
- Create `scripts/start_cli.sh`
- Add shebang and navigate to project root
- Execute `uv run python -m interfaces.cli "$@"`
- Make script executable with `chmod +x`
- Test script execution

### Task 11: Create E2E Test File
- Create `.claude/commands/e2e/test_cli_interface.md`
- Define test steps to validate:
  - CLI can be launched
  - `webbuilder history` command works
  - `webbuilder config list` command works
  - `webbuilder interactive` prompts appear
  - Help text is displayed properly
- Structure test similar to existing E2E tests (test_basic_query.md, test_complex_query.md)
- Include user story and success criteria
- Specify that tests should run with the convenience script

### Task 12: Update Project Documentation
- Update `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/README.md`
- Add "CLI Interface" section with:
  - Installation instructions
  - Usage examples for all commands
  - Interactive mode walkthrough
  - Configuration management guide
  - Troubleshooting section
- Include example outputs with rich formatting

### Task 13: Run Validation Commands
Execute all validation commands to ensure zero regressions and complete functionality:
- Run all CLI tests
- Run all existing tests to ensure no regressions
- Execute the E2E test
- Verify CLI help output
- Test CLI execution via script and python -m

## Testing Strategy
### Unit Tests
- **Output Formatting** (`test_output.py`): Test all rich formatting functions (panels, tables, spinners, messages)
- **Configuration Manager** (`test_config_manager.py`): Test get/set/list operations, integration with core config
- **History Tracking** (`test_history.py`): Test add, retrieve, display operations, JSON persistence, file creation
- **Command Handlers** (`test_cli_main.py`): Test request handler with mocked dependencies, error handling
- **Interactive Mode** (`test_interactive.py`): Test questionary prompts with mocked inputs, flow control
- **Main CLI** (`test_cli_main.py`): Test Typer command routing, parameter parsing, help text generation

All tests should mock external dependencies (GitHub CLI, API calls, file system where appropriate) to ensure fast, deterministic execution.

### Edge Cases
- Missing environment variables (ANTHROPIC_API_KEY, GITHUB_REPO_URL)
- Missing GitHub CLI (`gh` command not found)
- GitHub CLI not authenticated
- Invalid project path provided
- History file doesn't exist (should create)
- History file is corrupted JSON (should handle gracefully)
- Configuration file doesn't exist (should use defaults)
- User cancels interactive mode (should exit gracefully)
- Network errors during GitHub posting
- Invalid configuration keys
- Empty history display
- Concurrent access to history file

## Acceptance Criteria
- CLI can be invoked via `python -m interfaces.cli` or convenience script
- `request` command accepts NL input and creates GitHub issues (with confirmation)
- `interactive` command launches questionary-based interactive mode
- `history` command displays past requests in rich table format
- `config` command can get, set, and list configuration values
- History is persisted to `~/.webbuilder/history.json`
- All CLI output uses rich formatting for professional appearance
- Error messages are clear and actionable
- Help text is generated automatically by Typer and is comprehensive
- All unit tests pass with >80% coverage
- E2E test validates CLI functionality end-to-end
- No regressions in existing tac-webbuilder functionality
- Documentation is complete with usage examples

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

```bash
# Navigate to tac-webbuilder project
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# Run CLI unit tests
uv run pytest tests/interfaces/ -v

# Run all tests to ensure no regressions
uv run pytest -v

# Test CLI help output
uv run python -m interfaces.cli --help

# Test individual commands help
uv run python -m interfaces.cli request --help
uv run python -m interfaces.cli interactive --help
uv run python -m interfaces.cli history --help
uv run python -m interfaces.cli config --help

# Test configuration commands
uv run python -m interfaces.cli config list

# Test history command (should work even with no history)
uv run python -m interfaces.cli history

# Test convenience script
./scripts/start_cli.sh --help

# Read and execute E2E test
# Read .claude/commands/test_e2e.md, then read and execute .claude/commands/e2e/test_cli_interface.md
```

## Notes

### Design Decisions
1. **Typer Framework**: Chosen for its automatic help generation, type hints support, and seamless integration with rich
2. **Questionary**: Selected for interactive prompts with excellent UX (arrow key navigation, validation)
3. **Rich Library**: Provides professional terminal output with tables, panels, progress indicators, and syntax highlighting
4. **JSON-based History**: Simple, human-readable, easy to debug and extend
5. **Integration with Existing Config**: Leverages the existing Pydantic-based configuration system from core/config.py

### Implementation Notes
- This CLI is the primary interface for tac-webbuilder and should be intuitive and well-documented
- Follow patterns from the main application's NL processing system (app/server/core/)
- The CLI should validate all required dependencies (gh CLI, API keys) before attempting operations
- Error messages must be actionable and guide users to resolution
- History tracking enables users to monitor their request patterns and troubleshoot issues
- Configuration management allows users to customize behavior without editing files

### Future Extensibility
This CLI foundation enables future enhancements:
- **Project Templates** (Issue 6): `new` command will scaffold new web app projects
- **ADW Integration** (Issue 6): `integrate` command will set up ADW in existing codebases
- **Status Monitoring**: Track ADW workflow execution status in real-time
- **Workflow Management**: List, configure, and trigger specific ADW workflows
- **Template Customization**: Allow users to customize issue templates
- **Shell Completion**: Add autocomplete for bash/zsh/fish
- **Plugins**: Support third-party CLI extensions

### Dependencies on Main Application
While the tac-webbuilder is a separate project, the CLI will eventually integrate with the main application's NL processing capabilities. For now, the implementation should:
- Create stubs for NL processing that can later integrate with app/server/core modules
- Design interfaces that match the existing NL processing APIs
- Plan for future integration with the main application's features

### Required Environment Variables
- `ANTHROPIC_API_KEY` - For NL processing (when integrated)
- `GITHUB_REPO_URL` - Target repository for issue creation
- Optional: `WEBBUILDER_CONFIG` - Custom config file path

### Key Metrics for Success
- CLI execution time < 1s for synchronous commands (history, config)
- Clear error messages for all failure modes
- Zero breaking changes to existing tac-webbuilder functionality
- Test coverage >80% for all new CLI code
- Complete help documentation auto-generated by Typer
