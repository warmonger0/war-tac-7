# Integrating ADW into Existing Projects

This guide helps you integrate ADW (Agentic Development Workflow) capabilities into your existing web applications.

## Overview

ADW integration brings powerful automation and development workflow capabilities to your project, including:

- Automated issue creation and tracking
- Natural language processing for requirement extraction
- SQL query generation and data processing
- GitHub integration for automated issue posting
- Project detection and context analysis

## Prerequisites

Before integrating ADW, ensure you have:

1. Python 3.11 or higher
2. A GitHub account with repository access
3. API keys for OpenAI and/or Anthropic (optional but recommended)
4. Git installed and repository initialized

## Integration Steps

### Step 1: Install Dependencies

Add the required dependencies to your project:

```bash
# Using uv (recommended)
uv add fastapi uvicorn python-dotenv anthropic openai

# Or using pip
pip install fastapi uvicorn python-dotenv anthropic openai
```

### Step 2: Configure Environment Variables

Create a `.env` file in your project root:

```bash
# LLM API Keys (at least one required for NL processing)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# GitHub Configuration (optional, for issue posting)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=owner/repository
```

### Step 3: Copy ADW Core Modules

Copy the following directories from this project to your project:

```
your-project/
├── core/
│   ├── file_processor.py
│   ├── llm_processor.py
│   ├── nl_processor.py
│   ├── sql_processor.py
│   ├── github_poster.py
│   ├── issue_formatter.py
│   └── project_detector.py
```

### Step 4: Set Up API Endpoints

Create a basic FastAPI server to expose ADW functionality:

```python
from fastapi import FastAPI
from core.nl_processor import NLProcessor
from core.file_processor import FileProcessor
from core.github_poster import GitHubPoster

app = FastAPI()

@app.post("/api/process-request")
async def process_request(request: dict):
    processor = NLProcessor()
    result = await processor.process_request(request["text"])
    return result

@app.post("/api/convert-file")
async def convert_file(file_path: str):
    processor = FileProcessor()
    result = processor.convert_csv_to_sqlite(file_path)
    return {"database_path": result}
```

### Step 5: Configure MCP Integration

Copy the MCP configuration files:

```bash
cp .mcp.json.sample .mcp.json
cp playwright-mcp-config.json ./
```

Edit `.mcp.json` to match your project structure and requirements.

### Step 6: Test the Integration

Run the server and test the endpoints:

```bash
# Start the server
uvicorn server:app --reload

# Test an endpoint
curl -X POST http://localhost:8000/api/process-request \
  -H "Content-Type: application/json" \
  -d '{"text": "Create a user authentication feature"}'
```

## Framework-Specific Integration

### React/Vue/Angular Projects

For frontend projects, you'll typically integrate ADW as a development tool rather than runtime code:

1. Use ADW for generating issues and planning features
2. Run ADW server separately for development assistance
3. Use MCP integration with Claude Code for enhanced development

### Next.js/Full-Stack Projects

For full-stack projects, you can integrate ADW into your API routes:

```typescript
// app/api/adw/route.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(request: Request) {
  const { text } = await request.json();

  // Call ADW Python backend
  const result = await execAsync(
    `python -c "from core.nl_processor import NLProcessor; print(NLProcessor().process_request('${text}'))"`
  );

  return Response.json(result);
}
```

## Best Practices

1. **Keep ADW separate from production code**: ADW is a development tool, not production infrastructure
2. **Use environment variables**: Never commit API keys or tokens
3. **Configure .gitignore**: Ensure ADW-generated files are properly ignored
4. **Document custom workflows**: If you create custom ADW workflows, document them
5. **Test thoroughly**: Verify ADW integration doesn't interfere with your build process

## Troubleshooting

### Common Issues

**Issue**: Module import errors
- **Solution**: Ensure all core modules are copied and Python path is configured

**Issue**: API key not found
- **Solution**: Check `.env` file exists and contains valid keys

**Issue**: GitHub integration fails
- **Solution**: Verify GitHub token has correct permissions (repo, issues)

**Issue**: MCP server not starting
- **Solution**: Check Node.js is installed and `npx` is available

## Advanced Configuration

### Custom Workflow Integration

You can extend ADW with custom workflows:

```python
from core.nl_processor import NLProcessor

class CustomProcessor(NLProcessor):
    async def custom_workflow(self, text: str):
        # Your custom logic
        result = await self.analyze_intent(text)
        # Additional processing
        return result
```

### Integration with CI/CD

Add ADW to your CI/CD pipeline for automated issue generation:

```yaml
# .github/workflows/adw.yml
name: ADW Integration
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run ADW Analysis
        run: python scripts/analyze_changes.py
```

## Support

For questions or issues with integration:
1. Check the main README.md for general documentation
2. Review examples in the `examples/` directory
3. Open an issue on GitHub for specific problems

## Next Steps

After successful integration:
1. Explore the full ADW API documentation
2. Configure custom workflows for your team
3. Set up automated issue generation
4. Integrate with your existing development tools
