#!/bin/bash

################################################################################
# tac-webbuilder Environment Setup Script
#
# This script provides an interactive setup wizard for configuring your
# tac-webbuilder environment variables.
#
# Usage:
#   ./scripts/setup_env.sh
#
# The script will:
# - Check for existing .env file (with overwrite confirmation)
# - Guide you through required configuration
# - Offer optional configuration sections
# - Validate your inputs where possible
# - Create a working .env file
################################################################################

set -e  # Exit on error

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
ENV_SAMPLE="$PROJECT_ROOT/.env.sample"

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  tac-webbuilder Environment Configuration Setup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Check if .env.sample exists
if [ ! -f "$ENV_SAMPLE" ]; then
    echo -e "${RED}Error: .env.sample file not found at $ENV_SAMPLE${NC}"
    exit 1
fi

# Check for existing .env file
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Warning: .env file already exists at $ENV_FILE${NC}"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Setup cancelled. Your existing .env file was not modified.${NC}"
        exit 0
    fi
    echo ""
fi

# Create .env from sample
cp "$ENV_SAMPLE" "$ENV_FILE"
echo -e "${GREEN}✓ Created .env file from template${NC}"
echo ""

################################################################################
# Helper Functions
################################################################################

# Function to update a value in .env file
# Works on both macOS and Linux
update_env_value() {
    local key="$1"
    local value="$2"
    local file="$3"

    # Escape special characters for sed
    local escaped_value=$(echo "$value" | sed 's/[&/\]/\\&/g')

    # Different sed syntax for macOS vs Linux
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|^${key}=.*|${key}=${escaped_value}|" "$file"
    else
        # Linux
        sed -i "s|^${key}=.*|${key}=${escaped_value}|" "$file"
    fi
}

# Function to prompt for a value and update .env
# Usage: prompt_for_value "KEY" "Description" "default_value" "required"
prompt_for_value() {
    local key="$1"
    local description="$2"
    local default="$3"
    local required="$4"

    local prompt_text="$description"
    if [ -n "$default" ]; then
        prompt_text="$prompt_text [default: $default]"
    fi
    if [ "$required" = "true" ]; then
        prompt_text="$prompt_text (REQUIRED)"
    fi
    prompt_text="$prompt_text: "

    while true; do
        read -p "$prompt_text" value

        # Use default if no value provided
        if [ -z "$value" ] && [ -n "$default" ]; then
            value="$default"
        fi

        # Check if required field is empty
        if [ "$required" = "true" ] && [ -z "$value" ]; then
            echo -e "${RED}This field is required. Please provide a value.${NC}"
            continue
        fi

        # If not required and empty, skip
        if [ "$required" = "false" ] && [ -z "$value" ]; then
            echo -e "${YELLOW}Skipping (will use empty value)${NC}"
            return
        fi

        # Update the .env file
        update_env_value "$key" "$value" "$ENV_FILE"
        echo -e "${GREEN}✓ Set $key${NC}"
        return
    done
}

# Function to ask yes/no question
ask_yes_no() {
    local question="$1"
    read -p "$question (y/N): " answer
    [[ "$answer" =~ ^[Yy]$ ]]
}

################################################################################
# Required Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}REQUIRED CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "The following settings are required for basic functionality:"
echo ""

# Anthropic API Key (Required)
echo -e "${YELLOW}1. Anthropic API Key${NC}"
echo "   Get your API key from: https://console.anthropic.com/settings/keys"
prompt_for_value "ANTHROPIC_API_KEY" "Enter your Anthropic API key" "" "true"
echo ""

################################################################################
# Claude Code Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}CLAUDE CODE CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Auto-detect Claude Code path
CLAUDE_PATH=$(which claude 2>/dev/null || echo "")
if [ -n "$CLAUDE_PATH" ]; then
    echo -e "${GREEN}✓ Claude Code found at: $CLAUDE_PATH${NC}"
    update_env_value "CLAUDE_CODE_PATH" "$CLAUDE_PATH" "$ENV_FILE"
    echo ""
