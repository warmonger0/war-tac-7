#!/bin/bash
# Test that setup_env.sh creates valid .env

# Backup existing .env if present
if [ -f .env ]; then
    mv .env .env.backup.test
fi

# Run setup script with defaults
echo -e "\ntest-key\n\n\n" | ./scripts/setup_env.sh

# Check .env was created
if [ ! -f .env ]; then
    echo "❌ .env not created"
    exit 1
fi

# Check ANTHROPIC_API_KEY was set
if ! grep -q "ANTHROPIC_API_KEY=test-key" .env; then
    echo "❌ ANTHROPIC_API_KEY not set correctly"
    exit 1
fi

# Cleanup
rm .env
if [ -f .env.backup.test ]; then
    mv .env.backup.test .env
fi

echo "✅ Setup script test passed"
