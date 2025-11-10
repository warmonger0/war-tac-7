# Integrating ADW Workflow into Existing Codebase

This guide explains how to integrate the ADW (Autonomous Development Workflow) system into your existing web application, enabling natural language-driven feature development.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Integration Steps](#integration-steps)
- [Framework-Specific Notes](#framework-specific-notes)
- [Manual Configuration](#manual-configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Overview

The ADW workflow integration adds the following to your project:

- `.claude/` directory with Claude Code configuration and custom commands
- `adws/` directory with workflow automation scripts
- Environment variable configuration
- GitHub webhook setup for automated workflows
- Framework-specific slash commands

After integration, you can use natural language to request features, which are automatically planned, implemented, tested, and reviewed.

## Prerequisites

Before integrating ADW into your existing project, ensure you have:

### Required

- **Git repository** - Your project must be in a git repository
- **GitHub remote** - Repository must be pushed to GitHub
- **GitHub CLI** - Install with `brew install gh` (macOS) or see [GitHub CLI docs](https://cli.github.com/)
- **Supported framework** - React, Next.js, Vue, Svelte, or vanilla JavaScript/TypeScript

### Recommended

- **Tests configured** - Existing test framework (Jest, Vitest, Pytest, etc.)
- **Clean working tree** - Commit or stash any pending changes
- **Package manager** - npm, yarn, or bun for JavaScript projects
- **Python environment** - For backend projects using FastAPI/Django

## Quick Start

The fastest way to integrate ADW into your existing project:

```bash
# From the tac-webbuilder directory
./scripts/integrate_existing.sh /path/to/your/app
```

This script will:
1. Detect your framework and project structure
2. Generate a GitHub issue with integration steps
3. Let ADW automatically configure your project

Skip to [Manual Configuration](#manual-configuration) if you prefer to set up manually.

## Integration Steps

### 1. Run Integration Command

```bash
cd /path/to/tac-webbuilder
./scripts/integrate_existing.sh /path/to/your/app
```

The script will analyze your project and output:

```
📊 Detected framework: React + Vite
📊 Package manager: bun
📊 Test framework: Vitest
📊 Project structure:
    - src/ (source code)
    - tests/ (test files)
    - public/ (static assets)

✅ Created GitHub issue #123 for ADW integration
```

### 2. ADW Setup Issue

The integration creates a GitHub issue that will:

- Add `.claude/` directory with:
  - `settings.json` - Claude Code configuration
  - `commands/` - Custom slash commands for your stack
- Add `adws/` directory with workflow scripts
- Configure environment variables in `.env` and `.env.sample`
- Set up GitHub webhook (manual step)
- Create initial tests if missing
- Add framework-specific utilities

### 3. Monitor ADW Workflow

Once the issue is created, ADW will:

1. **Plan** - Analyze your project and create technical spec
2. **Implement** - Add ADW infrastructure
3. **Test** - Verify configuration works
4. **Review** - Create PR for review

Review and merge the PR when ready.

### 4. Manual Post-Integration Steps

After ADW completes setup:

#### a. Review Environment Variables

Check `.env.sample` and create `.env`:

```bash
cp .env.sample .env
# Edit .env and add your API keys
```

Common variables:
```env
# API Keys
ANTHROPIC_API_KEY=your-key-here
GITHUB_TOKEN=your-token-here

# Project Configuration
PROJECT_NAME=your-app
GITHUB_REPO=owner/repo

# Server Configuration (if applicable)
API_URL=http://localhost:8000
```

#### b. Configure GitHub Webhook

Set up webhook for automated workflows:

1. Go to your repo settings: `https://github.com/owner/repo/settings/hooks`
2. Click "Add webhook"
3. Configure:
   - **Payload URL**: Your webhook endpoint (if using tac-webbuilder API)
   - **Content type**: `application/json`
   - **Events**: Select "Issues" and "Pull requests"
   - **Active**: ✅ Checked
4. Save webhook

#### c. Test ADW Integration

Create a simple test issue:

```bash
# Using tac-webbuilder CLI
cd /path/to/tac-webbuilder
./scripts/start_cli.sh request "Add a button that logs 'Hello' when clicked"
```

Or create a GitHub issue manually with ADW labels.

## Framework-Specific Notes

### React Projects

**Detected indicators:**
- `package.json` with `react` dependency
- `src/` directory with `.jsx` or `.tsx` files
- Vite, Create React App, or custom build config

**Integration adds:**
- React Testing Library if not present
- Vitest or Jest configuration
- Component scaffolding commands
- API client utilities in `src/api/`

**Configuration:**
```json
// .claude/settings.json
{
  "rules": [
    "Use TypeScript for all new files",
    "Include tests with React Testing Library",
    "Follow React hooks best practices",
    "Update API client when adding endpoints"
  ]
}
```

**Commands added:**
- `/add-component` - Scaffold new React component
- `/add-api` - Add new API endpoint
- `/add-test` - Create component test

### Next.js Projects

**Detected indicators:**
- `package.json` with `next` dependency
- `app/` or `pages/` directory
- `next.config.js` or `next.config.mjs`

**Integration adds:**
- Jest with Next.js config if not present
- API route helpers
- Server/Client component utilities
- App Router or Pages Router specific commands

**Configuration:**
```json
// .claude/settings.json
{
  "rules": [
    "Use App Router patterns (not Pages Router)",
    "Server Components by default, Client Components when needed",
    "Include tests with Jest and React Testing Library",
    "Use Next.js Image component for images",
    "API routes in app/api/ directory"
  ]
}
```

**Commands added:**
- `/add-page` - Create new Next.js page
- `/add-api-route` - Add API route
- `/add-layout` - Create layout component
- `/add-server-action` - Add server action (App Router)

### Vue Projects

**Detected indicators:**
- `package.json` with `vue` dependency
- `src/` directory with `.vue` files
- Vite or Vue CLI config

**Integration adds:**
- Vue Test Utils if not present
- Vitest or Jest configuration
- Component scaffolding commands
- Pinia store utilities (if using Pinia)

**Configuration:**
```json
// .claude/settings.json
{
  "rules": [
    "Use Composition API (not Options API)",
    "Include tests with Vue Test Utils",
    "Use script setup syntax",
    "Follow Vue 3 best practices"
  ]
}
```

### Backend Projects (FastAPI, Express)

**FastAPI:**

**Detected indicators:**
- `main.py` or `app.py` with FastAPI import
- `requirements.txt` or `pyproject.toml` with `fastapi`

**Integration adds:**
- Pytest configuration
- Test client utilities
- OpenAPI/Swagger documentation helpers
- CRUD operation templates

**Express:**

**Detected indicators:**
- `package.json` with `express` dependency
- Server file (`server.js`, `index.js`, `app.js`)

**Integration adds:**
- Jest or Mocha configuration
- Supertest for API testing
- Route scaffolding commands
- Middleware utilities

### Vanilla JavaScript

**Detected indicators:**
- No major framework detected
- `.html`, `.css`, `.js` files
- Simple project structure

**Integration adds:**
- Basic testing with Jest (optional)
- ESLint configuration
- Simple build setup (optional)
- HTML/CSS/JS scaffolding commands

## Manual Configuration

If you prefer manual setup over the automated integration:

### Step 1: Add .claude Directory

```bash
cd /path/to/your/app
mkdir -p .claude/commands
```

Create `.claude/settings.json`:

```json
{
  "mcpServers": {},
  "rules": [
    "When implementing features, always include tests",
    "Use TypeScript for all new files (if applicable)",
    "Follow project coding standards",
    "Update documentation when adding features"
  ]
}
```

### Step 2: Add ADW Scripts (Optional)

If you want to use ADW automation scripts:

```bash
mkdir -p adws/adw_modules
```

Copy or link ADW scripts from tac-webbuilder or implement custom workflow scripts.

### Step 3: Environment Variables

Create `.env.sample`:

```env
# API Keys (add your keys to .env, not .env.sample)
ANTHROPIC_API_KEY=
GITHUB_TOKEN=

# Project Configuration
PROJECT_NAME=your-app
GITHUB_REPO=owner/repo
```

Create `.env` (add to `.gitignore`):

```env
ANTHROPIC_API_KEY=your-actual-key
GITHUB_TOKEN=your-actual-token
# ... other variables
```

### Step 4: Add Custom Commands

Create project-specific slash commands in `.claude/commands/`:

Example: `.claude/commands/add-component.md`

```markdown
Create a new React component with:
- TypeScript
- Component file in src/components/
- Test file using React Testing Library
- Export from index.ts
```

### Step 5: Health Check Endpoint (Backend Only)

Add a health check endpoint for monitoring:

**FastAPI:**
```python
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

**Express:**
```javascript
app.get('/health', (req, res) => {
  res.json({ status: 'ok' })
})
```

## Verification

After integration, verify everything works:

### 1. Check File Structure

```bash
ls -la .claude/
# Should show: settings.json, commands/

ls -la adws/  # If using ADW automation
# Should show: ADW workflow scripts
```

### 2. Test Environment Variables

```bash
# Check .env is ignored
git check-ignore .env
# Should output: .env

# Verify .env.sample is tracked
git ls-files .env.sample
# Should output: .env.sample
```

### 3. Run Tests

```bash
# React/Next.js/Vue
npm test

# FastAPI
pytest

# Express
npm test
```

### 4. Test Natural Language Request

Using tac-webbuilder:

```bash
cd /path/to/tac-webbuilder
./scripts/start_cli.sh request "Add a simple test feature to verify ADW integration"
```

Check that:
- GitHub issue is created
- Issue has proper labels
- ADW workflow can access your repo

## Troubleshooting

### Issue: Framework Not Detected

**Problem:** Integration script says "Unknown framework"

**Solution:**
- Ensure your project has clear framework indicators (package.json, main files)
- Manually specify framework in integration script (coming soon)
- Use manual configuration steps

### Issue: GitHub CLI Not Authenticated

**Problem:** `gh` command fails with authentication error

**Solution:**
```bash
gh auth login
# Follow prompts to authenticate
```

### Issue: Permission Denied on Scripts

**Problem:** Can't execute integration script

**Solution:**
```bash
chmod +x scripts/integrate_existing.sh
```

### Issue: Tests Failing After Integration

**Problem:** Existing tests break after ADW integration

**Solution:**
- Check if new dependencies conflict with existing ones
- Verify test configuration wasn't overwritten
- Review PR changes before merging
- Restore from git if needed: `git restore <file>`

### Issue: Environment Variables Not Loading

**Problem:** App can't find environment variables

**Solution:**
- Ensure `.env` file exists (copy from `.env.sample`)
- Check variable names match your framework:
  - Vite: `VITE_*`
  - Next.js: `NEXT_PUBLIC_*`
  - Create React App: `REACT_APP_*`
- Restart dev server after changing `.env`

### Issue: ADW Workflow Not Triggering

**Problem:** Creating issues doesn't start ADW workflow

**Solution:**
- Verify webhook is configured correctly
- Check issue has required labels
- Ensure GitHub token has necessary permissions
- Review webhook delivery logs in GitHub settings

### Issue: Conflicts with Existing .claude/ Directory

**Problem:** Your project already has a `.claude/` directory

**Solution:**
- Back up existing `.claude/` directory
- Merge ADW configuration with your existing setup
- Keep your custom commands and add ADW commands separately

## Next Steps

After successful integration:

1. **Read Documentation**
   - [CLI Reference](../docs/cli.md)
   - [Example Requests](../docs/examples.md)
   - [Architecture](../docs/architecture.md)

2. **Try Example Requests**
   - Start with simple features
   - Review ADW-generated code
   - Learn from the patterns

3. **Customize Configuration**
   - Add project-specific rules to `.claude/settings.json`
   - Create custom slash commands
   - Configure test preferences

4. **Share with Team**
   - Document ADW usage in your project README
   - Train team on natural language requests
   - Establish guidelines for ADW usage

## Support

If you encounter issues not covered here:

1. Check [Troubleshooting Guide](../docs/troubleshooting.md)
2. Review [GitHub Issues](https://github.com/owner/tac-webbuilder/issues)
3. Create new issue with:
   - Framework and version
   - Integration script output
   - Error messages
   - Project structure (sanitized)

---

**Need help?** Join our community or open an issue on GitHub.
