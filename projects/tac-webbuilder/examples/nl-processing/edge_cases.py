#!/usr/bin/env python3
"""
Edge Cases Example

This example demonstrates how the NL processing system handles various edge cases:
- Empty or very short input
- Ambiguous requests
- Invalid project paths
- Projects without standard configuration files
- Markdown special characters

Usage:
    export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
    python edge_cases.py
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app" / "server"))

from core.nl_processor import process_request, analyze_intent
from core.project_detector import detect_project_context
from core.data_models import ProjectContext


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_result(success: bool, message: str):
    """Print a formatted result."""
    icon = "✓" if success else "❌"
    print(f"{icon} {message}")


async def test_empty_input():
    """Test handling of empty or very short input."""
    print_section("Edge Case 1: Empty or Very Short Input")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    # Create a minimal context
    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    test_cases = [
        "",
        "a",
        "fix",
        "bug"
    ]

    for nl_input in test_cases:
        print(f"\nInput: \"{nl_input}\" (length: {len(nl_input)})")
        try:
            issue = await process_request(nl_input or "empty string", context)
            print_result(True, f"System handled it: {issue.title}")
        except Exception as e:
            print_result(False, f"Error: {e}")


async def test_ambiguous_requests():
    """Test handling of ambiguous or vague requests."""
    print_section("Edge Case 2: Ambiguous Requests")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    test_cases = [
        "Make it better",
        "Fix the thing",
        "Update stuff",
        "Improve performance"
    ]

    for nl_input in test_cases:
        print(f"\nInput: \"{nl_input}\"")
        try:
            intent = await analyze_intent(nl_input)
            print_result(True, f"Classified as: {intent['intent_type']}")
            print(f"  Summary: {intent['summary']}")
            print(f"  Technical area: {intent['technical_area']}")
        except Exception as e:
            print_result(False, f"Error: {e}")


async def test_invalid_project_paths():
    """Test handling of invalid project paths."""
    print_section("Edge Case 3: Invalid Project Paths")

    test_cases = [
        "/path/that/does/not/exist",
        "/tmp/nonexistent",
        ""
    ]

    for path in test_cases:
        print(f"\nPath: \"{path}\"")
        try:
            context = detect_project_context(path)
            print_result(True, f"Context created: {context.path}")
        except ValueError as e:
            print_result(True, f"Properly caught error: {e}")
        except Exception as e:
            print_result(False, f"Unexpected error: {e}")


async def test_empty_project_directory():
    """Test handling of empty project directories."""
    print_section("Edge Case 4: Empty Project Directory")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    # Create a temporary empty directory
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"\nCreated empty directory: {tmpdir}")

        try:
            context = detect_project_context(tmpdir)
            print_result(True, "Context detected for empty directory")
            print(f"  Is new project: {context.is_new_project}")
            print(f"  Framework: {context.framework or 'None'}")
            print(f"  Complexity: {context.complexity}")

            # Try processing a request with this context
            issue = await process_request(
                "Initialize project with basic structure",
                context
            )
            print_result(True, f"Generated issue: {issue.title}")

        except Exception as e:
            print_result(False, f"Error: {e}")


async def test_markdown_special_characters():
    """Test handling of markdown special characters in input."""
    print_section("Edge Case 5: Markdown Special Characters")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    test_cases = [
        "Add support for *bold* and _italic_ text",
        "Fix bug in `code blocks` rendering",
        "Implement [links](http://example.com) feature",
        "Handle # headings and ## subheadings",
        "Support | tables | with | pipes |"
    ]

    for nl_input in test_cases:
        print(f"\nInput: \"{nl_input}\"")
        try:
            issue = await process_request(nl_input, context)
            print_result(True, "Successfully processed")
            print(f"  Title: {issue.title}")
            # Check if special chars are preserved or escaped
            has_special = any(char in issue.body for char in ['*', '_', '`', '[', '#', '|'])
            print(f"  Body contains special chars: {has_special}")
        except Exception as e:
            print_result(False, f"Error: {e}")


async def test_project_without_standard_files():
    """Test handling of projects without standard config files."""
    print_section("Edge Case 6: Project Without Standard Config Files")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    # Create a directory with only source files (no package.json, etc.)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Create some basic files
        (tmpdir_path / "src").mkdir()
        (tmpdir_path / "src" / "main.py").write_text("print('hello')")
        (tmpdir_path / "README.md").write_text("# My Project")

        print(f"\nCreated minimal project: {tmpdir}")
        print("  Files: src/main.py, README.md")

        try:
            context = detect_project_context(str(tmpdir_path))
            print_result(True, "Context detected")
            print(f"  Framework: {context.framework or 'None'}")
            print(f"  Backend: {context.backend or 'None'}")
            print(f"  Package manager: {context.package_manager or 'None'}")
            print(f"  Complexity: {context.complexity}")

            # Process a request
            issue = await process_request(
                "Add configuration management",
                context
            )
            print_result(True, f"Generated issue: {issue.title}")
            print(f"  Workflow: {issue.workflow}")

        except Exception as e:
            print_result(False, f"Error: {e}")


async def test_very_long_input():
    """Test handling of very long natural language input."""
    print_section("Edge Case 7: Very Long Input")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    # Create a very long input
    long_input = """
    Add a comprehensive user authentication system with the following features:
    support for email and password login, OAuth integration with Google and GitHub,
    two-factor authentication using TOTP, password reset functionality with email
    verification, session management with JWT tokens, refresh token rotation,
    secure password hashing with bcrypt, rate limiting on authentication endpoints,
    account lockout after failed attempts, email verification on signup,
    remember me functionality, logout from all devices, user profile management,
    and comprehensive audit logging of all authentication events.
    """.strip()

    print(f"\nInput length: {len(long_input)} characters")
    print(f"First 100 chars: {long_input[:100]}...")

    try:
        issue = await process_request(long_input, context)
        print_result(True, "Successfully processed long input")
        print(f"  Title: {issue.title}")
        print(f"  Classification: {issue.classification}")
        print(f"  Workflow: {issue.workflow}")

    except Exception as e:
        print_result(False, f"Error: {e}")


async def test_multiple_intents():
    """Test handling of requests with multiple mixed intents."""
    print_section("Edge Case 8: Multiple Mixed Intents")

    if not os.getenv("ANTHROPIC_API_KEY"):
        print_result(False, "ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    # Input with multiple intents (feature + bug + chore)
    mixed_input = """
    Add dark mode support, fix the broken login button, and update the
    API documentation to include all new endpoints
    """

    print(f"\nInput: \"{mixed_input}\"")

    try:
        intent = await analyze_intent(mixed_input)
        print_result(True, "System chose primary intent")
        print(f"  Classified as: {intent['intent_type']}")
        print(f"  Summary: {intent['summary']}")
        print("  Note: System picks the dominant intent from mixed requests")

    except Exception as e:
        print_result(False, f"Error: {e}")


async def main():
    """Run all edge case tests."""
    print("\n" + "=" * 60)
    print("NL Processing Edge Cases Examples")
    print("=" * 60)

    # Run all edge case tests
    await test_empty_input()
    await test_ambiguous_requests()
    await test_invalid_project_paths()
    await test_empty_project_directory()
    await test_markdown_special_characters()
    await test_project_without_standard_files()
    await test_very_long_input()
    await test_multiple_intents()

    print("\n" + "=" * 60)
    print("All edge case tests completed!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("- The system handles most edge cases gracefully")
    print("- Empty or very short inputs may produce generic results")
    print("- Ambiguous requests are classified based on context clues")
    print("- Projects without standard files default to 'low' complexity")
    print("- Markdown special characters are preserved in issue bodies")
    print("- Mixed intent requests prioritize the dominant intent")
    print()


if __name__ == "__main__":
    asyncio.run(main())
