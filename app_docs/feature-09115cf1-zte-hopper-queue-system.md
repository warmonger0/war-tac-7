# ZTE Hopper - Automated Pipeline Queue System

**ADW ID:** 09115cf1
**Date:** 2025-11-10
**Specification:** specs/issue-52-adw-09115cf1-sdlc_planner-zte-hopper-queue-system.md

## Overview

The ZTE Hopper is an automated queue-based system that processes GitHub issues sequentially through Zero Touch Execution (ZTE) workflows. It eliminates the need for manual issue creation and monitoring by automatically processing markdown files dropped into a queue directory, creating GitHub issues, waiting for ADW completion, validating results, and archiving completed work.

## What Was Built

- **Queue-based processing system** with FIFO ordering by file creation timestamp
- **GitHub issue creation script** (`scripts/gi`) that wraps `gh issue create` and auto-triggers ZTE workflows
- **Main hopper script** (`scripts/zte_hopper.sh`) with 696 lines implementing all queue processing logic
- **Comprehensive validation system** with pre-flight and post-completion sanity checks
- **State management** using persistent state file tracking current progress
- **Process management** with PID file enforcement, graceful shutdown, and stop signals
- **Logging system** with automatic log rotation keeping last 10 logs
- **Directory structure** with queue/, completed/, and failed/ subdirectories

## Technical Implementation

### Files Modified

- `.mcp.json`: Updated configuration (minor change)
- `scripts/gi`: New 81-line bash script for creating GitHub issues from markdown files
- `scripts/zte_hopper.sh`: New 696-line bash script implementing the complete queue processing system
- `zte-hopper/README.md`: New 518-line comprehensive user documentation
- `zte-hopper/queue/.gitkeep`: Created queue directory for issues waiting to be processed
- `zte-hopper/completed/.gitkeep`: Created directory for successfully completed issues
- `zte-hopper/failed/.gitkeep`: Created directory for failed issues

### Key Changes

**scripts/gi - GitHub Issue Creator**
- Accepts `--title` and `--body-file` parameters
- Reads markdown file and creates GitHub issue
- Automatically appends ZTE workflow trigger (`adw_sdlc_zte_iso`) if not present
- Extracts and returns issue number from gh CLI output
- Includes comprehensive error handling and validation

**scripts/zte_hopper.sh - Queue Processing Engine**
- FIFO queue processing using file creation timestamps (works on both Linux and macOS)
- Pre-flight sanity checks: git worktree cleanliness, uncommitted changes, pull from origin
- Issue creation and workflow triggering using `scripts/gi`
- Polling mechanism checking every 30 seconds with 2-hour timeout
- Post-completion validation: issue closed, ZTE completion marker, SDLC phases, clean worktree
- Success/failure handling with automatic file movement
- State management with persistent `.hopper_state` file
- Single-instance enforcement using PID file
- Graceful shutdown with signal handlers (SIGINT/SIGTERM)
- Stop signal support via `.stop` file
- Comprehensive logging with automatic rotation

**Queue Processing Logic**
```bash
while queue is not empty:
    1. Get oldest file from queue/ (FIFO)
    2. Run pre-flight checks (git status, pull latest)
    3. Extract title from markdown (first # heading)
    4. Create GitHub issue via ./scripts/gi
    5. Wait for issue to close (poll every 30s, max 2 hours)
    6. Run post-completion validation:
       - Issue closed on GitHub
       - Contains "Zero Touch Execution Complete" marker
       - All SDLC phases completed (plan, build, test, review, doc, ship)
       - Git worktree is clean
    7. If pass: move to completed/, continue
    8. If fail: move to failed/, STOP processing
```

**Commands Implemented**
- `--work`: Start processing queue (processes all files sequentially)
- `--status`: Show queue status, current progress, and file counts
- `--stop`: Stop after current issue completes (creates `.stop` signal file)
- `--kill`: Kill immediately with graceful shutdown

## How to Use

### Basic Workflow

1. **Prepare issue markdown files** with first-level heading as title:
```markdown
# My Feature Request

This is the issue body with all details.

## Requirements
- Requirement 1
- Requirement 2
```

2. **Add files to queue**:
```bash
# Single issue
cp my-feature.md zte-hopper/queue/

# Multiple issues (will be processed in order by creation time)
cp issue-1.md issue-2.md issue-3.md zte-hopper/queue/
```

3. **Start the hopper**:
```bash
./scripts/zte_hopper.sh --work
```

4. **Monitor progress**:
```bash
# Check status in another terminal
./scripts/zte_hopper.sh --status

# View logs
tail -f zte-hopper/logs/hopper-*.log
```

