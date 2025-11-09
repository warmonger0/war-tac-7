# Feature: tac-webbuilder - Project Foundation & Core Infrastructure

## Metadata
issue_number: `1`
adw_id: `787fcff4`
issue_json: `{"number":1,"title":"create-tac-webbuilder-issue1","body":"\n# 🎯 ISSUE 1: tac-webbuilder - Project Foundation & Core Infrastructure\n\n## Overview\nCreate the foundational project structure for `tac-webbuilder` at `/Users/Warmonger0/tac/tac-webbuilder` and copy/adapt the ADW workflow system from tac-7.\n\n## Tasks\n\n### 1. Create Project Structure\n```\n/Users/Warmonger0/tac/tac-webbuilder/\n├── README.md\n├── .env.sample\n├── .gitignore\n├── core/\n│   ├── __init__.py\n│   └── config.py\n├── interfaces/\n│   ├── cli/\n│   └── web/\n├── adws/\n│   ├── README.md\n│   └── adw_modules/\n├── .claude/\n│   ├── commands/\n│   ├── hooks/\n│   └── settings.json\n├── templates/\n├── scripts/\n├── logs/\n├── agents/\n└── trees/\n```\n\n### 2. Copy ADW System from tac-7\nCopy and adapt these directories from `/Users/Warmonger0/tac/tac-7`:\n- `adws/adw_modules/` → `adws/adw_modules/`\n- `adws/adw_*_iso.py` scripts → `adws/`\n- `adws/adw_triggers/` → `adws/adw_triggers/`\n- `.claude/commands/` → `.claude/commands/`\n- `.claude/hooks/` → `.claude/hooks/`\n- `.claude/settings.json` → `.claude/settings.json`\n\n### 3. Create Configuration System\n**File**: `core/config.py`\n```python\n# Configuration management using Pydantic\n# Support for config.yaml and environment variables\n# GitHub, ADW, interfaces, and Claude settings\n```\n\n**File**: `config.yaml.sample`\n```yaml\ngithub:\n  default_repo: \"owner/tac-webbuilder\"\n  auto_post: false\nadw:\n  default_workflow: \"adw_sdlc_iso\"\n  default_model_set: \"base\"\ninterfaces:\n  cli:\n    enabled: true\n  web:\n    enabled: true\n    port: 5174\n```\n\n### 4. Environment Configuration\n**File**: `.env.sample`\n```bash\nGITHUB_REPO_URL=\"https://github.com/owner/tac-webbuilder\"\nGITHUB_PAT=\"ghp_xxxx\"\nANTHROPIC_API_KEY=\"sk-ant-xxxx\"\nCLAUDE_CODE_PATH=\"/path/to/claude\"\nAUTO_POST_ISSUES=\"false\"\nDEFAULT_WORKFLOW=\"adw_sdlc_iso\"\nWEB_UI_PORT=\"5174\"\n```\n\n### 5. Initialize Git Repository\n```bash\ncd /Users/Warmonger0/tac/tac-webbuilder\ngit init\ngit add .\ngit commit -m \"Initial project structure\"\n```\n\n### 6. Basic README\nCreate README.md with:\n- Project overview\n- Prerequisites\n- Quick start guide\n- Link to tac-7 for ADW documentation\n\n## Success Criteria\n- ✅ Project directory created at `/Users/Warmonger0/tac/tac-webbuilder`\n- ✅ All ADW modules copied and functional\n- ✅ Configuration system implemented\n- ✅ Git repository initialized\n- ✅ README documents the foundation\n\n## Dependencies\nNone (this is the starting point)\n\n## Next Issues\nAfter this completes, create:\n- **Issue 2**: Natural Language Processing & Issue Formatter\n\n## Workflow\n```\nadw_plan_build_test_iso model_set base\n```\n\n## Labels\n`infrastructure`, `foundation`, `webbuilder`\n"}`

## Feature Description
This feature creates a new standalone project called `tac-webbuilder` with its own foundational structure and a complete copy of the AI Developer Workflow (ADW) system from tac-7. The project will serve as a web-based interface for creating and managing GitHub issues that can be processed by the ADW system. This is the foundational infrastructure that enables all future tac-webbuilder development.

