#!/bin/bash
cd "$(dirname "$0")/../app/server"

echo "🚀 Starting webbuilder backend on port 8002..."
uv run uvicorn main:app --host 0.0.0.0 --port 8002 --reload
