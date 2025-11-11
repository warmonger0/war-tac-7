# Issue Tracking

## Overview

Issue tracking and lifecycle management for tac-webbuilder development. This directory organizes issues by their current state in the development workflow.

## Structure

The issue tracking system is organized into three lifecycle stages:

### planning/
Issues currently in the planning phase. These issues are being analyzed and specifications are being created.

**Status:** Planning and specification creation in progress

### active/
Issues actively being worked on. Implementation, testing, and review are happening for these issues.

**Status:** Active development, testing, or code review

### completed/
Issues that have been successfully implemented, reviewed, merged, and closed.

**Status:** Merged and closed

## Workflow

Issues move through these stages as they progress:

```
┌─────────┐     ┌────────┐     ┌───────────┐
│Planning │ --> │ Active │ --> │ Completed │
└─────────┘     └────────┘     └───────────┘
```

### Planning Stage
1. Issue created in GitHub
2. `sdlc_planner` analyzes the issue
3. Detailed specification created in `specs/`
4. Issue documentation added to `issues/planning/`

### Active Stage
1. Implementation begins based on specification
2. Issue documentation moved to `issues/active/`
3. Code changes made in dedicated git worktree
4. Tests written and validated
5. Pull request created

### Completed Stage
1. Code reviewed and approved
2. Pull request merged to main branch
3. GitHub issue closed
4. Issue documentation moved to `issues/completed/`

## Contents

Currently, these subdirectories are empty and will be populated as issues move through the development lifecycle.

- **planning/** - Issues in planning phase
- **active/** - Issues being actively worked on
- **completed/** - Finished and merged issues

## Issue Documentation

Each issue may have associated documentation:

- Planning notes and analysis
- Implementation progress tracking
- Test results and validation
- Review feedback and resolutions
- Post-completion retrospectives

## Integration with Specs

Issue planning creates detailed specifications stored in the `specs/` directory:

- Full specifications: `specs/issue-{number}-adw-{id}-*.md`
- Patch specifications: `specs/patch/patch-adw-{id}-*.md`

These specifications guide implementation and validation.

## See Also

- [Specifications](../specs/) - Detailed implementation plans created by SDLC planner
- [Feature Documentation](../app_docs/) - Completed feature documentation
- [ARCHITECTURE](../ARCHITECTURE.md) - System architecture overview
- [GitHub Issues](https://github.com/your-org/tac-webbuilder/issues) - Live issue tracking
