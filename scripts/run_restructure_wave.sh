#!/bin/bash
set -e

# Run restructure issues sequentially with validation
# Usage: ./scripts/run_restructure_wave.sh [starting-issue]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Issue definitions (title, body-file, description)
declare -a ISSUES=(
    "Integration Cleanup|issue-10c-integration-cleanup-v2.md|Wave 1: Cleanup old directories"
    "Documentation Structure|issue-11a-documentation-structure-v2.md|Wave 2: Create doc structure"
    "Move Docs & Specs|issue-11b-move-docs-specs-v2.md|Wave 2: Move documentation"
    "Move Issue Files|issue-11c-move-issue-files-v2.md|Wave 2: Move issue files"
    "Dependency Audit|issue-12a-dependency-audit-v2.md|Wave 3: Audit dependencies"
    "Extraction Tooling|issue-12b-extraction-tooling-v2.md|Wave 3: Create extraction scripts"
    "Final Validation|issue-12c-final-validation-v2.md|Wave 3: Final validation"
)

# Get starting index
START_INDEX=0
if [ -n "$1" ]; then
    START_INDEX=$1
    echo -e "${BLUE}ℹ️  Starting from issue index ${START_INDEX}${NC}"
fi

# Track overall progress
TOTAL_ISSUES=${#ISSUES[@]}
COMPLETED=0
FAILED=0

echo ""
echo "🚀 Restructure Wave Execution"
echo "=============================="
echo ""
echo "Total issues: ${TOTAL_ISSUES}"
echo "Starting from: ${START_INDEX}"
echo ""

# Function to check git worktree is clean
check_worktree_clean() {
    echo -e "${BLUE}🔍 Checking git worktree status...${NC}"

    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${RED}❌ Working tree has uncommitted changes${NC}"
        echo ""
        git status --short
        return 1
    fi

    # Check for untracked files (excluding known dirs)
    UNTRACKED=$(git ls-files --others --exclude-standard | grep -v "^archive/" | grep -v "^logs/" | grep -v "^trees/" | grep -v "^agents/" || true)
    if [ -n "$UNTRACKED" ]; then
        echo -e "${YELLOW}⚠️  Found untracked files (excluding logs/trees/agents):${NC}"
        echo "$UNTRACKED"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi

    echo -e "${GREEN}✅ Working tree is clean${NC}"
    return 0
}

# Function to wait for issue to complete
wait_for_issue() {
    local issue_number=$1
    local max_wait=3600  # 1 hour max
    local elapsed=0
    local check_interval=30

    echo -e "${BLUE}⏳ Waiting for issue #${issue_number} to complete...${NC}"

    while [ $elapsed -lt $max_wait ]; do
        # Check issue state
        STATE=$(gh issue view "$issue_number" --json state --jq '.state' 2>/dev/null || echo "UNKNOWN")

        if [ "$STATE" = "CLOSED" ]; then
            echo -e "${GREEN}✅ Issue #${issue_number} closed${NC}"
            return 0
        elif [ "$STATE" = "UNKNOWN" ]; then
            echo -e "${RED}❌ Could not query issue #${issue_number}${NC}"
            return 1
        fi

        # Check if workflow is still running (look for recent comments)
        RECENT_COMMENT=$(gh issue view "$issue_number" --json comments --jq '.comments[-1].body' 2>/dev/null || echo "")

        if [[ "$RECENT_COMMENT" == *"Zero Touch Execution Complete"* ]] || [[ "$RECENT_COMMENT" == *"Code has been shipped"* ]]; then
            echo -e "${GREEN}✅ Workflow completed for issue #${issue_number}${NC}"
            # Wait a bit for issue to close
            sleep 10
            return 0
        fi

        echo -n "."
        sleep $check_interval
        elapsed=$((elapsed + check_interval))
    done

    echo ""
    echo -e "${RED}❌ Timeout waiting for issue #${issue_number}${NC}"
    return 1
}

# Main execution loop
cd "$REPO_ROOT"

for i in $(seq $START_INDEX $((TOTAL_ISSUES - 1))); do
    IFS='|' read -r TITLE BODY_FILE DESCRIPTION <<< "${ISSUES[$i]}"

    ISSUE_NUM=$((i + 1))
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}📋 Issue ${ISSUE_NUM}/${TOTAL_ISSUES}: ${TITLE}${NC}"
    echo "   ${DESCRIPTION}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Pre-flight check
    if ! check_worktree_clean; then
        echo -e "${RED}❌ Pre-flight check failed${NC}"
        FAILED=$((FAILED + 1))

        echo ""
        read -p "Skip this issue and continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            continue
        else
            echo -e "${RED}❌ Wave execution stopped${NC}"
            exit 1
        fi
    fi

    # Pull latest changes
    echo -e "${BLUE}🔄 Pulling latest changes...${NC}"
    git pull --ff-only origin main || {
        echo -e "${RED}❌ Failed to pull latest changes${NC}"
        exit 1
    }

    # Create and trigger issue
    echo ""
    echo -e "${GREEN}🚀 Creating issue: ${TITLE}${NC}"
    echo ""

    ISSUE_OUTPUT=$("${SCRIPT_DIR}/gi" --title "$TITLE" --body-file "$BODY_FILE" 2>&1)
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "$ISSUE_OUTPUT"
        echo ""
        echo -e "${RED}❌ Failed to create issue${NC}"
        FAILED=$((FAILED + 1))
        exit 1
    fi

    # Extract issue number
    ISSUE_NUMBER=$(echo "$ISSUE_OUTPUT" | grep -o "https://github.com/[^/]*/[^/]*/issues/[0-9]*" | grep -o "[0-9]*$" | head -1)

    if [ -z "$ISSUE_NUMBER" ]; then
        echo "$ISSUE_OUTPUT"
        echo ""
        echo -e "${RED}❌ Could not extract issue number${NC}"
        FAILED=$((FAILED + 1))
        exit 1
    fi

    echo "$ISSUE_OUTPUT"
    echo ""
    echo -e "${GREEN}✅ Issue #${ISSUE_NUMBER} created and workflow triggered${NC}"
    echo ""

    # Wait for completion
    if wait_for_issue "$ISSUE_NUMBER"; then
        COMPLETED=$((COMPLETED + 1))
        echo ""
        echo -e "${GREEN}✅ Issue ${ISSUE_NUM}/${TOTAL_ISSUES} completed successfully${NC}"

        # Brief pause before next issue
        echo ""
        echo "Waiting 10 seconds before next issue..."
        sleep 10
    else
        echo ""
        echo -e "${RED}❌ Issue ${ISSUE_NUM}/${TOTAL_ISSUES} failed or timed out${NC}"
        FAILED=$((FAILED + 1))

        echo ""
        read -p "Continue with next issue? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}❌ Wave execution stopped${NC}"
            exit 1
        fi
    fi
done

# Final summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Restructure Wave Execution Complete"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total issues: ${TOTAL_ISSUES}"
echo -e "${GREEN}✅ Completed: ${COMPLETED}${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}❌ Failed: ${FAILED}${NC}"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎊 All issues completed successfully!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some issues had problems${NC}"
    exit 1
fi
