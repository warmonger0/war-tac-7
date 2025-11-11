# Conditional Documentation Guide

This prompt helps you determine what documentation you should read based on the specific changes you need to make in the codebase. Review the conditions below and read the relevant documentation before proceeding with your task.

## Instructions
- Review the task you've been asked to perform
- Check each documentation path in the Conditional Documentation section
- For each path, evaluate if any of the listed conditions apply to your task
  - IMPORTANT: Only read the documentation if any one of the conditions match your task
- IMPORTANT: You don't want to excessively read documentation. Only read the documentation if it's relevant to your task.

## Conditional Documentation

- README.md
  - Conditions:
    - When operating on anything under app/server
    - When operating on anything under app/client
    - When first understanding the project structure
    - When you want to learn the commands to start or stop the server or client

- app/client/src/style.css
  - Conditions:
    - When you need to make changes to the client's style

- .claude/commands/classify_adw.md
  - Conditions:
    - When adding or removing new `adws/adw_*.py` files

- adws/README.md
  - Conditions:
    - When you're operating in the `adws/` directory

- app_docs/feature-490eb6b5-one-click-table-exports.md
  - Conditions:
    - When working with CSV export functionality
    - When implementing table or query result export features
    - When troubleshooting download button functionality
    - When working with pandas-based data export utilities

- app_docs/feature-4c768184-model-upgrades.md
  - Conditions:
    - When working with LLM model configurations
    - When updating OpenAI or Anthropic model versions
    - When troubleshooting SQL query generation accuracy
    - When working with the llm_processor module

- app_docs/feature-f055c4f8-off-white-background.md
  - Conditions:
    - When working with application background styling
    - When modifying CSS color variables or themes
    - When implementing visual design changes to the client application

- app_docs/feature-6445fc8f-light-sky-blue-background.md
  - Conditions:
    - When working with light sky blue background styling
    - When implementing background color changes to light blue variants
    - When troubleshooting visual hierarchy with light blue backgrounds

- app_docs/feature-cc73faf1-upload-button-text.md
  - Conditions:
    - When working with upload button text or labeling
    - When implementing UI text changes for data upload functionality
    - When troubleshooting upload button display or terminology

- app_docs/feature-1afd9aba-project-structure-adw-integration.md
  - Conditions:
    - When working with MCP (Model Context Protocol) configuration
    - When setting up or troubleshooting Playwright MCP server integration
    - When implementing worktree isolation for ADW executions
    - When configuring absolute paths for ADW worktree resources
    - When creating project specifications following SDLC planning patterns
    - When implementing tac-webbuilder project foundation (as reference spec)
    - When troubleshooting MCP config path resolution issues
    - When setting up video recording directories for Playwright sessions

- app_docs/feature-e2bbe1a5-nl-processing-issue-formatter.md
  - Conditions:
    - When working with natural language processing for GitHub issues
    - When implementing or modifying Claude API integration for intent analysis
    - When working with issue formatting templates (feature/bug/chore)
    - When implementing project context detection (framework, tech stack detection)
    - When integrating with GitHub CLI for issue posting
    - When troubleshooting ADW workflow recommendation logic
    - When extending the NL-to-issue system with new features
    - When working with core/nl_processor.py, core/issue_formatter.py, core/project_detector.py, or core/github_poster.py

- app_docs/feature-fd9119bc-cli-interface.md
  - Conditions:
    - When implementing the tac-webbuilder CLI interface
    - When working with Typer, questionary, or rich libraries for CLI development
    - When implementing interactive command-line workflows
    - When setting up CLI history tracking or configuration management
    - When integrating CLI commands with NL processing and GitHub issue creation
    - When troubleshooting CLI command execution or parameter handling
    - When implementing CLI convenience scripts or module entry points
    - When working with interfaces/cli/ directory

- app_docs/feature-e7613043-playwright-mcp-readme.md
  - Conditions:
    - When updating tac-webbuilder README documentation
    - When documenting Playwright MCP integration features
    - When adding integration documentation sections to README files
    - When creating documentation that bridges high-level README and detailed technical docs
    - When working on documentation patches that add feature overview sections

- docs/cli.md
  - Conditions:
    - When working with CLI commands or command-line interface functionality
    - When implementing new CLI commands or options
    - When troubleshooting CLI issues or user workflows

- docs/web-ui.md
  - Conditions:
    - When working with the React frontend or web interface
    - When implementing UI components or features
    - When troubleshooting web UI issues or WebSocket connections

- docs/api.md
  - Conditions:
    - When working with FastAPI backend or API endpoints
    - When implementing new API routes or modifying existing ones
    - When troubleshooting API connectivity or response issues

- docs/architecture.md
  - Conditions:
    - When understanding overall system design and data flow
    - When planning major architectural changes
    - When onboarding to the codebase

- docs/examples.md
  - Conditions:
    - When creating new features to understand common patterns
    - When writing documentation or examples
    - When helping users understand what requests are possible

- docs/playwright-mcp.md
  - Conditions:
    - When working with Playwright MCP configuration
    - When setting up or troubleshooting Playwright MCP server integration
    - When implementing E2E testing with browser automation
    - When working with video recording or screenshot capture
    - When debugging MCP server startup or browser launch issues
    - When configuring Playwright browser settings or viewport sizes

