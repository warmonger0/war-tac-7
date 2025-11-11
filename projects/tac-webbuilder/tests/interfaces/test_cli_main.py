"""Tests for main CLI entry point."""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from interfaces.cli.main import app


runner = CliRunner()


class TestRequestCommand:
    """Test the request command."""

    @patch("interfaces.cli.main.handle_request")
    def test_request_basic(self, mock_handle):
        """Test basic request command."""
        mock_handle.return_value = True

        result = runner.invoke(app, ["request", "Add user authentication"])

        assert result.exit_code == 0
        mock_handle.assert_called_once_with(
            nl_input="Add user authentication",
            project_path=None,
            auto_post=False,
        )

    @patch("interfaces.cli.main.handle_request")
    def test_request_with_project(self, mock_handle):
        """Test request with project path."""
        mock_handle.return_value = True

        result = runner.invoke(
            app,
            ["request", "Fix bug", "--project", "/path/to/project"]
        )

        assert result.exit_code == 0
        mock_handle.assert_called_once_with(
            nl_input="Fix bug",
            project_path="/path/to/project",
            auto_post=False,
        )

    @patch("interfaces.cli.main.handle_request")
    def test_request_with_auto_post(self, mock_handle):
        """Test request with auto-post flag."""
        mock_handle.return_value = True

        result = runner.invoke(
            app,
            ["request", "Add feature", "--auto-post"]
        )

        assert result.exit_code == 0
        mock_handle.assert_called_once_with(
            nl_input="Add feature",
            project_path=None,
            auto_post=True,
        )

    @patch("interfaces.cli.main.handle_request")
    def test_request_failure(self, mock_handle):
        """Test request command failure."""
        mock_handle.return_value = False

        result = runner.invoke(app, ["request", "Test"])

        assert result.exit_code == 1


class TestInteractiveCommand:
    """Test the interactive command."""

    @patch("interfaces.cli.main.run_interactive_mode")
    def test_interactive(self, mock_run):
        """Test interactive command."""
        result = runner.invoke(app, ["interactive"])

        assert result.exit_code == 0
        mock_run.assert_called_once()


class TestHistoryCommand:
    """Test the history command."""

    @patch("interfaces.cli.main.get_history")
    def test_history_default(self, mock_get_history):
        """Test history command with default limit."""
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        result = runner.invoke(app, ["history"])

        assert result.exit_code == 0
        mock_history.display.assert_called_once_with(limit=10)

    @patch("interfaces.cli.main.get_history")
    def test_history_custom_limit(self, mock_get_history):
        """Test history command with custom limit."""
        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        result = runner.invoke(app, ["history", "--limit", "25"])

        assert result.exit_code == 0
        mock_history.display.assert_called_once_with(limit=25)


class TestConfigCommand:
    """Test the config command."""

    @patch("interfaces.cli.main.display_config")
    def test_config_list(self, mock_display):
        """Test config list action."""
        result = runner.invoke(app, ["config", "list"])

        assert result.exit_code == 0
        mock_display.assert_called_once()

    @patch("interfaces.cli.main.get_config_value")
    @patch("interfaces.cli.main.show_success")
    def test_config_get_success(self, mock_show_success, mock_get):
        """Test config get action success."""
        mock_get.return_value = "owner/repo"

        result = runner.invoke(app, ["config", "get", "github.default_repo"])

        assert result.exit_code == 0
        mock_get.assert_called_once_with("github.default_repo")

    @patch("interfaces.cli.main.get_config_value")
    @patch("interfaces.cli.main.show_error")
    def test_config_get_not_found(self, mock_show_error, mock_get):
        """Test config get action with non-existent key."""
        mock_get.return_value = None

        result = runner.invoke(app, ["config", "get", "nonexistent.key"])

        assert result.exit_code == 1

    @patch("interfaces.cli.main.set_config_value")
    def test_config_set_success(self, mock_set):
        """Test config set action success."""
        mock_set.return_value = True

        result = runner.invoke(
            app,
            ["config", "set", "github.default_repo", "owner/repo"]
        )

        assert result.exit_code == 0
        mock_set.assert_called_once_with("github.default_repo", "owner/repo")

    @patch("interfaces.cli.main.set_config_value")
    def test_config_set_failure(self, mock_set):
        """Test config set action failure."""
        mock_set.return_value = False

        result = runner.invoke(
            app,
            ["config", "set", "test.key", "value"]
        )

        assert result.exit_code == 1

    @patch("interfaces.cli.main.show_error")
    def test_config_set_missing_args(self, mock_show_error):
        """Test config set without required arguments."""
        result = runner.invoke(app, ["config", "set", "key"])

        assert result.exit_code == 1
        mock_show_error.assert_called_once()

    @patch("interfaces.cli.main.reset_config")
    def test_config_reset_success(self, mock_reset):
        """Test config reset action success."""
        mock_reset.return_value = True

        result = runner.invoke(app, ["config", "reset"])

        assert result.exit_code == 0
        mock_reset.assert_called_once()

    @patch("interfaces.cli.main.validate_config")
    def test_config_validate_success(self, mock_validate):
        """Test config validate action success."""
        mock_validate.return_value = True

        result = runner.invoke(app, ["config", "validate"])

        assert result.exit_code == 0
        mock_validate.assert_called_once()

    @patch("interfaces.cli.main.show_error")
    def test_config_invalid_action(self, mock_show_error):
        """Test config with invalid action."""
        result = runner.invoke(app, ["config", "invalid"])

        assert result.exit_code == 1
        mock_show_error.assert_called_once()


