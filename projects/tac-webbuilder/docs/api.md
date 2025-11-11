# TAC WebBuilder API Documentation

## Overview

The TAC WebBuilder API provides RESTful endpoints for natural language processing, file conversion, SQL generation, and GitHub integration.

**Base URL:** `http://localhost:8000/api`

## Authentication

Most endpoints require authentication via API keys configured in environment variables. Some endpoints may require GitHub authentication.

### Setting Up Authentication

```bash
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
```

## Endpoints

### Natural Language Processing

#### Process Natural Language Request

```http
POST /api/nl/process
Content-Type: application/json

{
  "text": "Create a user authentication system with login and registration",
  "project_path": "/path/to/project" // optional
}
```

**Response:**
```json
{
  "issue_type": "feature",
  "title": "Implement user authentication system",
  "requirements": [
    "Email/password login functionality",
    "User registration with validation",
    "Session management"
  ],
  "technical_approach": "Implement using FastAPI with JWT tokens...",
  "workflow_suggestion": "feature_medium",
  "complexity": "medium"
}
```

**Status Codes:**
- `200 OK` - Successfully processed
- `400 Bad Request` - Invalid input
- `500 Internal Server Error` - Processing failed

#### Analyze Intent

```http
POST /api/nl/analyze-intent
Content-Type: application/json

{
  "text": "Fix the bug where users can't upload files"
}
```

**Response:**
```json
{
  "intent": "bug_report",
  "confidence": 0.95,
  "keywords": ["bug", "upload", "files"],
  "suggested_labels": ["bug", "file-upload"]
}
```

### File Processing

#### Convert CSV to SQLite

```http
POST /api/files/csv-to-sqlite
Content-Type: multipart/form-data

file: <csv_file>
table_name: users // optional
```

**Response:**
```json
{
  "success": true,
  "database_path": "/tmp/data_1234.db",
  "table_name": "users",
  "rows_processed": 1500,
  "schema": {
    "id": "INTEGER",
    "username": "TEXT",
    "email": "TEXT",
    "created_at": "TEXT"
  }
}
```

#### Convert JSON to SQLite

```http
POST /api/files/json-to-sqlite
Content-Type: multipart/form-data

file: <json_file>
table_name: products // optional
flatten: true // optional
```

**Response:**
```json
{
  "success": true,
  "database_path": "/tmp/data_5678.db",
  "table_name": "products",
  "rows_processed": 500,
  "schema": {
    "id": "INTEGER",
    "name": "TEXT",
    "price": "REAL",
    "category": "TEXT"
  }
}
```

#### Get Database Schema

```http
GET /api/files/schema?db_path=/path/to/database.db
```

**Response:**
```json
{
  "tables": {
    "users": {
      "columns": ["id", "username", "email", "created_at"],
      "types": ["INTEGER", "TEXT", "TEXT", "TEXT"],
      "row_count": 1500
    },
    "posts": {
      "columns": ["id", "user_id", "title", "content"],
      "types": ["INTEGER", "INTEGER", "TEXT", "TEXT"],
      "row_count": 3200
    }
  }
}
```

### SQL Query Generation

#### Generate SQL Query

```http
POST /api/sql/generate
Content-Type: application/json

{
  "question": "Show me all users who registered in the last 30 days",
  "database_path": "/path/to/database.db",
  "llm_provider": "anthropic" // optional: "openai" or "anthropic"
}
```

**Response:**
```json
{
  "query": "SELECT * FROM users WHERE created_at >= date('now', '-30 days')",
  "explanation": "This query selects all user records where the created_at date is within the last 30 days",
  "estimated_rows": 150
}
```

#### Execute SQL Query

```http
POST /api/sql/execute
Content-Type: application/json

{
  "query": "SELECT * FROM users LIMIT 10",
  "database_path": "/path/to/database.db"
}
```

**Response:**
```json
{
  "success": true,
  "columns": ["id", "username", "email"],
  "data": [
    [1, "john_doe", "john@example.com"],
    [2, "jane_smith", "jane@example.com"]
  ],
  "row_count": 10,
  "execution_time_ms": 5
}
```

**Note:** Only SELECT queries are allowed for security reasons.

### GitHub Integration

#### Post Issue

```http
POST /api/github/post-issue
Content-Type: application/json

{
  "title": "Implement user authentication",
  "body": "## Description\n\nImplement a complete user authentication system...",
  "labels": ["feature", "high-priority"],
  "repository": "owner/repo", // optional, uses default if not provided
  "confirm": false // if true, requires user confirmation
}
```

