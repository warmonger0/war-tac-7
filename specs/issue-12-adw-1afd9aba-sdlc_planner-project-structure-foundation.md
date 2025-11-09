# Feature: tac-webbuilder - Project Foundation & Core Infrastructure

## Metadata
issue_number: `12`
adw_id: `1afd9aba`
issue_json: `{"number":12,"title":"Foundation: Project Structure & ADW Integration","body":"# 🎯 ISSUE 1: tac-webbuilder - Project Foundation & Core Infrastructure\n\n## Overview\nCreate the foundational project structure for `tac-webbuilder` at `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder` and copy/adapt the ADW workflow system from tac-7.\n\n## Tasks\n\n### 1. Create Project Structure\n```\n/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/\n├── README.md\n├── .env.sample\n├── .gitignore\n├── core/\n│   ├── __init__.py\n│   └── config.py\n├── interfaces/\n│   ├── cli/\n│   └── web/\n├── adws/\n│   ├── README.md\n│   └── adw_modules/\n├── .claude/\n│   ├── commands/\n│   ├── hooks/\n│   └── settings.json\n├── templates/\n├── scripts/\n├── logs/\n├── agents/\n└── trees/\n```\n\n### 2. Copy ADW System from tac-7\nCopy and adapt these directories from `/Users/Warmonger0/tac/tac-7`:\n- `adws/adw_modules/` → `adws/adw_modules/`\n- `adws/adw_*_iso.py` scripts → `adws/`\n- `adws/adw_triggers/` → `adws/adw_triggers/`\n- `.claude/commands/` → `.claude/commands/`\n- `.claude/hooks/` → `.claude/hooks/`\n- `.claude/settings.json` → `.claude/settings.json`\n\n### 3. Create Configuration System\n**File**: `core/config.py`\n```python\n# Configuration management using Pydantic\n# Support for config.yaml and environment variables\n# GitHub, ADW, interfaces, and Claude settings\n```\n\n**File**: `config.yaml.sample`\n```yaml\ngithub:\n  default_repo: \"owner/tac-webbuilder\"\n  auto_post: false\nadw:\n  default_workflow: \"adw_sdlc_iso\"\n  default_model_set: \"base\"\ninterfaces:\n  cli:\n    enabled: true\n  web:\n    enabled: true\n    port: 5174\n```\n\n### 4. Environment Configuration\n**File**: `.env.sample`\n```bash\nGITHUB_REPO_URL=\"https://github.com/owner/tac-webbuilder\"\nGITHUB_PAT=\"ghp_xxxx\"\nANTHROPIC_API_KEY=\"sk-ant-xxxx\"\nCLAUDE_CODE_PATH=\"/path/to/claude\"\nAUTO_POST_ISSUES=\"false\"\nDEFAULT_WORKFLOW=\"adw_sdlc_iso\"\nWEB_UI_PORT=\"5174\"\n```\n\n### 5. Initialize Directory\n```bash\nmkdir -p /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder\n```\n**Note**: No separate git init needed - this will be part of tac-7's repository\n\n### 6. Basic README\nCreate README.md with:\n- Project overview\n- Prerequisites\n- Quick start guide\n- Link to tac-7 for ADW documentation\n\n## Success Criteria\n- ✅ Project directory created at `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`\n- ✅ All ADW modules copied and functional\n- ✅ Configuration system implemented\n- ✅ Directory structure complete\n- ✅ README documents the foundation\n\n## Dependencies\nNone (this is the starting point)\n\n## Next Issues\nAfter this completes, create:\n- **Issue 2**: Natural Language Processing & Issue Formatter\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`infrastructure`, `foundation`, `webbuilder`\n\n\nWorkflow: \n  adw_sdlc_zte_iso"}`

## Feature Description
Create the foundational project structure and infrastructure for `tac-webbuilder`, a new tool within the tac-7 repository that will enable users to interact with AI Developer Workflows (ADW) through natural language. This foundation includes setting up the directory structure, copying/adapting the ADW system from tac-7, creating configuration management, and establishing the basic project scaffolding that future features will build upon.

The project will live at `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder` and will share the same git repository as tac-7 but maintain its own isolated directory structure, configuration, and codebase. This approach allows tac-webbuilder to leverage tac-7's existing ADW infrastructure while developing as an independent tool.

