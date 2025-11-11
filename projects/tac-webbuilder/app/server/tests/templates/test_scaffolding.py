"""Tests for template scaffolding and project creation."""

import json
import os
from pathlib import Path

import pytest


@pytest.fixture
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent.parent


@pytest.fixture
def templates_dir(project_root):
    """Get the templates directory."""
    return project_root / "templates"


@pytest.fixture
def template_structure_file(templates_dir):
    """Get the template structure JSON file."""
    return templates_dir / "template_structure.json"


class TestTemplateStructure:
    """Tests for template_structure.json file."""

    def test_template_structure_exists(self, template_structure_file):
        """Test that template_structure.json exists."""
        assert template_structure_file.exists(), "template_structure.json should exist"

    def test_template_structure_valid_json(self, template_structure_file):
        """Test that template_structure.json is valid JSON."""
        with open(template_structure_file) as f:
            data = json.load(f)
        assert isinstance(data, dict), "Template structure should be a dictionary"

    def test_template_structure_has_required_templates(self, template_structure_file):
        """Test that all required templates are defined."""
        with open(template_structure_file) as f:
            data = json.load(f)

        required_templates = ["react-vite", "nextjs", "vanilla"]
        for template in required_templates:
            assert template in data, f"Template '{template}' should be defined"

    def test_template_structure_has_required_fields(self, template_structure_file):
        """Test that each template has required fields."""
        with open(template_structure_file) as f:
            data = json.load(f)

        required_fields = ["files", "directories", "scripts", "ports", "description"]

        for template_name, template_data in data.items():
            for field in required_fields:
                assert field in template_data, (
                    f"Template '{template_name}' should have field '{field}'"
                )
            assert isinstance(template_data["files"], list)
            assert isinstance(template_data["directories"], list)
            assert isinstance(template_data["scripts"], dict)
            assert isinstance(template_data["ports"], dict)
            assert isinstance(template_data["description"], str)


class TestReactViteTemplate:
    """Tests for React + Vite template."""

    @pytest.fixture
    def react_vite_dir(self, templates_dir):
        return templates_dir / "new_webapp" / "react-vite"

    def test_react_vite_template_exists(self, react_vite_dir):
        """Test that React + Vite template directory exists."""
        assert react_vite_dir.exists(), "React + Vite template should exist"

    def test_react_vite_has_package_json(self, react_vite_dir):
        """Test that React + Vite template has package.json."""
        package_json = react_vite_dir / "package.json"
        assert package_json.exists(), "package.json should exist"

        with open(package_json) as f:
            data = json.load(f)

        assert "dependencies" in data
        assert "devDependencies" in data
        assert "scripts" in data
        assert "react" in data["dependencies"]
        assert "vite" in data["devDependencies"]

    def test_react_vite_has_vite_config(self, react_vite_dir):
        """Test that React + Vite template has vite.config.ts."""
        vite_config = react_vite_dir / "vite.config.ts"
        assert vite_config.exists(), "vite.config.ts should exist"

    def test_react_vite_has_tsconfig(self, react_vite_dir):
        """Test that React + Vite template has tsconfig.json."""
        tsconfig = react_vite_dir / "tsconfig.json"
        assert tsconfig.exists(), "tsconfig.json should exist"

        with open(tsconfig) as f:
            data = json.load(f)

        assert "compilerOptions" in data

    def test_react_vite_has_src_directory(self, react_vite_dir):
        """Test that React + Vite template has src directory with required files."""
        src_dir = react_vite_dir / "src"
        assert src_dir.exists(), "src directory should exist"

        required_files = ["main.tsx", "App.tsx", "types.d.ts"]
        for filename in required_files:
            assert (src_dir / filename).exists(), f"{filename} should exist in src/"

    def test_react_vite_has_claude_config(self, react_vite_dir):
        """Test that React + Vite template has .claude configuration."""
        claude_dir = react_vite_dir / ".claude"
        assert claude_dir.exists(), ".claude directory should exist"

        settings_file = claude_dir / "settings.json"
        assert settings_file.exists(), ".claude/settings.json should exist"

        with open(settings_file) as f:
            data = json.load(f)

        assert "rules" in data

    def test_react_vite_has_readme(self, react_vite_dir):
        """Test that React + Vite template has README."""
        readme = react_vite_dir / "README.md"
        assert readme.exists(), "README.md should exist"

    def test_react_vite_has_gitignore(self, react_vite_dir):
        """Test that React + Vite template has .gitignore."""
        gitignore = react_vite_dir / ".gitignore"
        assert gitignore.exists(), ".gitignore should exist"


