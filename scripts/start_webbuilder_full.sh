#!/bin/bash

# Start both backend and frontend
./scripts/start_webbuilder.sh &
BACKEND_PID=$!

./scripts/start_webbuilder_ui.sh &
FRONTEND_PID=$!

echo "✅ Web UI running:"
echo "   Frontend: http://localhost:5174"
echo "   Backend:  http://localhost:8002"
echo "   API Docs: http://localhost:8002/docs"

# Cleanup on exit
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT

wait
