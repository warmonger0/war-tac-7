# Patch Specifications

## Overview

Patch-level specifications for incremental changes, fixes, and small improvements. These documents guide focused, surgical changes to the codebase.

## Contents

### ADW 1afd9aba - Project Structure Foundation

- [Verify Git Commit Status](patch-adw-1afd9aba-verify-git-commit-status.md) - Validation of git commit workflow

### ADW 7a8b6bca - Backend Reorganization

- [Fix Main Import](patch-adw-7a8b6bca-fix-main-import.md) - Correct import path after reorganization

### ADW b5e84e34 - Frontend Migration

- [Fix Hardcoded Ports](patch-adw-b5e84e34-fix-hardcoded-ports.md) - Remove hardcoded port numbers
- [Remove Hardcoded Port in package.json](patch-adw-b5e84e34-remove-hardcoded-port-packagejson.md) - Update package.json configuration
- [Restore Original Frontend](patch-adw-b5e84e34-restore-original-frontend.md) - Revert frontend changes

### ADW e7613043 - Playwright MCP Integration

- [Add Playwright MCP README](patch-adw-e7613043-add-playwright-mcp-readme.md) - Create README for Playwright integration
- [Create MCP Config Files](patch-adw-e7613043-create-mcp-config-files.md) - Configuration file setup
- [Create Missing MCP Tests](patch-adw-e7613043-create-missing-mcp-tests.md) - Test coverage additions
- [Create Playwright MCP Docs](patch-adw-e7613043-create-playwright-mcp-docs.md) - Documentation creation
- [Execute Template Cleanup](patch-adw-e7613043-execute-template-cleanup.md) - Remove unused templates
- [Remove Template References](patch-adw-e7613043-remove-template-references.md) - Clean up template references

## Patch Specification Structure

Each patch specification typically includes:

- **Title** - Brief description of the change
- **ADW ID** - Link to parent ADW workflow
- **Problem** - What issue is being addressed
- **Solution** - How to fix it
- **Files Changed** - Specific files to modify
- **Validation** - How to verify the fix

## Naming Convention

Patch specifications follow this pattern:
```
patch-adw-{id}-{description}.md
```

- `{id}` - Parent ADW identifier (8-character hex)
- `{description}` - Brief description using kebab-case

## When to Create a Patch Spec

Create patch specifications for:
- Bug fixes discovered during implementation
- Small improvements that don't warrant a full issue
- Cleanup tasks identified during code review
- Configuration adjustments
- Documentation additions

## See Also

- [Specifications](../) - Full issue specifications
- [ARCHITECTURE](../../ARCHITECTURE.md) - System architecture
- [Feature Documentation](../../app_docs/) - Feature implementation docs
