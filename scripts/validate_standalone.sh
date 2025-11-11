#!/bin/bash
set -e

echo "🔍 Validating standalone project..."
ERRORS=0

# Check required directories exist
echo "  Checking directory structure..."
for dir in app scripts tests adws; do
    [ -d "$dir" ] || { echo "    ❌ Missing: $dir"; ERRORS=$((ERRORS+1)); }
done

# Check optional directories with warnings
for dir in app/client app/server; do
    [ -d "$dir" ] || echo "    ⚠️  Optional directory missing: $dir"
done

# Check parent path references
echo "  Checking for parent path references..."
REFS=$(grep -r "/Users/Warmonger0/tac/tac-7[^/]" . --include="*.py" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
[ "$REFS" = "0" ] || { echo "    ❌ Found $REFS parent path references"; ERRORS=$((ERRORS+1)); }

# Check Python imports work (if app.server exists)
if [ -d "app/server" ] && [ -f "app/server/main.py" ]; then
    echo "  Checking Python imports..."
    python3 -c "from app.server.main import app" 2>/dev/null || { echo "    ❌ Import failed"; ERRORS=$((ERRORS+1)); }
else
    echo "  ⚠️  Skipping Python import check (no app/server/main.py)"
fi

# Check scripts are executable
echo "  Checking script permissions..."
for script in scripts/*.sh; do
    [ -x "$script" ] || { echo "    ❌ Not executable: $script"; ERRORS=$((ERRORS+1)); }
done

# Report results
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ Validation passed - project is standalone!"
    exit 0
else
    echo "❌ Validation failed with $ERRORS error(s)"
    exit 1
fi
