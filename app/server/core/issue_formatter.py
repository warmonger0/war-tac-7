"""Issue Formatter module for creating well-formatted GitHub issues."""

from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from core.webbuilder_models import (
    GitHubIssue,
    ProjectContext,
    WorkflowSuggestion,
    IssuePreviewRequest,
    IssuePreviewResponse
)


# Issue templates for different types
ISSUE_TEMPLATES = {
    "feature": """# {title}

## Description
{description}

## Requirements
{requirements}

## Technical Approach
{technical_approach}

## Acceptance Criteria
{acceptance_criteria}

## Workflow
{adw_workflow} model_set {model_set}

## Labels
{labels}
""",

    "bug": """# {title}

## Issue Description
{description}

## Steps to Reproduce
{steps_to_reproduce}

## Expected vs Actual Behavior
### Expected
{expected_behavior}

### Actual
{actual_behavior}

## Technical Details
{technical_details}

## Workflow
adw_plan_build_test_iso model_set base

## Labels
{labels}
""",

    "chore": """# {title}

## Description
{description}

## Tasks
{tasks}

## Technical Approach
{technical_approach}

## Workflow
{adw_workflow} model_set {model_set}

## Labels
{labels}
"""
}


class IssueFormatter:
    """Formats GitHub issues with proper structure and styling."""

    def __init__(self):
        """Initialize the formatter with Rich console for terminal output."""
        self.console = Console()

    def format_issue(
        self,
        issue: GitHubIssue,
        template_override: Optional[str] = None
    ) -> str:
        """
        Format a GitHub issue using appropriate template.

        Args:
            issue: GitHubIssue object to format
            template_override: Optional custom template to use

        Returns:
            Formatted issue body as markdown string
        """
        # Select template based on issue classification
        if template_override:
            template = template_override
        else:
            template = ISSUE_TEMPLATES.get(
                issue.classification,
                ISSUE_TEMPLATES["feature"]  # Default to feature template
            )

        # Parse the issue body to extract sections
        sections = self._parse_issue_body(issue.body)

        # Build template variables
        template_vars = {
            "title": issue.title,
            "description": sections.get("description", ""),
            "requirements": self._format_requirements(sections.get("requirements", [])),
            "technical_approach": sections.get("technical_approach", ""),
            "adw_workflow": issue.workflow,
            "model_set": issue.model_set,
            "labels": ", ".join(issue.labels),
            "acceptance_criteria": sections.get("acceptance_criteria", ""),
            "tasks": sections.get("tasks", ""),
            "steps_to_reproduce": sections.get("steps_to_reproduce", "1. [Steps to be filled]"),
            "expected_behavior": sections.get("expected_behavior", "[To be filled]"),
            "actual_behavior": sections.get("actual_behavior", "[To be filled]"),
            "technical_details": sections.get("technical_details", "")
        }

        # Format the template
        formatted = template.format(**template_vars)

        # Add footer with generation info
        formatted += self._generate_footer()

        return formatted

    def _parse_issue_body(self, body: str) -> Dict[str, any]:
        """
        Parse issue body to extract different sections.

        Args:
            body: Raw issue body text

        Returns:
            Dictionary of parsed sections
        """
        sections = {}
        current_section = None
        current_content = []

        lines = body.split('\n')

        for line in lines:
            # Check if this is a section header
            if line.startswith('## '):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                    current_content = []

                # Start new section
                current_section = line[3:].strip().lower().replace(' ', '_')
            elif current_section:
                current_content.append(line)
            elif not sections.get('description'):
                # First content before any section is description
                if 'description' not in sections:
                    sections['description'] = ''
                sections['description'] += line + '\n'

        # Save last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        # Parse requirements if present as list
        if 'requirements' in sections:
            req_text = sections['requirements']
            requirements = []
            for line in req_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    requirements.append(line[2:])
                elif line:
                    requirements.append(line)
            sections['requirements'] = requirements

        return sections

    def _format_requirements(self, requirements: List[str]) -> str:
        """
        Format requirements list as markdown.

        Args:
            requirements: List of requirement strings

        Returns:
            Formatted requirements as markdown list
        """
        if not requirements:
            return "- No specific requirements identified"

        formatted = []
        for req in requirements:
            if not req.startswith('- '):
                req = f"- {req}"
            formatted.append(req)

        return '\n'.join(formatted)

    def _generate_footer(self) -> str:
        """
        Generate footer with metadata about issue generation.

        Returns:
            Footer string
        """
        return "\n\n---\n*Generated by TAC WebBuilder NL Processing System*"

    def suggest_adw_workflow(
        self,
        complexity: str,
        issue_type: str,
        component_count: int
    ) -> WorkflowSuggestion:
        """
        Suggest appropriate ADW workflow based on complexity factors.

        Args:
            complexity: Project complexity (low/medium/high)
            issue_type: Issue classification (feature/bug/chore)
            component_count: Number of components involved

        Returns:
            WorkflowSuggestion object
        """
        # Decision matrix for workflow selection
        if issue_type == "bug":
            # Bugs always use plan-build-test for validation
            return WorkflowSuggestion(
                workflow_name="adw_plan_build_test_iso",
                model_set="base",
                reasoning="Bug fixes require thorough testing and validation",
                alternative_workflows=["adw_sdlc_iso"]
            )

        if complexity == "high" or component_count > 5:
            # High complexity needs full SDLC
            return WorkflowSuggestion(
                workflow_name="adw_sdlc_iso",
                model_set="heavy",
                reasoning="Complex implementation requiring full SDLC workflow with heavy models",
                alternative_workflows=["adw_plan_build_test_iso"]
            )

        if complexity == "medium" or component_count > 2:
            # Medium complexity uses plan-build-test
            return WorkflowSuggestion(
                workflow_name="adw_plan_build_test_iso",
                model_set="base",
                reasoning="Moderate complexity suitable for structured plan-build-test workflow",
                alternative_workflows=["adw_sdlc_iso", "adw_simple_iso"]
            )

        # Low complexity uses simple workflow
        return WorkflowSuggestion(
            workflow_name="adw_simple_iso",
            model_set="base",
            reasoning="Simple task that can be handled with basic workflow",
            alternative_workflows=["adw_plan_build_test_iso"]
        )

    def format_preview(
        self,
        issue: GitHubIssue,
        format_type: str = "terminal"
    ) -> str:
        """
        Format issue for preview display.

        Args:
            issue: GitHubIssue to preview
            format_type: Format type (terminal/markdown/html)

        Returns:
            Formatted preview string
        """
        if format_type == "terminal":
            return self._format_terminal_preview(issue)
        elif format_type == "markdown":
            return self.format_issue(issue)
        elif format_type == "html":
            return self._format_html_preview(issue)
        else:
            return self.format_issue(issue)

    def _format_terminal_preview(self, issue: GitHubIssue) -> str:
        """
        Format issue for terminal display using Rich.

        Args:
            issue: GitHubIssue to display

        Returns:
            Terminal-formatted string
        """
        # Create a table for issue metadata
        table = Table(title="GitHub Issue Preview", show_header=True)
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        table.add_row("Title", issue.title)
        table.add_row("Type", issue.classification)
        table.add_row("Workflow", f"{issue.workflow} ({issue.model_set})")
        table.add_row("Labels", ", ".join(issue.labels))

        # Format the table
        from io import StringIO
        string_buffer = StringIO()
        console = Console(file=string_buffer)
        console.print(table)

        # Add body preview
        console.print("\n[bold cyan]Issue Body:[/bold cyan]")
        console.print(Panel(Markdown(issue.body[:500] + "..." if len(issue.body) > 500 else issue.body)))

        return string_buffer.getvalue()

    def _format_html_preview(self, issue: GitHubIssue) -> str:
        """
        Format issue for HTML display.

        Args:
            issue: GitHubIssue to display

        Returns:
            HTML-formatted string
        """
        import markdown

        html_template = """
        <div class="issue-preview">
            <h2>{title}</h2>
            <div class="metadata">
                <span class="issue-type">{classification}</span>
                <span class="workflow">{workflow} ({model_set})</span>
            </div>
            <div class="labels">
                {labels_html}
            </div>
            <div class="body">
                {body_html}
            </div>
        </div>
        """

        labels_html = "".join(
            f'<span class="label">{label}</span>' for label in issue.labels
        )

        body_html = markdown.markdown(issue.body)

        return html_template.format(
            title=issue.title,
            classification=issue.classification,
            workflow=issue.workflow,
            model_set=issue.model_set,
            labels_html=labels_html,
            body_html=body_html
        )

    def create_steps_to_reproduce(self, description: str) -> str:
        """
        Generate steps to reproduce for bug reports.

        Args:
            description: Bug description

        Returns:
            Formatted steps to reproduce
        """
        return """1. [Describe the initial state/setup]
2. [Describe the action taken]
3. [Describe what happened]
4. [Describe any error messages or unexpected behavior]"""

    def create_acceptance_criteria(self, requirements: List[str]) -> str:
        """
        Generate acceptance criteria from requirements.

        Args:
            requirements: List of requirements

        Returns:
            Formatted acceptance criteria
        """
        if not requirements:
            return "- [ ] Implementation complete\n- [ ] Tests pass\n- [ ] Documentation updated"

        criteria = []
        for req in requirements[:5]:  # Limit to 5 main criteria
            criteria.append(f"- [ ] {req}")

        # Add standard criteria
        criteria.extend([
            "- [ ] Unit tests written and passing",
            "- [ ] Integration tests passing",
            "- [ ] Documentation updated"
        ])

        return '\n'.join(criteria)


def preview_issue(request: IssuePreviewRequest) -> IssuePreviewResponse:
    """
    Preview an issue before posting.

    Args:
        request: IssuePreviewRequest with issue and format

    Returns:
        IssuePreviewResponse with formatted preview
    """
    formatter = IssueFormatter()

    # Format the preview
    formatted_preview = formatter.format_preview(
        request.issue,
        request.format
    )

    # Estimate complexity based on issue details
    component_count = len(request.issue.labels)
    if request.issue.workflow == "adw_sdlc_iso":
        estimated_complexity = "High - Full SDLC required"
        suggested_timeline = "3-5 days"
    elif request.issue.workflow == "adw_plan_build_test_iso":
        estimated_complexity = "Medium - Structured implementation"
        suggested_timeline = "1-3 days"
    else:
        estimated_complexity = "Low - Simple implementation"
        suggested_timeline = "< 1 day"

    return IssuePreviewResponse(
        formatted_preview=formatted_preview,
        estimated_complexity=estimated_complexity,
        suggested_timeline=suggested_timeline
    )