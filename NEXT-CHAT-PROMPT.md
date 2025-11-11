# Next Chat Prompt

## Context Summary

I'm executing a 9-issue restructure of tac-webbuilder to make it self-contained and extraction-ready.

**Session Background:**
- Started with 3 monolithic issues (80-127K tokens each - would hit limits)
- Split into 9 sub-issues across 3 waves (25-55K each)
- Issue 10a is currently running
- Created streamlined v2 versions (80% size reduction: 78K → 16K)
- Optimized models: 10b uses Sonnet, 10c-12c use Haiku (70% cost savings)
- Verified Issue #9 (validation/optimization) doesn't conflict with plan

**What Was Restructured:**
- ~50 misplaced files identified
- Frontend wrong location: `/app/webbuilder/client/` → should be `projects/tac-webbuilder/app/client/`
- Backend wrong structure: `interfaces/web/` → should be `app/server/`
- Documentation scattered in parent tac-7 → should be in project

**Files Available:**

Streamlined v2 versions (UPDATED - user enhanced 11b and 12b):
- `issue-10b-reorganize-backend-v2.md` (2.1K, Sonnet)
- `issue-10c-integration-cleanup-v2.md` (1.9K, Haiku)
- `issue-11a-documentation-structure-v2.md` (2.2K, Haiku)
- `issue-11b-move-docs-specs-v2.md` (1.6K, Haiku) ✅ **UPDATED - now includes path reference updates**
- `issue-11c-move-issue-files-v2.md` (1.3K, Haiku)
- `issue-12a-dependency-audit-v2.md` (1.4K, Haiku)
- `issue-12b-extraction-tooling-v2.md` (1.7K, Haiku) ✅ **UPDATED - now has robust scripts with error handling**
- `issue-12c-final-validation-v2.md` (1.8K, Haiku)

Reference files:
- `RESTRUCTURE-STREAMLINED.md` - Complete execution guide with all commands
- `RESTRUCTURE-ANALYSIS.md` - Original analysis of misplaced files
- `RESTRUCTURE-BREAKDOWN-ANALYSIS.md` - Token optimization rationale
- `RESTRUCTURE-ISSUES-SUMMARY.md` - Complete overview

Original verbose versions (for reference):
- `issue-10b-reorganize-backend.md` (11K)
- `issue-10c-integration-cleanup.md` (13K)
- etc.

## Current Status

✅ **Issue 10a**: Running (using original verbose version)
✅ **Issues 10b-12c**: Streamlined v2 ready
✅ **11b-v2**: Path reference updates ADDED by user
✅ **12b-v2**: Robust extraction scripts ADDED by user

## What I Need

**Ready to execute** - All v2 files are finalized and enhanced. Just need confirmation to proceed.

## How to Run Issues

```bash
./scripts/gi --title "Issue Title" --body-file issue-XX-name-v2.md
```

## Execution Plan (After 10a Completes)

**Wave 1 (App Structure):**
```bash
# Issue 10b - Backend (Sonnet)
./scripts/gi --title "Reorganize Backend Structure" --body-file issue-10b-reorganize-backend-v2.md

# Issue 10c - Integration (Haiku)
./scripts/gi --title "Integration & Cleanup" --body-file issue-10c-integration-cleanup-v2.md
```

**Wave 2 (Documentation):**
```bash
# Issue 11a - Structure (Haiku)
./scripts/gi --title "Documentation Structure" --body-file issue-11a-documentation-structure-v2.md

# Issue 11b - Move Docs (Haiku)
./scripts/gi --title "Move Docs & Specs" --body-file issue-11b-move-docs-specs-v2.md

# Issue 11c - Move Issues (Haiku)
./scripts/gi --title "Move Issue Files" --body-file issue-11c-move-issue-files-v2.md
```

**Wave 3 (Extraction):**
```bash
# Issue 12a - Audit (Haiku)
./scripts/gi --title "Dependency Audit" --body-file issue-12a-dependency-audit-v2.md

# Issue 12b - Tooling (Haiku)
./scripts/gi --title "Extraction Tooling" --body-file issue-12b-extraction-tooling-v2.md

# Issue 12c - Final (Haiku)
./scripts/gi --title "Final Validation" --body-file issue-12c-final-validation-v2.md
```

## Questions for You

1. Should I proceed with all v2 files as-is?
2. Any issues need review before running?
3. Ready to start executing after 10a completes?

## Key Reference

See `RESTRUCTURE-STREAMLINED.md` for:
- Complete validation commands after each issue
- File size comparisons
- Model assignments and rationale
- Expected outputs
