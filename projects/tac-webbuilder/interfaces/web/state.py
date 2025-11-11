"""
Request state management for web API.

This module manages the lifecycle of user requests from submission through
preview to GitHub posting, maintaining in-memory state for pending requests.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from uuid import uuid4

from interfaces.web.models import (
    GitHubIssue,
    ProjectContext,
    RequestPreviewResponse,
)

logger = logging.getLogger(__name__)


class RequestState:
    """
    Manages in-memory state for pending user requests.

    Handles the preview-before-post workflow where users can:
    1. Submit NL input
    2. Preview the formatted GitHub issue
    3. Confirm and post to GitHub
    """

    def __init__(self):
        """Initialize request state manager."""
        self.pending_requests: dict[str, dict] = {}
        logger.info("RequestState initialized")

    def create_request(
        self,
        nl_input: str,
        project_path: Optional[str] = None,
    ) -> str:
        """
        Create a new request and generate preview.

        Args:
            nl_input: Natural language description
            project_path: Optional project path (uses current dir if not specified)

        Returns:
            request_id: Unique identifier for this request

        Raises:
            ValueError: If project_path is invalid
        """
        request_id = str(uuid4())

        # Resolve project path
        if project_path:
            resolved_path = Path(project_path).resolve()
            if not resolved_path.exists():
                raise ValueError(f"Project path does not exist: {project_path}")
        else:
            resolved_path = Path.cwd()

        # Detect project context
        project_context = self._detect_project_context(resolved_path)

        # Generate GitHub issue preview
        github_issue = self._generate_issue_preview(nl_input, project_context)

        # Store request
        self.pending_requests[request_id] = {
            "nl_input": nl_input,
            "project_path": str(resolved_path),
            "project_context": project_context,
            "github_issue": github_issue,
            "created_at": datetime.now(),
            "status": "pending",
        }

        logger.info(f"Created request {request_id} for project {resolved_path}")
        return request_id

    def get_request(self, request_id: str) -> Optional[dict]:
        """
        Retrieve a pending request.

        Args:
            request_id: Request identifier

        Returns:
            Request data or None if not found
        """
        return self.pending_requests.get(request_id)

    def get_preview(self, request_id: str) -> RequestPreviewResponse:
        """
        Get formatted preview for a request.

        Args:
            request_id: Request identifier

        Returns:
            RequestPreviewResponse with GitHub issue and context

        Raises:
            KeyError: If request_id not found
        """
        request = self.pending_requests.get(request_id)
        if not request:
            raise KeyError(f"Request not found: {request_id}")

        return RequestPreviewResponse(
            request_id=request_id,
            github_issue=request["github_issue"],
            project_context=request["project_context"],
            created_at=request["created_at"],
        )

    def confirm_and_post(self, request_id: str) -> tuple[int, str]:
        """
        Post request to GitHub and remove from pending.

        Args:
            request_id: Request identifier

        Returns:
            Tuple of (issue_number, github_url)

        Raises:
            KeyError: If request_id not found
            RuntimeError: If posting to GitHub fails
        """
        request = self.pending_requests.get(request_id)
        if not request:
            raise KeyError(f"Request not found: {request_id}")

        try:
            # Post to GitHub using gh CLI
            issue_number, github_url = self._post_to_github(
                request["github_issue"],
                request["project_context"]
            )

            # Mark as posted
            request["status"] = "posted"
            request["issue_number"] = issue_number
            request["github_url"] = github_url
            request["posted_at"] = datetime.now()

            # Remove from pending
            self.pending_requests.pop(request_id, None)

            logger.info(f"Posted request {request_id} as issue #{issue_number}")
            return issue_number, github_url

        except Exception as e:
            logger.error(f"Failed to post request {request_id}: {e}")
            request["status"] = "failed"
            request["error"] = str(e)
            raise RuntimeError(f"Failed to post to GitHub: {e}")

    def cleanup_old_requests(self, max_age_hours: int = 24):
        """
        Remove requests older than the specified age.

        Args:
            max_age_hours: Maximum age in hours (default 24)
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        old_requests = [
            req_id
            for req_id, req in self.pending_requests.items()
            if req["created_at"] < cutoff_time
        ]

        for req_id in old_requests:
            self.pending_requests.pop(req_id, None)
            logger.info(f"Cleaned up old request {req_id}")

        if old_requests:
            logger.info(f"Cleaned up {len(old_requests)} old requests")

    def _detect_project_context(self, project_path: Path) -> ProjectContext:
        """
        Detect project context and metadata.

        Args:
            project_path: Path to project directory

        Returns:
            ProjectContext with detected information
        """
        # Simple detection logic
        # TODO: Integrate with core/project_detector.py when available
        project_name = project_path.name
        framework = None
        language = None
        tech_stack = []
        build_tools = []
        test_frameworks = []
        has_git = (project_path / ".git").exists()
        repo_url = None

        # Detect based on files present
        if (project_path / "package.json").exists():
            tech_stack.append("Node.js")
            build_tools.append("npm")
            language = "JavaScript/TypeScript"

        if (project_path / "pyproject.toml").exists():
            tech_stack.append("Python")
            build_tools.append("uv")
            language = "Python"

        if (project_path / "requirements.txt").exists():
            tech_stack.append("Python")
            build_tools.append("pip")
            language = "Python"

        if (project_path / "Cargo.toml").exists():
            tech_stack.append("Rust")
            build_tools.append("cargo")
            language = "Rust"

        # Detect frameworks
        if (project_path / "vite.config.ts").exists():
            framework = "Vite"
        elif (project_path / "next.config.js").exists():
            framework = "Next.js"

        # Detect test frameworks
        if (project_path / "pytest.ini").exists() or (project_path / "pyproject.toml").exists():
            test_frameworks.append("pytest")

        if (project_path / "vitest.config.ts").exists():
            test_frameworks.append("vitest")

        # Get repo URL if Git repo
        if has_git:
            try:
                import subprocess
                result = subprocess.run(
                    ["git", "config", "--get", "remote.origin.url"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    repo_url = result.stdout.strip()
            except Exception as e:
                logger.warning(f"Failed to get repo URL: {e}")

        return ProjectContext(
            project_path=str(project_path),
            project_name=project_name,
            framework=framework,
            language=language,
            tech_stack=tech_stack,
            build_tools=build_tools,
            test_frameworks=test_frameworks,
            has_git=has_git,
            repo_url=repo_url,
        )

    def _generate_issue_preview(
        self,
        nl_input: str,
        project_context: ProjectContext,
    ) -> GitHubIssue:
        """
        Generate GitHub issue preview from natural language input.

        Args:
            nl_input: Natural language description
            project_context: Project context information

        Returns:
            GitHubIssue formatted for GitHub
        """
        # Simple formatting logic
        # TODO: Integrate with core/nl_processor.py and core/issue_formatter.py when available

        # Extract potential title (first line or first sentence)
        lines = nl_input.strip().split("\n")
        first_line = lines[0].strip()

        # Use first line as title if short, otherwise create a title
        if len(first_line) < 80 and len(lines) > 1:
            title = first_line
            description = "\n".join(lines[1:]).strip()
        else:
            # Extract first sentence as title
            sentences = nl_input.split(".")
            title = sentences[0].strip() if sentences else nl_input[:80]
            description = nl_input

        # Format body
        body_parts = [
            "## Description",
            description,
            "",
            "## Project Context",
            f"- **Project**: {project_context.project_name}",
        ]

        if project_context.framework:
            body_parts.append(f"- **Framework**: {project_context.framework}")

        if project_context.language:
            body_parts.append(f"- **Language**: {project_context.language}")

        if project_context.tech_stack:
            body_parts.append(f"- **Tech Stack**: {', '.join(project_context.tech_stack)}")

        body_parts.extend([
            "",
            "---",
            "",
            "_This issue was generated by tac-webbuilder_",
        ])

        body = "\n".join(body_parts)

        # Determine labels based on content
        labels = ["tac-webbuilder"]
        if "bug" in nl_input.lower() or "fix" in nl_input.lower():
            labels.append("bug")
        if "feature" in nl_input.lower() or "add" in nl_input.lower():
            labels.append("enhancement")
        if "test" in nl_input.lower():
            labels.append("testing")

        return GitHubIssue(
            title=title,
            body=body,
            labels=labels,
            assignees=[],
            milestone=None,
        )

    def _post_to_github(
        self,
        github_issue: GitHubIssue,
        project_context: ProjectContext,
    ) -> tuple[int, str]:
        """
        Post issue to GitHub using gh CLI.

        Args:
            github_issue: Formatted GitHub issue
            project_context: Project context

        Returns:
            Tuple of (issue_number, github_url)

        Raises:
            RuntimeError: If posting fails
        """
        import subprocess
        import json

        # TODO: Integrate with core/github_poster.py when available

        try:
            # Prepare gh CLI command
            cmd = [
                "gh", "issue", "create",
                "--title", github_issue.title,
                "--body", github_issue.body,
                "--json", "number,url",
            ]

            # Add labels
            for label in github_issue.labels:
                cmd.extend(["--label", label])

            # Execute in project directory
            result = subprocess.run(
                cmd,
                cwd=project_context.project_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                raise RuntimeError(f"gh CLI error: {result.stderr}")

            # Parse response
            response = json.loads(result.stdout)
            issue_number = response["number"]
            github_url = response["url"]

            return issue_number, github_url

        except subprocess.TimeoutExpired:
            raise RuntimeError("GitHub posting timed out")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse gh CLI response: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to post to GitHub: {e}")


# Global state instance
_request_state: Optional[RequestState] = None


def get_request_state() -> RequestState:
    """
    Get or create the global request state instance.

    Returns:
        RequestState singleton instance
    """
    global _request_state
    if _request_state is None:
        _request_state = RequestState()
    return _request_state
