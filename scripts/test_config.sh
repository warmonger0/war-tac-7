#!/bin/bash

################################################################################
# tac-webbuilder Configuration Validation Script
#
# This script validates your tac-webbuilder environment configuration.
# It checks for:
# - Required environment variables
# - Tool availability (Claude Code, GitHub CLI)
# - Authentication status
# - Optional configuration completeness
#
# Usage:
#   ./scripts/test_config.sh
#
# Exit codes:
#   0 - All checks passed
#   1 - One or more errors found
################################################################################

# Don't exit on error - we want to check all validations
set +e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"
ENV_FILE="$PROJECT_ROOT/.env"

# Counters for errors and warnings
ERROR_COUNT=0
WARNING_COUNT=0

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  tac-webbuilder Configuration Validation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

################################################################################
# Check .env file exists
################################################################################

if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}✗ Error: .env file not found at $ENV_FILE${NC}"
    echo ""
    echo "To create your .env file, either:"
    echo "  1. Run the interactive setup: ./scripts/setup_env.sh"
    echo "  2. Copy manually: cp .env.sample .env"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"
echo ""

################################################################################
# Load environment variables
################################################################################

# Load .env file
set -a  # Export all variables
source "$ENV_FILE"
set +a  # Stop exporting

################################################################################
# Helper Functions
################################################################################

# Function to check required variable
check_required() {
    local var_name="$1"
    local var_value="${!var_name}"
    local description="$2"

    if [ -z "$var_value" ]; then
        echo -e "${RED}✗ $description ($var_name) is not set${NC}"
        ((ERROR_COUNT++))
        return 1
    else
        echo -e "${GREEN}✓ $description is set${NC}"
        return 0
    fi
}

# Function to check optional variable
check_optional() {
    local var_name="$1"
    local var_value="${!var_name}"
    local description="$2"

    if [ -z "$var_value" ]; then
        echo -e "${YELLOW}○ $description ($var_name) is not set (optional)${NC}"
        ((WARNING_COUNT++))
        return 1
    else
        echo -e "${GREEN}✓ $description is set${NC}"
        return 0
    fi
}

# Function to check command availability
check_command() {
    local cmd="$1"
    local description="$2"
    local install_hint="$3"

    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓ $description is installed${NC}"
        return 0
    else
        echo -e "${RED}✗ $description is not installed${NC}"
        if [ -n "$install_hint" ]; then
            echo -e "   ${YELLOW}Install: $install_hint${NC}"
        fi
        ((ERROR_COUNT++))
        return 1
    fi
}

################################################################################
# Validate Required Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}REQUIRED CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Anthropic API Key
check_required "ANTHROPIC_API_KEY" "Anthropic API Key"
echo ""

################################################################################
# Validate Tool Availability
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}REQUIRED TOOLS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Claude Code
if [ -n "$CLAUDE_CODE_PATH" ]; then
    if [ -x "$CLAUDE_CODE_PATH" ] || command -v "$CLAUDE_CODE_PATH" &> /dev/null; then
        echo -e "${GREEN}✓ Claude Code is available at: $CLAUDE_CODE_PATH${NC}"
    else
        echo -e "${RED}✗ Claude Code not found at specified path: $CLAUDE_CODE_PATH${NC}"
        echo -e "   ${YELLOW}Try running: which claude${NC}"
        ((ERROR_COUNT++))
    fi
else
    check_command "claude" "Claude Code" "npm install -g @anthropic-ai/claude-code"
fi
echo ""

# Check GitHub CLI
check_command "gh" "GitHub CLI" "https://cli.github.com/"

# Check GitHub authentication if gh is available
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✓ GitHub CLI is authenticated${NC}"
    else
        echo -e "${RED}✗ GitHub CLI is not authenticated${NC}"
        echo -e "   ${YELLOW}Run: gh auth login${NC}"
        ((ERROR_COUNT++))
    fi
fi
echo ""

################################################################################
# Validate Optional Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}OPTIONAL CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# GitHub PAT
check_optional "GITHUB_PAT" "GitHub Personal Access Token"

# OpenAI API Key
check_optional "OPENAI_API_KEY" "OpenAI API Key"

# E2B API Key
check_optional "E2B_API_KEY" "E2B API Key"

