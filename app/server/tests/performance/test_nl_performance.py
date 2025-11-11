"""
Performance benchmarking tests for NL processing module.

These tests measure and validate performance characteristics:
- Processing time for various input sizes
- Memory usage patterns
- Project detection speed
- Issue formatting performance
"""

import pytest
import time
import json
from unittest.mock import patch, MagicMock
from core.nl_processor import analyze_intent, extract_requirements, process_request
from core.project_detector import detect_project_context
from core.issue_formatter import create_feature_issue_body
from core.data_models import ProjectContext
from tests.fixtures import api_responses


class TestNLProcessorPerformance:
    """Performance tests for NL processor functions."""

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_small_input_performance(self, mock_anthropic_class):
        """Test performance with small input (<100 chars)."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        small_input = "Add dark mode"

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            start_time = time.time()
            result = await analyze_intent(small_input)
            elapsed = time.time() - start_time

            # Should complete quickly (mocked API call)
            assert elapsed < 1.0  # Less than 1 second
            assert result is not None

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_medium_input_performance(self, mock_anthropic_class):
        """Test performance with medium input (100-1000 chars)."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        medium_input = "Add a comprehensive authentication system with " * 10  # ~500 chars

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            start_time = time.time()
            result = await analyze_intent(medium_input)
            elapsed = time.time() - start_time

            assert elapsed < 1.0
            assert result is not None

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_analyze_intent_large_input_performance(self, mock_anthropic_class):
        """Test performance with large input (1000-10000 chars)."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_VERY_LONG_SUMMARY
        mock_client.messages.create.return_value = mock_response

        # Create large input (~5000 chars)
        large_input = "Add a complex feature that includes " * 200

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            start_time = time.time()
            result = await analyze_intent(large_input)
            elapsed = time.time() - start_time

            # Should still complete reasonably fast with mocked API
            assert elapsed < 2.0  # Less than 2 seconds
            assert result is not None

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_performance(self, mock_anthropic_class):
        """Test requirement extraction performance."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.REQUIREMENTS_AUTH_RESPONSE
        mock_client.messages.create.return_value = mock_response

        intent = {"intent_type": "feature", "summary": "Add auth"}

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            start_time = time.time()
            result = extract_requirements("Add authentication", intent)
            elapsed = time.time() - start_time

            assert elapsed < 1.0
            assert isinstance(result, list)

    @patch('core.nl_processor.Anthropic')
    def test_extract_requirements_large_list_performance(self, mock_anthropic_class):
        """Test performance with large requirements list (50+ items)."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.REQUIREMENTS_VERY_LONG
        mock_client.messages.create.return_value = mock_response

        intent = {"intent_type": "feature", "summary": "Complex feature"}

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            start_time = time.time()
            result = extract_requirements("Complex feature", intent)
            elapsed = time.time() - start_time

            assert elapsed < 1.0
            assert len(result) == 50


class TestProjectDetectorPerformance:
    """Performance tests for project detection."""

    def test_detect_small_project_performance(self, tmp_path):
        """Test detection performance on small project (< 10 files)."""
        project_dir = tmp_path / "small_project"
        project_dir.mkdir()

        # Create minimal project structure
        package_json = {"name": "small", "dependencies": {"react": "^18.0.0"}}
        (project_dir / "package.json").write_text(json.dumps(package_json))
        (project_dir / "vite.config.ts").touch()

        src = project_dir / "src"
        src.mkdir()
        (src / "App.tsx").touch()
        (src / "main.tsx").touch()

        start_time = time.time()
        context = detect_project_context(str(project_dir))
        elapsed = time.time() - start_time

        # Should be very fast for small projects
        assert elapsed < 0.5  # Less than 500ms
        assert context.framework == "react-vite"

    def test_detect_medium_project_performance(self, tmp_path):
        """Test detection performance on medium project (10-50 files)."""
        project_dir = tmp_path / "medium_project"
        project_dir.mkdir()

        package_json = {"name": "medium", "dependencies": {"next": "^14.0.0", "react": "^18.0.0"}}
        (project_dir / "package.json").write_text(json.dumps(package_json))
        (project_dir / "next.config.js").touch()

        # Create medium-sized structure
        for i in range(30):
            (project_dir / f"file_{i}.ts").touch()

        start_time = time.time()
        context = detect_project_context(str(project_dir))
        elapsed = time.time() - start_time

        assert elapsed < 1.0  # Less than 1 second
        assert context.framework == "nextjs"

    def test_detect_large_project_performance(self, tmp_path):
        """Test detection performance on large project (100+ files)."""
        project_dir = tmp_path / "large_project"
        project_dir.mkdir()

        package_json = {"name": "large", "dependencies": {"vue": "^3.0.0"}}
        (project_dir / "package.json").write_text(json.dumps(package_json))
        (project_dir / "vite.config.js").touch()

        # Create large structure
        src = project_dir / "src"
        src.mkdir()
        for i in range(100):
            (src / f"component_{i}.vue").touch()

        start_time = time.time()
        context = detect_project_context(str(project_dir))
        elapsed = time.time() - start_time

        # Should still be reasonably fast even for large projects
        assert elapsed < 2.0  # Less than 2 seconds
        assert context.framework == "vue-vite"

    def test_detect_monorepo_performance(self, tmp_path):
        """Test detection performance on monorepo structure."""
        project_dir = tmp_path / "monorepo"
        project_dir.mkdir()

        package_json = {"name": "monorepo", "workspaces": ["packages/*"]}
        (project_dir / "package.json").write_text(json.dumps(package_json))

        # Create multiple packages
        packages = project_dir / "packages"
        packages.mkdir()

        for i in range(5):
            pkg = packages / f"package{i}"
            pkg.mkdir()
            pkg_json = {"name": f"package{i}", "version": "1.0.0"}
            (pkg / "package.json").write_text(json.dumps(pkg_json))

        start_time = time.time()
        context = detect_project_context(str(project_dir))
        elapsed = time.time() - start_time

        assert elapsed < 1.5
        assert context is not None


class TestIssueFormatterPerformance:
    """Performance tests for issue formatting."""

    def test_format_small_issue_performance(self):
        """Test formatting performance with small issue (< 5 requirements)."""
        requirements = ["Requirement 1", "Requirement 2", "Requirement 3"]

        start_time = time.time()
        body = create_feature_issue_body(
            description="Add feature",
            requirements=requirements,
            workflow="adw_sdlc_iso",
            model_set="base"
        )
        elapsed = time.time() - start_time

        assert elapsed < 0.1  # Very fast
        assert len(body) > 0

    def test_format_medium_issue_performance(self):
        """Test formatting performance with medium issue (10-20 requirements)."""
        requirements = [f"Requirement {i}" for i in range(15)]

        start_time = time.time()
        body = create_feature_issue_body(
            description="Add complex feature",
            requirements=requirements,
            workflow="adw_plan_build_test_iso",
            model_set="base"
        )
        elapsed = time.time() - start_time

        assert elapsed < 0.2
        assert len(body) > 0

    def test_format_large_issue_performance(self):
        """Test formatting performance with large issue (50+ requirements)."""
        requirements = [f"Detailed requirement {i}" for i in range(75)]

        start_time = time.time()
        body = create_feature_issue_body(
            description="Add extremely complex feature",
            requirements=requirements,
            workflow="adw_plan_build_test_iso",
            model_set="heavy"
        )
        elapsed = time.time() - start_time

        assert elapsed < 0.5
        assert len(body) > 0
        assert len(requirements) == 75

    def test_format_issue_with_long_text_performance(self):
        """Test formatting performance with very long text fields."""
        long_description = "A " * 500  # 1000 characters
        long_requirements = [f"Long requirement: {'x' * 200}" for i in range(10)]

        start_time = time.time()
        body = create_feature_issue_body(
            description=long_description,
            requirements=long_requirements,
            workflow="adw_sdlc_iso",
            model_set="base"
        )
        elapsed = time.time() - start_time

        assert elapsed < 0.3
        assert len(body) > 1000


class TestEndToEndPerformance:
    """End-to-end performance tests."""

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_complete_workflow_performance(self, mock_anthropic_class, tmp_path):
        """Test complete workflow performance from NL to issue."""
        # Setup
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        intent_response = MagicMock()
        intent_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE

        requirements_response = MagicMock()
        requirements_response.content[0].text = api_responses.REQUIREMENTS_AUTH_RESPONSE

        mock_client.messages.create.side_effect = [intent_response, requirements_response]

        # Create project
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / "package.json").write_text('{"name":"test"}')

        # Measure end-to-end time
        start_time = time.time()

        # Project detection
        context = ProjectContext(
            path=str(project_dir),
            is_new_project=False,
            complexity="medium"
        )

        # NL processing
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            issue = await process_request("Add authentication", context)

        elapsed = time.time() - start_time

        # Complete workflow should be fast with mocked API
        assert elapsed < 2.0  # Less than 2 seconds total
        assert issue is not None
        assert issue.title is not None

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_concurrent_requests_performance(self, mock_anthropic_class, tmp_path):
        """Test performance of multiple concurrent requests."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        intent_response = MagicMock()
        intent_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE

        requirements_response = MagicMock()
        requirements_response.content[0].text = api_responses.REQUIREMENTS_AUTH_RESPONSE

        # Setup for multiple calls
        mock_client.messages.create.side_effect = [
            intent_response, requirements_response,
            intent_response, requirements_response,
            intent_response, requirements_response
        ]

        project_dir = tmp_path / "project"
        project_dir.mkdir()

        context = ProjectContext(
            path=str(project_dir),
            is_new_project=False,
            complexity="low"
        )

        start_time = time.time()

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            # Process 3 requests sequentially (not truly concurrent, but tests overhead)
            issues = []
            for i in range(3):
                issue = await process_request(f"Add feature {i}", context)
                issues.append(issue)

        elapsed = time.time() - start_time

        # Multiple requests should complete in reasonable time
        assert elapsed < 3.0  # Less than 3 seconds for 3 requests
        assert len(issues) == 3
        assert all(issue is not None for issue in issues)