## User Story
As a developer working on multiple TAC projects
I want a dedicated tac-webbuilder project with its own ADW system
So that I can build web-based tools for managing GitHub issues and ADW workflows independently from tac-7

## Problem Statement
Currently, there is no web-based interface for creating and formatting GitHub issues that work with the ADW system. To build such a tool (tac-webbuilder), we need a completely separate project with its own infrastructure, including a full copy of the ADW automation system that can process issues independently.

## Solution Statement
Create a new project at `/Users/Warmonger0/tac/tac-webbuilder` with a complete directory structure that includes:
1. Core configuration management using Pydantic and YAML
2. A full copy of the ADW workflow system from tac-7
3. Infrastructure for CLI and web interfaces
4. Proper Git initialization and documentation
5. Environment configuration for GitHub, Anthropic, and Claude integrations

This foundation will enable future development of web-based issue management tools.

## Relevant Files

### Files to Read (from tac-7 for reference)
- `README.md` - Understand current project structure and patterns
- `adws/README.md` - Deep understanding of ADW system architecture and isolated workflows
- `adws/adw_modules/data_types.py` - Understand ADW data models and state management
- `adws/adw_modules/workflow_ops.py` - Core workflow operations for reference
- `.claude/settings.json` - Claude Code configuration to replicate
- `.gitignore` - Copy ignore patterns to new project

### New Files
All files will be created in the new `/Users/Warmonger0/tac/tac-webbuilder/` directory:

#### Configuration Files
- `core/__init__.py` - Python package marker
- `core/config.py` - Pydantic-based configuration management
- `config.yaml.sample` - Sample YAML configuration
- `.env.sample` - Sample environment variables
- `.gitignore` - Git ignore patterns
- `README.md` - Project documentation

#### Directory Structure
- `interfaces/cli/` - Future CLI interface
- `interfaces/web/` - Future web interface
- `templates/` - Template files storage
- `scripts/` - Utility scripts
- `logs/` - Log files directory
- `agents/` - ADW agent execution logs
- `trees/` - ADW isolated worktrees

#### ADW System (copied from tac-7)
- `adws/README.md` - ADW documentation
- `adws/adw_modules/` - All ADW Python modules
- `adws/adw_*_iso.py` - All ADW workflow scripts
- `adws/adw_triggers/` - Webhook and cron triggers
- `adws/adw_tests/` - ADW test suite

#### Claude Code Configuration (copied from tac-7)
- `.claude/settings.json` - Claude Code settings
- `.claude/commands/` - All slash commands
- `.claude/hooks/` - All hook scripts

## Implementation Plan

### Phase 1: Foundation - Directory Creation
Create the base directory structure at `/Users/Warmonger0/tac/tac-webbuilder` with all required subdirectories including core, interfaces, adws, .claude, templates, scripts, logs, agents, and trees.

### Phase 2: Core Implementation - Copy ADW System
Copy the complete ADW system from `/Users/Warmonger0/tac/tac-7` including:
- All adws modules and scripts
- All .claude commands and hooks
- ADW triggers and test infrastructure
- Maintain file permissions and structure

### Phase 3: Integration - Configuration and Documentation
Create the configuration system with Pydantic models, set up environment files, initialize Git repository, and write comprehensive documentation that links back to tac-7 for ADW details.

## Step by Step Tasks

### 1. Create Base Directory Structure
- Create main project directory at `/Users/Warmonger0/tac/tac-webbuilder`
- Create subdirectories: `core/`, `interfaces/cli/`, `interfaces/web/`, `templates/`, `scripts/`, `logs/`, `agents/`, `trees/`
- Create Python package markers (`__init__.py`) where needed

### 2. Copy ADW System from tac-7
- Copy entire `adws/` directory from tac-7 to tac-webbuilder preserving structure
- Copy entire `.claude/` directory from tac-7 to tac-webbuilder
- Verify all Python scripts have correct permissions (executable for `.py` files)
- Verify all shell scripts have executable permissions

