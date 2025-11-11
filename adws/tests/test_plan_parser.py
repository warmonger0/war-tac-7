"""
Unit tests for plan_parser module.

Tests YAML extraction, parsing, and validation.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adw_modules.plan_parser import (
    extract_yaml_block,
    extract_plan_file_path,
    parse_plan,
    validate_workflow_config,
    WorkflowConfig
)


class TestYAMLExtraction:
    """Test YAML block extraction from AI responses."""

    def test_extract_yaml_with_fence(self):
        """Test extracting YAML from code fence."""
        text = """
Here's the plan:

```yaml
issue_type: feature
branch_name: feat-issue-123-adw-abc12345-test
```

More text...
"""
        yaml_text = extract_yaml_block(text)
        assert yaml_text is not None
        assert "issue_type: feature" in yaml_text
        assert "branch_name:" in yaml_text

    def test_extract_yaml_with_header(self):
        """Test extracting YAML with WORKFLOW CONFIGURATION header."""
        text = """
# WORKFLOW CONFIGURATION

issue_type: bug
branch_name: fix-issue-456-adw-def67890-patch

# Implementation Plan
More content...
"""
        yaml_text = extract_yaml_block(text)
        assert yaml_text is not None
        assert "issue_type: bug" in yaml_text

    def test_extract_yaml_missing(self):
        """Test when no YAML block present."""
        text = "Just some regular text without YAML"
        yaml_text = extract_yaml_block(text)
        assert yaml_text is None


class TestPlanFilePathExtraction:
    """Test plan file path extraction."""

    def test_extract_with_plan_file_marker(self):
        """Test extraction with 'Plan file:' marker."""
        text = """
Plan created successfully!

Plan file: specs/issue-123-adw-abc12345-sdlc_planner-add-feature.md
"""
        path = extract_plan_file_path(text)
        assert path == "specs/issue-123-adw-abc12345-sdlc_planner-add-feature.md"

    def test_extract_with_backticks(self):
        """Test extraction with backticks."""
        text = """
Plan file: `specs/issue-456-adw-def67890-sdlc_planner-fix-bug.md`
"""
        path = extract_plan_file_path(text)
        assert path == "specs/issue-456-adw-def67890-sdlc_planner-fix-bug.md"

    def test_extract_direct_match(self):
        """Test direct pattern match."""
        text = """
Created specs/issue-789-adw-ghi01234-sdlc_planner-update-docs.md
"""
        path = extract_plan_file_path(text)
        assert "specs/issue-789-adw-ghi01234-sdlc_planner-update-docs.md" in path

    def test_extract_missing(self):
        """Test when no path present."""
        text = "No plan file mentioned here"
        path = extract_plan_file_path(text)
        assert path is None


class TestPlanParsing:
    """Test complete plan parsing."""

    def test_parse_minimal_plan(self):
        """Test parsing minimal valid plan."""
        plan_text = """
```yaml
issue_type: feature
project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Test reasoning"
branch_name: feat-issue-123-adw-abc12345-test-feature
commit_message: "test: add feature"
validation_criteria:
  - check: "Branch created"
    expected: "feat-issue-123-adw-abc12345-test-feature"
```

# Feature: Test Feature

Implementation details...

Plan file: specs/issue-123-adw-abc12345-sdlc_planner-test-feature.md
"""
        config = parse_plan(plan_text)

        assert config.issue_type == "feature"
        assert config.project_context == "tac-7-root"
        assert config.requires_worktree is False
        assert config.confidence == "high"
        assert config.branch_name == "feat-issue-123-adw-abc12345-test-feature"
        assert config.commit_message == "test: add feature"
        assert len(config.validation_criteria) == 1
        assert config.plan_file_path == "specs/issue-123-adw-abc12345-sdlc_planner-test-feature.md"

    def test_parse_with_worktree_setup(self):
        """Test parsing plan with worktree configuration."""
        plan_text = """
