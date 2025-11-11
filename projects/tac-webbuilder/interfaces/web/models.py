"""
Pydantic models for the tac-webbuilder web API.

This module defines request and response models for all API endpoints,
providing validation, serialization, and documentation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ===== Core Data Models =====


class GitHubIssue(BaseModel):
    """Formatted GitHub issue ready for posting."""

    title: str = Field(..., description="Issue title")
    body: str = Field(..., description="Issue body in markdown format")
    labels: list[str] = Field(default_factory=list, description="Issue labels")
    assignees: list[str] = Field(default_factory=list, description="Issue assignees")
    milestone: Optional[str] = Field(None, description="Milestone name")


class ProjectContext(BaseModel):
    """Detected project context and metadata."""

    project_path: str = Field(..., description="Absolute path to project")
    project_name: str = Field(..., description="Project name")
    framework: Optional[str] = Field(None, description="Detected framework (e.g., React, FastAPI)")
    language: Optional[str] = Field(None, description="Primary programming language")
    tech_stack: list[str] = Field(default_factory=list, description="Detected technologies")
    build_tools: list[str] = Field(default_factory=list, description="Build tools (e.g., npm, uv)")
    test_frameworks: list[str] = Field(default_factory=list, description="Test frameworks")
    has_git: bool = Field(False, description="Whether project has Git repository")
    repo_url: Optional[str] = Field(None, description="Git repository URL if available")


class WorkflowPhase(str, Enum):
    """ADW workflow execution phases."""

    PLAN = "plan"
    BUILD = "build"
    TEST = "test"
    ISOLATE = "isolate"
    SHIP = "ship"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowStatus(str, Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ADWState(BaseModel):
    """ADW workflow state."""

    adw_id: str = Field(..., description="Unique ADW identifier")
    issue_number: int = Field(..., description="GitHub issue number")
    repo_url: str = Field(..., description="Repository URL")
    current_phase: WorkflowPhase = Field(..., description="Current execution phase")
    status: WorkflowStatus = Field(..., description="Overall workflow status")
    started_at: datetime = Field(..., description="Workflow start time")
    updated_at: datetime = Field(..., description="Last update time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    pr_number: Optional[int] = Field(None, description="Pull request number if created")
    pr_url: Optional[str] = Field(None, description="Pull request URL if created")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    phase_logs: dict[str, str] = Field(default_factory=dict, description="Logs per phase")


# ===== Request Models =====


class SubmitRequestModel(BaseModel):
    """Request body for submitting a new NL request."""

    nl_input: str = Field(..., description="Natural language description of the request", min_length=10)
    project_path: Optional[str] = Field(None, description="Path to project (uses current if not specified)")
    auto_post: bool = Field(False, description="Automatically post to GitHub without preview")


class AddProjectModel(BaseModel):
    """Request body for adding a new project."""

    project_path: str = Field(..., description="Absolute path to the project directory")


class SelectOptionModel(BaseModel):
    """Model for selecting an option from a list."""

    option_index: int = Field(..., description="Index of the selected option", ge=0)


# ===== Response Models =====


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field("ok", description="Service status")
    version: str = Field("1.0.0", description="API version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Current server time")


class RequestPreviewResponse(BaseModel):
    """Response for request preview endpoint."""

    request_id: str = Field(..., description="Unique request identifier")
    github_issue: GitHubIssue = Field(..., description="Formatted GitHub issue")
    project_context: ProjectContext = Field(..., description="Detected project context")
    created_at: datetime = Field(default_factory=datetime.now, description="Preview creation time")


class ConfirmResponse(BaseModel):
    """Response after confirming and posting an issue."""

    issue_number: int = Field(..., description="GitHub issue number")
    github_url: str = Field(..., description="URL to the created issue")
    workflow_info: Optional[dict[str, Any]] = Field(None, description="ADW workflow information if started")


class WorkflowSummary(BaseModel):
    """Summary information for a workflow."""

    adw_id: str = Field(..., description="Unique ADW identifier")
    issue_number: int = Field(..., description="GitHub issue number")
    current_phase: WorkflowPhase = Field(..., description="Current phase")
    status: WorkflowStatus = Field(..., description="Overall status")
    started_at: datetime = Field(..., description="Start time")
    updated_at: datetime = Field(..., description="Last update time")
    pr_url: Optional[str] = Field(None, description="Pull request URL if available")


class WorkflowListResponse(BaseModel):
    """Response for listing workflows."""

    workflows: list[WorkflowSummary] = Field(..., description="List of active workflows")
    total_count: int = Field(..., description="Total number of workflows")


class WorkflowStatusResponse(BaseModel):
    """Detailed workflow status response."""

    workflow: ADWState = Field(..., description="Complete workflow state")
    logs: dict[str, str] = Field(default_factory=dict, description="Phase-specific logs")
    recent_activity: list[str] = Field(default_factory=list, description="Recent log entries")


class ProjectSummary(BaseModel):
    """Summary information for a project."""

    project_id: str = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Project name")
    project_path: str = Field(..., description="Project path")
    framework: Optional[str] = Field(None, description="Detected framework")
    language: Optional[str] = Field(None, description="Primary language")
    last_used: Optional[datetime] = Field(None, description="Last time project was used")


class ProjectListResponse(BaseModel):
    """Response for listing projects."""

    projects: list[ProjectSummary] = Field(..., description="List of configured projects")
    total_count: int = Field(..., description="Total number of projects")


class RequestHistoryItem(BaseModel):
    """Single item in request history."""

    request_id: str = Field(..., description="Request identifier")
    nl_input: str = Field(..., description="Original natural language input")
    project_name: str = Field(..., description="Project name")
    issue_number: Optional[int] = Field(None, description="GitHub issue number if posted")
    github_url: Optional[str] = Field(None, description="GitHub URL if posted")
    created_at: datetime = Field(..., description="Request creation time")
    status: str = Field(..., description="Request status (pending, posted, cancelled)")


class HistoryResponse(BaseModel):
    """Response for request history."""

    history: list[RequestHistoryItem] = Field(..., description="List of past requests")
    total_count: int = Field(..., description="Total number of items")
    has_more: bool = Field(False, description="Whether more items are available")


# ===== WebSocket Messages =====


class WebSocketMessageType(str, Enum):
    """WebSocket message types."""

    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_PROGRESS = "workflow_progress"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    ERROR = "error"


class WebSocketMessage(BaseModel):
    """WebSocket message format."""

    type: WebSocketMessageType = Field(..., description="Message type")
    data: dict[str, Any] = Field(..., description="Message payload")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


# ===== Error Models =====


class ErrorDetail(BaseModel):
    """Error detail information."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict[str, Any]] = Field(None, description="Additional error details")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: ErrorDetail = Field(..., description="Error information")
    request_id: Optional[str] = Field(None, description="Request ID if available")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
