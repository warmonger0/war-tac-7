# Natural Language Processing API Reference

## Overview

The NL Processing API provides a comprehensive system for converting natural language requests into structured GitHub issues with automatic ADW workflow triggers. This API consists of four core modules that work together to analyze user intent, format issues, detect project context, and post to GitHub.

## Core Modules

- **nl_processor** - Intent analysis and requirement extraction using Claude API
- **issue_formatter** - Template-based issue formatting for different types
- **project_detector** - Framework and complexity detection from project structure
- **github_poster** - GitHub CLI integration with rich terminal previews
- **data_models** - Pydantic models for data validation and serialization

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` (required) - Anthropic API key for Claude access
- `GITHUB_REPO_URL` (optional) - GitHub repository URL (e.g., "owner/repo")

### Import Paths

All modules are located in `app/server/core/`:

```python
from app.server.core.nl_processor import (
    analyze_intent,
    extract_requirements,
    classify_issue_type,
    suggest_adw_workflow,
    process_request
)
from app.server.core.issue_formatter import (
    format_issue,
    validate_issue_body,
    format_requirements_list,
    create_feature_issue_body,
    create_bug_issue_body,
    create_chore_issue_body
)
from app.server.core.project_detector import (
    detect_project_context,
    detect_framework,
    detect_backend,
    calculate_complexity_from_structure
)
from app.server.core.github_poster import GitHubPoster
from app.server.core.data_models import GitHubIssue, ProjectContext
```

---

## nl_processor Module

### `analyze_intent(nl_input: str) -> dict`

Analyzes natural language input to extract intent, summary, and technical area using Claude API.

**Parameters:**
- `nl_input` (str) - Natural language description of desired feature/bug/chore

**Returns:**
- dict containing:
  - `intent_type` (str) - One of "feature", "bug", or "chore"
  - `summary` (str) - Brief one-sentence summary
  - `technical_area` (str) - Primary technical area (e.g., "UI", "authentication", "database")

**Raises:**
- `ValueError` - If ANTHROPIC_API_KEY environment variable is not set
- `Exception` - If Claude API call fails

**Example:**

```python
intent = await analyze_intent("Add dark mode toggle to settings page")
# {
#   "intent_type": "feature",
#   "summary": "Add dark mode toggle to application settings",
#   "technical_area": "UI"
# }
```

### `extract_requirements(nl_input: str, intent: dict) -> List[str]`

Extracts concrete, actionable technical requirements from natural language input.

**Parameters:**
- `nl_input` (str) - Natural language description
- `intent` (dict) - Intent analysis from `analyze_intent()`

**Returns:**
- List[str] - List of specific technical requirements

**Raises:**
- `ValueError` - If ANTHROPIC_API_KEY environment variable is not set
- `Exception` - If Claude API call fails

**Example:**

```python
requirements = extract_requirements(
    "Add dark mode toggle to settings page",
    intent
)
# [
#   "Create dark mode toggle component in settings",
#   "Implement theme switching state management",
#   "Add CSS-in-JS styles for dark theme",
#   "Update components to support theme switching"
# ]
```

### `classify_issue_type(intent: dict) -> str`

Determines issue classification based on intent analysis.

**Parameters:**
- `intent` (dict) - Intent analysis dictionary

**Returns:**
- str - Issue classification: "feature", "bug", or "chore"

**Example:**

```python
classification = classify_issue_type(intent)
# "feature"
```

### `suggest_adw_workflow(issue_type: str, complexity: str) -> Tuple[str, str]`

Recommends ADW workflow and model set based on issue type and complexity.

**Parameters:**
- `issue_type` (str) - One of "feature", "bug", or "chore"
- `complexity` (str) - One of "low", "medium", or "high"

**Returns:**
- Tuple[str, str] - (workflow_name, model_set)
  - workflow_name: ADW workflow identifier
  - model_set: "base" or "heavy"

**Workflow Recommendation Logic:**
- Bugs → `adw_plan_build_test_iso` with `base` model
- Chores → `adw_sdlc_iso` with `base` model
- Features (low complexity) → `adw_sdlc_iso` with `base` model
- Features (medium complexity) → `adw_plan_build_test_iso` with `base` model
- Features (high complexity) → `adw_plan_build_test_iso` with `heavy` model

**Example:**

```python
workflow, model_set = suggest_adw_workflow("feature", "medium")
# ("adw_plan_build_test_iso", "base")
```

### `process_request(nl_input: str, project_context: ProjectContext) -> GitHubIssue`

Main orchestration function that converts natural language to a complete GitHub issue.

**Parameters:**
- `nl_input` (str) - Natural language description
- `project_context` (ProjectContext) - Project context from `detect_project_context()`

**Returns:**
- GitHubIssue - Complete GitHub issue with all fields populated

**Raises:**
- `Exception` - If any step of the processing pipeline fails

**Processing Pipeline:**
1. Analyze intent
2. Extract requirements
3. Classify issue type
4. Suggest workflow based on complexity
5. Generate title and body
6. Create labels
7. Return GitHubIssue object

**Example:**

```python
from app.server.core.project_detector import detect_project_context

