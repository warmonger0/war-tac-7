# NL Processing Examples

This directory contains working examples demonstrating how to use the Natural Language Processing system.

## Overview of Examples

### Basic Examples
- **basic_usage.py** - Simple end-to-end example showing the complete workflow
- **example_inputs.json** - Sample natural language inputs for different scenarios
- **example_outputs.json** - Expected outputs for the sample inputs

### Advanced Examples
- **advanced_usage.py** - Complex scenarios with error handling and customization
- **edge_cases.py** - Examples of edge cases and how the system handles them

## How to Run Examples

### Prerequisites

1. Install dependencies:
   ```bash
   cd /path/to/tac-webbuilder
   uv sync
   ```

2. Set environment variables:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
   export GITHUB_REPO_URL="owner/repo"  # Optional
   ```

3. Authenticate with GitHub CLI:
   ```bash
   gh auth login
   ```

### Running Basic Example

```bash
cd examples/nl-processing
python basic_usage.py
```

This will:
1. Detect project context from a sample directory
2. Process a simple natural language request
3. Display the generated GitHub issue
4. (Optionally) post to GitHub with confirmation

### Running Advanced Example

```bash
python advanced_usage.py
```

This demonstrates:
- Error handling and recovery
- Custom workflow overrides
- Batch processing multiple requests
- Working with different project types

### Running Edge Cases Example

```bash
python edge_cases.py
```

This shows how the system handles:
- Empty or very short input
- Ambiguous requests
- Invalid project paths
- Projects without standard configuration files
- Markdown special characters

## Example Files

### basic_usage.py
Demonstrates the simplest possible usage:
- Detect project context
- Process natural language
- Generate and preview issue
- Post to GitHub (optional)

### advanced_usage.py
Shows advanced features:
- Error handling with try/except
- Retry logic for API failures
- Custom workflow selection
- Batch processing
- Different project types

### edge_cases.py
Handles special scenarios:
- Invalid inputs
- Missing dependencies
- API errors
- Ambiguous requests

### example_inputs.json
Sample inputs organized by category:
- Feature requests (simple, medium, complex)
- Bug reports
- Chore/maintenance tasks
- Edge cases

### example_outputs.json
Expected outputs for each input:
- Generated titles
- Issue bodies
- Classifications
- Workflow recommendations
- Labels

## Testing Examples

You can run examples as tests:

```bash
# Validate example scripts are syntactically correct
python -m py_compile basic_usage.py
python -m py_compile advanced_usage.py
python -m py_compile edge_cases.py

# Validate JSON files
python -c "import json; json.load(open('example_inputs.json'))"
python -c "import json; json.load(open('example_outputs.json'))"
```

## Modifying Examples

Feel free to modify these examples for your own use:

1. Change the natural language inputs
2. Adjust project paths to your own projects
3. Customize workflow recommendations
4. Add new scenarios

## Common Issues

### Import Errors

If you get import errors, make sure you're running from the correct directory:

```bash
cd /path/to/tac-webbuilder
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python examples/nl-processing/basic_usage.py
```

### API Key Errors

Verify your API key is set:
```bash
echo $ANTHROPIC_API_KEY
```

### GitHub CLI Errors

Check authentication:
```bash
gh auth status
```

## Next Steps

- Read the [API Reference](../../docs/api/nl-processing.md)
- Check the [Usage Guide](../../docs/guides/nl-processing-guide.md)
- Explore the [Architecture Documentation](../../docs/architecture/nl-processing-architecture.md)
