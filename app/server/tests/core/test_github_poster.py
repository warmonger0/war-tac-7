"""Unit tests for the GitHub Poster module."""

import pytest
import json
import subprocess
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from core.github_poster import (
    GitHubPoster,
    post_github_issue,
    check_gh_cli_status
)
from core.webbuilder_models import (
    GitHubIssue,
    GitHubPostRequest,
    GitHubPostResponse
)


class TestGitHubPoster:
    """Test suite for GitHubPoster class."""

    @pytest.fixture
    def poster(self):
        """Create GitHubPoster instance."""
        return GitHubPoster()

    @pytest.fixture
    def sample_issue(self):
        """Create a sample GitHubIssue for testing."""
        return GitHubIssue(
            title="Test Issue",
            body="This is a test issue body",
            labels=["test", "automated"],
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

    @patch('subprocess.run')
    def test_check_gh_cli_installed(self, mock_run, poster):
        """Test checking if gh CLI is installed."""
        # Mock successful gh version check
        mock_run.return_value = Mock(
            returncode=0,
            stdout="gh version 2.32.0"
        )

        result = poster._check_gh_cli()

        assert result is True
        # Should call gh --version and gh auth status
        assert mock_run.call_count == 2

    @patch('subprocess.run')
    def test_check_gh_cli_not_installed(self, mock_run, poster):
        """Test checking when gh CLI is not installed."""
        mock_run.side_effect = FileNotFoundError()

        result = poster._check_gh_cli()

        assert result is False

    @patch('subprocess.run')
    def test_check_gh_cli_not_authenticated(self, mock_run, poster):
        """Test checking when gh CLI is not authenticated."""
        # Version check succeeds
        version_result = Mock(returncode=0, stdout="gh version 2.32.0")
        # Auth check fails
        auth_result = Mock(returncode=1)

        mock_run.side_effect = [version_result, auth_result]

        result = poster._check_gh_cli()

        assert result is False

    def test_build_gh_command(self, poster, sample_issue):
        """Test building gh CLI command."""
        cmd = poster._build_gh_command(sample_issue)

        assert cmd[0:3] == ["gh", "issue", "create"]
        assert "--title" in cmd
        assert "Test Issue" in cmd
        assert "--body" in cmd
        assert "This is a test issue body" in cmd
        assert "--label" in cmd
        assert "test,automated" in cmd

    def test_build_gh_command_with_repository(self, poster, sample_issue):
        """Test building gh CLI command with specific repository."""
        cmd = poster._build_gh_command(sample_issue, "owner/repo")

        assert "--repo" in cmd
        assert "owner/repo" in cmd

    def test_parse_issue_number_from_url(self, poster):
        """Test parsing issue number from GitHub URL."""
        output = "https://github.com/owner/repo/issues/123"
        issue_number = poster._parse_issue_number(output)

        assert issue_number == 123

    def test_parse_issue_number_from_hash(self, poster):
        """Test parsing issue number from hash format."""
        output = "Created issue #456"
        issue_number = poster._parse_issue_number(output)

        assert issue_number == 456

    def test_parse_issue_number_not_found(self, poster):
        """Test parsing when issue number is not found."""
        output = "Some other output without issue number"
        issue_number = poster._parse_issue_number(output)

        assert issue_number is None

    @patch('subprocess.run')
    def test_get_issue_url(self, mock_run, poster):
        """Test getting issue URL after creation."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"url": "https://github.com/owner/repo/issues/789"}'
        )

        url = poster._get_issue_url(789)

        assert url == "https://github.com/owner/repo/issues/789"
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "gh" in cmd
        assert "issue" in cmd
        assert "view" in cmd
        assert "789" in cmd

    @patch('subprocess.run')
    def test_get_issue_url_with_repository(self, mock_run, poster):
        """Test getting issue URL with specific repository."""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='{"url": "https://github.com/owner/repo/issues/100"}'
        )

        url = poster._get_issue_url(100, "owner/repo")

        cmd = mock_run.call_args[0][0]
        assert "--repo" in cmd
        assert "owner/repo" in cmd

    def test_validate_issue_valid(self, poster, sample_issue):
        """Test validating a valid issue."""
        is_valid, error = poster.validate_issue(sample_issue)

        assert is_valid is True
        assert error is None

    def test_validate_issue_short_title(self, poster):
        """Test validating issue with too short title."""
        issue = GitHubIssue(
            title="Hi",
            body="This is a longer body content",
            labels=[],
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

        is_valid, error = poster.validate_issue(issue)

        assert is_valid is False
        assert "title is too short" in error

    def test_validate_issue_long_title(self, poster):
        """Test validating issue with too long title."""
        issue = GitHubIssue(
            title="x" * 300,  # Too long
            body="Body content",
            labels=[],
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

        is_valid, error = poster.validate_issue(issue)

        assert is_valid is False
        assert "title is too long" in error

    def test_validate_issue_short_body(self, poster):
        """Test validating issue with too short body."""
        issue = GitHubIssue(
            title="Valid Title",
            body="Short",
            labels=[],
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

        is_valid, error = poster.validate_issue(issue)

        assert is_valid is False
        assert "body is too short" in error

    def test_validate_issue_too_many_labels(self, poster):
        """Test validating issue with too many labels."""
        issue = GitHubIssue(
            title="Valid Title",
            body="Valid body content that is long enough",
            labels=[f"label{i}" for i in range(15)],  # Too many
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

        is_valid, error = poster.validate_issue(issue)

        assert is_valid is False
        assert "Too many labels" in error

    def test_validate_issue_invalid_label_format(self, poster):
        """Test validating issue with invalid label format."""
        issue = GitHubIssue(
            title="Valid Title",
            body="Valid body content",
            labels=["valid-label", "invalid@label!"],
            classification="feature",
            workflow="adw_simple_iso",
            model_set="base"
        )

        is_valid, error = poster.validate_issue(issue)

        assert is_valid is False
        assert "Invalid label format" in error

    @patch('core.github_poster.GitHubPoster._check_gh_cli')
    @patch('core.github_poster.Confirm.ask')
    @patch('subprocess.run')
    def test_post_issue_success(self, mock_run, mock_confirm, mock_check_cli, poster, sample_issue):
        """Test successful issue posting."""
        mock_check_cli.return_value = True
        mock_confirm.return_value = True
        mock_run.return_value = Mock(
            returncode=0,
            stdout="https://github.com/owner/repo/issues/42"
        )

        issue_number = poster.post_issue(sample_issue, confirm=True)

        assert issue_number == 42
        mock_run.assert_called_once()

    @patch('core.github_poster.GitHubPoster._check_gh_cli')
    @patch('core.github_poster.Confirm.ask')
    def test_post_issue_cancelled(self, mock_confirm, mock_check_cli, poster, sample_issue):
        """Test cancelled issue posting."""
        mock_check_cli.return_value = True
        mock_confirm.return_value = False

        issue_number = poster.post_issue(sample_issue, confirm=True)

        assert issue_number == -1

    @patch('core.github_poster.GitHubPoster._check_gh_cli')
    def test_post_issue_no_cli(self, mock_check_cli, poster, sample_issue):
        """Test posting when gh CLI is not available."""
        mock_check_cli.return_value = False

        issue_number = poster.post_issue(sample_issue, confirm=False)

        assert issue_number == -1

    @patch('core.github_poster.GitHubPoster._check_gh_cli')
    @patch('subprocess.run')
    def test_post_issue_dry_run(self, mock_run, mock_check_cli, poster, sample_issue):
        """Test dry run mode."""
        mock_check_cli.return_value = True

        issue_number = poster.post_issue(sample_issue, confirm=False, dry_run=True)

        assert issue_number == 0
        mock_run.assert_not_called()  # Should not actually run command

    def test_post_github_issue_function_invalid(self):
        """Test post_github_issue function with invalid issue."""
        request = GitHubPostRequest(
            issue=GitHubIssue(
                title="",  # Invalid - empty title
                body="Body",
                labels=[],
                classification="feature",
                workflow="adw_simple_iso",
                model_set="base"
            )
        )

        response = post_github_issue(request)

        assert response.success is False
        assert "too short" in response.error

    @patch('core.github_poster.GitHubPoster.post_issue')
    @patch('core.github_poster.GitHubPoster._get_issue_url')
    def test_post_github_issue_function_success(self, mock_get_url, mock_post):
        """Test successful post_github_issue function."""
        mock_post.return_value = 123
        mock_get_url.return_value = "https://github.com/owner/repo/issues/123"

        request = GitHubPostRequest(
            issue=GitHubIssue(
                title="Valid Title",
                body="Valid body content for testing",
                labels=["test"],
                classification="feature",
                workflow="adw_simple_iso",
                model_set="base"
            )
        )

        response = post_github_issue(request)

        assert response.success is True
        assert response.issue_number == 123
        assert response.issue_url == "https://github.com/owner/repo/issues/123"
        assert response.posted_at is not None

    @patch('subprocess.run')
    def test_check_gh_cli_status(self, mock_run):
        """Test check_gh_cli_status function."""
        # Mock successful responses
        version_result = Mock(
            returncode=0,
            stdout="gh version 2.32.0 (2023-07-24)"
        )
        auth_result = Mock(returncode=0)
        user_result = Mock(
            returncode=0,
            stdout="testuser\n"
        )

        mock_run.side_effect = [version_result, auth_result, user_result]

        status = check_gh_cli_status()

        assert status["installed"] is True
        assert status["authenticated"] is True
        assert status["version"] == "2.32.0"
        assert status["user"] == "testuser"

    @patch('subprocess.run')
    def test_check_gh_cli_status_not_installed(self, mock_run):
        """Test check_gh_cli_status when gh is not installed."""
        mock_run.side_effect = FileNotFoundError()

        status = check_gh_cli_status()

        assert status["installed"] is False
        assert status["authenticated"] is False
        assert status["version"] is None
        assert status["user"] is None

    @patch('subprocess.run')
    def test_check_gh_cli_status_not_authenticated(self, mock_run):
        """Test check_gh_cli_status when not authenticated."""
        version_result = Mock(
            returncode=0,
            stdout="gh version 2.32.0"
        )
        auth_result = Mock(returncode=1)  # Not authenticated

        mock_run.side_effect = [version_result, auth_result]

        status = check_gh_cli_status()

        assert status["installed"] is True
        assert status["authenticated"] is False
        assert status["version"] == "2.32.0"
        assert status["user"] is None

    def test_format_preview(self, poster, sample_issue):
        """Test formatting issue preview for terminal."""
        preview = poster.format_preview(sample_issue)

        # Should return a Rich Panel object
        from rich.panel import Panel
        assert isinstance(preview, Panel)