context = detect_project_context("/path/to/project")
issue = await process_request(
    "Add dark mode toggle to settings page",
    context
)
# GitHubIssue(
#   title="Add dark mode toggle to application settings",
#   body="## Description\n...",
#   labels=["feature", "ui", "react-vite"],
#   classification="feature",
#   workflow="adw_plan_build_test_iso",
#   model_set="base"
# )
```

---

## issue_formatter Module

### Issue Templates

The module provides three issue templates:

**ISSUE_TEMPLATES["feature"]:**
```markdown
# {title}

## Description
{description}

## Requirements
{requirements}

## Technical Approach
{technical_approach}

## Workflow
{workflow}
```

**ISSUE_TEMPLATES["bug"]:**
```markdown
# {title}

## Issue Description
{description}

## Steps to Reproduce
{steps}

## Expected vs Actual Behavior
**Expected:** {expected}
**Actual:** {actual}

## Workflow
{workflow}
```

**ISSUE_TEMPLATES["chore"]:**
```markdown
# {title}

## Description
{description}

## Tasks
{tasks}

## Workflow
{workflow}
```

### `format_issue(issue: GitHubIssue, template_data: Dict[str, Any]) -> str`

Formats a GitHub issue using the appropriate template.

**Parameters:**
- `issue` (GitHubIssue) - GitHubIssue object
- `template_data` (Dict[str, Any]) - Template variables

**Returns:**
- str - Formatted issue body as markdown

**Raises:**
- `ValueError` - If required template field is missing

**Example:**

```python
formatted = format_issue(issue, {
    "title": "Add Dark Mode",
    "description": "Add dark mode toggle",
    "requirements": "- Implement toggle\n- Add styles",
    "technical_approach": "Use context API",
    "workflow": "adw_sdlc_iso model_set base"
})
```

### `validate_issue_body(body: str) -> bool`

Validates that an issue body contains required sections.

**Parameters:**
- `body` (str) - Issue body markdown

**Returns:**
- bool - True if valid, False otherwise

**Example:**

```python
is_valid = validate_issue_body(issue.body)
# True
```

### `format_requirements_list(requirements: list) -> str`

Formats a list of requirements as markdown bullet points.

**Parameters:**
- `requirements` (list) - List of requirement strings

**Returns:**
- str - Formatted markdown string

**Example:**

```python
formatted = format_requirements_list([
    "Create toggle component",
    "Add theme switching"
])
# "- Create toggle component\n- Add theme switching"
```

### `format_technical_approach(approach: str) -> str`

Formats technical approach section with fallback for empty input.

**Parameters:**
- `approach` (str) - Technical approach description

**Returns:**
- str - Formatted approach or default text

**Example:**

```python
formatted = format_technical_approach("")
# "To be determined during implementation planning."
```

### `format_workflow_section(workflow: str, model_set: str) -> str`

Formats the workflow section with ADW command syntax.

**Parameters:**
- `workflow` (str) - ADW workflow name (e.g., "adw_sdlc_iso")
- `model_set` (str) - Model set ("base" or "heavy")

**Returns:**
- str - Formatted workflow command

**Example:**

```python
formatted = format_workflow_section("adw_sdlc_iso", "base")
# "adw_sdlc_iso model_set base"
```

### `escape_markdown_special_chars(text: str) -> str`

Escapes special markdown characters in text.

**Parameters:**
- `text` (str) - Input text

**Returns:**
- str - Text with escaped markdown characters

**Note:** Currently a placeholder implementation that preserves markdown syntax.

### `create_feature_issue_body(...) -> str`

Creates a formatted feature issue body.

**Parameters:**
- `description` (str) - Feature description
- `requirements` (list) - List of requirements
- `technical_approach` (str, optional) - Technical approach
- `workflow` (str, default="adw_sdlc_iso") - ADW workflow
- `model_set` (str, default="base") - Model set

**Returns:**
- str - Formatted feature issue body

**Example:**

```python
body = create_feature_issue_body(
    description="Add dark mode toggle",
    requirements=["Create toggle", "Add styles"],
    technical_approach="Use context API",
    workflow="adw_sdlc_iso",
    model_set="base"
)
```

### `create_bug_issue_body(...) -> str`

Creates a formatted bug issue body.

**Parameters:**
- `description` (str) - Bug description
- `steps` (str, optional) - Steps to reproduce
- `expected` (str, optional) - Expected behavior
- `actual` (str, optional) - Actual behavior
- `workflow` (str, default="adw_plan_build_test_iso") - ADW workflow
- `model_set` (str, default="base") - Model set

**Returns:**
- str - Formatted bug issue body

**Example:**

```python
body = create_bug_issue_body(
    description="Login button not responding",
    steps="1. Click login\n2. Observe no response",
    expected="Login form appears",
    actual="Nothing happens"
)
```

### `create_chore_issue_body(...) -> str`

Creates a formatted chore issue body.

**Parameters:**
- `description` (str) - Chore description
- `tasks` (list) - List of tasks
- `workflow` (str, default="adw_sdlc_iso") - ADW workflow
- `model_set` (str, default="base") - Model set

**Returns:**
- str - Formatted chore issue body

**Example:**

```python
body = create_chore_issue_body(
    description="Update documentation",
    tasks=["Update README", "Add API docs"],
    workflow="adw_sdlc_iso",
    model_set="base"
)
```

---

## project_detector Module

### `detect_project_context(path: str) -> ProjectContext`

Main function that detects project context by analyzing directory structure and files.

**Parameters:**
- `path` (str) - Path to project directory

**Returns:**
- ProjectContext - Object with all detected project information

**Raises:**
- `ValueError` - If project path does not exist

**Detection Process:**
1. Check if directory exists
2. Determine if new project (empty directory)
3. Detect framework (React, Vue, Next.js, FastAPI, Django, Flask, etc.)
4. Detect backend framework (if applicable)
5. Detect build tools (Vite, Webpack, TypeScript, Docker, etc.)
6. Detect package manager (npm, yarn, pnpm, bun, uv, poetry, etc.)
7. Check git initialization
8. Calculate complexity from structure

**Example:**

```python
context = detect_project_context("/path/to/react-app")
# ProjectContext(
#   path="/path/to/react-app",
#   is_new_project=False,
#   framework="react-vite",
#   backend=None,
#   complexity="medium",
#   build_tools=["vite", "typescript"],
#   package_manager="npm",
#   has_git=True
# )
```

### `detect_framework(path: Path) -> Optional[str]`

Detects frontend/application framework from project files.

**Parameters:**
- `path` (Path) - Project path

**Returns:**
- Optional[str] - Framework name or None

**Detected Frameworks:**
- `react-vite` - React with Vite
- `vue-vite` - Vue with Vite
- `vite` - Vite without specific framework
- `nextjs` - Next.js
- `react` - React (without Vite)
- `vue` - Vue
- `angular` - Angular
- `svelte` - Svelte

**Detection Method:**
- Checks for `vite.config.ts`/`vite.config.js`
- Analyzes `package.json` dependencies
- Identifies framework-specific files

**Example:**

```python
framework = detect_framework(Path("/path/to/project"))
# "react-vite"
```

### `detect_backend(path: Path) -> Optional[str]`

Detects backend framework from project files.

**Parameters:**
- `path` (Path) - Project path

**Returns:**
- Optional[str] - Backend framework name or None

**Detected Backends:**
- `fastapi` - FastAPI (Python)
- `django` - Django (Python)
- `flask` - Flask (Python)
- `express` - Express (Node.js)
- `fastify` - Fastify (Node.js)
- `nestjs` - NestJS (Node.js)

**Detection Method:**
- Checks `pyproject.toml` and `requirements.txt` for Python frameworks
- Checks `package.json` dependencies for Node.js frameworks

**Example:**

```python
backend = detect_backend(Path("/path/to/project"))
# "fastapi"
```

### `detect_build_tools(path: Path) -> List[str]`

Detects build tools in the project.

**Parameters:**
- `path` (Path) - Project path

**Returns:**
- List[str] - List of detected build tools

**Detected Tools:**
- `vite` - Vite bundler
- `webpack` - Webpack bundler
- `rollup` - Rollup bundler
- `typescript` - TypeScript compiler
- `babel` - Babel transpiler
- `make` - Make build tool
- `docker` - Docker containerization

**Example:**

```python
tools = detect_build_tools(Path("/path/to/project"))
# ["vite", "typescript", "docker"]
```

### `detect_package_manager(path: Path) -> Optional[str]`

Detects package manager used in the project.

**Parameters:**
- `path` (Path) - Project path

**Returns:**
- Optional[str] - Package manager name or None

**Detected Managers:**
- `bun` - Bun (checks for `bun.lockb`)
- `pnpm` - pnpm (checks for `pnpm-lock.yaml`)
- `yarn` - Yarn (checks for `yarn.lock`)
- `npm` - npm (checks for `package-lock.json`)
- `uv` - uv (checks for `uv.lock`)
- `poetry` - Poetry (checks for `poetry.lock`)
- `pipenv` - Pipenv (checks for `Pipfile.lock`)

**Example:**

```python
pm = detect_package_manager(Path("/path/to/project"))
# "npm"
```

### `calculate_complexity_from_structure(...) -> str`

Calculates project complexity based on structure and detected components.

**Parameters:**
- `path` (Path) - Project path
- `framework` (Optional[str]) - Detected framework
- `backend` (Optional[str]) - Detected backend
- `build_tools` (List[str]) - List of build tools

**Returns:**
- str - Complexity level: "low", "medium", or "high"

**Complexity Scoring:**
- File count > 100: +2 points
- File count > 50: +1 point
- Has framework: +1 point
- Has backend: +1 point
- More than 2 build tools: +1 point
- Has monorepo structure (`packages/` or `apps/`): +2 points

**Thresholds:**
- Score >= 5: "high"
- Score >= 3: "medium"
- Score < 3: "low"

**Example:**

```python
complexity = calculate_complexity_from_structure(
    Path("/path/to/project"),
    framework="react-vite",
    backend="fastapi",
    build_tools=["vite", "typescript", "docker"]
)
# "high"
```

### `suggest_workflow(context: ProjectContext) -> str`

Recommends ADW workflow based on project context.

**Parameters:**
- `context` (ProjectContext) - Project context object

**Returns:**
- str - Recommended workflow name

**Recommendation Logic:**
- High complexity → `adw_plan_build_test_iso`
- Medium complexity → `adw_plan_build_test_iso`
- Low complexity → `adw_sdlc_iso`

**Example:**

```python
workflow = suggest_workflow(context)
# "adw_plan_build_test_iso"
```

### `calculate_complexity(context: ProjectContext) -> str`

Wrapper that returns the already-calculated complexity from ProjectContext.

**Parameters:**
- `context` (ProjectContext) - Project context object

**Returns:**
- str - Complexity level

**Example:**

```python
complexity = calculate_complexity(context)
# "medium"
```

---

## github_poster Module

### `class GitHubPoster`

GitHub CLI wrapper for posting issues with preview and confirmation.

#### `__init__(repo_url: Optional[str] = None)`

Initialize GitHub poster.

**Parameters:**
- `repo_url` (Optional[str]) - GitHub repository URL (optional, uses current repo if None)

**Example:**

```python
poster = GitHubPoster("owner/repo")
# or
poster = GitHubPoster()  # Uses current repo
```

#### `format_preview(issue: GitHubIssue) -> str`

Creates a rich terminal preview of the issue.

**Parameters:**
- `issue` (GitHubIssue) - Issue object

**Returns:**
- str - Formatted preview string

**Example:**

```python
preview = poster.format_preview(issue)
# Returns formatted markdown with title, classification, labels, and body
```

#### `post_issue(issue: GitHubIssue, confirm: bool = True) -> int`

Posts issue to GitHub via gh CLI.

**Parameters:**
- `issue` (GitHubIssue) - Issue object to post
- `confirm` (bool, default=True) - If True, shows preview and requests confirmation

**Returns:**
- int - Issue number of created issue

**Raises:**
- `RuntimeError` - If gh CLI is not available, not authenticated, or posting fails
- `RuntimeError` - If user cancels posting (when confirm=True)

**Workflow:**
1. Validates gh CLI availability and authentication
2. Shows preview if confirm=True
3. Requests user confirmation
4. Posts issue via `gh issue create` command
5. Extracts and returns issue number

**Example:**

```python
try:
    issue_number = poster.post_issue(issue, confirm=True)
    print(f"Issue created: #{issue_number}")