5. **Stop gracefully** (finishes current issue):
```bash
./scripts/zte_hopper.sh --stop
```

6. **Emergency stop** (immediate):
```bash
./scripts/zte_hopper.sh --kill
```

### Issue File Requirements

- Must be `.md` extension
- Must have a first-level heading (`# Title`) as the first heading
- Heading text becomes the GitHub issue title
- File contents become the issue body
- ZTE workflow trigger is automatically added by `scripts/gi`

## Configuration

### Timeouts and Intervals

Configured in `scripts/zte_hopper.sh`:
- `POLL_INTERVAL=30` - Check issue status every 30 seconds
- `TIMEOUT_SECONDS=7200` - Maximum 2 hours per issue
- `MAX_POLLS=240` - Maximum poll attempts (timeout / interval)

### Directory Locations

- Queue: `zte-hopper/queue/`
- Completed: `zte-hopper/completed/`
- Failed: `zte-hopper/failed/`
- Logs: `zte-hopper/logs/`
- State: `zte-hopper/.hopper_state`
- PID: `zte-hopper/.hopper.pid`
- Stop signal: `zte-hopper/.stop`

### Log Rotation

Automatically keeps last 10 log files, deleting older ones.

## Testing

### Manual Testing

```bash
# 1. Create test issue file
cat > zte-hopper/queue/test-issue.md << 'EOF'
# Test Issue for ZTE Hopper

This is a test issue to validate the hopper works correctly.

## Test Details
- Should create issue on GitHub
- Should trigger ZTE workflow
- Should validate completion
EOF

# 2. Start hopper
./scripts/zte_hopper.sh --work

# 3. Monitor in another terminal
watch ./scripts/zte_hopper.sh --status

# 4. Check logs
tail -f zte-hopper/logs/hopper-*.log
```

### Validation Commands

```bash
# Verify directory structure
ls -la zte-hopper/queue/ zte-hopper/completed/ zte-hopper/failed/

# Check scripts are executable
test -x scripts/zte_hopper.sh && echo "hopper executable"
test -x scripts/gi && echo "gi executable"

# Test FIFO ordering
touch zte-hopper/queue/first.md
sleep 1
touch zte-hopper/queue/second.md
# Verify oldest (first.md) is selected
find zte-hopper/queue/ -type f -name "*.md" -exec stat -f '%m %N' {} \; | sort -n | head -1

# Verify script structure
grep -c "^[a-z_]*() {" scripts/zte_hopper.sh  # Should show many functions
wc -l scripts/zte_hopper.sh  # Should be ~696 lines
```

## Notes

### Safety Features

- **Single-instance enforcement**: Prevents multiple hopper processes from running simultaneously using PID file
- **Graceful shutdown**: Handles SIGINT/SIGTERM signals, cleans up state and PID files
- **Stop-after-current**: Creates `.stop` file to stop after current issue completes
- **Timeout protection**: Maximum 2-hour wait per issue prevents infinite waits
- **Git integration**: Auto-pulls between issues to stay current with main branch
- **Comprehensive validation**: Multi-point checks ensure issues actually completed successfully

### Failure Handling

When an issue fails validation:
1. Issue file is moved to `zte-hopper/failed/` with timestamp
2. Detailed error logged to log file
3. Hopper stops processing (exits with error code)
4. User must investigate failure, fix issue, and manually restart

### State File Format

The `.hopper_state` file uses bash-sourceable format:
```bash
STATE="RUNNING"
ISSUE_NUMBER="123"
ISSUE_FILE="/path/to/issue.md"
TIMESTAMP="1699632145"
```

### Completion Detection

The hopper validates ZTE completion through multiple indicators:
1. Issue state is CLOSED on GitHub
2. Last comment contains "Zero Touch Execution Complete" or "Code has been shipped"
3. All SDLC phases present in comments: plan, build, test, review, document, ship
4. Git worktree is clean (no uncommitted changes)

### Compatibility

- Works on both Linux (GNU find with -printf) and macOS (BSD find with stat)
- Requires bash 4.0+ for associative arrays and modern bash features
- Uses `set -euo pipefail` for strict error handling

### Integration with ADW System

The hopper complements existing ADW trigger mechanisms:
- **trigger_cron.py**: Monitors existing GitHub issues for "adw" comments
- **trigger_webhook.py**: Responds to GitHub webhook events in real-time
- **ZTE Hopper**: Creates new issues from local markdown files, processes sequentially

They can run simultaneously without conflict.

### Future Enhancements

Documented but not implemented:
- Real-time web visualization dashboard
- Live cost monitoring per issue
- Webhook integration (GitHub webhook triggers next issue)
- Parallel processing for independent issues
- Priority queue support
- Dry-run mode for testing without creating real issues
