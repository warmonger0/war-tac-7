# Streamlined Restructure Issues

## File Size Comparison

### Original (Verbose)
- issue-10a: 7.9K ✅ (already running)
- issue-10b: 11K → **2.1K** (81% reduction)
- issue-10c: 13K → **1.9K** (85% reduction)
- issue-11a: 25K → **2.2K** (91% reduction)
- issue-11b: 9.4K → **1.6K** (83% reduction)
- issue-11c: 3.2K → **1.3K** (59% reduction)
- issue-12a: 2.9K → **1.4K** (52% reduction)
- issue-12b: 2.0K → **1.7K** (15% reduction)
- issue-12c: 3.2K → **1.8K** (44% reduction)

### Total Reduction
- **Original**: 78K total
- **Streamlined**: 15.9K total
- **Savings**: 80% reduction

## Model Assignments

| Issue | Model | Why |
|-------|-------|-----|
| 10a | Sonnet | Already running |
| 10b | Sonnet | Import updates need accuracy |
| 10c | **Haiku** | Simple file operations |
| 11a | **Haiku** | Create directories/READMEs |
| 11b | **Haiku** | Move files |
| 11c | **Haiku** | Move files |
| 12a | **Haiku** | Grep and fix |
| 12b | **Haiku** | Create scripts |
| 12c | **Haiku** | Documentation |

**Cost Savings**: ~70% by using Haiku for 7/9 issues

## Execution Commands

### Wave 1: App Structure

```bash
# Issue 10a - ALREADY RUNNING
# (using original verbose version)

# Issue 10b - Backend Reorganization (Sonnet)
./scripts/gi --title "Reorganize Backend Structure" --body-file issue-10b-reorganize-backend-v2.md

# Validate 10b
cd projects/tac-webbuilder
grep -r "from interfaces.web" app/ tests/ | wc -l  # = 0
./scripts/start_web.sh &
sleep 3 && curl http://localhost:8002/health
killall uvicorn

# Issue 10c - Integration (Haiku)
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Integration & Cleanup" --body-file issue-10c-integration-cleanup-v2.md

# Validate 10c
cd projects/tac-webbuilder
./scripts/start_full.sh &
sleep 10 && curl http://localhost:8002/health && curl -I http://localhost:5174
killall uvicorn node
uv run pytest tests/ -v
```

### Wave 2: Documentation

```bash
# Issue 11a - Doc Structure (Haiku)
./scripts/gi --title "Documentation Structure" --body-file issue-11a-documentation-structure-v2.md

# Validate 11a
cd projects/tac-webbuilder
ls -la app_docs/ specs/ issues/
test -f ARCHITECTURE.md && echo "✅"

# Issue 11b - Move Docs (Haiku)
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Move Docs & Specs" --body-file issue-11b-move-docs-specs-v2.md

# Validate 11b
cd projects/tac-webbuilder
find app_docs -name "feature-*.md" | wc -l  # = 3
find specs/patch -name "patch-*.md" | wc -l  # = 8

# Issue 11c - Move Issues (Haiku)
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Move Issue Files" --body-file issue-11c-move-issue-files-v2.md

# Validate 11c
cd projects/tac-webbuilder
find issues/completed -name "*.md" | wc -l  # = 11
find issues/active -name "*.md" | wc -l  # = 9
```

### Wave 3: Extraction

```bash
# Issue 12a - Audit (Haiku)
./scripts/gi --title "Dependency Audit" --body-file issue-12a-dependency-audit-v2.md

# Validate 12a
cd projects/tac-webbuilder
grep -r "from interfaces.web" . --include="*.py" | wc -l  # = 0
./scripts/validate_standalone.sh  # if created

# Issue 12b - Tooling (Haiku)
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Extraction Tooling" --body-file issue-12b-extraction-tooling-v2.md

# Validate 12b
cd projects/tac-webbuilder
./scripts/validate_standalone.sh
./scripts/extract_project.sh /tmp/test
cd /tmp/test && ./scripts/validate_standalone.sh

# Issue 12c - Final (Haiku)
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Final Validation" --body-file issue-12c-final-validation-v2.md

# Validate 12c
cd projects/tac-webbuilder
test -f EXTRACTION_GUIDE.md && echo "✅"
./scripts/validate_standalone.sh
./scripts/extract_project.sh /tmp/final-test
cd /tmp/final-test && ./scripts/validate_standalone.sh && ./scripts/start_full.sh &
```

## Key Changes

### Removed Verbose Content
- ❌ Long explanations of "why"
- ❌ Detailed examples in issue body
- ❌ Multiple validation approaches
- ❌ Extensive notes sections
- ❌ Redundant context

### Kept Essential Content
- ✅ Clear goal statement
- ✅ Concrete tasks with bash commands
- ✅ File/directory paths
- ✅ Validation commands
- ✅ Dependencies

### Philosophy
**"Show, don't tell"** - Give commands, not explanations. The ADW agent has the context.

## Benefits

1. **Faster ADW execution** - Less to read
2. **Lower token usage** - 80% reduction
3. **Lower cost** - Haiku for 7/9 issues
4. **Same quality** - All essential info preserved
5. **Easier to scan** - Human reviewers benefit too

## Migration Note

**Issue 10a is already running** with the original verbose version. Starting with 10b, use the streamlined `-v2` versions.
