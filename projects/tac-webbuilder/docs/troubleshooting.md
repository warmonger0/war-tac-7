# TAC WebBuilder Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: uv command not found

**Symptoms:**
```bash
$ uv sync
bash: uv: command not found
```

**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"

# Verify installation
uv --version
```

#### Issue: Python version mismatch

**Symptoms:**
```
Error: Python 3.11 or higher required
```

**Solution:**
```bash
# Check current version
python --version

# Install Python 3.11+ using uv
uv python install 3.11

# Or use system package manager
# macOS:
brew install python@3.11

# Ubuntu:
sudo apt install python3.11
```

#### Issue: Dependency conflicts

**Symptoms:**
```
error: Failed to resolve dependencies
```

**Solution:**
```bash
# Clear cache and reinstall
uv cache clean
uv sync --force

# Or use pip as fallback
pip install -r requirements.txt --force-reinstall
```

### Server Issues

#### Issue: Port already in use

**Symptoms:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uv run uvicorn app.server.server:app --port 8001
```

#### Issue: Server crashes on startup

**Symptoms:**
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution:**
```bash
# Verify all dependencies installed
uv sync

# Check Python path
uv run python -c "import sys; print(sys.path)"

# Run with verbose logging
uv run uvicorn app.server.server:app --log-level debug
```

#### Issue: Hot reload not working

**Symptoms:**
Code changes not reflected without manual restart

**Solution:**
```bash
# Ensure --reload flag is used
uv run uvicorn app.server.server:app --reload

# Check file system limits (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### API Key Issues

#### Issue: OpenAI API key not working

**Symptoms:**
```
Error: OpenAI API key not found or invalid
```

**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Check key is set
cat .env | grep OPENAI_API_KEY

# Verify key format (should start with sk-)
echo $OPENAI_API_KEY

# Test key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Issue: Anthropic API key not working

**Symptoms:**
```
Error: Anthropic API key not found or invalid
```

**Solution:**
```bash
# Check key format (should start with sk-ant-)
echo $ANTHROPIC_API_KEY

# Test key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'
```

#### Issue: Keys not loading from .env

**Symptoms:**
API calls fail even though keys are in .env

**Solution:**
```python
# Verify python-dotenv is installed
uv add python-dotenv

# Load .env explicitly in code
from dotenv import load_dotenv
load_dotenv()

# Check if loaded
import os
print(os.getenv('OPENAI_API_KEY'))
```

### GitHub Integration Issues

#### Issue: GitHub CLI not authenticated

**Symptoms:**
```
Error: GitHub CLI not authenticated
```

**Solution:**
```bash
# Install GitHub CLI
brew install gh  # macOS
# or
sudo apt install gh  # Ubuntu

# Authenticate
gh auth login

# Verify
gh auth status
```

#### Issue: Permission denied when posting issues

**Symptoms:**
```
Error: Resource not accessible by integration
```

**Solution:**
```bash
# Check token scopes
gh auth status

# Token needs 'repo' and 'workflow' scopes
# Generate new token at: https://github.com/settings/tokens

# Update token
export GITHUB_TOKEN=ghp_your_new_token

# Or in .env file
echo "GITHUB_TOKEN=ghp_your_new_token" >> .env
```

#### Issue: Repository not found

**Symptoms:**
```
Error: Repository 'owner/repo' not found
```

**Solution:**
```bash
# Verify repository exists
gh repo view owner/repo

# Check GITHUB_REPO in .env
cat .env | grep GITHUB_REPO

# Format should be: owner/repository
# Example: GITHUB_REPO=anthropics/tac-webbuilder
```

### File Processing Issues

#### Issue: CSV conversion fails

**Symptoms:**
```
Error: Failed to parse CSV file
```

**Solution:**
```python
# Check file encoding
file -I yourfile.csv

# Try converting encoding
iconv -f ISO-8859-1 -t UTF-8 yourfile.csv > yourfile_utf8.csv

# Check for malformed CSV
python -c "
import csv
with open('yourfile.csv') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        print(f'Row {i}: {len(row)} columns')
"
```

#### Issue: JSON conversion fails

**Symptoms:**
```
Error: Invalid JSON format
```

**Solution:**
```bash
# Validate JSON
python -m json.tool yourfile.json

# Or use jq
jq . yourfile.json

# Common issues:
# - Trailing commas
# - Single quotes instead of double quotes
# - Missing closing brackets
```

#### Issue: Database file too large

**Symptoms:**
```
Error: Out of memory
```

**Solution:**
```python
# Process in chunks for large files
from core.file_processor import FileProcessor

fp = FileProcessor()

# For CSV
import pandas as pd
chunksize = 10000
for chunk in pd.read_csv('large.csv', chunksize=chunksize):
    chunk.to_sql('table_name', db_connection, if_exists='append')
```

### SQL Query Issues

#### Issue: Query blocked by safety check

**Symptoms:**
```
Error: Dangerous SQL keyword detected
```

**Solution:**
This is intentional security. The system only allows SELECT queries.

```python
# Only SELECT queries are allowed
# ✓ Allowed:
SELECT * FROM users WHERE created_at > '2024-01-01'

