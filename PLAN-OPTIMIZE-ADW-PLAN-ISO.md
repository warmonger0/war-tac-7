# Plan: Optimize adw_plan_iso.py to Reduce Token Costs by 85%

## Problem Statement

Current `adw_plan_iso.py` costs **$1.31 per planning phase** due to:
1. **Unnecessary AI calls** for deterministic tasks (classification, branch naming)
2. **Massive ops agent overhead** - 51 messages with 17k context tokens each for simple file operations
3. **Hardcoded webbuilder assumptions** - always creates worktrees and installs full stack dependencies
4. **No project context detection** - treats all issues as webbuilder features

For simple tasks like "create a bash script in tac-7 root", this is **catastrophic waste**.

## Goal

Reduce planning phase costs from **$1.31 → $0.20 (85% reduction)** by:
1. Making **tac-7 root the default** (no worktree unless explicitly needed)
2. Replacing **AI calls with deterministic code** where possible
3. Eliminating the **ops agent entirely** for infrastructure tasks
4. Making worktrees **opt-in for webbuilder**, not mandatory

## Analysis Tasks

### Task 1: Catalog All AI Agent Calls in adw_plan_iso.py

Document every AI agent invocation:

**File:** `adws/adw_plan_iso.py`

1. **Line 143:** `classify_issue()`
   - Agent: `issue_classifier`
   - Command: `/classify_issue`
   - Purpose: Determine /chore, /bug, or /feature
   - Tokens: ~22k (17k context + 5k input)
   - **Can Replace:** Yes - regex pattern matching

2. **Line 162:** `generate_branch_name()`
   - Agent: `branch_generator`
   - Command: `/generate_branch_name`
   - Purpose: Create git branch name
   - Tokens: ~22k (17k context + 5k input)
   - **Can Replace:** Yes - string templating

3. **Line 210:** `execute_template('/install_worktree')`
   - Agent: `ops`
   - Command: `/install_worktree`
   - Purpose: Copy files, install deps, setup DB
   - Tokens: ~892k total (51 messages × 17.5k each)
   - **Can Replace:** Yes - pure Python function

4. **Line 234:** `build_plan()`
   - Agent: `sdlc_planner`
   - Command: `/feature | /bug | /chore`
   - Purpose: Generate implementation plan
   - Tokens: ~210k across 8 messages
   - **Can Replace:** NO - core AI reasoning task

5. **Line 306:** `create_commit()`
   - Purpose: Generate commit message
   - Tokens: ~500 (likely already optimized)
   - **Can Replace:** Already mostly deterministic

**Total Wasteful Tokens:** ~936k tokens (~$1.10 of the $1.31 cost)

### Task 2: Identify Project Context Markers

Determine how to detect tac-7 root vs webbuilder:

**Check these locations:**
- Issue body contains: `**Project**: tac-7` or `**Project**: tac-7 (NOT tac-webbuilder)`
- Issue body contains: `**Working Directory**: /Users/.../tac-7` (not nested in projects/)
- Plan references: No `app/server`, `app/client`, `projects/tac-webbuilder` paths
- Issue title patterns: "script", "tool", "workflow", "automation"
- Label: Could add `project:tac-7-root` vs `project:webbuilder` labels

**Default behavior:**
- **ASSUME tac-7 root** unless explicit webbuilder markers detected
- Webbuilder markers: references to app/server, app/client, database, frontend, backend

### Task 3: Design Simple Mode vs Isolated Mode

Create two execution paths:

#### **Simple Mode (tac-7 root - NEW DEFAULT)**
```python
if detect_simple_mode(issue):
    # Work in main repo (pwd = /Users/.../tac-7)
    working_dir = os.getcwd()

    # No worktree creation
    # No port allocation
    # No dependency installation

    # Just create branch in main repo
    subprocess.run(['git', 'checkout', '-b', branch_name])

    # Generate plan in main repo
    plan_response = build_plan(issue, issue_command, adw_id, logger, working_dir)

    # Commit and push
    commit_changes(commit_msg)
```

