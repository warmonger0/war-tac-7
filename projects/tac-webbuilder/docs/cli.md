# TAC WebBuilder CLI Documentation

## Overview

The TAC WebBuilder Command Line Interface provides powerful tools for creating web applications, managing projects, and automating development workflows.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tac-webbuilder.git
cd tac-webbuilder

# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Basic Usage

### Starting the Server

```bash
# Development mode with auto-reload
uv run uvicorn app.server.server:app --reload

# Production mode
uv run uvicorn app.server.server:app --host 0.0.0.0 --port 8000
```

### Creating a New Project

```bash
# Interactive project creation
./scripts/setup_new_project.sh

# Specify project type
./scripts/setup_new_project.sh --type react-vite --name my-app
```

### Integrating with Existing Projects

```bash
# Add ADW capabilities to existing project
./scripts/integrate_existing.sh /path/to/project
```

## Commands

### Server Commands

#### Start Server
```bash
uv run uvicorn app.server.server:app --reload
```

Start the development server with hot-reload enabled.

**Options:**
- `--host HOST` - Bind to specific host (default: 127.0.0.1)
- `--port PORT` - Bind to specific port (default: 8000)
- `--reload` - Enable auto-reload on code changes

#### Run Tests
```bash
cd app/server && uv run pytest tests/
```

Run the complete test suite.

**Options:**
- `-v` - Verbose output
- `-k PATTERN` - Run tests matching pattern
- `--tb=short` - Short traceback format

### File Processing

#### Convert CSV to SQLite
```bash
uv run python -c "
from core.file_processor import FileProcessor
fp = FileProcessor()
db_path = fp.convert_csv_to_sqlite('data.csv')
print(f'Database created: {db_path}')
"
```

#### Convert JSON to SQLite
```bash
uv run python -c "
from core.file_processor import FileProcessor
fp = FileProcessor()
db_path = fp.convert_json_to_sqlite('data.json')
print(f'Database created: {db_path}')
"
```

### Natural Language Processing

#### Process Requirements
```bash
curl -X POST http://localhost:8000/api/nl/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Create a user authentication system with login and registration"
  }'
```

#### Generate SQL Query
```bash
curl -X POST http://localhost:8000/api/sql/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show me all users created in the last 30 days",
    "schema": {"users": ["id", "username", "created_at"]}
  }'
```

### GitHub Integration

#### Post Issue
```bash
curl -X POST http://localhost:8000/api/github/post-issue \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement user authentication",
    "body": "Feature description...",
    "labels": ["feature", "high-priority"]
  }'
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# GitHub Configuration
GITHUB_TOKEN=ghp_...
GITHUB_REPO=owner/repository

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

### Configuration File

Create a `config.yaml` for advanced configuration:

```yaml
llm:
  provider: anthropic  # or openai
  model: claude-3-5-sonnet-20241022
  temperature: 0.7

github:
  auto_post: false
  default_labels:
    - adw-generated

project:
  default_template: react-vite
  auto_git_init: true
```

## Advanced Usage

### Custom Workflows

Create custom ADW workflows:

```bash
# Create workflow directory
mkdir -p .adw/workflows

# Create custom workflow
cat > .adw/workflows/custom.yaml << EOF
name: Custom Feature Workflow
steps:
  - analyze_requirements
  - generate_issues
  - create_tasks
EOF
```

### Batch Processing

Process multiple files:

```bash
for file in data/*.csv; do
  uv run python -c "
from core.file_processor import FileProcessor
FileProcessor().convert_csv_to_sqlite('$file')
"
done
```

### Integration with Git Hooks

Set up pre-commit hooks:

```bash
# .git/hooks/pre-commit
#!/bin/bash
uv run pytest app/server/tests/
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uv run uvicorn app.server.server:app --port 8001
```

**Module not found errors:**
```bash
# Reinstall dependencies
uv sync --force

# Or
pip install -r requirements.txt --force-reinstall
```

**API key errors:**
```bash
# Verify .env file exists
ls -la .env

# Check environment variables are loaded
uv run python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

## Examples

### Complete Workflow Example

```bash
# 1. Start server
uv run uvicorn app.server.server:app --reload &

# 2. Process requirements
curl -X POST http://localhost:8000/api/nl/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Build a todo app with user auth"}'

# 3. Create GitHub issue
curl -X POST http://localhost:8000/api/github/post-issue \
  -H "Content-Type: application/json" \
  -d @issue.json

# 4. Stop server
pkill -f uvicorn
```

## Best Practices

1. **Use virtual environments**: Always work within uv or venv
2. **Version control**: Commit configuration samples, not secrets
3. **Test before deploy**: Run full test suite before pushing
4. **Monitor logs**: Use `--log-level debug` for troubleshooting
5. **Keep dependencies updated**: Regularly run `uv sync --upgrade`

## Additional Resources

- [Web UI Documentation](web-ui.md)
- [API Documentation](api.md)
- [Architecture Overview](architecture.md)
- [Examples and Tutorials](examples.md)
- [Troubleshooting Guide](troubleshooting.md)
