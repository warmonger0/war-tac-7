# tac-webbuilder Restructure - Issue Summary

## Overview

Complete breakdown of the tac-webbuilder restructure into 9 token-optimized sub-issues across 3 waves.

## Created Issues

### Analysis & Planning Documents
1. **RESTRUCTURE-ANALYSIS.md** - Complete restructure analysis
2. **RESTRUCTURE-BREAKDOWN-ANALYSIS.md** - Token optimization analysis
3. **RESTRUCTURE-ISSUES-SUMMARY.md** - This file

### Wave 1: App Structure Consolidation (Issues 10a-10c)

#### Issue 10a: Move Frontend Application
- **File**: `issue-10a-move-frontend.md`
- **Scope**: Move frontend from `/app/webbuilder/client/` to `/projects/tac-webbuilder/app/client/`
- **Tasks**: Create structure, move files, update config, create startup script
- **Estimated**: 35-45K tokens ✅
- **Risk**: Low
- **Dependencies**: None

#### Issue 10b: Reorganize Backend Structure
- **File**: `issue-10b-reorganize-backend.md`
- **Scope**: Reorganize backend from `/interfaces/web/` to `/app/server/`
- **Tasks**: Create structure, move files, update imports, update tests
- **Estimated**: 40-50K tokens ✅
- **Risk**: Medium (import path updates)
- **Dependencies**: Issue 10a

#### Issue 10c: Integration & Cleanup
- **File**: `issue-10c-integration-cleanup.md`
- **Scope**: Test integration, update docs, clean up old directories
- **Tasks**: Full stack startup, integration testing, README updates, cleanup
- **Estimated**: 25-35K tokens ✅
- **Risk**: Low
- **Dependencies**: Issues 10a, 10b

**Wave 1 Total**: 100-130K tokens across 3 issues (vs 80-105K in monolithic)

### Wave 2: Documentation Consolidation (Issues 11a-11c)

#### Issue 11a: Documentation Structure & Indexes
- **File**: `issue-11a-documentation-structure.md`
- **Scope**: Create doc structure, indexes, and ARCHITECTURE.md
- **Tasks**: Create directories, write READMEs, create ARCHITECTURE.md
- **Estimated**: 30-40K tokens ✅
- **Risk**: Very Low
- **Dependencies**: Wave 1 complete

#### Issue 11b: Move Feature Docs & Specs
- **File**: `issue-11b-move-docs-specs.md`
- **Scope**: Move feature docs (3) and patch specs (8) into project
- **Tasks**: Move files, update indexes, update cross-references
- **Estimated**: 35-45K tokens ✅
- **Risk**: Low
- **Dependencies**: Issue 11a

#### Issue 11c: Move Issue Tracking Files
- **File**: `issue-11c-move-issue-files.md`
- **Scope**: Move issue markdown files (24) and planning docs (3)
- **Tasks**: Move completed/active issues, move planning docs, update index
- **Estimated**: 30-40K tokens ✅
- **Risk**: Low
- **Dependencies**: Issues 11a, 11b

**Wave 2 Total**: 95-125K tokens across 3 issues (vs 82-108K in monolithic)

### Wave 3: Extraction Readiness (Issues 12a-12c)

#### Issue 12a: Dependency Audit & Resolution
- **File**: `issue-12a-dependency-audit.md`
- **Scope**: Audit and resolve all parent dependencies
- **Tasks**: Audit imports, paths, configs, scripts; resolve findings
- **Estimated**: 45-55K tokens ✅
- **Risk**: Medium
- **Dependencies**: Waves 1-2 complete

#### Issue 12b: Extraction Tooling
- **File**: `issue-12b-extraction-tooling.md`
- **Scope**: Create extraction and validation scripts
- **Tasks**: Create extract_project.sh, validate_standalone.sh, update configs
- **Estimated**: 35-45K tokens ✅
- **Risk**: Low
- **Dependencies**: Issue 12a

#### Issue 12c: Documentation & Final Validation
- **File**: `issue-12c-final-validation.md`
- **Scope**: Final docs, comprehensive validation, extraction test
- **Tasks**: Create EXTRACTION_GUIDE.md, update docs, full validation
- **Estimated**: 40-50K tokens ✅
- **Risk**: Low
- **Dependencies**: Issues 12a, 12b