class TestIntegrateCommand:
    """Test the integrate command."""

    @patch("interfaces.cli.main.handle_integrate")
    def test_integrate(self, mock_handle):
        """Test integrate command."""
        mock_handle.return_value = True

        result = runner.invoke(app, ["integrate", "/path/to/project"])

        assert result.exit_code == 0
        mock_handle.assert_called_once_with("/path/to/project")

    @patch("interfaces.cli.main.handle_integrate")
    def test_integrate_failure(self, mock_handle):
        """Test integrate command failure."""
        mock_handle.return_value = False

        result = runner.invoke(app, ["integrate", "/path"])

        assert result.exit_code == 1


class TestNewCommand:
    """Test the new command."""

    @patch("interfaces.cli.main.handle_new_project")
    def test_new_default_framework(self, mock_handle):
        """Test new command with default framework."""
        mock_handle.return_value = True

        result = runner.invoke(app, ["new", "myproject"])

        assert result.exit_code == 0
        mock_handle.assert_called_once_with("myproject", "react-vite")

    @patch("interfaces.cli.main.handle_new_project")
    def test_new_custom_framework(self, mock_handle):
        """Test new command with custom framework."""
        mock_handle.return_value = True

        result = runner.invoke(
            app,
            ["new", "myproject", "--framework", "vue"]
        )

        assert result.exit_code == 0
        mock_handle.assert_called_once_with("myproject", "vue")

    @patch("interfaces.cli.main.handle_new_project")
    def test_new_failure(self, mock_handle):
        """Test new command failure."""
        mock_handle.return_value = False

        result = runner.invoke(app, ["new", "myproject"])

        assert result.exit_code == 1


class TestVersionCommand:
    """Test the version command."""

    @patch("interfaces.cli.main.show_info")
    def test_version(self, mock_show_info):
        """Test version command."""
        result = runner.invoke(app, ["version"])

        assert result.exit_code == 0
        mock_show_info.assert_called_once()
        # Check that version string is in the call
        call_args = mock_show_info.call_args[0][0]
        assert "tac-webbuilder CLI version" in call_args


class TestHelpText:
    """Test help text generation."""

    def test_help_main(self):
        """Test main help text."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "webbuilder" in result.stdout.lower()

    def test_help_request(self):
        """Test request command help."""
        result = runner.invoke(app, ["request", "--help"])

        assert result.exit_code == 0
        assert "natural language" in result.stdout.lower()

    def test_help_interactive(self):
        """Test interactive command help."""
        result = runner.invoke(app, ["interactive", "--help"])

        assert result.exit_code == 0
        assert "interactive" in result.stdout.lower()

    def test_help_history(self):
        """Test history command help."""
        result = runner.invoke(app, ["history", "--help"])

        assert result.exit_code == 0
        assert "history" in result.stdout.lower() or "past" in result.stdout.lower()

    def test_help_config(self):
        """Test config command help."""
        result = runner.invoke(app, ["config", "--help"])

        assert result.exit_code == 0
        assert "config" in result.stdout.lower()
