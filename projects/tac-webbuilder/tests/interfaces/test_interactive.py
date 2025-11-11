"""Tests for CLI interactive mode."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

from interfaces.cli.interactive import (
    PathValidator,
    NonEmptyValidator,
    prompt_project_path,
    prompt_nl_request,
    handle_submit_request,
    handle_view_history,
    handle_create_project,
    handle_integrate_adw,
    run_interactive_mode,
)


class TestValidators:
    """Test questionary validators."""

    def test_path_validator_valid(self):
        """Test path validator with valid path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            validator = PathValidator()
            doc = MagicMock(text=tmpdir)
            # Should not raise
            validator.validate(doc)

    def test_path_validator_nonexistent(self):
        """Test path validator with non-existent path."""
        from questionary import ValidationError

        validator = PathValidator()
        doc = MagicMock(text="/nonexistent/path")

        with pytest.raises(ValidationError):
            validator.validate(doc)

    def test_path_validator_file(self):
        """Test path validator with file instead of directory."""
        from questionary import ValidationError

        with tempfile.NamedTemporaryFile() as tmp:
            validator = PathValidator()
            doc = MagicMock(text=tmp.name)

            with pytest.raises(ValidationError):
                validator.validate(doc)

    def test_non_empty_validator_valid(self):
        """Test non-empty validator with valid input."""
        validator = NonEmptyValidator()
        doc = MagicMock(text="some text")
        # Should not raise
        validator.validate(doc)

    def test_non_empty_validator_empty(self):
        """Test non-empty validator with empty input."""
        from questionary import ValidationError

        validator = NonEmptyValidator()
        doc = MagicMock(text="")

        with pytest.raises(ValidationError):
            validator.validate(doc)

    def test_non_empty_validator_whitespace(self):
        """Test non-empty validator with whitespace."""
        from questionary import ValidationError

        validator = NonEmptyValidator()
        doc = MagicMock(text="   ")

        with pytest.raises(ValidationError):
            validator.validate(doc)


class TestPromptProjectPath:
    """Test project path prompting."""

    @patch("questionary.confirm")
    def test_prompt_project_path_use_current(self, mock_confirm):
        """Test using current directory."""
        mock_confirm.return_value.ask.return_value = True

        result = prompt_project_path()

        assert result == str(Path.cwd())

    @patch("questionary.path")
    @patch("questionary.confirm")
    def test_prompt_project_path_custom(self, mock_confirm, mock_path):
        """Test using custom path."""
        mock_confirm.return_value.ask.return_value = False
        mock_path.return_value.ask.return_value = "/custom/path"

        result = prompt_project_path()

        assert result == "/custom/path"

    @patch("questionary.confirm")
    def test_prompt_project_path_cancelled(self, mock_confirm):
        """Test cancelling path prompt."""
        mock_confirm.return_value.ask.return_value = None

        result = prompt_project_path()

        assert result is None

    @patch("questionary.confirm")
    def test_prompt_project_path_keyboard_interrupt(self, mock_confirm):
        """Test keyboard interrupt during path prompt."""
        mock_confirm.return_value.ask.side_effect = KeyboardInterrupt

        result = prompt_project_path()

        assert result is None


class TestPromptNLRequest:
    """Test natural language request prompting."""

    @patch("questionary.text")
    def test_prompt_nl_request_success(self, mock_text):
        """Test successful NL request prompt."""
        mock_text.return_value.ask.return_value = "Add user authentication"

        result = prompt_nl_request()

        assert result == "Add user authentication"

    @patch("questionary.text")
    def test_prompt_nl_request_cancelled(self, mock_text):
        """Test cancelled NL request prompt."""
        mock_text.return_value.ask.return_value = None

        result = prompt_nl_request()

        assert result is None

    @patch("questionary.text")
    def test_prompt_nl_request_keyboard_interrupt(self, mock_text):
        """Test keyboard interrupt during NL request prompt."""
        mock_text.return_value.ask.side_effect = KeyboardInterrupt

        result = prompt_nl_request()

        assert result is None


