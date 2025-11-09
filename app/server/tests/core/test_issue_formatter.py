import pytest
from core.issue_formatter import (
    format_issue,
    validate_issue_body,
    format_requirements_list,
    format_technical_approach,
    format_workflow_section,
    create_feature_issue_body,
    create_bug_issue_body,
    create_chore_issue_body,
    ISSUE_TEMPLATES
)
from core.data_models import GitHubIssue


class TestIssueFormatter:

    def test_format_requirements_list_with_items(self):
        """Test formatting a list of requirements."""
        requirements = ["Requirement 1", "Requirement 2", "Requirement 3"]
        result = format_requirements_list(requirements)

        assert "- Requirement 1" in result
        assert "- Requirement 2" in result
        assert "- Requirement 3" in result

    def test_format_requirements_list_empty(self):
        """Test formatting an empty requirements list."""
        requirements = []
        result = format_requirements_list(requirements)

        assert result == "- To be determined"

    def test_format_technical_approach_with_content(self):
        """Test formatting technical approach with content."""
        approach = "Use React hooks for state management"
        result = format_technical_approach(approach)

        assert result == "Use React hooks for state management"

    def test_format_technical_approach_empty(self):
        """Test formatting empty technical approach."""
        result = format_technical_approach("")

        assert result == "To be determined during implementation planning."

    def test_format_technical_approach_none(self):
        """Test formatting None technical approach."""
        result = format_technical_approach(None)

        assert result == "To be determined during implementation planning."

    def test_format_workflow_section(self):
        """Test formatting workflow section."""
        result = format_workflow_section("adw_sdlc_iso", "base")

        assert result == "adw_sdlc_iso model_set base"

    def test_format_workflow_section_heavy(self):
        """Test formatting workflow with heavy model set."""
        result = format_workflow_section("adw_plan_build_test_iso", "heavy")

        assert result == "adw_plan_build_test_iso model_set heavy"

    def test_create_feature_issue_body(self):
        """Test creating a feature issue body."""
        result = create_feature_issue_body(
            description="Add dark mode to the application",
            requirements=["Create theme toggle", "Add CSS variables", "Persist preference"],
            technical_approach="Use React Context for theme state",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        assert "# Feature Request" in result
        assert "Add dark mode to the application" in result
        assert "- Create theme toggle" in result
        assert "Use React Context for theme state" in result
        assert "adw_sdlc_iso model_set base" in result

    def test_create_feature_issue_body_no_technical_approach(self):
        """Test creating feature issue without technical approach."""
        result = create_feature_issue_body(
            description="Add search functionality",
            requirements=["Add search bar", "Implement search algorithm"],
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        assert "To be determined during implementation planning" in result

    def test_create_bug_issue_body(self):
        """Test creating a bug issue body."""
        result = create_bug_issue_body(
            description="Login button is not responding",
            steps="1. Navigate to login page\n2. Click login button",
            expected="Button should trigger login flow",
            actual="Nothing happens",
            workflow="adw_plan_build_test_iso",
            model_set="base"
        )

        assert "# Bug Report" in result
        assert "Login button is not responding" in result
        assert "1. Navigate to login page" in result
        assert "Button should trigger login flow" in result
        assert "Nothing happens" in result
        assert "adw_plan_build_test_iso model_set base" in result

    def test_create_bug_issue_body_minimal(self):
        """Test creating bug issue with minimal information."""
        result = create_bug_issue_body(
            description="Error when saving data",
            workflow="adw_plan_build_test_iso",
            model_set="base"
        )

        assert "Error when saving data" in result
        assert "To be documented" in result

    def test_create_chore_issue_body(self):
        """Test creating a chore issue body."""
        result = create_chore_issue_body(
            description="Update project dependencies",
            tasks=["Update npm packages", "Update Python packages", "Test all functionality"],
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        assert "# Chore" in result
        assert "Update project dependencies" in result
        assert "- Update npm packages" in result
        assert "- Update Python packages" in result
        assert "adw_sdlc_iso model_set base" in result

    def test_format_issue_feature(self):
        """Test formatting a feature issue."""
        issue = GitHubIssue(
            title="Add Dark Mode",
            body="",  # Will be overridden by template
            labels=["feature", "UI"],
            classification="feature",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        template_data = {
            "title": "Add Dark Mode",
            "description": "Add dark mode support to the application",
            "requirements": "- Create theme toggle\n- Add CSS variables",
            "technical_approach": "Use React Context"
        }

        result = format_issue(issue, template_data)

        assert "# Add Dark Mode" in result
        assert "Add dark mode support" in result
        assert "Create theme toggle" in result
        assert "adw_sdlc_iso model_set base" in result

    def test_format_issue_bug(self):
        """Test formatting a bug issue."""
        issue = GitHubIssue(
            title="Login Button Broken",
            body="",
            labels=["bug"],
            classification="bug",
            workflow="adw_plan_build_test_iso",
            model_set="base"
        )

        template_data = {
            "title": "Login Button Broken",
            "description": "Login button not responding to clicks",
            "steps": "1. Click login button",
            "expected": "Should trigger login",
            "actual": "Nothing happens"
        }

        result = format_issue(issue, template_data)

        assert "# Login Button Broken" in result
        assert "Login button not responding" in result
        assert "1. Click login button" in result
        assert "adw_plan_build_test_iso model_set base" in result

    def test_format_issue_chore(self):
        """Test formatting a chore issue."""
        issue = GitHubIssue(
            title="Update Dependencies",
            body="",
            labels=["chore"],
            classification="chore",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        template_data = {
            "title": "Update Dependencies",
            "description": "Update all project dependencies",
            "tasks": "- Update npm packages\n- Update pip packages"
        }

        result = format_issue(issue, template_data)

        assert "# Update Dependencies" in result
        assert "Update all project dependencies" in result
        assert "Update npm packages" in result
        assert "adw_sdlc_iso model_set base" in result

    def test_format_issue_missing_field(self):
        """Test that missing template fields raise an error."""
        issue = GitHubIssue(
            title="Test",
            body="",
            labels=[],
            classification="feature",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        template_data = {
            "title": "Test"
            # Missing required fields
        }

        with pytest.raises(ValueError) as exc_info:
            format_issue(issue, template_data)

        assert "Missing required template field" in str(exc_info.value)

    def test_validate_issue_body_valid(self):
        """Test validating a valid issue body."""
        body = """## Description
This is a test issue.

## Workflow
adw_sdlc_iso model_set base
"""
        result = validate_issue_body(body)
        assert result is True

    def test_validate_issue_body_missing_sections(self):
        """Test validating issue body with missing sections."""
        body = "This is just plain text without any sections."
        result = validate_issue_body(body)
        assert result is False

    def test_validate_issue_body_missing_workflow(self):
        """Test validating issue body without workflow section."""
        body = """## Description
This is a test issue.
"""
        result = validate_issue_body(body)
        assert result is False

    def test_issue_templates_exist(self):
        """Test that all required templates exist."""
        assert "feature" in ISSUE_TEMPLATES
        assert "bug" in ISSUE_TEMPLATES
        assert "chore" in ISSUE_TEMPLATES

    def test_issue_templates_structure(self):
        """Test that templates have required placeholders."""
        # Feature template
        assert "{title}" in ISSUE_TEMPLATES["feature"]
        assert "{description}" in ISSUE_TEMPLATES["feature"]
        assert "{requirements}" in ISSUE_TEMPLATES["feature"]
        assert "{workflow}" in ISSUE_TEMPLATES["feature"]

        # Bug template
        assert "{title}" in ISSUE_TEMPLATES["bug"]
        assert "{description}" in ISSUE_TEMPLATES["bug"]
        assert "{steps}" in ISSUE_TEMPLATES["bug"]
        assert "{workflow}" in ISSUE_TEMPLATES["bug"]

        # Chore template
        assert "{title}" in ISSUE_TEMPLATES["chore"]
        assert "{description}" in ISSUE_TEMPLATES["chore"]
        assert "{tasks}" in ISSUE_TEMPLATES["chore"]
        assert "{workflow}" in ISSUE_TEMPLATES["chore"]