## User Story
As a developer working with tac-7's AI Developer Workflows
I want a dedicated web-based interface to interact with ADW using natural language
So that I can create and manage GitHub issues and trigger workflows without manually writing markdown or interacting with the command line

## Problem Statement
Currently, using tac-7's ADW system requires:
1. Manual creation of GitHub issues with specific markdown formatting
2. Understanding of ADW workflow syntax and commands
3. Direct command-line interaction with ADW scripts
4. Knowledge of the exact file structure and configuration requirements

This creates barriers for users who want to leverage ADW's powerful automation but prefer a more intuitive, natural language interface. There is no web UI or conversational interface to simplify ADW interactions.

## Solution Statement
Create `tac-webbuilder` as a new project within tac-7 that provides:
1. A solid foundation with proper directory structure and configuration management
2. Complete integration with tac-7's existing ADW workflow system
3. A configuration system supporting both YAML files and environment variables
4. Proper separation of concerns with modular architecture (core, interfaces, templates)
5. Extensible structure ready for CLI and web interfaces
6. Comprehensive documentation linking back to tac-7's ADW system

This foundation will enable future features to add natural language processing, a CLI interface, and a web UI without requiring architectural changes.

## Relevant Files
Use these files to implement the feature:

### Existing Files to Reference
- `/Users/Warmonger0/tac/tac-7/README.md` - Main tac-7 project documentation, structure reference
- `/Users/Warmonger0/tac/tac-7/adws/README.md` - Complete ADW system documentation to understand what needs copying
- `/Users/Warmonger0/tac/tac-7/adws/adw_modules/` - Core ADW modules (agent.py, data_types.py, github.py, git_ops.py, state.py, workflow_ops.py, worktree_ops.py, utils.py, r2_uploader.py)
- `/Users/Warmonger0/tac/tac-7/adws/adw_*_iso.py` - All ADW workflow scripts that need copying
- `/Users/Warmonger0/tac/tac-7/adws/adw_triggers/` - Automation trigger scripts (trigger_cron.py, trigger_webhook.py)
- `/Users/Warmonger0/tac/tac-7/.claude/commands/` - All slash command definitions
- `/Users/Warmonger0/tac/tac-7/.claude/hooks/` - All Claude Code hooks
- `/Users/Warmonger0/tac/tac-7/.claude/settings.json` - Claude Code configuration
- `/Users/Warmonger0/tac/tac-7/.gitignore` - Git ignore patterns to adapt
- `/Users/Warmonger0/tac/tac-7/.env.sample` - Environment variable template

