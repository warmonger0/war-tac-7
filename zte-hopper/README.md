# ZTE Hopper - Automated Pipeline Queue System

The ZTE Hopper is an automated queue system that processes GitHub issues sequentially through Zero Touch Execution (ZTE) workflows with comprehensive validation between each issue.

## Overview

ZTE Hopper enables batch processing of multiple GitHub issues without manual intervention. Simply drop markdown files into the queue directory, run a single command, and the system will:

1. Process issues in FIFO order (oldest first)
2. Automatically create GitHub issues with ZTE workflow triggers
3. Wait for each issue to complete (polling every 30 seconds)
4. Validate completion with comprehensive sanity checks
5. Move completed issues to the `completed/` directory
6. Stop immediately if any issue fails validation

This transforms a manual, monitoring-intensive process into a fully automated pipeline ideal for processing large batches of related changes.

## Directory Structure

```
zte-hopper/
├── queue/          # Issues waiting to be processed (FIFO by creation date)
├── completed/      # Successfully completed and validated issues
├── failed/         # Issues that failed validation (timestamped)
├── logs/           # Execution logs (kept last 10)
├── .hopper_state   # Current processing state (auto-generated)
├── .hopper.pid     # Running process ID (auto-generated)
└── README.md       # This file
```

## Setup

### Prerequisites

1. **Git repository** - Must run from repository root with `.git` directory
2. **GitHub CLI** - `gh` command must be installed and authenticated
3. **ZTE workflows** - ADW system must be set up (`adws/` directory)
4. **Clean worktree** - No uncommitted changes before starting

### Installation

No installation required - the system is ready to use once the repository is set up:

```bash
# Verify setup
ls -la zte-hopper/
ls -la scripts/zte_hopper.sh
ls -la scripts/gi
```

## Usage

### Adding Issues to Queue

To queue an issue for processing, simply copy a markdown file into the `queue/` directory:

```bash
# Single issue
cp my-feature-request.md zte-hopper/queue/

# Multiple issues
cp issue-1.md issue-2.md issue-3.md zte-hopper/queue/

# Batch copy
cp restructure-issues/*.md zte-hopper/queue/
```

**Issue File Format:**

```markdown
# Issue Title Goes Here

This becomes the GitHub issue body.

## Requirements
- Feature requirement 1
- Feature requirement 2

## Details
Any markdown formatting works here.
```

**Requirements:**
- Files must be `.md` extension
- Must have a first-level heading (`# Title`) as the first heading in the file
- The heading text becomes the GitHub issue title
- Everything in the file becomes the issue body
- ZTE workflow trigger is automatically added

### Starting Processing

Start the hopper to process all queued issues:

```bash
./scripts/zte_hopper.sh --work
```

The hopper will:
- Process issues in FIFO order (by file creation time)
- Log all operations to `zte-hopper/logs/hopper-YYYYMMDD-HHMMSS.log`
- Continue processing until queue is empty or an issue fails
- Run unattended - you can close the terminal (use `nohup` for true background operation)

### Monitoring Progress

Check the current status:

```bash
./scripts/zte_hopper.sh --status
```

Example output:
```
ZTE Hopper Status
=================

Status: RUNNING (PID: 12345)

State: RUNNING
Current Issue: #52
Current File: feature-authentication.md
Time Elapsed: 245s

Queue: 3 files
Completed: 5 files
Failed: 0 files

Latest Log: zte-hopper/logs/hopper-20241110-143022.log
```

Watch the log file in real-time:

```bash
tail -f zte-hopper/logs/hopper-*.log
```

### Stopping Gracefully

To stop after the current issue completes:

```bash
./scripts/zte_hopper.sh --stop
```

This creates a stop signal that the hopper checks between issues and during polling.

### Emergency Stop

To kill the hopper immediately:

```bash
./scripts/zte_hopper.sh --kill
```

This sends a SIGTERM signal for graceful cleanup. If the process doesn't exit within 10 seconds, it sends SIGKILL.

## Validation and Sanity Checks

### Pre-flight Checks (Before Each Issue)

Before creating each GitHub issue, the hopper verifies:

- ✓ Git worktree is clean (no uncommitted changes)
- ✓ No unexpected untracked files
- ✓ Successfully pulled latest from `origin/main`

If pre-flight checks fail, the issue file is moved to `failed/` and processing stops.

### Post-completion Validation (After Each Issue)

After an issue closes, the hopper validates:

