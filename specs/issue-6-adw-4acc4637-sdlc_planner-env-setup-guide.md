# Feature: Environment Configuration Setup Guide

## Metadata
issue_number: `6`
adw_id: `4acc4637`
issue_json: `{"number":6,"title":"8-env-setup-guide","body":"# 🎯 ISSUE 8: tac-webbuilder - Environment Configuration Setup Guide\n\n## Overview\nCreate a comprehensive environment setup guide and interactive configuration tool to help users properly configure all required `.env` variables for tac-webbuilder.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory.\n\n## Dependencies\n**Requires**: Issue 1 (Project Foundation) to be completed\n\n## Tasks\n\n### 1. Comprehensive .env.sample File\n**File**: `tac-webbuilder/.env.sample`\n\nBased on tac-7's configuration, create a complete `.env.sample`...(truncated for brevity)"}`

## Feature Description
Create a comprehensive environment configuration setup system that helps users properly configure all required environment variables for the tac-webbuilder application. This includes creating an enhanced `.env.sample` file with detailed documentation, interactive shell scripts for guided setup and validation, comprehensive documentation, and automated tests. The system will make it easy for new users to get started and ensure proper configuration across development teams.

## User Story
As a new developer or team member
I want to easily set up and validate my environment configuration
So that I can start using tac-webbuilder quickly without configuration errors or missing required variables

## Problem Statement
Currently, the project has a basic `.env.sample` file, but it lacks comprehensive documentation, interactive setup guidance, and validation tools. New users must manually figure out which environment variables are required vs optional, where to obtain API keys and credentials, and whether their configuration is correct. This leads to:
- Configuration errors that are only discovered when features are used
- Time wasted troubleshooting missing or incorrect environment variables
- Inconsistent configuration across team members
- No clear guidance on optional vs required settings
- No validation mechanism to catch configuration issues early

## Solution Statement
Build a comprehensive environment configuration system with:
1. **Enhanced `.env.sample`** - Detailed documentation for every variable with clear required/optional markers, descriptions, and links to obtain credentials
2. **Interactive Setup Script** (`scripts/setup_env.sh`) - Guided prompts for required and optional configuration with intelligent defaults
3. **Validation Script** (`scripts/test_config.sh`) - Automated checks for configuration completeness and correctness
4. **Documentation** (`docs/configuration.md`) - Complete reference guide with setup instructions, troubleshooting, and best practices
5. **Automated Tests** - Ensure setup and validation scripts work correctly

This solution provides a smooth onboarding experience, catches configuration errors early, and maintains consistency across development environments.

## Relevant Files
Use these files to implement the feature:

- **README.md** - Main project documentation that needs to be updated with configuration instructions
- **.env.sample** - Root-level environment sample that needs to be enhanced with comprehensive documentation
- **app/server/.env.sample** - Server-specific environment sample that needs to be reviewed for API key documentation
- **scripts/start.sh** - Existing startup script that validates .env presence (reference for validation patterns)
- **scripts/copy_dot_env.sh** - Existing utility for copying env files (reference for similar functionality)
- **.claude/commands/conditional_docs.md** - Documentation guide that may need updates if new docs are added
- **.claude/commands/test_e2e.md** - E2E test runner pattern to follow for validation commands
- **.claude/commands/e2e/test_basic_query.md** - Example E2E test structure for reference

### New Files

- **scripts/setup_env.sh** - Interactive configuration script with guided prompts for all environment variables
- **scripts/test_config.sh** - Validation script that checks configuration completeness and correctness
- **docs/configuration.md** - Comprehensive configuration reference documentation
- **tests/scripts/test_setup_env.sh** - Bash tests for setup script functionality
- **tests/scripts/test_config_validation.py** - Python tests for configuration validation logic
- **.claude/commands/e2e/test_env_setup.md** - E2E test to validate the setup and configuration workflow

## Implementation Plan

### Phase 1: Foundation
Create the core documentation and sample files that will serve as the foundation for the interactive tools. This includes enhancing the `.env.sample` file with comprehensive inline documentation for every environment variable, including clear markers for required vs optional settings, descriptions, default values, and links to obtain credentials. This enhanced sample file becomes the single source of truth for what configuration is needed.

### Phase 2: Core Implementation
Build the interactive setup and validation scripts. The `setup_env.sh` script will provide guided prompts for users to configure their environment, with intelligent defaults, validation of required fields, and optional configuration sections. The `test_config.sh` script will validate that all required settings are present, check that tools (Claude Code, GitHub CLI) are installed and configured, and provide clear error messages and next steps when issues are found.

