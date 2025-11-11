# tac-webbuilder Restructure - Execution Commands

## Overview
Commands to create and validate each of the 9 restructure issues using the `./scripts/gi` script and ADW workflow.

## Wave 1: App Structure Consolidation

### Issue 10a: Move Frontend Application

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Move Frontend Application" --body-file issue-10a-move-frontend.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify directory structure
ls -la app/client/
find app/client -type f | wc -l
# Should show 18+ files

# 2. Verify old directory empty
ls /Users/Warmonger0/tac/tac-7/app/webbuilder/client/ 2>/dev/null || echo "✅ Old directory removed"

# 3. Test frontend startup
./scripts/start_client.sh &
sleep 5
curl -I http://localhost:5174
# Should return 200 OK
killall node

# 4. Check browser (manual)
# Open http://localhost:5174 in browser - UI should load
```

---

### Issue 10b: Reorganize Backend Structure

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Reorganize Backend Structure" --body-file issue-10b-reorganize-backend.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify directory structure
ls -la app/server/
ls -la app/server/core/
ls -la app/server/routes/
find app/server -type f -name "*.py" | wc -l
# Should show 12+ files

# 2. Verify no old imports
grep -r "from interfaces.web" app/ core/ tests/ | wc -l
# Should be 0

# 3. Verify old directory empty
ls interfaces/web/ 2>/dev/null || echo "✅ Old directory removed"

# 4. Test Python imports
source .venv/bin/activate
python3 -c "from app.server.main import app; print('✅ Imports work')"

# 5. Test backend startup
./scripts/start_web.sh &
sleep 5
curl http://localhost:8002/health
# Should return: {"status":"healthy"}
killall uvicorn

# 6. Run backend tests
uv run pytest tests/interfaces/web/ -v || uv run pytest tests/app/server/ -v
```

---

### Issue 10c: Integration & Cleanup

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Integration & Cleanup" --body-file issue-10c-integration-cleanup.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify start_full.sh exists and is executable
test -x scripts/start_full.sh && echo "✅ start_full.sh executable"

# 2. Test full stack startup
./scripts/start_full.sh &
sleep 10

# 3. Test backend
curl http://localhost:8002/health
# Should return: {"status":"healthy"}

# 4. Test frontend
curl -I http://localhost:5174
# Should return 200 OK

# 5. Test frontend-backend integration (manual)
# Open http://localhost:5174 in browser
# Submit a test request
# Verify API calls work in Network tab

# 6. Stop services
killall uvicorn node

# 7. Run all tests
uv run pytest tests/ -v

# 8. Verify old directories cleaned up
ls /Users/Warmonger0/tac/tac-7/app/webbuilder/ 2>/dev/null || echo "✅ Old frontend dir removed"
ls interfaces/web/ 2>/dev/null || echo "✅ Old backend dir removed"

# 9. Verify README updated
grep -A 5 "app/client" README.md
grep -A 5 "app/server" README.md
```

**🎉 Wave 1 Complete - Full Stack Validated**

---

## Wave 2: Documentation Consolidation

### Issue 11a: Documentation Structure & Indexes

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Documentation Structure & Indexes" --body-file issue-11a-documentation-structure.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify directories created
ls -la | grep -E "app_docs|specs|issues"
ls -la issues/ | grep -E "completed|active|planning"
ls -la specs/ | grep "patch"

# 2. Verify all README files exist
test -f app_docs/README.md && echo "✅ app_docs/README.md"
test -f specs/README.md && echo "✅ specs/README.md"
test -f specs/patch/README.md && echo "✅ specs/patch/README.md"
test -f issues/README.md && echo "✅ issues/README.md"
test -f docs/README.md && echo "✅ docs/README.md"

# 3. Verify ARCHITECTURE.md created
test -f ARCHITECTURE.md && wc -l ARCHITECTURE.md
# Should show ~400+ lines

# 4. Verify main README updated
grep "## Documentation" README.md
grep "ARCHITECTURE.md" README.md

# 5. Count README files
find . -name "README.md" -not -path "./node_modules/*" -not -path "./.venv/*" | wc -l
# Should be 7+
```

---

### Issue 11b: Move Feature Docs & Specs

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Move Feature Docs & Specs" --body-file issue-11b-move-docs-specs.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify feature docs moved
ls -la app_docs/
find app_docs -name "feature-*.md" | wc -l
# Should be 3

# 2. Verify patch specs moved
ls -la specs/patch/
find specs/patch -name "patch-*.md" | wc -l
# Should be 8

