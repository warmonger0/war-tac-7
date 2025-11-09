# Feature: Project Structure & ADW Integration

**ADW ID:** 1afd9aba
**Date:** 2025-11-09
**Specification:** specs/issue-12-adw-1afd9aba-sdlc_planner-project-structure-foundation.md

## Overview

This feature establishes the foundational project structure and ADW (AI Developer Workflow) integration configuration for the tac-7 repository. It updates MCP (Model Context Protocol) configuration paths to use absolute paths instead of relative paths, and creates a patch specification for verifying git commit status.

## What Was Built

This implementation focuses on configuration path management and verification tooling:

- **Absolute Path Configuration**: Updated MCP and Playwright configurations to use absolute paths in the worktree isolation directory
- **Patch Specification**: Created a verification patch spec to validate git commit status for staged files
- **Project Foundation Spec**: Documented complete specification for tac-webbuilder project structure (specification only, implementation pending)

## Technical Implementation

### Files Modified

- `.mcp.json`: Updated Playwright MCP config path from relative `./playwright-mcp-config.json` to absolute `/Users/Warmonger0/tac/tac-7/trees/1afd9aba/playwright-mcp-config.json`
- `playwright-mcp-config.json`: Updated video recording directory from relative `./videos` to absolute `/Users/Warmonger0/tac/tac-7/trees/1afd9aba/videos`

### Files Created

- `specs/issue-12-adw-1afd9aba-sdlc_planner-project-structure-foundation.md`: Comprehensive specification (332 lines) detailing the complete tac-webbuilder project foundation including:
  - Directory structure with core/, interfaces/, adws/, templates/, scripts/ modules
  - ADW system copying strategy from parent tac-7 project
  - Configuration management using Pydantic with YAML and environment variable support
  - 25-step implementation plan with detailed tasks
  - Testing strategy and acceptance criteria
  - 15 validation commands for zero-regression verification

- `specs/patch/patch-adw-1afd9aba-verify-git-commit-status.md`: Verification patch specification (69 lines) for validating git commit status of staged files, including:
  - Git status verification steps
  - File tracking validation commands
  - Documentation of findings when files are already committed

### Key Changes

- **Configuration Path Management**: Switched from relative to absolute paths in the worktree isolation directory (`trees/1afd9aba/`) to ensure MCP servers and Playwright have reliable file system references regardless of execution context
- **Specification-First Approach**: Created comprehensive specification before implementation, following SDLC planning best practices with detailed step-by-step instructions
- **Patch Verification System**: Established pattern for creating verification patches that document expected git states and provide validation commands

## How to Use

### MCP Configuration

The MCP configuration now uses absolute paths in worktree isolation directories:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated",
        "--config",
        "/Users/Warmonger0/tac/tac-7/trees/1afd9aba/playwright-mcp-config.json"
      ]
    }
  }
}
```

This ensures Playwright MCP server correctly locates its configuration file when executed from any working directory within the worktree.

### Playwright Video Recording

Video recording directory is now absolute:

```json
{
  "contextOptions": {
    "recordVideo": {
      "dir": "/Users/Warmonger0/tac/tac-7/trees/1afd9aba/videos",
      "size": {
        "width": 1920,
        "height": 1080
      }
    }
  }
}
```

This ensures all browser session videos are consistently saved to the worktree's `videos/` directory.

### Project Specification

The tac-webbuilder project specification at `specs/issue-12-adw-1afd9aba-sdlc_planner-project-structure-foundation.md` provides:

1. **Implementation Plan**: 25 sequential steps from directory creation to validation
2. **Configuration System**: Pydantic-based configuration loading from YAML and environment variables
3. **ADW Integration**: Complete copying strategy for adw_modules, scripts, triggers, tests, and documentation
4. **Validation Commands**: 15 commands to verify the implementation with zero regressions

To implement the specification:
```bash
# Follow steps 1-25 in the specification sequentially
# Each step has clear verification criteria
# Run all validation commands after implementation
```

### Patch Verification

The patch specification provides git verification commands:

```bash
# Verify clean working tree
git status

