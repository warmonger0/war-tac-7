# Feature: Natural Language Processing & Issue Formatter

## Metadata
issue_number: `14`
adw_id: `e2bbe1a5`
issue_json: `{"number":14,"title":"Foundation: natural language processing","body":"# 🎯 ISSUE 2: tac-webbuilder - Natural Language Processing & Issue Formatter\n\n## Overview\nImplement the core natural language processing system that converts user requests into formatted GitHub issues.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory.\n\n## Dependencies\n**Requires**: Issue 1 (Project Foundation) to be completed\n\n## Tasks\n\n### 1. Natural Language Processor\n**File**: `core/nl_processor.py`\n\n**Purpose**: Convert natural language → structured GitHub issues using Claude API\n\n**Key Functions**:\n```python\ndef process_request(\n    nl_input: str,\n    project_context: ProjectContext\n) -> GitHubIssue:\n    \"\"\"\n    Use Claude API to:\n    1. Analyze user intent\n    2. Extract requirements\n    3. Determine issue type (/feature, /bug, /chore)\n    4. Suggest appropriate ADW workflow\n    5. Return structured GitHubIssue object\n    \"\"\"\n\nasync def analyze_intent(nl_input: str) -> dict:\n    \"\"\"Use Claude to understand what user wants to build.\"\"\"\n\ndef extract_requirements(nl_input: str, intent: dict) -> list[str]:\n    \"\"\"Extract technical requirements from request.\"\"\"\n```\n\n### 2. Issue Formatter\n**File**: `core/issue_formatter.py`\n\n**Purpose**: Format GitHub issues with ADW triggers\n\n**Templates**:\n```python\nISSUE_TEMPLATES = {\n    \"feature\": \"\"\"# {title}\n\n## Description\n{description}\n\n## Requirements\n{requirements}\n\n## Technical Approach\n{technical_approach}\n\n## Workflow\n{adw_workflow} {model_set}\n\"\"\",\n\n    \"bug\": \"\"\"# {title}\n\n## Issue Description\n{description}\n\n## Steps to Reproduce\n{steps}\n\n## Expected vs Actual Behavior\n...\n\n## Workflow\nadw_plan_build_test_iso model_set base\n\"\"\",\n}\n```\n\n### 3. Project Detector\n**File**: `core/project_detector.py`\n\n**Purpose**: Analyze project context (new vs existing, framework, stack)\n\n**Key Functions**:\n```python\ndef detect_project_context(path: str) -> ProjectContext:\n    \"\"\"\n    Detect:\n    - Is new project or existing codebase?\n    - Framework (React, Next.js, Vue, etc.)\n    - Backend (FastAPI, Express, etc.)\n    - Build tools, package managers\n    - Git status\n    \"\"\"\n\ndef suggest_workflow(context: ProjectContext) -> str:\n    \"\"\"Recommend ADW workflow based on complexity.\"\"\"\n```\n\n### 4. GitHub Poster\n**File**: `core/github_poster.py`\n\n**Purpose**: Post issues to GitHub with optional confirmation\n\n**Key Functions**:\n```python\nclass GitHubPoster:\n    def post_issue(\n        self,\n        issue: GitHubIssue,\n        confirm: bool = True\n    ) -> int:\n        \"\"\"\n        Post issue via gh CLI.\n        Show preview if confirm=True.\n        Return issue number.\n        \"\"\"\n\n    def format_preview(self, issue: GitHubIssue) -> str:\n        \"\"\"Format issue for terminal display.\"\"\"\n```\n\n### 5. Data Models\n**File**: `core/data_models.py`\n\n```python\nfrom pydantic import BaseModel\n\nclass GitHubIssue(BaseModel):\n    title: str\n    body: str\n    labels: list[str]\n    classification: str  # /feature, /bug, /chore\n    workflow: str        # adw_sdlc_iso, etc.\n    model_set: str       # base or heavy\n\nclass ProjectContext(BaseModel):\n    path: str\n    is_new_project: bool\n    framework: str | None\n    backend: str | None\n    complexity: str      # low, medium, high\n```\n\n## Dependencies (Python)\nAdd to `pyproject.toml`:\n```toml\nanthropic = \"^0.40.0\"\npydantic = \"^2.0.0\"\nrich = \"^13.0.0\"\n```\n\n## Test Cases\nCreate `tests/core/test_nl_processor.py`:\n```python\ndef test_process_simple_feature_request():\n    \"\"\"Test: 'Add dark mode' → feature issue\"\"\"\n\ndef test_process_bug_report():\n    \"\"\"Test: 'Login button not working' → bug issue\"\"\"\n\ndef test_detect_new_project():\n    \"\"\"Test empty directory → is_new_project=True\"\"\"\n\ndef test_detect_react_project():\n    \"\"\"Test existing React app → framework='react-vite'\"\"\"\n```\n\n## Success Criteria\n- ✅ NL processor converts requests to structured issues\n- ✅ Issue formatter creates well-formatted GitHub markdown\n- ✅ Project detector identifies framework and context\n- ✅ GitHub poster can preview and post issues\n- ✅ All tests pass\n\n## Next Issues\nAfter this completes, create in parallel:\n- **Issue 3**: CLI Interface\n- **Issue 4**: Web UI - Backend API\n\n## Workflow\n```\nadw_plan_build_test_iso model_set heavy\n```\n\n## Labels\n`core-feature`, `natural-language`, `webbuilder`\n"}`

## Feature Description
Implement a comprehensive natural language processing system that converts user requests (like "Add dark mode" or "Fix login button") into structured, well-formatted GitHub issues with appropriate ADW workflow triggers. The system analyzes user intent, determines issue type (feature/bug/chore), detects project context (framework, tech stack, complexity), and generates formatted GitHub issues that can be posted directly via the GitHub CLI. This feature extends the existing NL-to-SQL application by adding capabilities to create development workflow automation.

## User Story
As a developer
I want to convert natural language requests into structured GitHub issues
So that I can quickly create actionable, well-formatted issues with appropriate ADW workflows without manually writing all the boilerplate

## Problem Statement
Creating well-structured GitHub issues with appropriate ADW workflow triggers requires significant manual effort and domain knowledge. Developers need to understand the project context, classify the issue type, determine complexity, suggest appropriate workflows, and format everything consistently. This is time-consuming and error-prone, especially for new team members or when working across multiple projects with different conventions.

## Solution Statement
Build a natural language processing system that leverages Claude API to automatically analyze user requests, extract requirements, classify issues, detect project context, and generate properly formatted GitHub issues with ADW workflow triggers. The system will follow existing patterns from the codebase's LLM integration (similar to core/llm_processor.py) and extend the data models to support GitHub issue generation workflows.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/data_models.py** - Already contains Pydantic BaseModel patterns; will be extended with GitHubIssue and ProjectContext models
- **app/server/core/llm_processor.py** - Contains existing LLM integration patterns with OpenAI and Anthropic; provides template for nl_processor.py
- **app/server/pyproject.toml** - Dependency management; needs updates for pydantic and rich libraries
- **app/server/tests/core/test_llm_processor.py** - Testing patterns with mocking LLM providers; template for new tests
- **README.md** - Project documentation; will need updates for new features

### New Files

The following new files will be created:

- **app/server/core/nl_processor.py** - Core natural language processing module for converting user requests to structured GitHub issues using Claude API
- **app/server/core/issue_formatter.py** - Issue template system and formatting logic for different issue types (feature/bug/chore)
- **app/server/core/project_detector.py** - Project context detection (framework, tech stack, complexity analysis)
- **app/server/core/github_poster.py** - GitHub CLI integration for posting issues with preview and confirmation
- **app/server/tests/core/test_nl_processor.py** - Unit tests for NL processor with mocked LLM calls
- **app/server/tests/core/test_issue_formatter.py** - Unit tests for issue formatting templates
- **app/server/tests/core/test_project_detector.py** - Unit tests for project context detection
- **app/server/tests/core/test_github_poster.py** - Unit tests for GitHub CLI integration

## Implementation Plan

### Phase 1: Foundation
Extend the existing data models and set up dependencies to support GitHub issue generation. This phase prepares the foundation by adding new Pydantic models for GitHubIssue and ProjectContext, and ensuring all required libraries (anthropic, pydantic, rich) are available. The existing codebase already has anthropic and pydantic, but we need to verify versions and add rich for terminal formatting.

### Phase 2: Core Implementation
Implement the four core processing modules: nl_processor (intent analysis and requirement extraction), issue_formatter (template-based formatting), project_detector (framework and complexity detection), and github_poster (CLI integration). Each module follows existing patterns from the codebase and integrates with the Claude API for intelligent analysis.

### Phase 3: Integration
Add comprehensive test coverage following the existing test patterns (see tests/core/test_llm_processor.py), integrate with the existing FastAPI server if needed for web-based access, and update documentation. Tests will mock LLM providers and verify core functionality without requiring live API calls.

## Step by Step Tasks

### 1. Extend Data Models
- Read `app/server/core/data_models.py` to understand existing patterns
- Add `GitHubIssue` model with fields: title, body, labels, classification, workflow, model_set
- Add `ProjectContext` model with fields: path, is_new_project, framework, backend, complexity
- Add `NLProcessRequest` model with fields: nl_input, project_path (optional)
- Add `NLProcessResponse` model with fields: github_issue, project_context, error (optional)

### 2. Update Dependencies
- Read `app/server/pyproject.toml` to check existing dependencies
- Verify anthropic version is >= 0.40.0 (currently 0.54.0, no change needed)
- Verify pydantic version is >= 2.0.0 (no version specified, check current)
- Add `rich = "^13.0.0"` to dependencies array if not present
- Run `cd app/server && uv sync --all-extras` to install dependencies

### 3. Implement Natural Language Processor (core/nl_processor.py)
- Create `app/server/core/nl_processor.py` following patterns from `core/llm_processor.py`
- Implement `analyze_intent(nl_input: str) -> dict` using Claude API to extract user intent
- Implement `extract_requirements(nl_input: str, intent: dict) -> list[str]` to pull out technical requirements
- Implement `classify_issue_type(intent: dict) -> str` to determine /feature, /bug, or /chore
- Implement `suggest_adw_workflow(issue_type: str, complexity: str) -> tuple[str, str]` to recommend workflow and model_set
- Implement main `process_request(nl_input: str, project_context: ProjectContext) -> GitHubIssue` that orchestrates the above functions
- Include error handling patterns similar to llm_processor.py
- Use environment variable `ANTHROPIC_API_KEY` for API access

### 4. Implement Issue Formatter (core/issue_formatter.py)
- Create `app/server/core/issue_formatter.py`
- Define `ISSUE_TEMPLATES` dictionary with templates for feature, bug, and chore
- Implement `format_issue(issue: GitHubIssue, template_data: dict) -> str` to populate templates
- Implement `validate_issue_body(body: str) -> bool` to ensure required sections are present
- Add helper functions for formatting requirements, technical approach, and workflow sections
- Include Markdown formatting utilities for consistent output

### 5. Implement Project Detector (core/project_detector.py)
- Create `app/server/core/project_detector.py`
- Implement `detect_project_context(path: str) -> ProjectContext` that analyzes:
  - Check if directory is empty (is_new_project)
  - Detect framework by checking for package.json, requirements.txt, pyproject.toml, etc.
  - Identify specific frameworks (React, Next.js, Vue, FastAPI, Express) by analyzing config files
  - Detect build tools (vite, webpack, rollup) and package managers (npm, yarn, bun, uv)
  - Check git status (initialized, uncommitted changes, etc.)
- Implement `suggest_workflow(context: ProjectContext) -> str` to recommend ADW workflow based on complexity
- Implement `calculate_complexity(context: ProjectContext) -> str` (low/medium/high) based on project size and structure
- Add caching mechanism to avoid redundant file system scans

### 6. Implement GitHub Poster (core/github_poster.py)
- Create `app/server/core/github_poster.py`
- Implement `GitHubPoster` class with methods:
  - `__init__(repo_url: str)` to initialize with repository URL
  - `format_preview(issue: GitHubIssue) -> str` to create rich terminal preview using the rich library
  - `post_issue(issue: GitHubIssue, confirm: bool = True) -> int` to post via `gh issue create` CLI command
  - `_execute_gh_command(cmd: list[str]) -> str` helper for running gh CLI commands
  - `_validate_gh_cli() -> bool` to check if gh CLI is installed and authenticated
- Use `subprocess` module for CLI interaction
- Add error handling for CLI failures and authentication issues

### 7. Create Unit Tests for NL Processor
- Create `app/server/tests/core/test_nl_processor.py` following patterns from `test_llm_processor.py`
- Test `analyze_intent()` with mocked Claude API responses
- Test `extract_requirements()` with various NL inputs
- Test `classify_issue_type()` for feature, bug, and chore detection
- Test `suggest_adw_workflow()` for different complexity levels
- Test `process_request()` end-to-end with mocked dependencies
- Test error handling when API key is missing
- Test error handling when Claude API fails
- Mock Anthropic API calls using `unittest.mock.patch`

### 8. Create Unit Tests for Issue Formatter
- Create `app/server/tests/core/test_issue_formatter.py`
- Test template formatting for all issue types (feature, bug, chore)
- Test `validate_issue_body()` with valid and invalid bodies
- Test Markdown formatting helpers
- Test edge cases with missing or empty fields
- Test template substitution with special characters

### 9. Create Unit Tests for Project Detector
- Create `app/server/tests/core/test_project_detector.py`
- Test `detect_project_context()` with various project structures:
  - Empty directory (new project)
  - React + Vite project
  - FastAPI project
  - Next.js project
  - Existing natural language SQL interface (current project)
- Test `suggest_workflow()` with different complexity levels
- Test `calculate_complexity()` with small, medium, and large projects
- Use `pytest.fixture` to create temporary test directories with sample project files
- Test git status detection

### 10. Create Unit Tests for GitHub Poster
- Create `app/server/tests/core/test_github_poster.py`
- Test `format_preview()` output formatting
- Test `post_issue()` with mocked `gh` CLI calls
- Test `_validate_gh_cli()` with both installed and missing CLI
- Test error handling for authentication failures
- Test confirmation workflow (accept/reject)
- Mock subprocess calls using `unittest.mock.patch`

### 11. Integration Testing
- Create `app/server/tests/test_nl_workflow_integration.py` for end-to-end testing
- Test full workflow: NL input → intent analysis → project detection → issue formatting → (optionally) GitHub posting
- Test with real project directory paths (use test fixtures)
- Test error propagation through the entire workflow
- Verify that all components work together correctly

### 12. Documentation Updates
- Update `README.md` with new features:
  - Add "NL to GitHub Issue" section
  - Document required environment variables (ANTHROPIC_API_KEY, GITHUB_REPO_URL)
  - Add usage examples for each module
  - Document GitHub CLI setup requirements
- Create docstrings for all public functions and classes
- Add inline comments for complex logic
- Document ADW workflow recommendations and model_set options

### 13. Run All Validation Commands
- Execute all validation commands listed below to ensure zero regressions
- Fix any failing tests or build errors
- Verify all new functionality works as expected

## Testing Strategy

### Unit Tests
1. **NL Processor Tests** (`test_nl_processor.py`):
   - Mock Claude API responses to test intent analysis without live API calls
   - Test classification accuracy for different input types
   - Test requirement extraction with various natural language patterns
   - Test workflow suggestion logic with different complexity scenarios

2. **Issue Formatter Tests** (`test_issue_formatter.py`):
   - Test template rendering with complete and partial data
   - Test Markdown formatting edge cases
   - Test validation logic for required sections
   - Test special character handling in titles and bodies

3. **Project Detector Tests** (`test_project_detector.py`):
   - Create temporary test directories with sample project structures
   - Test detection accuracy for major frameworks (React, Vue, Next.js, FastAPI)
   - Test complexity calculation with different project sizes
   - Test git status detection with various repository states

4. **GitHub Poster Tests** (`test_github_poster.py`):
   - Mock subprocess calls to test CLI integration without actual GitHub API calls
   - Test preview formatting with rich library
   - Test confirmation workflow logic
   - Test error handling for missing CLI or authentication failures

5. **Integration Tests** (`test_nl_workflow_integration.py`):
   - Test complete workflow from NL input to formatted issue
   - Test error propagation between components
   - Test with real project structures (fixtures)
   - Verify consistent behavior across different scenarios

### Edge Cases
1. **Invalid NL Input**:
   - Empty strings
   - Very long inputs (> 10,000 characters)
   - Inputs with special characters, emojis, or code snippets
   - Ambiguous requests that could be interpreted multiple ways

2. **Project Detection Edge Cases**:
   - Non-existent directories
   - Directories without read permissions
   - Mixed-framework projects (e.g., React frontend + FastAPI backend)
   - Projects without package manager files

3. **API Failures**:
   - Network timeouts
   - Rate limiting responses
   - Invalid API keys
   - Malformed API responses

4. **GitHub CLI Edge Cases**:
   - CLI not installed
   - Authentication failures
   - Repository not found
   - Network failures during issue creation

5. **Template Formatting Edge Cases**:
   - Missing required fields
   - Fields with Markdown-breaking characters
   - Very long requirement lists
   - Empty technical approach sections

## Acceptance Criteria
- [ ] NL processor successfully converts natural language requests like "Add dark mode" into structured GitHubIssue objects with appropriate title, body, labels, classification, workflow, and model_set
- [ ] Issue formatter generates well-formatted GitHub markdown with all required sections (Description, Requirements, Technical Approach, Workflow) for feature, bug, and chore templates
- [ ] Project detector accurately identifies project type (new vs existing), framework (React, Next.js, Vue, FastAPI, etc.), backend, build tools, and calculates complexity (low/medium/high)
- [ ] GitHub poster validates gh CLI installation, generates rich terminal preview, and successfully posts issues (with optional confirmation) returning the issue number
- [ ] All unit tests pass with 100% success rate (4 test files, ~40+ test cases)
- [ ] Integration tests verify end-to-end workflow from NL input to formatted issue
- [ ] No regressions in existing functionality (all existing tests pass)
- [ ] Code follows existing patterns from core/llm_processor.py and core/data_models.py
- [ ] All dependencies are properly declared in pyproject.toml and install without errors
- [ ] Documentation is complete with usage examples, API documentation, and setup instructions

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest tests/core/test_nl_processor.py -v` - Run NL processor tests to validate intent analysis and classification
- `cd app/server && uv run pytest tests/core/test_issue_formatter.py -v` - Run issue formatter tests to validate template rendering
- `cd app/server && uv run pytest tests/core/test_project_detector.py -v` - Run project detector tests to validate context detection
- `cd app/server && uv run pytest tests/core/test_github_poster.py -v` - Run GitHub poster tests to validate CLI integration
- `cd app/server && uv run pytest tests/test_nl_workflow_integration.py -v` - Run integration tests to validate end-to-end workflow
- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate no breaking changes
- `python -c "from app.server.core.nl_processor import process_request; print('✓ NL Processor import successful')"` - Verify module imports
- `python -c "from app.server.core.issue_formatter import format_issue; print('✓ Issue Formatter import successful')"` - Verify module imports
- `python -c "from app.server.core.project_detector import detect_project_context; print('✓ Project Detector import successful')"` - Verify module imports
- `python -c "from app.server.core.github_poster import GitHubPoster; print('✓ GitHub Poster import successful')"` - Verify module imports