### New Files
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/README.md` - Main project documentation
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/.env.sample` - Environment configuration template
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/.gitignore` - Git ignore rules for tac-webbuilder
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/config.yaml.sample` - YAML configuration template
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/core/__init__.py` - Core module initialization
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/core/config.py` - Configuration management using Pydantic
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/pyproject.toml` - Python project configuration with uv
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/interfaces/__init__.py` - Interfaces module initialization
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/interfaces/cli/__init__.py` - CLI interface placeholder
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/interfaces/web/__init__.py` - Web interface placeholder
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/templates/issue_template.md` - Template for generating GitHub issues
- `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/scripts/setup.sh` - Initial setup script
- `/Users/Warmonger0/tac/tac-7/.gitignore` - Update to include projects/ exclusions (if needed)

## Implementation Plan

### Phase 1: Foundation - Directory Structure
Create the complete directory structure for tac-webbuilder with all necessary subdirectories and placeholder files. This establishes the physical project layout and ensures all future components have proper locations.

### Phase 2: Core Implementation - Copy ADW System and Create Configuration
Copy the entire ADW system from tac-7 (modules, scripts, triggers) to tac-webbuilder and create the configuration management system using Pydantic. This provides the workflow automation infrastructure and flexible configuration handling.

### Phase 3: Integration - Documentation and Validation
Create comprehensive documentation that explains the project structure, links to tac-7's ADW documentation, and validates that all copied components work correctly in their new location.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Create Root Project Directory
- Create the main project directory at `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/`
- Verify the directory is created successfully

### Step 2: Create Directory Structure
- Create `core/` directory for configuration and core utilities
- Create `interfaces/` directory with `cli/` and `web/` subdirectories
- Create `adws/` directory for ADW workflow system
- Create `.claude/` directory with `commands/` and `hooks/` subdirectories
- Create `templates/` directory for issue and workflow templates
- Create `scripts/` directory for utility scripts
- Create `logs/` directory for runtime logging (should be in .gitignore)
- Create `agents/` directory for agent execution artifacts (should be in .gitignore)
- Create `trees/` directory for worktree isolation (should be in .gitignore)

### Step 3: Copy ADW Modules
- Copy entire `/Users/Warmonger0/tac/tac-7/adws/adw_modules/` directory to `projects/tac-webbuilder/adws/adw_modules/`
- Verify all Python files are copied correctly: `__init__.py`, `agent.py`, `data_types.py`, `git_ops.py`, `github.py`, `r2_uploader.py`, `state.py`, `utils.py`, `workflow_ops.py`, `worktree_ops.py`

### Step 4: Copy ADW Workflow Scripts
- Copy all `adw_*_iso.py` scripts from `/Users/Warmonger0/tac/tac-7/adws/` to `projects/tac-webbuilder/adws/`
- Include: `adw_build_iso.py`, `adw_document_iso.py`, `adw_patch_iso.py`, `adw_plan_build_document_iso.py`, `adw_plan_build_iso.py`, `adw_plan_build_review_iso.py`, `adw_plan_build_test_iso.py`, `adw_plan_build_test_review_iso.py`, `adw_plan_iso.py`, `adw_review_iso.py`, `adw_sdlc_iso.py`, `adw_sdlc_zte_iso.py`, `adw_ship_iso.py`, `adw_test_iso.py`
- Verify all scripts are executable (chmod +x where needed)

### Step 5: Copy ADW Triggers
- Copy entire `/Users/Warmonger0/tac/tac-7/adws/adw_triggers/` directory to `projects/tac-webbuilder/adws/adw_triggers/`
- Verify `trigger_cron.py` and `trigger_webhook.py` are present

### Step 6: Copy ADW Tests
- Copy entire `/Users/Warmonger0/tac/tac-7/adws/adw_tests/` directory to `projects/tac-webbuilder/adws/adw_tests/`
- This ensures all test utilities and health checks are available

### Step 7: Copy ADW Documentation
- Copy `/Users/Warmonger0/tac/tac-7/adws/README.md` to `projects/tac-webbuilder/adws/README.md`
- This maintains the complete ADW documentation within the tac-webbuilder project

### Step 8: Copy Claude Commands
- Copy entire `/Users/Warmonger0/tac/tac-7/.claude/commands/` directory to `projects/tac-webbuilder/.claude/commands/`
- Verify all slash command files are present including e2e test commands

### Step 9: Copy Claude Hooks
- Copy entire `/Users/Warmonger0/tac/tac-7/.claude/hooks/` directory to `projects/tac-webbuilder/.claude/hooks/`
- Verify hook scripts are executable

### Step 10: Copy Claude Settings
- Copy `/Users/Warmonger0/tac/tac-7/.claude/settings.json` to `projects/tac-webbuilder/.claude/settings.json`
- This maintains consistent Claude Code configuration

### Step 11: Create Python Project Configuration
- Create `projects/tac-webbuilder/pyproject.toml` with:
  - Project name: `tac-webbuilder`
  - Python version requirement: `>=3.10`
  - Dependencies: `pydantic`, `pydantic-settings`, `pyyaml`, `python-dotenv`
  - Development dependencies: `pytest`, `pytest-cov`
  - Use `uv` as the build system

### Step 12: Create Core Module Initialization
- Create `projects/tac-webbuilder/core/__init__.py` as empty initialization file
- Add docstring explaining this is the core configuration and utilities module

### Step 13: Create Configuration Management System
- Create `projects/tac-webbuilder/core/config.py` with:
  - Pydantic `BaseSettings` models for configuration
  - Support for loading from `config.yaml` and environment variables
  - Configuration sections: `GitHubConfig`, `ADWConfig`, `InterfacesConfig`, `ClaudeConfig`
  - Main `AppConfig` class that aggregates all configuration sections
  - Environment variable prefix: `TWB_` (tac-webbuilder)
  - YAML file loading with fallback to environment variables
  - Validation for required fields (GitHub repo, API keys)

### Step 14: Create YAML Configuration Template
- Create `projects/tac-webbuilder/config.yaml.sample` with:
  - `github` section: `default_repo`, `auto_post` (false by default)
  - `adw` section: `default_workflow` (adw_sdlc_iso), `default_model_set` (base)
  - `interfaces` section: `cli.enabled` (true), `web.enabled` (true), `web.port` (5174)
  - `claude` section: `code_path` (/path/to/claude)
  - Comments explaining each configuration option

### Step 15: Create Environment Variable Template
- Create `projects/tac-webbuilder/.env.sample` with:
  - `GITHUB_REPO_URL` - GitHub repository URL for issue posting
  - `GITHUB_PAT` - GitHub Personal Access Token
  - `ANTHROPIC_API_KEY` - Anthropic API key for Claude
  - `CLAUDE_CODE_PATH` - Path to Claude Code CLI
  - `AUTO_POST_ISSUES` - Boolean flag (false by default)
  - `DEFAULT_WORKFLOW` - Default ADW workflow to use
  - `WEB_UI_PORT` - Port for web interface
  - Comments explaining each variable and where to obtain values

### Step 16: Create Git Ignore File
- Create `projects/tac-webbuilder/.gitignore` based on `/Users/Warmonger0/tac/tac-7/.gitignore`
- Include patterns for: `.env`, `.ports.env`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `*.db`, `.vscode/`, `.DS_Store`, `logs/`, `agents/`, `trees/`, `storage.json`, `screenshots/`, `videos/`, `config.yaml` (exclude sample only)

### Step 17: Create Interface Module Placeholders
- Create `projects/tac-webbuilder/interfaces/__init__.py` with docstring
- Create `projects/tac-webbuilder/interfaces/cli/__init__.py` with docstring explaining future CLI interface
- Create `projects/tac-webbuilder/interfaces/web/__init__.py` with docstring explaining future web interface

### Step 18: Create Issue Template
- Create `projects/tac-webbuilder/templates/issue_template.md` with:
  - Markdown template structure for generating GitHub issues
  - Placeholder variables: `{title}`, `{description}`, `{workflow}`, `{labels}`
  - Instructions on how to use the template

### Step 19: Create Setup Script
- Create `projects/tac-webbuilder/scripts/setup.sh` that:
  - Checks for required tools (uv, gh, claude)
  - Checks for `.env` file (copies from `.env.sample` if missing)
  - Checks for `config.yaml` file (copies from `config.yaml.sample` if missing)
  - Runs `uv sync` to install dependencies
  - Verifies GitHub authentication with `gh auth status`
  - Provides helpful error messages and next steps
  - Is executable (chmod +x)

### Step 20: Create Main README
- Create `projects/tac-webbuilder/README.md` with:
  - Project overview and purpose
  - Architecture explanation (relationship to tac-7)
  - Prerequisites list (Python 3.10+, uv, gh, claude)
  - Quick start guide (setup script, configuration)
  - Project structure explanation with directory tree
  - Configuration documentation (YAML and environment variables)
  - Link to `/Users/Warmonger0/tac/tac-7/adws/README.md` for complete ADW documentation
  - Future roadmap (CLI interface, web UI, NL processing)
  - Development guidelines
  - Troubleshooting section

### Step 21: Update Parent Git Ignore (if needed)
- Read `/Users/Warmonger0/tac/tac-7/.gitignore`
- Check if `projects/` needs to be excluded or if specific patterns should be added
- Add `projects/*/logs/`, `projects/*/agents/`, `projects/*/trees/` if not already covered by existing patterns

### Step 22: Initialize Python Project
- Run `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && uv sync` to create virtual environment and install dependencies
- Verify the environment is created successfully

### Step 23: Create Basic Test for Configuration
- Create `projects/tac-webbuilder/tests/__init__.py`
- Create `projects/tac-webbuilder/tests/test_config.py` with:
  - Test loading configuration from YAML file
  - Test loading configuration from environment variables
  - Test validation of required fields
  - Test default values
  - Test configuration precedence (env vars override YAML)

### Step 24: Validate ADW System Integration
- Run a health check to ensure ADW modules are importable in the new location
- Create a simple validation script `projects/tac-webbuilder/scripts/validate_adw.py` that:
  - Imports key modules from `adws.adw_modules`
  - Checks that all expected ADW scripts exist
  - Verifies all slash commands are present
  - Reports any missing or broken imports

### Step 25: Run Validation Commands
- Execute all validation commands to ensure the foundation is complete with zero regressions

## Testing Strategy

### Unit Tests
- **Configuration Loading Tests**: Test that `core/config.py` correctly loads from YAML and environment variables
- **Configuration Validation Tests**: Test that required fields are validated and helpful errors are raised
- **Configuration Precedence Tests**: Test that environment variables override YAML values
- **Default Values Tests**: Test that sensible defaults are applied when optional configs are missing

### Integration Tests
- **ADW Module Import Tests**: Verify all copied ADW modules can be imported without errors
- **Setup Script Tests**: Test that `scripts/setup.sh` runs successfully in a clean environment
- **Validation Script Tests**: Test that `scripts/validate_adw.py` correctly identifies all ADW components

### Edge Cases
- Missing `.env` file (should copy from `.env.sample`)
- Missing `config.yaml` file (should copy from `.config.yaml.sample`)
- Invalid YAML syntax in config file
- Missing required environment variables
- Invalid GitHub repository URL format
- Missing ADW scripts or modules after copying
- Permission errors on hook scripts and setup scripts

## Acceptance Criteria
- ✅ All directories created under `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/`
- ✅ Complete ADW system copied (modules, scripts, triggers, tests, documentation)
- ✅ All Claude Code configuration copied (commands, hooks, settings)
- ✅ Configuration management system implemented with Pydantic
- ✅ Both YAML and environment variable configuration supported
- ✅ Project documentation complete with links to tac-7 ADW docs
- ✅ Python project initialized with `uv` and dependencies installed
- ✅ Setup script runs successfully and validates prerequisites
- ✅ Validation script confirms all ADW components are present and functional
- ✅ Configuration tests pass and validate loading from both sources
- ✅ Git ignore patterns prevent committing sensitive files or generated artifacts
- ✅ README provides clear quick start and architectural overview
- ✅ Interface module placeholders created for future CLI and web implementations

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `ls -la /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/` - Verify project directory exists
- `ls -la /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/adws/adw_modules/` - Verify ADW modules copied
- `ls -la /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/adws/*.py` - Verify ADW scripts copied
- `ls -la /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/.claude/commands/` - Verify Claude commands copied
- `cat /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/pyproject.toml` - Verify Python project configuration
- `cat /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/core/config.py` - Verify configuration system created
- `cat /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/config.yaml.sample` - Verify YAML config template
- `cat /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/.env.sample` - Verify environment template
- `cat /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/README.md` - Verify main documentation
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && uv sync` - Install dependencies and verify setup
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && uv run python -c "from core.config import AppConfig; print('Config imports successfully')"` - Verify configuration module imports
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && uv run python -c "from adws.adw_modules.agent import Agent; print('ADW modules import successfully')"` - Verify ADW modules import
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && uv run pytest tests/test_config.py -v` - Run configuration tests
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && bash scripts/validate_adw.py` - Run ADW validation script
- `cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder && bash scripts/setup.sh` - Run setup script to verify it works

## Notes

### Project Relationship to tac-7
- `tac-webbuilder` lives within the tac-7 repository under `projects/`
- It shares the same git repository but maintains its own directory structure
- It copies the ADW system rather than importing it, allowing independent evolution
- Future: May extract to separate repository if it grows significantly

### Configuration Design Decisions
- Using Pydantic for robust configuration validation and type safety
- Supporting both YAML files and environment variables for flexibility
- Environment variables take precedence over YAML to allow easy overrides
- Prefix `TWB_` for environment variables to avoid conflicts

### Future Extensions
This foundation supports:
1. **Issue 2**: Natural language processing to convert user input to GitHub issues
2. **Issue 3**: CLI interface for terminal-based interactions
3. **Issue 4**: Web backend API for the web interface
4. **Issue 5**: Web frontend UI for browser-based interactions
5. **Issue 6**: Template system for various issue types and workflows

### Dependencies to Install
Using `uv` for dependency management, the following will be added to `pyproject.toml`:
- `pydantic` - Configuration validation
- `pydantic-settings` - Settings management from environment
- `pyyaml` - YAML configuration file parsing
- `python-dotenv` - .env file loading (may not be needed with pydantic-settings)
- `pytest` - Testing framework (dev dependency)
- `pytest-cov` - Coverage reporting (dev dependency)

### ADW System Independence
While copying the ADW system creates duplication, it provides:
- Independent evolution of tac-webbuilder's workflow needs
- Isolation from changes in tac-7's ADW implementation
- Ability to customize workflows specifically for web interface use cases
- Clear boundaries between projects

Future consideration: Extract ADW to a shared Python package that both projects import.
