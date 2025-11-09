"""Project Detector module for analyzing project context and structure."""

import os
import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from core.webbuilder_models import ProjectContext


class ProjectDetector:
    """Detects and analyzes project context for better issue generation."""

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        # Frontend frameworks
        "react-vite": {
            "files": ["vite.config.js", "vite.config.ts", "package.json"],
            "package_indicators": ["react", "vite"],
            "priority": 1
        },
        "react-cra": {
            "files": ["package.json", "src/App.js", "src/App.jsx", "src/App.tsx"],
            "package_indicators": ["react-scripts"],
            "priority": 2
        },
        "nextjs": {
            "files": ["next.config.js", "next.config.mjs", "pages", "app"],
            "package_indicators": ["next"],
            "priority": 1
        },
        "vue": {
            "files": ["vue.config.js", "vite.config.js"],
            "package_indicators": ["vue"],
            "priority": 2
        },
        "angular": {
            "files": ["angular.json", "angular.config.js"],
            "package_indicators": ["@angular/core"],
            "priority": 1
        },
        "svelte": {
            "files": ["svelte.config.js"],
            "package_indicators": ["svelte"],
            "priority": 2
        }
    }

    # Backend framework patterns
    BACKEND_PATTERNS = {
        "fastapi": {
            "files": ["main.py", "app.py", "server.py"],
            "package_indicators": ["fastapi", "uvicorn"],
            "content_indicators": ["from fastapi import", "FastAPI()"],
            "priority": 1
        },
        "express": {
            "files": ["app.js", "server.js", "index.js"],
            "package_indicators": ["express"],
            "content_indicators": ["require('express')", "require(\"express\")", "from 'express'"],
            "priority": 1
        },
        "django": {
            "files": ["manage.py", "settings.py", "wsgi.py"],
            "package_indicators": ["django"],
            "priority": 1
        },
        "flask": {
            "files": ["app.py", "application.py"],
            "package_indicators": ["flask"],
            "content_indicators": ["from flask import", "Flask(__name__)"],
            "priority": 2
        },
        "rails": {
            "files": ["Gemfile", "config.ru", "Rakefile"],
            "package_indicators": ["rails"],
            "priority": 1
        },
        "springboot": {
            "files": ["pom.xml", "build.gradle", "application.properties"],
            "content_indicators": ["spring.boot", "springframework"],
            "priority": 1
        }
    }

    # Build tool patterns
    BUILD_TOOLS = {
        "npm": ["package.json", "package-lock.json"],
        "yarn": ["yarn.lock"],
        "pnpm": ["pnpm-lock.yaml"],
        "bun": ["bun.lockb"],
        "pip": ["requirements.txt", "Pipfile"],
        "poetry": ["poetry.lock", "pyproject.toml"],
        "uv": ["uv.lock"],
        "cargo": ["Cargo.toml", "Cargo.lock"],
        "maven": ["pom.xml"],
        "gradle": ["build.gradle", "gradle.properties"]
    }

    def __init__(self):
        """Initialize the project detector."""
        self.detected_files_cache = {}

    def detect_project_context(self, path: str) -> ProjectContext:
        """
        Main function to detect project context.

        Args:
            path: Path to the project directory

        Returns:
            ProjectContext object with detected information
        """
        project_path = Path(path).resolve()

        # Check if path exists and is a directory
        if not project_path.exists():
            return self._create_empty_context(str(project_path))

        if not project_path.is_dir():
            project_path = project_path.parent

        # Scan directory for key files
        detected_files = self._scan_directory(project_path)

        # Determine if new or existing project
        is_new_project = self._is_new_project(detected_files)

        # Detect framework
        framework = self._detect_framework(project_path, detected_files)

        # Detect backend
        backend = self._detect_backend(project_path, detected_files)

        # Detect build tools
        build_tools = self._detect_build_tools(detected_files)

        # Check for git
        has_git = (project_path / ".git").exists()

        # Estimate complexity
        complexity = self._estimate_complexity(
            detected_files,
            framework,
            backend,
            is_new_project
        )

        return ProjectContext(
            path=str(project_path),
            is_new_project=is_new_project,
            framework=framework,
            backend=backend,
            complexity=complexity,
            build_tools=build_tools,
            has_git=has_git,
            detected_files=list(detected_files.keys())[:20]  # Limit to 20 files
        )

    def _scan_directory(self, path: Path) -> Dict[str, Path]:
        """
        Scan directory for relevant files.

        Args:
            path: Project directory path

        Returns:
            Dictionary of filename to path mappings
        """
        detected_files = {}

        # Common patterns to look for
        important_files = [
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "build.gradle",
            ".gitignore",
            "README.md",
            "Dockerfile",
            "docker-compose.yml",
            "Makefile"
        ]

        # Config files
        config_patterns = [
            "*.config.js",
            "*.config.ts",
            "*.config.json",
            "*.conf",
            "*.yml",
            "*.yaml"
        ]

        # Scan root directory first
        try:
            for item in path.iterdir():
                if item.is_file():
                    # Check if it's an important file
                    if item.name in important_files:
                        detected_files[item.name] = item
                    # Check config patterns
                    for pattern in config_patterns:
                        if item.match(pattern):
                            detected_files[item.name] = item

            # Check common subdirectories
            subdirs_to_check = ["src", "app", "lib", "server", "client", "pages", "components"]
            for subdir in subdirs_to_check:
                subdir_path = path / subdir
                if subdir_path.exists() and subdir_path.is_dir():
                    detected_files[subdir] = subdir_path
                    # Check for specific files in subdirectories
                    for item in subdir_path.iterdir():
                        if item.is_file() and item.suffix in [".py", ".js", ".ts", ".jsx", ".tsx"]:
                            # Store just a few examples
                            if len([k for k in detected_files.keys() if k.startswith(subdir + "/")]) < 3:
                                detected_files[f"{subdir}/{item.name}"] = item

        except PermissionError:
            # Handle permission errors gracefully
            pass

        return detected_files

    def _is_new_project(self, detected_files: Dict[str, Path]) -> bool:
        """
        Determine if this is a new project or existing codebase.

        Args:
            detected_files: Dictionary of detected files

        Returns:
            True if new project, False if existing
        """
        # Indicators of existing project
        existing_indicators = [
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "bun.lockb",
            "poetry.lock",
            "uv.lock",
            "Cargo.lock",
            "go.sum",
            ".git",
            "node_modules",
            "venv",
            ".venv",
            "dist",
            "build"
        ]

        # Check for lock files or build artifacts
        for indicator in existing_indicators:
            if indicator in detected_files:
                return False

        # Check for substantial source code
        source_files = [f for f in detected_files.keys() if any(
            f.endswith(ext) for ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs"]
        )]

        # If more than 5 source files, likely existing project
        if len(source_files) > 5:
            return False

        # Check if only has basic setup files
        setup_only_files = ["package.json", "pyproject.toml", "requirements.txt", ".gitignore", "README.md"]
        non_setup_files = [f for f in detected_files.keys() if f not in setup_only_files]

        # If only setup files or very few other files, likely new
        return len(non_setup_files) < 3

    def _detect_framework(self, path: Path, detected_files: Dict[str, Path]) -> Optional[str]:
        """
        Detect frontend framework.

        Args:
            path: Project path
            detected_files: Dictionary of detected files

        Returns:
            Detected framework name or None
        """
        # Check package.json if exists
        package_json_path = detected_files.get("package.json")
        package_data = {}

        if package_json_path:
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Get all dependencies
        all_deps = []
        if package_data:
            all_deps.extend(package_data.get("dependencies", {}).keys())
            all_deps.extend(package_data.get("devDependencies", {}).keys())

        # Check each framework pattern
        best_match = None
        best_priority = 999

        for framework, pattern in self.FRAMEWORK_PATTERNS.items():
            matches = 0

            # Check files
            for file in pattern["files"]:
                if file in detected_files:
                    matches += 2  # File presence is strong indicator

            # Check package indicators
            for indicator in pattern.get("package_indicators", []):
                if indicator in all_deps:
                    matches += 3  # Package dependency is very strong indicator

            # If we have matches and better priority, update best match
            if matches > 0 and pattern["priority"] < best_priority:
                best_match = framework
                best_priority = pattern["priority"]

        return best_match

    def _detect_backend(self, path: Path, detected_files: Dict[str, Path]) -> Optional[str]:
        """
        Detect backend framework.

        Args:
            path: Project path
            detected_files: Dictionary of detected files

        Returns:
            Detected backend framework or None
        """
        # Check package.json for Node.js backends
        package_json_path = detected_files.get("package.json")
        package_data = {}

        if package_json_path:
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Get all dependencies
        all_deps = []
        if package_data:
            all_deps.extend(package_data.get("dependencies", {}).keys())
            all_deps.extend(package_data.get("devDependencies", {}).keys())

        # Check Python requirements files
        python_deps = []
        if "requirements.txt" in detected_files:
            try:
                with open(detected_files["requirements.txt"], 'r') as f:
                    python_deps = [line.split('==')[0].strip() for line in f if line.strip() and not line.startswith('#')]
            except IOError:
                pass

        # Check pyproject.toml for Python dependencies
        if "pyproject.toml" in detected_files:
            try:
                with open(detected_files["pyproject.toml"], 'r') as f:
                    content = f.read()
                    # Simple parsing for dependencies
                    if "fastapi" in content.lower():
                        python_deps.append("fastapi")
                    if "django" in content.lower():
                        python_deps.append("django")
                    if "flask" in content.lower():
                        python_deps.append("flask")
            except IOError:
                pass

        # Check each backend pattern
        best_match = None
        best_priority = 999

        for backend, pattern in self.BACKEND_PATTERNS.items():
            matches = 0

            # Check files
            for file in pattern["files"]:
                if file in detected_files:
                    matches += 2

            # Check package indicators
            for indicator in pattern.get("package_indicators", []):
                if indicator in all_deps or indicator in python_deps:
                    matches += 3

            # Check file content indicators
            if "content_indicators" in pattern:
                for file_name, file_path in detected_files.items():
                    if file_path.is_file() and file_name.endswith(('.py', '.js', '.ts')):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read(1000)  # Read first 1000 chars
                                for indicator in pattern["content_indicators"]:
                                    if indicator in content:
                                        matches += 2
                                        break
                        except (IOError, UnicodeDecodeError):
                            pass

            # Update best match
            if matches > 0 and pattern["priority"] < best_priority:
                best_match = backend
                best_priority = pattern["priority"]

        return best_match

    def _detect_build_tools(self, detected_files: Dict[str, Path]) -> List[str]:
        """
        Detect build tools and package managers.

        Args:
            detected_files: Dictionary of detected files

        Returns:
            List of detected build tools
        """
        detected_tools = []

        for tool, indicators in self.BUILD_TOOLS.items():
            for indicator in indicators:
                if indicator in detected_files:
                    detected_tools.append(tool)
                    break

        return detected_tools

    def _estimate_complexity(
        self,
        detected_files: Dict[str, Path],
        framework: Optional[str],
        backend: Optional[str],
        is_new_project: bool
    ) -> str:
        """
        Estimate project complexity.

        Args:
            detected_files: Dictionary of detected files
            framework: Detected framework
            backend: Detected backend
            is_new_project: Whether this is a new project

        Returns:
            Complexity level: "low", "medium", or "high"
        """
        complexity_score = 0

        # New projects are simpler
        if is_new_project:
            return "low"

        # File count contributes to complexity
        file_count = len(detected_files)
        if file_count > 50:
            complexity_score += 3
        elif file_count > 20:
            complexity_score += 2
        elif file_count > 10:
            complexity_score += 1

        # Multiple technologies increase complexity
        if framework and backend:
            complexity_score += 2
        elif framework or backend:
            complexity_score += 1

        # Check for additional complexity indicators
        complexity_indicators = [
            "docker-compose.yml",
            "Dockerfile",
            "kubernetes",
            ".github/workflows",
            "terraform",
            "ansible"
        ]

        for indicator in complexity_indicators:
            if any(indicator in f for f in detected_files.keys()):
                complexity_score += 1

        # Determine complexity level
        if complexity_score >= 5:
            return "high"
        elif complexity_score >= 3:
            return "medium"
        else:
            return "low"

    def _create_empty_context(self, path: str) -> ProjectContext:
        """
        Create an empty project context for non-existent paths.

        Args:
            path: Project path

        Returns:
            Empty ProjectContext
        """
        return ProjectContext(
            path=path,
            is_new_project=True,
            framework=None,
            backend=None,
            complexity="low",
            build_tools=[],
            has_git=False,
            detected_files=[]
        )

    def suggest_workflow(self, context: ProjectContext) -> str:
        """
        Suggest ADW workflow based on project context.

        Args:
            context: ProjectContext object

        Returns:
            Suggested workflow name
        """
        if context.is_new_project:
            # New projects can start with simpler workflow
            return "adw_simple_iso"

        if context.complexity == "high":
            # Complex projects need full SDLC
            return "adw_sdlc_iso"

        if context.complexity == "medium":
            # Medium complexity uses plan-build-test
            return "adw_plan_build_test_iso"

        # Default to simple workflow
        return "adw_simple_iso"


def detect_project_context(path: str) -> ProjectContext:
    """
    Convenience function to detect project context.

    Args:
        path: Path to analyze

    Returns:
        ProjectContext object
    """
    detector = ProjectDetector()
    return detector.detect_project_context(path)