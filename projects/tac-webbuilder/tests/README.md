# Test Suite Documentation

Comprehensive test suite for the Natural Language Processing module with >90% code coverage.

## Table of Contents

- [Overview](#overview)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Coverage Reports](#coverage-reports)
- [Test Categories](#test-categories)
- [Writing New Tests](#writing-new-tests)
- [Best Practices](#best-practices)

## Overview

This test suite provides comprehensive coverage for the NL processing module, including:
- Unit tests for all core modules
- Integration tests for end-to-end workflows
- Performance benchmarks
- Edge case and error handling tests
- Fixtures for reusable test data

### Coverage Goals

- **Target**: >90% line coverage for all core modules
- **nl_processor.py**: 95%+ coverage
- **issue_formatter.py**: 95%+ coverage
- **project_detector.py**: 90%+ coverage

## Running Tests

### Run All Tests

```bash
cd app/server
uv run pytest
```

### Run Specific Test Files

```bash
# NL Processor tests
uv run pytest tests/core/test_nl_processor.py -v

# Issue Formatter tests
uv run pytest tests/core/test_issue_formatter.py -v

# Project Detector tests
uv run pytest tests/core/test_project_detector.py -v

# Integration tests
uv run pytest tests/test_nl_workflow_integration.py -v

# Performance tests
uv run pytest tests/performance/ -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
uv run pytest --cov=core --cov-report=term --cov-report=html

# View HTML report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

### Run Specific Test Classes or Methods

```bash
# Run a specific test class
uv run pytest tests/core/test_nl_processor.py::TestNLProcessorEdgeCases -v

# Run a specific test method
uv run pytest tests/core/test_nl_processor.py::TestNLProcessor::test_analyze_intent_feature -v

# Run tests matching a pattern
uv run pytest -k "edge_case" -v
```

## Test Structure

```
tests/
├── __init__.py
├── README.md                           # This file
├── conftest.py                         # Shared pytest fixtures
├── fixtures/                           # Test data fixtures
│   ├── __init__.py
│   ├── api_responses.py               # Mock API responses
│   └── project_samples.py             # Sample project structures
├── core/                              # Unit tests
│   ├── test_nl_processor.py          # NL processor tests (52 tests)
│   ├── test_issue_formatter.py       # Issue formatter tests (70 tests)
│   ├── test_project_detector.py      # Project detector tests (90 tests)
│   └── ...
├── performance/                       # Performance benchmarks
│   └── test_nl_performance.py        # Performance tests
└── test_nl_workflow_integration.py   # Integration tests (17 tests)
```

## Coverage Reports

### Latest Coverage Summary

```
Module                    Stmts   Miss  Cover
--------------------------------------------
core/nl_processor.py        71      5    93%
core/issue_formatter.py     44      2    95%
core/project_detector.py   179     18    90%
--------------------------------------------
TOTAL                      294     25    91%
```

### Viewing Coverage Details

1. Run tests with coverage: `uv run pytest --cov=core --cov-report=html`
2. Open the HTML report: `open htmlcov/index.html`
3. Click on any module to see line-by-line coverage

### Uncovered Code

Most uncovered code is:
- Error handling paths that are difficult to trigger
- Edge cases in markdown cleaning
- Optional validation logic

## Test Categories

### Unit Tests

#### NL Processor Tests (`test_nl_processor.py`)

**Basic Tests (19 tests)**
- Intent analysis for feature/bug/chore
- Requirement extraction
- Issue classification
- Workflow suggestion
- End-to-end request processing

**Edge Case Tests (33 tests)**
- Empty and whitespace-only input
- Very long input (10,000+ characters)
- Unicode characters and emojis
- Special characters and markdown
- Malformed JSON responses
- XSS and SQL injection attempts
- API errors and rate limiting
- Missing fields and None values
- All workflow/complexity combinations

#### Issue Formatter Tests (`test_issue_formatter.py`)

**Basic Tests (33 tests)**
- Requirement list formatting
- Technical approach formatting
- Workflow section formatting
- Feature/bug/chore issue creation
- Template validation

**Edge Case Tests (37 tests)**
- Unicode and emoji handling
- Very long requirements lists (100+ items)
- Special character escaping
- HTML injection prevention
- Missing template variables
- Invalid classification types
- Empty and None value handling

#### Project Detector Tests (`test_project_detector.py`)

**Basic Tests (44 tests)**
- Framework detection (React, Vue, Next.js, Angular, etc.)
- Backend detection (FastAPI, Express, Flask, etc.)
- Build tool detection
- Package manager detection
- Git initialization check
- Complexity calculation

**Edge Case Tests (46 tests)**
- Corrupted configuration files
- Mixed framework scenarios
- Permission errors
- Non-existent paths
- Symbolic links
- Very large project structures
- Additional framework support (Svelte, Solid.js, Remix, Nuxt, NestJS, Fastify, Hono)
- Monorepo detection

### Integration Tests (`test_nl_workflow_integration.py`)

**Basic Integration (7 tests)**
- Complete NL-to-issue workflow
- Project context detection integration
- Bug report workflow
- Chore workflow
- High complexity feature workflow
- GitHub posting integration (mocked)

**Failure Scenarios (10 tests)**
- Partial API failures
- Malformed API responses
- Empty requirements handling
- API rate limit errors
- Very long input handling
- Project detection failures
- Unicode in NL input
- Concurrent workflow isolation
- Multiple project type testing

### Performance Tests (`test_nl_performance.py`)

**NL Processor Performance (5 tests)**
- Small input (<100 chars): <1s
- Medium input (100-1000 chars): <1s
- Large input (1000-10000 chars): <2s
- Requirement extraction: <1s
- Large requirements list (50+ items): <1s

**Project Detector Performance (4 tests)**
- Small projects (<10 files): <0.5s
- Medium projects (10-50 files): <1s
- Large projects (100+ files): <2s
- Monorepo structures: <1.5s

**Issue Formatter Performance (4 tests)**
- Small issues (<5 requirements): <0.1s
- Medium issues (10-20 requirements): <0.2s
- Large issues (50+ requirements): <0.5s
- Very long text fields: <0.3s

**End-to-End Performance (3 tests)**
- Complete workflow: <2s (mocked)
- Concurrent requests (3x): <3s
- Memory usage validation

## Writing New Tests

### Test File Template

```python
import pytest
from unittest.mock import patch, MagicMock
from core.module_name import function_to_test
from tests.fixtures import api_responses, project_samples


class TestModuleName:
    """Tests for module_name functionality."""

    def test_basic_functionality(self):
        """Test basic happy path."""
        result = function_to_test("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case with special input."""
        result = function_to_test("")
        assert result is not None


class TestModuleNameEdgeCases:
    """Comprehensive edge case tests."""

    @pytest.mark.parametrize("input,expected", [
        ("case1", "result1"),
        ("case2", "result2"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple input variations."""
        result = function_to_test(input)
        assert result == expected
```

### Using Fixtures

```python
def test_with_project_fixture(react_vite_project):
    """Test using a project fixture."""
    context = detect_project_context(str(react_vite_project))
    assert context.framework == "react-vite"

def test_with_mock_api(mock_anthropic_client):
    """Test using mock API client fixture."""
    mock_client, mock_response = mock_anthropic_client
    # Configure mock response
    mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
    # Use in test
```

### Mocking Best Practices

```python
# Mock external API calls
@patch('core.nl_processor.Anthropic')
async def test_with_mocked_api(mock_anthropic_class):
    mock_client = MagicMock()
    mock_anthropic_class.return_value = mock_client
    # Configure mock responses
    mock_response = MagicMock()
    mock_response.content[0].text = json.dumps({"key": "value"})
    mock_client.messages.create.return_value = mock_response
    # Test function

# Mock environment variables
with patch.dict('os.environ', {'API_KEY': 'test-key'}):
    result = function_requiring_api_key()

# Mock file system operations
@patch('pathlib.Path.exists')
def test_file_operations(mock_exists):
    mock_exists.return_value = True
    # Test function
```

## Best Practices

### 1. Test Naming

- Use descriptive test names that explain what is being tested
- Follow the pattern: `test_<function>_<scenario>_<expected>`
- Examples:
  - `test_analyze_intent_feature_returns_valid_intent`
  - `test_extract_requirements_empty_input_raises_error`
  - `test_format_issue_missing_template_field_raises_exception`

### 2. Test Organization

- Group related tests in classes
- Use separate classes for edge cases (`TestModuleNameEdgeCases`)
- Keep test files focused on single modules
- Use `conftest.py` for shared fixtures

### 3. Assertions

- Use specific assertions with clear messages
- Test both positive and negative cases
- Verify error messages contain expected text
- Check all relevant properties of returned objects

```python
# Good
assert result.framework == "react-vite"
assert "Error analyzing intent" in str(exc_info.value)
assert len(requirements) > 0

# Avoid
assert result  # Too vague
assert True  # Meaningless
```

### 4. Mocking

- Mock external dependencies (APIs, file system, network)
- Don't mock the code under test
- Use fixtures for commonly mocked objects
- Verify mocks were called correctly

```python
mock_client.messages.create.assert_called_once()
assert mock_execute.call_count == 3
```

### 5. Fixtures

- Use pytest fixtures for test data and setup
- Leverage shared fixtures in `conftest.py`
- Use `tmp_path` fixture for file system tests
- Create reusable fixtures in `tests/fixtures/`

### 6. Parametrization

- Use `@pytest.mark.parametrize` for testing multiple inputs
- Reduces code duplication
- Makes test cases more readable

```python
@pytest.mark.parametrize("input,expected", [
    ("feature", "adw_sdlc_iso"),
    ("bug", "adw_plan_build_test_iso"),
    ("chore", "adw_sdlc_iso"),
])
def test_workflow_suggestions(input, expected):
    workflow, _ = suggest_adw_workflow(input, "low")
    assert workflow == expected
```

### 7. Test Independence

- Each test should be independent
- Don't rely on test execution order
- Clean up resources in teardown
- Use fixtures for test isolation

### 8. Performance Tests

- Set clear performance thresholds
- Document expected performance targets
- Use mocked APIs for consistent timing
- Test both small and large inputs

### 9. Edge Cases

- Test boundary conditions
- Test with None, empty, and invalid inputs
- Test error paths and exceptions
- Test Unicode, special characters, and very long inputs

### 10. Documentation

- Add clear docstrings to all test methods
- Document what is being tested and why
- Explain any complex test setup
- Update this README when adding new test categories

## Common Patterns

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test an async function."""
    result = await async_function()
    assert result is not None
```

### Exception Testing

```python
def test_function_raises_error():
    """Test that function raises expected error."""
    with pytest.raises(ValueError) as exc_info:
        function_that_should_fail()
    assert "expected error message" in str(exc_info.value)
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiple_inputs(input, expected):
    """Test with multiple input/output pairs."""
    assert double(input) == expected
```

### Fixture Usage

```python
@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return {"key": "value"}

def test_with_fixture(sample_data):
    """Test using fixture data."""
    assert sample_data["key"] == "value"
```

## Troubleshooting

### Tests Fail Due to Import Errors

- Ensure you're in the correct directory: `cd app/server`
- Verify dependencies are installed: `uv sync`
- Check Python path: `uv run python -c "import core"`

### Tests Timeout

- Check for infinite loops in code under test
- Verify mocks are configured correctly
- Ensure async functions are properly awaited

### Coverage Not Improving

- Check if code paths are actually exercised
- Verify mocks aren't preventing code execution
- Use `pytest --cov=core --cov-report=term-missing` to see uncovered lines

### Flaky Tests

- Check for race conditions in async code
- Verify tests don't depend on external state
- Use proper mocking for time-dependent code
- Ensure proper cleanup in fixtures

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

- Fast execution (<60 seconds for full suite)
- No external dependencies (all APIs mocked)
- Deterministic results (no flaky tests)
- Clear failure messages

### CI Configuration Example

```yaml
- name: Run tests
  run: |
    cd app/server
    uv sync
    uv run pytest --cov=core --cov-report=term --cov-report=xml

- name: Check coverage
  run: |
    cd app/server
    uv run pytest --cov=core --cov-report=term --cov-fail-under=90
```

## Contributing

When adding new features:

1. Write tests first (TDD approach recommended)
2. Aim for >90% coverage of new code
3. Add edge case tests for error conditions
4. Update this README if adding new test categories
5. Run full test suite before submitting PR

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-cov documentation](https://pytest-cov.readthedocs.io/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html)
