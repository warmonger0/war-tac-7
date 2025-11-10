"""Tests for MCP configuration presence in all templates."""

import json
from pathlib import Path

# Get project root (5 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates" / "new_webapp"


def test_react_vite_has_mcp():
    """Verify React-Vite template includes both MCP files."""
    template_dir = TEMPLATES_DIR / "react-vite"
    
    mcp_config = template_dir / ".mcp.json.sample"
    playwright_config = template_dir / "playwright-mcp-config.json"
    
    assert mcp_config.exists(), "React-Vite template missing .mcp.json.sample"
    assert playwright_config.exists(), "React-Vite template missing playwright-mcp-config.json"
    
    # Verify files are valid JSON
    with open(mcp_config, 'r') as f:
        json.load(f)
    with open(playwright_config, 'r') as f:
        json.load(f)


def test_nextjs_has_mcp():
    """Verify Next.js template includes both MCP files."""
    template_dir = TEMPLATES_DIR / "nextjs"
    
    mcp_config = template_dir / ".mcp.json.sample"
    playwright_config = template_dir / "playwright-mcp-config.json"
    
    assert mcp_config.exists(), "Next.js template missing .mcp.json.sample"
    assert playwright_config.exists(), "Next.js template missing playwright-mcp-config.json"
    
    # Verify files are valid JSON
    with open(mcp_config, 'r') as f:
        json.load(f)
    with open(playwright_config, 'r') as f:
        json.load(f)


def test_vanilla_has_mcp():
    """Verify Vanilla JS template includes both MCP files."""
    template_dir = TEMPLATES_DIR / "vanilla"
    
    mcp_config = template_dir / ".mcp.json.sample"
    playwright_config = template_dir / "playwright-mcp-config.json"
    
    assert mcp_config.exists(), "Vanilla template missing .mcp.json.sample"
    assert playwright_config.exists(), "Vanilla template missing playwright-mcp-config.json"
    
    # Verify files are valid JSON
    with open(mcp_config, 'r') as f:
        json.load(f)
    with open(playwright_config, 'r') as f:
        json.load(f)


def test_react_vite_gitignore_includes_mcp():
    """Verify React-Vite .gitignore has MCP patterns."""
    gitignore_path = TEMPLATES_DIR / "react-vite" / ".gitignore"
    
    assert gitignore_path.exists(), "React-Vite .gitignore not found"
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    assert ".mcp.json" in content, "React-Vite .gitignore missing .mcp.json"
    assert "videos/" in content, "React-Vite .gitignore missing videos/"


def test_nextjs_gitignore_includes_mcp():
    """Verify Next.js .gitignore has MCP patterns."""
    gitignore_path = TEMPLATES_DIR / "nextjs" / ".gitignore"
    
    assert gitignore_path.exists(), "Next.js .gitignore not found"
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    assert ".mcp.json" in content, "Next.js .gitignore missing .mcp.json"
    assert "videos/" in content, "Next.js .gitignore missing videos/"


def test_vanilla_gitignore_includes_mcp():
    """Verify Vanilla JS .gitignore has MCP patterns."""
    gitignore_path = TEMPLATES_DIR / "vanilla" / ".gitignore"
    
    assert gitignore_path.exists(), "Vanilla .gitignore not found"
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    assert ".mcp.json" in content, "Vanilla .gitignore missing .mcp.json"
    assert "videos/" in content, "Vanilla .gitignore missing videos/"


def test_mcp_configs_use_relative_paths():
    """Verify all template configs use relative paths (./videos, not absolute)."""
    templates = ["react-vite", "nextjs", "vanilla"]
    
    for template in templates:
        # Check MCP config
        mcp_config_path = TEMPLATES_DIR / template / ".mcp.json.sample"
        with open(mcp_config_path, 'r') as f:
            mcp_config = json.load(f)
        
        playwright_args = mcp_config["mcpServers"]["playwright"]["args"]
        config_idx = playwright_args.index("--config")
        config_path = playwright_args[config_idx + 1]
        
        assert config_path.startswith("./"), f"{template}: MCP config path should be relative"
        assert not config_path.startswith("/"), f"{template}: MCP config path should not be absolute"
        
        # Check Playwright config
        playwright_config_path = TEMPLATES_DIR / template / "playwright-mcp-config.json"
        with open(playwright_config_path, 'r') as f:
            playwright_config = json.load(f)
        
        if "contextOptions" in playwright_config["browser"]:
            if "recordVideo" in playwright_config["browser"]["contextOptions"]:
                video_config = playwright_config["browser"]["contextOptions"]["recordVideo"]
                
                if video_config is not None and "dir" in video_config:
                    video_dir = video_config["dir"]
                    assert video_dir.startswith("./"), f"{template}: Video directory should use relative path"
                    assert not video_dir.startswith("/"), f"{template}: Video directory should not be absolute"


def test_template_mcp_configs_match_root():
    """Verify template MCP configurations match the root configuration structure."""
    templates = ["react-vite", "nextjs", "vanilla"]
    
    # Read root config
    root_mcp_path = PROJECT_ROOT / ".mcp.json.sample"
    with open(root_mcp_path, 'r') as f:
        root_config = json.load(f)
    
    root_playwright_path = PROJECT_ROOT / "playwright-mcp-config.json"
    with open(root_playwright_path, 'r') as f:
        root_playwright_config = json.load(f)
    
    for template in templates:
        # Check MCP config structure matches
        template_mcp_path = TEMPLATES_DIR / template / ".mcp.json.sample"
        with open(template_mcp_path, 'r') as f:
            template_config = json.load(f)
        
        assert template_config.keys() == root_config.keys(), \
            f"{template}: MCP config keys don't match root"
        
        # Check Playwright config structure matches
        template_playwright_path = TEMPLATES_DIR / template / "playwright-mcp-config.json"
        with open(template_playwright_path, 'r') as f:
            template_playwright_config = json.load(f)
        
        assert template_playwright_config.keys() == root_playwright_config.keys(), \
            f"{template}: Playwright config keys don't match root"
        
        # Verify browser name is the same
        assert template_playwright_config["browser"]["browserName"] == \
            root_playwright_config["browser"]["browserName"], \
            f"{template}: Browser name should match root config"