**Wave 3 Total**: 120-150K tokens across 3 issues (vs 88-127K in monolithic)

## Execution Sequence

Execute in this order:

```
Wave 1: App Structure
├── Issue 10a: Move Frontend ────────┐
├── Issue 10b: Reorganize Backend ───┤ (depends on 10a)
└── Issue 10c: Integration & Cleanup ┘ (depends on 10a, 10b)
    │
    └─► Validate: Full stack works
        │
        │
Wave 2: Documentation
├── Issue 11a: Documentation Structure ─────┐
├── Issue 11b: Move Docs & Specs ───────────┤ (depends on 11a)
└── Issue 11c: Move Issue Files ────────────┘ (depends on 11a)
    │
    └─► Validate: All docs self-contained
        │
        │
Wave 3: Extraction
├── Issue 12a: Dependency Audit ────────────┐
├── Issue 12b: Extraction Tooling ──────────┤ (depends on 12a)
└── Issue 12c: Final Validation ────────────┘ (depends on 12a, 12b)
    │
    └─► Validate: Extraction works, project standalone
```

## Token Comparison

### Monolithic Approach (3 issues)
- Issue 10: 80-105K tokens ⚠️
- Issue 11: 82-108K tokens ⚠️
- Issue 12: 88-127K tokens ⚠️
- **Total**: 250-340K tokens across 3 workflows

### Breakdown Approach (9 sub-issues)
- Issues 10a-10c: 100-130K tokens ✅
- Issues 11a-11c: 95-125K tokens ✅
- Issues 12a-12c: 120-150K tokens ✅
- **Total**: 315-405K tokens across 9 workflows

### Why More Tokens But Better?
- **Better Distribution**: 25-55K per workflow vs 80-127K
- **Better Caching**: Smaller contexts = better prompt cache hits
- **Lower Risk**: Smaller scopes = fewer failures
- **Faster Iterations**: Each workflow completes faster
- **Incremental Validation**: Test after each step
- **Clearer Progress**: 9 smaller wins vs 3 large efforts

**Expected Savings**: 20-30% from improved caching and fewer retries

## Creating GitHub Issues

Use these commands to create GitHub issues:

```bash
cd /Users/Warmonger0/tac/tac-7

# Wave 1
gh issue create --title "🎯 Issue 10a: Move Frontend Application" \
  --body-file issue-10a-move-frontend.md \
  --label enhancement,restructure,wave-1

gh issue create --title "🎯 Issue 10b: Reorganize Backend Structure" \
  --body-file issue-10b-reorganize-backend.md \
  --label enhancement,restructure,wave-1

gh issue create --title "🎯 Issue 10c: Integration & Cleanup" \
  --body-file issue-10c-integration-cleanup.md \
  --label enhancement,restructure,wave-1

# Wave 2
gh issue create --title "🎯 Issue 11a: Documentation Structure & Indexes" \
  --body-file issue-11a-documentation-structure.md \
  --label documentation,restructure,wave-2

gh issue create --title "🎯 Issue 11b: Move Feature Docs & Specs" \
  --body-file issue-11b-move-docs-specs.md \
  --label documentation,restructure,wave-2

gh issue create --title "🎯 Issue 11c: Move Issue Tracking Files" \
  --body-file issue-11c-move-issue-files.md \
  --label documentation,restructure,wave-2

# Wave 3
gh issue create --title "🎯 Issue 12a: Dependency Audit & Resolution" \
  --body-file issue-12a-dependency-audit.md \
  --label enhancement,restructure,wave-3

gh issue create --title "🎯 Issue 12b: Extraction Tooling" \
  --body-file issue-12b-extraction-tooling.md \
  --label enhancement,restructure,wave-3

gh issue create --title "🎯 Issue 12c: Documentation & Final Validation" \
  --body-file issue-12c-final-validation.md \
  --label enhancement,restructure,wave-3
```

## Validation Checkpoints

After each wave:

