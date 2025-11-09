#!/bin/bash
set -e

echo "=========================================="
echo "tac-webbuilder Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for required tools
echo "Checking for required tools..."

# Check for uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv not found${NC}"
    echo "  Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
else
    echo -e "${GREEN}✓ uv found${NC}"
fi

# Check for gh
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠ gh (GitHub CLI) not found${NC}"
    echo "  Install gh: https://cli.github.com/"
    echo "  This is optional but recommended for GitHub integration"
else
    echo -e "${GREEN}✓ gh found${NC}"
fi

# Check for claude
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠ claude not found${NC}"
    echo "  Install Claude Code: https://docs.claude.com/"
    echo "  This is optional but recommended for ADW workflows"
else
    echo -e "${GREEN}✓ claude found${NC}"
fi

echo ""
echo "Configuring environment..."

# Check for .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠ .env file not found${NC}"
    echo "  Copying .env.sample to .env..."
    cp .env.sample .env
    echo -e "${GREEN}✓ Created .env file${NC}"
    echo "  ${YELLOW}Please edit .env and add your API keys and configuration${NC}"
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Check for config.yaml
if [ ! -f config.yaml ]; then
    echo -e "${YELLOW}⚠ config.yaml file not found${NC}"
    echo "  Copying config.yaml.sample to config.yaml..."
    cp config.yaml.sample config.yaml
    echo -e "${GREEN}✓ Created config.yaml file${NC}"
    echo "  ${YELLOW}Please edit config.yaml to customize your configuration${NC}"
else
    echo -e "${GREEN}✓ config.yaml file exists${NC}"
fi

echo ""
echo "Installing Python dependencies..."

# Install dependencies with uv
uv sync

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

echo ""
echo "Verifying GitHub authentication..."

# Verify GitHub authentication if gh is available
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✓ GitHub authentication verified${NC}"
    else
        echo -e "${YELLOW}⚠ GitHub not authenticated${NC}"
        echo "  Run: gh auth login"
    fi
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys"
echo "  2. Edit config.yaml to customize your configuration"
echo "  3. Run: uv run python -c \"from core.config import load_config; load_config()\""
echo "  4. Check the README.md for usage instructions"
echo ""
