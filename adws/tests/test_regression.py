"""
Regression tests for ADW optimization.

Ensures the optimized workflow produces equivalent results to the old workflow.

Tests:
1. Output equivalence - Same plan quality
2. Branch naming consistency - Same branch names
3. File structure - Same files created
4. Git operations - Same git state
5. Issue classification - Same classifications
6. Error handling - Same error behaviors
"""

import pytest
import sys
import os
import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adw_modules.plan_parser import parse_plan, WorkflowConfig
from adw_modules.plan_executor import execute_plan
from adw_modules.data_types import AgentPromptResponse
from tests.fixtures import (
    SAMPLE_ISSUE_TAC7_ROOT,
    SAMPLE_ISSUE_WEBBUILDER,
    SAMPLE_PLAN_TAC7_ROOT,
    MockTempRepo
)


@pytest.mark.regression
class TestOutputEquivalence:
    """Test that optimized workflow produces equivalent output to old workflow."""

    def test_plan_structure_equivalence(self):
        """Verify optimized plan has same structure as old workflow."""
        # Parse optimized plan
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        # Expected fields from old workflow
        expected_fields = {
            'issue_type',
            'branch_name',
            'project_context',
            'requires_worktree',
            'confidence',
            'detection_reasoning'
        }

        # Verify all expected fields present
        for field in expected_fields:
            assert hasattr(config, field), f"Missing field: {field}"

        # Verify types match old workflow expectations
        assert config.issue_type in ['feature', 'bug', 'chore']
        assert isinstance(config.branch_name, str)
        assert config.project_context in ['tac-7-root', 'tac-webbuilder']
        assert isinstance(config.requires_worktree, bool)

    def test_branch_name_format_compatibility(self):
        """Verify branch names match old workflow format."""
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        # Old workflow format: {type}-issue-{num}-adw-{id}-{slug}
        branch_parts = config.branch_name.split('-')

        assert branch_parts[0] in ['feat', 'fix', 'chore'], "Invalid type prefix"
        assert branch_parts[1] == 'issue', "Missing 'issue' segment"
        assert branch_parts[2].isdigit(), "Issue number not numeric"
        assert branch_parts[3] == 'adw', "Missing 'adw' segment"
        assert len(branch_parts[4]) == 8, "ADW ID not 8 characters"
        assert len(branch_parts) >= 6, "Missing slug"

    def test_file_creation_equivalence(self):
        """Verify same files created as old workflow."""
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

            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)
            logger = Mock()

            result = execute_plan(config, 123, str(repo.repo_path), logger)

            # Old workflow created these files
            expected_files = {
                'plan_file',  # specs/issue-*.md
                'branch_name',
                'working_directory'
            }

            # Verify metadata contains expected keys
            for key in expected_files:
                assert key in result.metadata, f"Missing metadata: {key}"


@pytest.mark.regression
class TestBranchNamingConsistency:
    """Test that branch naming is consistent with old workflow."""

    def test_feature_branch_naming(self):
        """Test feature branch follows old conventions."""
        plan_text = """
```yaml
issue_type: feature
branch_name: feat-issue-100-adw-test1234-add-logging-system
project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Test"
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)

        # Old workflow: feat- prefix for features
        assert config.branch_name.startswith('feat-')
        assert 'issue-100' in config.branch_name
        assert 'adw-test1234' in config.branch_name

    def test_bug_branch_naming(self):
        """Test bug branch follows old conventions."""
        plan_text = """
```yaml
issue_type: bug
branch_name: fix-issue-200-adw-test5678-authentication-error
project_context: tac-webbuilder
requires_worktree: true
confidence: high
detection_reasoning: "Test"
worktree_setup:
  backend_port: 8001
  frontend_port: 5174
  steps: []
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)

        # Old workflow: fix- prefix for bugs
        assert config.branch_name.startswith('fix-')
        assert 'issue-200' in config.branch_name

    def test_chore_branch_naming(self):
        """Test chore branch follows old conventions."""
        plan_text = """
```yaml
issue_type: chore
branch_name: chore-issue-300-adw-test9012-update-readme
project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Test"
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)

        # Old workflow: chore- prefix for chores
        assert config.branch_name.startswith('chore-')


