# Natural Language Processing Usage Guide

## Introduction

The Natural Language Processing (NL Processing) system enables you to convert plain English descriptions of features, bugs, or tasks into properly formatted GitHub issues with automatic ADW (AI Developer Workflow) triggers. Instead of manually writing detailed issue descriptions, you can simply describe what you want in natural language, and the system handles the rest.

### What Can It Do?

- **Intent Analysis**: Understands whether you're describing a feature, bug, or chore
- **Requirement Extraction**: Breaks down your description into actionable technical requirements
- **Project Detection**: Analyzes your project to understand frameworks, tools, and complexity
- **Issue Generation**: Creates properly formatted GitHub issues with appropriate ADW workflows
- **GitHub Integration**: Posts issues directly to GitHub with preview and confirmation

### When to Use It

- Creating new feature requests from high-level descriptions
- Reporting bugs without manually formatting issue templates
- Generating maintenance/chore tasks for documentation, refactoring, etc.
- Automating issue creation in CI/CD pipelines
- Building custom development tools that interact with GitHub

---

## Prerequisites

### Required Software

1. **Python 3.10+**
   ```bash
   python --version  # Should be 3.10 or higher
   ```

2. **GitHub CLI (gh)**
   ```bash
   # macOS
   brew install gh

   # Linux
   sudo apt install gh

   # Windows
   choco install gh

   # Verify installation
   gh --version
   ```

3. **GitHub CLI Authentication**
   ```bash
   gh auth login
   # Follow the prompts to authenticate with your GitHub account
   ```

### Required Environment Variables

Create a `.env` file or export these variables:

```bash
# Required: Anthropic API key for Claude access
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxxxx"

# Optional: GitHub repository URL (defaults to current repo)
export GITHUB_REPO_URL="owner/repo"
```

### Verify Setup

Test that everything is configured correctly:

```bash
# Check Python version
python --version

# Check gh CLI is authenticated
gh auth status

# Check environment variables
echo $ANTHROPIC_API_KEY
```

---

## Quick Start

### Basic Usage Example

Here's the simplest way to use the NL processing system:

```python
import asyncio
from app.server.core.nl_processor import process_request
from app.server.core.project_detector import detect_project_context
from app.server.core.github_poster import GitHubPoster

async def main():
    # 1. Detect your project context
    context = detect_project_context(".")

    # 2. Process a natural language request
    issue = await process_request(
        "Add a dark mode toggle to the settings page",
        context
    )

    # 3. Post to GitHub
    poster = GitHubPoster()
    issue_number = poster.post_issue(issue, confirm=True)
    print(f"Created issue #{issue_number}")

asyncio.run(main())
```

That's it! The system will:
1. Analyze your project structure
2. Parse your natural language input
3. Generate a formatted GitHub issue
4. Show you a preview
5. Post it to GitHub after confirmation

---

## Step-by-Step Guide

### Step 1: Setting Up Environment Variables

Create a `.env` file in your project root:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Optional (defaults to current repo)
GITHUB_REPO_URL=yourusername/your-repo
```

Load the environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Verify
assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not set"
```

### Step 2: Detecting Project Context

The system needs to understand your project before generating issues:

```python
from app.server.core.project_detector import detect_project_context

# Detect context from current directory
context = detect_project_context(".")

# Or specify a path
context = detect_project_context("/path/to/your/project")

# Inspect the detected context
print(f"Framework: {context.framework}")
print(f"Backend: {context.backend}")
print(f"Complexity: {context.complexity}")
print(f"Build Tools: {', '.join(context.build_tools)}")
print(f"Package Manager: {context.package_manager}")
```

**Example Output:**
```
Framework: react-vite
Backend: None
Complexity: medium
Build Tools: vite, typescript
Package Manager: npm
```

### Step 3: Processing Natural Language Requests

Now you can convert natural language to structured issues:

```python
import asyncio
from app.server.core.nl_processor import process_request

async def process_my_request():
    # Simple feature request
    issue = await process_request(
        "Add a dark mode toggle to the settings page",
        context
    )

    # Inspect the generated issue
    print(f"Title: {issue.title}")
    print(f"Classification: {issue.classification}")
    print(f"Workflow: {issue.workflow}")
    print(f"Model Set: {issue.model_set}")
    print(f"Labels: {', '.join(issue.labels)}")
    print(f"\nBody:\n{issue.body}")

    return issue

issue = asyncio.run(process_my_request())
```

