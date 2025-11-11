# Extraction and Validation Tooling

**ADW ID:** 5b192684
**Date:** November 11, 2025
**Specification:** specs/issue-65-adw-5b192684-sdlc_planner-extraction-validation-tooling.md

## Overview

This feature provides automated extraction and validation tooling to enable the tac-webbuilder project to be extracted as a standalone, portable project. It includes validation scripts to ensure projects are self-contained with no parent path dependencies, and extraction scripts to automate the process of copying, initializing, and setting up extracted projects in new locations.

## What Was Built

- **Validation Script** (`validate_standalone.sh`) - Comprehensive validation tool that checks project integrity
- **Extraction Script** (`extract_project.sh`) - Automated extraction tool for creating standalone project copies
- **Configuration Samples** - Updated `.env.sample` and new `config.yaml.sample` with relative paths
- **Unit Tests** (`test_extraction_validation.py`) - Pytest-based tests for validation logic
- **Documentation Updates** - Updated project configuration files for standalone deployment

## Technical Implementation

### Files Modified

- `scripts/validate_standalone.sh`: New validation script (45 lines) that checks directory structure, parent path references, Python imports, and script permissions
- `scripts/extract_project.sh`: New extraction script (69 lines) that automates pre-flight checks, file copying, git initialization, and dependency installation
- `.env.sample`: Added `PROJECT_ROOT=.` and `CONFIG_FILE=./config.yaml` for standalone project configuration (11 lines added)
- `config.yaml.sample`: New configuration template (19 lines) with relative paths for project root, trees_dir, and logs_dir
- `tests/test_extraction_validation.py`: New test suite (132 lines) with 9 test cases covering validation logic
- `scripts/expose_webhook.sh`: File permissions updated (mode change)
- `scripts/run_restructure_wave.sh`: File permissions updated (mode change)
- `.mcp.json`: Minor configuration update (2 lines changed)
- `playwright-mcp-config.json`: Minor configuration update (2 lines changed)

### Key Changes

1. **Standalone Validation** - Automated checks ensure projects have no dependencies on parent monorepo structure by validating directory structure, detecting parent path references, verifying Python imports, and checking script permissions

2. **Automated Extraction** - Single-command extraction process with intelligent file copying (excludes .git, node_modules, .venv, caches), git initialization with clean history, configuration file setup, and dependency installation for both Python and Node.js

3. **Relative Path Configuration** - Sample configuration files use relative paths (`.` for project root, `./trees`, `./logs`) to support standalone deployment without hardcoded absolute paths

4. **Comprehensive Testing** - Unit tests validate directory structure checking, parent path reference detection, script permission validation, and extraction pre-flight checks using pytest fixtures

5. **Error Handling** - Both scripts use `set -e` for immediate error termination, provide clear error messages with emoji indicators, track error counts, and exit with appropriate status codes

## How to Use

### Validating Current Project

To validate that your current project is standalone and has no parent dependencies:

```bash
./scripts/validate_standalone.sh
```

The script will check:
- Required directory structure (app, scripts, tests, adws)
- No parent path references in Python/Markdown files
- Python imports work correctly
- All shell scripts are executable

### Extracting to New Location

To extract the project to a new standalone location:

```bash
./scripts/extract_project.sh /path/to/destination
```

The script will:
1. Validate source location (must be run from project root)
2. Check destination doesn't already exist
3. Copy files with intelligent exclusions
4. Initialize new git repository
5. Create configuration files from samples
6. Set up Python virtual environment
7. Install Node.js dependencies
8. Provide next-steps guidance

### After Extraction

Navigate to the extracted project and validate:

```bash
cd /path/to/destination
./scripts/validate_standalone.sh
./scripts/start_full.sh
```

## Configuration

### .env Configuration

The `.env.sample` file now includes standalone project configuration:

```bash
# Project root directory (relative path for standalone)
PROJECT_ROOT=.

# Configuration file path (relative path for standalone)
CONFIG_FILE=./config.yaml
```

Copy `.env.sample` to `.env` and customize as needed.

### config.yaml Configuration

The `config.yaml.sample` provides a template for project configuration:

```yaml
project:
  root: .

adw:
  trees_dir: ./trees
  logs_dir: ./logs
```

Copy `config.yaml.sample` to `config.yaml` and customize paths if needed.

## Testing

### Running Unit Tests

The test suite validates the validation and extraction logic:

```bash
cd app/server
uv run pytest tests/test_extraction_validation.py -v
```

Test coverage includes:
- Directory structure validation (valid and missing directories)
- Parent path reference detection (with and without references)
- Script permission validation (executable and non-executable)
- Extraction pre-flight checks (source validation, destination checking)

### Integration Testing

For end-to-end testing of the extraction process:

```bash
# Test extraction to temporary location
./scripts/extract_project.sh /tmp/test-extract-$(date +%s)
cd /tmp/test-extract-*

# Validate extracted project
./scripts/validate_standalone.sh

# Test configuration files
ls -la .env config.yaml
grep "PROJECT_ROOT" .env
cat config.yaml

# Cleanup
cd ..
rm -rf test-extract-*
```

## Notes

### Script Requirements

Both scripts require:
- Bash 4+ with `set -e` and `[[` conditional support
- `python3` in PATH for validation checks
- `uv` installed for Python environment setup (extraction only)
- `npm` installed for Node.js dependencies (extraction only)
- `rsync` for efficient file copying (extraction only)

### Exclusion Patterns

The extraction script excludes:
- Version control: `.git`
- Dependencies: `node_modules`, `.venv`
- Build artifacts: `__pycache__`, `*.pyc`, `.DS_Store`
- Project-specific: `trees/*`, `logs/*`

### Security Considerations

- The validation script pattern `/Users/Warmonger0/tac/tac-7[^/]` is specific to avoid false positives
- Extracted `.env` files should be added to `.gitignore` to prevent credential exposure
- The extraction script preserves file permissions via rsync

### Future Enhancements

- Docker-based extraction (Dockerfile and docker-compose.yml generation)
- TypeScript/JavaScript import path validation
- Branch/tag selection for extraction
- Dry-run mode to preview extraction
- Checksum validation for file integrity
- Subdirectory-only extraction (backend or frontend only)
- Version checks for required tools (uv, npm, python3)
- Progress indicators for long-running operations
