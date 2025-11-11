"""Command handlers for CLI interface."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from interfaces.cli.output import (
    show_error,
    show_success,
    show_info,
    show_warning,
    show_panel,
    show_markdown,
    get_progress_spinner,
    confirm_action,
)
from interfaces.cli.history import get_history
from interfaces.cli.config_manager import load_cli_config


def check_dependencies() -> tuple[bool, list[str]]:
    """
    Check if required dependencies are available.

    Returns:
        Tuple of (all_ok, missing_dependencies)
    """
    missing = []

    # Check for gh CLI
    try:
        result = subprocess.run(
            ["gh", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            missing.append("GitHub CLI (gh)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        missing.append("GitHub CLI (gh)")

    # Check for ANTHROPIC_API_KEY (optional for now)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        # Don't add to missing - it's optional for now
        pass

    # Check for GitHub authentication
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            missing.append("GitHub CLI authentication (run: gh auth login)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Already caught above

    return (len(missing) == 0, missing)


def detect_project_context(project_path: Optional[str] = None) -> dict:
    """
    Detect project context from the given path or current directory.

    Args:
        project_path: Optional project path to analyze

    Returns:
        Dictionary with project context information
    """
    path = Path(project_path) if project_path else Path.cwd()

    if not path.exists():
        return {"error": f"Path does not exist: {path}"}

    if not path.is_dir():
        return {"error": f"Path is not a directory: {path}"}

    context = {
        "path": str(path.absolute()),
        "name": path.name,
        "exists": True,
    }

    # Check for common project markers
    has_package_json = (path / "package.json").exists()
    has_pyproject = (path / "pyproject.toml").exists()
    has_requirements = (path / "requirements.txt").exists()
    has_git = (path / ".git").exists()

    context["has_package_json"] = has_package_json
    context["has_pyproject"] = has_pyproject
    context["has_requirements"] = has_requirements
    context["is_git_repo"] = has_git

    # Detect project type
    if has_package_json:
        context["type"] = "node"
    elif has_pyproject or has_requirements:
        context["type"] = "python"
    else:
        context["type"] = "unknown"

    return context


def get_github_repo_url() -> Optional[str]:
    """
    Get GitHub repository URL from config or git remote.

    Returns:
        GitHub repository URL or None
    """
    # Try config first
    config = load_cli_config()
    if config.github.repo_url:
        return config.github.repo_url

    # Try to get from git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path.cwd(),
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return None


def format_issue_preview(nl_input: str, project_context: dict) -> str:
    """
    Format a preview of the issue that will be created.

    Args:
        nl_input: Natural language input
        project_context: Project context dictionary

    Returns:
        Formatted markdown preview
    """
    preview = f"""# Issue Preview

## User Request
{nl_input}

## Project Context
- **Path**: {project_context.get('path', 'N/A')}
- **Type**: {project_context.get('type', 'unknown')}
- **Git Repository**: {'Yes' if project_context.get('is_git_repo') else 'No'}

---

*Note: This is a preview. The actual issue will be generated with more details.*
"""
    return preview


def post_github_issue(title: str, body: str, repo_url: Optional[str] = None) -> tuple[bool, Optional[str], Optional[int]]:
    """
    Post an issue to GitHub using gh CLI.

    Args:
        title: Issue title
        body: Issue body
        repo_url: Optional repository URL

    Returns:
        Tuple of (success, issue_url, issue_number)
    """
    try:
        cmd = ["gh", "issue", "create", "--title", title, "--body", body]

        if repo_url:
            cmd.extend(["--repo", repo_url])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            issue_url = result.stdout.strip()
            # Extract issue number from URL
            issue_number = None
            if issue_url:
                parts = issue_url.split("/")
                if parts:
                    try:
                        issue_number = int(parts[-1])
                    except ValueError:
                        pass

            return (True, issue_url, issue_number)
        else:
            return (False, None, None)

    except subprocess.TimeoutExpired:
        return (False, None, None)
    except Exception:
        return (False, None, None)


def handle_request(
    nl_input: str,
    project_path: Optional[str] = None,
    auto_post: bool = False,
) -> bool:
    """
    Handle a natural language request.

    This is the main command handler that:
    1. Validates dependencies
    2. Detects project context
    3. Processes the NL request (stubbed for now)
    4. Shows preview
    5. Posts to GitHub
    6. Saves to history

    Args:
        nl_input: Natural language input from user
        project_path: Optional project path
        auto_post: Whether to skip confirmation

    Returns:
        True if successful, False otherwise
    """
    # Step 1: Check dependencies
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        show_error(
            f"Missing dependencies:\n" + "\n".join(f"  - {dep}" for dep in missing),
            title="Dependency Check Failed",
        )
        return False

    # Step 2: Detect project context
    show_info("Detecting project context...")
    project_context = detect_project_context(project_path)

    if "error" in project_context:
        show_error(project_context["error"])
        return False

    # Step 3: Get GitHub repo URL
    repo_url = get_github_repo_url()
    if not repo_url:
        show_warning(
            "No GitHub repository configured.\n"
            "Set with: webbuilder config set github.repo_url <url>\n"
            "Or ensure you're in a git repository with a remote.",
        )
        return False

    # Step 4: Process NL request (STUB - will integrate with NL processor later)
    show_info("Processing natural language request...")

    # For now, create a simple issue
    issue_title = f"Request: {nl_input[:60]}"
    issue_body = f"""# Natural Language Request

{nl_input}

## Project Information
- **Path**: {project_context['path']}
- **Type**: {project_context.get('type', 'unknown')}

---

*This issue was created by tac-webbuilder CLI*
"""

    # Step 5: Show preview
    if not auto_post:
        show_panel("Issue Preview", title="Generated Issue")
        show_markdown(f"**Title**: {issue_title}\n\n{issue_body}")
        print()

        if not confirm_action("Post this issue to GitHub?"):
            show_info("Request cancelled")
            return False

    # Step 6: Post to GitHub
    with get_progress_spinner("Posting to GitHub...") as progress:
        task = progress.add_task("Posting...", total=None)
        success, issue_url, issue_number = post_github_issue(
            title=issue_title,
            body=issue_body,
            repo_url=repo_url,
        )

    if not success:
        show_error("Failed to create GitHub issue")
        # Save to history as error
        history = get_history()
        history.add_request(
            nl_input=nl_input,
            project=project_context["path"],
            status="error",
            error="Failed to create GitHub issue",
        )
        return False

    # Step 7: Save to history
    history = get_history()
    history.add_request(
        nl_input=nl_input,
        issue_number=issue_number,
        issue_url=issue_url,
        project=project_context["path"],
        status="success",
    )

    # Step 8: Show success
    show_success(
        f"Issue created successfully!\n\n"
        f"Issue #{issue_number}: {issue_url}\n\n"
        f"Track progress with: webbuilder history"
    )

    return True


def handle_new_project(name: str, framework: str = "react-vite") -> bool:
    """
    Handle creating a new project (STUB for future implementation).

    Args:
        name: Project name
        framework: Framework to use

    Returns:
        True if successful, False otherwise
    """
    show_warning(
        "Project creation is not yet implemented.\n"
        "This feature will be available in a future release."
    )
    return False


def handle_integrate(path: str) -> bool:
    """
    Handle ADW integration into existing project (STUB for future implementation).

    Args:
        path: Project path

    Returns:
        True if successful, False otherwise
    """
    show_warning(
        "ADW integration is not yet implemented.\n"
        "This feature will be available in a future release."
    )
    return False
