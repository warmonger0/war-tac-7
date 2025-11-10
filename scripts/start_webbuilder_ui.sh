#!/bin/bash
cd "$(dirname "$0")/../app/webbuilder/client"

echo "🎨 Starting webbuilder frontend on port 5174..."
npm run dev