else
    echo -e "${YELLOW}Warning: 'claude' command not found in PATH${NC}"
    echo "You may need to install Claude Code: npm install -g @anthropic-ai/claude-code"
    if ask_yes_no "Do you want to specify a custom path to Claude Code?"; then
        prompt_for_value "CLAUDE_CODE_PATH" "Enter full path to Claude Code executable" "claude" "false"
    fi
    echo ""
fi

################################################################################
# Optional Configuration
################################################################################

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}OPTIONAL CONFIGURATION${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "The following settings are optional but enable additional features."
echo ""

# GitHub Configuration
if ask_yes_no "Configure GitHub Personal Access Token?"; then
    echo ""
    echo -e "${YELLOW}GitHub PAT Configuration${NC}"
    echo "   Create a token at: https://github.com/settings/tokens"
    echo "   Required scopes: repo, workflow, read:org"
    echo ""
    prompt_for_value "GITHUB_PAT" "Enter your GitHub Personal Access Token" "" "false"
    echo ""
fi

# OpenAI API Key
if ask_yes_no "Configure OpenAI API Key (for SQL features)?"; then
    echo ""
    echo -e "${YELLOW}OpenAI API Key Configuration${NC}"
    echo "   Get your API key from: https://platform.openai.com/api-keys"
    echo ""
    prompt_for_value "OPENAI_API_KEY" "Enter your OpenAI API key" "" "false"
    echo ""
fi

# E2B API Key
if ask_yes_no "Configure E2B Cloud Sandbox?"; then
    echo ""
    echo -e "${YELLOW}E2B API Key Configuration${NC}"
    echo "   Get your API key from: https://e2b.dev/docs/getting-started/api-key"
    echo ""
    prompt_for_value "E2B_API_KEY" "Enter your E2B API key" "" "false"
    echo ""
fi

# Cloudflare Tunnel
if ask_yes_no "Configure Cloudflare Tunnel (for ADW webhooks)?"; then
    echo ""
    echo -e "${YELLOW}Cloudflare Tunnel Configuration${NC}"
    echo "   Setup guide: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/"
    echo ""
    prompt_for_value "CLOUDFLARED_TUNNEL_TOKEN" "Enter your Cloudflare Tunnel token" "" "false"
    echo ""
fi

# Cloudflare R2
if ask_yes_no "Configure Cloudflare R2 (for screenshot uploads)?"; then
    echo ""
    echo -e "${YELLOW}Cloudflare R2 Configuration${NC}"
    echo "   Setup guide: https://dash.cloudflare.com/?to=/:account/r2"
    echo ""
    prompt_for_value "CLOUDFLARE_ACCOUNT_ID" "Enter your Cloudflare Account ID" "" "false"
    prompt_for_value "CLOUDFLARE_R2_ACCESS_KEY_ID" "Enter your R2 Access Key ID" "" "false"
    prompt_for_value "CLOUDFLARE_R2_SECRET_ACCESS_KEY" "Enter your R2 Secret Access Key" "" "false"
    prompt_for_value "CLOUDFLARE_R2_BUCKET_NAME" "Enter your R2 Bucket Name" "" "false"
    prompt_for_value "CLOUDFLARE_R2_PUBLIC_DOMAIN" "Enter your R2 Public Domain" "" "false"
    echo ""
fi

################################################################################
# Setup Complete
################################################################################

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ Environment Configuration Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Your configuration has been saved to: ${BLUE}$ENV_FILE${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Validate your configuration:"
echo -e "     ${BLUE}./scripts/test_config.sh${NC}"
echo ""
echo "  2. Review the configuration documentation:"
echo -e "     ${BLUE}docs/configuration.md${NC}"
echo ""
echo "  3. Start the application:"
echo -e "     ${BLUE}./scripts/start.sh${NC}"
echo ""
echo -e "${YELLOW}Security Reminder:${NC}"
echo "  - Never commit your .env file to version control"
echo "  - Rotate your API keys regularly (every 90 days recommended)"
echo "  - Keep your credentials secure and private"
echo ""