### Step 4: Previewing the Generated Issue

Before posting to GitHub, you can preview the issue:

```python
from app.server.core.github_poster import GitHubPoster

poster = GitHubPoster()

# Get formatted preview
preview = poster.format_preview(issue)
print(preview)
```

This shows a rich terminal preview with:
- Issue title
- Classification (feature/bug/chore)
- Labels
- Workflow recommendation
- Full issue body

### Step 5: Posting to GitHub

Finally, post the issue to GitHub:

```python
# Post with confirmation prompt
issue_number = poster.post_issue(issue, confirm=True)
print(f"✓ Issue #{issue_number} created")

# Or post without confirmation (for automation)
issue_number = poster.post_issue(issue, confirm=False)
```

---

## Advanced Usage

### Handling Different Project Types

#### React with Vite

```python
context = detect_project_context("/path/to/react-vite-project")
# ProjectContext(
#   framework="react-vite",
#   complexity="medium",
#   build_tools=["vite", "typescript"],
#   package_manager="npm"
# )

issue = await process_request(
    "Add authentication with JWT tokens and protected routes",
    context
)
# Recommended workflow: adw_plan_build_test_iso with base model
```

#### Next.js Application

```python
context = detect_project_context("/path/to/nextjs-app")
# ProjectContext(
#   framework="nextjs",
#   complexity="high",
#   build_tools=["typescript"],
#   package_manager="yarn"
# )

issue = await process_request(
    "Implement server-side rendering for product pages",
    context
)
# Recommended workflow: adw_plan_build_test_iso with heavy model
```

#### FastAPI Backend

```python
context = detect_project_context("/path/to/fastapi-project")
# ProjectContext(
#   backend="fastapi",
#   complexity="medium",
#   package_manager="uv"
# )

issue = await process_request(
    "Add rate limiting middleware to protect API endpoints",
    context
)
# Recommended workflow: adw_plan_build_test_iso with base model
```

#### Monorepo / Complex Projects

```python
context = detect_project_context("/path/to/monorepo")
# ProjectContext(
#   framework="react-vite",
#   backend="fastapi",
#   complexity="high",
#   build_tools=["vite", "typescript", "docker"],
#   package_manager="pnpm"
# )

issue = await process_request(
    "Add shared component library used by all frontend apps",
    context
)
# Recommended workflow: adw_plan_build_test_iso with heavy model
```

### Customizing Workflow Recommendations

You can override the automatic workflow recommendation:

```python
from app.server.core.data_models import GitHubIssue

# Process request normally
issue = await process_request("Add feature X", context)

# Override workflow and model set
issue.workflow = "adw_sdlc_zte_iso"  # Zero-test-error workflow
issue.model_set = "heavy"            # Use heavy model set

# Post with custom workflow
poster.post_issue(issue, confirm=True)
```

### Error Handling and Recovery

Implement robust error handling:

```python
import asyncio
from app.server.core.nl_processor import process_request
from app.server.core.project_detector import detect_project_context
from app.server.core.github_poster import GitHubPoster

async def safe_issue_creation(nl_input: str, project_path: str):
    try:
        # Detect project context
        context = detect_project_context(project_path)

    except ValueError as e:
        print(f"❌ Invalid project path: {e}")
        return None

    try:
        # Process NL request
        issue = await process_request(nl_input, context)

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("💡 Check that ANTHROPIC_API_KEY is set")
        return None

    except Exception as e:
        print(f"❌ Failed to process request: {e}")
        return None

    try:
        # Post to GitHub
        poster = GitHubPoster()
        issue_number = poster.post_issue(issue, confirm=True)
        print(f"✓ Issue #{issue_number} created successfully")
        return issue_number

    except RuntimeError as e:
        print(f"❌ GitHub CLI error: {e}")
        print("💡 Make sure gh CLI is installed and authenticated")
        return None

# Usage
issue_number = asyncio.run(safe_issue_creation(
    "Add dark mode toggle",
    "/path/to/project"
))
```

### Working with Different Issue Types

#### Feature Requests

```python
# Simple feature
issue = await process_request(
    "Add a search bar to the navigation header",
    context
)

# Complex feature with multiple requirements
issue = await process_request(
    "Implement real-time collaborative editing with WebSockets, "
    "cursor tracking, and conflict resolution",
    context
)
```

