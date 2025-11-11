#!/usr/bin/env python3
"""
Advanced NL Processing Usage Example

This example demonstrates advanced features:
- Error handling and retry logic
- Custom workflow overrides
- Batch processing multiple requests
- Working with different project types
- Detailed logging

Usage:
    export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
    python advanced_usage.py
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Optional, List

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app" / "server"))

from core.nl_processor import process_request, analyze_intent
from core.project_detector import detect_project_context
from core.github_poster import GitHubPoster
from core.data_models import GitHubIssue, ProjectContext


async def process_with_retry(
    nl_input: str,
    context: ProjectContext,
    max_retries: int = 3
) -> Optional[GitHubIssue]:
    """
    Process NL request with exponential backoff retry logic.

    Args:
        nl_input: Natural language input
        context: Project context
        max_retries: Maximum number of retry attempts

    Returns:
        GitHubIssue object or None if all retries failed
    """
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}/{max_retries}...")
            issue = await process_request(nl_input, context)
            print(f"  ✓ Success on attempt {attempt + 1}")
            return issue

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"  ⚠ Attempt {attempt + 1} failed: {e}")
                print(f"  Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"  ❌ All {max_retries} attempts failed")
                print(f"  Last error: {e}")
                return None


async def batch_process_requests(
    requests: List[str],
    context: ProjectContext,
    delay: float = 1.0
) -> List[Optional[GitHubIssue]]:
    """
    Process multiple requests with rate limiting.

    Args:
        requests: List of natural language inputs
        context: Project context
        delay: Delay between requests (seconds)

    Returns:
        List of GitHubIssue objects (or None for failures)
    """
    issues = []

    for i, req in enumerate(requests, 1):
        print(f"\nProcessing request {i}/{len(requests)}: \"{req}\"")
        issue = await process_with_retry(req, context)
        issues.append(issue)

        # Rate limiting delay
        if i < len(requests):
            print(f"  Waiting {delay}s before next request...")
            time.sleep(delay)

    return issues


def override_workflow(issue: GitHubIssue, workflow: str, model_set: str) -> GitHubIssue:
    """
    Override the automatically recommended workflow.

    Args:
        issue: GitHubIssue object
        workflow: Custom workflow name
        model_set: Custom model set

    Returns:
        Modified GitHubIssue object
    """
    print(f"  Original: {issue.workflow} model_set {issue.model_set}")
    issue.workflow = workflow
    issue.model_set = model_set
    print(f"  Override: {issue.workflow} model_set {issue.model_set}")
    return issue


async def demo_error_handling():
    """Demonstrate comprehensive error handling."""
    print("=" * 60)
    print("Demo 1: Error Handling and Retry Logic")
    print("=" * 60)
    print()

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        return

    # Detect context
    project_path = Path(__file__).parent.parent.parent
    try:
        context = detect_project_context(str(project_path))
        print(f"✓ Project context detected (complexity: {context.complexity})")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return

    # Process with retry
    print("\nProcessing request with retry logic...")
    issue = await process_with_retry(
        "Add comprehensive error handling to the API endpoints",
        context,
        max_retries=3
    )

    if issue:
        print(f"\n✓ Generated issue: {issue.title}")
    else:
        print("\n❌ Failed to generate issue after retries")


async def demo_custom_workflow():
    """Demonstrate custom workflow overrides."""
    print("\n")
    print("=" * 60)
    print("Demo 2: Custom Workflow Override")
    print("=" * 60)
    print()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    print("Processing request with automatic workflow...")
    issue = await process_request(
        "Add new API endpoint for user preferences",
        context
    )

    print(f"\nGenerated issue: {issue.title}")
    print("\nOverriding workflow recommendation...")
    issue = override_workflow(issue, "adw_sdlc_zte_iso", "heavy")
    print("✓ Workflow overridden")


async def demo_batch_processing():
    """Demonstrate batch processing multiple requests."""
    print("\n")
    print("=" * 60)
    print("Demo 3: Batch Processing Multiple Requests")
    print("=" * 60)
    print()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        return

    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))

    requests = [
        "Add input validation to all form fields",
        "Implement rate limiting for API endpoints",
        "Add comprehensive logging throughout the application"
    ]

    print(f"Processing {len(requests)} requests with rate limiting...")
    issues = await batch_process_requests(requests, context, delay=1.0)

    # Summary
    print("\n")
    print("=" * 60)
    print("Batch Processing Summary:")
    print("-" * 60)
    successful = sum(1 for issue in issues if issue is not None)
    print(f"Total requests: {len(requests)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(requests) - successful}")
    print()

    for i, (req, issue) in enumerate(zip(requests, issues), 1):
        status = "✓" if issue else "❌"
        title = issue.title if issue else "Failed"
        print(f"{status} Request {i}: {title}")


async def demo_different_project_types():
    """Demonstrate handling different project types."""
    print("\n")
    print("=" * 60)
    print("Demo 4: Different Project Types")
    print("=" * 60)
    print()

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not set")
        return

    # Example 1: Python backend project
    print("Example 1: Python Backend (FastAPI)")
    print("-" * 60)
    project_path = Path(__file__).parent.parent.parent
    context = detect_project_context(str(project_path))
    print(f"Framework: {context.framework or 'None'}")
    print(f"Backend: {context.backend or 'None'}")
    print(f"Complexity: {context.complexity}")

    issue = await process_request(
        "Add authentication middleware with JWT validation",
        context
    )
    print(f"Generated: {issue.title}")
    print(f"Workflow: {issue.workflow} model_set {issue.model_set}")

    # Note: For other project types, you would use different project paths
    # This is just demonstrating how the system adapts to different contexts


async def main():
    """Run all advanced usage demonstrations."""
    print()
    print("=" * 60)
    print("NL Processing Advanced Usage Examples")
    print("=" * 60)
    print()

    # Demo 1: Error handling and retry
    await demo_error_handling()

    # Demo 2: Custom workflow override
    await demo_custom_workflow()

    # Demo 3: Batch processing
    await demo_batch_processing()

    # Demo 4: Different project types
    await demo_different_project_types()

    print("\n")
    print("=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    asyncio.run(main())