# Verify no staged changes
git diff --cached --stat

# Verify file tracking
git ls-files | wc -l
git ls-files | grep -E "(core/|adws/|interfaces/|tests/|scripts/)"

# Verify commit history
git log --oneline -5
```

## Configuration

### MCP Server Configuration

- **Config Location**: Worktree-specific `.mcp.json` in trees/{adw_id}/ directory
- **Playwright Config**: Absolute path to `playwright-mcp-config.json` in same worktree
- **Video Storage**: Absolute path to `videos/` directory in worktree

### Worktree Isolation

The configuration supports ADW worktree isolation:
- Each ADW execution gets a dedicated worktree in `trees/{adw_id}/`
- Configuration files use absolute paths specific to that worktree
- Videos and artifacts are stored within the worktree directory
- Isolation prevents conflicts between concurrent ADW executions

## Testing

### MCP Configuration Testing

Verify MCP server can locate configuration:
```bash
cd /Users/Warmonger0/tac/tac-7/trees/1afd9aba
npx @playwright/mcp@latest --isolated --config "$PWD/playwright-mcp-config.json"
```

### Playwright Video Testing

Verify video recording uses correct directory:
```bash
ls -la /Users/Warmonger0/tac/tac-7/trees/1afd9aba/videos/
```

### Git Status Verification

Run patch validation commands:
```bash
git status  # Should show clean working tree
git diff --cached --stat  # Should show no staged files
git ls-files | wc -l  # Should show 160+ tracked files
```

### Specification Validation

Review specification completeness:
```bash
cat specs/issue-12-adw-1afd9aba-sdlc_planner-project-structure-foundation.md
# Verify: 25 implementation steps, testing strategy, acceptance criteria, validation commands
```

## Notes

### Path Management Strategy

**Why Absolute Paths?**
- MCP servers execute in unpredictable working directories
- Playwright needs reliable paths for video recording and configuration
- Worktree isolation requires self-contained configuration
- Absolute paths eliminate "file not found" errors when paths are resolved relative to unexpected directories

**Tradeoff:**
- Absolute paths are worktree-specific and not portable
- Each worktree gets its own configuration copies with different absolute paths
- This is intentional - worktrees are isolated execution environments

### Specification vs Implementation

This feature establishes the **specification** for tac-webbuilder but does not implement it. The specification serves as:
- Complete blueprint for future implementation
- Documentation of architectural decisions
- Validation criteria for implementation completeness
- Testing strategy for zero-regression verification

### Patch Verification Pattern

The patch specification demonstrates a verification pattern:
1. Issue raised about git commit status
2. Patch spec created with verification steps
3. Verification reveals files already committed
4. Patch documents findings and confirms no action needed

This pattern is useful for:
- Validating assumptions about repository state
- Documenting expected git behavior
- Creating runbook-style verification procedures
- Resolving confusion about file staging and commit status

### ADW Worktree Isolation

The configuration changes support ADW's worktree isolation model:
- Each ADW execution gets a unique worktree ID (e.g., `1afd9aba`)
- Worktree directory: `trees/{adw_id}/`
- Configuration files are copied to worktree with updated paths
- Artifacts (videos, logs) stay within worktree
- Multiple ADW executions can run concurrently without conflicts

### Future Considerations

**MCP Configuration Management:**
- Consider template-based config generation for new worktrees
- Automate absolute path substitution when creating worktree configs
- Add validation to ensure config paths exist before MCP server starts

**Specification Implementation:**
- The tac-webbuilder spec is ready for implementation
- All 25 steps are documented with clear acceptance criteria
- Validation commands provide zero-regression verification
- Configuration system uses modern Python practices (Pydantic, uv)

**Path Portability:**
- Current absolute paths are machine-specific
- Consider environment variable expansion: `${TAC_ROOT}/trees/${ADW_ID}/videos`
- Would require MCP server to support variable interpolation
- Or create wrapper script that expands variables before starting MCP
