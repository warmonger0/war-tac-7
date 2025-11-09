import os
import json
from typing import Tuple, List
from anthropic import Anthropic
from core.data_models import GitHubIssue, ProjectContext


async def analyze_intent(nl_input: str) -> dict:
    """
    Use Claude API to understand what user wants to build.

    Args:
        nl_input: Natural language description of the desired feature/bug/chore

    Returns:
        Dictionary containing:
        - intent_type: "feature", "bug", or "chore"
        - summary: Brief summary of the intent
        - technical_area: Technical area (e.g., "authentication", "UI", "database")
    """
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        prompt = f"""Analyze this natural language request and extract the intent:

Request: "{nl_input}"

Provide your analysis as a JSON object with the following fields:
- intent_type: Must be one of "feature", "bug", or "chore"
- summary: A brief one-sentence summary of what the user wants
- technical_area: The primary technical area (e.g., "UI", "authentication", "database", "API", "testing")

Guidelines:
- "feature": New functionality or enhancement to existing functionality
- "bug": Something that's broken or not working as expected
- "chore": Maintenance tasks, refactoring, documentation, setup

Return ONLY the JSON object, no explanations."""

        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=300,
            temperature=0.1,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result_text = response.content[0].text.strip()

        # Clean up markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())

    except Exception as e:
        raise Exception(f"Error analyzing intent with Anthropic: {str(e)}")


def extract_requirements(nl_input: str, intent: dict) -> List[str]:
    """
    Extract technical requirements from the natural language request.

    Args:
        nl_input: Natural language description
        intent: Intent analysis dictionary from analyze_intent()

    Returns:
        List of technical requirements
    """
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        client = Anthropic(api_key=api_key)

        prompt = f"""Based on this request and its intent analysis, extract specific technical requirements:

Request: "{nl_input}"
Intent: {json.dumps(intent, indent=2)}

Extract a list of specific, actionable technical requirements. Each requirement should be:
- Concrete and testable
- Focused on implementation details
- Written in clear, technical language

Return your answer as a JSON array of strings. Example format:
["Implement user authentication with JWT tokens", "Create login form with email/password fields", "Add password hashing with bcrypt"]

Return ONLY the JSON array, no explanations."""

        response = client.messages.create(
            model="claude-sonnet-4-0",
            max_tokens=500,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result_text = response.content[0].text.strip()

        # Clean up markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]

        return json.loads(result_text.strip())

    except Exception as e:
        raise Exception(f"Error extracting requirements with Anthropic: {str(e)}")


def classify_issue_type(intent: dict) -> str:
    """
    Determine issue classification based on intent analysis.

    Args:
        intent: Intent analysis dictionary

    Returns:
        Issue classification: "feature", "bug", or "chore"
    """
    return intent.get("intent_type", "feature")


def suggest_adw_workflow(issue_type: str, complexity: str) -> Tuple[str, str]:
    """
    Recommend ADW workflow and model set based on issue type and complexity.

    Args:
        issue_type: "feature", "bug", or "chore"
        complexity: "low", "medium", or "high"

    Returns:
        Tuple of (workflow, model_set)
    """
    # Workflow recommendation logic based on complexity and type
    if issue_type == "bug":
        return ("adw_plan_build_test_iso", "base")
    elif issue_type == "chore":
        return ("adw_sdlc_iso", "base")
    else:  # feature
        if complexity == "high":
            return ("adw_plan_build_test_iso", "heavy")
        elif complexity == "medium":
            return ("adw_plan_build_test_iso", "base")
        else:  # low
            return ("adw_sdlc_iso", "base")


async def process_request(nl_input: str, project_context: ProjectContext) -> GitHubIssue:
    """
    Main orchestration function that converts natural language to GitHub issue.

    Args:
        nl_input: Natural language description of the desired feature/bug/chore
        project_context: Project context information

    Returns:
        GitHubIssue object with all fields populated
    """
    try:
        # Step 1: Analyze intent
        intent = await analyze_intent(nl_input)

        # Step 2: Extract requirements
        requirements = extract_requirements(nl_input, intent)

        # Step 3: Classify issue type
        classification = classify_issue_type(intent)

        # Step 4: Suggest workflow based on complexity
        workflow, model_set = suggest_adw_workflow(classification, project_context.complexity)

        # Step 5: Generate title
        title = intent.get("summary", nl_input[:100])

        # Step 6: Generate issue body (will be formatted by issue_formatter)
        # For now, create a basic structure
        body_parts = [
            "## Description",
            f"{intent.get('summary', nl_input)}",
            "",
            "## Requirements",
        ]

        for req in requirements:
            body_parts.append(f"- {req}")

        body_parts.extend([
            "",
            "## Technical Area",
            f"{intent.get('technical_area', 'General')}",
            "",
            "## Workflow",
            f"{workflow} model_set {model_set}"
        ])

        body = "\n".join(body_parts)

        # Step 7: Generate labels
        labels = [classification, intent.get('technical_area', 'general').lower()]
        if project_context.framework:
            labels.append(project_context.framework)

        # Step 8: Create GitHubIssue object
        return GitHubIssue(
            title=title,
            body=body,
            labels=labels,
            classification=classification,
            workflow=workflow,
            model_set=model_set
        )

    except Exception as e:
        raise Exception(f"Error processing NL request: {str(e)}")