## Notes

### Implementation Considerations
1. **Reuse Existing Patterns**: The codebase already has excellent patterns for LLM integration in `core/llm_processor.py`. Follow the same structure for API client initialization, error handling, and markdown cleanup.

2. **API Provider Priority**: Like `llm_processor.py`, implement provider priority (OpenAI first, then Anthropic fallback) if needed. For this feature, we're focusing on Anthropic/Claude since the issue specifically requests Claude API, but the architecture should support extension.

3. **Environment Variable Requirements**:
   - `ANTHROPIC_API_KEY` - Required for Claude API access
   - `GITHUB_REPO_URL` - Optional, for GitHub poster (defaults to current repo)
   - `OPENAI_API_KEY` - Optional, if OpenAI fallback is implemented

4. **GitHub CLI Setup**: The GitHub poster requires `gh` CLI to be installed and authenticated. Include clear error messages and validation checks to guide users through setup.

5. **Project Detection Limitations**: Project detector uses heuristics (file patterns) which may not be 100% accurate for all projects. Document known limitations and allow for manual override via `ProjectContext` constructor.

6. **ADW Workflow Recommendations**: The workflow suggestion logic should follow these patterns:
   - Simple features (low complexity) → `adw_sdlc_iso model_set base`
   - Complex features (high complexity) → `adw_plan_build_test_iso model_set heavy`
   - Bugs → `adw_plan_build_test_iso model_set base`
   - Chores → `adw_sdlc_iso model_set base`

