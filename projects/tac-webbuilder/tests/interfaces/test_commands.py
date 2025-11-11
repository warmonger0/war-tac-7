"""Tests for CLI command handlers."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
import subprocess

from interfaces.cli.commands import (
    check_dependencies,
    detect_project_context,
    get_github_repo_url,
    format_issue_preview,
    post_github_issue,
    handle_request,
    handle_new_project,
    handle_integrate,
)


class TestCheckDependencies:
    """Test dependency checking."""

    def test_check_dependencies_all_ok(self):
        """Test when all dependencies are available."""
        with patch("subprocess.run") as mock_run:
            # Mock gh --version
            mock_run.return_value = MagicMock(returncode=0, stdout="gh version 2.0.0")
            all_ok, missing = check_dependencies()
            # Note: Will fail on gh auth status, so not all_ok
            assert isinstance(missing, list)

    def test_check_dependencies_gh_missing(self):
        """Test when gh CLI is missing."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            all_ok, missing = check_dependencies()
            assert not all_ok
            assert "GitHub CLI (gh)" in missing

    def test_check_dependencies_gh_not_authenticated(self):
        """Test when gh CLI is not authenticated."""
        def mock_run_side_effect(cmd, **kwargs):
            if "auth" in cmd:
                return MagicMock(returncode=1)
            return MagicMock(returncode=0)

        with patch("subprocess.run", side_effect=mock_run_side_effect):
            all_ok, missing = check_dependencies()
            assert not all_ok
            assert any("authentication" in dep.lower() for dep in missing)


class TestDetectProjectContext:
    """Test project context detection."""

    def test_detect_project_context_python(self):
        """Test detecting Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            (project_path / "pyproject.toml").touch()

            context = detect_project_context(str(project_path))

            assert context["exists"] is True
            assert context["type"] == "python"
            assert context["has_pyproject"] is True

    def test_detect_project_context_node(self):
        """Test detecting Node.js project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            (project_path / "package.json").touch()

            context = detect_project_context(str(project_path))

            assert context["exists"] is True
            assert context["type"] == "node"
            assert context["has_package_json"] is True

    def test_detect_project_context_git_repo(self):
        """Test detecting git repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)
            (project_path / ".git").mkdir()

            context = detect_project_context(str(project_path))

            assert context["is_git_repo"] is True

    def test_detect_project_context_nonexistent(self):
        """Test detecting non-existent path."""
        context = detect_project_context("/nonexistent/path")
        assert "error" in context

    def test_detect_project_context_current_dir(self):
        """Test detecting current directory."""
        context = detect_project_context()
        assert context["exists"] is True
        assert "path" in context


class TestGetGitHubRepoUrl:
    """Test getting GitHub repository URL."""

    def test_get_github_repo_url_from_config(self):
        """Test getting repo URL from config."""
        mock_config = MagicMock()
        mock_config.github.repo_url = "https://github.com/owner/repo"

        with patch("interfaces.cli.commands.load_cli_config", return_value=mock_config):
            url = get_github_repo_url()
            assert url == "https://github.com/owner/repo"

    def test_get_github_repo_url_from_git(self):
        """Test getting repo URL from git remote."""
        mock_config = MagicMock()
        mock_config.github.repo_url = None

        mock_result = MagicMock(
            returncode=0,
            stdout="https://github.com/owner/repo.git\n"
        )

        with patch("interfaces.cli.commands.load_cli_config", return_value=mock_config):
            with patch("subprocess.run", return_value=mock_result):
                url = get_github_repo_url()
                assert url == "https://github.com/owner/repo.git"

    def test_get_github_repo_url_none(self):
        """Test when no repo URL is available."""
        mock_config = MagicMock()
        mock_config.github.repo_url = None

        with patch("interfaces.cli.commands.load_cli_config", return_value=mock_config):
            with patch("subprocess.run", side_effect=FileNotFoundError):
                url = get_github_repo_url()
                assert url is None


class TestFormatIssuePreview:
    """Test issue preview formatting."""

    def test_format_issue_preview(self):
        """Test formatting issue preview."""
        nl_input = "Add user authentication feature"
        project_context = {
            "path": "/path/to/project",
            "type": "python",
            "is_git_repo": True,
        }

        preview = format_issue_preview(nl_input, project_context)

        assert "Add user authentication feature" in preview
        assert "/path/to/project" in preview
        assert "python" in preview


class TestPostGitHubIssue:
    """Test posting issues to GitHub."""

    def test_post_github_issue_success(self):
        """Test successfully posting an issue."""
        mock_result = MagicMock(
            returncode=0,
            stdout="https://github.com/owner/repo/issues/123"
        )

        with patch("subprocess.run", return_value=mock_result):
            success, url, number = post_github_issue(
                "Test Issue",
                "Test Body",
                "https://github.com/owner/repo"
            )

            assert success is True
            assert url == "https://github.com/owner/repo/issues/123"
            assert number == 123

    def test_post_github_issue_failure(self):
        """Test failed issue posting."""
        mock_result = MagicMock(returncode=1)

        with patch("subprocess.run", return_value=mock_result):
            success, url, number = post_github_issue("Title", "Body")

            assert success is False
            assert url is None
            assert number is None

    def test_post_github_issue_timeout(self):
        """Test issue posting timeout."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("gh", 30)):
            success, url, number = post_github_issue("Title", "Body")

            assert success is False