**After Wave 1**:
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_full.sh
# Verify both frontend and backend work
uv run pytest tests/ -v
```

**After Wave 2**:
```bash
# Verify all docs are self-contained
ls app_docs/ specs/ issues/
# Check no docs remain in parent
ls /Users/Warmonger0/tac/tac-7/app_docs/
ls /Users/Warmonger0/tac/tac-7/specs/patch/
```

**After Wave 3**:
```bash
./scripts/validate_standalone.sh
./scripts/extract_project.sh /tmp/final-test
cd /tmp/final-test
./scripts/validate_standalone.sh
./scripts/start_full.sh
```

## Files Created

### Issue Markdown Files (9)
- `issue-10a-move-frontend.md`
- `issue-10b-reorganize-backend.md`
- `issue-10c-integration-cleanup.md`
- `issue-11a-documentation-structure.md`
- `issue-11b-move-docs-specs.md`
- `issue-11c-move-issue-files.md`
- `issue-12a-dependency-audit.md`
- `issue-12b-extraction-tooling.md`
- `issue-12c-final-validation.md`

### Analysis Documents (3)
- `RESTRUCTURE-ANALYSIS.md`
- `RESTRUCTURE-BREAKDOWN-ANALYSIS.md`
- `RESTRUCTURE-ISSUES-SUMMARY.md`

### Original Monolithic Issues (3) - Reference Only
- `issue-10-restructure-app-directory.md`
- `issue-11-consolidate-documentation.md`
- `issue-12-extraction-readiness.md`

## Success Metrics

Upon completion of all 9 issues:

### Structure
- ✅ Frontend at `app/client/`
- ✅ Backend at `app/server/`
- ✅ All docs in `app_docs/`, `specs/`, `issues/`, `docs/`
- ✅ No files in parent tac-7 structure

### Functionality
- ✅ Full stack starts successfully
- ✅ All tests pass
- ✅ All features work
- ✅ No regressions

### Documentation
- ✅ README comprehensive
- ✅ ARCHITECTURE complete
- ✅ EXTRACTION_GUIDE detailed
- ✅ All docs indexed
- ✅ No broken links

### Extraction
- ✅ `validate_standalone.sh` passes
- ✅ `extract_project.sh` works
- ✅ Extracted project runs
- ✅ No parent dependencies

## Timeline Estimate

Based on token estimates and typical ADW execution:

- **Wave 1**: 3-4 hours (3 issues)
- **Wave 2**: 2-3 hours (3 issues)
- **Wave 3**: 3-4 hours (3 issues)
- **Total**: 8-11 hours across 9 workflows

Compared to monolithic approach:
- **Monolithic**: 6-9 hours (but higher failure risk)
- **Breakdown**: 8-11 hours (but much higher success rate)

**Trade-off**: Slightly more time, but significantly higher quality and success probability.

## Next Steps

1. **Review** all 9 issue files
2. **Confirm** the breakdown strategy
3. **Create** GitHub issues using commands above
4. **Execute** Wave 1 (Issues 10a-10c)
5. **Validate** after Wave 1
6. **Execute** Wave 2 (Issues 11a-11c)
7. **Validate** after Wave 2
8. **Execute** Wave 3 (Issues 12a-12c)
9. **Final Validation** and celebration! 🎉

## Benefits Summary

✅ **Token Optimized**: Each workflow 25-55K tokens (optimal range)
✅ **Lower Risk**: Smaller scopes = fewer failure points
✅ **Better Caching**: Improved prompt cache efficiency
✅ **Incremental Validation**: Test after each step
✅ **Clear Progress**: Track 9 milestones vs 3
✅ **Easy Debugging**: Isolate issues to specific workflows
✅ **Better Git History**: Smaller, focused commits
✅ **Flexible Execution**: Can pause/resume between waves

## Conclusion

The 9-issue breakdown approach provides optimal token usage, lower risk, and higher success probability compared to the 3-issue monolithic approach. All issues are ADW-ready and can be executed sequentially with validation checkpoints between waves.

**Status**: ✅ All 9 sub-issues created and ready for execution
**Recommendation**: Execute in sequence, validate after each wave
**Expected Outcome**: Fully self-contained, extraction-ready tac-webbuilder project
