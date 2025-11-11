# TAC WebBuilder Architecture

## Overview

TAC WebBuilder is built using a modular architecture that separates concerns and enables extensibility. The system is designed around the Agentic Development Workflow (ADW) concept, providing intelligent automation for web development tasks.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Web UI (React)                       │
│  - Dashboard  - NL Processing  - File Ops  - GitHub     │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/WebSocket
┌──────────────────────┴──────────────────────────────────┐
│                 FastAPI Server (Python)                  │
│  ┌────────────┬────────────┬────────────┬─────────────┐ │
│  │ API Layer  │ Processing │ Integration│ Orchestration│ │
│  └────────────┴────────────┴────────────┴─────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
┌──────┴─────┐ ┌──────┴──────┐ ┌─────┴────┐
│ Core       │ │ External    │ │ Storage  │
│ Modules    │ │ Services    │ │ Layer    │
│            │ │             │ │          │
│ - NL       │ │ - OpenAI    │ │ - SQLite │
│ - File     │ │ - Anthropic │ │ - Files  │
│ - SQL      │ │ - GitHub    │ │ - Temp   │
│ - Project  │ │             │ │          │
└────────────┘ └─────────────┘ └──────────┘
```

## Core Components

### 1. Natural Language Processor (nl_processor.py)

Handles natural language understanding and requirement extraction.

**Responsibilities:**
- Intent analysis (feature, bug, chore)
- Requirement extraction
- Technical approach generation
- Workflow suggestion

**Key Methods:**
- `analyze_intent()` - Classify user intent
- `extract_requirements()` - Extract structured requirements
- `process_request()` - End-to-end processing
- `suggest_adw_workflow()` - Recommend appropriate workflow

### 2. File Processor (file_processor.py)

Manages file format conversions and data processing.

**Responsibilities:**
- CSV to SQLite conversion
- JSON/JSONL to SQLite conversion
- Schema inference
- Data validation and cleaning

**Key Methods:**
- `convert_csv_to_sqlite()`
- `convert_json_to_sqlite()`
- `discover_jsonl_fields()`
- `flatten_json_object()`

### 3. SQL Processor (sql_processor.py)

Provides safe SQL query generation and execution.

**Responsibilities:**
- Natural language to SQL translation
- Query safety validation
- Schema extraction
- Query execution with safety checks

**Key Methods:**
- `get_database_schema()`
- `execute_sql_safely()` - Only allows SELECT
- Dangerous keyword detection

### 4. LLM Processor (llm_processor.py)

Interfaces with Large Language Model APIs.

**Responsibilities:**
- OpenAI and Anthropic API integration
- Provider fallback logic
- Response cleaning and parsing
- Schema formatting for prompts

**Key Methods:**
- `generate_sql()` - Generate SQL from natural language
- Provider selection logic
- Response post-processing

### 5. GitHub Poster (github_poster.py)

Manages GitHub API interactions for issue management.

**Responsibilities:**
- Issue creation
- Repository information retrieval
- GitHub CLI integration
- Authentication management

**Key Methods:**
- `post_issue()` - Create GitHub issues
- `get_repo_info()` - Fetch repository details
- `validate_gh_cli()` - Verify GitHub CLI setup

### 6. Issue Formatter (issue_formatter.py)

Formats issues according to templates and best practices.

**Responsibilities:**
- Markdown formatting
- Template application
- Workflow section generation
- Validation of issue structure

**Key Methods:**
- `format_issue()` - Format complete issue
- `create_feature_issue_body()`
- `create_bug_issue_body()`
- `create_chore_issue_body()`

### 7. Project Detector (project_detector.py)

Analyzes project structure and suggests configurations.

**Responsibilities:**
- Framework detection (React, Next.js, etc.)
- Backend technology identification
- Build tool detection
- Complexity assessment

**Key Methods:**
- `detect_project_context()` - Complete analysis
- `detect_framework()` - Identify frontend framework
- `detect_backend()` - Identify backend technology
- `calculate_complexity()` - Assess project complexity

### 8. Routes Analyzer (routes_analyzer.py)

Analyzes API routes in server files.

**Responsibilities:**
- Route extraction from code
- HTTP method detection
- Endpoint documentation extraction
- Route organization

**Key Methods:**
- `analyze_routes()` - Extract all routes
- AST-based parsing for accuracy

## Data Flow

### 1. Natural Language Processing Flow

```
User Input (Text)
    ↓
NL Processor
    ↓
Intent Analysis → Issue Type
    ↓
Requirement Extraction → Structured Requirements
    ↓
Technical Approach Generation
    ↓
Workflow Suggestion
    ↓
Formatted Output
```

### 2. File Processing Flow

```
File Upload (CSV/JSON)
    ↓