#### **Isolated Mode (webbuilder - OPT-IN)**
```python
else:  # Webbuilder or explicit isolation requested
    # Existing worktree logic
    worktree_path = create_worktree(adw_id, branch_name, logger)
    setup_worktree_dependencies_pure_python(worktree_path, ports)
    plan_response = build_plan(issue, issue_command, adw_id, logger, worktree_path)
```

### Task 4: Create Pure Python Replacement Functions

#### Replace `classify_issue()` with pattern matching:
```python
def classify_issue_deterministic(issue: GitHubIssue) -> str:
    """Classify issue using keyword matching."""
    text = f"{issue.title} {issue.body}".lower()

    # Bug indicators
    if any(word in text for word in ['fix', 'bug', 'error', 'broken', 'issue']):
        return '/bug'

    # Chore indicators
    if any(word in text for word in ['refactor', 'cleanup', 'update', 'upgrade', 'chore']):
        return '/chore'

    # Default to feature
    return '/feature'
```

#### Replace `generate_branch_name()` with template:
```python
def generate_branch_name_deterministic(issue: GitHubIssue, issue_class: str, adw_id: str) -> str:
    """Generate branch name from template."""
    prefix = issue_class.lstrip('/')  # Remove leading /
    slug = slugify(issue.title, max_length=50)
    return f"{prefix}-issue-{issue.number}-adw-{adw_id}-{slug}"
```

#### Replace `/install_worktree` ops agent with Python:
```python
def setup_worktree_dependencies(worktree_path: str, backend_port: int, frontend_port: int):
    """Install dependencies without AI overhead."""
    import shutil
    import subprocess

    # Copy env files
    shutil.copy('.env.sample', f'{worktree_path}/.env')
    shutil.copy('app/server/.env.sample', f'{worktree_path}/app/server/.env')

    # Append port config
    with open(f'{worktree_path}/.env', 'a') as f:
        f.write(f'\nBACKEND_PORT={backend_port}\n')
        f.write(f'FRONTEND_PORT={frontend_port}\n')

    # Install backend deps
    subprocess.run(['uv', 'sync', '--all-extras'],
                   cwd=f'{worktree_path}/app/server', check=True)

    # Install frontend deps
    subprocess.run(['bun', 'install'],
                   cwd=f'{worktree_path}/app/client', check=True)

    # Setup database
    subprocess.run(['./scripts/reset_db.sh'],
                   cwd=worktree_path, check=True)
```

## Implementation Plan

### Phase 1: Add Project Detection (2 hours)

**File:** `adws/adw_modules/project_detection.py` (NEW)

```python
def detect_project_context(issue: GitHubIssue) -> str:
    """Detect if issue is for tac-7 root or webbuilder."""
    # Check explicit markers
    if "NOT tac-webbuilder" in issue.body:
        return "tac-7-root"

    if "projects/tac-webbuilder" in issue.body:
        return "webbuilder"

    # Check for webbuilder indicators
    webbuilder_keywords = [
        'app/server', 'app/client', 'database',
        'frontend', 'backend', 'API endpoint'
    ]

    if any(keyword in issue.body for keyword in webbuilder_keywords):
        return "webbuilder"

    # Default to tac-7 root
    return "tac-7-root"

def requires_worktree(issue: GitHubIssue) -> bool:
    """Determine if issue needs isolated worktree."""
    return detect_project_context(issue) == "webbuilder"
```

### Phase 2: Create Deterministic Helpers (3 hours)

**File:** `adws/adw_modules/deterministic_ops.py` (NEW)

Implement:
- `classify_issue_deterministic()`
- `generate_branch_name_deterministic()`
- `setup_worktree_dependencies_pure_python()`

### Phase 3: Modify adw_plan_iso.py (4 hours)

**Changes to:** `adws/adw_plan_iso.py`

1. Add imports:
```python
from adw_modules.project_detection import requires_worktree, detect_project_context
from adw_modules.deterministic_ops import (
    classify_issue_deterministic,
    generate_branch_name_deterministic,
    setup_worktree_dependencies_pure_python
)
```

2. After fetching issue, detect mode:
```python
# Line ~130, after fetch_issue
project_context = detect_project_context(issue)
needs_worktree = requires_worktree(issue)

logger.info(f"Project context: {project_context}, Needs worktree: {needs_worktree}")
```