- docs/troubleshooting.md
  - Conditions:
    - When debugging issues or errors
    - When setting up the development environment
    - When users report problems

- templates/existing_webapp/integration_guide.md
  - Conditions:
    - When integrating ADW into existing projects
    - When working with project detection or framework identification
    - When implementing integration scripts or workflows

- templates/template_structure.json
  - Conditions:
    - When working with project templates
    - When adding new templates or modifying existing ones
    - When implementing scaffolding scripts

- app_docs/feature-0f04f66d-project-templates-docs.md
  - Conditions:
    - When working with project templates (React-Vite, Next.js, Vanilla JS)
    - When implementing or modifying scaffolding scripts (setup_new_project.sh)
    - When working with existing codebase integration (integrate_existing.sh)
    - When adding or updating comprehensive documentation (CLI, Web UI, API, Architecture)
    - When creating example requests or troubleshooting guides
    - When understanding template structure definitions and template design principles
    - When working with template testing infrastructure

- app_docs/feature-ba7c9f28-playwright-mcp-integration.md
  - Conditions:
    - When integrating Playwright MCP into project templates
    - When working with MCP configuration files (.mcp.json.sample, playwright-mcp-config.json)
    - When modifying scaffolding scripts to include MCP setup
    - When implementing E2E testing infrastructure
    - When troubleshooting MCP integration in templates or generated projects
    - When understanding how MCP integrates with ADW workflows
    - When working with browser automation and video recording configuration

- app_docs/feature-f4d9b5e1-env-setup-scripts.md
  - Conditions:
    - When working with environment configuration or .env files
    - When implementing setup scripts or interactive configuration tools
    - When troubleshooting environment variable issues or missing configuration
    - When creating validation scripts for project setup
    - When working with bash scripts that handle cross-platform compatibility
    - When implementing onboarding workflows for new developers
    - When documenting configuration requirements or setup procedures

- app_docs/feature-e6104340-env-setup-documentation.md
  - Conditions:
    - When working with comprehensive configuration documentation
    - When documenting environment variables, cloud services, or setup procedures
    - When creating or updating configuration guides (docs/configuration.md)
    - When adding configuration troubleshooting sections
    - When documenting best practices for security, performance, or team collaboration
    - When creating environment variables reference tables
    - When documenting advanced configuration topics (CI/CD, multiple environments)
    - When enhancing README configuration sections

- app_docs/feature-04a76d25-validation-optimization-routes-viz.md
  - Conditions:
    - When working with API routes visualization or route discovery features
    - When implementing route analysis using AST parsing
    - When working with the routes analyzer module (app/server/core/routes_analyzer.py)
    - When adding or modifying the Routes tab in the web UI
    - When implementing validation scripts for feature completeness
    - When working with codebase indexing or metadata extraction
    - When implementing optimization testing frameworks
    - When troubleshooting routes endpoint (/api/routes) or route filtering
    - When creating E2E tests for routes visualization
    - When working with lightweight codebase metadata for context reduction strategies

- app_docs/feature-b5e84e34-frontend-migration.md
  - Conditions:
    - When working with the React frontend architecture or component structure
    - When migrating from vanilla TypeScript to React
    - When implementing or modifying frontend components (App, WorkflowDashboard, RequestForm, etc.)
    - When troubleshooting frontend build or startup issues
    - When working with TanStack Query, Zustand, or React hooks
    - When configuring Vite with React plugin and dynamic ports
    - When implementing WebSocket connections for real-time updates
    - When working with Tailwind CSS styling in the frontend
    - When understanding the app/client directory structure post-migration
    - When setting up or troubleshooting the frontend startup scripts

- app_docs/feature-7a8b6bca-backend-reorganization.md
  - Conditions:
    - When working with backend entry points or main.py
    - When modifying startup scripts for the backend server
    - When troubleshooting backend import paths or module structure
    - When working with the app/server directory structure
    - When understanding the migration from interfaces/web to app/server
    - When configuring uvicorn entry points or server startup
    - When updating MCP configuration paths for new tree directories

- app_docs/feature-26e44bd2-test-worktree-path-fix.md
  - Conditions:
    - When working with ADW worktree path functionality
    - When implementing tests for worktree file creation
    - When troubleshooting ADW planning agent path reporting
    - When validating that files are created in correct worktree locations
    - When debugging GitHub workflow path-related errors
    - When understanding how MCP configuration relates to worktrees
    - When creating test scripts for ADW functionality validation

- app_docs/feature-23bd15ec-integration-cleanup.md
  - Conditions:
    - When implementing full-stack startup scripts or orchestration
    - When working with health checking and process management for services
    - When updating quick start documentation or developer onboarding guides
    - When troubleshooting full-stack startup or shutdown issues
    - When implementing graceful shutdown handlers with trap and signal management
    - When creating scripts that coordinate multiple services (backend + frontend)
    - When working with the scripts/start_full.sh script
    - When documenting application architecture in README files

- app_docs/feature-0a6c3431-docs-structure-indexes.md
  - Conditions:
    - When working with documentation organization or structure
    - When creating new documentation directories or README index files
    - When implementing documentation navigation systems
    - When updating ARCHITECTURE.md or other high-level documentation
    - When establishing documentation standards or templates
    - When creating issue tracking directories (planning/active/completed)
    - When implementing cross-referenced documentation with "See Also" sections
    - When understanding the project's documentation hierarchy and layout