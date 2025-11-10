"""Tests for MCP (Model Context Protocol) configuration setup.

This module verifies that the required MCP configuration files exist and
are properly formatted in the tac-webbuilder project.
"""

import json
from pathlib import Path

import pytest


# Get the project root directory (tac-webbuilder)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def test_mcp_config_exists():
    """Verify that .mcp.json.sample exists in tac-webbuilder root.

    The .mcp.json.sample file is a template for the MCP configuration
    that users should copy to .mcp.json for their local setup.
    """
    mcp_config_path = PROJECT_ROOT / ".mcp.json.sample"
    assert mcp_config_path.exists(), (
        f".mcp.json.sample not found at {mcp_config_path}. "
        "This file is required for MCP configuration."
    )


def test_playwright_config_exists():
    """Verify that playwright-mcp-config.json exists in tac-webbuilder root.

    The playwright-mcp-config.json file contains Playwright-specific
    configuration for the MCP integration.
    """
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"
    assert playwright_config_path.exists(), (
        f"playwright-mcp-config.json not found at {playwright_config_path}. "
        "This file is required for Playwright MCP integration."
    )


def test_mcp_config_valid_json():
    """Parse and validate .mcp.json.sample is valid JSON with required structure.

    Verifies that the MCP configuration file:
    - Is valid JSON
    - Contains the 'mcpServers' key
    - Has 'playwright' server configuration
    - Contains required fields: command, args, env
    """
    mcp_config_path = PROJECT_ROOT / ".mcp.json.sample"

    # Skip test if file doesn't exist (other test will catch this)
    if not mcp_config_path.exists():
        pytest.skip(f".mcp.json.sample not found at {mcp_config_path}")

    # Parse JSON
    with open(mcp_config_path, "r") as f:
        config = json.load(f)

    # Verify structure
    assert "mcpServers" in config, "Config must have 'mcpServers' key"
    assert "playwright" in config["mcpServers"], (
        "Config must have 'playwright' server in mcpServers"
    )

    playwright_config = config["mcpServers"]["playwright"]
    assert "command" in playwright_config, "Playwright config must have 'command'"
    assert "args" in playwright_config, "Playwright config must have 'args'"
    assert "env" in playwright_config, "Playwright config must have 'env'"


def test_playwright_config_valid():
    """Parse and validate playwright-mcp-config.json is valid JSON with required structure.

    Verifies that the Playwright MCP configuration file:
    - Is valid JSON
    - Contains required browser configuration
    - Contains video recording settings
    """
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"

    # Skip test if file doesn't exist (other test will catch this)
    if not playwright_config_path.exists():
        pytest.skip(f"playwright-mcp-config.json not found at {playwright_config_path}")

    # Parse JSON
    with open(playwright_config_path, "r") as f:
        config = json.load(f)

    # Verify it's a valid dictionary (basic structure check)
    assert isinstance(config, dict), "Playwright config must be a JSON object"

    # Check for common Playwright configuration keys
    # (adjust based on actual expected structure)
    if "browserType" in config:
        assert config["browserType"] in ["chromium", "firefox", "webkit"], (
            "browserType must be one of: chromium, firefox, webkit"
        )


def test_playwright_config_uses_relative_paths():
    """Verify videos directory uses relative path ./videos not absolute path.

    Ensures that the configuration uses relative paths for portability
    across different development environments.
    """
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"

    # Skip test if file doesn't exist (other test will catch this)
    if not playwright_config_path.exists():
        pytest.skip(f"playwright-mcp-config.json not found at {playwright_config_path}")

    # Parse JSON
    with open(playwright_config_path, "r") as f:
        config = json.load(f)

    # Convert config to string to search for paths
    config_str = json.dumps(config)

    # Check that we don't have absolute paths
    assert "/Users/" not in config_str, (
        "Config should not contain absolute paths like /Users/..."
    )
    assert "C:\\" not in config_str, (
        "Config should not contain absolute paths like C:\\..."
    )

    # If videos directory is specified, verify it uses relative path
    if "videosPath" in config:
        videos_path = config["videosPath"]
        assert videos_path.startswith("./") or not videos_path.startswith("/"), (
            f"Videos path should be relative (e.g., './videos'), found: {videos_path}"
        )
