# tac-webbuilder Restructure Analysis

## Context

The original intent was to use tac-7's ADW workflow to build an analogous system in a project that could be extracted as its own standalone repository. Due to context issues when building in a sibling directory, it was built as a subproject at `/projects/tac-webbuilder/`.

**Goal**: Make `projects/tac-webbuilder/` completely self-contained, mirroring tac-7's structure, so it can be extracted as an independent project.

## Structure Comparison

### tac-7 Structure (Parent)
```
/Users/Warmonger0/tac/tac-7/
├── README.md                    # Main documentation
├── .gitignore                   # Git ignore patterns
├── app/                         # Application code
│   ├── client/                  # Frontend (React/Vite)
│   └── server/                  # Backend (FastAPI)
├── adws/                        # ADW workflow system
│   ├── adw_modules/
│   ├── adw_tests/
│   └── adw_triggers/
├── scripts/                     # Utility scripts
├── specs/                       # Feature specifications
│   └── patch/                   # Patch specifications
├── app_docs/                    # Feature documentation
└── projects/                    # Sub-projects
    └── tac-webbuilder/
```

### tac-webbuilder Structure (Current)
```
/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/
├── README.md                    # ✅ Present
├── .gitignore                   # ✅ Present
├── pyproject.toml              # ✅ Present
├── config.yaml.sample          # ✅ Present
├── .env.sample                 # ✅ Present
├── core/                       # ✅ Core modules
├── interfaces/                 # ✅ Interfaces
│   ├── cli/                    # ✅ CLI interface
│   └── web/                    # ⚠️  Backend only - MISSING client/
├── adws/                       # ✅ ADW workflow system
│   ├── adw_modules/
│   ├── adw_tests/
│   └── adw_triggers/
├── scripts/                    # ✅ Utility scripts
├── templates/                  # ✅ Templates
├── tests/                      # ✅ Tests
├── docs/                       # ✅ Some docs
├── logs/                       # ✅ (gitignored)
├── trees/                      # ✅ (gitignored)
└── agents/                     # ✅ (gitignored)
```

### What Should Be Present (Target Structure)
```
/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/
├── README.md
├── .gitignore
├── pyproject.toml
├── config.yaml.sample
├── .env.sample
├── app/                        # ❌ MISSING - Should mirror tac-7
│   ├── client/                 # ❌ Currently at /app/webbuilder/client/
│   └── server/                 # ❌ Currently scattered in interfaces/web/
├── adws/                       # ✅ Present
├── scripts/                    # ✅ Present
├── specs/                      # ❌ MISSING - specs are in parent /specs/
│   └── patch/                  # ❌ Patches are in parent /specs/patch/
├── app_docs/                   # ❌ MISSING - docs are in parent /app_docs/
└── tests/                      # ✅ Present
```

## Misplaced Files Inventory

### Category 1: Frontend Application (HIGH PRIORITY)
**Current Location**: `/Users/Warmonger0/tac/tac-7/app/webbuilder/client/`
**Target Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/app/client/`
**Files**: 18+ files (React/TypeScript/Vite application)
- `index.html`
- `package.json`
- `package-lock.json`
- `tsconfig.json`
- `vite.config.ts`
- `tailwind.config.js`
- `postcss.config.js`
- `src/` directory (all components, hooks, types)

**Impact**: CRITICAL - Frontend is completely outside the project structure

### Category 2: Backend Server (HIGH PRIORITY)
**Current Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/interfaces/web/`
**Target Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/app/server/`
**Files**:
- `server.py` → `app/server/server.py`
- `models.py` → `app/server/core/models.py`
- `state.py` → `app/server/core/state.py`
- `websocket.py` → `app/server/core/websocket.py`
- `workflow_monitor.py` → `app/server/core/workflow_monitor.py`
- `routes/` → `app/server/routes/`

**Impact**: HIGH - Inconsistent with tac-7 pattern

### Category 3: Feature Documentation (MEDIUM PRIORITY)
**Current Location**: `/Users/Warmonger0/tac/tac-7/app_docs/`
**Target Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/app_docs/`
**Files**:
- `feature-fd9119bc-cli-interface.md`
- `feature-e7613043-playwright-mcp-readme.md`
- `feature-1afd9aba-project-structure-adw-integration.md`