except RuntimeError as e:
    print(f"Failed to post issue: {e}")
```

#### `get_repo_info() -> dict`

Gets information about the current/specified repository.

**Returns:**
- dict - Repository information (name, owner, url)

**Raises:**
- `RuntimeError` - If unable to get repo info

**Example:**

```python
repo_info = poster.get_repo_info()
# {
#   "name": "my-repo",
#   "owner": {"login": "username"},
#   "url": "https://github.com/username/my-repo"
# }
```

---

## data_models Module

### `class GitHubIssue`

Pydantic model for GitHub issue representation.

**Fields:**
- `title` (str) - Issue title
- `body` (str) - Issue body in GitHub markdown format
- `labels` (List[str], default=[]) - Issue labels
- `classification` (Literal["feature", "bug", "chore"]) - Issue type classification
- `workflow` (str) - ADW workflow command (e.g., "adw_sdlc_iso")
- `model_set` (Literal["base", "heavy"]) - Model set for ADW workflow

**Example:**

```python
issue = GitHubIssue(
    title="Add dark mode toggle",
    body="## Description\n...",
    labels=["feature", "ui"],
    classification="feature",
    workflow="adw_sdlc_iso",
    model_set="base"
)
```

### `class ProjectContext`

Pydantic model for project context information.

**Fields:**
- `path` (str) - Project directory path
- `is_new_project` (bool) - Whether this is a new project
- `framework` (Optional[str], default=None) - Detected framework
- `backend` (Optional[str], default=None) - Detected backend framework
- `complexity` (Literal["low", "medium", "high"]) - Project complexity level
- `build_tools` (Optional[List[str]], default=[]) - Detected build tools
- `package_manager` (Optional[str], default=None) - Detected package manager
- `has_git` (bool, default=False) - Whether project has git initialized

**Example:**

```python
context = ProjectContext(
    path="/path/to/project",
    is_new_project=False,
    framework="react-vite",
    backend=None,
    complexity="medium",
    build_tools=["vite", "typescript"],
    package_manager="npm",
    has_git=True
)
```

---

## Error Handling

### Common Exceptions

**ValueError:**
- Raised when ANTHROPIC_API_KEY is not set
- Raised when project path does not exist
- Raised when required template field is missing

**RuntimeError:**
- Raised when gh CLI is not available or not authenticated
- Raised when GitHub CLI command fails
- Raised when user cancels issue posting

**Exception:**
- Generic exception for Claude API failures
- Generic exception for NL processing pipeline failures

### Error Handling Example

```python
from app.server.core.nl_processor import process_request
from app.server.core.project_detector import detect_project_context
from app.server.core.github_poster import GitHubPoster

