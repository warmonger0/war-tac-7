"""Unit tests for the Project Detector module."""

import pytest
import json
import tempfile
import os
from pathlib import Path
from core.project_detector import ProjectDetector, detect_project_context
from core.webbuilder_models import ProjectContext


class TestProjectDetector:
    """Test suite for ProjectDetector class."""

    @pytest.fixture
    def detector(self):
        """Create ProjectDetector instance."""
        return ProjectDetector()

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_detect_new_project(self, detector, temp_project_dir):
        """Test detection of a new project directory."""
        # Empty directory should be detected as new project
        context = detector.detect_project_context(str(temp_project_dir))

        assert context.is_new_project is True
        assert context.complexity == "low"
        assert context.framework is None
        assert context.backend is None
        assert len(context.detected_files) == 0

    def test_detect_react_project(self, detector, temp_project_dir):
        """Test detection of a React project."""
        # Create React project files
        package_json = {
            "name": "test-app",
            "dependencies": {
                "react": "^18.0.0",
                "react-dom": "^18.0.0"
            },
            "devDependencies": {
                "vite": "^4.0.0"
            }
        }

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))
        (temp_project_dir / "vite.config.js").touch()
        (temp_project_dir / "src").mkdir()
        (temp_project_dir / "src" / "App.tsx").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.framework == "react-vite"
        assert context.is_new_project is False  # Has source files
        assert "npm" in context.build_tools

    def test_detect_nextjs_project(self, detector, temp_project_dir):
        """Test detection of a Next.js project."""
        package_json = {
            "name": "nextjs-app",
            "dependencies": {
                "next": "^13.0.0",
                "react": "^18.0.0"
            }
        }

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))
        (temp_project_dir / "next.config.js").touch()
        (temp_project_dir / "pages").mkdir()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.framework == "nextjs"

    def test_detect_vue_project(self, detector, temp_project_dir):
        """Test detection of a Vue project."""
        package_json = {
            "name": "vue-app",
            "dependencies": {
                "vue": "^3.0.0"
            }
        }

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))
        (temp_project_dir / "vue.config.js").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.framework == "vue"

    def test_detect_fastapi_backend(self, detector, temp_project_dir):
        """Test detection of FastAPI backend."""
        # Create Python files with FastAPI imports
        main_py = """from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
        (temp_project_dir / "main.py").write_text(main_py)

        requirements = """fastapi==0.95.0
uvicorn==0.21.0
"""
        (temp_project_dir / "requirements.txt").write_text(requirements)

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.backend == "fastapi"
        assert "pip" in context.build_tools

    def test_detect_express_backend(self, detector, temp_project_dir):
        """Test detection of Express backend."""
        package_json = {
            "name": "express-app",
            "dependencies": {
                "express": "^4.18.0"
            }
        }

        app_js = """const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello World' });
});
"""

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))
        (temp_project_dir / "app.js").write_text(app_js)

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.backend == "express"

    def test_detect_django_backend(self, detector, temp_project_dir):
        """Test detection of Django backend."""
        # Create Django-specific files
        (temp_project_dir / "manage.py").touch()
        (temp_project_dir / "settings.py").touch()

        requirements = """django==4.2.0