### 3. Create Core Configuration System
- Create `core/__init__.py` as empty package marker
- Create `core/config.py` with Pydantic models for:
  - GitHub settings (repo URL, PAT, auto_post flag)
  - ADW settings (default workflow, model set)
  - Interface settings (CLI and web configurations)
  - Environment variable loading with python-dotenv
- Use Pydantic BaseSettings for automatic environment variable integration
- Support both config.yaml and environment variables with env vars taking precedence

### 4. Create Configuration Templates
- Create `config.yaml.sample` with example configuration for GitHub, ADW, and interfaces
- Create `.env.sample` with all required environment variables as templates
- Include clear comments explaining each configuration option
- Document which variables are required vs optional

### 5. Create .gitignore File
- Copy base patterns from tac-7's .gitignore
- Add Python-specific ignores: `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/`
- Add environment and config ignores: `.env`, `config.yaml`
- Add ADW-specific ignores: `agents/*/`, `trees/*/`, `logs/*.log`
- Add IDE ignores: `.vscode/`, `.idea/`, `*.swp`

### 6. Create Project README.md
- Write project overview explaining tac-webbuilder's purpose
- List prerequisites: Python 3.10+, uv, GitHub CLI, Claude Code CLI
- Provide setup instructions for installing dependencies and configuring environment
- Include quick start guide referencing tac-7/adws/README.md for detailed ADW documentation
- Document project structure with explanations
- Add links to tac-7 repository for ADW documentation

### 7. Initialize Git Repository
- Run `git init` in `/Users/Warmonger0/tac/tac-webbuilder`
- Add all files to staging with `git add .`
- Create initial commit with message: "Initial project structure for tac-webbuilder"
- Verify git status shows clean working directory

### 8. Create pyproject.toml for Dependencies
- Create `pyproject.toml` with project metadata
- Add dependencies: pydantic, pydantic-settings, python-dotenv, pyyaml
- Configure uv package management
- Set Python version requirement (>=3.10)

### 9. Validate ADW System Integrity
- Verify all ADW scripts are present and executable
- Check that adw_modules imports work correctly
- Verify .claude/commands and .claude/hooks are complete
- Test that configuration system loads properly

### 10. Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify project structure is correct
- Test configuration loading
- Validate Git repository initialization

## Testing Strategy

### Unit Tests
Since this is infrastructure setup, traditional unit tests are not applicable. However, we will perform validation tests:

1. **Directory Structure Validation**:
   - Verify all required directories exist
   - Check that Python package markers are in place
   - Validate file permissions

2. **Configuration System Tests**:
   - Test config.py can load from environment variables
   - Test config.py can load from YAML file
   - Verify environment variable precedence over YAML
   - Test missing required variables raise appropriate errors

3. **ADW System Integrity**:
   - Verify all ADW Python modules import successfully
   - Check that all ADW scripts are present
   - Validate .claude commands structure

4. **Git Repository Tests**:
   - Verify git repository is initialized
   - Check that .gitignore is working correctly
   - Validate initial commit exists

### Edge Cases
1. **Directory Already Exists**: Handle case where `/Users/Warmonger0/tac/tac-webbuilder` already exists
2. **Permission Issues**: Handle file permission errors during copy operations
3. **Missing Source Files**: Verify all source files in tac-7 exist before copying
4. **Invalid Configuration**: Test behavior with malformed YAML or missing env vars
5. **Import Errors**: Handle cases where copied Python modules have import issues

## Acceptance Criteria
1. ✅ Directory `/Users/Warmonger0/tac/tac-webbuilder` exists with complete structure
2. ✅ All subdirectories (core, interfaces, adws, .claude, templates, scripts, logs, agents, trees) are created
3. ✅ Complete ADW system copied from tac-7 with all modules, scripts, triggers, and tests
4. ✅ All .claude commands and hooks copied and preserved
5. ✅ Configuration system (core/config.py) implemented with Pydantic models
6. ✅ config.yaml.sample and .env.sample files created with proper documentation
7. ✅ .gitignore file created with appropriate patterns
8. ✅ README.md written with comprehensive documentation
9. ✅ pyproject.toml created with correct dependencies
10. ✅ Git repository initialized with initial commit
11. ✅ All Python files have correct imports and no syntax errors
12. ✅ File permissions preserved for executable scripts
13. ✅ Configuration system can load from both environment variables and YAML
14. ✅ Documentation clearly links to tac-7 for detailed ADW information

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

