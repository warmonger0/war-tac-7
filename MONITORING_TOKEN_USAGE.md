# Token Usage Monitoring Guide

## Overview

The `monitor_adw_tokens.py` script monitors token usage for ADW workflows **without adding to context overhead**. It runs outside of Claude Code and reads the `raw_output.jsonl` files that agents create.

## Why This Doesn't Add Context Overhead

- ✅ Runs as a **separate Python process** (not inside Claude Code)
- ✅ Only **reads** existing files (doesn't modify them)
- ✅ Not loaded into Claude's context
- ✅ Zero impact on workflow execution

## Usage

### Monitor Specific Workflow

```bash
uv run adws/monitor_adw_tokens.py <adw_id>

# Example:
uv run adws/monitor_adw_tokens.py 5afcc315
```

### Monitor Latest Workflow

```bash
uv run adws/monitor_adw_tokens.py --latest
```

### Continuous Monitoring (Watch Mode)

Updates every 10 seconds until you press Ctrl+C:

```bash
uv run adws/monitor_adw_tokens.py <adw_id> --watch

# Example:
uv run adws/monitor_adw_tokens.py 5afcc315 --watch
```

### Detailed View

Shows individual token breakdowns per phase:

```bash
uv run adws/monitor_adw_tokens.py <adw_id> --detail
```

## Finding the ADW ID

The ADW ID is posted in the first GitHub issue comment when a workflow starts:

```bash
# View issue comments
gh issue view <issue_number> --json comments --jq '.comments[0].body'

# Look for: "Starting workflow with ID: `5afcc315`"
```

Or use `--latest` to automatically monitor the most recent workflow.

## Example Workflow

```bash
# 1. Create issue with ZTE workflow
gh issue create --title "template docs" --body-file issue-6-templates-docs.md

# 2. Get ADW ID from issue
ADW_ID=$(gh issue view 26 --json comments --jq '.comments[0].body' | grep -o 'ID: `[^`]*`' | cut -d'`' -f2)

# 3. Monitor in watch mode
uv run adws/monitor_adw_tokens.py $ADW_ID --watch
```

## Output Explanation

### Summary View (Default)

```
📦 sdlc_planner
  Messages: 27
  Total In: 1,187,212 | Out: 36,094
```

- **Messages**: Number of API calls in this phase
- **Total In**: Sum of input + cache_create + cache_read tokens
- **Out**: Output tokens generated

### Detailed View (--detail)

```
📦 sdlc_planner
  Messages: 27
  Input: 10,740
  Cache Create: 283,059
  Cache Read: 893,413
  Output: 36,094
  Cache Efficiency: 76.3%
```

- **Input**: Fresh input tokens sent
- **Cache Create**: New tokens added to cache
- **Cache Read**: Tokens read from cache (cheaper)
- **Cache Efficiency**: Percentage of cache hits

### Cost Estimate

Based on Claude Sonnet 4.5 pricing:
- Input tokens: $3 per million
- Cache writes: $3.75 per million
- Cache reads: $0.30 per million (90% cheaper!)
- Output: $15 per million

## Token Optimization Results

From Issue #24 (Web Frontend):
- **Total Messages**: 295
- **Cache Efficiency**: 94.0%
- **Total Cost**: ~$8.40
- **Without Cache**: Would have been ~$40-50
- **Savings**: ~85%

The 70% reduction in repository context (from ~100K to ~30K tokens) enabled:
- Lower cache creation costs
- Faster workflow execution
- More efficient cache reuse

## Integration with ZTE Workflows

When using `adw_sdlc_zte_iso` workflows:

1. **Start monitoring before creating issue:**
   ```bash
   # Terminal 1: Create issue
   gh issue create --title "feature" --body-file issue.md

   # Terminal 2: Start monitoring
   uv run adws/monitor_adw_tokens.py --latest --watch
   ```

2. **Monitor runs independently** - doesn't interfere with workflow
3. **Real-time updates** show progress through phases
4. **Final report** shows complete token usage after workflow finishes

## Tips

- Use `--watch` mode for long-running workflows (build, review phases)
- Use `--detail` for final reports and cost analysis
- Keep monitoring terminal open to track progress
- Compare token usage across workflows to identify optimization opportunities
