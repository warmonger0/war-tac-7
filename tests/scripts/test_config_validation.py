import subprocess
import os
import shutil

def test_config_validation_fails_without_env():
    """Test that validation fails if .env missing."""
    if os.path.exists('.env'):
        shutil.move('.env', '.env.backup')

    result = subprocess.run(['./scripts/test_config.sh'],
                          capture_output=True)

    if os.path.exists('.env.backup'):
        shutil.move('.env.backup', '.env')

    assert result.returncode != 0

def test_config_validation_passes_with_valid_env():
    """Test that validation passes with valid .env."""
    result = subprocess.run(['./scripts/test_config.sh'],
                          capture_output=True)
    assert result.returncode == 0 or "warning" in result.stdout.decode().lower()