- ✓ Issue state is `CLOSED` on GitHub
- ✓ Issue contains "Zero Touch Execution Complete" or "Code has been shipped" marker
- ✓ All SDLC phases are mentioned in comments: `plan`, `build`, `test`, `review`, `document`, `ship`
- ✓ Git worktree is clean (excluding expected directories: `trees/`, `agents/`, `logs/`)

If validation fails, the issue file is moved to `failed/` and processing stops immediately.

## Processing Flow

For each issue in the queue:

```
1. Get oldest .md file from queue/ (FIFO)
2. Run pre-flight checks
3. Extract title from markdown (first # heading)
4. Create GitHub issue using ./scripts/gi
5. Wait for issue to close (poll every 30s, max 2 hours)
6. Run post-completion validation
7. If all checks pass:
   - Move file to completed/
   - Continue to next issue
8. If any check fails:
   - Move file to failed/ (with timestamp)
   - Log error details
   - STOP processing
   - Require manual intervention
```

## State Management

The hopper maintains state in `.hopper_state`:

```bash
STATE="RUNNING"           # IDLE|RUNNING|STOPPED|FAILED
ISSUE_NUMBER="52"         # Current GitHub issue number
ISSUE_FILE="feature.md"   # Current file being processed
TIMESTAMP="1699632145"    # Start time (Unix timestamp)
```

This state persists across restarts and enables monitoring.

## Error Handling

### Failed Issues

When an issue fails validation:
- File is moved to `failed/YYYYMMDD-HHMMSS-filename.md`
- Error details logged to log file
- Processing stops immediately
- State set to `FAILED`

To retry a failed issue:
1. Review the log file to understand the failure
2. Fix the issue (manual GitHub operations, git cleanup, etc.)
3. Move the file back to queue: `mv zte-hopper/failed/timestamp-file.md zte-hopper/queue/`
4. Restart hopper: `./scripts/zte_hopper.sh --work`

### Timeout

If an issue doesn't close within 2 hours:
- Issue is marked as failed
- File moved to `failed/` directory
- Processing stops

### Network Failures

GitHub API calls include basic retry logic. If `gh` commands fail:
- Error is logged
- Issue is marked as failed
- Processing stops

## Advanced Usage

### Background Execution

To run the hopper in the background (survives terminal close):

```bash
nohup ./scripts/zte_hopper.sh --work > /dev/null 2>&1 &
```

Monitor with:
```bash
./scripts/zte_hopper.sh --status
tail -f zte-hopper/logs/hopper-*.log
```

### FIFO Ordering

Issues are processed strictly FIFO by file creation time. To control order:

```bash
# Create files in specific order
touch zte-hopper/queue/01-first.md
sleep 1
touch zte-hopper/queue/02-second.md
sleep 1
touch zte-hopper/queue/03-third.md

# Or use timestamps in filenames (for reference only - creation time is what matters)
touch zte-hopper/queue/20241110-001-feature.md
touch zte-hopper/queue/20241110-002-bugfix.md
```

Verify order:
```bash
find zte-hopper/queue/ -type f -name "*.md" -printf '%T@ %p\n' | sort -n
```

### Processing Large Batches

For processing many issues (e.g., 20+ issues):

1. Prepare all issue markdown files
2. Copy all to queue in desired order
3. Start hopper: `./scripts/zte_hopper.sh --work`
4. Optional: Run in background with `nohup`
5. Monitor: `watch -n 30 './scripts/zte_hopper.sh --status'`
6. Check logs periodically for any issues

The hopper will process all issues sequentially, stopping only if one fails.

## Troubleshooting

### "Another hopper instance is already running"

**Cause:** A hopper process is already running, or a stale PID file exists.

**Solution:**
```bash
# Check if actually running
./scripts/zte_hopper.sh --status

# If stale, manually remove PID file
rm zte-hopper/.hopper.pid

# If running, kill it first
./scripts/zte_hopper.sh --kill
```

### "Git worktree is not clean"

**Cause:** Uncommitted changes in the repository.

**Solution:**
```bash
# Check what's uncommitted
git status

# Commit or stash changes
git add .
git commit -m "commit message"

# Or stash
git stash
```

### "Could not extract title from file"

**Cause:** Markdown file doesn't have a first-level heading (`# Title`).

**Solution:**
- Ensure your markdown file starts with `# Title` (or has it as the first heading)
- Check file encoding (must be UTF-8)
- Verify file isn't empty

### "Issue did not complete in time"

**Cause:** Issue took longer than 2-hour timeout.

**Solution:**
- Check issue on GitHub to see if it's still processing
- If issue completed after timeout, manually move file to completed:
  ```bash
  mv zte-hopper/failed/timestamp-file.md zte-hopper/completed/
  ```
