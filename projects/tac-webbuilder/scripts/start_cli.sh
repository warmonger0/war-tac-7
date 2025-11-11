#!/bin/bash
# Convenience script to launch the tac-webbuilder CLI

# Navigate to the project root directory
cd "$(dirname "$0")/.."

# Run the CLI with uv
uv run python -m interfaces.cli "$@"
