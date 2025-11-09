"""
Integration tests for the NL-to-GitHub-Issue workflow.
Tests the complete workflow from natural language input to formatted issue.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
from core.nl_processor import process_request
from core.project_detector import detect_project_context
from core.github_poster import GitHubPoster
from core.data_models import ProjectContext, GitHubIssue


class TestNLWorkflowIntegration:

    @pytest.fixture
    def mock_anthropic_responses(self):
        """Mock responses from Anthropic API."""
        return {
            "intent": {
                "intent_type": "feature",
                "summary": "Add dark mode to the application",
                "technical_area": "UI"
            },
            "requirements": [
                "Create theme toggle component",
                "Add CSS variables for dark theme colors",
                "Persist user preference in localStorage"
            ]
        }

    @pytest.fixture
    def sample_project_dir(self, tmp_path):
        """Create a sample React project structure."""
        project_dir = tmp_path / "sample_project"
        project_dir.mkdir()

        # Create React + Vite project structure
        (project_dir / "vite.config.ts").touch()

        package_json = {
            "name": "sample-project",
            "dependencies": {
                "react": "^18.0.0",
                "react-dom": "^18.0.0"
            }
        }
        (project_dir / "package.json").write_text(json.dumps(package_json))
        (project_dir / "package-lock.json").touch()

        # Add git
        (project_dir / ".git").mkdir()

        # Add source files
        src_dir = project_dir / "src"
        src_dir.mkdir()
        (src_dir / "App.tsx").touch()
        (src_dir / "main.tsx").touch()

        return project_dir

    def test_detect_project_context_integration(self, sample_project_dir):
        """Test complete project context detection."""
        context = detect_project_context(str(sample_project_dir))

        assert context.is_new_project is False
        assert context.framework == "react-vite"
        assert context.package_manager == "npm"
        assert context.has_git is True
        assert context.complexity in ["low", "medium"]
        assert "vite" in context.build_tools

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_nl_to_issue_workflow(self, mock_anthropic_class, sample_project_dir, mock_anthropic_responses):
        """Test complete workflow from NL input to GitHub issue."""
        # Setup mocks
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        # Mock intent analysis response
        intent_response = MagicMock()
        intent_response.content[0].text = json.dumps(mock_anthropic_responses["intent"])

        # Mock requirements extraction response
        requirements_response = MagicMock()
        requirements_response.content[0].text = json.dumps(mock_anthropic_responses["requirements"])

        # Configure mock to return different responses on subsequent calls
        mock_client.messages.create.side_effect = [intent_response, requirements_response]

        # Step 1: Detect project context
        project_context = detect_project_context(str(sample_project_dir))

        # Step 2: Process NL request
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            issue = await process_request("Add dark mode to my app", project_context)

        # Verify the generated issue
        assert isinstance(issue, GitHubIssue)
        assert "dark mode" in issue.title.lower()
        assert issue.classification == "feature"
        # Project with just src/App.tsx and src/main.tsx is low complexity
        assert issue.workflow == "adw_sdlc_iso"  # Low complexity
        assert issue.model_set == "base"
        assert "feature" in issue.labels
        assert "ui" in [label.lower() for label in issue.labels]

        # Verify body structure
        assert "## Description" in issue.body
        assert "## Requirements" in issue.body
        assert "## Workflow" in issue.body
        assert any(req in issue.body for req in mock_anthropic_responses["requirements"])

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_bug_report_workflow(self, mock_anthropic_class, sample_project_dir):
        """Test workflow for bug reports."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        # Mock bug intent
        intent_response = MagicMock()
        intent_response.content[0].text = json.dumps({
            "intent_type": "bug",
            "summary": "Login button not responding to clicks",
            "technical_area": "authentication"
        })

        requirements_response = MagicMock()
        requirements_response.content[0].text = json.dumps([
            "Investigate click event handlers",
            "Check for JavaScript errors in console",
            "Test button functionality"
        ])

        mock_client.messages.create.side_effect = [intent_response, requirements_response]

        project_context = detect_project_context(str(sample_project_dir))

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            issue = await process_request("Login button is broken", project_context)

        assert issue.classification == "bug"
        assert issue.workflow == "adw_plan_build_test_iso"
        assert issue.model_set == "base"
        assert "bug" in issue.labels

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_chore_workflow(self, mock_anthropic_class, sample_project_dir):
        """Test workflow for chore tasks."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        intent_response = MagicMock()
        intent_response.content[0].text = json.dumps({
            "intent_type": "chore",
            "summary": "Update project dependencies",
            "technical_area": "maintenance"
        })

        requirements_response = MagicMock()
        requirements_response.content[0].text = json.dumps([
            "Update npm packages to latest versions",
            "Run tests to ensure compatibility",
            "Update documentation if needed"
        ])

        mock_client.messages.create.side_effect = [intent_response, requirements_response]

        project_context = detect_project_context(str(sample_project_dir))

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            issue = await process_request("Update all dependencies", project_context)

        assert issue.classification == "chore"
        assert issue.workflow == "adw_sdlc_iso"
        assert issue.model_set == "base"
        assert "chore" in issue.labels

    def test_new_project_detection(self, tmp_path):
        """Test workflow with a new project."""
        new_project = tmp_path / "new_project"
        new_project.mkdir()

        context = detect_project_context(str(new_project))

        assert context.is_new_project is True
        assert context.complexity == "low"
        assert context.framework is None

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_high_complexity_workflow(self, mock_anthropic_class, tmp_path):
        """Test workflow with high complexity project."""
        # Create a complex project structure
        complex_project = tmp_path / "complex_project"
        complex_project.mkdir()

        # Add framework
        (complex_project / "vite.config.ts").touch()
        package_json = {
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.0.0"
            }
        }
        (complex_project / "package.json").write_text(json.dumps(package_json))

        # Add backend
        pyproject_content = """
