# Feature: Natural Language Processing & Issue Formatter

## Metadata
issue_number: `7`
adw_id: `902b35e6`
issue_json: `{"number":7,"title":"2-nl-processing","body":"# 🎯 ISSUE 2: tac-webbuilder - Natural Language Processing & Issue Formatter\n\n## Overview\nImplement the core natural language processing system that converts user requests into formatted GitHub issues.\n\n## Project Location\n**Working Directory**: `/Users/Warmonger0/tac/tac-webbuilder`\n\nAll file paths in this issue are relative to this directory.\n\n## Dependencies\n**Requires**: Issue 1 (Project Foundation) to be completed\n\n## Tasks\n\n### 1. Natural Language Processor\n**File**: `core/nl_processor.py`\n\n**Purpose**: Convert natural language → structured GitHub issues using Claude API\n\n**Key Functions**:\n```python\ndef process_request(\n    nl_input: str,\n    project_context: ProjectContext\n) -> GitHubIssue:\n    \"\"\"\n    Use Claude API to:\n    1. Analyze user intent\n    2. Extract requirements\n    3. Determine issue type (/feature, /bug, /chore)\n    4. Suggest appropriate ADW workflow\n    5. Return structured GitHubIssue object\n    \"\"\"\n\nasync def analyze_intent(nl_input: str) -> dict:\n    \"\"\"Use Claude to understand what user wants to build.\"\"\"\n\ndef extract_requirements(nl_input: str, intent: dict) -> list[str]:\n    \"\"\"Extract technical requirements from request.\"\"\"\n```\n\n### 2. Issue Formatter\n**File**: `core/issue_formatter.py`\n\n**Purpose**: Format GitHub issues with ADW triggers\n\n**Templates**:\n```python\nISSUE_TEMPLATES = {\n    \"feature\": \"\"\"# {title}\n\n## Description\n{description}\n\n## Requirements\n{requirements}\n\n## Technical Approach\n{technical_approach}\n\n## Workflow\n{adw_workflow} {model_set}\n\"\"\",\n\n    \"bug\": \"\"\"# {title}\n\n## Issue Description\n{description}\n\n## Steps to Reproduce\n{steps}\n\n## Expected vs Actual Behavior\n...\n\n## Workflow\nadw_plan_build_test_iso model_set base\n\"\"\",\n}\n```\n\n### 3. Project Detector\n**File**: `core/project_detector.py`\n\n**Purpose**: Analyze project context (new vs existing, framework, stack)\n\n**Key Functions**:\n```python\ndef detect_project_context(path: str) -> ProjectContext:\n    \"\"\"\n    Detect:\n    - Is new project or existing codebase?\n    - Framework (React, Next.js, Vue, etc.)\n    - Backend (FastAPI, Express, etc.)\n    - Build tools, package managers\n    - Git status\n    \"\"\"\n\ndef suggest_workflow(context: ProjectContext) -> str:\n    \"\"\"Recommend ADW workflow based on complexity.\"\"\"\n```\n\n### 4. GitHub Poster\n**File**: `core/github_poster.py`\n\n**Purpose**: Post issues to GitHub with optional confirmation\n\n**Key Functions**:\n```python\nclass GitHubPoster:\n    def post_issue(\n        self,\n        issue: GitHubIssue,\n        confirm: bool = True\n    ) -> int:\n        \"\"\"\n        Post issue via gh CLI.\n        Show preview if confirm=True.\n        Return issue number.\n        \"\"\"\n\n    def format_preview(self, issue: GitHubIssue) -> str:\n        \"\"\"Format issue for terminal display.\"\"\"\n```\n\n### 5. Data Models\n**File**: `core/data_models.py`\n\n```python\nfrom pydantic import BaseModel\n\nclass GitHubIssue(BaseModel):\n    title: str\n    body: str\n    labels: list[str]\n    classification: str  # /feature, /bug, /chore\n    workflow: str        # adw_sdlc_iso, etc.\n    model_set: str       # base or heavy\n\nclass ProjectContext(BaseModel):\n    path: str\n    is_new_project: bool\n    framework: str | None\n    backend: str | None\n    complexity: str      # low, medium, high\n```\n\n## Dependencies (Python)\nAdd to `pyproject.toml`:\n```toml\nanthropic = \"^0.40.0\"\npydantic = \"^2.0.0\"\nrich = \"^13.0.0\"\n```\n\n## Test Cases\nCreate `tests/core/test_nl_processor.py`:\n```python\ndef test_process_simple_feature_request():\n    \"\"\"Test: 'Add dark mode' → feature issue\"\"\"\n\ndef test_process_bug_report():\n    \"\"\"Test: 'Login button not working' → bug issue\"\"\"\n\ndef test_detect_new_project():\n    \"\"\"Test empty directory → is_new_project=True\"\"\"\n\ndef test_detect_react_project():\n    \"\"\"Test existing React app → framework='react-vite'\"\"\"\n```\n\n## Success Criteria\n- ✅ NL processor converts requests to structured issues\n- ✅ Issue formatter creates well-formatted GitHub markdown\n- ✅ Project detector identifies framework and context\n- ✅ GitHub poster can preview and post issues\n- ✅ All tests pass\n\n## Next Issues\nAfter this completes, create in parallel:\n- **Issue 3**: CLI Interface\n- **Issue 4**: Web UI - Backend API\n\n## Workflow\n```\nadw_plan_build_test_iso model_set heavy\n```\n\n## Labels\n`core-feature`, `natural-language`, `webbuilder`\n"}`

## Feature Description
This feature implements a comprehensive Natural Language Processing (NLP) system integrated with GitHub issue formatting capabilities. The system will convert natural language user requests into well-structured GitHub issues, automatically classify them by type (feature/bug/chore), detect project context, and suggest appropriate AI Developer Workflow (ADW) processes. This forms the core intelligence layer that bridges human intent with automated development workflows.

## User Story
As a developer or project manager
I want to describe what I need to build in natural language
So that the system can automatically create structured GitHub issues with proper ADW workflows

## Problem Statement
Currently, creating well-structured GitHub issues requires manual formatting, understanding of ADW workflows, and technical knowledge to properly classify issues. This creates friction in the development process and requires developers to context-switch from thinking about problems to formatting issues. Additionally, choosing the correct ADW workflow and model set requires understanding of project complexity that may not be immediately apparent.

## Solution Statement
We will implement an intelligent NLP system using the Anthropic Claude API that analyzes natural language input, understands user intent, extracts technical requirements, and automatically generates properly formatted GitHub issues. The system will detect project context (framework, stack, complexity) to suggest appropriate ADW workflows and model sets. This solution leverages existing patterns from the current codebase's LLM integration while extending it to handle issue generation rather than SQL queries.

## Relevant Files
Use these files to implement the feature:

- `README.md` - Project overview and structure understanding
- `app/server/core/data_models.py` - Existing Pydantic model patterns to follow for new data models
- `app/server/core/llm_processor.py` - Reference for Anthropic API integration patterns
- `app/server/server.py` - FastAPI server patterns and API endpoint structure
- `app/server/pyproject.toml` - For adding new dependencies
- `adws/adw_modules/data_types.py` - Understanding ADW data structures
- `adws/adw_modules/github.py` - Reference for GitHub integration
- `.claude/commands/test_e2e.md` - E2E test runner documentation
- `.claude/commands/e2e/test_basic_query.md` - E2E test example

### New Files
- `app/server/core/nl_processor.py` - Natural language processing engine
- `app/server/core/issue_formatter.py` - Issue template formatting system
- `app/server/core/project_detector.py` - Project context detection
- `app/server/core/github_poster.py` - GitHub issue posting integration
- `app/server/core/webbuilder_models.py` - WebBuilder-specific data models
- `app/server/tests/core/test_nl_processor.py` - NL processor tests
- `app/server/tests/core/test_issue_formatter.py` - Issue formatter tests
- `app/server/tests/core/test_project_detector.py` - Project detector tests
- `app/server/tests/core/test_github_poster.py` - GitHub poster tests
- `app/client/src/components/IssueBuilder.tsx` - UI component for issue building
- `app/client/src/api/webbuilder.ts` - API client for WebBuilder endpoints
- `.claude/commands/e2e/test_nl_issue_generation.md` - E2E test for NL issue generation

## Implementation Plan
### Phase 1: Foundation
Set up the core data models and dependencies needed for the NLP system. This includes installing required packages, creating Pydantic models for type safety, and establishing the basic structure for all modules.

### Phase 2: Core Implementation
Implement the main NLP processing logic using Anthropic's Claude API, create issue formatting templates, develop project context detection algorithms, and build the GitHub integration layer. Each component will be built independently with clear interfaces for integration.

### Phase 3: Integration
Connect the NLP system to the existing FastAPI backend, create new API endpoints for issue generation, implement frontend components for user interaction, and ensure all components work together seamlessly with proper error handling and validation.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update Dependencies
- Navigate to `app/server` directory
- Add required dependencies to `pyproject.toml`:
  - `anthropic` (already present, verify version)
  - `pydantic` (verify version 2.0+)
  - `rich==13.0.0` for terminal formatting
- Run `uv sync --all-extras` to install dependencies
- Verify installation by importing packages in Python

### 2. Create WebBuilder Data Models
- Create `app/server/core/webbuilder_models.py`
- Define `GitHubIssue` Pydantic model with all required fields
- Define `ProjectContext` model for project detection
- Define `NLProcessingRequest` and `NLProcessingResponse` models
- Add proper type hints and validation
- Import and test models in Python REPL

### 3. Implement Natural Language Processor
- Create `app/server/core/nl_processor.py`
- Implement `analyze_intent()` function using Anthropic API
- Create prompt templates for intent analysis
- Implement `extract_requirements()` to parse technical requirements
- Implement `determine_issue_type()` for classification
- Implement main `process_request()` function
- Add comprehensive error handling and logging

### 4. Create Issue Formatter Module
- Create `app/server/core/issue_formatter.py`
- Define issue templates for feature, bug, and chore types
- Implement `format_issue()` function with template substitution
- Add markdown formatting utilities
- Implement `suggest_adw_workflow()` based on complexity
- Create preview formatting for terminal display

### 5. Develop Project Detector
- Create `app/server/core/project_detector.py`
- Implement file system scanning for project detection
- Add framework detection (React, Vue, Next.js, etc.)
- Add backend detection (FastAPI, Express, etc.)
- Implement `detect_project_context()` main function
- Add complexity scoring algorithm
- Create workflow suggestion logic

### 6. Build GitHub Poster Integration
- Create `app/server/core/github_poster.py`
- Implement `GitHubPoster` class
- Add `post_issue()` method using subprocess for gh CLI
- Implement `format_preview()` for terminal display
- Add confirmation prompt functionality
- Add error handling for gh CLI failures
- Implement issue number extraction from response

### 7. Create API Endpoints
- Update `app/server/server.py` with new endpoints
- Add `POST /api/webbuilder/process` endpoint
- Add `POST /api/webbuilder/preview` endpoint
- Add `GET /api/webbuilder/context` endpoint
- Implement request/response handling
- Add proper error responses and status codes

### 8. Write Unit Tests for NL Processor
- Create `app/server/tests/core/test_nl_processor.py`
- Write test for simple feature request processing
- Write test for bug report processing
- Write test for ambiguous input handling
- Add tests for error conditions
- Mock Anthropic API calls for testing

### 9. Write Unit Tests for Other Modules
- Create `app/server/tests/core/test_issue_formatter.py`
- Create `app/server/tests/core/test_project_detector.py`
- Create `app/server/tests/core/test_github_poster.py`
- Write comprehensive test coverage for each module
- Test edge cases and error conditions

### 10. Create Frontend API Client
- Create `app/client/src/api/webbuilder.ts`
- Define TypeScript interfaces matching backend models
- Implement API client functions for all endpoints
- Add proper error handling and type safety
- Export functions for component use

### 11. Build Issue Builder UI Component
- Create `app/client/src/components/IssueBuilder.tsx`
- Design input interface for natural language requests
- Add project context display
- Implement issue preview functionality
- Add confirmation and submission UI
- Style with existing CSS patterns

### 12. Integrate UI Component
- Update main application to include IssueBuilder
- Add routing or modal for issue builder
- Connect to API client
- Implement state management
- Add loading and error states

### 13. Create E2E Test for NL Issue Generation
- Create `.claude/commands/e2e/test_nl_issue_generation.md`
- Define user story for NL to issue conversion
- Write step-by-step test procedure
- Include verification points for all functionality
- Add screenshot capture requirements
- Define success criteria

### 14. Run Validation Commands
- Run server tests: `cd app/server && uv run pytest`
- Check TypeScript compilation: `cd app/client && bun tsc --noEmit`
- Build frontend: `cd app/client && bun run build`
- Execute E2E test using test runner
- Verify all tests pass with zero regressions

## Testing Strategy
### Unit Tests
- Test NL processor with various input types (features, bugs, questions)
- Test issue formatter with different templates and data
- Test project detector with mock file systems
- Test GitHub poster with mocked gh CLI calls
- Test API endpoints with mock services
- Test error handling and edge cases

### Edge Cases
- Empty or null natural language input
- Extremely long input text (>10000 characters)
- Unsupported languages or gibberish input
- Project directories without clear framework
- Mixed project types (multiple frameworks)
- GitHub CLI not installed or not authenticated
- API rate limiting from Anthropic
- Network failures during API calls
- Malformed project structures
- Concurrent request handling

## Acceptance Criteria
- Natural language input successfully converts to structured GitHub issues
- Issue type classification achieves >90% accuracy for clear inputs
- Project context detection correctly identifies major frameworks
- ADW workflow suggestions match project complexity
- GitHub issues post successfully via gh CLI
- Preview functionality displays formatted issues correctly
- All API endpoints return proper status codes and error messages
- Frontend UI provides smooth user experience with loading states
- All unit tests pass with 100% success rate
- E2E test validates complete flow from input to issue creation
- System handles errors gracefully without crashes
- Performance: NL processing completes in <5 seconds

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- `cd app/server && uv run pytest -v tests/core/test_nl_processor.py` - Test NL processor functionality
- `cd app/server && uv run pytest -v tests/core/test_issue_formatter.py` - Test issue formatting
- `cd app/server && uv run pytest -v tests/core/test_project_detector.py` - Test project detection
- `cd app/server && uv run pytest -v tests/core/test_github_poster.py` - Test GitHub integration
- `cd app/server && uv run pytest` - Run all server tests to validate no regressions
- `cd app/client && bun tsc --noEmit` - Validate TypeScript compilation
- `cd app/client && bun run build` - Validate frontend builds successfully
- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_nl_issue_generation.md` to validate the NL to issue generation flow works end-to-end

## Notes
- The Anthropic API key must be properly configured in the environment variables
- This implementation uses similar patterns to the existing LLM processor for consistency
- The rich library is used for terminal formatting to provide better user experience in CLI mode
- The GitHub CLI (gh) must be installed and authenticated for issue posting to work
- Consider implementing caching for project context detection to improve performance on repeated calls
- The system is designed to be extensible for future issue types beyond feature/bug/chore
- Rate limiting should be considered for production deployment to manage API costs
- Future enhancement: Add support for batch processing multiple issues
- Consider adding webhook support for automated issue creation triggers