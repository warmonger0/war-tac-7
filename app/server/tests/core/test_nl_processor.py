"""Unit tests for the Natural Language Processor module."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from core.nl_processor import NLProcessor, process_nl_request
from core.webbuilder_models import (
    NLProcessingRequest,
    GitHubIssue,
    ProjectContext,
    WorkflowSuggestion
)


class TestNLProcessor:
    """Test suite for NLProcessor class."""

    @pytest.fixture
    def mock_anthropic_client(self):
        """Create a mock Anthropic client."""
        with patch('core.nl_processor.Anthropic') as mock:
            yield mock

    @pytest.fixture
    def nl_processor(self, mock_anthropic_client):
        """Create NLProcessor instance with mocked Anthropic client."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            processor = NLProcessor()
            return processor

    @pytest.mark.asyncio
    async def test_process_simple_feature_request(self, nl_processor, mock_anthropic_client):
        """Test processing a simple feature request."""
        # Mock Anthropic responses
        mock_response = Mock()
        mock_response.content = [Mock(text='{"primary_intent": "Add dark mode feature", '
                                       '"action_type": "create", '
                                       '"target_components": ["UI", "settings"], '
                                       '"technical_keywords": ["dark mode", "theme"], '
                                       '"suggested_issue_type": "feature", '
                                       '"ambiguity_level": "low"}')]

        nl_processor.client.messages.create = Mock(return_value=mock_response)

        # Process request
        issue = await nl_processor.process_request(
            "Add dark mode to the application settings",
            None
        )

        # Assertions
        assert isinstance(issue, GitHubIssue)
        assert issue.classification == "feature"
        assert issue.title
        assert issue.body
        assert len(issue.labels) > 0
        assert issue.workflow in ["adw_simple_iso", "adw_plan_build_test_iso", "adw_sdlc_iso"]

    @pytest.mark.asyncio
    async def test_process_bug_report(self, nl_processor, mock_anthropic_client):
        """Test processing a bug report."""
        # Mock Anthropic responses for bug
        mock_response = Mock()
        mock_response.content = [Mock(text='{"primary_intent": "Fix login button issue", '
                                       '"action_type": "fix", '
                                       '"target_components": ["authentication", "UI"], '
                                       '"technical_keywords": ["login", "button", "not working"], '
                                       '"suggested_issue_type": "bug", '
                                       '"ambiguity_level": "low"}')]

        nl_processor.client.messages.create = Mock(return_value=mock_response)

        # Process request
        issue = await nl_processor.process_request(
            "Login button not working on the homepage",
            None
        )

        # Assertions
        assert issue.classification == "bug"
        assert "login" in issue.title.lower() or "fix" in issue.title.lower()
        assert issue.workflow == "adw_plan_build_test_iso"  # Bugs should use this workflow
        assert issue.model_set == "base"

    @pytest.mark.asyncio
    async def test_analyze_intent(self, nl_processor):
        """Test intent analysis functionality."""
        # Mock Anthropic response
        mock_response = Mock()
        mock_response.content = [Mock(text='{"primary_intent": "Build user dashboard", '
                                       '"action_type": "create", '
                                       '"target_components": ["dashboard"], '
                                       '"technical_keywords": ["dashboard", "user"], '
                                       '"suggested_issue_type": "feature", '
                                       '"ambiguity_level": "medium"}')]

        nl_processor.client.messages.create = Mock(return_value=mock_response)

        # Analyze intent
        intent = await nl_processor.analyze_intent("Create a user dashboard with analytics")

        # Assertions
        assert intent["primary_intent"] == "Build user dashboard"
        assert intent["action_type"] == "create"
        assert "dashboard" in intent["target_components"]
        assert intent["suggested_issue_type"] == "feature"
        assert intent["ambiguity_level"] == "medium"

    def test_extract_requirements(self, nl_processor):
        """Test requirement extraction."""
        # Mock Anthropic response
        mock_response = Mock()
        mock_response.content = [Mock(text="- User authentication required\n"
                                       "- Dashboard should load in under 2 seconds\n"
                                       "- Mobile responsive design")]

        nl_processor.client.messages.create = Mock(return_value=mock_response)

        # Extract requirements
        intent = {"primary_intent": "Build dashboard"}
        requirements = nl_processor.extract_requirements(
            "Create a fast, mobile-friendly dashboard with auth",
            intent
        )

        # Assertions
        assert len(requirements) == 3
        assert "User authentication required" in requirements
        assert "Dashboard should load in under 2 seconds" in requirements
        assert "Mobile responsive design" in requirements

    def test_determine_issue_type(self, nl_processor):
        """Test issue type determination."""
        # Test feature
        intent = {"action_type": "create", "suggested_issue_type": "feature"}
        assert nl_processor.determine_issue_type(intent) == "feature"

        # Test bug
        intent = {"action_type": "fix", "suggested_issue_type": "bug"}
        assert nl_processor.determine_issue_type(intent) == "bug"

        # Test chore
        intent = {"action_type": "analyze", "suggested_issue_type": "chore"}
        assert nl_processor.determine_issue_type(intent) == "chore"

        # Test unknown defaults to suggested
        intent = {"action_type": "unknown", "suggested_issue_type": "feature"}
        assert nl_processor.determine_issue_type(intent) == "feature"

    def test_suggest_workflow_simple(self, nl_processor):
        """Test workflow suggestion for simple tasks."""
        intent = {
            "ambiguity_level": "low",
            "target_components": ["button"]
        }
        requirements = ["Add click handler"]

        suggestion = nl_processor.suggest_workflow(intent, None, requirements)

        assert isinstance(suggestion, WorkflowSuggestion)
        assert suggestion.workflow_name in ["adw_simple_iso", "adw_plan_build_test_iso"]
        assert suggestion.model_set == "base"

    def test_suggest_workflow_complex(self, nl_processor):
        """Test workflow suggestion for complex tasks."""
        intent = {
            "ambiguity_level": "high",
            "target_components": ["auth", "database", "api", "ui", "testing"]
        }
        requirements = [f"Requirement {i}" for i in range(15)]  # Many requirements

        context = ProjectContext(
            path="/test",
            is_new_project=False,
            complexity="high",
            framework="react-vite",
            backend="fastapi"
        )

        suggestion = nl_processor.suggest_workflow(intent, context, requirements)

        assert suggestion.workflow_name == "adw_sdlc_iso"
        assert suggestion.model_set == "heavy"

    def test_generate_title(self, nl_processor):
        """Test title generation."""
        # Test with primary intent
        intent = {"primary_intent": "Implement user authentication system"}
        title = nl_processor.generate_title("Add auth", intent)
        assert title == "Implement user authentication system"

        # Test without primary intent (fallback)
        intent = {"primary_intent": ""}
        title = nl_processor.generate_title("Add authentication to the app. It should be secure.", intent)
        assert title == "Add authentication to the app"

        # Test capitalization
        intent = {"primary_intent": "add dark mode"}
        title = nl_processor.generate_title("add dark mode", intent)
        assert title == "Add dark mode"

    @pytest.mark.asyncio
    async def test_process_nl_request_with_error(self, mock_anthropic_client):
        """Test error handling in process_nl_request."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            # Mock to raise an exception
            mock_anthropic_client.side_effect = Exception("API Error")

            request = NLProcessingRequest(
                nl_input="Test request",
                auto_detect_context=False
            )

            response = await process_nl_request(request)

            assert response.error == "API Error"
            assert response.confidence_score == 0.0
            assert response.issue.title == "Error processing request"

    @pytest.mark.asyncio
    async def test_process_nl_request_with_project_context(self, mock_anthropic_client):
        """Test processing with project context detection."""
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            with patch('core.nl_processor.detect_project_context') as mock_detect:
                # Mock project detection
                mock_detect.return_value = ProjectContext(
                    path="/test/project",
                    is_new_project=False,
                    framework="react-vite",
                    backend="fastapi",
                    complexity="medium",
                    build_tools=["npm"],
                    has_git=True,
                    detected_files=["package.json", "src/App.tsx"]
                )

                # Mock Anthropic responses
                mock_instance = Mock()
                mock_response = Mock()
                mock_response.content = [Mock(text='{"primary_intent": "Add feature", '
                                               '"action_type": "create", '
                                               '"target_components": ["component"], '
                                               '"technical_keywords": ["feature"], '
                                               '"suggested_issue_type": "feature", '
                                               '"ambiguity_level": "low"}')]
                mock_instance.messages.create = Mock(return_value=mock_response)
                mock_anthropic_client.return_value = mock_instance

                request = NLProcessingRequest(
                    nl_input="Add new feature",
                    project_path="/test/project",
                    auto_detect_context=True
                )

                response = await process_nl_request(request)

                assert response.project_context is not None
                assert response.project_context.framework == "react-vite"
                assert response.project_context.backend == "fastapi"
                mock_detect.assert_called_once_with("/test/project")

    def test_build_issue_body(self, nl_processor):
        """Test building complete issue body."""
        description = "## User Request\nAdd dark mode"
        requirements = ["Toggle in settings", "Save preference"]
        technical_approach = "### Components\n- Settings UI\n- Theme Context"
        workflow_suggestion = WorkflowSuggestion(
            workflow_name="adw_plan_build_test_iso",
            model_set="base",
            reasoning="Medium complexity feature"
        )

        body = nl_processor.build_issue_body(
            description,
            requirements,
            technical_approach,
            workflow_suggestion,
            "feature"
        )

        assert "## User Request" in body
        assert "## Requirements" in body
        assert "Toggle in settings" in body
        assert "## Technical Approach" in body
        assert "## Workflow" in body
        assert "adw_plan_build_test_iso model_set base" in body
        assert "/feature" in body

    def test_determine_labels(self, nl_processor):
        """Test label determination."""
        intent = {
            "target_components": ["auth", "database"],
            "ambiguity_level": "high"
        }

        context = ProjectContext(
            path="/test",
            is_new_project=False,
            framework="react-vite",
            backend="fastapi",
            complexity="medium"
        )

        labels = nl_processor.determine_labels(intent, "feature", context)

        assert "feature" in labels
        assert "webbuilder" in labels
        assert "react-vite" in labels
        assert "fastapi" in labels
        assert "auth" in labels
        assert "database" in labels
        assert "needs-clarification" in labels  # Due to high ambiguity

    @pytest.mark.asyncio
    async def test_malformed_json_response(self, nl_processor):
        """Test handling of malformed JSON response from Anthropic."""
        # Mock Anthropic response with invalid JSON
        mock_response = Mock()
        mock_response.content = [Mock(text="This is not valid JSON")]

        nl_processor.client.messages.create = Mock(return_value=mock_response)

        # Should fallback to basic analysis
        intent = await nl_processor.analyze_intent("Test input")

        assert intent["primary_intent"] == "Test input"  # Uses first 100 chars
        assert intent["action_type"] == "create"
        assert intent["ambiguity_level"] == "high"
        assert "Could not parse user intent clearly" in intent.get("needs_clarification", [])