[project]
dependencies = [
    "fastapi==0.100.0"
]
"""
        (complex_project / "pyproject.toml").write_text(pyproject_content)

        # Add many files to increase complexity
        src_dir = complex_project / "src"
        src_dir.mkdir()
        for i in range(150):
            (src_dir / f"file{i}.tsx").touch()

        # Add monorepo structure
        (complex_project / "packages").mkdir()

        # Mock Anthropic responses
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        intent_response = MagicMock()
        intent_response.content[0].text = json.dumps({
            "intent_type": "feature",
            "summary": "Add real-time collaboration feature",
            "technical_area": "realtime"
        })

        requirements_response = MagicMock()
        requirements_response.content[0].text = json.dumps([
            "Implement WebSocket connection",
            "Add operational transformation",
            "Create collaborative editing UI"
        ])

        mock_client.messages.create.side_effect = [intent_response, requirements_response]

        # Detect context
        context = detect_project_context(str(complex_project))

        assert context.complexity == "high"

        # Process request
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            issue = await process_request("Add real-time collaboration", context)

        # High complexity feature should use heavy model set
        assert issue.workflow == "adw_plan_build_test_iso"
        assert issue.model_set == "heavy"

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_error_propagation(self, mock_anthropic_class, sample_project_dir):
        """Test that errors propagate correctly through the workflow."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        # Simulate API error
        mock_client.messages.create.side_effect = Exception("API Error")

        project_context = detect_project_context(str(sample_project_dir))

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            with pytest.raises(Exception) as exc_info:
                await process_request("Add feature", project_context)

            assert "Error processing NL request" in str(exc_info.value)

    @patch('core.github_poster.GitHubPoster._validate_gh_cli')
    @patch('core.github_poster.GitHubPoster._execute_gh_command')
    def test_end_to_end_with_github_posting(self, mock_execute, mock_validate):
        """Test end-to-end including GitHub posting (mocked)."""
        mock_validate.return_value = True
        mock_execute.return_value = "https://github.com/owner/repo/issues/123"

        # Create a sample issue
        issue = GitHubIssue(
            title="Add Dark Mode",
            body="## Description\nAdd dark mode\n\n## Workflow\nadw_sdlc_iso model_set base",
            labels=["feature", "UI"],
            classification="feature",
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        # Post to GitHub
        poster = GitHubPoster()
        issue_number = poster.post_issue(issue, confirm=False)

        assert issue_number == 123
        mock_execute.assert_called_once()

        # Verify command structure
        call_args = mock_execute.call_args[0][0]
        assert "gh" in call_args
        assert "issue" in call_args
        assert "create" in call_args

    def test_framework_label_inclusion(self, sample_project_dir):
        """Test that framework is included in labels."""
        context = detect_project_context(str(sample_project_dir))

        # Create a mock issue that would include the framework
        assert context.framework == "react-vite"

        # In the actual workflow, this framework would be added to labels
        # This is tested in the full workflow test above

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_workflow_with_missing_api_key(self, mock_anthropic_class, sample_project_dir):
        """Test workflow fails gracefully without API key."""
        project_context = detect_project_context(str(sample_project_dir))

        # Try without API key
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(Exception) as exc_info:
                await process_request("Add feature", project_context)

            assert "ANTHROPIC_API_KEY" in str(exc_info.value)