class TestHandleRequest:
    """Test the main request handler."""

    @patch("interfaces.cli.commands.check_dependencies")
    @patch("interfaces.cli.commands.detect_project_context")
    @patch("interfaces.cli.commands.get_github_repo_url")
    @patch("interfaces.cli.commands.post_github_issue")
    @patch("interfaces.cli.commands.get_history")
    @patch("interfaces.cli.commands.show_info")
    @patch("interfaces.cli.commands.show_success")
    def test_handle_request_success(
        self,
        mock_show_success,
        mock_show_info,
        mock_get_history,
        mock_post,
        mock_get_repo,
        mock_detect,
        mock_check_deps,
    ):
        """Test successful request handling."""
        # Setup mocks
        mock_check_deps.return_value = (True, [])
        mock_detect.return_value = {"path": "/test", "type": "python", "is_git_repo": True}
        mock_get_repo.return_value = "https://github.com/owner/repo"
        mock_post.return_value = (True, "https://github.com/owner/repo/issues/123", 123)

        mock_history = MagicMock()
        mock_get_history.return_value = mock_history

        # Execute
        result = handle_request("Add feature", auto_post=True)

        # Verify
        assert result is True
        mock_history.add_request.assert_called_once()
        call_args = mock_history.add_request.call_args
        assert call_args[1]["status"] == "success"

    @patch("interfaces.cli.commands.check_dependencies")
    @patch("interfaces.cli.commands.show_error")
    def test_handle_request_missing_dependencies(
        self,
        mock_show_error,
        mock_check_deps,
    ):
        """Test request handling with missing dependencies."""
        mock_check_deps.return_value = (False, ["GitHub CLI (gh)"])

        result = handle_request("Test request")

        assert result is False
        mock_show_error.assert_called_once()

    @patch("interfaces.cli.commands.check_dependencies")
    @patch("interfaces.cli.commands.detect_project_context")
    @patch("interfaces.cli.commands.show_error")
    def test_handle_request_invalid_project(
        self,
        mock_show_error,
        mock_detect,
        mock_check_deps,
    ):
        """Test request handling with invalid project path."""
        mock_check_deps.return_value = (True, [])
        mock_detect.return_value = {"error": "Path does not exist"}

        result = handle_request("Test", project_path="/invalid")

        assert result is False
        mock_show_error.assert_called_once()

    @patch("interfaces.cli.commands.check_dependencies")
    @patch("interfaces.cli.commands.detect_project_context")
    @patch("interfaces.cli.commands.get_github_repo_url")
    @patch("interfaces.cli.commands.show_warning")
    def test_handle_request_no_repo_url(
        self,
        mock_show_warning,
        mock_get_repo,
        mock_detect,
        mock_check_deps,
    ):
        """Test request handling without GitHub repo URL."""
        mock_check_deps.return_value = (True, [])
        mock_detect.return_value = {"path": "/test", "type": "python"}
        mock_get_repo.return_value = None

        result = handle_request("Test")

        assert result is False
        mock_show_warning.assert_called_once()

    @patch("interfaces.cli.commands.check_dependencies")
    @patch("interfaces.cli.commands.detect_project_context")
    @patch("interfaces.cli.commands.get_github_repo_url")
    @patch("interfaces.cli.commands.confirm_action")
    @patch("interfaces.cli.commands.show_info")
    @patch("interfaces.cli.commands.show_panel")
    @patch("interfaces.cli.commands.show_markdown")
    @patch("builtins.print")
    def test_handle_request_user_cancels(
        self,
        mock_print,
        mock_show_markdown,
        mock_show_panel,
        mock_show_info,
        mock_confirm,
        mock_get_repo,
        mock_detect,
        mock_check_deps,
    ):
        """Test request handling when user cancels."""
        mock_check_deps.return_value = (True, [])
        mock_detect.return_value = {"path": "/test", "type": "python"}
        mock_get_repo.return_value = "https://github.com/owner/repo"
        mock_confirm.return_value = False

        result = handle_request("Test", auto_post=False)

        assert result is False


class TestHandleNewProject:
    """Test new project creation handler."""

    @patch("interfaces.cli.commands.show_warning")
    def test_handle_new_project_stub(self, mock_show_warning):
        """Test that new project is stubbed."""
        result = handle_new_project("myproject")
        assert result is False
        mock_show_warning.assert_called_once()


class TestHandleIntegrate:
    """Test ADW integration handler."""

    @patch("interfaces.cli.commands.show_warning")
    def test_handle_integrate_stub(self, mock_show_warning):
        """Test that integration is stubbed."""
        result = handle_integrate("/path/to/project")
        assert result is False
        mock_show_warning.assert_called_once()