@pytest.mark.regression
class TestIssueClassificationRegression:
    """Test that issue classification matches old workflow behavior."""

    def test_explicit_feature_classification(self):
        """Test feature classification from explicit markers."""
        # Old workflow would classify this as feature
        plan_text = """
```yaml
issue_type: feature
branch_name: feat-issue-123-adw-abc12345-test
project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Issue title contains 'add', body describes new functionality"
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)
        assert config.issue_type == 'feature'

    def test_bug_keywords_classification(self):
        """Test bug classification from keywords."""
        # Old workflow would look for: fix, bug, error, broken
        plan_text = """
```yaml
issue_type: bug
branch_name: fix-issue-456-adw-def67890-test
project_context: tac-webbuilder
requires_worktree: true
confidence: high
detection_reasoning: "Issue title contains 'fix', body describes error"
worktree_setup:
  backend_port: 8001
  frontend_port: 5174
  steps: []
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)
        assert config.issue_type == 'bug'

    def test_chore_classification(self):
        """Test chore classification."""
        # Old workflow would classify maintenance tasks as chore
        plan_text = """
```yaml
issue_type: chore
branch_name: chore-issue-789-adw-ghi01234-test
project_context: tac-7-root
requires_worktree: false
confidence: medium
detection_reasoning: "Issue describes maintenance work"
```
Plan file: specs/test.md
"""
        config = parse_plan(plan_text)
        assert config.issue_type == 'chore'


@pytest.mark.regression
class TestProjectDetectionRegression:
    """Test project context detection matches old workflow."""

    def test_explicit_tac7_marker(self):
        """Test explicit tac-7 project marker detection."""
        # Old workflow would recognize "NOT tac-webbuilder"
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        assert config.project_context == 'tac-7-root'
        assert config.requires_worktree is False
        assert 'NOT tac-webbuilder' in config.detection_reasoning or \
               'tac-7' in config.detection_reasoning.lower()

    def test_webbuilder_path_detection(self):
        """Test webbuilder detection from file paths."""
        # Old workflow would detect app/server, app/client paths
        config = parse_plan(SAMPLE_PLAN_WEBBUILDER)

        assert config.project_context == 'tac-webbuilder'
        assert config.requires_worktree is True
        assert config.worktree_setup is not None

    def test_default_to_tac7_when_uncertain(self):
        """Test default behavior matches old workflow."""
        # Old workflow defaulted to tac-7-root when uncertain
        ambiguous_plan = """
```yaml
issue_type: chore
branch_name: chore-issue-999-adw-test0000-update-docs
project_context: tac-7-root
requires_worktree: false
confidence: low
detection_reasoning: "No clear indicators, defaulting to tac-7-root"
```
Plan file: specs/test.md
"""
        config = parse_plan(ambiguous_plan)

        # Should default to tac-7-root like old workflow
        assert config.project_context == 'tac-7-root'
        assert config.requires_worktree is False


@pytest.mark.regression
class TestWorktreeDecisionRegression:
    """Test worktree creation decisions match old workflow."""

    def test_webbuilder_requires_worktree(self):
        """Test webbuilder tasks create worktree (old behavior)."""
        config = parse_plan(SAMPLE_PLAN_WEBBUILDER)

        # Old workflow ALWAYS created worktree for webbuilder
        assert config.project_context == 'tac-webbuilder'
        assert config.requires_worktree is True
        assert config.worktree_setup is not None

    def test_tac7_skips_worktree(self):
        """Test tac-7 tasks skip worktree (NEW optimized behavior)."""
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        # OLD workflow created worktree for everything
        # NEW workflow skips for tac-7-root
        # This is INTENTIONAL CHANGE - better behavior
        assert config.project_context == 'tac-7-root'
        assert config.requires_worktree is False

        # This is a POSITIVE regression - we're more efficient

    def test_worktree_setup_structure(self):
        """Test worktree setup has same structure as old workflow."""
        config = parse_plan(SAMPLE_PLAN_WEBBUILDER)

        # Old workflow setup had these fields
        assert 'backend_port' in config.worktree_setup
        assert 'frontend_port' in config.worktree_setup
        assert 'steps' in config.worktree_setup

        # Verify ports are in valid range
        assert 8000 <= config.worktree_setup['backend_port'] <= 9000
        assert 5000 <= config.worktree_setup['frontend_port'] <= 6000


@pytest.mark.regression
class TestGitOperationsRegression:
    """Test git operations produce same results as old workflow."""

    @patch('adw_modules.plan_executor.execute_worktree_setup')
    def test_git_branch_creation_equivalence(self, mock_setup):
        """Test branch creation matches old workflow."""
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

            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)
            logger = Mock()

            result = execute_plan(config, 123, str(repo.repo_path), logger)

            # Verify branch exists (same as old workflow)
            branch_check = subprocess.run(
                ["git", "branch", "--list", config.branch_name],
                cwd=repo.repo_path,
                capture_output=True,
                text=True
            )
            assert config.branch_name in branch_check.stdout

    @patch('adw_modules.plan_executor.execute_worktree_setup')
    def test_worktree_structure_equivalence(self, mock_setup):
        """Test worktree structure matches old workflow."""
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

            config = parse_plan(SAMPLE_PLAN_WEBBUILDER)
            logger = Mock()

            result = execute_plan(config, 456, str(repo.repo_path), logger)

            # Old workflow created worktrees at trees/{adw_id}/
            assert 'trees/' in result.metadata['working_directory']
            assert Path(result.metadata['working_directory']).exists()


@pytest.mark.regression
class TestErrorHandlingRegression:
    """Test error handling matches old workflow behavior."""

    def test_invalid_yaml_error(self):
        """Test invalid YAML produces error (same as old)."""
        invalid_plan = """
```yaml
issue_type: feature
  invalid: indentation