3. Replace AI classification (Line 143):
```python
# OLD: issue_command, error = classify_issue(issue, adw_id, logger)
# NEW:
issue_command = classify_issue_deterministic(issue)
logger.info(f"Issue classified as: {issue_command}")
```

4. Replace AI branch naming (Line 162):
```python
# OLD: branch_name, error = generate_branch_name(issue, issue_command, adw_id, logger)
# NEW:
branch_name = generate_branch_name_deterministic(issue, issue_command, adw_id)
logger.info(f"Generated branch name: {branch_name}")
```

5. Conditional worktree creation (Line 180):
```python
if needs_worktree:
    # Create worktree for webbuilder
    worktree_path = create_worktree(adw_id, branch_name, logger)
    setup_worktree_dependencies_pure_python(worktree_path, backend_port, frontend_port)
    working_dir = worktree_path
else:
    # Work in main repo for tac-7 root
    working_dir = os.getcwd()
    # Create branch in main repo
    subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
    # No dependency installation needed
```

6. Update plan generation to use working_dir:
```python
# Line 234 already supports working_dir parameter
plan_response = build_plan(issue, issue_command, adw_id, logger, working_dir)
```

### Phase 4: Update /feature.md Template (1 hour)

**File:** `.claude/commands/feature.md`

Change lines 32-44 to be conditional:

```markdown
## Relevant Files

**IMPORTANT:** Check the issue body for project context first.

**If issue specifies tac-7 root (NOT webbuilder):**
- Focus on: `scripts/**`, `adws/**`, root-level files
- Ignore: `app/server/**`, `app/client/**`, `projects/**`

**If issue is for webbuilder or doesn't specify:**
- `README.md` - Contains the project overview
- `app/server/**` - Backend codebase
- `app/client/**` - Frontend codebase
- `scripts/**` - Helper scripts
- `adws/**` - ADW workflows

Read `.claude/commands/conditional_docs.md` to check if additional docs are needed.
```

### Phase 5: Testing (2 hours)

**Test Cases:**

1. **Simple tac-7 script issue** (like issue #43):
   - Should NOT create worktree
   - Should NOT call ops agent
   - Should work in main repo
   - Expected cost: ~$0.20

2. **Webbuilder feature issue**:
   - Should create worktree
   - Should install dependencies (but via Python, not ops)
   - Expected cost: ~$0.25

3. **Ambiguous issue**:
   - Should default to tac-7 root (no worktree)
   - Can be overridden if issue body has webbuilder keywords

## Success Criteria

- [ ] Planning phase cost reduced from $1.31 → $0.20 for tac-7 root tasks
- [ ] Planning phase cost reduced from $1.31 → $0.25 for webbuilder tasks
- [ ] Zero ops agent calls for dependency installation
- [ ] Deterministic classification and branch naming (no AI)
- [ ] tac-7 root is default behavior
- [ ] Webbuilder mode only activates when explicitly needed
- [ ] Existing webbuilder workflows still work correctly

## Estimated Time: 12 hours

## Estimated Cost Savings

- **Current average:** $1.31 per planning phase
- **After optimization:** $0.20 per planning phase
- **Savings per issue:** $1.11 (85% reduction)
- **For 100 issues:** $111 saved
- **For ZTE workflow (6 phases):** Even larger multiplier effect

## Next Steps

1. Create a new GitHub issue with this plan as the body
2. Use command: `adw_sdlc_zte_iso model_set base`
3. Let it execute in a fresh context
4. Monitor token usage with `monitor_adw_tokens.py`
5. Validate cost reduction achieved

## Files to Modify

- `adws/adw_plan_iso.py` (main changes)
- `adws/adw_modules/project_detection.py` (NEW)
- `adws/adw_modules/deterministic_ops.py` (NEW)
- `.claude/commands/feature.md` (template updates)
- `README.md` (document new default behavior)

## Files to Read for Context

- `adws/adw_plan_iso.py` - Current implementation
- `adws/adw_modules/workflow_ops.py` - Helper functions
- `adws/adw_modules/worktree_ops.py` - Worktree utilities
- `.claude/commands/install_worktree.md` - What ops agent does
- `agents/8810522b/adw_plan_iso/execution.log` - Real execution trace
- Current token monitoring output (from issue #43)