class TestNextJSTemplate:
    """Tests for Next.js template."""

    @pytest.fixture
    def nextjs_dir(self, templates_dir):
        return templates_dir / "new_webapp" / "nextjs"

    def test_nextjs_template_exists(self, nextjs_dir):
        """Test that Next.js template directory exists."""
        assert nextjs_dir.exists(), "Next.js template should exist"

    def test_nextjs_has_package_json(self, nextjs_dir):
        """Test that Next.js template has package.json."""
        package_json = nextjs_dir / "package.json"
        assert package_json.exists(), "package.json should exist"

        with open(package_json) as f:
            data = json.load(f)

        assert "dependencies" in data
        assert "next" in data["dependencies"]
        assert "react" in data["dependencies"]

    def test_nextjs_has_config(self, nextjs_dir):
        """Test that Next.js template has next.config.js."""
        config = nextjs_dir / "next.config.js"
        assert config.exists(), "next.config.js should exist"

    def test_nextjs_has_app_directory(self, nextjs_dir):
        """Test that Next.js template has app directory (App Router)."""
        app_dir = nextjs_dir / "app"
        assert app_dir.exists(), "app directory should exist"

        required_files = ["layout.tsx", "page.tsx"]
        for filename in required_files:
            assert (app_dir / filename).exists(), f"{filename} should exist in app/"

    def test_nextjs_has_api_route(self, nextjs_dir):
        """Test that Next.js template has example API route."""
        api_route = nextjs_dir / "app" / "api" / "hello" / "route.ts"
        assert api_route.exists(), "Example API route should exist"

    def test_nextjs_has_claude_config(self, nextjs_dir):
        """Test that Next.js template has .claude configuration."""
        claude_dir = nextjs_dir / ".claude"
        assert claude_dir.exists(), ".claude directory should exist"

        settings_file = claude_dir / "settings.json"
        assert settings_file.exists(), ".claude/settings.json should exist"


class TestVanillaTemplate:
    """Tests for Vanilla JavaScript template."""

    @pytest.fixture
    def vanilla_dir(self, templates_dir):
        return templates_dir / "new_webapp" / "vanilla"

    def test_vanilla_template_exists(self, vanilla_dir):
        """Test that Vanilla template directory exists."""
        assert vanilla_dir.exists(), "Vanilla template should exist"

    def test_vanilla_has_required_files(self, vanilla_dir):
        """Test that Vanilla template has all required files."""
        required_files = ["index.html", "style.css", "script.js", "README.md"]
        for filename in required_files:
            assert (vanilla_dir / filename).exists(), f"{filename} should exist"

    def test_vanilla_html_is_valid(self, vanilla_dir):
        """Test that index.html has basic HTML structure."""
        html_file = vanilla_dir / "index.html"
        with open(html_file) as f:
            content = f.read()

        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "<head>" in content
        assert "<body>" in content

    def test_vanilla_has_gitignore(self, vanilla_dir):
        """Test that Vanilla template has .gitignore."""
        gitignore = vanilla_dir / ".gitignore"
        assert gitignore.exists(), ".gitignore should exist"


class TestIntegrationGuide:
    """Tests for integration guide."""

    def test_integration_guide_exists(self, templates_dir):
        """Test that integration guide exists."""
        guide = templates_dir / "existing_webapp" / "integration_guide.md"
        assert guide.exists(), "Integration guide should exist"

    def test_integration_guide_has_content(self, templates_dir):
        """Test that integration guide has substantial content."""
        guide = templates_dir / "existing_webapp" / "integration_guide.md"
        with open(guide) as f:
            content = f.read()

        # Check for key sections
        assert "# Integrating ADW" in content or "## Overview" in content
        assert len(content) > 1000, "Integration guide should have substantial content"


class TestScaffoldingScripts:
    """Tests for scaffolding scripts."""

    def test_setup_new_project_script_exists(self, project_root):
        """Test that setup_new_project.sh exists."""
        script = project_root / "scripts" / "setup_new_project.sh"
        assert script.exists(), "setup_new_project.sh should exist"

    def test_setup_new_project_script_is_executable(self, project_root):
        """Test that setup_new_project.sh is executable."""
        script = project_root / "scripts" / "setup_new_project.sh"
        assert os.access(script, os.X_OK), "setup_new_project.sh should be executable"

    def test_setup_new_project_script_has_shebang(self, project_root):
        """Test that setup_new_project.sh has proper shebang."""
        script = project_root / "scripts" / "setup_new_project.sh"
        with open(script) as f:
            first_line = f.readline()
        assert first_line.startswith("#!/bin/bash"), "Script should have bash shebang"

    def test_integrate_existing_script_exists(self, project_root):
        """Test that integrate_existing.sh exists."""
        script = project_root / "scripts" / "integrate_existing.sh"
        assert script.exists(), "integrate_existing.sh should exist"

    def test_integrate_existing_script_is_executable(self, project_root):
        """Test that integrate_existing.sh is executable."""
        script = project_root / "scripts" / "integrate_existing.sh"
        assert os.access(script, os.X_OK), "integrate_existing.sh should be executable"


class TestDocumentation:
    """Tests for documentation files."""

    def test_all_documentation_exists(self, project_root):
        """Test that all documentation files exist."""
        docs_dir = project_root / "docs"
        assert docs_dir.exists(), "docs directory should exist"

        required_docs = [
            "cli.md",
            "web-ui.md",
            "api.md",
            "architecture.md",
            "examples.md",
            "troubleshooting.md",
        ]

        for doc in required_docs:
            doc_file = docs_dir / doc
            assert doc_file.exists(), f"{doc} should exist"

    def test_documentation_has_content(self, project_root):
        """Test that documentation files have substantial content."""
        docs_dir = project_root / "docs"

        required_docs = [
            "cli.md",
            "web-ui.md",
            "api.md",
            "architecture.md",
            "examples.md",
            "troubleshooting.md",
        ]

        for doc in required_docs:
            doc_file = docs_dir / doc
            with open(doc_file) as f:
                content = f.read()
            assert len(content) > 500, f"{doc} should have substantial content"