- For very large features, consider splitting into smaller issues

### "Missing ZTE completion marker"

**Cause:** Issue closed but ZTE workflow didn't complete normally.

**Solution:**
- Check issue comments on GitHub
- Verify ZTE workflow actually ran (look for "adw_sdlc_zte_iso" in comments)
- Check if workflow failed mid-execution
- May need to manually close and complete the work

### "Failed validation" / "Missing SDLC phases"

**Cause:** Issue closed without completing all SDLC phases.

**Solution:**
- Review issue comments to see which phase failed
- Check ZTE workflow logs
- May indicate a bug in the ZTE workflow itself
- Manually complete missing phases if needed

## Logs and Debugging

### Log Files

Logs are stored in `zte-hopper/logs/hopper-YYYYMMDD-HHMMSS.log`

Log levels:
- `INFO` - Normal operations
- `WARN` - Warnings (non-fatal)
- `ERROR` - Errors (fatal, cause failures)
- `DEBUG` - Detailed debugging information

### Log Rotation

The hopper automatically keeps the last 10 log files and deletes older ones.

### Reading Logs

```bash
# View latest log
cat $(ls -t zte-hopper/logs/hopper-*.log | head -1)

# Follow live
tail -f zte-hopper/logs/hopper-*.log

# Search for errors
grep ERROR zte-hopper/logs/hopper-*.log

# See specific issue processing
grep "#52" zte-hopper/logs/hopper-*.log
```

## Best Practices

1. **Test First** - Process a single small test issue before queueing many
2. **Review Files** - Double-check markdown files have proper format before queueing
3. **Monitor Initially** - Watch the first few issues complete to ensure everything works
4. **Clean State** - Always start with a clean git worktree
5. **Batch Related Issues** - Queue related issues together for efficient processing
6. **Check Logs** - Review logs after batch completion to catch any warnings

## Limitations

- **Sequential Only** - Processes one issue at a time (no parallel processing)
- **No Prioritization** - Strict FIFO ordering (no priority queue)
- **2-Hour Timeout** - Issues taking longer will fail (cannot be configured)
- **No Resume** - If hopper is killed, must manually restart (doesn't auto-resume)
- **GitHub API Limits** - Heavy use may hit GitHub API rate limits (built-in 30s polling helps)

## Future Enhancements

Documented but not implemented:

- Real-time web visualization dashboard
- Live cost monitoring per issue
- Webhook integration (GitHub webhook triggers next issue)
- Parallel processing for independent issues
- Priority queue support
- Configurable timeout per issue
- Auto-resume after crash
- Email/Slack notifications
- Dry-run mode for testing

## Examples

### Example 1: Simple Feature Queue

```bash
# Create issue files
cat > zte-hopper/queue/add-logging.md << 'EOF'
# Add Structured Logging

Add structured JSON logging to the application.

## Requirements
- Use Winston or Bunyan
- Log to stdout
- Include request IDs
EOF

cat > zte-hopper/queue/add-metrics.md << 'EOF'
# Add Prometheus Metrics

Add Prometheus metrics endpoint.

## Requirements
- Expose /metrics endpoint
- Track request counts
- Track response times
EOF

# Process
./scripts/zte_hopper.sh --work
```

### Example 2: Large Restructure

```bash
# Copy all restructure issues at once
cp specs/restructure-phase-*.md zte-hopper/queue/

# Verify count
ls zte-hopper/queue/*.md | wc -l

# Start processing (run in background)
nohup ./scripts/zte_hopper.sh --work > /dev/null 2>&1 &

# Monitor progress
watch -n 30 './scripts/zte_hopper.sh --status'
```

### Example 3: Handling Failures

```bash
# Start processing
./scripts/zte_hopper.sh --work

# ... Issue #52 fails validation ...

# Check what failed
ls zte-hopper/failed/
cat zte-hopper/logs/hopper-*.log | grep ERROR

# Fix the issue manually on GitHub
gh issue view 52
gh issue close 52 --comment "Manually completed"

# Move to completed and continue
mv zte-hopper/failed/*-add-feature.md zte-hopper/completed/

# Restart hopper for remaining issues
./scripts/zte_hopper.sh --work
```

## Support

For issues or questions:

1. Check this README first
2. Review logs in `zte-hopper/logs/`
3. Check GitHub issues in the repository
4. Review ZTE workflow documentation in `adws/README.md`

## See Also

- [ADW System Documentation](../adws/README.md)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Zero Touch Execution Workflows](../adws/adw_sdlc_zte_iso.py)
