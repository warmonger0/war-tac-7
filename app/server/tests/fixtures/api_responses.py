"""Mock API responses for testing Claude API integration."""

import json

# Successful intent analysis responses
INTENT_FEATURE_RESPONSE = json.dumps({
    "intent_type": "feature",
    "summary": "Add dark mode to the application",
    "technical_area": "UI"
})

INTENT_BUG_RESPONSE = json.dumps({
    "intent_type": "bug",
    "summary": "Login button is not responding to clicks",
    "technical_area": "authentication"
})

INTENT_CHORE_RESPONSE = json.dumps({
    "intent_type": "chore",
    "summary": "Update dependencies to latest versions",
    "technical_area": "maintenance"
})

# Successful requirement extraction responses
REQUIREMENTS_AUTH_RESPONSE = json.dumps([
    "Implement JWT authentication",
    "Create login form with email and password fields",
    "Add password hashing with bcrypt",
    "Implement session management"
])

REQUIREMENTS_DARKMODE_RESPONSE = json.dumps([
    "Create theme toggle component",
    "Add CSS variables for light/dark themes",
    "Persist theme preference in localStorage",
    "Update all components to respect theme"
])

# Responses with markdown code blocks (should be cleaned)
INTENT_WITH_MARKDOWN = f"""```json
{INTENT_FEATURE_RESPONSE}
```"""

REQUIREMENTS_WITH_MARKDOWN = f"""```json
{REQUIREMENTS_AUTH_RESPONSE}
```"""

# Edge case responses
INTENT_EMPTY_TECHNICAL_AREA = json.dumps({
    "intent_type": "feature",
    "summary": "Generic task",
    "technical_area": ""
})

REQUIREMENTS_EMPTY_LIST = json.dumps([])

REQUIREMENTS_SINGLE_ITEM = json.dumps([
    "Single requirement"
])

REQUIREMENTS_VERY_LONG = json.dumps([
    f"Requirement {i}: This is a very detailed requirement with lots of text"
    for i in range(50)
])

# Unicode and special character responses
INTENT_UNICODE = json.dumps({
    "intent_type": "feature",
    "summary": "Add support for emoji reactions 🎉 and internationalization (中文, 日本語)",
    "technical_area": "i18n"
})

REQUIREMENTS_SPECIAL_CHARS = json.dumps([
    "Handle markdown **bold** and _italic_ text",
    "Support HTML entities &lt; &gt; &amp;",
    "Process URLs https://example.com correctly",
    "Handle quotes \"double\" and 'single'"
])

# Malformed responses (invalid JSON)
MALFORMED_JSON_RESPONSE = "This is not valid JSON {invalid"

MALFORMED_JSON_MISSING_BRACE = '{"intent_type": "feature", "summary": "Test"'

MALFORMED_JSON_EXTRA_COMMA = '{"intent_type": "feature", "summary": "Test",}'

# Responses with extra whitespace
INTENT_WITH_WHITESPACE = f"""

{INTENT_FEATURE_RESPONSE}

"""

# Responses with nested markdown blocks
INTENT_NESTED_MARKDOWN = f"""```json
```json
{INTENT_FEATURE_RESPONSE}
```
```"""

# Very long input response
INTENT_VERY_LONG_SUMMARY = json.dumps({
    "intent_type": "feature",
    "summary": "A " + "very " * 100 + "long summary",
    "technical_area": "general"
})

# Response with all optional fields
INTENT_ALL_FIELDS = json.dumps({
    "intent_type": "feature",
    "summary": "Complete feature request",
    "technical_area": "fullstack",
    "complexity": "high",
    "estimated_effort": "3 days",
    "dependencies": ["auth", "database"]
})

# API error responses
API_ERROR_RATE_LIMIT = {
    "error": "rate_limit_exceeded",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
}

API_ERROR_AUTH = {
    "error": "invalid_api_key",
    "message": "The provided API key is invalid or has been revoked."
}

API_ERROR_TIMEOUT = {
    "error": "timeout",
    "message": "The request timed out. Please try again."
}

API_ERROR_SERVER = {
    "error": "server_error",
    "message": "An internal server error occurred. Please try again later."
}

# Empty and whitespace-only responses
RESPONSE_EMPTY = ""
RESPONSE_WHITESPACE_ONLY = "   \n  \t  \n  "
RESPONSE_NULL = "null"

# Injection attempt responses (for security testing)
INTENT_XSS_ATTEMPT = json.dumps({
    "intent_type": "feature",
    "summary": "<script>alert('XSS')</script>",
    "technical_area": "security"
})

INTENT_SQL_INJECTION_ATTEMPT = json.dumps({
    "intent_type": "bug",
    "summary": "'; DROP TABLE users; --",
    "technical_area": "database"
})

REQUIREMENTS_MARKDOWN_INJECTION = json.dumps([
    "[Link](javascript:alert('XSS'))",
    "![Image](javascript:alert('XSS'))",
    "# Heading with <script>alert('XSS')</script>"
])