```yaml
issue_type: bug
project_context: tac-webbuilder
requires_worktree: true
confidence: high
detection_reasoning: "Webbuilder task"
branch_name: fix-issue-456-adw-def67890-patch-error
worktree_setup:
  backend_port: 8001
  frontend_port: 5174
  steps:
    - action: create_ports_env
      description: "Create port config"
    - action: install_backend
      command: "cd app/server && uv sync"
```

Plan file: specs/issue-456-adw-def67890-sdlc_planner-patch-error.md
"""
        config = parse_plan(plan_text)

        assert config.issue_type == "bug"
        assert config.requires_worktree is True
        assert config.worktree_setup is not None
        assert config.worktree_setup['backend_port'] == 8001
        assert config.worktree_setup['frontend_port'] == 5174
        assert len(config.worktree_setup['steps']) == 2

    def test_parse_missing_yaml(self):
        """Test error when YAML block missing."""
        plan_text = "Just markdown content without YAML"

        with pytest.raises(ValueError, match="No YAML configuration block found"):
            parse_plan(plan_text)

    def test_parse_invalid_yaml(self):
        """Test error with invalid YAML syntax."""
        plan_text = """
```yaml
issue_type: feature
  invalid indentation:
branch_name: test
```
"""
        with pytest.raises(ValueError, match="Invalid YAML syntax"):
            parse_plan(plan_text)

    def test_parse_missing_required_field(self):
        """Test error when required field missing."""
        plan_text = """
```yaml
issue_type: feature
project_context: tac-7-root
requires_worktree: false
confidence: high
detection_reasoning: "Test"
# branch_name is missing!
```
"""
        with pytest.raises(ValueError, match="branch_name is required"):
            parse_plan(plan_text)


class TestWorkflowConfigValidation:
    """Test workflow configuration validation."""

    def test_validate_valid_config(self):
        """Test validation passes for valid config."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="tac-7-root",
            requires_worktree=False,
            confidence="high",
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test"
        )

        errors = validate_workflow_config(config)
        assert len(errors) == 0

    def test_validate_invalid_issue_type(self):
        """Test validation fails for invalid issue type."""
        config = WorkflowConfig(
            issue_type="invalid",
            project_context="tac-7-root",
            requires_worktree=False,
            confidence="high",
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test"
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("Invalid issue_type" in e for e in errors)

    def test_validate_invalid_project_context(self):
        """Test validation fails for invalid project context."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="invalid-context",
            requires_worktree=False,
            confidence="high",
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test"
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("Invalid project_context" in e for e in errors)

    def test_validate_invalid_confidence(self):
        """Test validation fails for invalid confidence level."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="tac-7-root",
            requires_worktree=False,
            confidence="very-high",  # Invalid
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test"
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("Invalid confidence" in e for e in errors)

    def test_validate_invalid_branch_name_format(self):
        """Test validation fails for wrong branch name format."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="tac-7-root",
            requires_worktree=False,
            confidence="high",
            detection_reasoning="Test",
            branch_name="invalid-branch-name"  # Wrong format
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("Invalid branch_name format" in e for e in errors)

    def test_validate_worktree_required_but_no_setup(self):
        """Test validation fails when worktree required but setup missing."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="tac-webbuilder",
            requires_worktree=True,
            confidence="high",
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test",
            worktree_setup=None  # Missing!
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("worktree_setup is missing" in e for e in errors)

    def test_validate_worktree_setup_missing_ports(self):
        """Test validation fails when worktree setup missing ports."""
        config = WorkflowConfig(
            issue_type="feature",
            project_context="tac-webbuilder",
            requires_worktree=True,
            confidence="high",
            detection_reasoning="Test",
            branch_name="feat-issue-123-adw-abc12345-test",
            worktree_setup={
                "steps": []
                # Missing backend_port and frontend_port
            }
        )

        errors = validate_workflow_config(config)
        assert len(errors) > 0
        assert any("backend_port" in e for e in errors)
        assert any("frontend_port" in e for e in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
