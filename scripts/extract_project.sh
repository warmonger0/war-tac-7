#!/bin/bash
set -e

DEST=${1:?Usage: $0 <destination>}
SRC=$(pwd)

# Pre-flight checks
echo "🔍 Pre-flight checks..."

# Check source is tac-webbuilder
[ -d "app/server" ] || { echo "❌ Run from tac-webbuilder root"; exit 1; }

# Check destination doesn't exist
[ -d "$DEST" ] && { echo "❌ $DEST already exists"; exit 1; }

# Check we're in projects/tac-webbuilder
[[ "$SRC" == */projects/tac-webbuilder ]] || echo "⚠️  Warning: Not in expected location"

echo "📦 Extracting tac-webbuilder to $DEST..."

# Copy with exclusions
echo "  Copying files..."
rsync -av --exclude='.git' --exclude='node_modules' \
  --exclude='.venv' --exclude='__pycache__' \
  --exclude='*.pyc' --exclude='.DS_Store' \
  --exclude='trees/*' --exclude='logs/*' \
  "$SRC/" "$DEST/" || { echo "❌ rsync failed"; exit 1; }

cd "$DEST"

# Setup git
echo "  Initializing git..."
git init || { echo "❌ git init failed"; exit 1; }
git add .
git commit -m "Initial extraction from tac-webbuilder" || { echo "❌ git commit failed"; exit 1; }

# Setup config
echo "  Creating config files..."
cp .env.sample .env 2>/dev/null || echo "  ⚠️  No .env.sample found"
cp config.yaml.sample config.yaml 2>/dev/null || echo "  ⚠️  No config.yaml.sample found"

# Python setup (if pyproject.toml exists)
if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
    echo "  Setting up Python environment..."
    uv venv || { echo "❌ uv venv failed"; exit 1; }
    source .venv/bin/activate
    uv pip install -e . || { echo "❌ pip install failed"; exit 1; }
else
    echo "  ⚠️  No Python project files found (pyproject.toml or setup.py), skipping Python setup"
fi

# Node setup (if app/client exists)
if [ -d "app/client" ]; then
    echo "  Setting up Node environment..."
    cd app/client
    npm install || { echo "❌ npm install failed"; exit 1; }
    cd "$DEST"
else
    echo "  ⚠️  No app/client directory found, skipping Node setup"
fi

cd "$DEST"
echo ""
echo "✅ Extraction complete!"
echo ""
echo "Next steps:"
echo "  cd $DEST"
echo "  ./scripts/validate_standalone.sh"
echo "  ./scripts/start_full.sh"