try:
    # Detect project context
    context = detect_project_context("/path/to/project")

    # Process NL request
    issue = await process_request("Add dark mode", context)

    # Post to GitHub
    poster = GitHubPoster()
    issue_number = poster.post_issue(issue, confirm=False)

    print(f"Success! Issue #{issue_number} created")

except ValueError as e:
    print(f"Configuration error: {e}")
except RuntimeError as e:
    print(f"GitHub CLI error: {e}")
except Exception as e:
    print(f"Processing error: {e}")
```

---

## Complete Usage Example

```python
import asyncio
from app.server.core.nl_processor import process_request
from app.server.core.project_detector import detect_project_context
from app.server.core.github_poster import GitHubPoster

async def main():
    # Step 1: Detect project context
    project_path = "/path/to/my-react-app"
    context = detect_project_context(project_path)

    print(f"Detected: {context.framework} project")
    print(f"Complexity: {context.complexity}")

    # Step 2: Process natural language request
    nl_input = "Add dark mode toggle to the settings page with localStorage persistence"
    issue = await process_request(nl_input, context)

    print(f"\nGenerated Issue:")
    print(f"Title: {issue.title}")
    print(f"Type: {issue.classification}")
    print(f"Workflow: {issue.workflow} model_set {issue.model_set}")
    print(f"Labels: {', '.join(issue.labels)}")

    # Step 3: Post to GitHub (with confirmation)
    poster = GitHubPoster()
    try:
        issue_number = poster.post_issue(issue, confirm=True)
        print(f"\n✓ Issue #{issue_number} created successfully!")
    except RuntimeError as e:
        print(f"\n✗ Failed to post issue: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## API Rate Limits

### Anthropic Claude API

- **Rate Limit:** Varies by API tier
- **Retry Strategy:** Implement exponential backoff for 429 responses
- **Best Practice:** Cache intent analysis results when possible

### GitHub CLI

- **Rate Limit:** 5000 requests/hour for authenticated users
- **Best Practice:** Use `gh auth status` to verify authentication before posting

---

## Testing

All modules include comprehensive test suites with mocked dependencies:

```bash
# Run all NL processing tests
uv run pytest app/server/tests/core/test_nl_processor.py -v
uv run pytest app/server/tests/core/test_issue_formatter.py -v
uv run pytest app/server/tests/core/test_project_detector.py -v
uv run pytest app/server/tests/core/test_github_poster.py -v

# Run integration tests
uv run pytest app/server/tests/test_nl_workflow_integration.py -v
```

See test files for detailed examples of mocking and fixture usage.
