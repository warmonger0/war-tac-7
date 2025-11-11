"""
Request submission and management routes.

Handles the preview-before-post workflow for creating GitHub issues from
natural language input.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, status

from interfaces.web.models import (
    ConfirmResponse,
    RequestPreviewResponse,
    SubmitRequestModel,
)
from interfaces.web.state import get_request_state

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["requests"])


@router.post(
    "/request",
    response_model=RequestPreviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new request",
    description="Submit natural language input and get a preview of the generated GitHub issue",
)
async def submit_request(req: SubmitRequestModel) -> RequestPreviewResponse:
    """
    Submit a new NL request and generate issue preview.

    Args:
        req: Request submission data

    Returns:
        RequestPreviewResponse with formatted issue and project context

    Raises:
        HTTPException: If project path is invalid or request creation fails
    """
    try:
        state = get_request_state()

        # If auto_post is True, create and immediately post
        if req.auto_post:
            request_id = state.create_request(req.nl_input, req.project_path)
            try:
                # Auto-confirm and post
                await confirm_and_post(request_id)
            except HTTPException:
                # If posting fails, still return the preview
                pass

        # Create request and get preview
        request_id = state.create_request(req.nl_input, req.project_path)
        preview = state.get_preview(request_id)

        logger.info(f"Created request {request_id}")
        return preview

    except ValueError as e:
        logger.error(f"Invalid request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to create request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create request: {str(e)}",
        )


@router.get(
    "/preview/{request_id}",
    response_model=RequestPreviewResponse,
    summary="Get request preview",
    description="Retrieve the formatted GitHub issue preview for a pending request",
)
async def get_preview(request_id: str) -> RequestPreviewResponse:
    """
    Get formatted issue preview for a request.

    Args:
        request_id: Unique request identifier

    Returns:
        RequestPreviewResponse with GitHub issue and context

    Raises:
        HTTPException: If request_id not found
    """
    try:
        state = get_request_state()
        preview = state.get_preview(request_id)

        logger.info(f"Retrieved preview for request {request_id}")
        return preview

    except KeyError:
        logger.warning(f"Request not found: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request not found: {request_id}",
        )
    except Exception as e:
        logger.error(f"Failed to get preview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get preview: {str(e)}",
        )


@router.post(
    "/confirm/{request_id}",
    response_model=ConfirmResponse,
    summary="Confirm and post issue",
    description="Confirm the request and post the issue to GitHub",
)
async def confirm_and_post(request_id: str) -> ConfirmResponse:
    """
    Confirm request and post issue to GitHub.

    Args:
        request_id: Unique request identifier

    Returns:
        ConfirmResponse with issue number and URL

    Raises:
        HTTPException: If request not found or posting fails
    """
    try:
        state = get_request_state()

        # Post to GitHub
        issue_number, github_url = state.confirm_and_post(request_id)

        logger.info(f"Posted request {request_id} as issue #{issue_number}")

        # TODO: Start ADW workflow if configured
        workflow_info: dict[str, Any] = {
            "workflow_started": False,
            "message": "ADW workflow integration not yet implemented",
        }

        return ConfirmResponse(
            issue_number=issue_number,
            github_url=github_url,
            workflow_info=workflow_info,
        )

    except KeyError:
        logger.warning(f"Request not found: {request_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Request not found: {request_id}",
        )
    except RuntimeError as e:
        logger.error(f"Failed to post to GitHub: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to confirm request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to confirm request: {str(e)}",
        )
