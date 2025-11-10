#!/bin/bash

# Navigate to project root to source environment
PROJECT_ROOT="$(dirname "$0")/.."
cd "$PROJECT_ROOT"

# Source .ports.env if it exists, otherwise use fallback
if [ -f ".ports.env" ]; then
    source .ports.env
    export FRONTEND_PORT
    echo "📦 Loaded port configuration from .ports.env"
else
    export FRONTEND_PORT=5174
    echo "⚠️  .ports.env not found, using fallback port 5174"
fi

# Navigate to client directory
cd "projects/tac-webbuilder/app/client"

echo "🚀 Starting tac-webbuilder frontend on port ${FRONTEND_PORT}..."
npm run dev
