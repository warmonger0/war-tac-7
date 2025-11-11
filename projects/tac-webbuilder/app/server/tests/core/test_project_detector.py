import pytest
import json
from core.project_detector import (
    detect_project_context,
    is_directory_empty,
    detect_framework,
    detect_backend,
    detect_build_tools,
    detect_package_manager,
    check_git_initialized,
    calculate_complexity_from_structure,
    suggest_workflow,
    calculate_complexity
)
from core.data_models import ProjectContext


class TestProjectDetector:

    @pytest.fixture
    def tmp_project_dir(self, tmp_path):
        """Create a temporary project directory."""
        return tmp_path / "test_project"

    def test_is_directory_empty_true(self, tmp_path):
        """Test detecting an empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = is_directory_empty(empty_dir)
        assert result is True

    def test_is_directory_empty_with_hidden_files(self, tmp_path):
        """Test directory with only hidden files is considered empty."""
        dir_with_hidden = tmp_path / "hidden"
        dir_with_hidden.mkdir()
        (dir_with_hidden / ".gitignore").touch()

        result = is_directory_empty(dir_with_hidden)
        assert result is True

    def test_is_directory_empty_false(self, tmp_path):
        """Test detecting a non-empty directory."""
        non_empty = tmp_path / "non_empty"
        non_empty.mkdir()
        (non_empty / "file.txt").touch()

        result = is_directory_empty(non_empty)
        assert result is False

    def test_detect_framework_react_vite(self, tmp_path):
        """Test detecting React with Vite."""
        project_dir = tmp_path / "react_project"
        project_dir.mkdir()

        # Create vite config
        (project_dir / "vite.config.ts").touch()

        # Create package.json with React
        package_json = {
            "dependencies": {
                "react": "^18.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_framework(project_dir)
        assert result == "react-vite"

    def test_detect_framework_nextjs(self, tmp_path):
        """Test detecting Next.js."""
        project_dir = tmp_path / "next_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_framework(project_dir)
        assert result == "nextjs"

    def test_detect_framework_vue_vite(self, tmp_path):
        """Test detecting Vue with Vite."""
        project_dir = tmp_path / "vue_project"
        project_dir.mkdir()

        (project_dir / "vite.config.js").touch()

        package_json = {
            "dependencies": {
                "vue": "^3.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_framework(project_dir)
        assert result == "vue-vite"

    def test_detect_framework_none(self, tmp_path):
        """Test when no framework is detected."""
        project_dir = tmp_path / "no_framework"
        project_dir.mkdir()

        result = detect_framework(project_dir)
        assert result is None

    def test_detect_backend_fastapi(self, tmp_path):
        """Test detecting FastAPI."""
        project_dir = tmp_path / "fastapi_project"
        project_dir.mkdir()

        pyproject_content = """
