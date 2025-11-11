# E2E Test: CLI Interface

## User Story
As a developer using tac-webbuilder, I want to verify that the CLI interface works correctly end-to-end, including launching the CLI, viewing help, checking configuration, viewing history, and accessing interactive mode.

## Test Environment
- **Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`
- **Test Type**: End-to-end CLI functionality test
- **Prerequisites**:
  - Dependencies installed (`uv sync` completed)
  - CLI package built and available
  - No GitHub authentication required for basic commands

## Test Steps

### 1. Test CLI Module Entry Point
**Purpose**: Verify CLI can be launched via Python module

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli --help
```

**Expected Output**:
- Exit code: 0
- Output contains: "webbuilder" and command descriptions
- Shows available commands: request, interactive, history, config, integrate, new, version

### 2. Test Convenience Script
**Purpose**: Verify launch script works correctly

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_cli.sh --help
```

**Expected Output**:
- Exit code: 0
- Same help output as module entry point

### 3. Test Version Command
**Purpose**: Verify version information displays correctly

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli version
```

**Expected Output**:
- Exit code: 0
- Output contains: "tac-webbuilder CLI version 0.1.0"

### 4. Test History Command (Empty)
**Purpose**: Verify history works even with no entries

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli history
```

**Expected Output**:
- Exit code: 0
- Output contains: "No history found" or displays empty table
- No errors

### 5. Test Config List Command
**Purpose**: Verify configuration can be listed

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli config list
```

**Expected Output**:
- Exit code: 0
- Displays configuration table with keys like:
  - github.default_repo
  - github.auto_post
  - adw.default_workflow
  - interfaces.cli.enabled
- Shows config file location

### 6. Test Config Get Command
**Purpose**: Verify individual config values can be retrieved

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli config get adw.default_workflow
```

**Expected Output**:
- Exit code: 0
- Output contains the config value (e.g., "adw_sdlc_iso")

### 7. Test Config Validate Command
**Purpose**: Verify configuration validation works

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli config validate
```

**Expected Output**:
- Exit code: 0
- Output contains: "Configuration is valid" or specific validation errors

### 8. Test Request Command Help
**Purpose**: Verify request command has proper documentation

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli request --help
```

**Expected Output**:
- Exit code: 0
- Shows command description and usage
- Lists options: --project, --auto-post
- Shows examples

### 9. Test Interactive Command Help
**Purpose**: Verify interactive command has proper documentation

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli interactive --help
```

**Expected Output**:
- Exit code: 0
- Describes interactive mode functionality
- Mentions menu-driven interface

### 10. Test History Command with Limit
**Purpose**: Verify history limit option works

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli history --limit 25
```

**Expected Output**:
- Exit code: 0
- Command executes without error

### 11. Test New Command (Stub)
**Purpose**: Verify stub commands show appropriate messages

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli new testproject 2>&1 | head -20
```

**Expected Output**:
- Exit code: 1 (not implemented)
- Output contains: "not yet implemented" or "coming soon"

### 12. Test Integrate Command (Stub)
**Purpose**: Verify integrate stub shows appropriate message

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
uv run python -m interfaces.cli integrate /tmp 2>&1 | head -20
```

**Expected Output**:
- Exit code: 1 (not implemented)
- Output contains: "not yet implemented" or "coming soon"

## Success Criteria

All tests must pass with the following conditions:
-  CLI can be launched via both `python -m interfaces.cli` and `./scripts/start_cli.sh`
-  Help text is comprehensive and properly formatted
-  Version command displays correct version
-  History command works even with no entries
-  Config commands (list, get, validate) execute successfully
-  All commands have proper help documentation
-  Stub commands show appropriate "coming soon" messages
-  No Python exceptions or stack traces for normal operations
-  Exit codes are correct (0 for success, 1 for expected failures)

## Notes

- This test does NOT require GitHub authentication
- This test does NOT attempt to post issues to GitHub
- Interactive mode is not tested (requires user input)
- Request command with actual issue creation is not tested (requires GitHub setup)
- These are basic smoke tests to ensure the CLI infrastructure works

## Cleanup

No cleanup required - all commands are read-only or modify only config files.

## Related Tests

- Unit tests: `tests/interfaces/test_cli_main.py`
- Integration tests would require GitHub authentication setup
