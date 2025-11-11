"""
Workflow monitoring and status routes.

Provides endpoints for listing active ADW workflows and retrieving
detailed workflow status and logs.
"""

import logging

from fastapi import APIRouter, HTTPException, Query, status

from interfaces.web.models import WorkflowListResponse, WorkflowStatusResponse
from interfaces.web.workflow_monitor import get_workflow_monitor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["workflows"])


@router.get(
    "/workflows",
    response_model=WorkflowListResponse,
    summary="List active workflows",
    description="List all active ADW workflow executions",
)
async def list_workflows(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of workflows to return"),
) -> WorkflowListResponse:
    """
    List all active ADW workflows.

    Args:
        limit: Maximum number of workflows to return (1-100)

    Returns:
        WorkflowListResponse with list of workflows

    Raises:
        HTTPException: If workflow listing fails
    """
    try:
        monitor = get_workflow_monitor()
        workflows = monitor.list_active_workflows()

        # Apply limit
        limited_workflows = workflows[:limit]

        logger.info(f"Listed {len(limited_workflows)} workflows")

        return WorkflowListResponse(
            workflows=limited_workflows,
            total_count=len(workflows),
        )

    except Exception as e:
        logger.error(f"Failed to list workflows: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list workflows: {str(e)}",
        )


@router.get(
    "/workflows/{adw_id}",
    response_model=WorkflowStatusResponse,
    summary="Get workflow status",
    description="Get detailed status and logs for a specific workflow",
)
async def get_workflow_status(adw_id: str) -> WorkflowStatusResponse:
    """
    Get detailed status for a specific workflow.

    Args:
        adw_id: Unique ADW identifier

    Returns:
        WorkflowStatusResponse with complete workflow state and logs

    Raises:
        HTTPException: If workflow not found or status retrieval fails
    """
    try:
        monitor = get_workflow_monitor()

        # Get workflow state
        workflow_state = monitor.get_workflow_status(adw_id)
        if not workflow_state:
            logger.warning(f"Workflow not found: {adw_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow not found: {adw_id}",
            )

        # Get logs
        logs = monitor.get_workflow_logs(adw_id)

        # Extract recent activity (last 10 lines from each log)
        recent_activity = []
        for phase, log_content in logs.items():
            lines = log_content.strip().split("\n")
            recent_lines = lines[-10:] if len(lines) > 10 else lines
            for line in recent_lines:
                if line.strip():
                    recent_activity.append(f"[{phase}] {line}")

        logger.info(f"Retrieved status for workflow {adw_id}")

        return WorkflowStatusResponse(
            workflow=workflow_state,
            logs=logs,
            recent_activity=recent_activity[-20:],  # Last 20 activity items
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get workflow status for {adw_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow status: {str(e)}",
        )
