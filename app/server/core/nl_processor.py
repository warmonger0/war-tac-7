"""Natural Language Processor for converting user requests to GitHub issues."""

import os
import json
import time
from typing import Dict, List, Optional, Any
from anthropic import Anthropic
from core.webbuilder_models import (
    GitHubIssue,
    ProjectContext,
    IntentAnalysis,
    NLProcessingRequest,
    NLProcessingResponse,
    WorkflowSuggestion
)


class NLProcessor:
    """Handles natural language processing for issue generation."""

    def __init__(self):
        """Initialize the NL processor with Anthropic client."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic(api_key=api_key)

    async def process_request(
        self,
        nl_input: str,
        project_context: Optional[ProjectContext] = None
    ) -> GitHubIssue:
        """
        Main processing function to convert NL input to GitHub issue.

        Args:
            nl_input: Natural language input from user
            project_context: Optional project context for better analysis

        Returns:
            GitHubIssue object ready for formatting and posting
        """
        # Analyze user intent
        intent = await self.analyze_intent(nl_input)

        # Extract technical requirements
        requirements = self.extract_requirements(nl_input, intent)

        # Determine issue type
        issue_type = self.determine_issue_type(intent)

        # Suggest workflow based on complexity
        workflow_suggestion = self.suggest_workflow(
            intent,
            project_context,
            requirements
        )

        # Generate issue title and description
        title = self.generate_title(nl_input, intent)
        description = self.generate_description(
            nl_input,
            intent,
            requirements,
            project_context
        )

        # Create technical approach section
        technical_approach = self.create_technical_approach(
            intent,
            requirements,
            project_context
        )

        # Build the complete issue body
        body = self.build_issue_body(
            description,
            requirements,
            technical_approach,
            workflow_suggestion,
            issue_type
        )

        # Determine labels
        labels = self.determine_labels(intent, issue_type, project_context)

        return GitHubIssue(
            title=title,
            body=body,
            labels=labels,
            classification=issue_type,
            workflow=workflow_suggestion.workflow_name,
            model_set=workflow_suggestion.model_set
        )

    async def analyze_intent(self, nl_input: str) -> Dict[str, Any]:
        """
        Use Claude to understand what the user wants to build.

        Args:
            nl_input: Natural language input from user

        Returns:
            Dictionary containing intent analysis
        """
        prompt = f"""Analyze the following user request for software development and extract their intent:

User Request: "{nl_input}"

Provide a JSON response with the following structure:
{{
    "primary_intent": "Brief description of what user wants to achieve",
    "action_type": "create|modify|fix|analyze|unknown",
    "target_components": ["list", "of", "components", "mentioned"],
    "technical_keywords": ["technical", "terms", "found"],
    "suggested_issue_type": "feature|bug|chore",
    "ambiguity_level": "low|medium|high",
    "needs_clarification": ["list of unclear points if any"]
}}

Focus on understanding:
1. What is the user trying to build or fix?
2. What components or features are involved?
3. Is this a new feature, bug fix, or maintenance task?
4. Are there any technical requirements mentioned?