7. **Testing Strategy**: All tests should mock external dependencies (Claude API, GitHub CLI) to ensure fast, deterministic test execution. Use `pytest.fixture` for creating test data and temporary directories.

8. **Future Extensibility**: This foundation can be extended in future issues:
   - Issue 3: CLI Interface - Add command-line tool for easy access
   - Issue 4: Web UI Backend API - Add FastAPI endpoints for web-based access
   - Issue 5: Frontend Integration - Build React UI for the NL-to-issue workflow

9. **Dependencies Already Satisfied**: The pyproject.toml shows anthropic (0.54.0) and pydantic are already installed. Only need to add `rich` for terminal formatting in the GitHub poster preview feature.

10. **Relationship to Existing Features**: This feature is orthogonal to the existing NL-to-SQL functionality. Both use similar LLM processing patterns but serve different purposes (SQL generation vs. GitHub issue generation). The shared patterns make implementation straightforward.

### Potential Challenges
- **Ambiguous NL Input**: User requests may be vague or ambiguous. The intent analysis should make reasonable assumptions and include them in the issue body for review.
- **Project Detection Accuracy**: Some projects may have unconventional structure. Provide clear error messages and fallback to generic templates when detection fails.
- **GitHub CLI Authentication**: Users may not have gh CLI set up. Provide helpful error messages with setup instructions.
- **API Rate Limits**: Claude API has rate limits. Implement exponential backoff and clear error messages for rate limit errors.

### Success Metrics
- NL processor accurately classifies 95%+ of clear feature/bug/chore requests
- Project detector identifies framework correctly for major frameworks (React, Vue, Next.js, FastAPI, Express)
- GitHub poster successfully posts issues when gh CLI is properly configured
- All tests pass with mocked dependencies (no live API calls in CI)
- Zero regressions in existing NL-to-SQL functionality