#### Bug Reports

```python
# Bug with clear description
issue = await process_request(
    "Login button doesn't respond when clicked. Expected: login form appears. "
    "Actual: nothing happens.",
    context
)

# The system will detect this as a bug and use adw_plan_build_test_iso
```

#### Chores and Maintenance

```python
# Documentation task
issue = await process_request(
    "Update API documentation to include new authentication endpoints",
    context
)

# Refactoring task
issue = await process_request(
    "Refactor user service to use dependency injection",
    context
)

# The system will detect these as chores and use adw_sdlc_iso
```

---

## Configuration Options

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# Optional - GitHub configuration
GITHUB_REPO_URL=owner/repo

# Optional - Claude API configuration
ANTHROPIC_API_ENDPOINT=https://api.anthropic.com  # Custom endpoint
ANTHROPIC_MODEL=claude-sonnet-4-0                  # Custom model
```

### Model Selection

The system uses Claude Sonnet 4.0 by default. You can customize this in the code:

```python
# In nl_processor.py, modify the model parameter:
response = client.messages.create(
    model="claude-sonnet-4-0",  # or "claude-opus-4-0" for more accuracy
    max_tokens=300,
    temperature=0.1,
    messages=[{"role": "user", "content": prompt}]
)
```

### Workflow Customization

Customize how workflows are recommended:

```python
from app.server.core.nl_processor import suggest_adw_workflow

# Override the suggest_adw_workflow function
def custom_workflow_suggestion(issue_type: str, complexity: str):
    # Custom logic
    if issue_type == "feature" and complexity == "high":
        return ("adw_sdlc_zte_iso", "heavy")  # Zero-test-error workflow
    else:
        return suggest_adw_workflow(issue_type, complexity)

# Use in processing
# ...modify the process_request function to use custom_workflow_suggestion
```

---

## Best Practices

### Writing Effective Natural Language Requests

**Good Examples:**

✅ **Specific and actionable:**
```
"Add a dark mode toggle to the settings page with localStorage persistence"
```

✅ **Includes context:**
```
"Fix the login button that doesn't respond when clicked. Expected: login form appears. Actual: nothing happens"
```

✅ **Clear technical direction:**
```
"Implement user authentication with JWT tokens, refresh token rotation, and secure HTTP-only cookies"
```

**Poor Examples:**

❌ **Too vague:**
```
"Make the app better"
```

❌ **Lacks context:**
```
"Button broken"
```

❌ **Multiple unrelated requests:**
```
"Add dark mode, fix login, update docs, and refactor database"
```

### When to Use Different Issue Types

**Use "feature" for:**
- New functionality
- Enhancements to existing features
- UI/UX improvements
- Performance optimizations

**Use "bug" for:**
- Broken functionality
- Errors and exceptions
- Incorrect behavior
- Visual glitches

**Use "chore" for:**
- Documentation updates
- Dependency updates
- Refactoring without behavior changes
- Build system improvements
- Configuration changes

### Project Organization for Optimal Detection

Structure your projects with standard files for best detection:

**Frontend Projects:**
```
my-project/
├── package.json          # For framework detection
├── vite.config.ts        # For Vite detection
├── tsconfig.json         # For TypeScript detection
├── package-lock.json     # For npm detection
└── src/
    └── ...
```

**Backend Projects:**
```
my-project/
├── pyproject.toml        # For Python framework detection
├── requirements.txt      # Alternative Python detection
├── uv.lock               # For uv detection
└── app/
    └── ...
```

**Monorepos:**
```
monorepo/
├── packages/             # Monorepo indicator
│   ├── frontend/
│   └── backend/
└── apps/                 # Alternative monorepo indicator
    └── web/
```

---

## Troubleshooting

### Common Errors and Solutions

#### 1. "ANTHROPIC_API_KEY environment variable not set"

**Problem:** The Claude API key is not configured.

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-xxxxx" >> .env
```

#### 2. "GitHub CLI (gh) is not installed or not authenticated"

**Problem:** GitHub CLI is not available or not logged in.

**Solution:**
```bash
# Install gh CLI
brew install gh  # macOS
sudo apt install gh  # Linux

# Authenticate
gh auth login

# Verify
gh auth status
```

