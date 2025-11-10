# Environment Setup Scripts

**ADW ID:** f4d9b5e1
**Date:** 2025-11-10
**Specification:** specs/issue-30-adw-f4d9b5e1-sdlc_planner-env-setup-scripts.md

## Overview

Created interactive environment configuration scripts for tac-webbuilder that provide a guided setup experience for new users. The feature includes a comprehensive `.env.sample` file with detailed documentation, an interactive setup script that walks users through configuration, and a validation script that checks configuration correctness and system prerequisites.

## What Was Built

- **Comprehensive .env.sample file** - Documents all environment variables with clear required/optional labels, inline comments, credential source URLs, and a quick start checklist
- **Interactive setup script** (`scripts/setup_env.sh`) - Guides users through environment configuration with intelligent defaults, optional sections, and cross-platform compatibility
- **Configuration validation script** (`scripts/test_config.sh`) - Validates required variables, tool installations, authentication status, and provides actionable error messages
- **Test scripts** - Automated tests for setup and validation script functionality
- **Updated README** - Documentation for using the new setup and validation tools

## Technical Implementation

### Files Modified

- `.env.sample` (118 lines added) - Expanded with comprehensive documentation organized by category (Anthropic, Claude Code, GitHub, ADW, Web UI, Cloud Services)
- `scripts/setup_env.sh` (173 lines, new file) - Interactive bash script with prompt_for_value function, macOS/Linux sed compatibility, and nested optional configuration sections
- `scripts/test_config.sh` (164 lines, new file) - Validation script with check_required/check_optional functions, tool verification, and summary reporting
- `README.md` (44 lines modified) - Added sections for interactive setup, manual setup, and configuration validation with clear examples
- `tests/scripts/test_setup_env.sh` (30 lines, new file) - Bash test script for setup functionality
- `tests/scripts/test_config_validation.py` (22 lines, new file) - Python pytest tests for validation script

### Key Changes

- **Interactive prompting system**: `prompt_for_value()` function handles required/optional fields with validation, defaults, and cross-platform sed updates
- **Intelligent defaults**: Automatically detects Claude Code path with `which claude` fallback
- **Organized configuration flow**: Separates required configuration from optional sections with skip capability
- **Comprehensive validation**: Checks not just environment variables, but also tool installations (Claude Code, GitHub CLI), authentication status, and configuration file presence
- **Excellent UX**: Uses emojis, clear formatting, progress indicators, and actionable error messages with remediation steps
- **Cross-platform compatibility**: Handles macOS (`sed -i ''`) and Linux (`sed -i`) differences with `$OSTYPE` detection

## How to Use

### Interactive Setup (Recommended)

1. Navigate to the tac-webbuilder directory
2. Run the interactive setup script:
   ```bash
   ./scripts/setup_env.sh
   ```
3. Follow the prompts:
   - Enter your Anthropic API key (required)
   - Confirm or modify Claude Code path (auto-detected)
   - Choose whether to configure optional settings
   - If configuring optionals, select which services to set up (GitHub, ADW, Web UI, Cloud services)
4. Review the created `.env` file
5. Run validation to verify configuration

### Validation

After setup (or anytime you modify `.env`), validate your configuration:

```bash
./scripts/test_config.sh
```

The validation script will:
- Check all required variables are set
- Verify Claude Code is installed and accessible
- Check GitHub CLI installation and authentication status
- Validate optional service configurations if provided
- Provide a summary with error/warning counts and actionable next steps

### Manual Setup

If you prefer manual configuration:

1. Copy the sample file:
   ```bash
   cp .env.sample .env
   ```
2. Edit `.env` and fill in values following the inline documentation
3. Run validation to check your configuration:
   ```bash
   ./scripts/test_config.sh
   ```

## Configuration

### Required Variables

- `ANTHROPIC_API_KEY` - Your Anthropic API key from https://console.anthropic.com/settings/keys

### Optional Variables

**Claude Code:**
- `CLAUDE_CODE_PATH` - Path to Claude Code binary (default: `claude`)
- `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` - Keep Claude in project root (recommended: `true`)

**GitHub:**
- `GITHUB_PAT` - Personal access token (if not using `gh auth login`)
- `GITHUB_REPO_URL` - Default repository (format: `owner/repo`)
- `AUTO_POST_ISSUES` - Auto-post issues without confirmation (default: `false`)

**ADW Workflow:**
- `DEFAULT_WORKFLOW` - Default workflow (options: `adw_sdlc_iso`, `adw_plan_build_test_iso`, `adw_build_iso`)
- `DEFAULT_MODEL_SET` - Default model set (options: `base`, `heavy`)

**Web UI:**
- `WEB_UI_PORT` - Frontend port (default: `5174`)
- `WEB_API_PORT` - Backend API port (default: `8002`)

**Cloud Services:**
- `E2B_API_KEY` - E2B cloud sandbox key from https://e2b.dev/docs
- `CLOUDFLARED_TUNNEL_TOKEN` - Cloudflare Tunnel token for webhooks
- `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_R2_ACCESS_KEY_ID`, `CLOUDFLARE_R2_SECRET_ACCESS_KEY`, `CLOUDFLARE_R2_BUCKET_NAME`, `CLOUDFLARE_R2_PUBLIC_DOMAIN` - R2 configuration for screenshot uploads

## Testing

### Manual Testing

Test the setup script:
```bash
# Interactive test (will prompt for input)
./scripts/setup_env.sh

# Test validation
./scripts/test_config.sh
```

### Automated Testing

Run the test scripts:
```bash
# Bash test for setup script
./tests/scripts/test_setup_env.sh

# Python pytest for validation script
cd app/server && uv run pytest tests/scripts/test_config_validation.py
```

## Notes

- **Cross-platform compatibility**: Scripts detect macOS vs Linux and use appropriate sed syntax
- **Overwrite protection**: Setup script prompts before overwriting existing `.env` file
- **Idempotent validation**: Validation script is safe to run repeatedly without side effects
- **Clear error messages**: Both scripts provide actionable error messages with remediation steps
- **Conditional R2 check**: R2 configuration is only validated if any R2 variable is set, avoiding noise for users who don't need it
- **Exit codes**: Validation script exits with code 1 on errors, 0 on success or warnings only
- **GitHub authentication**: Scripts support both `gh auth login` (recommended) and `GITHUB_PAT` environment variable
- **Quick start checklist**: `.env.sample` includes a checklist at the bottom to guide new users through the setup process
- **Executable by default**: Scripts include `chmod +x` permissions and proper bash shebangs

## Benefits

### For New Users
- Reduces setup time from hours (with documentation lookup and troubleshooting) to minutes
- Eliminates guessing about which configuration is required vs optional
- Provides immediate feedback on configuration errors
- Includes links to get all necessary credentials

### For Teams
- `.env.sample` serves as living documentation of all configuration options
- Consistent configuration structure across team members
- Validation prevents common setup mistakes before they cause runtime errors
- Easy to share and maintain configuration standards

### For Development
- Quick verification that environment is correctly configured
- Catches missing tools or authentication issues early
- Scripts make onboarding new developers faster and more reliable
- Supports both interactive and non-interactive workflows