Response (JSON only):"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-0",
                max_tokens=500,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON response
            json_str = response.content[0].text.strip()
            # Clean up if wrapped in markdown
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]

            return json.loads(json_str.strip())

        except json.JSONDecodeError:
            # Fallback to basic analysis
            return {
                "primary_intent": nl_input[:100],
                "action_type": "create",
                "target_components": [],
                "technical_keywords": [],
                "suggested_issue_type": "feature",
                "ambiguity_level": "high",
                "needs_clarification": ["Could not parse user intent clearly"]
            }
        except Exception as e:
            raise Exception(f"Error analyzing intent with Anthropic: {str(e)}")

    def extract_requirements(self, nl_input: str, intent: Dict[str, Any]) -> List[str]:
        """
        Extract technical requirements from the request.

        Args:
            nl_input: Natural language input from user
            intent: Analyzed intent dictionary

        Returns:
            List of technical requirements
        """
        prompt = f"""Extract technical requirements from this user request:

User Request: "{nl_input}"

Intent Analysis: {json.dumps(intent, indent=2)}

List the specific technical requirements as bullet points. Focus on:
- Functional requirements (what the feature should do)
- Technical specifications mentioned
- Performance requirements
- UI/UX requirements
- Integration requirements

Requirements (one per line, start each with "-"):"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-0",
                max_tokens=300,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )

            requirements_text = response.content[0].text.strip()
            # Parse requirements into list
            requirements = []
            for line in requirements_text.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    requirements.append(line[1:].strip())
                elif line:  # Non-empty line without dash
                    requirements.append(line)

            return requirements if requirements else ["No specific requirements identified"]

        except Exception as e:
            # Fallback to basic extraction
            return [
                f"Implement {intent.get('primary_intent', 'requested functionality')}",
                "Ensure code quality and proper testing"
            ]

    def determine_issue_type(self, intent: Dict[str, Any]) -> str:
        """
        Determine the issue classification based on intent.

        Args:
            intent: Analyzed intent dictionary

        Returns:
            Issue type: "feature", "bug", or "chore"
        """
        action_type = intent.get("action_type", "unknown")
        suggested_type = intent.get("suggested_issue_type", "feature")

        # Map action types to issue types
        if action_type == "fix":
            return "bug"
        elif action_type in ["create", "modify"]:
            return "feature"
        elif action_type == "analyze":
            return "chore"
        else:
            return suggested_type

    def suggest_workflow(
        self,
        intent: Dict[str, Any],
        project_context: Optional[ProjectContext],
        requirements: List[str]
    ) -> WorkflowSuggestion:
        """
        Suggest ADW workflow based on complexity and requirements.

        Args:
            intent: Analyzed intent dictionary
            project_context: Optional project context
            requirements: List of requirements

        Returns:
            WorkflowSuggestion object
        """
        # Determine complexity
        complexity_factors = {
            "high": 0,
            "medium": 0,
            "low": 0
        }

        # Check intent complexity
        if intent.get("ambiguity_level") == "high":
            complexity_factors["high"] += 1
        elif intent.get("ambiguity_level") == "medium":
            complexity_factors["medium"] += 1
        else:
            complexity_factors["low"] += 1

        # Check requirements count
        if len(requirements) > 10:
            complexity_factors["high"] += 2
        elif len(requirements) > 5:
            complexity_factors["medium"] += 2
        else:
            complexity_factors["low"] += 2

        # Check project context complexity
        if project_context:
            if project_context.complexity == "high":
                complexity_factors["high"] += 1
            elif project_context.complexity == "medium":
                complexity_factors["medium"] += 1
            else:
                complexity_factors["low"] += 1

        # Check for multiple components
        components = intent.get("target_components", [])
        if len(components) > 3:
            complexity_factors["high"] += 1
        elif len(components) > 1:
            complexity_factors["medium"] += 1
        else:
            complexity_factors["low"] += 1

        # Determine overall complexity
        if complexity_factors["high"] >= complexity_factors["medium"] and complexity_factors["high"] >= complexity_factors["low"]:
            workflow = "adw_sdlc_iso"
            model_set = "heavy"
            reasoning = "Complex task requiring comprehensive SDLC workflow with heavy models"
        elif complexity_factors["medium"] >= complexity_factors["low"]:
            workflow = "adw_plan_build_test_iso"
            model_set = "base"
            reasoning = "Medium complexity task suitable for plan-build-test workflow"
        else:
            workflow = "adw_simple_iso"
            model_set = "base"
            reasoning = "Simple task that can be handled with basic workflow"

        # Adjust for bug fixes
        issue_type = self.determine_issue_type(intent)
        if issue_type == "bug":
            workflow = "adw_plan_build_test_iso"
            model_set = "base"
            reasoning = "Bug fix requiring testing and validation"

        return WorkflowSuggestion(
            workflow_name=workflow,
            model_set=model_set,
            reasoning=reasoning,
            alternative_workflows=[
                "adw_sdlc_iso",
                "adw_plan_build_test_iso",
                "adw_simple_iso"
            ]
        )

    def generate_title(self, nl_input: str, intent: Dict[str, Any]) -> str:
        """
        Generate a concise issue title.

        Args:
            nl_input: Natural language input
            intent: Analyzed intent

        Returns:
            Issue title string
        """
        primary_intent = intent.get("primary_intent", "")

        if primary_intent:
            # Clean up and shorten the primary intent for title
            title = primary_intent[:80]  # Limit length
            if not title[0].isupper():
                title = title[0].upper() + title[1:]
            return title
        else:
            # Fallback: use first sentence or phrase from input
            title = nl_input.split('.')[0][:80]
            if not title[0].isupper():
                title = title[0].upper() + title[1:]
            return title

    def generate_description(
        self,
        nl_input: str,
        intent: Dict[str, Any],
        requirements: List[str],
        project_context: Optional[ProjectContext]
    ) -> str:
        """
        Generate detailed issue description.

        Args:
            nl_input: Natural language input
            intent: Analyzed intent
            requirements: List of requirements
            project_context: Optional project context

        Returns:
            Description string
        """
        description_parts = []

        # Add user's original request
        description_parts.append(f"## User Request\n{nl_input}")

        # Add intent summary
        description_parts.append(f"\n## Intent\n{intent.get('primary_intent', 'No clear intent identified')}")

        # Add context if available
        if project_context:
            context_info = []
            if project_context.framework:
                context_info.append(f"- Framework: {project_context.framework}")
            if project_context.backend:
                context_info.append(f"- Backend: {project_context.backend}")
            if context_info:
                description_parts.append(f"\n## Project Context\n" + "\n".join(context_info))

        # Note any ambiguities
        if intent.get("needs_clarification"):
            clarifications = intent.get("needs_clarification", [])
            if clarifications:
                description_parts.append(f"\n## Points Requiring Clarification\n" +
                                       "\n".join(f"- {c}" for c in clarifications))

        return "\n".join(description_parts)

    def create_technical_approach(
        self,
        intent: Dict[str, Any],
        requirements: List[str],
        project_context: Optional[ProjectContext]
    ) -> str:
        """
        Create technical approach section based on analysis.

        Args:
            intent: Analyzed intent
            requirements: List of requirements
            project_context: Optional project context

        Returns:
            Technical approach string
        """
        approach_parts = []

        # Add components to implement
        components = intent.get("target_components", [])
        if components:
            approach_parts.append("### Components to Implement")
            for component in components:
                approach_parts.append(f"- {component}")

        # Add technical considerations
        keywords = intent.get("technical_keywords", [])
        if keywords:
            approach_parts.append("\n### Technical Considerations")
            for keyword in keywords:
                approach_parts.append(f"- {keyword}")

        # Add framework-specific notes if context available
        if project_context and project_context.framework:
            approach_parts.append(f"\n### Framework Notes")
            approach_parts.append(f"- Using {project_context.framework} patterns and conventions")

        return "\n".join(approach_parts) if approach_parts else "To be determined during implementation"

    def build_issue_body(
        self,
        description: str,
        requirements: List[str],
        technical_approach: str,
        workflow_suggestion: WorkflowSuggestion,
        issue_type: str
    ) -> str:
        """
        Build the complete issue body with all sections.

        Args:
            description: Issue description
            requirements: List of requirements
            technical_approach: Technical approach section
            workflow_suggestion: Workflow suggestion
            issue_type: Issue type (feature/bug/chore)

        Returns:
            Complete issue body in markdown
        """
        body_parts = [description]

        # Add requirements section
        if requirements:
            body_parts.append("\n## Requirements")
            for req in requirements:
                body_parts.append(f"- {req}")

        # Add technical approach
        body_parts.append(f"\n## Technical Approach\n{technical_approach}")

        # Add workflow section
        body_parts.append(f"\n## Workflow")
        body_parts.append(f"{workflow_suggestion.workflow_name} model_set {workflow_suggestion.model_set}")
        body_parts.append(f"*Reasoning: {workflow_suggestion.reasoning}*")

        # Add issue type marker
        body_parts.append(f"\n## Type\n/{issue_type}")

        return "\n".join(body_parts)

    def determine_labels(
        self,
        intent: Dict[str, Any],
        issue_type: str,
        project_context: Optional[ProjectContext]
    ) -> List[str]:
        """
        Determine appropriate labels for the issue.

        Args:
            intent: Analyzed intent
            issue_type: Issue type
            project_context: Optional project context

        Returns:
            List of label strings
        """
        labels = []

        # Add issue type label
        labels.append(issue_type)

        # Add webbuilder label
        labels.append("webbuilder")

        # Add framework labels if known
        if project_context:
            if project_context.framework:
                labels.append(project_context.framework)
            if project_context.backend:
                labels.append(project_context.backend)

        # Add component labels
        components = intent.get("target_components", [])
        for component in components[:3]:  # Limit to 3 component labels
            if component and len(component) < 20:  # Reasonable label length
                labels.append(component.lower().replace(" ", "-"))

        # Add complexity label
        ambiguity = intent.get("ambiguity_level", "medium")
        if ambiguity == "high":
            labels.append("needs-clarification")

        return labels


async def process_nl_request(request: NLProcessingRequest) -> NLProcessingResponse:
    """
    Main entry point for processing NL requests.

    Args:
        request: NLProcessingRequest object

    Returns:
        NLProcessingResponse with generated issue and metadata
    """
    start_time = time.time()

    try:
        # Initialize processor
        processor = NLProcessor()

        # Detect project context if requested
        project_context = None
        if request.auto_detect_context and request.project_path:
            from core.project_detector import detect_project_context
            project_context = detect_project_context(request.project_path)

        # Process the request
        issue = await processor.process_request(
            request.nl_input,
            project_context
        )

        # Get intent analysis for response
        intent = await processor.analyze_intent(request.nl_input)
        requirements = processor.extract_requirements(request.nl_input, intent)

        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000

        # Calculate confidence score based on ambiguity
        ambiguity_level = intent.get("ambiguity_level", "medium")
        confidence_map = {"low": 0.9, "medium": 0.7, "high": 0.4}
        confidence_score = confidence_map.get(ambiguity_level, 0.5)

        return NLProcessingResponse(
            issue=issue,
            project_context=project_context,
            confidence_score=confidence_score,
            intent_analysis=intent,
            requirements=requirements,
            processing_time_ms=processing_time_ms
        )

    except Exception as e:
        processing_time_ms = (time.time() - start_time) * 1000
        return NLProcessingResponse(
            issue=GitHubIssue(
                title="Error processing request",
                body="Failed to process natural language request",
                labels=["error"],
                classification="chore",
                workflow="adw_simple_iso",
                model_set="base"
            ),
            project_context=None,
            confidence_score=0.0,
            intent_analysis={},
            requirements=[],
            processing_time_ms=processing_time_ms,
            error=str(e)
        )