# ✗ Blocked:
UPDATE users SET password = 'new'
DELETE FROM users
DROP TABLE users
```

#### Issue: SQL generation produces incorrect query

**Symptoms:**
Generated SQL doesn't match the question

**Solution:**
```python
# Provide more context in the question
# Instead of: "Show users"
# Use: "Show all users from the users table ordered by created_at"

# Verify schema is correct
from core.sql_processor import SQLProcessor
sql = SQLProcessor()
schema = sql.get_database_schema(db_path)
print(schema)

# Try different LLM provider
result = llm.generate_sql(question, schema, "anthropic")  # or "openai"
```

### NL Processing Issues

#### Issue: Poor requirement extraction

**Symptoms:**
Extracted requirements don't match input

**Solution:**
```python
# Be more specific in input
# Instead of: "Add feature"
# Use: "Add user profile editing feature with avatar upload and bio"

# Specify requirements explicitly
# Use bullet points:
text = """
Create user authentication with:
- Email/password login
- OAuth (Google, GitHub)
- Password reset via email
- Session management
"""

result = await processor.process_request(text)
```

#### Issue: Wrong issue type classification

**Symptoms:**
Feature classified as bug or vice versa

**Solution:**
```python
# Use explicit keywords
# For features: "Create", "Add", "Implement", "Build"
# For bugs: "Fix", "Error", "Bug", "Issue", "Problem"
# For chores: "Update", "Refactor", "Clean", "Maintain"

# Override classification if needed
result = await processor.process_request(text)
result["issue_type"] = "feature"  # Manual override
```

### Performance Issues

#### Issue: Slow API responses

**Symptoms:**
Requests take 30+ seconds

**Solution:**
```python
# LLM calls are inherently slow (5-30 seconds)
# Use caching for repeated queries

import functools

@functools.lru_cache(maxsize=100)
def cached_generate_sql(question: str, schema_str: str):
    return generate_sql(question, eval(schema_str))

# Or use Redis for distributed caching
```

#### Issue: High memory usage

**Symptoms:**
Server using > 1GB RAM

**Solution:**
```bash
# Monitor memory
uv run python -c "
import psutil
process = psutil.Process()
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"

# Reduce worker count
uv run uvicorn app.server.server:app --workers 1

# Process files in chunks
# Close database connections after use
```

### Testing Issues

#### Issue: Tests failing locally

**Symptoms:**
```
45 failed, 203 passed
```

**Solution:**
```bash
# Run specific test
cd app/server
uv run pytest tests/core/test_nl_processor.py -v

# Check test dependencies
uv run pytest --collect-only

# Clear pytest cache
rm -rf .pytest_cache
uv run pytest --cache-clear

# Update test fixtures if needed
```

#### Issue: Tests pass locally but fail in CI

**Symptoms:**
Different results in GitHub Actions

**Solution:**
```yaml
# Verify Python version in CI matches local
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'

# Install exact dependencies
- run: uv sync --frozen

# Check for timing issues
- run: uv run pytest tests/ --timeout=60
```

### MCP Configuration Issues

#### Issue: MCP server not starting

**Symptoms:**
```
Error: Failed to start MCP server
```

**Solution:**
```bash
# Check Node.js is installed
node --version
npm --version

# Install Playwright MCP
npm install -g @playwright/mcp@latest

# Verify config file exists
cat .mcp.json.sample

# Copy sample to active config
cp .mcp.json.sample .mcp.json

# Test manually
npx @playwright/mcp@latest --config ./playwright-mcp-config.json
```

#### Issue: Video recording fails

**Symptoms:**
```
Error: Cannot create videos directory
```

**Solution:**
```bash
# Create videos directory
mkdir -p videos

# Check permissions
chmod 755 videos

# Verify path in config
cat playwright-mcp-config.json

# Should be relative: "./videos" not absolute
```

## Debug Mode

### Enable Debug Logging

```python
import logging

# Set debug level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run with debug output
logger = logging.getLogger(__name__)
logger.debug("Debug information here")
```

### Server Debug Mode

```bash
# Start with debug logging
uv run uvicorn app.server.server:app --log-level debug --reload

# Or set in code
import logging
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
```

## Getting Help

### Before Opening an Issue

1. **Search existing issues**: Check if someone else had the same problem
2. **Check logs**: Include relevant log output
3. **Minimal reproduction**: Create minimal code to reproduce the issue
4. **Environment details**: Include OS, Python version, dependency versions

### Information to Include

```bash
# System information
uname -a
python --version
uv --version

# Dependency versions
uv pip list

# Error logs
uv run uvicorn app.server.server:app 2>&1 | tee error.log

# Configuration (redact secrets!)
cat .env | sed 's/=.*/=***/'
```

### Community Resources

- **GitHub Issues**: https://github.com/your-org/tac-webbuilder/issues
- **Documentation**: https://tac-webbuilder.readthedocs.io
- **Examples**: See `examples/` directory

## Additional Resources

- [CLI Documentation](cli.md)
- [Web UI Documentation](web-ui.md)
- [API Documentation](api.md)
- [Architecture Overview](architecture.md)
- [Examples and Tutorials](examples.md)
