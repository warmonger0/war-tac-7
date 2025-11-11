#!/usr/bin/env python3
"""
Basic NL Processing Usage Example

This example demonstrates the simplest way to use the NL processing system:
1. Detect project context
2. Process a natural language request
3. Generate and preview a GitHub issue
4. (Optionally) post to GitHub

Usage:
    export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
    python basic_usage.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app" / "server"))

from core.nl_processor import process_request
from core.project_detector import detect_project_context
from core.github_poster import GitHubPoster


async def main():
    """Main function demonstrating basic NL processing workflow."""

    print("=" * 60)
    print("NL Processing Basic Usage Example")
    print("=" * 60)
    print()

    # Step 1: Verify environment variables
    print("Step 1: Checking environment variables...")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("💡 Set it with: export ANTHROPIC_API_KEY='sk-ant-api03-xxxxx'")
        return
    print("✓ ANTHROPIC_API_KEY is set")
    print()

    # Step 2: Detect project context
    print("Step 2: Detecting project context...")
    # Use the tac-webbuilder project itself as an example
    project_path = Path(__file__).parent.parent.parent
    print(f"Analyzing project at: {project_path}")

    try:
        context = detect_project_context(str(project_path))
        print("✓ Project context detected:")
        print(f"  - Framework: {context.framework or 'None'}")
        print(f"  - Backend: {context.backend or 'None'}")
        print(f"  - Complexity: {context.complexity}")
        print(f"  - Build Tools: {', '.join(context.build_tools) or 'None'}")
        print(f"  - Package Manager: {context.package_manager or 'None'}")
        print(f"  - Has Git: {context.has_git}")
    except Exception as e:
        print(f"❌ ERROR: Failed to detect project context: {e}")
        return
    print()

    # Step 3: Process natural language request
    print("Step 3: Processing natural language request...")
    nl_input = "Add a dark mode toggle to the settings page with localStorage persistence"
    print(f"Input: \"{nl_input}\"")
    print()

    try:
        print("Analyzing intent and extracting requirements...")
        issue = await process_request(nl_input, context)
        print("✓ GitHub issue generated successfully!")
    except Exception as e:
        print(f"❌ ERROR: Failed to process request: {e}")
        return
    print()

    # Step 4: Display the generated issue
    print("Step 4: Generated GitHub Issue:")
    print("-" * 60)
    print(f"Title: {issue.title}")
    print(f"Classification: {issue.classification}")
    print(f"Workflow: {issue.workflow} model_set {issue.model_set}")
    print(f"Labels: {', '.join(issue.labels)}")
    print()
    print("Body:")
    print(issue.body)
    print("-" * 60)
    print()

    # Step 5: Preview and optionally post to GitHub
    print("Step 5: Post to GitHub (optional)")
    print()

    # Ask user if they want to post
    response = input("Would you like to post this issue to GitHub? (y/N): ").strip().lower()

    if response in ['y', 'yes']:
        try:
            poster = GitHubPoster()
            print("\nPosting issue to GitHub...")
            issue_number = poster.post_issue(issue, confirm=False)
            print(f"✓ Issue #{issue_number} created successfully!")
        except RuntimeError as e:
            print(f"❌ ERROR: Failed to post issue: {e}")
            print("💡 Make sure gh CLI is installed and authenticated:")
            print("   brew install gh")
            print("   gh auth login")
    else:
        print("Skipping GitHub post.")

    print()
    print("=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
