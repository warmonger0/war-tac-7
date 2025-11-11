"""
Test fixtures for ADW optimization tests.

Provides mock data, sample plans, and helper utilities.
"""

import json
import tempfile
import os
from pathlib import Path
from typing import Dict, Any


# Sample GitHub Issues
SAMPLE_ISSUE_TAC7_ROOT = {
    "number": 123,
    "title": "Add logging to ADW workflow",
    "body": """
**Project**: tac-7 (NOT tac-webbuilder)
**Working Directory**: /Users/test/tac-7

Add comprehensive logging to the ADW workflow scripts in `adws/`.

## Requirements
- Add debug logging throughout `adw_plan_iso.py`
- Create log rotation configuration
- Update documentation

## Files
- `adws/adw_plan_iso.py`
- `adws/adw_modules/utils.py`
- `docs/logging.md`
""",
    "state": "open",
    "labels": ["enhancement"],
    "user": {"login": "testuser"}
}

SAMPLE_ISSUE_WEBBUILDER = {
    "number": 456,
    "title": "Fix authentication bug in login flow",
    "body": """
**Project**: tac-webbuilder
**Working Directory**: /Users/test/tac-7/projects/tac-webbuilder

Users are unable to login due to JWT token validation error.

## Steps to Reproduce
1. Navigate to login page
2. Enter valid credentials
3. Click submit
4. Error: "Invalid token signature"

## Expected
User should be logged in successfully

## Technical Details
- Backend: `app/server/core/auth.py`
- Frontend: `app/client/src/api/client.ts`
- Database: User authentication table
""",
    "state": "open",
    "labels": ["bug"],
    "user": {"login": "testuser"}
}

SAMPLE_ISSUE_AMBIGUOUS = {
    "number": 789,
    "title": "Update documentation",
    "body": """
Update the README to reflect recent changes.

## Changes Needed
- Update installation instructions
- Add new environment variables
- Update architecture diagram
""",
    "state": "open",
    "labels": ["documentation"],
    "user": {"login": "testuser"}
}


# Sample AI Responses (Comprehensive Plans)
SAMPLE_PLAN_TAC7_ROOT = """
Here's the comprehensive workflow plan:

```yaml
# WORKFLOW CONFIGURATION

issue_type: feature

project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Issue explicitly states 'NOT tac-webbuilder' and references adws/ directory"

branch_name: feat-issue-123-adw-abc12345-add-logging

commit_message: |
  feat: add logging to ADW workflow

  ADW: abc12345
  Issue: #123

validation_criteria:
  - check: "Branch created"
    expected: "feat-issue-123-adw-abc12345-add-logging"
  - check: "Plan file exists"
    expected: "specs/issue-123-adw-abc12345-sdlc_planner-add-logging.md"
  - check: "No worktree created"
    expected: "Worktree not required"
```

# Feature: Add Logging to ADW Workflow

## Metadata
issue_number: `123`
adw_id: `abc12345`

## Feature Description
Add comprehensive logging throughout the ADW workflow scripts to improve debugging and monitoring.

## Implementation Plan

### Phase 1: Setup Logging Infrastructure
- Configure logging module
- Set up log rotation
- Add debug/info/error levels

### Phase 2: Instrument Code
- Add logging to adw_plan_iso.py
- Add logging to utility modules
- Add logging to agent execution

### Phase 3: Documentation
- Document logging configuration
- Add troubleshooting guide

## Step by Step Tasks

### Task 1: Configure Logging
- Update `adws/adw_modules/utils.py` with logging setup
- Add log rotation configuration
- Configure log levels based on environment

### Task 2: Add Logging Statements
- Instrument `adws/adw_plan_iso.py` with debug/info logs
- Add error logging with stack traces
- Log timing information for performance monitoring

### Task 3: Update Documentation
- Add logging section to README
- Create troubleshooting guide
- Document log file locations

## Validation Commands
- Run workflow and verify logs are created
- Test log rotation
- Verify debug mode works

Plan file: specs/issue-123-adw-abc12345-sdlc_planner-add-logging.md
"""

