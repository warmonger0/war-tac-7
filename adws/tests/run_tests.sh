#!/bin/bash
# Test runner for ADW optimization tests

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}ADW Optimization Test Suite${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}✗ pytest not found${NC}"
    echo "Installing pytest..."
    pip install pytest pytest-cov pyyaml
fi

# Change to project root
cd "$PROJECT_ROOT"

# Parse command line arguments
MODE="${1:-all}"

case "$MODE" in
    "unit")
        echo -e "${YELLOW}Running unit tests only...${NC}"
        pytest adws/tests/ -v -m "not integration" --tb=short
        ;;

    "integration")
        echo -e "${YELLOW}Running integration tests only...${NC}"
        pytest adws/tests/ -v -m integration --tb=short
        ;;

    "fast")
        echo -e "${YELLOW}Running fast tests (excluding slow)...${NC}"
        pytest adws/tests/ -v -m "not slow" --tb=short
        ;;

    "coverage")
        echo -e "${YELLOW}Running tests with coverage report...${NC}"
        pytest adws/tests/ -v --cov=adws/adw_modules --cov-report=html --cov-report=term
        echo ""
        echo -e "${GREEN}✓ Coverage report generated at htmlcov/index.html${NC}"
        ;;

    "parser")
        echo -e "${YELLOW}Running plan_parser tests...${NC}"
        pytest adws/tests/test_plan_parser.py -v
        ;;

    "executor")
        echo -e "${YELLOW}Running plan_executor tests...${NC}"
        pytest adws/tests/test_plan_executor.py -v
        ;;

    "watch")
        echo -e "${YELLOW}Running tests in watch mode...${NC}"
        if ! command -v pytest-watch &> /dev/null; then
            pip install pytest-watch
        fi
        pytest-watch adws/tests/ -v
        ;;

    "debug")
        echo -e "${YELLOW}Running tests in debug mode...${NC}"
        pytest adws/tests/ -vv -s --tb=long
        ;;

    "regression")
        echo -e "${YELLOW}Running regression tests...${NC}"
        pytest adws/tests/ -v -m regression --tb=short
        ;;

    "comparison")
        echo -e "${YELLOW}Running workflow comparison tests...${NC}"
        pytest adws/tests/ -v -m comparison -s --tb=short
        ;;

    "all"|*)
        echo -e "${YELLOW}Running all tests...${NC}"
        pytest adws/tests/ -v --tb=short
        ;;
esac

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}======================================${NC}"
else
    echo -e "${RED}======================================${NC}"
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${RED}======================================${NC}"
fi

exit $EXIT_CODE