# Cloudflare Tunnel
check_optional "CLOUDFLARED_TUNNEL_TOKEN" "Cloudflare Tunnel Token"

echo ""

################################################################################
# Validate Cloudflare R2 Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}CLOUDFLARE R2 CONFIGURATION (Optional)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if any R2 variables are set
R2_VARS_SET=0
[ -n "$CLOUDFLARE_ACCOUNT_ID" ] && ((R2_VARS_SET++))
[ -n "$CLOUDFLARE_R2_ACCESS_KEY_ID" ] && ((R2_VARS_SET++))
[ -n "$CLOUDFLARE_R2_SECRET_ACCESS_KEY" ] && ((R2_VARS_SET++))
[ -n "$CLOUDFLARE_R2_BUCKET_NAME" ] && ((R2_VARS_SET++))
[ -n "$CLOUDFLARE_R2_PUBLIC_DOMAIN" ] && ((R2_VARS_SET++))

if [ $R2_VARS_SET -eq 0 ]; then
    echo -e "${YELLOW}○ Cloudflare R2 not configured (all variables empty)${NC}"
    echo -e "   Screenshots will use local file paths instead"
elif [ $R2_VARS_SET -eq 5 ]; then
    echo -e "${GREEN}✓ Cloudflare R2 fully configured${NC}"
else
    echo -e "${YELLOW}⚠ Cloudflare R2 partially configured ($R2_VARS_SET/5 variables set)${NC}"
    echo -e "   ${YELLOW}For R2 to work, all 5 variables must be set:${NC}"
    check_optional "CLOUDFLARE_ACCOUNT_ID" "  - Account ID"
    check_optional "CLOUDFLARE_R2_ACCESS_KEY_ID" "  - Access Key ID"
    check_optional "CLOUDFLARE_R2_SECRET_ACCESS_KEY" "  - Secret Access Key"
    check_optional "CLOUDFLARE_R2_BUCKET_NAME" "  - Bucket Name"
    check_optional "CLOUDFLARE_R2_PUBLIC_DOMAIN" "  - Public Domain"
fi
echo ""

################################################################################
# Validate Playwright MCP Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}PLAYWRIGHT MCP CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

PLAYWRIGHT_CONFIG="$PROJECT_ROOT/playwright-mcp-config.json"
if [ -f "$PLAYWRIGHT_CONFIG" ]; then
    echo -e "${GREEN}✓ Playwright MCP configuration file found${NC}"

    # Check if videos directory exists (from config)
    VIDEOS_DIR="$PROJECT_ROOT/videos"
    if [ -d "$VIDEOS_DIR" ]; then
        echo -e "${GREEN}✓ Videos directory exists${NC}"
    else
        echo -e "${YELLOW}○ Videos directory will be created when needed${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Playwright MCP configuration file not found${NC}"
    echo -e "   ${YELLOW}Expected at: $PLAYWRIGHT_CONFIG${NC}"
    ((WARNING_COUNT++))
fi
echo ""

################################################################################
# Summary Report
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}VALIDATION SUMMARY${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $ERROR_COUNT -eq 0 ] && [ $WARNING_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Your configuration is complete.${NC}"
    EXIT_CODE=0
elif [ $ERROR_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠ Configuration valid with $WARNING_COUNT warning(s)${NC}"
    echo -e "   Optional features may not be available"
    EXIT_CODE=0
else
    echo -e "${RED}✗ Configuration incomplete: $ERROR_COUNT error(s), $WARNING_COUNT warning(s)${NC}"
    EXIT_CODE=1
fi

echo ""
echo -e "${YELLOW}Errors:${NC}   $ERROR_COUNT"
echo -e "${YELLOW}Warnings:${NC} $WARNING_COUNT"
echo ""

################################################################################
# Next Steps
################################################################################

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Next Steps:${NC}"
    echo "  - Start the application: ./scripts/start.sh"
    echo "  - Read the documentation: docs/configuration.md"
    echo "  - Run E2E tests: .claude/commands/test_e2e.md"
else
    echo -e "${YELLOW}To Fix Issues:${NC}"
    echo "  1. Run the setup script: ./scripts/setup_env.sh"
    echo "  2. Edit .env manually: nano .env"
    echo "  3. See documentation: docs/configuration.md"
fi
echo ""

exit $EXIT_CODE
