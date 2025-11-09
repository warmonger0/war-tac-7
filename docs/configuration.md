# tac-webbuilder Configuration Guide

Complete reference documentation for configuring tac-webbuilder environment variables and development environment.

## Table of Contents

- [Quick Setup](#quick-setup)
- [Configuration Overview](#configuration-overview)
- [Required Configuration](#required-configuration)
- [Optional Configuration](#optional-configuration)
- [Cloud Services Setup](#cloud-services-setup)
- [Environment Variables Reference](#environment-variables-reference)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)

## Quick Setup

Get started with tac-webbuilder in 3 steps:

### Option 1: Interactive Setup (Recommended)

```bash
# Run the interactive setup wizard
./scripts/setup_env.sh

# Validate your configuration
./scripts/test_config.sh

# Start the application
./scripts/start.sh
```

### Option 2: Manual Setup

```bash
# Copy the sample file
cp .env.sample .env

# Edit with your preferred editor
nano .env  # or vim, code, etc.

# Validate your configuration
./scripts/test_config.sh
```

### Option 3: Quick Minimal Setup

For the absolute minimum to get started:

```bash
# Copy sample and set only the required API key
cp .env.sample .env
echo "ANTHROPIC_API_KEY=your-api-key-here" >> .env

# Validate
./scripts/test_config.sh
```

## Configuration Overview

tac-webbuilder uses environment variables for configuration. These are stored in a `.env` file in the project root. The configuration is organized into several categories:

- **Anthropic Configuration** (Required) - API keys for Claude Code
- **Claude Code Configuration** - Path and behavior settings
- **GitHub Configuration** - Authentication for GitHub integration
- **ADW Workflow Configuration** - Webhook and automation setup
- **Web Application Configuration** - API keys for SQL features
- **Cloud Services Configuration** - E2B, Cloudflare R2
- **Playwright MCP Configuration** - Browser automation settings

### Configuration Files

| File | Purpose | Version Control |
|------|---------|-----------------|
| `.env` | Your actual configuration with secrets | **Never commit** (in .gitignore) |
| `.env.sample` | Template with documentation | Commit to repository |
| `playwright-mcp-config.json` | Playwright browser settings | Commit to repository |

## Required Configuration

These settings are required for basic functionality.

### Anthropic API Key

**Variable**: `ANTHROPIC_API_KEY`
**Required**: Yes
**Purpose**: Authentication for Claude Code programmatic mode

#### How to Obtain

1. Go to [Anthropic Console](https://console.anthropic.com/settings/keys)
2. Sign in or create an account
3. Navigate to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Store it securely in your password manager

#### Setup

```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

#### Cost & Usage

- Pay-as-you-go pricing
- Monitor usage in [Anthropic Console](https://console.anthropic.com/settings/usage)
- Set up billing alerts to avoid unexpected charges
- Typical development usage: $5-20/month

#### Security Notes

- Never commit this key to version control
- Rotate keys every 90 days
- Use separate keys for development and production
- Revoke keys immediately if compromised

## Optional Configuration

These settings enable additional features but aren't required for basic functionality.

### Claude Code Path

**Variable**: `CLAUDE_CODE_PATH`
**Required**: No
**Default**: `claude` (assumes in PATH)
**Purpose**: Location of Claude Code executable

#### When to Configure

Only needed if:
- Claude Code is not in your system PATH
- You have multiple Claude Code installations
- The `claude` command doesn't work

#### Setup

```bash
# Auto-detect (recommended)
./scripts/setup_env.sh  # Will auto-detect and set

# Or manually find the path
which claude
# Copy the output path and set:
CLAUDE_CODE_PATH=/usr/local/bin/claude
```

### Claude Code Behavior

**Variable**: `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`
**Required**: No
**Default**: `true`
**Purpose**: Return to project root after commands

#### Options

- `true` - Claude Code returns to project root after each command (recommended)
- `false` - Claude Code maintains its current working directory

```bash
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=true
```

### GitHub Personal Access Token

**Variable**: `GITHUB_PAT`
**Required**: No
**Purpose**: Use different GitHub account than default `gh auth` login

#### When to Configure

Only needed if:
- You want ADW to use a different GitHub account
- Your default `gh auth` account isn't appropriate for this project
- You need programmatic GitHub access in CI/CD

#### How to Obtain

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" (classic or fine-grained)
3. Select required scopes:
   - `repo` - Full repository access
   - `workflow` - Update GitHub Actions workflows
   - `read:org` - Read organization data (for private repos)
4. Generate and copy the token
5. Store securely in password manager

#### Setup

```bash
GITHUB_PAT=ghp_your_token_here
```

#### Best Practices

- Use Fine-Grained tokens with minimum required permissions
- Set expiration (90 days recommended)
- Use separate tokens for different projects
- Revoke immediately if compromised

### OpenAI API Key

**Variable**: `OPENAI_API_KEY`
**Required**: No
**Purpose**: Enable OpenAI models for natural language to SQL feature

#### When to Configure

- You prefer OpenAI models over Anthropic for SQL generation
- You want to compare results between providers
- You have existing OpenAI credits

**Note**: You need either OpenAI or Anthropic API key for SQL features. The `ANTHROPIC_API_KEY` (defined above) can also be used for SQL features.

#### How to Obtain

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Store securely

#### Setup

```bash
OPENAI_API_KEY=sk-your-openai-key-here
```

## Cloud Services Setup

These services enhance tac-webbuilder with cloud features.

### E2B Cloud Sandbox

**Variable**: `E2B_API_KEY`
**Required**: No
**Purpose**: Isolated code execution environments for agents

#### Benefits

- Secure sandboxed execution
- Persistent environments
- Pre-configured development containers
- Better isolation for untrusted code

#### Setup Guide

1. **Sign up**: Go to [E2B](https://e2b.dev)
2. **Get API key**: Navigate to [API Keys](https://e2b.dev/docs/getting-started/api-key)
3. **Configure**:
   ```bash
   E2B_API_KEY=e2b_your_api_key_here
   ```
4. **Verify**: Run `./scripts/test_config.sh`

#### Usage

E2B is automatically used by agents when configured. No code changes needed.

### Cloudflare Tunnel (for ADW Webhooks)

**Variable**: `CLOUDFLARED_TUNNEL_TOKEN`
**Required**: No
**Purpose**: Expose local webhook server to GitHub

#### When to Use

- You want GitHub to automatically trigger ADW workflows via webhooks
- You're testing webhook integrations locally
- You don't want to deploy webhook server to cloud

#### Setup Guide

1. **Install cloudflared**:
   ```bash
   # macOS
   brew install cloudflared

   # Linux
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
   sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
   sudo chmod +x /usr/local/bin/cloudflared
   ```

2. **Authenticate**:
   ```bash
   cloudflared tunnel login
   ```

3. **Create tunnel**:
   ```bash
   cloudflared tunnel create tac-webhook
   ```

4. **Get tunnel token**:
   - Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
   - Navigate to Access > Tunnels
   - Find your tunnel and copy the token

5. **Configure**:
   ```bash
   CLOUDFLARED_TUNNEL_TOKEN=your_tunnel_token_here
   ```

6. **Run tunnel**:
   ```bash
   cloudflared tunnel run tac-webhook
   ```

7. **Configure GitHub webhook**:
   - Use the tunnel URL as webhook endpoint
   - Set up in GitHub repository settings

#### Alternative

If you don't need webhooks, ADW can be used manually without Cloudflare Tunnel.

### Cloudflare R2 (Screenshot Storage)

**Variables**: Multiple (all required for R2 to work)
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_R2_ACCESS_KEY_ID`
- `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
- `CLOUDFLARE_R2_BUCKET_NAME`
- `CLOUDFLARE_R2_PUBLIC_DOMAIN`

**Purpose**: Upload review screenshots to cloud storage

#### Benefits

- Screenshots visible directly in GitHub comments (as images, not file paths)
- Easy sharing with team members
- Persistent storage
- Cost-effective ($0.015/GB/month)

#### Setup Guide

1. **Create R2 bucket**:
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
   - Navigate to R2 Object Storage
   - Click "Create bucket"
   - Name it (e.g., `tac-screenshots`)

2. **Create API token**:
   - In R2 dashboard, click "Manage R2 API Tokens"
   - Click "Create API token"
   - Select permissions: Object Read & Write
   - Copy the Access Key ID and Secret Access Key

3. **Set up public access**:
   - In bucket settings, enable public access
   - Configure custom domain or use R2.dev subdomain
   - Note the public domain URL

4. **Get account ID**:
   - Found in Cloudflare dashboard URL
   - Or in R2 bucket details

5. **Configure**:
   ```bash
   CLOUDFLARE_ACCOUNT_ID=your_account_id
   CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key_id
   CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_access_key
   CLOUDFLARE_R2_BUCKET_NAME=tac-screenshots
   CLOUDFLARE_R2_PUBLIC_DOMAIN=https://tac-screenshots.your-account.r2.dev
   ```

6. **Verify**:
   ```bash
   ./scripts/test_config.sh
   # Should show "✓ Cloudflare R2 fully configured"
   ```

#### Fallback Behavior

If R2 is not configured, screenshots use local file paths in comments. This works but requires manual sharing of files.

## Environment Variables Reference

Complete reference table of all environment variables.

### Required Variables

| Variable | Description | Example | How to Obtain |
|----------|-------------|---------|---------------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude Code | `sk-ant-***` | [console.anthropic.com](https://console.anthropic.com/settings/keys) |

### Claude Code Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CLAUDE_CODE_PATH` | Path to Claude Code executable | `claude` | `/usr/local/bin/claude` |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Return to root after commands | `true` | `true` or `false` |

### GitHub Variables

| Variable | Description | Example | How to Obtain |
|----------|-------------|---------|---------------|
| `GITHUB_PAT` | GitHub Personal Access Token | `ghp_***` | [github.com/settings/tokens](https://github.com/settings/tokens) |

### Web Application Variables

| Variable | Description | Example | How to Obtain |
|----------|-------------|---------|---------------|
| `OPENAI_API_KEY` | OpenAI API key for SQL features | `sk-***` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |

### Cloud Services Variables

| Variable | Description | Example | How to Obtain |
|----------|-------------|---------|---------------|
| `E2B_API_KEY` | E2B sandbox API key | `e2b_***` | [e2b.dev/docs/getting-started/api-key](https://e2b.dev/docs/getting-started/api-key) |
| `CLOUDFLARED_TUNNEL_TOKEN` | Cloudflare Tunnel token | `eyJ***` | Cloudflare Zero Trust dashboard |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare account ID | `abc123...` | Cloudflare dashboard |
| `CLOUDFLARE_R2_ACCESS_KEY_ID` | R2 access key ID | `abc123...` | R2 API token creation |
| `CLOUDFLARE_R2_SECRET_ACCESS_KEY` | R2 secret key | `xyz789...` | R2 API token creation |
| `CLOUDFLARE_R2_BUCKET_NAME` | R2 bucket name | `tac-screenshots` | Your bucket name |
| `CLOUDFLARE_R2_PUBLIC_DOMAIN` | R2 public URL | `https://...` | Bucket settings |

## Troubleshooting

### Common Issues

#### 1. "claude: command not found"

**Problem**: Claude Code is not installed or not in PATH

**Solutions**:
```bash
# Check if installed
which claude

# Install if missing
npm install -g @anthropic-ai/claude-code

# Or set custom path in .env
CLAUDE_CODE_PATH=/path/to/claude
```

#### 2. "GitHub authentication failed"

**Problem**: GitHub CLI not authenticated

**Solutions**:
```bash
# Authenticate with GitHub CLI
gh auth login

# Or set GITHUB_PAT in .env
GITHUB_PAT=ghp_your_token_here

# Verify authentication
gh auth status
```

#### 3. "Invalid API key"

**Problem**: API key format is incorrect or expired

**Checklist**:
- [ ] No extra spaces or newlines in .env
- [ ] Key starts with correct prefix (`sk-ant-` for Anthropic)
- [ ] Key hasn't been revoked or expired
- [ ] Key has required permissions
- [ ] Copied entire key (they're long!)

**Verify**:
```bash
# Check key format in .env
cat .env | grep ANTHROPIC_API_KEY
# Should be: ANTHROPIC_API_KEY=sk-ant-...

# No spaces around = sign
# No quotes unless key contains special characters
```

#### 4. "Webhook not receiving events"

**Problem**: Cloudflare Tunnel not working

**Debug Steps**:
```bash
# 1. Verify tunnel token is set
./scripts/test_config.sh

# 2. Check if cloudflared is running
ps aux | grep cloudflared

# 3. Start tunnel manually
cloudflared tunnel run tac-webhook

# 4. Check tunnel status in Cloudflare dashboard

# 5. Verify GitHub webhook configuration
# Go to: Settings > Webhooks in your repo
```

#### 5. "Configuration valid with warnings"

**Problem**: Optional features not configured

**Action**: This is normal! Warnings indicate optional features. You can:
- Ignore if you don't need those features
- Configure them later when needed
- See [Optional Configuration](#optional-configuration) section

#### 6. "R2 screenshots not appearing"

**Problem**: Incomplete R2 configuration

**Solution**: All 5 R2 variables must be set:
```bash
./scripts/test_config.sh
# Look for "Cloudflare R2 partially configured"

# Set all variables:
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_R2_ACCESS_KEY_ID=...
CLOUDFLARE_R2_SECRET_ACCESS_KEY=...
CLOUDFLARE_R2_BUCKET_NAME=...
CLOUDFLARE_R2_PUBLIC_DOMAIN=...
```

### Validation Commands

```bash
# Full validation
./scripts/test_config.sh

# Check specific tool
which claude
gh --version
gh auth status

# Test .env file loading
source .env && echo $ANTHROPIC_API_KEY

# Verify .env file format
cat -A .env | head  # Should not show ^M (Windows line endings)
```

### Getting Help

If issues persist:

1. **Check configuration**:
   ```bash
   ./scripts/test_config.sh
   ```

2. **Review this documentation**: Ensure all steps followed correctly

3. **Check example configuration**: Compare your .env with .env.sample

4. **File an issue**: Include sanitized validation output (remove API keys!)

## Best Practices

### Security

#### Never Commit Secrets
```bash
# Verify .env is in .gitignore
cat .gitignore | grep ".env"

# Check for accidentally staged .env
git status

# If .env was committed, remove from history:
git rm --cached .env
git commit -m "Remove .env from version control"
```

#### Rotate API Keys Regularly
- Set calendar reminder every 90 days
- Generate new key
- Update .env
- Revoke old key
- Test application

#### Use Environment-Specific Files
```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production

# Load with:
source .env.development
```

#### Store in Password Manager
- 1Password, LastPass, Bitwarden, etc.
- Create secure note for each project
- Share with team through password manager (not Slack/email!)

### Performance

#### Monitor API Usage
- Check Anthropic Console daily during active development
- Set up billing alerts
- Monitor costs per feature/workflow
- Optimize prompts to reduce token usage

#### Optimize E2B Usage
- Only use for untrusted code execution
- Reuse environments when possible
- Clean up unused environments

#### Video Recording
```json
// playwright-mcp-config.json
{
  "browser": {
    "contextOptions": {
      "recordVideo": {
        // Disable for faster tests
        "dir": null
      }
    }
  }
}
```

### Development

#### Use Separate Development Keys
- Never use production keys in development
- Create separate API keys for dev/staging/prod
- Easier to track usage and revoke if needed

#### Document Custom Configuration
```bash
# Add comments to your .env
# (Note: .env doesn't officially support comments, so use separate doc)

# Create .env.notes (not committed)
echo "ANTHROPIC_API_KEY: Development key, expires 2024-06-01" > .env.notes
```

#### Team Onboarding
1. Clone repository
2. Run `./scripts/setup_env.sh`
3. Follow interactive prompts
4. Validate with `./scripts/test_config.sh`
5. Start working!

## Advanced Configuration

### Multiple Environments

Create environment-specific files:

```bash
# Create files
cp .env.sample .env.development
cp .env.sample .env.production

# Use with scripts
ENV_FILE=.env.production ./scripts/test_config.sh
```

### CI/CD Configuration

For GitHub Actions:

```yaml
# .github/workflows/test.yml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  GITHUB_PAT: ${{ secrets.GITHUB_PAT }}
```

Store secrets in:
- GitHub Settings > Secrets and variables > Actions

### Docker Configuration

```dockerfile
# Dockerfile
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# docker-compose.yml
services:
  app:
    env_file:
      - .env
```

### Custom Playwright Configuration

Edit `playwright-mcp-config.json`:

```json
{
  "browser": {
    "browserName": "firefox",  // chromium, firefox, webkit
    "launchOptions": {
      "headless": false,  // Show browser
      "slowMo": 100       // Slow down for debugging
    },
    "contextOptions": {
      "viewport": {
        "width": 1280,
        "height": 720
      },
      "recordVideo": {
        "dir": "./test-videos",
        "size": {
          "width": 1280,
          "height": 720
        }
      }
    }
  }
}
```

### Loading Order

Configuration is loaded in this order (later overrides earlier):

1. `.env.sample` (defaults)
2. `.env` (your configuration)
3. Environment variables (shell exports)
4. Command-line arguments (if supported)

Example:
```bash
# .env has ANTHROPIC_API_KEY=key1
# Override for one command:
ANTHROPIC_API_KEY=key2 ./scripts/test_config.sh
```

## Related Documentation

- [README.md](../README.md) - Project overview and quick start
- [ADW README](../adws/README.md) - ADW workflow system
- [E2E Tests](./.claude/commands/test_e2e.md) - End-to-end testing guide

## Contributing

Found an issue with this documentation? Please:

1. Check if it's already documented
2. Verify the issue exists
3. File an issue with:
   - What you expected
   - What actually happened
   - Steps to reproduce (without sharing secrets!)
   - Sanitized validation output

---

**Last Updated**: 2025-11-09
**Version**: 1.0.0
