#!/bin/bash
#
# Start the tac-webbuilder web backend server
#
# This script starts the FastAPI backend server on port 8002 with hot-reload enabled.
# It checks for required environment variables and kills any existing process on the port.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to project root
cd "$(dirname "$0")/.." || exit 1

echo -e "${BLUE}=€ Starting tac-webbuilder Web Backend${NC}"
echo ""

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${YELLOW}   Warning: ANTHROPIC_API_KEY not set${NC}"
    echo "   Set it in .env file or export it"
fi

if [ -z "$GITHUB_REPO_URL" ] && [ -z "$TWB_GITHUB_REPO_URL" ]; then
    echo -e "${YELLOW}   Warning: GITHUB_REPO_URL not set${NC}"
    echo "   Set it in .env file or export it"
fi

# Load environment variables from .env if it exists
if [ -f .env ]; then
    echo -e "${GREEN}${NC} Loading environment from .env"
    export $(grep -v '^#' .env | xargs)
fi

# Get port from environment or use default
PORT=${TWB_WEB_BACKEND_PORT:-8002}
HOST=${TWB_WEB_BACKEND_HOST:-0.0.0.0}

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}   Port $PORT is already in use${NC}"
    echo -e "${YELLOW}   Killing existing process...${NC}"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 1
fi

echo -e "${GREEN}${NC} Port $PORT is available"
echo ""
echo -e "${BLUE}Starting FastAPI server on ${HOST}:${PORT}${NC}"
echo -e "${BLUE}API Documentation: http://localhost:${PORT}/docs${NC}"
echo -e "${BLUE}WebSocket endpoint: ws://localhost:${PORT}/ws${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the server
uv run uvicorn interfaces.web.server:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload \
    --log-level info

# Capture exit code
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}${NC} Server stopped gracefully"
else
    echo -e "${RED}${NC} Server stopped with error (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE
