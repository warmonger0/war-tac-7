# TAC WebBuilder Examples and Tutorials

## Getting Started Examples

### Example 1: Processing a Simple Feature Request

```python
from core.nl_processor import NLProcessor

processor = NLProcessor()
result = await processor.process_request(
    "Create a user profile page with avatar upload and bio editing"
)

print(f"Issue Type: {result['issue_type']}")
print(f"Requirements: {result['requirements']}")
print(f"Workflow: {result['workflow_suggestion']}")
```

**Output:**
```
Issue Type: feature
Requirements: ['User profile display', 'Avatar upload functionality', 'Bio text editing']
Workflow: feature_medium
```

### Example 2: Converting CSV to SQLite

```python
from core.file_processor import FileProcessor

processor = FileProcessor()
db_path = processor.convert_csv_to_sqlite('users.csv', 'users')

# Query the data
from core.sql_processor import SQLProcessor
sql = SQLProcessor()
schema = sql.get_database_schema(db_path)
print(f"Tables: {schema}")
```

### Example 3: Generating SQL from Natural Language

```python
from core.llm_processor import LLMProcessor

processor = LLMProcessor()
query = await processor.generate_sql(
    question="Show me top 10 users by registration date",
    schema={"users": ["id", "username", "created_at"]},
    llm_provider="anthropic"
)

print(f"Generated Query: {query}")
```

### Example 4: Creating a GitHub Issue

```python
from core.github_poster import GitHubPoster
from core.issue_formatter import IssueFormatter

# Format the issue
formatter = IssueFormatter()
formatted = formatter.format_issue({
    "issue_type": "feature",
    "title": "User authentication",
    "requirements": ["Login", "Registration", "Password reset"],
    "technical_approach": "JWT tokens with FastAPI"
})

# Post to GitHub
poster = GitHubPoster(repo="owner/repo")
issue_url = poster.post_issue(
    title=formatted["title"],
    body=formatted["body"],
    labels=["feature"]
)

print(f"Issue created: {issue_url}")
```

## Complete Workflow Examples

### Workflow 1: From Idea to GitHub Issue

```python
import asyncio
from core.nl_processor import NLProcessor
from core.github_poster import GitHubPoster

async def create_issue_from_idea(idea_text: str):
    # Step 1: Process the idea
    processor = NLProcessor()
    analysis = await processor.process_request(idea_text)

    # Step 2: Format the issue
    from core.issue_formatter import IssueFormatter
    formatter = IssueFormatter()
    formatted = formatter.format_issue(analysis)

    # Step 3: Post to GitHub
    poster = GitHubPoster()
    issue_url = poster.post_issue(
        title=formatted["title"],
        body=formatted["body"],
        labels=analysis.get("labels", [])
    )

    return issue_url

# Usage
idea = "Build a dashboard that shows real-time analytics with charts and export to PDF"
issue_url = asyncio.run(create_issue_from_idea(idea))
print(f"Created issue: {issue_url}")
```

### Workflow 2: Data Analysis Pipeline

```python
from core.file_processor import FileProcessor
from core.sql_processor import SQLProcessor
from core.llm_processor import LLMProcessor

# Step 1: Convert data file to SQLite
fp = FileProcessor()
db_path = fp.convert_csv_to_sqlite('sales_data.csv', 'sales')

# Step 2: Get schema
sql = SQLProcessor()
schema = sql.get_database_schema(db_path)

# Step 3: Generate insights with LLM
llm = LLMProcessor()
queries = [
    "What were the top 5 products by revenue?",
    "Show monthly sales trends",
    "Which customers made the most purchases?"
]

for question in queries:
    query = await llm.generate_sql(question, schema, "anthropic")
    results = sql.execute_sql_safely(db_path, query)
    print(f"Q: {question}")
    print(f"A: {results}\n")
```

### Workflow 3: Project Setup and Detection

```python
from core.project_detector import ProjectDetector

# Analyze existing project
detector = ProjectDetector()
context = detector.detect_project_context("/path/to/my-app")

print(f"Framework: {context['framework']}")
print(f"Backend: {context['backend']}")
print(f"Complexity: {context['complexity']}")
print(f"Suggested Workflow: {context['workflow_suggestion']}")

# Based on detection, suggest actions
if context['complexity'] == 'high':
    print("Recommendation: Use feature_heavy workflow")
    print("Consider: Breaking down into multiple smaller issues")
elif context['framework'] is None:
    print("No framework detected - might be vanilla JS project")
```

## API Usage Examples

### Using the REST API

