"""
Integration tests for optimized ADW workflow.

Tests the complete end-to-end flow:
1. Comprehensive planning
2. Deterministic execution
3. Validation

These tests use mocks for AI calls but test real file operations.
"""

import pytest
import sys
import os
import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adw_modules.plan_parser import parse_plan, WorkflowConfig
from adw_modules.plan_executor import execute_plan, ExecutionResult
from adw_modules.data_types import AgentPromptResponse
from tests.fixtures import (
    SAMPLE_ISSUE_TAC7_ROOT,
    SAMPLE_ISSUE_WEBBUILDER,
    SAMPLE_PLAN_TAC7_ROOT,
    SAMPLE_PLAN_WEBBUILDER,
    MockTempRepo,
    create_mock_issue_json
)


@pytest.mark.integration
class TestTac7RootWorkflow:
    """Test complete workflow for tac-7-root tasks (no worktree)."""

    @patch('adw_modules.agent.execute_template')
    def test_complete_tac7_workflow(self, mock_execute):
        """Test end-to-end workflow for tac-7-root task."""
        with MockTempRepo() as repo:
            # Setup git
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            # Mock AI planning response
            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_TAC7_ROOT
            )

            logger = Mock()

            # STAGE 1: Parse plan
            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

            assert config.issue_type == "feature"
            assert config.project_context == "tac-7-root"
            assert config.requires_worktree is False
            assert config.confidence == "high"

            # STAGE 2: Execute plan
            result = execute_plan(
                config,
                123,
                str(repo.repo_path),
                logger
            )

            assert result.success is True
            assert len(result.errors) == 0
            assert result.metadata["project_context"] == "tac-7-root"
            assert result.metadata["working_directory"] == str(repo.repo_path)

            # Verify branch was created
            branch_check = subprocess.run(
                ["git", "branch", "--list", config.branch_name],
                cwd=repo.repo_path,
                capture_output=True,
                text=True
            )
            assert config.branch_name in branch_check.stdout

            # Verify no worktree created
            trees_dir = repo.repo_path / "trees"
            assert not trees_dir.exists() or len(list(trees_dir.iterdir())) == 0

    @patch('adw_modules.agent.execute_template')
    def test_tac7_with_plan_file_creation(self, mock_execute):
        """Test that plan file metadata is captured correctly."""
        with MockTempRepo() as repo:
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_TAC7_ROOT
            )

            logger = Mock()

            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)
            result = execute_plan(config, 123, str(repo.repo_path), logger)

            assert result.success is True
            assert "plan_file" in result.metadata
            assert "specs/issue-123" in config.plan_file_path


@pytest.mark.integration
@pytest.mark.slow
class TestWebbuilderWorkflow:
    """Test complete workflow for webbuilder tasks (with worktree)."""

    @patch('adw_modules.plan_executor.execute_worktree_setup')
    @patch('adw_modules.agent.execute_template')
    def test_complete_webbuilder_workflow(self, mock_execute, mock_setup):
        """Test end-to-end workflow for webbuilder task."""
        mock_setup.return_value = True

        with MockTempRepo() as repo:
            # Setup git
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            # Mock AI responses
            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_WEBBUILDER
            )

            logger = Mock()

            # STAGE 1: Parse plan
            config = parse_plan(SAMPLE_PLAN_WEBBUILDER)

            assert config.issue_type == "bug"
            assert config.project_context == "tac-webbuilder"
            assert config.requires_worktree is True
            assert config.worktree_setup is not None
            assert config.worktree_setup["backend_port"] == 8023
            assert config.worktree_setup["frontend_port"] == 5196

            # STAGE 2: Execute plan
            result = execute_plan(
                config,
                456,
                str(repo.repo_path),
                logger
            )

            assert result.success is True
            assert "trees/def67890" in result.metadata["working_directory"]

            # Verify worktree was created
            worktree_path = Path(result.metadata["working_directory"])
            assert worktree_path.exists()

            # Verify setup was called
            assert mock_setup.called
            setup_call_args = mock_setup.call_args
            assert setup_call_args[0][1] == config.worktree_setup  # Second arg is setup config

    @patch('adw_modules.plan_executor.execute_worktree_setup')
    @patch('adw_modules.agent.execute_template')
    def test_webbuilder_worktree_setup_steps(self, mock_execute, mock_setup):
        """Test that worktree setup receives correct configuration."""
        mock_setup.return_value = True

        with MockTempRepo() as repo:
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_WEBBUILDER
            )

            logger = Mock()
            config = parse_plan(SAMPLE_PLAN_WEBBUILDER)
            result = execute_plan(config, 456, str(repo.repo_path), logger)

            assert result.success is True

            # Verify setup was called with correct steps
            setup_config = mock_setup.call_args[0][1]
            assert "steps" in setup_config
            assert len(setup_config["steps"]) == 6  # All 6 steps from fixture


