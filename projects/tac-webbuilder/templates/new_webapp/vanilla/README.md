# Vanilla JavaScript Application

This is a simple HTML/CSS/JavaScript application with no build tools required.

## Getting Started

1. Open `index.html` in your web browser
2. Or use a simple HTTP server:
   ```bash
   python -m http.server 8000
   # or
   npx serve .
   ```

## Structure

- `index.html` - Main HTML file
- `style.css` - Styles
- `script.js` - JavaScript code

## MCP Integration

This template includes Model Context Protocol (MCP) configuration for enhanced development capabilities:

- `.mcp.json.sample` - Sample MCP server configuration
- `playwright-mcp-config.json` - Playwright MCP configuration for browser automation

To use MCP:
1. Copy `.mcp.json.sample` to `.mcp.json`
2. Configure as needed for your development environment