**Impact**: MEDIUM - Documentation should live with the project

### Category 4: Specifications (MEDIUM PRIORITY)
**Current Location**: `/Users/Warmonger0/tac/tac-7/specs/patch/`
**Target Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/specs/patch/`
**Files**: 8 patch specification files
- `patch-adw-e7613043-add-playwright-mcp-readme.md`
- `patch-adw-e7613043-create-mcp-config-files.md`
- `patch-adw-e7613043-create-missing-mcp-tests.md`
- `patch-adw-e7613043-create-playwright-mcp-docs.md`
- `patch-adw-e7613043-execute-template-cleanup.md`
- `patch-adw-e7613043-implement-missing-mcp-config.md`
- `patch-adw-e7613043-remove-template-references.md`
- `patch-adw-1afd9aba-verify-git-commit-status.md`

**Impact**: MEDIUM - Specs should live with the project

### Category 5: Issue Markdown Files (LOW PRIORITY)
**Current Location**: `/Users/Warmonger0/tac/tac-7/` (root)
**Target Location**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/issues/`
**Files**: 10+ issue files
- `issue-1-foundation.md`
- `issue-2-nl-processing.md`
- `issue-3-cli-interface.md`
- `issue-4-web-backend.md`
- `issue-5-web-frontend.md`
- `issue-6-templates-docs.md`
- `issue-7-playwright-mcp.md`
- `issue-8-env-setup-guide.md`
- `issue-8a-env-setup-scripts.md`
- `issue-8b-config-documentation.md`
- `issue-9-validation-optimization.md`
- `Create-tac-webbuilder.md`

**Impact**: LOW - These are temporary work files (already in .gitignore)

