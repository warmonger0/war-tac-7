"""
Request history routes.

Provides access to past request history with pagination and filtering.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

from interfaces.web.models import HistoryResponse, RequestHistoryItem

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["history"])

# History file path
_history_file = Path("request_history.json")


def _load_history() -> list[dict]:
    """Load request history from file."""
    if not _history_file.exists():
        return []

    try:
        with open(_history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug(f"Loaded {len(data)} history items")
            return data
    except Exception as e:
        logger.error(f"Failed to load history: {e}")
        return []


def _save_history_item(item: dict):
    """Save a history item to file."""
    try:
        history = _load_history()
        history.append(item)

        # Keep only last 1000 items
        if len(history) > 1000:
            history = history[-1000:]

        with open(_history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, default=str)

        logger.debug(f"Saved history item: {item.get('request_id')}")
    except Exception as e:
        logger.error(f"Failed to save history item: {e}")


@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Get request history",
    description="Retrieve past request history with pagination",
)
async def get_history(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of items to return"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    project: Optional[str] = Query(None, description="Filter by project name"),
) -> HistoryResponse:
    """
    Get request history with pagination.

    Args:
        limit: Maximum number of items to return (1-100)
        offset: Number of items to skip (for pagination)
        project: Optional project name filter

    Returns:
        HistoryResponse with paginated history items

    Raises:
        HTTPException: If history retrieval fails
    """
    try:
        # Load history
        history_data = _load_history()

        # Filter by project if specified
        if project:
            history_data = [
                item for item in history_data
                if item.get("project_name") == project
            ]

        # Sort by created_at (newest first)
        history_data.sort(
            key=lambda x: x.get("created_at", ""),
            reverse=True,
        )

        # Apply pagination
        total_count = len(history_data)
        paginated_data = history_data[offset:offset + limit]
        has_more = (offset + limit) < total_count

        # Convert to response models
        history_items = []
        for item in paginated_data:
            try:
                history_item = RequestHistoryItem(
                    request_id=item.get("request_id", "unknown"),
                    nl_input=item.get("nl_input", ""),
                    project_name=item.get("project_name", "unknown"),
                    issue_number=item.get("issue_number"),
                    github_url=item.get("github_url"),
                    created_at=datetime.fromisoformat(item.get("created_at", datetime.now().isoformat())),
                    status=item.get("status", "unknown"),
                )
                history_items.append(history_item)
            except Exception as e:
                logger.warning(f"Failed to parse history item: {e}")
                continue

        logger.info(f"Retrieved {len(history_items)} history items (offset={offset}, limit={limit})")

        return HistoryResponse(
            history=history_items,
            total_count=total_count,
            has_more=has_more,
        )

    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}",
        )


# Utility function for other modules to add history items
def add_history_item(
    request_id: str,
    nl_input: str,
    project_name: str,
    issue_number: Optional[int] = None,
    github_url: Optional[str] = None,
    status: str = "pending",
):
    """
    Add an item to request history.

    Args:
        request_id: Unique request identifier
        nl_input: Natural language input
        project_name: Project name
        issue_number: GitHub issue number if posted
        github_url: GitHub URL if posted
        status: Request status
    """
    item = {
        "request_id": request_id,
        "nl_input": nl_input,
        "project_name": project_name,
        "issue_number": issue_number,
        "github_url": github_url,
        "created_at": datetime.now().isoformat(),
        "status": status,
    }
    _save_history_item(item)