Since this creates a NEW project outside the current repository, validation commands will verify the setup:

```bash
# Verify directory structure
ls -la /Users/Warmonger0/tac/tac-webbuilder
ls -la /Users/Warmonger0/tac/tac-webbuilder/core
ls -la /Users/Warmonger0/tac/tac-webbuilder/adws
ls -la /Users/Warmonger0/tac/tac-webbuilder/.claude

# Verify ADW system is complete
find /Users/Warmonger0/tac/tac-webbuilder/adws -name "adw_*_iso.py" | wc -l  # Should match tac-7 count
find /Users/Warmonger0/tac/tac-webbuilder/.claude/commands -name "*.md" | wc -l  # Should match tac-7 count

# Verify Python imports work
cd /Users/Warmonger0/tac/tac-webbuilder && python3 -c "from core.config import *"
cd /Users/Warmonger0/tac/tac-webbuilder && python3 -c "from adws.adw_modules import data_types, workflow_ops"

# Verify Git repository
cd /Users/Warmonger0/tac/tac-webbuilder && git status
cd /Users/Warmonger0/tac/tac-webbuilder && git log --oneline | head -1

# Verify configuration files exist
test -f /Users/Warmonger0/tac/tac-webbuilder/config.yaml.sample && echo "config.yaml.sample exists"
test -f /Users/Warmonger0/tac/tac-webbuilder/.env.sample && echo ".env.sample exists"
test -f /Users/Warmonger0/tac/tac-webbuilder/.gitignore && echo ".gitignore exists"
test -f /Users/Warmonger0/tac/tac-webbuilder/README.md && echo "README.md exists"
test -f /Users/Warmonger0/tac/tac-webbuilder/pyproject.toml && echo "pyproject.toml exists"

# Count directory structure
find /Users/Warmonger0/tac/tac-webbuilder -type d | wc -l  # Should have substantial directory count

# Verify no syntax errors in core module
cd /Users/Warmonger0/tac/tac-webbuilder && python3 -m py_compile core/config.py
```

Note: Traditional pytest/tsc/build commands don't apply here as this task creates a NEW project foundation, not modifying existing app/server or app/client code.

## Notes

### Important Considerations
1. **New Project Context**: This task creates a completely new project at `/Users/Warmonger0/tac/tac-webbuilder`, separate from the current tac-7 repository
2. **ADW System Duplication**: The entire ADW system is being copied, not shared, so tac-webbuilder will have its own independent ADW automation
3. **No Server/Client**: This foundation does NOT include the FastAPI/Vite application from tac-7. It's purely infrastructure for future web-based issue management tools
4. **Configuration Flexibility**: The Pydantic-based config system should support both YAML files and environment variables, with env vars taking precedence
5. **Future Extensibility**: The interfaces/cli and interfaces/web directories are placeholders for future development

### Dependencies to Install
When implementing, use `uv` to add:
- `pydantic>=2.0` - For configuration models
- `pydantic-settings>=2.0` - For environment variable integration
- `python-dotenv` - For .env file loading
- `pyyaml` - For YAML configuration file support

### File Permissions
Ensure the following files remain executable after copying:
- All `adws/adw_*_iso.py` scripts
- All `adws/adw_triggers/*.py` scripts
- All `.claude/hooks/*.py` scripts
- Any shell scripts in `scripts/` directory

### Links to tac-7
The README should clearly document that:
- ADW system documentation is in `/Users/Warmonger0/tac/tac-7/adws/README.md`
- ADW examples and usage can be found in tac-7 repository
- tac-webbuilder inherits the ADW system but will extend it for web-based issue management

### Future Development Path
After this foundation is complete, the next steps will be:
1. Natural language processing for issue formatting
2. Web UI for creating formatted issues
3. Integration with GitHub API for posting issues
4. ADW workflow triggers from web interface