[project]
dependencies = [
    "fastapi==0.100.0"
]
"""
        (project_dir / "pyproject.toml").write_text(pyproject_content)

        result = detect_backend(project_dir)
        assert result == "fastapi"

    def test_detect_backend_express(self, tmp_path):
        """Test detecting Express."""
        project_dir = tmp_path / "express_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "express": "^4.18.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_backend(project_dir)
        assert result == "express"

    def test_detect_backend_none(self, tmp_path):
        """Test when no backend is detected."""
        project_dir = tmp_path / "no_backend"
        project_dir.mkdir()

        result = detect_backend(project_dir)
        assert result is None

    def test_detect_build_tools_multiple(self, tmp_path):
        """Test detecting multiple build tools."""
        project_dir = tmp_path / "build_tools"
        project_dir.mkdir()

        (project_dir / "vite.config.ts").touch()
        (project_dir / "tsconfig.json").touch()
        (project_dir / "Dockerfile").touch()

        result = detect_build_tools(project_dir)

        assert "vite" in result
        assert "typescript" in result
        assert "docker" in result

    def test_detect_build_tools_none(self, tmp_path):
        """Test when no build tools are detected."""
        project_dir = tmp_path / "no_tools"
        project_dir.mkdir()

        result = detect_build_tools(project_dir)
        assert result == []

    def test_detect_package_manager_bun(self, tmp_path):
        """Test detecting Bun."""
        project_dir = tmp_path / "bun_project"
        project_dir.mkdir()

        (project_dir / "bun.lockb").touch()

        result = detect_package_manager(project_dir)
        assert result == "bun"

    def test_detect_package_manager_npm(self, tmp_path):
        """Test detecting npm."""
        project_dir = tmp_path / "npm_project"
        project_dir.mkdir()

        (project_dir / "package-lock.json").touch()

        result = detect_package_manager(project_dir)
        assert result == "npm"

    def test_detect_package_manager_uv(self, tmp_path):
        """Test detecting uv."""
        project_dir = tmp_path / "uv_project"
        project_dir.mkdir()

        (project_dir / "uv.lock").touch()

        result = detect_package_manager(project_dir)
        assert result == "uv"

    def test_detect_package_manager_default_npm(self, tmp_path):
        """Test default to npm when package.json exists."""
        project_dir = tmp_path / "default_npm"
        project_dir.mkdir()

        (project_dir / "package.json").touch()

        result = detect_package_manager(project_dir)
        assert result == "npm"

    def test_detect_package_manager_none(self, tmp_path):
        """Test when no package manager is detected."""
        project_dir = tmp_path / "no_pm"
        project_dir.mkdir()

        result = detect_package_manager(project_dir)
        assert result is None

    def test_check_git_initialized_true(self, tmp_path):
        """Test detecting git initialization."""
        project_dir = tmp_path / "git_project"
        project_dir.mkdir()

        git_dir = project_dir / ".git"
        git_dir.mkdir()

        result = check_git_initialized(project_dir)
        assert result is True

    def test_check_git_initialized_false(self, tmp_path):
        """Test when git is not initialized."""
        project_dir = tmp_path / "no_git"
        project_dir.mkdir()

        result = check_git_initialized(project_dir)
        assert result is False

    def test_calculate_complexity_low(self, tmp_path):
        """Test calculating low complexity."""
        project_dir = tmp_path / "low_complexity"
        project_dir.mkdir()

        # Create a few files
        (project_dir / "index.js").touch()
        (project_dir / "style.css").touch()

        complexity = calculate_complexity_from_structure(
            project_dir,
            framework=None,
            backend=None,
            build_tools=[]
        )

        assert complexity == "low"

    def test_calculate_complexity_medium(self, tmp_path):
        """Test calculating medium complexity."""
        project_dir = tmp_path / "medium_complexity"
        project_dir.mkdir()

        # Create multiple files
        src_dir = project_dir / "src"
        src_dir.mkdir()
        for i in range(60):
            (src_dir / f"file{i}.js").touch()

        complexity = calculate_complexity_from_structure(
            project_dir,
            framework="react",
            backend="express",  # Add backend to increase complexity
            build_tools=["vite", "typescript"]  # Multiple build tools
        )

        assert complexity == "medium"

    def test_calculate_complexity_high(self, tmp_path):
        """Test calculating high complexity."""
        project_dir = tmp_path / "high_complexity"
        project_dir.mkdir()

        # Create many files
        src_dir = project_dir / "src"
        src_dir.mkdir()
        for i in range(120):
            (src_dir / f"file{i}.js").touch()

        # Add monorepo structure
        packages_dir = project_dir / "packages"
        packages_dir.mkdir()

        complexity = calculate_complexity_from_structure(
            project_dir,
            framework="nextjs",
            backend="fastapi",
            build_tools=["vite", "typescript", "docker"]
        )

        assert complexity == "high"

    def test_suggest_workflow_low(self):
        """Test workflow suggestion for low complexity."""
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="low"
        )

        result = suggest_workflow(context)
        assert result == "adw_sdlc_iso"

    def test_suggest_workflow_medium(self):
        """Test workflow suggestion for medium complexity."""
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="medium"
        )

        result = suggest_workflow(context)
        assert result == "adw_plan_build_test_iso"

    def test_suggest_workflow_high(self):
        """Test workflow suggestion for high complexity."""
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="high"
        )

        result = suggest_workflow(context)
        assert result == "adw_plan_build_test_iso"

    def test_calculate_complexity_wrapper(self):
        """Test the complexity calculation wrapper."""
        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="medium"
        )

        result = calculate_complexity(context)
        assert result == "medium"

    def test_detect_project_context_new_project(self, tmp_path):
        """Test detecting context for a new project."""
        project_dir = tmp_path / "new_project"
        project_dir.mkdir()

        context = detect_project_context(str(project_dir))

        assert context.is_new_project is True
        assert context.complexity == "low"
        assert context.framework is None
        assert context.backend is None

    def test_detect_project_context_react_project(self, tmp_path):
        """Test detecting context for a React project."""
        project_dir = tmp_path / "react_app"
        project_dir.mkdir()

        # Setup React project
        (project_dir / "vite.config.ts").touch()
        package_json = {
            "dependencies": {
                "react": "^18.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))
        (project_dir / "package-lock.json").touch()

        # Add git
        (project_dir / ".git").mkdir()

        # Add some files
        src_dir = project_dir / "src"
        src_dir.mkdir()
        for i in range(10):
            (src_dir / f"component{i}.tsx").touch()

        context = detect_project_context(str(project_dir))

        assert context.is_new_project is False
        assert context.framework == "react-vite"
        assert context.package_manager == "npm"
        assert context.has_git is True
        assert "vite" in context.build_tools

    def test_detect_project_context_nonexistent_path(self):
        """Test error when path doesn't exist."""
        with pytest.raises(ValueError) as exc_info:
            detect_project_context("/nonexistent/path")

        assert "Project path does not exist" in str(exc_info.value)

    def test_detect_framework_vite_only(self, tmp_path):
        """Test detecting Vite without specific framework."""
        project_dir = tmp_path / "vite_only"
        project_dir.mkdir()

        (project_dir / "vite.config.js").touch()

        result = detect_framework(project_dir)
        assert result == "vite"

    def test_detect_framework_angular(self, tmp_path):
        """Test detecting Angular."""
        project_dir = tmp_path / "angular_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "@angular/core": "^17.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_framework(project_dir)
        assert result == "angular"

    def test_detect_framework_svelte(self, tmp_path):
        """Test detecting Svelte."""
        project_dir = tmp_path / "svelte_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "svelte": "^4.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_framework(project_dir)
        assert result == "svelte"

    def test_detect_framework_pyproject_exists(self, tmp_path):
        """Test that pyproject.toml returns None for frontend framework."""
        project_dir = tmp_path / "python_project"
        project_dir.mkdir()

        (project_dir / "pyproject.toml").touch()

        result = detect_framework(project_dir)
        assert result is None

    def test_detect_backend_django_pyproject(self, tmp_path):
        """Test detecting Django from pyproject.toml."""
        project_dir = tmp_path / "django_project"
        project_dir.mkdir()

        pyproject_content = """
[project]
dependencies = [
    "Django==5.0.0"
]
"""
        (project_dir / "pyproject.toml").write_text(pyproject_content)

        result = detect_backend(project_dir)
        assert result == "django"

    def test_detect_backend_flask_pyproject(self, tmp_path):
        """Test detecting Flask from pyproject.toml."""
        project_dir = tmp_path / "flask_project"
        project_dir.mkdir()

        pyproject_content = """
[project]
dependencies = [
    "Flask==3.0.0"
]
"""
        (project_dir / "pyproject.toml").write_text(pyproject_content)

        result = detect_backend(project_dir)
        assert result == "flask"

    def test_detect_backend_django_requirements(self, tmp_path):
        """Test detecting Django from requirements.txt."""
        project_dir = tmp_path / "django_req_project"
        project_dir.mkdir()

        (project_dir / "requirements.txt").write_text("Django==5.0.0\n")

        result = detect_backend(project_dir)
        assert result == "django"

    def test_detect_backend_flask_requirements(self, tmp_path):
        """Test detecting Flask from requirements.txt."""
        project_dir = tmp_path / "flask_req_project"
        project_dir.mkdir()

        (project_dir / "requirements.txt").write_text("Flask==3.0.0\n")

        result = detect_backend(project_dir)
        assert result == "flask"

    def test_detect_backend_fastapi_requirements(self, tmp_path):
        """Test detecting FastAPI from requirements.txt."""
        project_dir = tmp_path / "fastapi_req_project"
        project_dir.mkdir()

        (project_dir / "requirements.txt").write_text("fastapi==0.100.0\n")

        result = detect_backend(project_dir)
        assert result == "fastapi"

    def test_detect_backend_fastify(self, tmp_path):
        """Test detecting Fastify."""
        project_dir = tmp_path / "fastify_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "fastify": "^4.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_backend(project_dir)
        assert result == "fastify"

    def test_detect_backend_nestjs(self, tmp_path):
        """Test detecting NestJS."""
        project_dir = tmp_path / "nestjs_project"
        project_dir.mkdir()

        package_json = {
            "dependencies": {
                "@nestjs/core": "^10.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))

        result = detect_backend(project_dir)
        assert result == "nestjs"