# 3. Verify parent directories cleaned
ls /Users/Warmonger0/tac/tac-7/app_docs/ | grep feature || echo "✅ No features in parent"
ls /Users/Warmonger0/tac/tac-7/specs/patch/ | grep patch-adw || echo "✅ No patches in parent"

# 4. Verify indexes updated
cat app_docs/README.md | grep "CLI Interface"
cat specs/patch/README.md | grep "e7613043"

# 5. Verify README links to features
cat README.md | grep "feature-fd9119bc-cli-interface.md"
```

---

### Issue 11c: Move Issue Tracking Files

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Move Issue Tracking Files" --body-file issue-11c-move-issue-files.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify completed issues moved
ls -la issues/completed/
find issues/completed -name "issue-*.md" | wc -l
# Should be 11 (issues 1-9, plus 8a, 8b)

# 2. Verify active issues moved
ls -la issues/active/
find issues/active -name "issue-*.md" | wc -l
# Should be 9 (issues 10a-10c, 11a-11c, 12a-12c)

# 3. Verify planning docs moved
ls -la issues/planning/
ls issues/planning/ | grep -E "Create-tac-webbuilder|RESTRUCTURE"
# Should show 3 files

# 4. Verify parent cleaned
ls /Users/Warmonger0/tac/tac-7/issue-*.md 2>/dev/null | wc -l || echo "✅ No issues in parent"

# 5. Verify issues/README.md updated
cat issues/README.md | grep "Completed Issues"
cat issues/README.md | grep "Active Issues"
```

**🎉 Wave 2 Complete - Documentation Self-Contained**

---

## Wave 3: Extraction Readiness

### Issue 12a: Dependency Audit & Resolution

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Dependency Audit & Resolution" --body-file issue-12a-dependency-audit.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify no parent imports
grep -r "from /Users/Warmonger0/tac/tac-7[^/]" . \
  --include="*.py" \
  --exclude-dir=node_modules \
  --exclude-dir=.venv | wc -l
# Should be 0

# 2. Verify no parent paths
grep -r "/Users/Warmonger0/tac/tac-7[^/]" . \
  --include="*.py" \
  --include="*.sh" \
  --include="*.yaml" \
  --exclude-dir=node_modules \
  --exclude-dir=.venv | wc -l
# Should be 0

# 3. Verify no old imports
grep -r "from interfaces.web" . --include="*.py" | wc -l
# Should be 0

# 4. Test Python imports
source .venv/bin/activate
python3 -c "from app.server.main import app; print('✅ Imports work')"

# 5. Run all tests
uv run pytest tests/ -v
# All tests should pass
```

---

### Issue 12b: Extraction Tooling

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Extraction Tooling" --body-file issue-12b-extraction-tooling.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify scripts created and executable
test -x scripts/extract_project.sh && echo "✅ extract_project.sh"
test -x scripts/validate_standalone.sh && echo "✅ validate_standalone.sh"

# 2. Run validation script
./scripts/validate_standalone.sh
# Should pass all checks

# 3. Test extraction (dry run)
./scripts/extract_project.sh /tmp/tac-webbuilder-test

# 4. Validate extracted project
cd /tmp/tac-webbuilder-test
./scripts/validate_standalone.sh
# Should pass

# 5. Test extracted project runs
./scripts/start_web.sh &
sleep 5
curl http://localhost:8002/health
# Should return: {"status":"healthy"}
killall uvicorn

# 6. Clean up test
cd ~
rm -rf /tmp/tac-webbuilder-test

# 7. Return to project
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 8. Verify configs use relative paths
cat .env.sample | grep "PROJECT_ROOT=\."
cat config.yaml.sample | grep "root: \."
```

---

### Issue 12c: Documentation & Final Validation

**Create Issue:**
```bash
cd /Users/Warmonger0/tac/tac-7
./scripts/gi --title "Documentation & Final Validation" --body-file issue-12c-final-validation.md
```

**Validate After Completion:**
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# 1. Verify EXTRACTION_GUIDE.md created
test -f EXTRACTION_GUIDE.md && wc -l EXTRACTION_GUIDE.md
# Should show ~200+ lines

# 2. Verify README extraction section added
grep -A 10 "Extracting as Standalone Project" README.md

# 3. Verify ARCHITECTURE.md updated
grep -A 5 "Standalone Deployment" ARCHITECTURE.md