SAMPLE_PLAN_WEBBUILDER = """
Comprehensive plan created:

```yaml
issue_type: bug

project_context: tac-webbuilder
requires_worktree: true
confidence: high
detection_reasoning: "Issue references app/server and app/client directories, mentions FastAPI and React"

branch_name: fix-issue-456-adw-def67890-authentication-bug

worktree_setup:
  backend_port: 8023
  frontend_port: 5196
  steps:
    - action: create_ports_env
      description: "Create .ports.env with custom ports"
    - action: copy_env_files
      description: "Copy .env files from parent repo"
      fallback: "Use .env.sample if needed"
    - action: copy_mcp_files
      description: "Copy MCP configuration files"
      path_updates:
        - file: .mcp.json
          update: "Update to absolute path"
        - file: playwright-mcp-config.json
          update: "Update videos directory to absolute path"
    - action: install_backend
      command: "cd app/server && uv sync --all-extras"
      working_dir: app/server
    - action: install_frontend
      command: "cd app/client && bun install"
      working_dir: app/client
    - action: setup_database
      command: "./scripts/reset_db.sh"
      working_dir: "."

commit_message: |
  fix: resolve JWT token validation error

  ADW: def67890
  Issue: #456

validation_criteria:
  - check: "Branch created in worktree"
    expected: "fix-issue-456-adw-def67890-authentication-bug"
  - check: "Worktree exists"
    expected: "trees/def67890/ directory"
  - check: "Dependencies installed"
    expected: ".venv and node_modules present"
  - check: "Plan file created"
    expected: "specs/issue-456-adw-def67890-sdlc_planner-authentication-bug.md"
```

# Bug: Fix Authentication Error

## Metadata
issue_number: `456`
adw_id: `def67890`

## Bug Description
JWT token validation failing during login, preventing users from authenticating.

## Root Cause Analysis
The JWT secret key is not being loaded correctly from environment variables.

## Solution
Update auth.py to properly load JWT secret from .env file.

## Implementation
- Fix JWT secret loading in app/server/core/auth.py
- Add validation tests
- Update error messages

Plan file: specs/issue-456-adw-def67890-sdlc_planner-authentication-bug.md
"""


# Mock Execution Results
def create_mock_execution_result(success=True, worktree=False):
    """Create mock ExecutionResult."""
    from adw_modules.plan_executor import ExecutionResult

    result = ExecutionResult()
    result.success = success

    if worktree:
        result.files_created = [
            "trees/abc12345/.ports.env",
            "trees/abc12345/.env",
            "trees/abc12345/app/server/.env",
            "trees/abc12345/.mcp.json",
            "trees/abc12345/playwright-mcp-config.json",
            "specs/issue-123-adw-abc12345-sdlc_planner-feature.md"
        ]
        result.commands_executed = [
            {"command": "uv sync --all-extras", "success": True},
            {"command": "bun install", "success": True},
            {"command": "./scripts/reset_db.sh", "success": True}
        ]
        result.metadata = {
            "worktree_path": "trees/abc12345",
            "backend_port": 8023,
            "frontend_port": 5196
        }
    else:
        result.files_created = [
            "specs/issue-123-adw-abc12345-sdlc_planner-feature.md"
        ]
        result.metadata = {
            "working_directory": "/Users/test/tac-7"
        }

    if not success:
        result.add_error("Mock execution error")

    return result


class MockTempRepo:
    """Create temporary mock repository for testing."""

    def __init__(self):
        self.temp_dir = None
        self.repo_path = None

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir)

        # Create directory structure
        (self.repo_path / "adws").mkdir()
        (self.repo_path / "adws" / "adw_modules").mkdir()
        (self.repo_path / "specs").mkdir()
        (self.repo_path / "trees").mkdir()
        (self.repo_path / "app" / "server").mkdir(parents=True)
        (self.repo_path / "app" / "client").mkdir(parents=True)

        # Create dummy files
        (self.repo_path / ".env.sample").write_text("DATABASE_URL=sqlite:///test.db\n")
        (self.repo_path / "app" / "server" / ".env.sample").write_text("SECRET_KEY=test\n")
        (self.repo_path / ".mcp.json").write_text('{"config": "./playwright-mcp-config.json"}\n')
        (self.repo_path / "playwright-mcp-config.json").write_text('{"dir": "./videos"}\n')

        # Initialize git repo
        os.system(f"cd {self.repo_path} && git init && git config user.email 'test@test.com' && git config user.name 'Test'")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.temp_dir:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_worktree(self, adw_id: str, branch_name: str):
        """Create a mock worktree."""
        worktree_path = self.repo_path / "trees" / adw_id
        worktree_path.mkdir(parents=True, exist_ok=True)

        # Copy structure
        for subdir in ["app/server", "app/client", "specs"]:
            (worktree_path / subdir).mkdir(parents=True, exist_ok=True)

        return str(worktree_path)


def create_mock_issue_json(issue_dict: Dict[str, Any]) -> str:
    """Convert issue dict to JSON string."""
    return json.dumps(issue_dict, indent=2)


# Pytest fixtures
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Export commonly used fixtures
__all__ = [
    'SAMPLE_ISSUE_TAC7_ROOT',
    'SAMPLE_ISSUE_WEBBUILDER',
    'SAMPLE_ISSUE_AMBIGUOUS',
    'SAMPLE_PLAN_TAC7_ROOT',
    'SAMPLE_PLAN_WEBBUILDER',
    'create_mock_execution_result',
    'MockTempRepo',
    'create_mock_issue_json'
]
