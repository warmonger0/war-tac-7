import pytest
import subprocess
from unittest.mock import patch, MagicMock
from core.github_poster import GitHubPoster
from core.data_models import GitHubIssue


class TestGitHubPoster:

    @pytest.fixture
    def sample_issue(self):
        """Create a sample GitHub issue for testing."""
        return GitHubIssue(
            title="Add Dark Mode",
            body="## Description\nAdd dark mode to the application\n\n## Workflow\nadw_sdlc_iso model_set base",
            labels=["feature", "UI"],
            classification="feature",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

    @pytest.fixture
    def poster(self):
        """Create a GitHubPoster instance."""
        return GitHubPoster()

    def test_init_without_repo(self):
        """Test initializing without repo URL."""
        poster = GitHubPoster()
        assert poster.repo_url is None

    def test_init_with_repo(self):
        """Test initializing with repo URL."""
        poster = GitHubPoster(repo_url="owner/repo")
        assert poster.repo_url == "owner/repo"

    def test_format_preview(self, poster, sample_issue):
        """Test formatting issue preview."""
        preview = poster.format_preview(sample_issue)

        assert "Add Dark Mode" in preview
        assert "feature" in preview
        assert "UI" in preview
        assert "adw_sdlc_iso model_set base" in preview
        assert "## Description" in preview

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_post_issue_without_confirmation(self, mock_execute, mock_validate, poster, sample_issue):
        """Test posting issue without confirmation."""
        mock_validate.return_value = True
        mock_execute.return_value = "https://github.com/owner/repo/issues/42"

        result = poster.post_issue(sample_issue, confirm=False)

        assert result == 42
        mock_validate.assert_called_once()
        mock_execute.assert_called_once()

        # Verify command structure
        call_args = mock_execute.call_args[0][0]
        assert call_args[0] == "gh"
        assert call_args[1] == "issue"
        assert call_args[2] == "create"
        assert "--title" in call_args
        assert "Add Dark Mode" in call_args
        assert "--body" in call_args
        assert "--label" in call_args

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._show_preview')
    @patch('core.github_poster.input')
    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_post_issue_with_confirmation_yes(
        self, mock_execute, mock_input, mock_preview, mock_validate, poster, sample_issue
    ):
        """Test posting issue with user confirmation (yes)."""
        mock_validate.return_value = True
        mock_input.return_value = "y"
        mock_execute.return_value = "https://github.com/owner/repo/issues/123"

        result = poster.post_issue(sample_issue, confirm=True)

        assert result == 123
        mock_preview.assert_called_once_with(sample_issue)
        mock_input.assert_called_once()

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._show_preview')
    @patch('core.github_poster.input')
    def test_post_issue_with_confirmation_no(
        self, mock_input, mock_preview, mock_validate, poster, sample_issue
    ):
        """Test posting issue with user rejection."""
        mock_validate.return_value = True
        mock_input.return_value = "n"

        with pytest.raises(RuntimeError) as exc_info:
            poster.post_issue(sample_issue, confirm=True)

        assert "User cancelled" in str(exc_info.value)

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    def test_post_issue_gh_not_available(self, mock_validate, poster, sample_issue):
        """Test posting when gh CLI is not available."""
        mock_validate.return_value = False

        with pytest.raises(RuntimeError) as exc_info:
            poster.post_issue(sample_issue, confirm=False)

        assert "GitHub CLI (gh) is not installed" in str(exc_info.value)

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_post_issue_with_repo_url(self, mock_execute, mock_validate, sample_issue):
        """Test posting issue with specified repo URL."""
        poster = GitHubPoster(repo_url="owner/repo")
        mock_validate.return_value = True
        mock_execute.return_value = "https://github.com/owner/repo/issues/99"

        result = poster.post_issue(sample_issue, confirm=False)

        assert result == 99

        # Verify repo was included in command
        call_args = mock_execute.call_args[0][0]
        assert "--repo" in call_args
        assert "owner/repo" in call_args

    @patch('core.github_poster.subprocess.run')
    def test_validate_gh_cli_success(self, mock_run, poster):
        """Test successful gh CLI validation."""
        mock_run.return_value = MagicMock(returncode=0)

        result = poster._validate_gh_cli()

        assert result is True
        assert mock_run.call_count == 2  # version check + auth check

    @patch('core.github_poster.subprocess.run')
    def test_validate_gh_cli_not_installed(self, mock_run, poster):
        """Test validation when gh is not installed."""
        mock_run.side_effect = FileNotFoundError()

        result = poster._validate_gh_cli()

        assert result is False

    @patch('core.github_poster.subprocess.run')
    def test_validate_gh_cli_not_authenticated(self, mock_run, poster):
        """Test validation when gh is not authenticated."""
        # First call (version check) succeeds, second call (auth check) fails
        mock_run.side_effect = [
            MagicMock(returncode=0),
            subprocess.CalledProcessError(1, "gh auth status")
        ]

        result = poster._validate_gh_cli()

        assert result is False

    @patch('core.github_poster.subprocess.run')
    def test_execute_gh_command_success(self, mock_run, poster):
        """Test successful command execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Command output"
        )

        result = poster._execute_gh_command(["gh", "repo", "view"])

        assert result == "Command output"

    @patch('core.github_poster.subprocess.run')
    def test_execute_gh_command_failure(self, mock_run, poster):
        """Test command execution failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "gh", stderr="Error message"
        )

        with pytest.raises(RuntimeError) as exc_info:
            poster._execute_gh_command(["gh", "invalid", "command"])

        assert "GitHub CLI command failed" in str(exc_info.value)

    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_get_repo_info(self, mock_execute, poster):
        """Test getting repository information."""
        mock_execute.return_value = '{"name": "test-repo", "owner": {"login": "owner"}, "url": "https://github.com/owner/test-repo"}'

        result = poster.get_repo_info()

        assert result["name"] == "test-repo"
        assert result["owner"]["login"] == "owner"

    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_get_repo_info_with_url(self, mock_execute):
        """Test getting repo info with specified URL."""
        poster = GitHubPoster(repo_url="owner/repo")
        mock_execute.return_value = '{"name": "repo", "owner": {"login": "owner"}}'

        result = poster.get_repo_info()

        assert result["name"] == "repo"

        # Verify repo URL was passed in command
        call_args = mock_execute.call_args[0][0]
        assert "owner/repo" in call_args

    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_get_repo_info_failure(self, mock_execute, poster):
        """Test error handling when getting repo info fails."""
        mock_execute.side_effect = Exception("Command failed")

        with pytest.raises(RuntimeError) as exc_info:
            poster.get_repo_info()

        assert "Failed to get repository info" in str(exc_info.value)

    def test_post_issue_labels_formatting(self, sample_issue):
        """Test that labels are properly formatted in command."""
        poster = GitHubPoster()

        with patch.object(poster, '_validate_gh_cli', return_value=True):
            with patch.object(poster, '_execute_gh_command') as mock_execute:
                mock_execute.return_value = "https://github.com/owner/repo/issues/1"

                poster.post_issue(sample_issue, confirm=False)

                call_args = mock_execute.call_args[0][0]
                # Find the labels in the command
                label_idx = call_args.index("--label")
                labels = call_args[label_idx + 1]

                assert "feature" in labels
                assert "UI" in labels

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_post_issue_extracts_number_correctly(self, mock_execute, mock_validate, poster, sample_issue):
        """Test that issue number is correctly extracted from URL."""
        mock_validate.return_value = True

        # Test various URL formats
        test_cases = [
            ("https://github.com/owner/repo/issues/1", 1),
            ("https://github.com/owner/repo/issues/999", 999),
            ("https://github.com/owner/repo/issues/42\n", 42),
        ]

        for url, expected_number in test_cases:
            mock_execute.return_value = url
            result = poster.post_issue(sample_issue, confirm=False)
            assert result == expected_number
