"""WebBuilder-specific data models for NL processing and issue generation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime


# GitHub Issue Models
class GitHubIssue(BaseModel):
    """Model representing a GitHub issue to be created."""
    title: str = Field(..., description="Issue title")
    body: str = Field(..., description="Issue body in Markdown format")
    labels: List[str] = Field(default_factory=list, description="Issue labels")
    classification: Literal["feature", "bug", "chore"] = Field(
        ..., description="Issue type classification"
    )
    workflow: str = Field(
        ..., description="ADW workflow (e.g., adw_sdlc_iso, adw_plan_build_test_iso)"
    )
    model_set: Literal["base", "heavy"] = Field(
        default="base", description="Model set for ADW workflow"
    )
    issue_number: Optional[int] = Field(
        None, description="GitHub issue number after creation"
    )


# Project Context Models
class ProjectContext(BaseModel):
    """Model representing the context of a project directory."""
    path: str = Field(..., description="Absolute path to the project")
    is_new_project: bool = Field(
        ..., description="Whether this is a new project or existing codebase"
    )
    framework: Optional[str] = Field(
        None, description="Detected frontend framework (e.g., react-vite, nextjs, vue)"
    )
    backend: Optional[str] = Field(
        None, description="Detected backend framework (e.g., fastapi, express, django)"
    )
    complexity: Literal["low", "medium", "high"] = Field(
        default="medium", description="Estimated project complexity"
    )
    build_tools: List[str] = Field(
        default_factory=list, description="Detected build tools (e.g., npm, yarn, bun)"
    )
    has_git: bool = Field(default=False, description="Whether the project has git initialized")
    detected_files: List[str] = Field(
        default_factory=list, description="Key files detected for context"
    )


# NL Processing Models
class NLProcessingRequest(BaseModel):
    """Request model for natural language processing."""
    nl_input: str = Field(..., description="Natural language input from user")
    project_path: Optional[str] = Field(
        None, description="Optional project path for context detection"
    )
    auto_detect_context: bool = Field(
        default=True, description="Whether to automatically detect project context"
    )
    confirm_before_post: bool = Field(
        default=True, description="Whether to confirm before posting to GitHub"
    )


class NLProcessingResponse(BaseModel):
    """Response model for natural language processing."""
    issue: GitHubIssue = Field(..., description="Generated GitHub issue")
    project_context: Optional[ProjectContext] = Field(
        None, description="Detected project context if applicable"
    )
    confidence_score: float = Field(
        ..., description="Confidence score of the NL processing (0-1)"
    )
    intent_analysis: dict = Field(
        ..., description="Analysis of user intent from NL input"
    )
    requirements: List[str] = Field(
        ..., description="Extracted technical requirements"
    )
    processing_time_ms: float = Field(
        ..., description="Time taken to process the request in milliseconds"
    )
    error: Optional[str] = Field(None, description="Error message if processing failed")


# Intent Analysis Models
class IntentAnalysis(BaseModel):
    """Model for analyzed user intent from natural language."""
    primary_intent: str = Field(..., description="Primary user intent")
    action_type: Literal["create", "modify", "fix", "analyze", "unknown"] = Field(
        ..., description="Type of action requested"
    )
    target_components: List[str] = Field(
        default_factory=list, description="Components or features mentioned"
    )
    technical_keywords: List[str] = Field(
        default_factory=list, description="Technical keywords extracted"
    )
    suggested_issue_type: Literal["feature", "bug", "chore"] = Field(
        ..., description="Suggested issue classification"
    )
    ambiguity_level: Literal["low", "medium", "high"] = Field(
        default="low", description="Level of ambiguity in the request"
    )


# Issue Preview Models
class IssuePreviewRequest(BaseModel):
    """Request model for previewing an issue before posting."""
    issue: GitHubIssue = Field(..., description="Issue to preview")
    format: Literal["markdown", "terminal", "html"] = Field(
        default="terminal", description="Preview format"
    )


class IssuePreviewResponse(BaseModel):
    """Response model for issue preview."""
    formatted_preview: str = Field(..., description="Formatted issue preview")
    estimated_complexity: str = Field(
        ..., description="Estimated implementation complexity"
    )
    suggested_timeline: Optional[str] = Field(
        None, description="Suggested timeline for implementation"
    )


# GitHub Posting Models
class GitHubPostRequest(BaseModel):
    """Request model for posting an issue to GitHub."""
    issue: GitHubIssue = Field(..., description="Issue to post")
    repository: Optional[str] = Field(
        None, description="Repository in format owner/repo (uses current if not specified)"
    )
    dry_run: bool = Field(
        default=False, description="If true, validates but doesn't actually post"
    )


class GitHubPostResponse(BaseModel):
    """Response model for GitHub issue posting."""
    success: bool = Field(..., description="Whether the issue was posted successfully")
    issue_number: Optional[int] = Field(
        None, description="GitHub issue number if successful"
    )
    issue_url: Optional[str] = Field(
        None, description="URL to the created issue"
    )
    error: Optional[str] = Field(None, description="Error message if posting failed")
    posted_at: Optional[datetime] = Field(
        None, description="Timestamp when issue was posted"
    )


# Workflow Suggestion Models
class WorkflowSuggestion(BaseModel):
    """Model for ADW workflow suggestions."""
    workflow_name: str = Field(..., description="Suggested ADW workflow name")
    model_set: Literal["base", "heavy"] = Field(
        ..., description="Suggested model set"
    )
    reasoning: str = Field(
        ..., description="Explanation for why this workflow was suggested"
    )
    alternative_workflows: List[str] = Field(
        default_factory=list, description="Alternative workflow options"
    )
    estimated_tokens: Optional[int] = Field(
        None, description="Estimated token usage for the workflow"
    )


# Error Models
class WebBuilderError(BaseModel):
    """Model for WebBuilder-specific errors."""
    error_type: Literal["nlp_error", "github_error", "context_error", "validation_error"] = Field(
        ..., description="Type of error"
    )
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    suggestion: Optional[str] = Field(
        None, description="Suggestion for resolving the error"
    )
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")