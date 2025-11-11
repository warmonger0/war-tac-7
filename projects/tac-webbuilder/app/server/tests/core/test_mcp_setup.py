"""Tests for root-level MCP configuration validity."""

import json
from pathlib import Path

# Get project root (4 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def test_mcp_config_exists():
    """Verify .mcp.json.sample exists in project root."""
    mcp_config_path = PROJECT_ROOT / ".mcp.json.sample"
    assert mcp_config_path.exists(), ".mcp.json.sample not found in project root"


def test_playwright_config_exists():
    """Verify playwright-mcp-config.json exists in project root."""
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"
    assert playwright_config_path.exists(), "playwright-mcp-config.json not found in project root"


def test_mcp_config_valid_json():
    """Verify .mcp.json.sample is valid JSON with correct structure."""
    mcp_config_path = PROJECT_ROOT / ".mcp.json.sample"
    
    with open(mcp_config_path, 'r') as f:
        config = json.load(f)
    
    # Verify structure
    assert "mcpServers" in config, ".mcp.json.sample missing 'mcpServers' key"
    assert "playwright" in config["mcpServers"], ".mcp.json.sample missing 'playwright' server"
    
    playwright_config = config["mcpServers"]["playwright"]
    assert "command" in playwright_config, "playwright config missing 'command'"
    assert "args" in playwright_config, "playwright config missing 'args'"
    assert playwright_config["command"] == "npx", "playwright command should be 'npx'"
    assert "@playwright/mcp@latest" in playwright_config["args"], "playwright args missing @playwright/mcp@latest"


def test_playwright_config_valid():
    """Verify playwright-mcp-config.json is valid JSON with required fields."""
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"
    
    with open(playwright_config_path, 'r') as f:
        config = json.load(f)
    
    # Verify structure
    assert "browser" in config, "playwright-mcp-config.json missing 'browser' key"
    
    browser_config = config["browser"]
    assert "browserName" in browser_config, "browser config missing 'browserName'"
    assert "launchOptions" in browser_config, "browser config missing 'launchOptions'"
    assert "contextOptions" in browser_config, "browser config missing 'contextOptions'"
    
    # Verify browser name is valid
    valid_browsers = ["chromium", "firefox", "webkit"]
    assert browser_config["browserName"] in valid_browsers, f"browserName must be one of {valid_browsers}"
    
    # Verify headless mode is configured
    assert "headless" in browser_config["launchOptions"], "launchOptions missing 'headless'"
    assert isinstance(browser_config["launchOptions"]["headless"], bool), "headless must be boolean"


def test_mcp_config_references_playwright_config():
    """Verify .mcp.json.sample references the correct Playwright config path."""
    mcp_config_path = PROJECT_ROOT / ".mcp.json.sample"
    
    with open(mcp_config_path, 'r') as f:
        config = json.load(f)
    
    playwright_args = config["mcpServers"]["playwright"]["args"]
    
    # Check that --config flag is present
    assert "--config" in playwright_args, "playwright args missing --config flag"
    
    # Get the config path (should be after --config)
    config_idx = playwright_args.index("--config")
    assert config_idx + 1 < len(playwright_args), "--config flag has no value"
    
    config_path = playwright_args[config_idx + 1]
    assert config_path == "./playwright-mcp-config.json", "playwright config path should be relative"


def test_playwright_config_uses_relative_video_path():
    """Verify playwright-mcp-config.json uses relative path for video directory."""
    playwright_config_path = PROJECT_ROOT / "playwright-mcp-config.json"
    
    with open(playwright_config_path, 'r') as f:
        config = json.load(f)
    
    # Check if recordVideo is configured
    if "contextOptions" in config["browser"] and "recordVideo" in config["browser"]["contextOptions"]:
        video_config = config["browser"]["contextOptions"]["recordVideo"]
        
        if video_config is not None and "dir" in video_config:
            video_dir = video_config["dir"]
            assert video_dir.startswith("./"), f"Video directory should use relative path, got: {video_dir}"
            assert not video_dir.startswith("/"), f"Video directory should not be absolute path, got: {video_dir}"