### Category 6: Codebase Indexing Tool (EVALUATION NEEDED)
**Current Location**: `/Users/Warmonger0/tac/tac-7/adws/`
**Potential Targets**:
- Option A: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder/scripts/` (if tac-webbuilder specific)
- Option B: Keep in parent `/adws/` (if generic/reusable)
**Files**:
- `index_codebase.py`
- `adw_modules/codebase_expert_concept.md`

**Impact**: LOW - Needs evaluation of whether it's project-specific or generic

## ADW Issue Strategy

Given the complexity and interdependencies, I recommend **3 sequential issues**:

### Issue #10: Mirror app/ Structure - Frontend & Backend Consolidation
**Priority**: CRITICAL
**Estimated Effort**: Large
**Focus**: Create `app/` directory structure matching tac-7

**Tasks**:
1. Create `app/client/` and `app/server/` directory structure
2. Move frontend from `/app/webbuilder/client/` → `/projects/tac-webbuilder/app/client/`
3. Move backend from `/interfaces/web/` → `/projects/tac-webbuilder/app/server/`
4. Update all import paths in Python files
5. Update all API endpoint URLs in frontend
6. Update npm scripts and build configs
7. Update startup scripts (`scripts/start_web.sh`, etc.)
8. Create new unified startup script
9. Update documentation references
10. Validate both frontend and backend work after move
11. Run all existing tests to ensure no regressions

**Success Criteria**:
- `app/client/` contains full frontend application
- `app/server/` contains full backend application
- Both can start and communicate correctly
- All tests pass
- Documentation updated

### Issue #11: Documentation & Specifications Consolidation
**Priority**: HIGH
**Estimated Effort**: Medium
**Focus**: Move all tac-webbuilder documentation into the project

**Tasks**:
1. Create `app_docs/` directory in tac-webbuilder
2. Move feature docs from `/app_docs/` → `/projects/tac-webbuilder/app_docs/`
3. Create `specs/` and `specs/patch/` directories
4. Move patch specs from `/specs/patch/` → `/projects/tac-webbuilder/specs/patch/`
5. Move issue markdown files from root to `/projects/tac-webbuilder/issues/`
6. Update any cross-references in documentation
7. Update README to reflect new documentation structure
8. Create index/catalog of all documentation

**Success Criteria**:
- All tac-webbuilder documentation is self-contained
- Documentation is organized and discoverable
- README points to correct doc locations
- No broken documentation links

### Issue #12: Extraction Readiness - Final Cleanup & Validation
**Priority**: MEDIUM
**Estimated Effort**: Small
**Focus**: Ensure complete self-containment and extraction readiness

**Tasks**:
1. Audit all imports for parent directory references
2. Audit all file paths for parent directory references
3. Create comprehensive extraction guide/script
4. Evaluate codebase indexing tool placement
5. Update .gitignore to be self-contained
6. Update README with extraction instructions
7. Create validation script to check for external dependencies
8. Document any remaining parent project dependencies (if unavoidable)
9. Create ARCHITECTURE.md documenting the structure
10. Test extraction in a temporary location

**Success Criteria**:
- No code references parent tac-7 structure
- All file paths are relative to project root
- Extraction guide is complete and tested
- Project can run independently when extracted
- All documentation is accurate

## Recommended Approach

### Phase 1: Plan & Prepare
1. Review this analysis
2. Confirm the strategy
3. Ensure git branch is clean
4. Create feature branch for restructure

### Phase 2: Execute Issues Sequentially
1. **Issue #10** (app/ structure) - Most critical, highest risk
   - Run full test suite before and after
   - Validate frontend and backend individually
   - Validate full integration

2. **Issue #11** (documentation) - Lower risk, high value
   - Verify all docs moved
   - Check no broken links

3. **Issue #12** (extraction readiness) - Final polish
   - Comprehensive validation
   - Extraction dry-run

### Phase 3: Validate & Document
1. Run all tests
2. Start both frontend and backend
3. Test full user workflow
4. Update main tac-7 README to document the subproject
5. Consider creating extraction script for future use

## Risk Assessment

### High Risk Items
1. **Frontend import path updates** - Many files import from `src/`
2. **Backend API path updates** - Frontend calls backend APIs
3. **Startup script coordination** - Multiple scripts reference paths
4. **Test file paths** - Tests reference modules by path

### Mitigation Strategies
1. Use search/replace for systematic path updates
2. Create comprehensive test plan before changes
3. Test incrementally after each major move
4. Keep backup of working state
5. Use git branches for safe experimentation

## Questions to Resolve

1. **CLI Interface**: Should `interfaces/cli/` also move to `app/cli/` for consistency?
   - Currently tac-7 doesn't have a CLI, so no precedent
   - Could argue for `app/cli/` to mirror `app/client/` and `app/server/`
   - Or keep as `interfaces/cli/` since it's different from web app

2. **Codebase Indexing**: Is `index_codebase.py` generic or tac-webbuilder specific?
   - Usage example specifically mentions tac-webbuilder
   - Could be useful for other projects
   - Recommend: Keep in parent `/adws/` as a generic tool

3. **Tests Structure**: Should tests mirror `app/` structure?
   - Currently: `tests/interfaces/web/`
   - After move: Keep as is, or reorganize to `tests/app/server/`?
   - Recommend: Reorganize to match new structure

4. **Backward Compatibility**: Do we need to maintain any parent references?
   - For ADW execution context?
   - For shared utilities?
   - Recommend: Document but minimize

## Summary

**Total Files to Move**: ~40-50 files
**New Directories to Create**: 6-8 directories
**Import Statements to Update**: ~30-50 files
**Documentation Updates**: ~15 files
**Estimated Total Effort**: 2-3 ADW workflow executions

**Primary Benefits**:
1. Complete self-containment
2. Easy extraction as standalone project
3. Consistent with tac-7 structure pattern
4. Better organization and maintainability
5. Clear separation of concerns

**Primary Risks**:
1. Breaking existing functionality during moves
2. Missing import path updates
3. Test failures from path changes
4. Startup script coordination issues

**Recommendation**: Execute the 3-issue sequential plan with careful validation at each step.
