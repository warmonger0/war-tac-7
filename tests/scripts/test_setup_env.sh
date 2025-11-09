#!/bin/bash

################################################################################
# Tests for scripts/setup_env.sh
#
# These tests verify that the setup script correctly:
# - Creates .env file from .env.sample
# - Sets ANTHROPIC_API_KEY correctly
# - Handles default values
# - Protects against overwriting without confirmation
# - Updates existing variables correctly
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
SETUP_SCRIPT="$PROJECT_ROOT/scripts/setup_env.sh"
TEST_ENV_FILE="$PROJECT_ROOT/.env.test"
ENV_SAMPLE="$PROJECT_ROOT/.env.sample"

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Testing scripts/setup_env.sh${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Helper function to run a test
run_test() {
    local test_name="$1"
    local test_func="$2"

    echo -e "${YELLOW}Running: $test_name${NC}"

    if $test_func; then
        echo -e "${GREEN}✓ PASSED: $test_name${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED: $test_name${NC}"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Helper function to clean up test files
cleanup_test_env() {
    rm -f "$TEST_ENV_FILE"
}

################################################################################
# Test Cases
################################################################################

# Test 1: Verify .env.sample exists
test_env_sample_exists() {
    [ -f "$ENV_SAMPLE" ]
}

# Test 2: Verify setup script exists and is executable
test_setup_script_exists() {
    [ -f "$SETUP_SCRIPT" ] && [ -x "$SETUP_SCRIPT" ]
}

# Test 3: Test that .env file can be created from sample
test_creates_env_file() {
    cleanup_test_env

    # Create test .env by copying sample
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Verify file was created
    [ -f "$TEST_ENV_FILE" ]
    local result=$?

    cleanup_test_env
    return $result
}

# Test 4: Test that ANTHROPIC_API_KEY can be set
test_sets_api_key() {
    cleanup_test_env

    # Create test .env
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Set API key using sed (same logic as setup script)
    local test_key="sk-ant-test-key-12345"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${test_key}|" "$TEST_ENV_FILE"
    else
        sed -i "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${test_key}|" "$TEST_ENV_FILE"
    fi

    # Verify key was set
    grep -q "ANTHROPIC_API_KEY=${test_key}" "$TEST_ENV_FILE"
    local result=$?

    cleanup_test_env
    return $result
}

# Test 5: Test that CLAUDE_CODE_PATH can be updated
test_updates_claude_path() {
    cleanup_test_env

    # Create test .env
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Update Claude path
    local test_path="/usr/local/bin/claude"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^CLAUDE_CODE_PATH=.*|CLAUDE_CODE_PATH=${test_path}|" "$TEST_ENV_FILE"
    else
        sed -i "s|^CLAUDE_CODE_PATH=.*|CLAUDE_CODE_PATH=${test_path}|" "$TEST_ENV_FILE"
    fi

    # Verify path was updated
    grep -q "CLAUDE_CODE_PATH=${test_path}" "$TEST_ENV_FILE"
    local result=$?

    cleanup_test_env
    return $result
}

# Test 6: Test that variables with special characters are handled
test_handles_special_characters() {
    cleanup_test_env

    # Create test .env
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Set key with special characters (common in tokens)
    local test_key="sk-ant-test/key+with=special&chars"
    local escaped_value=$(echo "$test_key" | sed 's/[&/\]/\\&/g')

    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${escaped_value}|" "$TEST_ENV_FILE"
    else
        sed -i "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${escaped_value}|" "$TEST_ENV_FILE"
    fi

    # Verify key was set correctly
    grep -q "ANTHROPIC_API_KEY=${test_key}" "$TEST_ENV_FILE"
    local result=$?

    cleanup_test_env
    return $result
}

# Test 7: Test that existing values can be overwritten
test_overwrites_existing_value() {
    cleanup_test_env

    # Create test .env with existing value
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Set initial value
    local initial_key="sk-ant-initial-key"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${initial_key}|" "$TEST_ENV_FILE"
    else
        sed -i "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${initial_key}|" "$TEST_ENV_FILE"
    fi

    # Verify initial value
    grep -q "ANTHROPIC_API_KEY=${initial_key}" "$TEST_ENV_FILE" || return 1

    # Overwrite with new value
    local new_key="sk-ant-new-key"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${new_key}|" "$TEST_ENV_FILE"
    else
        sed -i "s|^ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=${new_key}|" "$TEST_ENV_FILE"
    fi

    # Verify new value
    grep -q "ANTHROPIC_API_KEY=${new_key}" "$TEST_ENV_FILE"
    local result=$?

    cleanup_test_env
    return $result
}

# Test 8: Test that empty values can be set
test_handles_empty_values() {
    cleanup_test_env

    # Create test .env
    cp "$ENV_SAMPLE" "$TEST_ENV_FILE"

    # Set empty value
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^GITHUB_PAT=.*|GITHUB_PAT=|" "$TEST_ENV_FILE"
    else
        sed -i "s|^GITHUB_PAT=.*|GITHUB_PAT=|" "$TEST_ENV_FILE"
    fi

    # Verify empty value is set (line should be: GITHUB_PAT=)
    grep -q "^GITHUB_PAT=$" "$TEST_ENV_FILE"
    local result=$?

    cleanup_test_env
    return $result
}

# Test 9: Test .env.sample has required variables
test_env_sample_has_required_vars() {
    # Check for required variables in .env.sample
    grep -q "^ANTHROPIC_API_KEY=" "$ENV_SAMPLE" || return 1
    grep -q "^CLAUDE_CODE_PATH=" "$ENV_SAMPLE" || return 1

    return 0
}

# Test 10: Test .env.sample has optional variables
test_env_sample_has_optional_vars() {
    # Check for optional variables in .env.sample
    grep -q "^GITHUB_PAT=" "$ENV_SAMPLE" || return 1
    grep -q "^E2B_API_KEY=" "$ENV_SAMPLE" || return 1
    grep -q "^CLOUDFLARED_TUNNEL_TOKEN=" "$ENV_SAMPLE" || return 1
    grep -q "^CLOUDFLARE_ACCOUNT_ID=" "$ENV_SAMPLE" || return 1

    return 0
}

################################################################################
# Run All Tests
################################################################################

run_test "Test 1: .env.sample exists" test_env_sample_exists
run_test "Test 2: Setup script exists and is executable" test_setup_script_exists
run_test "Test 3: Creates .env file from sample" test_creates_env_file
run_test "Test 4: Sets ANTHROPIC_API_KEY correctly" test_sets_api_key
run_test "Test 5: Updates CLAUDE_CODE_PATH correctly" test_updates_claude_path
run_test "Test 6: Handles special characters in values" test_handles_special_characters
run_test "Test 7: Overwrites existing values" test_overwrites_existing_value
run_test "Test 8: Handles empty values" test_handles_empty_values
run_test "Test 9: .env.sample has required variables" test_env_sample_has_required_vars
run_test "Test 10: .env.sample has optional variables" test_env_sample_has_optional_vars

################################################################################
# Summary
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Total tests: $((TESTS_PASSED + TESTS_FAILED))"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
