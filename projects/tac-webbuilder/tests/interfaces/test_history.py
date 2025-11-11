"""Tests for CLI history tracking."""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

from interfaces.cli.history import RequestHistory, get_history


@pytest.fixture
def temp_history_file():
    """Create a temporary history file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([], f)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    temp_path.unlink(missing_ok=True)


@pytest.fixture
def history(temp_history_file):
    """Create a RequestHistory instance with temp file."""
    return RequestHistory(history_file=temp_history_file)


class TestHistoryInitialization:
    """Test history initialization."""

    def test_init_creates_file(self):
        """Test that initialization creates history file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_path = Path(tmpdir) / "history.json"
            history = RequestHistory(history_file=history_path)
            assert history_path.exists()

    def test_init_creates_directory(self):
        """Test that initialization creates parent directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_path = Path(tmpdir) / "subdir" / "history.json"
            history = RequestHistory(history_file=history_path)
            assert history_path.parent.exists()
            assert history_path.exists()


class TestAddRequest:
    """Test adding requests to history."""

    def test_add_request_basic(self, history):
        """Test adding a basic request."""
        history.add_request(
            nl_input="Add user authentication",
            issue_number=123,
            project="/path/to/project",
            status="success",
        )

        entries = history.get_all()
        assert len(entries) == 1
        assert entries[0]["nl_input"] == "Add user authentication"
        assert entries[0]["issue_number"] == 123
        assert entries[0]["status"] == "success"

    def test_add_request_with_url(self, history):
        """Test adding request with issue URL."""
        history.add_request(
            nl_input="Fix bug",
            issue_number=456,
            issue_url="https://github.com/owner/repo/issues/456",
            status="success",
        )

        entries = history.get_all()
        assert entries[0]["issue_url"] == "https://github.com/owner/repo/issues/456"

    def test_add_request_with_error(self, history):
        """Test adding request with error."""
        history.add_request(
            nl_input="Invalid request",
            status="error",
            error="API key not found",
        )

        entries = history.get_all()
        assert entries[0]["status"] == "error"
        assert entries[0]["error"] == "API key not found"

    def test_add_multiple_requests(self, history):
        """Test adding multiple requests."""
        history.add_request("Request 1", issue_number=1, status="success")
        history.add_request("Request 2", issue_number=2, status="success")
        history.add_request("Request 3", issue_number=3, status="success")

        entries = history.get_all()
        assert len(entries) == 3
        # Most recent should be first
        assert entries[0]["nl_input"] == "Request 3"
        assert entries[1]["nl_input"] == "Request 2"
        assert entries[2]["nl_input"] == "Request 1"

    def test_add_request_timestamp(self, history):
        """Test that timestamp is added."""
        history.add_request("Test request", status="success")

        entries = history.get_all()
        assert "timestamp" in entries[0]
        # Verify it's a valid ISO timestamp
        datetime.fromisoformat(entries[0]["timestamp"])


class TestGetRecent:
    """Test getting recent requests."""

    def test_get_recent_default_limit(self, history):
        """Test getting recent requests with default limit."""
        # Add 15 requests
        for i in range(15):
            history.add_request(f"Request {i}", issue_number=i, status="success")

        recent = history.get_recent()
        assert len(recent) == 10  # Default limit

    def test_get_recent_custom_limit(self, history):
        """Test getting recent requests with custom limit."""
        # Add 10 requests
        for i in range(10):
            history.add_request(f"Request {i}", status="success")

        recent = history.get_recent(limit=5)
        assert len(recent) == 5

    def test_get_recent_order(self, history):
        """Test that recent requests are in correct order."""
        history.add_request("First", issue_number=1, status="success")
        history.add_request("Second", issue_number=2, status="success")
        history.add_request("Third", issue_number=3, status="success")

        recent = history.get_recent()
        assert recent[0]["nl_input"] == "Third"
        assert recent[1]["nl_input"] == "Second"
        assert recent[2]["nl_input"] == "First"


class TestGetAll:
    """Test getting all history entries."""

    def test_get_all_empty(self, history):
        """Test getting all entries when history is empty."""
        entries = history.get_all()
        assert entries == []

    def test_get_all_with_entries(self, history):
        """Test getting all entries."""
        for i in range(5):
            history.add_request(f"Request {i}", status="success")

        entries = history.get_all()
        assert len(entries) == 5


class TestClear:
    """Test clearing history."""

    def test_clear_history(self, history):
        """Test clearing all history."""
        # Add some entries
        history.add_request("Request 1", status="success")
        history.add_request("Request 2", status="success")

        assert len(history.get_all()) == 2

        # Clear history
        result = history.clear()
        assert result is True
        assert len(history.get_all()) == 0


class TestDisplay:
    """Test displaying history."""

    def test_display_empty(self, history):
        """Test displaying empty history."""
        with patch("interfaces.cli.history.show_info"):
            with patch("builtins.print"):
                history.display()
                # Should not raise any errors

    def test_display_with_entries(self, history):
        """Test displaying history with entries."""
        history.add_request(
            "Add feature",
            issue_number=123,
            project="/project",
            status="success",
        )

        with patch("interfaces.cli.history.print_table"):
            with patch("builtins.print"):
                history.display()
                # Should not raise any errors

    def test_display_with_limit(self, history):
        """Test displaying history with custom limit."""
        # Add multiple entries
        for i in range(15):
            history.add_request(f"Request {i}", status="success")

        with patch("interfaces.cli.history.print_table"):
            with patch("builtins.print"):
                history.display(limit=5)


class TestGetByIssue:
    """Test getting history by issue number."""

    def test_get_by_issue_found(self, history):
        """Test getting entry by issue number."""
        history.add_request("Request 1", issue_number=123, status="success")
        history.add_request("Request 2", issue_number=456, status="success")

        entry = history.get_by_issue(123)
        assert entry is not None
        assert entry["nl_input"] == "Request 1"
        assert entry["issue_number"] == 123

    def test_get_by_issue_not_found(self, history):
        """Test getting non-existent issue."""
        history.add_request("Request", issue_number=123, status="success")

        entry = history.get_by_issue(999)
        assert entry is None


class TestUpdateStatus:
    """Test updating history entry status."""

    def test_update_status_success(self, history):
        """Test updating status successfully."""
        history.add_request("Request", issue_number=123, status="pending")

        result = history.update_status(123, "success")
        assert result is True

        entry = history.get_by_issue(123)
        assert entry["status"] == "success"

    def test_update_status_with_error(self, history):
        """Test updating status with error message."""
        history.add_request("Request", issue_number=123, status="pending")

        result = history.update_status(123, "error", error="API failed")
        assert result is True

        entry = history.get_by_issue(123)
        assert entry["status"] == "error"
        assert entry["error"] == "API failed"

    def test_update_status_not_found(self, history):
        """Test updating non-existent issue."""
        result = history.update_status(999, "success")
        assert result is False

    def test_update_status_adds_timestamp(self, history):
        """Test that update adds updated_at timestamp."""
        history.add_request("Request", issue_number=123, status="pending")

        history.update_status(123, "success")

        entry = history.get_by_issue(123)
        assert "updated_at" in entry


class TestCorruptedHistory:
    """Test handling of corrupted history file."""

    def test_read_corrupted_json(self):
        """Test reading corrupted JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json {{{")
            temp_path = Path(f.name)

        try:
            with patch("interfaces.cli.history.show_error"):
                history = RequestHistory(history_file=temp_path)
                entries = history.get_all()
                assert entries == []
        finally:
            temp_path.unlink(missing_ok=True)

    def test_read_non_list_json(self):
        """Test reading JSON that's not a list."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"not": "a list"}, f)
            temp_path = Path(f.name)

        try:
            history = RequestHistory(history_file=temp_path)
            entries = history.get_all()
            assert entries == []
        finally:
            temp_path.unlink(missing_ok=True)


class TestGetHistoryFunction:
    """Test the get_history convenience function."""

    def test_get_history_singleton(self):
        """Test that get_history returns same instance."""
        history1 = get_history()
        history2 = get_history()
        assert history1 is history2
