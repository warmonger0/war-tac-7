#!/bin/bash
cd "$(dirname "$0")/../projects/tac-webbuilder/app/client"

echo "🎨 Starting webbuilder frontend on port 5174..."
npm run dev
