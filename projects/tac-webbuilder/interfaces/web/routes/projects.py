"""
Project management routes.

Handles project listing, addition, and context retrieval for the web API.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from interfaces.web.models import (
    AddProjectModel,
    ProjectContext,
    ProjectListResponse,
    ProjectSummary,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["projects"])

# Simple in-memory project registry (could be moved to a JSON file)
_projects_cache: Optional[dict[str, ProjectContext]] = None
_projects_file = Path("projects.json")


def _load_projects() -> dict[str, ProjectContext]:
    """Load projects from file or return empty dict."""
    global _projects_cache

    if _projects_cache is not None:
        return _projects_cache

    if _projects_file.exists():
        try:
            with open(_projects_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                _projects_cache = {
                    proj_id: ProjectContext(**proj_data)
                    for proj_id, proj_data in data.items()
                }
                logger.info(f"Loaded {len(_projects_cache)} projects from file")
                return _projects_cache
        except Exception as e:
            logger.error(f"Failed to load projects file: {e}")

    _projects_cache = {}
    return _projects_cache


def _save_projects():
    """Save projects to file."""
    try:
        projects = _load_projects()
        data = {
            proj_id: proj.model_dump()
            for proj_id, proj in projects.items()
        }
        with open(_projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Saved {len(projects)} projects to file")
    except Exception as e:
        logger.error(f"Failed to save projects: {e}")


def _detect_project_context(project_path: Path) -> ProjectContext:
    """
    Detect project context (duplicated from state.py for now).

    TODO: Move to shared utility module.
    """
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


@router.get(
    "/projects",
    response_model=ProjectListResponse,
    summary="List projects",
    description="List all configured projects with their context information",
)
async def list_projects() -> ProjectListResponse:
    """
    List all configured projects.

    Returns:
        ProjectListResponse with list of projects

    Raises:
        HTTPException: If project listing fails
    """
    try:
        projects = _load_projects()

        summaries = [
            ProjectSummary(
                project_id=proj_id,
                project_name=proj.project_name,
                project_path=proj.project_path,
                framework=proj.framework,
                language=proj.language,
                last_used=None,  # TODO: Track last used time
            )
            for proj_id, proj in projects.items()
        ]

        logger.info(f"Listed {len(summaries)} projects")

        return ProjectListResponse(
            projects=summaries,
            total_count=len(summaries),
        )

    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list projects: {str(e)}",
        )


@router.post(
    "/projects",
    response_model=ProjectContext,
    status_code=status.HTTP_201_CREATED,
    summary="Add project",
    description="Add a new project and detect its context",
)
async def add_project(req: AddProjectModel) -> ProjectContext:
    """
    Add a new project and analyze its context.

    Args:
        req: Request with project path

    Returns:
        ProjectContext with detected information

    Raises:
        HTTPException: If project path is invalid or detection fails
    """
    try:
        project_path = Path(req.project_path).resolve()

        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {req.project_path}")

        if not project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {req.project_path}")

        # Detect project context
        context = _detect_project_context(project_path)

        # Generate project ID
        project_id = project_path.name.lower().replace(" ", "-")

        # Store in registry
        projects = _load_projects()
        projects[project_id] = context
        _save_projects()

        logger.info(f"Added project {project_id} at {project_path}")

        return context

    except ValueError as e:
        logger.error(f"Invalid project: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to add project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add project: {str(e)}",
        )


@router.get(
    "/projects/{project_id}/context",
    response_model=ProjectContext,
    summary="Get project context",
    description="Get detected context for a specific project",
)
async def get_project_context(project_id: str) -> ProjectContext:
    """
    Get cached project context.

    Args:
        project_id: Project identifier

    Returns:
        ProjectContext with detected information

    Raises:
        HTTPException: If project not found
    """
    try:
        projects = _load_projects()

        if project_id not in projects:
            logger.warning(f"Project not found: {project_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        context = projects[project_id]
        logger.info(f"Retrieved context for project {project_id}")

        return context

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get project context: {str(e)}",
        )