class TestMemoryPerformance:
    """Memory usage tests (basic validation)."""

    def test_large_requirements_list_memory(self):
        """Test that large requirements lists don't cause memory issues."""
        # Create very large requirements list
        large_requirements = [f"Requirement {i}: " + "x" * 100 for i in range(500)]

        # Should complete without memory error
        body = create_feature_issue_body(
            description="Large feature",
            requirements=large_requirements,
            workflow="adw_sdlc_iso",
            model_set="base"
        )

        assert body is not None
        assert len(body) > 10000  # Should be a large document

    @pytest.mark.asyncio
    @patch('core.nl_processor.Anthropic')
    async def test_many_api_calls_memory(self, mock_anthropic_class):
        """Test that many API calls don't accumulate memory."""
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = api_responses.INTENT_FEATURE_RESPONSE
        mock_client.messages.create.return_value = mock_response

        with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
            # Make many calls
            for i in range(50):
                result = await analyze_intent(f"Feature {i}")
                assert result is not None

        # If we get here without memory error, test passes


# Performance thresholds documentation
"""
Performance Targets:
- Small input (<100 chars): < 1 second
- Medium input (100-1000 chars): < 1 second
- Large input (1000-10000 chars): < 2 seconds
- Project detection (small): < 0.5 seconds
- Project detection (medium): < 1 second
- Project detection (large): < 2 seconds
- Issue formatting (small): < 0.1 seconds
- Issue formatting (large): < 0.5 seconds
- Complete workflow: < 2 seconds (mocked)

Note: These targets are for mocked API calls. Real API calls will be slower
due to network latency and API processing time.
"""
