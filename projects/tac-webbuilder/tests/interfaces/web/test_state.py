"""Tests for request state management."""

import pytest
from pathlib import Path

from interfaces.web.state import RequestState


@pytest.fixture
def state():
    """Create a fresh RequestState instance for each test."""
    return RequestState()


def test_create_request(state, tmp_path):
    """Test creating a new request."""
    # Use a temporary directory as the project path
    request_id = state.create_request("Add a new feature", str(tmp_path))

    assert request_id is not None
    assert request_id in state.pending_requests

    request = state.get_request(request_id)
    assert request is not None
    assert request["nl_input"] == "Add a new feature"
    assert request["status"] == "pending"


def test_get_preview(state, tmp_path):
    """Test getting a request preview."""
    request_id = state.create_request("Add a new feature", str(tmp_path))
    preview = state.get_preview(request_id)

    assert preview is not None
    assert preview.request_id == request_id
    assert preview.github_issue is not None
    assert preview.project_context is not None


def test_get_preview_nonexistent(state):
    """Test getting preview for non-existent request raises KeyError."""
    with pytest.raises(KeyError):
        state.get_preview("nonexistent-id")


def test_invalid_project_path(state):
    """Test that invalid project path raises ValueError."""
    with pytest.raises(ValueError, match="does not exist"):
        state.create_request("Test", "/nonexistent/path")


def test_cleanup_old_requests(state, tmp_path):
    """Test cleaning up old requests."""
    from datetime import datetime, timedelta

    # Create a request
    request_id = state.create_request("Test", str(tmp_path))

    # Manually set created_at to old time
    state.pending_requests[request_id]["created_at"] = datetime.now() - timedelta(hours=25)

    # Cleanup
    state.cleanup_old_requests(max_age_hours=24)

    # Request should be removed
    assert request_id not in state.pending_requests