# 4. Run validation script
./scripts/validate_standalone.sh
# Must pass all checks

# 5. Run all tests
uv run pytest tests/ -v
# All tests must pass

# 6. Test full stack
./scripts/start_full.sh &
sleep 10
curl http://localhost:8002/health
curl -I http://localhost:5174
# Both should succeed

# 7. Test frontend integration (manual)
# Open http://localhost:5174
# Submit a test request
# Verify workflow monitoring works

# 8. Stop services
killall uvicorn node

# 9. FINAL EXTRACTION TEST
./scripts/extract_project.sh /tmp/final-validation
cd /tmp/final-validation

# 10. Validate extracted project
./scripts/validate_standalone.sh
# Must pass

# 11. Test extracted project
uv run pytest tests/ -v
# All tests must pass

./scripts/start_full.sh &
sleep 10
curl http://localhost:8002/health
curl -I http://localhost:5174
# Both should succeed

# 12. Stop and clean up
killall uvicorn node
cd ~
rm -rf /tmp/final-validation

# 13. Return to project
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

echo "🎉🎉🎉 RESTRUCTURE COMPLETE! 🎉🎉🎉"
echo "tac-webbuilder is now fully self-contained and extraction-ready!"
```

**🎉🎉🎉 Wave 3 Complete - Project Extraction Ready! 🎉🎉🎉**

---

## Quick Validation Summary

After completing all 9 issues:

```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder

# Structure check
tree app/ -L 2
tree app_docs/ specs/ issues/ -L 1

# Dependency check
./scripts/validate_standalone.sh

# Functional check
uv run pytest tests/ -v
./scripts/start_full.sh &
sleep 10
curl http://localhost:8002/health
curl -I http://localhost:5174
killall uvicorn node

# Extraction check
./scripts/extract_project.sh /tmp/final-test
cd /tmp/final-test
./scripts/validate_standalone.sh
./scripts/start_full.sh &
sleep 10
curl http://localhost:8002/health
killall uvicorn node
cd ~ && rm -rf /tmp/final-test

echo "✅ ALL VALIDATIONS PASSED!"
```

---

## Execution Checklist

Use this checklist to track progress:

**Wave 1: App Structure**
- [ ] 10a: Move Frontend - Issue created & validated
- [ ] 10b: Reorganize Backend - Issue created & validated
- [ ] 10c: Integration & Cleanup - Issue created & validated
- [ ] Wave 1 complete validation passed

**Wave 2: Documentation**
- [ ] 11a: Documentation Structure - Issue created & validated
- [ ] 11b: Move Docs & Specs - Issue created & validated
- [ ] 11c: Move Issue Files - Issue created & validated
- [ ] Wave 2 complete validation passed

**Wave 3: Extraction**
- [ ] 12a: Dependency Audit - Issue created & validated
- [ ] 12b: Extraction Tooling - Issue created & validated
- [ ] 12c: Final Validation - Issue created & validated
- [ ] Wave 3 complete validation passed
- [ ] Full extraction test passed

**Final Milestone**
- [ ] All 9 issues completed
- [ ] All validations passed
- [ ] Project is extraction-ready
- [ ] Documentation is complete
- [ ] 🎉 CELEBRATION! 🎉

---

## Troubleshooting

### If an issue fails validation:

1. **Review the ADW output** for errors
2. **Check the specific validation** that failed
3. **Fix manually if needed** (small fixes)
4. **Re-run validation** to confirm fix
5. **Move to next issue** once validation passes

### If extraction test fails:

1. Check `./scripts/validate_standalone.sh` output
2. Look for parent path references
3. Look for import errors
4. Fix in source project
5. Re-test extraction

### Common issues:

- **Import errors**: Check for `from interfaces.web` references
- **Path errors**: Check for absolute `/Users/Warmonger0/tac/tac-7[^/]` paths
- **Missing files**: Check if all files were moved correctly
- **Script permissions**: Run `chmod +x scripts/*.sh`

---

## Notes

- Execute issues **sequentially** (don't skip ahead)
- **Validate after each issue** before proceeding
- **Validate after each wave** before starting next wave
- Keep the **final extraction test** for Issue 12c only
- If you find issues during validation, **fix them before proceeding**

---

## Success!

When all validations pass:

```
✅ App structure reorganized
✅ Documentation self-contained
✅ Dependencies resolved
✅ Extraction tooling created
✅ All tests passing
✅ Full stack working
✅ Extraction successful

🎉 tac-webbuilder is extraction-ready! 🎉
```