**Response:**
```json
{
  "success": true,
  "issue_number": 42,
  "issue_url": "https://github.com/owner/repo/issues/42",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Repository Info

```http
GET /api/github/repo-info?repo=owner/repo
```

**Response:**
```json
{
  "name": "repo",
  "owner": "owner",
  "full_name": "owner/repo",
  "description": "Repository description",
  "default_branch": "main",
  "open_issues": 15,
  "is_private": false
}
```

#### List Issues

```http
GET /api/github/issues?repo=owner/repo&state=open&labels=feature,bug
```

**Response:**
```json
{
  "issues": [
    {
      "number": 42,
      "title": "Implement user authentication",
      "state": "open",
      "labels": ["feature", "high-priority"],
      "created_at": "2024-01-15T10:30:00Z",
      "url": "https://github.com/owner/repo/issues/42"
    }
  ],
  "total_count": 1
}
```

### Project Detection

#### Detect Project Context

```http
POST /api/project/detect
Content-Type: application/json

{
  "project_path": "/path/to/project"
}
```

**Response:**
```json
{
  "framework": "react-vite",
  "backend": "fastapi",
  "build_tools": ["vite", "npm"],
  "package_manager": "npm",
  "has_git": true,
  "complexity": "medium",
  "suggested_workflow": "feature_medium",
  "file_count": 150,
  "languages": ["TypeScript", "Python"]
}
```

#### Analyze Routes

```http
POST /api/project/analyze-routes
Content-Type: application/json

{
  "server_file_path": "/path/to/server.py"
}
```

**Response:**
```json
{
  "routes": [
    {
      "path": "/api/users",
      "methods": ["GET", "POST"],
      "description": "User management endpoints",
      "parameters": ["id", "username"]
    },
    {
      "path": "/api/posts",
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "description": "Post CRUD operations"
    }
  ]
}
```

### Issue Formatting

#### Format Issue

```http
POST /api/issues/format
Content-Type: application/json

{
  "issue_type": "feature",
  "title": "User authentication",
  "requirements": ["Login", "Registration", "Password reset"],
  "technical_approach": "Use JWT tokens with FastAPI",
  "workflow": "feature_medium"
}
```

**Response:**
```json
{
  "formatted_body": "## Description\n\n...\n\n## Requirements\n\n- [ ] Login\n...",
  "title": "Implement user authentication",
  "labels": ["feature", "medium-complexity"]
}
```

## Error Handling

All endpoints follow a consistent error format:

```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

- `INVALID_INPUT` - Request data is invalid or missing required fields
- `AUTH_FAILED` - Authentication or authorization failed
- `NOT_FOUND` - Requested resource not found
- `PROCESSING_ERROR` - Error during processing operation
- `DB_ERROR` - Database operation failed
- `LLM_ERROR` - LLM API call failed
- `GITHUB_ERROR` - GitHub API operation failed

## Rate Limiting

API endpoints are rate limited to prevent abuse:

- **General endpoints:** 100 requests per minute
- **LLM endpoints:** 20 requests per minute (due to external API limits)
- **File upload endpoints:** 10 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248600
```

## Pagination

Endpoints returning lists support pagination:

```http
GET /api/github/issues?page=2&per_page=25
```

Response includes pagination metadata:
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 25,
    "total_pages": 5,
    "total_items": 120
  }
}
```

## Webhooks

Configure webhooks to receive notifications:

```http
POST /api/webhooks/configure
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["issue.created", "processing.completed"],
  "secret": "your-webhook-secret"
}
```

### Webhook Events

- `issue.created` - New GitHub issue created
- `issue.updated` - Issue updated
- `processing.completed` - NL processing completed
- `file.processed` - File conversion completed
- `query.generated` - SQL query generated

## Client Libraries

### Python

```python
import requests

class TACWebBuilderClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def process_nl(self, text):
        response = requests.post(
            f"{self.base_url}/api/nl/process",
            json={"text": text}
        )
        return response.json()

# Usage
client = TACWebBuilderClient()
result = client.process_nl("Create a todo app")
```

### JavaScript/TypeScript

```typescript
class TACWebBuilderClient {
  constructor(private baseUrl = 'http://localhost:8000') {}

  async processNL(text: string) {
    const response = await fetch(`${this.baseUrl}/api/nl/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    return response.json();
  }
}

// Usage
const client = new TACWebBuilderClient();
const result = await client.processNL('Create a todo app');
```

## Best Practices

1. **Use appropriate LLM provider**: Choose based on your needs and API limits
2. **Handle errors gracefully**: Always check response status and handle errors
3. **Respect rate limits**: Implement exponential backoff for retries
4. **Validate input**: Sanitize and validate data before sending
5. **Cache responses**: Cache results when appropriate to reduce API calls
6. **Use webhooks**: For long-running operations, use webhooks instead of polling

## Additional Resources

- [CLI Documentation](cli.md)
- [Web UI Documentation](web-ui.md)
- [Architecture Overview](architecture.md)
- [Examples and Tutorials](examples.md)
- [Troubleshooting Guide](troubleshooting.md)