File Processor
    ↓
Format Detection
    ↓
Schema Inference
    ↓
Data Validation & Cleaning
    ↓
SQLite Database Creation
    ↓
Database File Return
```

### 3. SQL Generation Flow

```
Natural Language Question + Database Schema
    ↓
LLM Processor
    ↓
Context Formation
    ↓
LLM API Call (OpenAI/Anthropic)
    ↓
SQL Query Extraction
    ↓
Safety Validation
    ↓
Query Execution (if safe)
    ↓
Results Return
```

### 4. GitHub Issue Creation Flow

```
Issue Data
    ↓
Issue Formatter
    ↓
Template Selection
    ↓
Markdown Formatting
    ↓
GitHub Poster
    ↓
GitHub CLI/API Call
    ↓
Issue URL Return
```

## Technology Stack

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **HTTP Server:** Uvicorn
- **Database:** SQLite (for data processing)
- **Testing:** pytest

### External Services
- **LLM APIs:**
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
- **Version Control:** GitHub API/CLI
- **Browser Automation:** Playwright MCP

### Frontend (if using UI)
- **Framework:** React/Next.js
- **Build Tool:** Vite/Next.js
- **Language:** TypeScript

### Development Tools
- **Package Manager:** uv (Python), npm/bun (JS)
- **Linting:** Ruff (Python), ESLint (JS)
- **Formatting:** Black (Python), Prettier (JS)
- **Type Checking:** mypy (Python), TypeScript

## Security Considerations

### 1. SQL Injection Prevention
- Parameterized queries only
- Whitelist of allowed SQL keywords
- READ-ONLY operations (SELECT only)
- No dynamic table/column names

### 2. API Key Management
- Environment variables for keys
- Never commit keys to version control
- Rotate keys regularly
- Separate keys per environment

### 3. File Processing
- Size limits on uploads
- Validation of file types
- Sandboxed processing
- Temporary file cleanup

### 4. GitHub Integration
- Token with minimal required scopes
- Confirmation before posting issues
- Rate limiting
- Audit logging

## Scalability

### Current Design
- Synchronous processing
- Single-threaded server
- Local file storage
- Suitable for: Individual developers, small teams

### Scaling Options

**Horizontal Scaling:**
- Multiple server instances
- Load balancer
- Shared storage (S3, etc.)
- Redis for caching

**Vertical Scaling:**
- Async processing with `asyncio`
- Background workers (Celery)
- Database connection pooling
- Caching layer

**Database Scaling:**
- Migrate from SQLite to PostgreSQL
- Read replicas
- Connection pooling
- Query optimization

## Extension Points

### 1. Custom LLM Providers
```python
class CustomLLMProvider(LLMProvider):
    def generate_sql(self, question: str, schema: dict) -> str:
        # Custom implementation
        pass
```

### 2. Additional File Formats
```python
class FileProcessor:
    def convert_xml_to_sqlite(self, xml_path: str) -> str:
        # New format support
        pass
```

### 3. Custom Workflows
```python
class CustomWorkflow:
    def execute(self, context: dict) -> dict:
        # Custom workflow logic
        pass
```

### 4. Integration Plugins
```python
class SlackIntegration:
    def post_message(self, message: str):
        # External service integration
        pass
```

## Testing Strategy

### Unit Tests
- Individual function testing
- Mocked external dependencies
- Fast execution (< 1 second per test)

### Integration Tests
- Component interaction testing
- Real database operations
- File system operations
- Moderate execution time

### End-to-End Tests
- Full workflow testing
- Real API calls (with test keys)
- UI automation (Playwright)
- Slower execution

## Deployment

### Development
```bash
uv run uvicorn app.server.server:app --reload
```

### Production
```bash
uv run uvicorn app.server.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["uv", "run", "uvicorn", "app.server.server:app", "--host", "0.0.0.0"]
```

## Monitoring

### Metrics to Track
- Request count and latency
- LLM API usage and costs
- File processing success rate
- GitHub API rate limit status
- Error rates by endpoint

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Log aggregation (e.g., CloudWatch, Datadog)
- Request/response logging

## Future Architecture Considerations

### Microservices Migration
- Separate NL processing service
- Dedicated file processing service
- API gateway pattern
- Service mesh for communication

### Event-Driven Architecture
- Message queue (RabbitMQ, Kafka)
- Async processing
- Event sourcing
- CQRS pattern

### Serverless Options
- Lambda functions for processing
- API Gateway
- S3 for file storage
- DynamoDB for metadata

## Additional Resources

- [CLI Documentation](cli.md)
- [Web UI Documentation](web-ui.md)
- [API Documentation](api.md)
- [Examples and Tutorials](examples.md)
- [Troubleshooting Guide](troubleshooting.md)
