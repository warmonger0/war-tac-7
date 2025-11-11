"""Shared pytest fixtures and configuration for the test suite."""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from tests.fixtures import api_responses, project_samples


@pytest.fixture
def mock_anthropic_client():
    """Create a mock Anthropic client for testing."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_client.messages.create.return_value = mock_response
    return mock_client, mock_response


@pytest.fixture
def sample_intent_feature():
    """Sample feature intent response."""
    return json.loads(api_responses.INTENT_FEATURE_RESPONSE)


@pytest.fixture
def sample_intent_bug():
    """Sample bug intent response."""
    return json.loads(api_responses.INTENT_BUG_RESPONSE)


@pytest.fixture
def sample_intent_chore():
    """Sample chore intent response."""
    return json.loads(api_responses.INTENT_CHORE_RESPONSE)


@pytest.fixture
def sample_requirements():
    """Sample requirements list."""
    return json.loads(api_responses.REQUIREMENTS_AUTH_RESPONSE)


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def react_vite_project(temp_project_dir):
    """Create a React + Vite project structure."""
    package_json_path = temp_project_dir / "package.json"
    package_json_path.write_text(
        project_samples.get_sample_project_json("react-vite")
    )

    # Create vite config
    vite_config = temp_project_dir / "vite.config.ts"
    vite_config.write_text("export default {}")

    # Create src directory
    src_dir = temp_project_dir / "src"
    src_dir.mkdir()
    (src_dir / "App.tsx").write_text("export default function App() {}")

    return temp_project_dir


@pytest.fixture
def nextjs_project(temp_project_dir):
    """Create a Next.js project structure."""
    package_json_path = temp_project_dir / "package.json"
    package_json_path.write_text(
        project_samples.get_sample_project_json("nextjs")
    )

    # Create next.config.js
    next_config = temp_project_dir / "next.config.js"
    next_config.write_text("module.exports = {}")

    # Create app directory
    app_dir = temp_project_dir / "app"
    app_dir.mkdir()
    (app_dir / "page.tsx").write_text("export default function Page() {}")

    return temp_project_dir


@pytest.fixture
def fastapi_project(temp_project_dir):
    """Create a FastAPI project structure."""
    pyproject_path = temp_project_dir / "pyproject.toml"
    pyproject_path.write_text(project_samples.FASTAPI_PYPROJECT_TOML)

    # Create main.py
    main_py = temp_project_dir / "main.py"
    main_py.write_text("from fastapi import FastAPI\napp = FastAPI()")

    return temp_project_dir


@pytest.fixture
def empty_project(temp_project_dir):
    """Create an empty project directory."""
    # Just .gitignore
    (temp_project_dir / ".gitignore").write_text("node_modules/\n")
    return temp_project_dir


@pytest.fixture
def corrupted_package_json_project(temp_project_dir):
    """Create a project with corrupted package.json."""
    package_json_path = temp_project_dir / "package.json"
    package_json_path.write_text(project_samples.CORRUPTED_PACKAGE_JSON)
    return temp_project_dir


@pytest.fixture
def monorepo_project(temp_project_dir):
    """Create a monorepo structure with multiple packages."""
    # Root package.json
    package_json_path = temp_project_dir / "package.json"
    package_json_path.write_text(
        project_samples.get_sample_project_json("turborepo")
    )

    # Create apps directory with React app
    apps_dir = temp_project_dir / "apps"
    apps_dir.mkdir()
    web_dir = apps_dir / "web"
    web_dir.mkdir()
    (web_dir / "package.json").write_text(
        project_samples.get_sample_project_json("react-vite")
    )

    # Create packages directory
    packages_dir = temp_project_dir / "packages"
    packages_dir.mkdir()

    return temp_project_dir


@pytest.fixture
def api_error_responses():
    """Collection of API error responses for testing error handling."""
    return {
        "rate_limit": api_responses.API_ERROR_RATE_LIMIT,
        "auth": api_responses.API_ERROR_AUTH,
        "timeout": api_responses.API_ERROR_TIMEOUT,
        "server": api_responses.API_ERROR_SERVER
    }


@pytest.fixture
def special_char_inputs():
    """Test inputs with special characters, Unicode, and edge cases."""
    return {
        "unicode": "Add emoji support 🎉 and i18n (中文, 日本語, العربية)",
        "markdown": "Add **bold** and _italic_ support with `code` blocks",
        "html": "Handle <script>alert('xss')</script> and &lt;entities&gt;",
        "sql": "'; DROP TABLE users; --",
        "very_long": "A " + "very " * 1000 + "long input",
        "empty": "",
        "whitespace": "   \n  \t  \n  ",
        "newlines": "First line\n\nSecond line\n\nThird line",
        "quotes": 'Mix of "double" and \'single\' quotes',
        "paths": "/usr/local/bin and C:\\Windows\\System32",
        "urls": "Check https://example.com and http://test.org",
        "emails": "Contact admin@example.com or support@test.org"
    }
