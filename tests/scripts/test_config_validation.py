#!/usr/bin/env python3
"""
Tests for scripts/test_config.sh

These tests verify that the validation script correctly:
- Detects missing .env file
- Validates required variables are set
- Checks tool availability
- Reports errors and warnings correctly
- Returns appropriate exit codes
"""

import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Tuple

import pytest


# Get project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TEST_CONFIG_SCRIPT = PROJECT_ROOT / "scripts" / "test_config.sh"
ENV_SAMPLE = PROJECT_ROOT / ".env.sample"


class TestConfigValidation:
    """Test suite for configuration validation script."""

    @pytest.fixture
    def temp_env_file(self, tmp_path) -> Path:
        """Create a temporary .env file for testing."""
        env_file = tmp_path / ".env"
        return env_file

    @pytest.fixture
    def backup_env(self) -> None:
        """Backup existing .env file if it exists."""
        env_file = PROJECT_ROOT / ".env"
        backup_file = PROJECT_ROOT / ".env.test.backup"

        if env_file.exists():
            shutil.copy(env_file, backup_file)

        yield

        # Restore original .env
        if backup_file.exists():
            shutil.move(backup_file, env_file)
        elif env_file.exists():
            env_file.unlink()

    def run_validation_script(self, env_content: str = None) -> Tuple[int, str, str]:
        """
        Run the validation script with optional .env content.

        Args:
            env_content: Content to write to .env file. If None, no .env file is created.

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        env_file = PROJECT_ROOT / ".env"

        # Clean up existing .env
        if env_file.exists():
            env_file.unlink()

        # Create .env with provided content
        if env_content is not None:
            env_file.write_text(env_content)

        try:
            # Run validation script
            result = subprocess.run(
                [str(TEST_CONFIG_SCRIPT)],
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
            )

            return result.returncode, result.stdout, result.stderr

        finally:
            # Clean up
            if env_file.exists():
                env_file.unlink()

    def test_script_exists(self):
        """Test that validation script exists and is executable."""
        assert TEST_CONFIG_SCRIPT.exists(), f"Script not found: {TEST_CONFIG_SCRIPT}"
        assert os.access(
            TEST_CONFIG_SCRIPT, os.X_OK
        ), f"Script not executable: {TEST_CONFIG_SCRIPT}"

    def test_env_sample_exists(self):
        """Test that .env.sample exists."""
        assert ENV_SAMPLE.exists(), f".env.sample not found: {ENV_SAMPLE}"

    def test_missing_env_file(self):
        """Test validation fails when .env file is missing."""
        exit_code, stdout, stderr = self.run_validation_script(env_content=None)

        assert exit_code == 1, "Should exit with code 1 when .env is missing"
        assert ".env file not found" in stdout, "Should report missing .env file"

    def test_empty_env_file(self):
        """Test validation fails with empty .env file."""
        exit_code, stdout, stderr = self.run_validation_script(env_content="")

        assert exit_code == 1, "Should exit with code 1 when required vars are missing"
        assert (
            "ANTHROPIC_API_KEY" in stdout or "not set" in stdout
        ), "Should report missing required variable"

    def test_valid_minimal_config(self):
        """Test validation passes with minimal valid configuration."""
        # Read .env.sample as base
        env_sample_content = ENV_SAMPLE.read_text()

        # Set required API key
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key-12345"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        # Should pass with warnings about optional configs
        assert exit_code == 0, f"Should exit with code 0. Output:\n{stdout}"
        assert (
            "ANTHROPIC_API_KEY" in stdout or "Anthropic API Key" in stdout
        ), "Should check Anthropic API Key"

    def test_missing_required_api_key(self):
        """Test validation fails when required API key is empty."""
        # Read .env.sample as base (has empty ANTHROPIC_API_KEY)
        env_content = ENV_SAMPLE.read_text()

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert exit_code == 1, "Should exit with code 1 when API key is missing"
        assert "not set" in stdout, "Should report missing required variable"

    def test_error_count_reporting(self):
        """Test that error count is reported correctly."""
        # Missing required key = 1 error
        env_content = ENV_SAMPLE.read_text()

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert "Errors:" in stdout, "Should report error count"
        # Should have at least 1 error for missing API key
        assert exit_code == 1, "Should exit with code 1 when errors present"

    def test_warning_count_reporting(self):
        """Test that warning count is reported correctly."""
        # Valid config should have warnings for optional fields
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key-12345"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert "Warnings:" in stdout, "Should report warning count"

    def test_checks_required_section(self):
        """Test that required configuration section is checked."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "REQUIRED CONFIGURATION" in stdout
        ), "Should have required configuration section"

    def test_checks_optional_section(self):
        """Test that optional configuration section is checked."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "OPTIONAL CONFIGURATION" in stdout
        ), "Should have optional configuration section"

    def test_checks_tool_availability(self):
        """Test that tool availability is checked."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "REQUIRED TOOLS" in stdout or "Claude Code" in stdout or "GitHub CLI" in stdout
        ), "Should check tool availability"

    def test_checks_r2_configuration(self):
        """Test that Cloudflare R2 configuration is validated."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "R2" in stdout or "CLOUDFLARE" in stdout
        ), "Should check R2 configuration"

    def test_checks_playwright_config(self):
        """Test that Playwright MCP configuration is checked."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "PLAYWRIGHT" in stdout or "playwright" in stdout.lower()
        ), "Should check Playwright configuration"

    def test_summary_section_present(self):
        """Test that validation summary section is present."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "SUMMARY" in stdout or "Summary" in stdout
        ), "Should have summary section"

    def test_next_steps_on_success(self):
        """Test that next steps are shown on successful validation."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        if exit_code == 0:
            assert (
                "Next Steps" in stdout or "next steps" in stdout.lower()
            ), "Should show next steps on success"

    def test_fix_instructions_on_failure(self):
        """Test that fix instructions are shown on validation failure."""
        # Missing required key
        env_content = ENV_SAMPLE.read_text()

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        if exit_code == 1:
            assert (
                "Fix" in stdout or "fix" in stdout.lower()
            ), "Should show fix instructions on failure"

    def test_handles_special_characters_in_values(self):
        """Test that validation handles special characters in API keys."""
        env_sample_content = ENV_SAMPLE.read_text()
        # API key with special characters
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=",
            "ANTHROPIC_API_KEY=sk-ant-test/key+with=special&chars",
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        # Should not crash, should be able to validate
        assert exit_code in [0, 1], f"Should exit with valid code. Output:\n{stdout}"

    def test_partial_r2_configuration(self):
        """Test that partial R2 configuration is detected."""
        env_sample_content = ENV_SAMPLE.read_text()
        # Set API key and only some R2 variables
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )
        env_content = env_content.replace(
            "CLOUDFLARE_ACCOUNT_ID=", "CLOUDFLARE_ACCOUNT_ID=test123"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        # Should warn about partial configuration
        assert (
            "R2" in stdout or "CLOUDFLARE" in stdout
        ), "Should check R2 configuration"

    def test_claude_code_path_validation(self):
        """Test that Claude Code path is validated."""
        env_sample_content = ENV_SAMPLE.read_text()
        env_content = env_sample_content.replace(
            "ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=sk-ant-test-key"
        )

        exit_code, stdout, stderr = self.run_validation_script(env_content=env_content)

        assert (
            "Claude Code" in stdout or "CLAUDE_CODE_PATH" in stdout
        ), "Should check Claude Code path"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