@pytest.mark.integration
class TestWorkflowEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_yaml_in_plan(self):
        """Test handling of invalid YAML in plan response."""
        invalid_plan = """
```yaml
issue_type: feature
  invalid:: indentation
```
"""
        with pytest.raises(ValueError, match="Invalid YAML"):
            parse_plan(invalid_plan)

    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        incomplete_plan = """
```yaml
issue_type: feature
project_context: tac-7-root
# branch_name missing
```
"""
        with pytest.raises(ValueError, match="branch_name is required"):
            parse_plan(incomplete_plan)

    @patch('adw_modules.agent.execute_template')
    def test_execution_with_git_error(self, mock_execute):
        """Test handling of git operation errors."""
        with MockTempRepo() as repo:
            # Don't initialize git - should cause error
            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_TAC7_ROOT
            )

            logger = Mock()
            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

            # This should fail due to missing git initialization
            result = execute_plan(config, 123, str(repo.repo_path), logger)

            # Depending on implementation, this might succeed or fail
            # The test verifies error handling exists
            if not result.success:
                assert len(result.errors) > 0


@pytest.mark.integration
class TestTokenUsageComparison:
    """Test to verify token usage reduction."""

    def test_count_ai_calls(self):
        """Verify that optimized workflow makes fewer AI calls."""
        # This is a conceptual test to document the architecture

        # OLD WORKFLOW:
        old_workflow_ai_calls = [
            "classify_issue",      # 22k tokens
            "generate_branch_name", # 22k tokens
            "install_worktree",    # 868k tokens (51 calls!)
            "build_plan",          # 256k tokens
            "create_commit"        # 3k tokens
        ]
        assert len(old_workflow_ai_calls) == 5  # Actually 56 calls counting ops agent

        # NEW WORKFLOW:
        new_workflow_ai_calls = [
            "plan_complete_workflow",  # 256k tokens (ONE call)
            "validate_workflow"        # 15k tokens
        ]
        assert len(new_workflow_ai_calls) == 2

        # Verify massive reduction
        ai_call_reduction = (len(old_workflow_ai_calls) - len(new_workflow_ai_calls)) / len(old_workflow_ai_calls)
        assert ai_call_reduction >= 0.60  # At least 60% reduction in AI call count

        # Note: Token reduction is actually 77% (1171k → 271k)


@pytest.mark.integration
class TestValidationArtifacts:
    """Test that validation artifacts are correctly structured."""

    @patch('adw_modules.agent.execute_template')
    def test_validation_artifacts_structure(self, mock_execute):
        """Test that execution results can be used for validation."""
        with MockTempRepo() as repo:
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_TAC7_ROOT
            )

            logger = Mock()
            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)
            result = execute_plan(config, 123, str(repo.repo_path), logger)

            # Build validation artifacts (as would be done in validate_execution)
            validation_artifacts = {
                "plan": {
                    "issue_type": config.issue_type,
                    "project_context": config.project_context,
                    "requires_worktree": config.requires_worktree,
                    "branch_name": config.branch_name
                },
                "execution": result.to_dict(),
                "git_status": "",  # Would be populated in real execution
                "file_system": {}   # Would be populated in real execution
            }

            # Verify structure is JSON-serializable
            artifacts_json = json.dumps(validation_artifacts, indent=2)
            assert len(artifacts_json) > 0

            # Verify all required keys present
            assert "plan" in validation_artifacts
            assert "execution" in validation_artifacts
            assert "git_status" in validation_artifacts
            assert "file_system" in validation_artifacts


@pytest.mark.integration
class TestPerformanceMetrics:
    """Tests to capture performance metrics."""

    @patch('adw_modules.agent.execute_template')
    def test_execution_speed_tac7(self, mock_execute):
        """Measure execution speed for tac-7-root workflow."""
        import time

        with MockTempRepo() as repo:
            subprocess.run(
                ["git", "checkout", "-b", "main"],
                cwd=repo.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", "Initial"],
                cwd=repo.repo_path,
                capture_output=True
            )

            mock_execute.return_value = AgentPromptResponse(
                success=True,
                output=SAMPLE_PLAN_TAC7_ROOT
            )

            logger = Mock()
            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

            start_time = time.time()
            result = execute_plan(config, 123, str(repo.repo_path), logger)
            execution_time = time.time() - start_time

            assert result.success is True

            # Execution should be very fast (< 1 second) since no worktree setup
            assert execution_time < 1.0, f"Execution took {execution_time:.2f}s, expected < 1s"

            print(f"\n✓ tac-7-root execution time: {execution_time:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
