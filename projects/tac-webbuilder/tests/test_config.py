"""
Tests for configuration management system.
"""

import os
from pathlib import Path
import tempfile
import pytest
import yaml

from core.config import (
    AppConfig,
    GitHubConfig,
    ADWConfig,
    InterfacesConfig,
    ClaudeConfig,
    load_config,
)


class TestGitHubConfig:
    """Tests for GitHub configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = GitHubConfig()
        assert config.default_repo == ""
        assert config.auto_post is False
        assert config.pat is None

    def test_repo_format_validation(self):
        """Test repository format validation."""
        # Valid format
        config = GitHubConfig(default_repo="owner/repo")
        assert config.default_repo == "owner/repo"

        # Invalid format should raise error
        with pytest.raises(ValueError, match="Repository must be in format"):
            GitHubConfig(default_repo="invalid-format")

    def test_environment_variable_loading(self):
        """Test loading from environment variables."""
        os.environ["TWB_GITHUB_DEFAULT_REPO"] = "test/repo"
        os.environ["TWB_GITHUB_AUTO_POST"] = "true"

        config = GitHubConfig()
        assert config.default_repo == "test/repo"
        assert config.auto_post is True

        # Cleanup
        del os.environ["TWB_GITHUB_DEFAULT_REPO"]
        del os.environ["TWB_GITHUB_AUTO_POST"]


class TestADWConfig:
    """Tests for ADW configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ADWConfig()
        assert config.default_workflow == "adw_sdlc_iso"
        assert config.default_model_set == "base"

    def test_environment_variable_loading(self):
        """Test loading from environment variables."""
        os.environ["TWB_ADW_DEFAULT_WORKFLOW"] = "adw_plan_build_iso"
        os.environ["TWB_ADW_DEFAULT_MODEL_SET"] = "advanced"

        config = ADWConfig()
        assert config.default_workflow == "adw_plan_build_iso"
        assert config.default_model_set == "advanced"

        # Cleanup
        del os.environ["TWB_ADW_DEFAULT_WORKFLOW"]
        del os.environ["TWB_ADW_DEFAULT_MODEL_SET"]


class TestInterfacesConfig:
    """Tests for interfaces configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = InterfacesConfig()
        assert config.cli.enabled is True
        assert config.web.enabled is True
        assert config.web.port == 5174
        assert config.web.host == "127.0.0.1"

    def test_port_validation(self):
        """Test port number validation."""
        # Valid ports
        from core.config import WebConfig

        config = WebConfig(port=8080)
        assert config.port == 8080

        # Invalid ports
        with pytest.raises(ValueError, match="Port must be between"):
            WebConfig(port=0)

        with pytest.raises(ValueError, match="Port must be between"):
            WebConfig(port=70000)


class TestClaudeConfig:
    """Tests for Claude configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = ClaudeConfig()
        assert config.code_path == "/usr/local/bin/claude"
        assert config.api_key is None


class TestAppConfig:
    """Tests for main application configuration."""

    def test_default_values(self):
        """Test default configuration values."""
        config = AppConfig()
        assert isinstance(config.github, GitHubConfig)
        assert isinstance(config.adw, ADWConfig)
        assert isinstance(config.interfaces, InterfacesConfig)
        assert isinstance(config.claude, ClaudeConfig)

    def test_from_yaml(self):
        """Test loading configuration from YAML file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml_config = {
                "github": {
                    "default_repo": "owner/test-repo",
                    "auto_post": True,
                },
                "adw": {
                    "default_workflow": "adw_test_iso",
                    "default_model_set": "advanced",
                },
                "interfaces": {
                    "cli": {"enabled": False},
                    "web": {"enabled": True, "port": 8080},
                },
                "claude": {
                    "code_path": "/custom/path/claude",
                },
            }
            yaml.dump(yaml_config, f)
            yaml_path = f.name

        try:
            config = AppConfig.from_yaml(yaml_path)

            assert config.github.default_repo == "owner/test-repo"
            assert config.github.auto_post is True
            assert config.adw.default_workflow == "adw_test_iso"
            assert config.adw.default_model_set == "advanced"
            assert config.interfaces.cli.enabled is False
            assert config.interfaces.web.enabled is True
            assert config.interfaces.web.port == 8080
            assert config.claude.code_path == "/custom/path/claude"
        finally:
            os.unlink(yaml_path)

    def test_from_yaml_file_not_found(self):
        """Test loading from non-existent YAML file."""
        with pytest.raises(FileNotFoundError):
            AppConfig.from_yaml("/nonexistent/config.yaml")

    def test_yaml_values_loaded(self):
        """Test that YAML configuration values are properly loaded."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml_config = {
                "github": {
                    "default_repo": "yaml/repo",
                    "auto_post": True,
                },
                "adw": {
                    "default_workflow": "yaml_workflow",
                },
            }
            yaml.dump(yaml_config, f)
            yaml_path = f.name

        try:
            config = AppConfig.from_yaml(yaml_path)

            # YAML values should be loaded
            assert config.github.default_repo == "yaml/repo"
            assert config.github.auto_post is True
            assert config.adw.default_workflow == "yaml_workflow"
        finally:
            os.unlink(yaml_path)

    def test_load_with_default_config(self):
        """Test load() method with default config.yaml."""
        # Create a temporary directory to simulate project root
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            yaml_config = {
                "github": {"default_repo": "test/repo"},
            }
            with open(config_path, "w") as f:
                yaml.dump(yaml_config, f)

            # Change to temp directory
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                config = AppConfig.load()
                assert config.github.default_repo == "test/repo"
            finally:
                os.chdir(original_cwd)

    def test_load_config_function(self):
        """Test the convenience load_config function."""
        config = load_config()
        assert isinstance(config, AppConfig)