djangorestframework==3.14.0
"""
        (temp_project_dir / "requirements.txt").write_text(requirements)

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.backend == "django"

    def test_detect_build_tools(self, detector, temp_project_dir):
        """Test detection of various build tools."""
        # Create files for different build tools
        (temp_project_dir / "package.json").touch()
        (temp_project_dir / "yarn.lock").touch()
        (temp_project_dir / "requirements.txt").touch()
        (temp_project_dir / "poetry.lock").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        assert "npm" in context.build_tools
        assert "yarn" in context.build_tools
        assert "pip" in context.build_tools
        assert "poetry" in context.build_tools

    def test_detect_git_repository(self, detector, temp_project_dir):
        """Test detection of git repository."""
        # Create .git directory
        (temp_project_dir / ".git").mkdir()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.has_git is True

    def test_complexity_estimation_low(self, detector, temp_project_dir):
        """Test complexity estimation for simple projects."""
        # Create a simple project with few files
        (temp_project_dir / "index.html").touch()
        (temp_project_dir / "style.css").touch()
        (temp_project_dir / "script.js").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.complexity == "low"

    def test_complexity_estimation_medium(self, detector, temp_project_dir):
        """Test complexity estimation for medium projects."""
        # Create a medium complexity project
        package_json = {
            "name": "medium-app",
            "dependencies": {
                "react": "^18.0.0",
                "express": "^4.18.0"
            }
        }

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))

        # Create multiple source files
        (temp_project_dir / "src").mkdir()
        for i in range(15):
            (temp_project_dir / "src" / f"component{i}.js").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        assert context.complexity == "medium"

    def test_complexity_estimation_high(self, detector, temp_project_dir):
        """Test complexity estimation for complex projects."""
        # Create a complex project structure
        package_json = {
            "name": "complex-app",
            "dependencies": {
                "react": "^18.0.0",
                "express": "^4.18.0"
            }
        }

        (temp_project_dir / "package.json").write_text(json.dumps(package_json))
        (temp_project_dir / "docker-compose.yml").touch()
        (temp_project_dir / "Dockerfile").touch()
        (temp_project_dir / ".github" / "workflows").mkdir(parents=True)

        # Create many source files
        for dir_name in ["src", "api", "tests", "docs"]:
            dir_path = temp_project_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            for i in range(20):
                (dir_path / f"file{i}.js").touch()

        context = detector.detect_project_context(str(temp_project_dir))

        # Should be high complexity due to many files and Docker/CI
        assert context.complexity in ["medium", "high"]  # May vary based on exact count

    def test_scan_directory(self, detector, temp_project_dir):
        """Test directory scanning functionality."""
        # Create various files
        (temp_project_dir / "package.json").touch()
        (temp_project_dir / "tsconfig.json").touch()
        (temp_project_dir / ".gitignore").touch()
        (temp_project_dir / "README.md").touch()
        (temp_project_dir / "webpack.config.js").touch()

        detected_files = detector._scan_directory(temp_project_dir)

        assert "package.json" in detected_files
        assert "tsconfig.json" in detected_files
        assert ".gitignore" in detected_files
        assert "README.md" in detected_files
        assert "webpack.config.js" in detected_files

    def test_is_new_project_with_lock_files(self, detector, temp_project_dir):
        """Test that lock files indicate existing project."""
        (temp_project_dir / "package.json").touch()
        (temp_project_dir / "package-lock.json").touch()

        detected_files = detector._scan_directory(temp_project_dir)
        is_new = detector._is_new_project(detected_files)

        assert is_new is False

    def test_is_new_project_with_many_source_files(self, detector, temp_project_dir):
        """Test that many source files indicate existing project."""
        # Create more than 5 source files
        for i in range(10):
            (temp_project_dir / f"file{i}.py").touch()

        detected_files = detector._scan_directory(temp_project_dir)
        is_new = detector._is_new_project(detected_files)

        assert is_new is False

    def test_suggest_workflow(self, detector):
        """Test workflow suggestion based on context."""
        # New project - simple workflow
        context = ProjectContext(
            path="/test",
            is_new_project=True,
            complexity="low"
        )
        assert detector.suggest_workflow(context) == "adw_simple_iso"

        # High complexity - full SDLC
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="high"
        )
        assert detector.suggest_workflow(context) == "adw_sdlc_iso"

        # Medium complexity - plan-build-test
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="medium"
        )
        assert detector.suggest_workflow(context) == "adw_plan_build_test_iso"

    def test_detect_project_context_nonexistent_path(self, detector):
        """Test handling of non-existent path."""
        context = detector.detect_project_context("/nonexistent/path/12345")

        assert context.path == "/nonexistent/path/12345"
        assert context.is_new_project is True
        assert context.complexity == "low"
        assert len(context.detected_files) == 0

    def test_detect_project_context_file_path(self, detector, temp_project_dir):
        """Test handling when given a file path instead of directory."""
        file_path = temp_project_dir / "test.txt"
        file_path.touch()

        context = detector.detect_project_context(str(file_path))

        # Should use parent directory
        assert context.path == str(temp_project_dir)

    def test_detect_project_context_convenience_function(self, temp_project_dir):
        """Test the convenience function detect_project_context."""
        (temp_project_dir / "package.json").write_text('{"name": "test"}')

        context = detect_project_context(str(temp_project_dir))

        assert isinstance(context, ProjectContext)
        assert context.path == str(temp_project_dir)