### Phase 3: Integration
Create comprehensive documentation in `docs/configuration.md` that serves as the complete reference guide. Update the main `README.md` with quick start instructions that reference the new tools. Build automated tests to ensure the setup and validation scripts work correctly. Create an E2E test that validates the complete workflow from initial setup through successful validation.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### Task 1: Create Enhanced .env.sample File
- Read the current `.env.sample` file to understand existing structure
- Read `app/server/.env.sample` to understand application-specific requirements
- Create an enhanced `.env.sample` file in the project root with:
  - Clear section headers for different configuration areas (Anthropic, Claude Code, GitHub, ADW Workflows, Web UI, Cloud Services, Playwright MCP)
  - Detailed inline comments for every variable explaining purpose, requirements, and how to obtain values
  - (REQUIRED) or (Optional) markers for each variable
  - Default values where appropriate
  - Links to documentation and credential sources
  - A quick start checklist at the end
- Ensure backward compatibility with existing configuration

### Task 2: Create Interactive Setup Script
- Create `scripts/setup_env.sh` with:
  - Shebang and error handling (`set -e`)
  - Check for existing `.env` file with overwrite confirmation
  - `prompt_for_value()` function that handles required/optional fields and updates `.env`
  - OS-specific `sed` handling (macOS vs Linux)
  - Prompts for required configuration (ANTHROPIC_API_KEY)
  - Auto-detection of CLAUDE_CODE_PATH using `which claude`
  - Optional configuration sections with user confirmation
  - Clear success message and next steps
- Make the script executable with `chmod +x`
- Test that it creates valid `.env` files

### Task 3: Create Configuration Validation Script
- Create `scripts/test_config.sh` with:
  - Check that `.env` file exists
  - Load environment variables from `.env`
  - `check_required()` and `check_optional()` functions that track errors/warnings
  - Validation of required settings (ANTHROPIC_API_KEY)
  - Validation of tool availability (Claude Code, GitHub CLI)
  - Validation of authentication status (gh auth status)
  - Checks for optional cloud services (E2B, Cloudflare Tunnel, R2)
  - Validation of Playwright MCP configuration files
  - Summary report with error/warning counts
  - Appropriate exit codes (0 for success, 1 for errors)
- Make the script executable with `chmod +x`
- Test with various configuration scenarios

### Task 4: Create E2E Test for Setup Workflow
- Create `.claude/commands/e2e/test_env_setup.md` with:
  - User story describing the setup experience
  - Test steps that validate:
    - Running `setup_env.sh` with interactive prompts
    - Creating `.env` file with correct values
    - Running `test_config.sh` to validate configuration
    - Handling missing required fields
    - Handling optional configuration sections
  - Success criteria for complete setup workflow
  - Screenshot capture points for documentation
- Follow the structure from `test_basic_query.md`

### Task 5: Create Comprehensive Configuration Documentation
- Create `docs/configuration.md` with:
  - Overview section explaining the configuration system
  - Quick setup instructions (3 steps: run setup, verify, or manual)
  - Detailed documentation for every environment variable organized by category:
    - Description, default value, example, how to obtain
  - Cloud services setup guides with step-by-step instructions
  - Troubleshooting section for common issues
  - Best practices for security, performance, and development
  - Environment variables reference table
- Ensure all information is accurate and matches `.env.sample`

### Task 6: Create Automated Tests for Setup Scripts
- Create `tests/scripts/` directory if it doesn't exist
- Create `tests/scripts/test_setup_env.sh`:
  - Test that setup script creates `.env` file
  - Test that ANTHROPIC_API_KEY is set correctly
  - Test with default values
  - Test overwrite protection
- Create `tests/scripts/test_config_validation.py`:
  - Test validation fails without `.env` file
  - Test validation passes with valid configuration
  - Test error/warning detection
  - Test exit codes
- Make test scripts executable

### Task 7: Update README.md with Configuration Section
- Read the current README.md to understand structure
- Add a new "Configuration" section after "Setup" with:
  - Quick setup command (`./scripts/setup_env.sh`)
  - Verification command (`./scripts/test_config.sh`)
  - Reference to full documentation (`docs/configuration.md`)
- Keep the existing environment configuration section but add references to new tools
- Ensure the documentation flow is logical

### Task 8: Update Conditional Docs (if needed)
- Read `.claude/commands/conditional_docs.md`
- Add entry for `docs/configuration.md` if documentation about configuration system is needed:
  - When working with environment variables
  - When troubleshooting configuration issues
  - When setting up new development environments

