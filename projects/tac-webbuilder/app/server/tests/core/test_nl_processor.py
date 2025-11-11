import pytest
import os
import json
from unittest.mock import patch, MagicMock
from core.nl_processor import (
    analyze_intent,
    extract_requirements,
    classify_issue_type,
    suggest_adw_workflow,
    process_request
)
from core.data_models import ProjectContext


class TestNLProcessor:

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_feature(self, mock_anthropic_class):
        """Test analyzing intent for a feature request."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = json.dumps({
            "intent_type": "feature",
            "summary": "Add dark mode to the application",
            "technical_area": "UI"
        })
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent("Add dark mode to my app")

            assert result["intent_type"] == "feature"
            assert result["summary"] == "Add dark mode to the application"
            assert result["technical_area"] == "UI"
            mock_client.messages.create.assert_called_once()

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_bug(self, mock_anthropic_class):
        """Test analyzing intent for a bug report."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = json.dumps({
            "intent_type": "bug",
            "summary": "Login button is not responding to clicks",
            "technical_area": "authentication"
        })
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent("Login button not working")

            assert result["intent_type"] == "bug"
            assert "Login button" in result["summary"]
            assert result["technical_area"] == "authentication"

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_clean_markdown(self, mock_anthropic_class):
        """Test that markdown code blocks are cleaned from responses."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = f"""```json
{json.dumps({"intent_type": "chore", "summary": "Update dependencies", "technical_area": "maintenance"})}
```"""
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent("Update all npm packages")

            assert result["intent_type"] == "chore"
            assert "dependencies" in result["summary"]

    @pytest.mark.asyncio
    async def test_analyze_intent_no_api_key(self):
        """Test error when ANTHROPIC_API_KEY is not set."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(Exception) as exc_info:
                await analyze_intent("Add dark mode")

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_api_error(self, mock_anthropic_class):
        """Test handling of API errors."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            with pytest.raises(Exception) as exc_info:
                await analyze_intent("Add dark mode")

            assert "Error analyzing intent with Anthropic" in str(exc_info.value)

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_success(self, mock_anthropic_class):
        """Test extracting requirements from NL input."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = json.dumps([
            "Implement JWT authentication",
            "Create login form with email and password fields",
            "Add password hashing with bcrypt"
        ])
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature", "summary": "Add user authentication"}
            result = extract_requirements("Add user authentication to my app", intent)

            assert len(result) == 3
            assert "JWT" in result[0]
            assert "login form" in result[1]
            assert "bcrypt" in result[2]

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_clean_markdown(self, mock_anthropic_class):
        """Test that markdown is cleaned from requirement extraction."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = '```json\n["Requirement 1", "Requirement 2"]\n```'
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            result = extract_requirements("Test input", intent)

            assert len(result) == 2
            assert result[0] == "Requirement 1"

    def test_extract_requirements_no_api_key(self):
        """Test error when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            intent = {"intent_type": "feature"}

            with pytest.raises(Exception) as exc_info:
                extract_requirements("Test input", intent)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    def test_classify_issue_type_feature(self):
        """Test classifying a feature request."""
        intent = {"intent_type": "feature", "summary": "Add dark mode"}
        result = classify_issue_type(intent)
        assert result == "feature"

    def test_classify_issue_type_bug(self):
        """Test classifying a bug report."""
        intent = {"intent_type": "bug", "summary": "Login broken"}
        result = classify_issue_type(intent)
        assert result == "bug"

    def test_classify_issue_type_chore(self):
        """Test classifying a chore."""
        intent = {"intent_type": "chore", "summary": "Update deps"}
        result = classify_issue_type(intent)
        assert result == "chore"

    def test_classify_issue_type_default(self):
        """Test default classification when intent_type is missing."""
        intent = {"summary": "Some task"}
        result = classify_issue_type(intent)
        assert result == "feature"

    def test_suggest_adw_workflow_bug(self):
        """Test workflow suggestion for bugs."""
        workflow, model_set = suggest_adw_workflow("bug", "low")
        assert workflow == "adw_plan_build_test_iso"
        assert model_set == "base"

    def test_suggest_adw_workflow_chore(self):
        """Test workflow suggestion for chores."""
        workflow, model_set = suggest_adw_workflow("chore", "low")
        assert workflow == "adw_sdlc_iso"
        assert model_set == "base"

    def test_suggest_adw_workflow_feature_low(self):
        """Test workflow suggestion for low complexity features."""
        workflow, model_set = suggest_adw_workflow("feature", "low")
        assert workflow == "adw_sdlc_iso"
        assert model_set == "base"

    def test_suggest_adw_workflow_feature_medium(self):
        """Test workflow suggestion for medium complexity features."""
        workflow, model_set = suggest_adw_workflow("feature", "medium")
        assert workflow == "adw_plan_build_test_iso"
        assert model_set == "base"

    def test_suggest_adw_workflow_feature_high(self):
        """Test workflow suggestion for high complexity features."""
        workflow, model_set = suggest_adw_workflow("feature", "high")
        assert workflow == "adw_plan_build_test_iso"
        assert model_set == "heavy"

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_success(self, mock_extract, mock_analyze):
        """Test end-to-end request processing."""
        # Mock the async function - use AsyncMock or return the dict directly

        mock_analyze.return_value = {
            "intent_type": "feature",
            "summary": "Add dark mode",
            "technical_area": "UI"
        }

        mock_extract.return_value = [
            "Create theme toggle component",
            "Add CSS variables for light/dark themes",
            "Persist theme preference in localStorage"
        ]

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            framework="react-vite",
            backend=None,
            complexity="medium"
        )

        result = await process_request("Add dark mode to my app", project_context)

        assert result.title == "Add dark mode"
        assert result.classification == "feature"
        assert result.workflow == "adw_plan_build_test_iso"
        assert result.model_set == "base"
        assert "ui" in result.labels  # Labels are lowercased
        assert "react-vite" in result.labels
        assert "## Description" in result.body
        assert "## Requirements" in result.body

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    async def test_process_request_error_handling(self, mock_analyze):
        """Test error handling in process_request."""
        mock_analyze.side_effect = Exception("API Error")

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            complexity="low"
        )

        with pytest.raises(Exception) as exc_info:
            await process_request("Add feature", project_context)

        assert "Error processing NL request" in str(exc_info.value)