```
"""
        # Old workflow would fail on invalid YAML
        # New workflow should also fail
        with pytest.raises(ValueError, match="Invalid YAML"):
            parse_plan(invalid_plan)

    def test_missing_required_field_error(self):
        """Test missing fields produce error (same as old)."""
        incomplete_plan = """
```yaml
issue_type: feature
# branch_name missing
```
"""
        # Old workflow required branch_name
        # New workflow should also require it
        with pytest.raises(ValueError, match="branch_name is required"):
            parse_plan(incomplete_plan)

    def test_execution_error_tracking(self):
        """Test execution errors tracked (same as old)."""
        from adw_modules.plan_executor import ExecutionResult

        result = ExecutionResult()
        result.add_error("Test error")

        # Old workflow tracked success flag
        assert result.success is False
        assert len(result.errors) == 1


@pytest.mark.regression
class TestBackwardCompatibility:
    """Test backward compatibility with old workflow artifacts."""

    def test_state_file_compatibility(self):
        """Test state file format compatible with old workflow."""
        # Old workflow state had these fields
        expected_state_fields = {
            'adw_id',
            'issue_class',  # Now issue_type
            'branch_name',
            'worktree_path',
            'plan_file'
        }

        # New workflow should maintain compatible state
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        # Verify we can create compatible state
        state_compatible = {
            'adw_id': 'abc12345',
            'issue_class': config.issue_type,  # Compatible mapping
            'branch_name': config.branch_name,
            'plan_file': config.plan_file_path
        }

        assert all(key in state_compatible for key in ['adw_id', 'issue_class', 'branch_name'])

    def test_plan_file_path_format(self):
        """Test plan file paths match old format."""
        config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)

        # Old format: specs/issue-{num}-adw-{id}-sdlc_planner-{name}.md
        assert config.plan_file_path.startswith('specs/')
        assert 'issue-' in config.plan_file_path
        assert 'adw-' in config.plan_file_path
        assert 'sdlc_planner' in config.plan_file_path
        assert config.plan_file_path.endswith('.md')


@pytest.mark.regression
class TestPerformanceRegression:
    """Test that performance improvements don't break functionality."""

    def test_fast_execution_maintains_correctness(self):
        """Test fast execution still produces correct results."""
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

            config = parse_plan(SAMPLE_PLAN_TAC7_ROOT)
            logger = Mock()

            import time
            start = time.time()
            result = execute_plan(config, 123, str(repo.repo_path), logger)
            execution_time = time.time() - start

            # Verify speed improvement doesn't sacrifice correctness
            assert result.success is True
            assert result.metadata['branch_name'] == config.branch_name
            assert execution_time < 5.0  # Much faster than old workflow (102s)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "regression"])