### Task 9: Validation - Run All Validation Commands
- Execute all validation commands listed in the "Validation Commands" section
- Ensure zero regressions in existing functionality
- Verify all new scripts work correctly
- Run the E2E test for the setup workflow
- Fix any issues discovered during validation

## Testing Strategy

### Unit Tests

**Setup Script Tests** (`tests/scripts/test_setup_env.sh`):
- Creates `.env` file from `.env.sample`
- Sets ANTHROPIC_API_KEY correctly
- Handles default values
- Protects against overwriting without confirmation
- Updates existing variables correctly

**Validation Script Tests** (`tests/scripts/test_config_validation.py`):
- Detects missing `.env` file
- Validates required variables are set
- Checks tool availability (Claude Code, gh CLI)
- Reports errors and warnings correctly
- Returns appropriate exit codes

### Integration Tests

**E2E Setup Workflow Test** (`.claude/commands/e2e/test_env_setup.md`):
- Complete setup workflow from start to finish
- Interactive prompts and user inputs
- Configuration validation
- Error handling and recovery

### Edge Cases

- **Missing .env file**: Validation script provides clear error and instructions
- **Invalid API keys**: Validation script detects empty required fields
- **Missing tools**: Validation detects missing Claude Code or GitHub CLI
- **Partial configuration**: Optional fields can be skipped without errors
- **Overwrite protection**: Setup script confirms before overwriting existing `.env`
- **Platform differences**: Scripts handle macOS and Linux sed differences
- **Authentication issues**: Validation detects when GitHub CLI is not authenticated
- **Invalid file paths**: Setup script validates CLAUDE_CODE_PATH exists

## Acceptance Criteria

- ✅ `.env.sample` file contains comprehensive documentation for all environment variables with clear required/optional markers
- ✅ `scripts/setup_env.sh` guides users through interactive configuration with intelligent defaults
- ✅ `scripts/test_config.sh` validates configuration and reports errors/warnings clearly
- ✅ `docs/configuration.md` provides complete reference documentation for all configuration options
- ✅ README.md includes clear instructions for using the new configuration tools
- ✅ All scripts are executable and handle errors gracefully
- ✅ Scripts work correctly on both macOS and Linux
- ✅ Required fields are enforced while optional fields can be skipped
- ✅ Validation script detects missing tools and authentication issues
- ✅ Automated tests pass for setup and validation scripts
- ✅ E2E test validates complete setup workflow
- ✅ Documentation includes troubleshooting guides and best practices
- ✅ Security best practices are documented (never commit .env, rotate keys, etc.)
- ✅ All existing functionality continues to work without regression

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute the new `.claude/commands/e2e/test_env_setup.md` E2E test file to validate the setup workflow
- `./scripts/test_config.sh` - Validate current configuration passes all checks
- `cd tests/scripts && ./test_setup_env.sh` - Validate setup script creates correct configuration
- `cd tests/scripts && uv run pytest test_config_validation.py` - Validate configuration validation logic
- `cd app/server && uv run pytest` - Run server tests to validate zero regressions
- `cd app/client && bun tsc --noEmit` - Run TypeScript checks to validate zero regressions
- `cd app/client && bun run build` - Build frontend to validate zero regressions

## Notes

### Implementation Considerations
- This feature is primarily documentation and tooling, not application functionality changes
- Scripts should be idempotent (safe to run multiple times)
- Follow existing script patterns from `scripts/start.sh` and `scripts/copy_dot_env.sh`
- Use consistent error messaging and color coding (GREEN, BLUE, RED, YELLOW)
- Platform compatibility is important (macOS vs Linux, especially for `sed` commands)

### Future Enhancements
- Interactive validation with prompts to fix detected issues
- Support for `.env.local` for local overrides
- Environment variable encryption for sensitive values
- Integration with secret management tools (1Password, AWS Secrets Manager)
- Docker-based development environment configuration
- CI/CD environment configuration validation

### Related Documentation
- [ADW README](adws/README.md) - ADW system documentation
- [Scripts README](scripts/README.md) - If created in future
- [Troubleshooting Guide](docs/troubleshooting.md) - If created in future

### Security Notes
- Scripts must never log or display sensitive values (API keys, tokens)
- `.env` file should be in `.gitignore` (already configured)
- Documentation emphasizes never committing `.env` to version control
- Recommend regular API key rotation
- Emphasize minimum required token scopes for GitHub PAT

### Dependencies on Other Issues
- This issue can be implemented independently
- Works well in parallel with Issue 1 (Project Foundation)
- Setup scripts will be useful for all subsequent development work
