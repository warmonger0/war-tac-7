"""Tests for CLI configuration manager."""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml
import tempfile

from interfaces.cli.config_manager import (
    ensure_config_dir,
    get_config_path,
    load_cli_config,
    get_config_value,
    set_config_value,
    list_config,
    display_config,
    reset_config,
    validate_config,
    DEFAULT_CONFIG_PATH,
)


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        config_data = {
            "github": {
                "default_repo": "owner/repo",
                "auto_post": False,
            },
            "adw": {
                "default_workflow": "adw_sdlc_iso",
            },
        }
        yaml.dump(config_data, f)
        temp_path = f.name

    yield Path(temp_path)

    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def mock_config_path(temp_config_file):
    """Mock the config path to use temp file."""
    with patch("interfaces.cli.config_manager.get_config_path") as mock:
        mock.return_value = temp_config_file
        yield mock


class TestConfigDirectory:
    """Test configuration directory management."""

    def test_ensure_config_dir(self):
        """Test config directory creation."""
        with patch("interfaces.cli.config_manager.DEFAULT_CONFIG_PATH") as mock_path:
            mock_parent = MagicMock()
            mock_path.parent = mock_parent
            ensure_config_dir()
            mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestConfigPath:
    """Test configuration path resolution."""

    def test_get_config_path_default(self):
        """Test default config path."""
        with patch.dict(os.environ, {}, clear=True):
            path = get_config_path()
            assert path == DEFAULT_CONFIG_PATH

    def test_get_config_path_custom(self):
        """Test custom config path from environment."""
        custom_path = "/custom/path/config.yaml"
        with patch.dict(os.environ, {"WEBBUILDER_CONFIG": custom_path}):
            path = get_config_path()
            assert path == Path(custom_path)


class TestConfigLoading:
    """Test configuration loading."""

    def test_load_cli_config_existing(self, temp_config_file):
        """Test loading existing config file."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = temp_config_file
            config = load_cli_config()
            assert config.github.default_repo == "owner/repo"

    def test_load_cli_config_nonexistent(self):
        """Test loading when config file doesn't exist."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = Path("/nonexistent/config.yaml")
            config = load_cli_config()
            # Should load defaults
            assert config is not None


class TestGetConfig:
    """Test getting configuration values."""

    def test_get_config_value_success(self, mock_config_path):
        """Test getting existing config value."""
        value = get_config_value("github.default_repo")
        assert value == "owner/repo"

    def test_get_config_value_nested(self, mock_config_path):
        """Test getting nested config value."""
        value = get_config_value("adw.default_workflow")
        assert value == "adw_sdlc_iso"

    def test_get_config_value_nonexistent(self, mock_config_path):
        """Test getting non-existent config value."""
        value = get_config_value("nonexistent.key")
        assert value is None

    def test_get_config_value_boolean(self, mock_config_path):
        """Test getting boolean config value."""
        value = get_config_value("github.auto_post")
        assert value == "False"


class TestSetConfig:
    """Test setting configuration values."""

    def test_set_config_value_success(self, temp_config_file):
        """Test setting config value."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = temp_config_file
            with patch("interfaces.cli.config_manager.show_success"):
                result = set_config_value("github.default_repo", "newowner/newrepo")
                assert result is True

                # Verify value was written
                with open(temp_config_file) as f:
                    data = yaml.safe_load(f)
                    assert data["github"]["default_repo"] == "newowner/newrepo"

    def test_set_config_value_boolean(self, temp_config_file):
        """Test setting boolean config value."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = temp_config_file
            with patch("interfaces.cli.config_manager.show_success"):
                set_config_value("github.auto_post", "true")

                # Verify boolean conversion
                with open(temp_config_file) as f:
                    data = yaml.safe_load(f)
                    assert data["github"]["auto_post"] is True

    def test_set_config_value_integer(self, temp_config_file):
        """Test setting integer config value."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = temp_config_file
            with patch("interfaces.cli.config_manager.show_success"):
                set_config_value("interfaces.web.port", "8080")

                # Verify integer conversion
                with open(temp_config_file) as f:
                    data = yaml.safe_load(f)
                    assert data["interfaces"]["web"]["port"] == 8080

    def test_set_config_value_new_file(self):
        """Test setting config value creates new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_config = Path(tmpdir) / "new_config.yaml"
            with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
                mock_path.return_value = new_config
                with patch("interfaces.cli.config_manager.ensure_config_dir"):
                    with patch("interfaces.cli.config_manager.show_success"):
                        result = set_config_value("github.default_repo", "owner/repo")
                        assert result is True
                        assert new_config.exists()


class TestListConfig:
    """Test listing configuration."""

    def test_list_config(self, mock_config_path):
        """Test listing all config values."""
        config_dict = list_config()
        assert "github.default_repo" in config_dict
        assert "adw.default_workflow" in config_dict
        assert config_dict["github.default_repo"] == "owner/repo"

    def test_list_config_includes_all_sections(self, mock_config_path):
        """Test that list_config includes all config sections."""
        config_dict = list_config()
        # Check for keys from different sections
        assert any(k.startswith("github.") for k in config_dict)
        assert any(k.startswith("adw.") for k in config_dict)
        assert any(k.startswith("interfaces.") for k in config_dict)


class TestDisplayConfig:
    """Test displaying configuration."""

    def test_display_config(self, mock_config_path):
        """Test displaying config as table."""
        with patch("interfaces.cli.config_manager.print_table"):
            with patch("builtins.print"):
                display_config()
                # Should not raise any errors

    def test_display_config_empty(self):
        """Test displaying when no config available."""
        with patch("interfaces.cli.config_manager.list_config") as mock_list:
            mock_list.return_value = {}
            with patch("interfaces.cli.config_manager.show_error"):
                display_config()


class TestResetConfig:
    """Test resetting configuration."""

    def test_reset_config_existing(self, temp_config_file):
        """Test resetting existing config file."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = temp_config_file
            with patch("interfaces.cli.config_manager.show_success"):
                result = reset_config()
                assert result is True
                assert not temp_config_file.exists()

    def test_reset_config_nonexistent(self):
        """Test resetting when no config file exists."""
        with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
            mock_path.return_value = Path("/nonexistent/config.yaml")
            with patch("interfaces.cli.config_manager.show_error"):
                result = reset_config()
                assert result is False


class TestValidateConfig:
    """Test configuration validation."""

    def test_validate_config_valid(self, mock_config_path):
        """Test validating correct config."""
        with patch("interfaces.cli.config_manager.show_success"):
            result = validate_config()
            assert result is True

    def test_validate_config_invalid_repo_format(self):
        """Test validation fails for invalid repo format."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump({"github": {"default_repo": "invalid"}}, f)
            temp_path = Path(f.name)

        try:
            with patch("interfaces.cli.config_manager.get_config_path") as mock_path:
                mock_path.return_value = temp_path
                with patch("interfaces.cli.config_manager.show_error"):
                    # The validation will fail during config loading
                    try:
                        result = validate_config()
                        # If it doesn't raise, it should return False
                        assert result is False
                    except ValueError:
                        # Expected - invalid config format
                        pass
        finally:
            temp_path.unlink(missing_ok=True)