class TestHandleSubmitRequest:
    """Test submit request handler."""

    @patch("interfaces.cli.interactive.handle_request")
    @patch("questionary.confirm")
    @patch("interfaces.cli.interactive.prompt_nl_request")
    @patch("interfaces.cli.interactive.prompt_project_path")
    @patch("interfaces.cli.interactive.show_info")
    @patch("builtins.print")
    def test_handle_submit_request_success(
        self,
        mock_print,
        mock_show_info,
        mock_prompt_path,
        mock_prompt_nl,
        mock_confirm,
        mock_handle_request,
    ):
        """Test successful request submission."""
        mock_prompt_path.return_value = "/test/path"
        mock_prompt_nl.return_value = "Test request"
        mock_confirm.return_value.ask.return_value = True
        mock_handle_request.return_value = True

        result = handle_submit_request()

        assert result is True
        mock_handle_request.assert_called_once_with(
            nl_input="Test request",
            project_path="/test/path",
            auto_post=False,
        )

    @patch("interfaces.cli.interactive.prompt_project_path")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.show_error")
    @patch("builtins.print")
    def test_handle_submit_request_cancelled_path(
        self,
        mock_print,
        mock_show_error,
        mock_show_info,
        mock_prompt_path,
    ):
        """Test cancelling at path prompt."""
        mock_prompt_path.return_value = None

        result = handle_submit_request()

        assert result is False
        mock_show_error.assert_called_with("Cancelled")

    @patch("interfaces.cli.interactive.prompt_nl_request")
    @patch("interfaces.cli.interactive.prompt_project_path")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.show_error")
    @patch("builtins.print")
    def test_handle_submit_request_cancelled_nl(
        self,
        mock_print,
        mock_show_error,
        mock_show_info,
        mock_prompt_path,
        mock_prompt_nl,
    ):
        """Test cancelling at NL request prompt."""
        mock_prompt_path.return_value = "/test/path"
        mock_prompt_nl.return_value = None

        result = handle_submit_request()

        assert result is False

    @patch("questionary.confirm")
    @patch("interfaces.cli.interactive.prompt_nl_request")
    @patch("interfaces.cli.interactive.prompt_project_path")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.show_error")
    @patch("builtins.print")
    def test_handle_submit_request_cancelled_confirm(
        self,
        mock_print,
        mock_show_error,
        mock_show_info,
        mock_prompt_path,
        mock_prompt_nl,
        mock_confirm,
    ):
        """Test cancelling at confirmation prompt."""
        mock_prompt_path.return_value = "/test/path"
        mock_prompt_nl.return_value = "Test request"
        mock_confirm.return_value.ask.return_value = False

        result = handle_submit_request()

        assert result is False


class TestHandleViewHistory:
    """Test view history handler."""

    @patch("interfaces.cli.interactive.get_history")
    @patch("questionary.select")
    def test_handle_view_history_default(self, mock_select, mock_get_history):
        """Test viewing history with default limit."""
        mock_history = MagicMock()
        mock_history.get_all.return_value = []
        mock_get_history.return_value = mock_history
        mock_select.return_value.ask.return_value = "10 (default)"

        result = handle_view_history()

        assert result is True
        mock_history.display.assert_called_once_with(limit=10)

    @patch("interfaces.cli.interactive.get_history")
    @patch("questionary.select")
    def test_handle_view_history_all(self, mock_select, mock_get_history):
        """Test viewing all history."""
        mock_history = MagicMock()
        mock_history.get_all.return_value = [1, 2, 3, 4, 5]
        mock_get_history.return_value = mock_history
        mock_select.return_value.ask.return_value = "All"

        result = handle_view_history()

        assert result is True
        mock_history.display.assert_called_once_with(limit=5)

    @patch("questionary.select")
    def test_handle_view_history_cancelled(self, mock_select):
        """Test cancelling history view."""
        mock_select.return_value.ask.return_value = None

        result = handle_view_history()

        assert result is False


class TestHandleCreateProject:
    """Test create project handler (stub)."""

    @patch("interfaces.cli.interactive.show_info")
    def test_handle_create_project(self, mock_show_info):
        """Test create project stub."""
        result = handle_create_project()
        assert result is False
        assert mock_show_info.call_count >= 1


class TestHandleIntegrateADW:
    """Test ADW integration handler (stub)."""

    @patch("interfaces.cli.interactive.show_info")
    def test_handle_integrate_adw(self, mock_show_info):
        """Test integrate ADW stub."""
        result = handle_integrate_adw()
        assert result is False
        assert mock_show_info.call_count >= 1


class TestRunInteractiveMode:
    """Test the main interactive mode loop."""

    @patch("interfaces.cli.interactive.handle_submit_request")
    @patch("questionary.select")
    @patch("interfaces.cli.interactive.show_success")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.print_divider")
    @patch("builtins.print")
    def test_run_interactive_mode_exit(
        self,
        mock_print,
        mock_divider,
        mock_show_info,
        mock_show_success,
        mock_select,
        mock_handle_submit,
    ):
        """Test exiting interactive mode."""
        mock_select.return_value.ask.return_value = "Exit"

        run_interactive_mode()

        mock_show_success.assert_called()

    @patch("interfaces.cli.interactive.handle_submit_request")
    @patch("questionary.select")
    @patch("interfaces.cli.interactive.show_success")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.print_divider")
    @patch("builtins.print")
    def test_run_interactive_mode_submit_then_exit(
        self,
        mock_print,
        mock_divider,
        mock_show_info,
        mock_show_success,
        mock_select,
        mock_handle_submit,
    ):
        """Test submitting request then exiting."""
        mock_select.return_value.ask.side_effect = [
            "Submit a request for existing project",
            "Exit",
        ]
        mock_handle_submit.return_value = True

        run_interactive_mode()

        mock_handle_submit.assert_called_once()

    @patch("questionary.select")
    @patch("interfaces.cli.interactive.show_success")
    @patch("interfaces.cli.interactive.show_info")
    @patch("interfaces.cli.interactive.print_divider")
    @patch("builtins.print")
    def test_run_interactive_mode_keyboard_interrupt(
        self,
        mock_print,
        mock_divider,
        mock_show_info,
        mock_show_success,
        mock_select,
    ):
        """Test keyboard interrupt in interactive mode."""
        mock_select.return_value.ask.side_effect = KeyboardInterrupt

        run_interactive_mode()

        mock_show_success.assert_called()