#### 3. "Project path does not exist: /path/to/project"

**Problem:** Invalid project path provided.

**Solution:**
```python
# Use absolute path
context = detect_project_context("/absolute/path/to/project")

# Or use current directory
context = detect_project_context(".")

# Verify path exists
import os
assert os.path.exists(project_path), f"Path does not exist: {project_path}"
```

#### 4. "Error analyzing intent with Anthropic: ..."

**Problem:** Claude API call failed (rate limit, network error, invalid key).

**Solutions:**
- **Rate limit:** Wait and retry with exponential backoff
- **Network error:** Check internet connection
- **Invalid key:** Verify ANTHROPIC_API_KEY is correct

```python
import time

async def analyze_with_retry(nl_input: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return await analyze_intent(nl_input)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

#### 5. "Failed to post issue to GitHub: ..."

**Problem:** GitHub CLI command failed.

**Solutions:**
- Verify repository URL is correct
- Check you have write access to the repository
- Ensure gh CLI is authenticated

```bash
# Test gh CLI
gh repo view owner/repo

# Re-authenticate if needed
gh auth logout
gh auth login
```

### Debugging Tips

#### Enable Verbose Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Now you'll see detailed logs
issue = await process_request(nl_input, context)
```

#### Inspect Intermediate Results

```python
# Check intent analysis
intent = await analyze_intent(nl_input)
print(f"Intent: {intent}")

# Check requirements
requirements = extract_requirements(nl_input, intent)
print(f"Requirements: {requirements}")

# Check project context
context = detect_project_context(".")
print(f"Context: {context.model_dump()}")
```

#### Dry Run Without Posting

```python
# Generate issue without posting
issue = await process_request(nl_input, context)

# Preview only (don't post)
poster = GitHubPoster()
preview = poster.format_preview(issue)
print(preview)

# Skip posting by not calling post_issue()
```

---

## FAQ

### Q: Can I use OpenAI instead of Anthropic?

**A:** Currently, the system only supports Anthropic's Claude API. OpenAI support could be added by implementing an alternative to `analyze_intent()` and `extract_requirements()`.

### Q: How much does it cost to use?

**A:** Costs depend on your Anthropic API usage. Each request typically uses:
- `analyze_intent()`: ~200-300 tokens (~$0.001)
- `extract_requirements()`: ~400-500 tokens (~$0.002)
- Total per issue: ~$0.003

### Q: Can I use this in CI/CD pipelines?

**A:** Yes! Set `confirm=False` to skip interactive prompts:

```python
issue_number = poster.post_issue(issue, confirm=False)
```

### Q: How accurate is project detection?

**A:** Project detection is based on file patterns and is generally accurate for standard project structures. For edge cases, you can manually create a `ProjectContext` object:

```python
from app.server.core.data_models import ProjectContext

context = ProjectContext(
    path="/path/to/project",
    is_new_project=False,
    framework="custom-framework",
    complexity="medium",
    build_tools=["custom-tool"],
    package_manager="custom-pm",
    has_git=True
)
```

### Q: Can I customize issue templates?

**A:** Yes! Modify the `ISSUE_TEMPLATES` dictionary in `app/server/core/issue_formatter.py`:

```python
ISSUE_TEMPLATES["feature"] = """# {title}

## Custom Section
{custom_field}

## Description
{description}

...
"""
```

### Q: What if my request is ambiguous?

**A:** The system makes reasonable assumptions based on intent analysis. For best results, be as specific as possible in your natural language input.

### Q: Can I batch process multiple requests?

**A:** Yes:

```python
requests = [
    "Add dark mode",
    "Fix login button",
    "Update API docs"
]

for req in requests:
    issue = await process_request(req, context)
    poster.post_issue(issue, confirm=False)
    await asyncio.sleep(1)  # Rate limiting
```

---

## Next Steps

- **Read the [API Reference](../api/nl-processing.md)** for detailed function documentation
- **Explore the [Architecture Guide](../architecture/nl-processing-architecture.md)** to understand system design
- **Check out the [Examples](../../examples/nl-processing/README.md)** for more code samples
- **Run the tests** to see the system in action:
  ```bash
  uv run pytest app/server/tests/core/test_nl_processor.py -v
  ```

---

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the test files for usage examples
- Review the API documentation for detailed information
