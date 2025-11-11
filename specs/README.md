# Specifications

## Overview

Feature and issue planning specifications created by the ADW SDLC planner. These documents provide detailed implementation plans, task breakdowns, and validation criteria for development work.

## Contents

### Issue Specifications

Issue specifications are created by the `sdlc_planner` agent and guide the implementation of features and fixes.

- [issue-12: Project Structure Foundation](issue-12-adw-1afd9aba-sdlc_planner-project-structure-foundation.md) - Initial project structure and ADW integration
- [issue-14: NL Processing & Issue Formatter](issue-14-adw-e2bbe1a5-sdlc_planner-nl-processing-issue-formatter.md) - Natural language processing and GitHub issue generation
- [issue-16: CLI Interface](issue-16-adw-fd9119bc-sdlc_planner-cli-interface.md) - Command-line interface implementation
- [issue-21: Web Backend API](issue-21-adw-8c59601f-sdlc_planner-web-backend-api.md) - Backend API and web service
- [issue-47: Update Upload Button](issue-47-adw-cc73faf1-sdlc_planner-update-upload-button.md) - UI improvement for upload button text
- [issue-53: Documentation Structure & Indexes](issue-53-adw-0a6c3431-sdlc_planner-docs-structure-indexes.md) - Documentation organization (this chore)

### Subdirectories

- [patch/](patch/) - Patch-level specifications for smaller changes and fixes

## Specification Structure

Each specification document typically includes:

- **Metadata** - Issue number, ADW ID, and GitHub issue reference
- **Description** - What the specification covers
- **Relevant Files** - Files that need to be created or modified
- **Step by Step Tasks** - Detailed implementation steps
- **Validation Commands** - Commands to verify correct implementation
- **Notes** - Additional context and considerations

## Naming Convention

Specifications follow this naming pattern:
```
issue-{number}-adw-{id}-{agent}-{description}.md
```

- `{number}` - GitHub issue number
- `{id}` - Unique ADW identifier (8-character hex)
- `{agent}` - Agent that created the spec (e.g., `sdlc_planner`)
- `{description}` - Brief description using kebab-case

## Workflow

1. **Planning** - Issue is created in GitHub
2. **Specification** - `sdlc_planner` analyzes and creates a detailed spec
3. **Implementation** - Development work follows the spec
4. **Validation** - Commands verify correct implementation
5. **Completion** - Issue is closed and documented

## See Also

- [ARCHITECTURE](../ARCHITECTURE.md) - System architecture overview
- [Feature Documentation](../app_docs/) - Implemented feature docs
- [Technical Documentation](../docs/) - Integration guides
- [Issues](../issues/) - Issue tracking and lifecycle management
