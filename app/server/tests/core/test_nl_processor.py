import pytest
import os
import json
from unittest.mock import patch, MagicMock, AsyncMock
from core.nl_processor import (
    analyze_intent,
    extract_requirements,
    classify_issue_type,
    suggest_adw_workflow,
    process_request
)
from core.data_models import ProjectContext
from tests.fixtures import api_responses


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


class TestNLProcessorEdgeCases:
    """Comprehensive edge case tests for NL Processor."""

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_empty_input(self, mock_anthropic_class):
        """Test handling of empty string input."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            # Should still process empty input and return valid response
            result = await analyze_intent("")
            assert "intent_type" in result

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_very_long_input(self, mock_anthropic_class):
        """Test handling of extremely long input."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_VERY_LONG_SUMMARY
        mock_client.messages.create.return_value = mock_response

        very_long_input = "A " + "very " * 1000 + "long request"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(very_long_input)
            assert result["intent_type"] in ["feature", "bug", "chore"]

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_unicode_characters(self, mock_anthropic_class):
        """Test handling of Unicode characters and emojis."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_UNICODE
        mock_client.messages.create.return_value = mock_response

        unicode_input = "Add emoji support 🎉 and i18n (中文, 日本語, العربية)"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(unicode_input)
            assert result["intent_type"] == "feature"
            assert result["technical_area"] == "i18n"

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_special_characters(self, mock_anthropic_class):
        """Test handling of special characters and markdown."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        special_input = 'Add **bold** and _italic_ with "quotes" and <tags>'

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(special_input)
            assert "intent_type" in result

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_whitespace_only(self, mock_anthropic_class):
        """Test handling of whitespace-only input."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        whitespace_input = "   \n  \t  \n  "

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(whitespace_input)
            assert "intent_type" in result

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_malformed_json_response(self, mock_anthropic_class):
        """Test handling of malformed JSON in API response."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.MALFORMED_JSON_RESPONSE
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            with pytest.raises(Exception) as exc_info:
                await analyze_intent("Add feature")
            assert "Error analyzing intent" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_response_with_extra_whitespace(self, mock_anthropic_class):
        """Test cleaning of extra whitespace in API response."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_WITH_WHITESPACE
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent("Add feature")
            assert result["intent_type"] == "feature"

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_nested_markdown_blocks(self, mock_anthropic_class):
        """Test cleaning of nested markdown code blocks."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        # Create a response with nested markdown blocks
        mock_response.content[0].text = f"```json\n{api_responses.INTENT_FEATURE_RESPONSE}\n```"
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent("Add feature")
            assert result["intent_type"] == "feature"

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_xss_attempt(self, mock_anthropic_class):
        """Test handling of potential XSS injection attempts."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_XSS_ATTEMPT
        mock_client.messages.create.return_value = mock_response

        xss_input = "<script>alert('XSS')</script>"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(xss_input)
            # Should process without error and return structured data
            assert "intent_type" in result

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_sql_injection_attempt(self, mock_anthropic_class):
        """Test handling of potential SQL injection attempts."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_SQL_INJECTION_ATTEMPT
        mock_client.messages.create.return_value = mock_response

        sql_input = "'; DROP TABLE users; --"

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            result = await analyze_intent(sql_input)
            # Should process without error
            assert "intent_type" in result

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_empty_response(self, mock_anthropic_class):
        """Test handling of empty requirements list."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.REQUIREMENTS_EMPTY_LIST
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            result = extract_requirements("Simple task", intent)
            assert isinstance(result, list)
            assert len(result) == 0

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_very_long_list(self, mock_anthropic_class):
        """Test handling of very long requirements list."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.REQUIREMENTS_VERY_LONG
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            result = extract_requirements("Complex feature", intent)
            assert isinstance(result, list)
            assert len(result) == 50

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_special_characters(self, mock_anthropic_class):
        """Test handling of special characters in requirements."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.REQUIREMENTS_SPECIAL_CHARS
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            result = extract_requirements("Feature with special chars", intent)
            assert len(result) == 4
            assert "**bold**" in result[0]

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_api_error(self, mock_anthropic_class):
        """Test error handling when API fails."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            with pytest.raises(Exception) as exc_info:
                extract_requirements("Test", intent)
            assert "Error extracting requirements" in str(exc_info.value)

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_malformed_json(self, mock_anthropic_class):
        """Test handling of malformed JSON in requirements response."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.MALFORMED_JSON_RESPONSE
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            intent = {"intent_type": "feature"}
            with pytest.raises(Exception) as exc_info:
                extract_requirements("Test", intent)
            assert "Error extracting requirements" in str(exc_info.value)

    def test_classify_issue_type_missing_intent_type(self):
        """Test classification with missing intent_type field."""
        intent = {"summary": "Some task"}
        result = classify_issue_type(intent)
        assert result == "feature"  # Default

    def test_classify_issue_type_empty_dict(self):
        """Test classification with empty intent dictionary."""
        intent = {}
        result = classify_issue_type(intent)
        assert result == "feature"  # Default

    def test_classify_issue_type_invalid_type(self):
        """Test classification with invalid intent_type value."""
        intent = {"intent_type": "invalid_type"}
        result = classify_issue_type(intent)
        assert result == "invalid_type"  # Returns as-is

    @pytest.mark.parametrize("issue_type,complexity,expected_workflow,expected_model", [
        ("bug", "low", "adw_plan_build_test_iso", "base"),
        ("bug", "medium", "adw_plan_build_test_iso", "base"),
        ("bug", "high", "adw_plan_build_test_iso", "base"),
        ("chore", "low", "adw_sdlc_iso", "base"),
        ("chore", "medium", "adw_sdlc_iso", "base"),
        ("chore", "high", "adw_sdlc_iso", "base"),
        ("feature", "low", "adw_sdlc_iso", "base"),
        ("feature", "medium", "adw_plan_build_test_iso", "base"),
        ("feature", "high", "adw_plan_build_test_iso", "heavy"),
    ])
    def test_suggest_adw_workflow_all_combinations(self, issue_type, complexity, expected_workflow, expected_model):
        """Test all combinations of issue types and complexity levels."""
        workflow, model_set = suggest_adw_workflow(issue_type, complexity)
        assert workflow == expected_workflow
        assert model_set == expected_model

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_with_no_framework(self, mock_extract, mock_analyze):
        """Test processing with no framework detected."""
        mock_analyze.return_value = {
            "intent_type": "feature",
            "summary": "Add feature",
            "technical_area": "general"
        }
        mock_extract.return_value = ["Requirement 1"]

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=True,
            framework=None,
            backend=None,
            complexity="low"
        )

        result = await process_request("Add feature", project_context)
        assert result.title == "Add feature"
        assert "general" in result.labels

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_with_backend(self, mock_extract, mock_analyze):
        """Test processing with backend framework."""
        mock_analyze.return_value = {
            "intent_type": "feature",
            "summary": "Add API endpoint",
            "technical_area": "API"
        }
        mock_extract.return_value = ["Create REST endpoint", "Add validation"]

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            framework="react-vite",
            backend="fastapi",
            complexity="medium"
        )

        result = await process_request("Add API endpoint", project_context)
        assert result.title == "Add API endpoint"
        assert "react-vite" in result.labels

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_extract_requirements_error(self, mock_extract, mock_analyze):
        """Test error handling when requirement extraction fails."""
        mock_analyze.return_value = {
            "intent_type": "feature",
            "summary": "Add feature",
            "technical_area": "general"
        }
        mock_extract.side_effect = Exception("Extraction failed")

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            complexity="low"
        )

        with pytest.raises(Exception) as exc_info:
            await process_request("Add feature", project_context)
        assert "Error processing NL request" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_empty_requirements(self, mock_extract, mock_analyze):
        """Test processing with empty requirements list."""
        mock_analyze.return_value = {
            "intent_type": "feature",
            "summary": "Simple task",
            "technical_area": "general"
        }
        mock_extract.return_value = []

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            complexity="low"
        )

        result = await process_request("Simple task", project_context)
        assert result.title == "Simple task"
        assert "## Requirements" in result.body

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_missing_summary(self, mock_extract, mock_analyze):
        """Test processing when summary is missing from intent."""
        mock_analyze.return_value = {
            "intent_type": "feature",
            "technical_area": "general"
            # summary is missing
        }
        mock_extract.return_value = ["Requirement 1"]

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            complexity="low"
        )

        input_text = "Add a new feature to the system"
        result = await process_request(input_text, project_context)
        # Should use truncated input as title
        assert len(result.title) <= 100

    @pytest.mark.asyncio
    @patch('core.nl_processor.analyze_intent')
    @patch('core.nl_processor.extract_requirements')
    async def test_process_request_missing_technical_area(self, mock_extract, mock_analyze):
        """Test processing when technical_area is missing from intent."""
        mock_analyze.return_value = {
            "intent_type": "chore",
            "summary": "Update dependencies"
            # technical_area is missing
        }
        mock_extract.return_value = ["Update package.json"]

        project_context = ProjectContext(
            path="/test/project",
            is_new_project=False,
            complexity="low"
        )

        result = await process_request("Update deps", project_context)
        assert result.title == "Update dependencies"
        assert "general" in result.labels  # Default technical area
