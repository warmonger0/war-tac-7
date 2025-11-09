"""GitHub Poster module for creating GitHub issues via gh CLI."""

import subprocess
import json
import re
from datetime import datetime
from typing import Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from core.webbuilder_models import (
    GitHubIssue,
    GitHubPostRequest,
    GitHubPostResponse,
    WebBuilderError
)


class GitHubPoster:
    """Handles posting issues to GitHub using gh CLI."""

    def __init__(self):
        """Initialize the GitHub poster."""
        self.console = Console()

    def post_issue(
        self,
        issue: GitHubIssue,
        confirm: bool = True,
        repository: Optional[str] = None,
        dry_run: bool = False
    ) -> int:
        """
        Post issue to GitHub via gh CLI.

        Args:
            issue: GitHubIssue to post
            confirm: Whether to show preview and confirm before posting
            repository: Optional repository in format owner/repo
            dry_run: If True, validate but don't actually post

        Returns:
            Issue number if successful, -1 if cancelled or failed
        """
        # Check if gh CLI is available
        if not self._check_gh_cli():
            self.console.print("[red]Error: GitHub CLI (gh) is not installed or not authenticated[/red]")
            return -1

        # Format the issue for display
        if confirm:
            preview = self.format_preview(issue)
            self.console.print(preview)

            if not dry_run:
                if not Confirm.ask("[cyan]Post this issue to GitHub?[/cyan]"):
                    self.console.print("[yellow]Issue posting cancelled[/yellow]")
                    return -1

        # If dry run, return here
        if dry_run:
            self.console.print("[green]Dry run successful - issue validated but not posted[/green]")
            return 0

        # Prepare gh command
        cmd = self._build_gh_command(issue, repository)

        try:
            # Execute gh command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            # Parse issue number from output
            issue_number = self._parse_issue_number(result.stdout)

            if issue_number:
                self.console.print(f"[green]✓ Issue #{issue_number} created successfully[/green]")

                # Get issue URL
                issue_url = self._get_issue_url(issue_number, repository)
                if issue_url:
                    self.console.print(f"[cyan]View at: {issue_url}[/cyan]")

                return issue_number
            else:
                self.console.print("[yellow]Issue created but could not parse issue number[/yellow]")
                return 0

        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error posting issue: {e.stderr}[/red]")
            return -1
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {str(e)}[/red]")
            return -1

    def format_preview(self, issue: GitHubIssue) -> Panel:
        """
        Format issue for terminal display preview.

        Args:
            issue: GitHubIssue to preview

        Returns:
            Rich Panel with formatted preview
        """
        # Build preview content
        content = f"""[bold cyan]Title:[/bold cyan] {issue.title}

[bold cyan]Type:[/bold cyan] {issue.classification}

[bold cyan]Labels:[/bold cyan] {', '.join(issue.labels)}

[bold cyan]Workflow:[/bold cyan] {issue.workflow} (model_set: {issue.model_set})

[bold cyan]Body Preview:[/bold cyan]
{issue.body[:500]}{'...' if len(issue.body) > 500 else ''}"""

        return Panel(
            content,
            title="[bold]GitHub Issue Preview[/bold]",
            border_style="cyan"
        )

    def _check_gh_cli(self) -> bool:
        """
        Check if gh CLI is installed and authenticated.

        Returns:
            True if gh CLI is available and authenticated
        """
        try:
            # Check if gh is installed
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                check=True
            )

            # Check if authenticated
            auth_result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True
            )

            return auth_result.returncode == 0

        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _build_gh_command(
        self,
        issue: GitHubIssue,
        repository: Optional[str] = None
    ) -> list:
        """
        Build the gh CLI command for creating an issue.

        Args:
            issue: GitHubIssue to post
            repository: Optional repository specification

        Returns:
            List of command arguments
        """
        cmd = ["gh", "issue", "create"]

        # Add title
        cmd.extend(["--title", issue.title])

        # Add body
        cmd.extend(["--body", issue.body])

        # Add labels
        if issue.labels:
            cmd.extend(["--label", ",".join(issue.labels)])

        # Add repository if specified
        if repository:
            cmd.extend(["--repo", repository])

        return cmd

    def _parse_issue_number(self, output: str) -> Optional[int]:
        """
        Parse issue number from gh CLI output.

        Args:
            output: Output from gh issue create command

        Returns:
            Issue number if found, None otherwise
        """
        # gh CLI typically outputs a URL like:
        # https://github.com/owner/repo/issues/123
        url_pattern = r'/issues/(\d+)'
        match = re.search(url_pattern, output)

        if match:
            return int(match.group(1))

        # Also try to find just a number (some versions might output differently)
        number_pattern = r'#(\d+)'
        match = re.search(number_pattern, output)

        if match:
            return int(match.group(1))

        return None

    def _get_issue_url(
        self,
        issue_number: int,
        repository: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the URL for a created issue.

        Args:
            issue_number: Issue number
            repository: Optional repository specification

        Returns:
            Issue URL if successful, None otherwise
        """
        try:
            cmd = ["gh", "issue", "view", str(issue_number), "--json", "url"]

            if repository:
                cmd.extend(["--repo", repository])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            data = json.loads(result.stdout)
            return data.get("url")

        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return None

    def validate_issue(self, issue: GitHubIssue) -> Tuple[bool, Optional[str]]:
        """
        Validate an issue before posting.

        Args:
            issue: GitHubIssue to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check title
        if not issue.title or len(issue.title) < 5:
            return False, "Issue title is too short (minimum 5 characters)"

        if len(issue.title) > 256:
            return False, "Issue title is too long (maximum 256 characters)"

        # Check body
        if not issue.body or len(issue.body) < 10:
            return False, "Issue body is too short (minimum 10 characters)"

        # Check labels
        if len(issue.labels) > 10:
            return False, "Too many labels (maximum 10)"

        # Check for invalid characters in labels
        for label in issue.labels:
            if not re.match(r'^[a-zA-Z0-9\-\s]+$', label):
                return False, f"Invalid label format: {label}"

        return True, None


def post_github_issue(request: GitHubPostRequest) -> GitHubPostResponse:
    """
    Post an issue to GitHub.

    Args:
        request: GitHubPostRequest with issue details

    Returns:
        GitHubPostResponse with result
    """
    poster = GitHubPoster()

    # Validate the issue first
    is_valid, error_message = poster.validate_issue(request.issue)

    if not is_valid:
        return GitHubPostResponse(
            success=False,
            error=error_message
        )

    try:
        # Post the issue
        issue_number = poster.post_issue(
            request.issue,
            confirm=False,  # No confirmation in API mode
            repository=request.repository,
            dry_run=request.dry_run
        )

        if issue_number > 0:
            # Get issue URL if possible
            issue_url = poster._get_issue_url(issue_number, request.repository)

            return GitHubPostResponse(
                success=True,
                issue_number=issue_number,
                issue_url=issue_url,
                posted_at=datetime.now()
            )
        elif issue_number == 0 and request.dry_run:
            return GitHubPostResponse(
                success=True,
                issue_number=None,
                issue_url=None,
                posted_at=None
            )
        else:
            return GitHubPostResponse(
                success=False,
                error="Failed to post issue or posting was cancelled"
            )

    except Exception as e:
        return GitHubPostResponse(
            success=False,
            error=str(e)
        )


def check_gh_cli_status() -> dict:
    """
    Check the status of gh CLI installation and authentication.

    Returns:
        Dictionary with status information
    """
    status = {
        "installed": False,
        "authenticated": False,
        "version": None,
        "user": None
    }

    try:
        # Check version
        version_result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        status["installed"] = True

        # Parse version
        version_match = re.search(r'gh version ([\d.]+)', version_result.stdout)
        if version_match:
            status["version"] = version_match.group(1)

        # Check auth status
        auth_result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )

        if auth_result.returncode == 0:
            status["authenticated"] = True

            # Try to get user info
            user_result = subprocess.run(
                ["gh", "api", "user", "--jq", ".login"],
                capture_output=True,
                text=True
            )
            if user_result.returncode == 0:
                status["user"] = user_result.stdout.strip()

    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    return status