```bash
# Process natural language request
curl -X POST http://localhost:8000/api/nl/process \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Add a search feature with filters and pagination"
  }'

# Convert file to SQLite
curl -X POST http://localhost:8000/api/files/csv-to-sqlite \
  -F "file=@data.csv" \
  -F "table_name=my_data"

# Generate SQL
curl -X POST http://localhost:8000/api/sql/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Show users who signed up this month",
    "database_path": "/tmp/data.db"
  }'

# Create GitHub issue
curl -X POST http://localhost:8000/api/github/post-issue \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implement search feature",
    "body": "Feature description...",
    "labels": ["feature", "enhancement"]
  }'
```

### Python Client Example

```python
import requests

class TACClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def process_nl(self, text: str):
        response = requests.post(
            f"{self.base_url}/api/nl/process",
            json={"text": text}
        )
        return response.json()

    def generate_sql(self, question: str, db_path: str):
        response = requests.post(
            f"{self.base_url}/api/sql/generate",
            json={
                "question": question,
                "database_path": db_path
            }
        )
        return response.json()

# Usage
client = TACClient()
result = client.process_nl("Create a blog system")
print(result)
```

## Advanced Examples

### Custom LLM Integration

```python
from core.llm_processor import LLMProcessor
import anthropic

class CustomLLMProcessor(LLMProcessor):
    async def generate_with_custom_model(self, prompt: str):
        client = anthropic.Anthropic(api_key=self.anthropic_key)

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.5,
            system="You are an expert software architect",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

# Usage
processor = CustomLLMProcessor()
result = await processor.generate_with_custom_model(
    "Design a microservices architecture for e-commerce"
)
```

### Batch Processing

```python
import asyncio
from pathlib import Path
from core.file_processor import FileProcessor

async def batch_convert_files(directory: str):
    fp = FileProcessor()
    csv_files = Path(directory).glob("*.csv")

    tasks = []
    for csv_file in csv_files:
        task = asyncio.to_thread(
            fp.convert_csv_to_sqlite,
            str(csv_file),
            csv_file.stem
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

# Convert all CSV files in directory
results = asyncio.run(batch_convert_files("./data"))
print(f"Converted {len(results)} files")
```

## Integration Examples

### CI/CD Integration

```yaml
# .github/workflows/adw.yml
name: ADW Analysis
on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Analyze PR description
        run: |
          uv run python scripts/analyze_pr.py "${{ github.event.pull_request.body }}"

      - name: Post results
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'ADW Analysis completed!'
            })
```

### VS Code Extension Integration

```typescript
// extension.ts
import * as vscode from 'vscode';
import axios from 'axios';

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand(
    'tac.processSelection',
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;

      const selection = editor.document.getText(editor.selection);

      const response = await axios.post('http://localhost:8000/api/nl/process', {
        text: selection
      });

      vscode.window.showInformationMessage(
        `Issue Type: ${response.data.issue_type}`
      );
    }
  );

  context.subscriptions.push(disposable);
}
```

## Testing Examples

### Unit Test Example

```python
import pytest
from core.nl_processor import NLProcessor

@pytest.mark.asyncio
async def test_feature_detection():
    processor = NLProcessor()
    result = await processor.process_request(
        "Add user authentication with OAuth"
    )

    assert result["issue_type"] == "feature"
    assert "authentication" in str(result["requirements"]).lower()
    assert result["workflow_suggestion"] in ["feature_low", "feature_medium", "feature_heavy"]
```

### Integration Test Example

```python
import pytest
from core.file_processor import FileProcessor
from core.sql_processor import SQLProcessor
import tempfile
import csv

def test_csv_to_sqlite_integration():
    # Create temporary CSV
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'email'])
        writer.writerow([1, 'John', 'john@example.com'])
        csv_path = f.name

    # Convert to SQLite
    fp = FileProcessor()
    db_path = fp.convert_csv_to_sqlite(csv_path, 'users')

    # Query the database
    sql = SQLProcessor()
    results = sql.execute_sql_safely(db_path, "SELECT * FROM users")

    assert len(results["data"]) == 1
    assert results["data"][0][1] == 'John'
```

## Troubleshooting Examples

### Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from core.nl_processor import NLProcessor

processor = NLProcessor()
logger.debug("Starting NL processing...")
result = await processor.process_request("Create a feature")
logger.debug(f"Result: {result}")
```

### Error Handling

```python
from core.github_poster import GitHubPoster

try:
    poster = GitHubPoster()
    poster.post_issue(title="Test", body="Test issue")
except Exception as e:
    print(f"Error posting issue: {e}")
    # Fallback: save to file
    with open('failed_issues.txt', 'a') as f:
        f.write(f"Title: Test\nBody: Test issue\n\n")
```

## Additional Resources

- [CLI Documentation](cli.md)
- [Web UI Documentation](web-ui.md)
- [API Documentation](api.md)
- [Architecture Overview](architecture.md)
- [Troubleshooting Guide](troubleshooting.md)
