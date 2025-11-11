"""Request history tracking for CLI interface."""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from interfaces.cli.output import (
    create_table,
    print_table,
    show_error,
    show_info,
)


# Default history file path
DEFAULT_HISTORY_PATH = Path.home() / ".webbuilder" / "history.json"


class RequestHistory:
    """Manages request history with JSON-based persistence."""

    def __init__(self, history_file: Optional[Path] = None):
        """
        Initialize the request history manager.

        Args:
            history_file: Path to the history file (default: ~/.webbuilder/history.json)
        """
        self.history_file = history_file or DEFAULT_HISTORY_PATH
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Ensure the history file and its directory exist."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_file.exists():
            self._write_history([])

    def _read_history(self) -> List[Dict[str, Any]]:
        """
        Read history from the JSON file.

        Returns:
            List of history entries
        """
        try:
            with open(self.history_file, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            show_error(f"History file corrupted: {self.history_file}")
            return []
        except Exception as e:
            show_error(f"Error reading history: {e}")
            return []

    def _write_history(self, history: List[Dict[str, Any]]) -> None:
        """
        Write history to the JSON file.

        Args:
            history: List of history entries
        """
        try:
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2, default=str)
        except Exception as e:
            show_error(f"Error writing history: {e}")

    def add_request(
        self,
        nl_input: str,
        issue_number: Optional[int] = None,
        issue_url: Optional[str] = None,
        project: Optional[str] = None,
        status: str = "pending",
        error: Optional[str] = None,
    ) -> None:
        """
        Add a request to the history.

        Args:
            nl_input: Natural language input from the user
            issue_number: GitHub issue number (if created)
            issue_url: GitHub issue URL (if created)
            project: Project path or name
            status: Request status (pending, success, error)
            error: Error message if status is error
        """
        history = self._read_history()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "nl_input": nl_input,
            "issue_number": issue_number,
            "issue_url": issue_url,
            "project": project,
            "status": status,
            "error": error,
        }

        history.insert(0, entry)  # Add to beginning (most recent first)
        self._write_history(history)

    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent requests from history.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of history entries (most recent first)
        """
        history = self._read_history()
        return history[:limit]

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all history entries.

        Returns:
            List of all history entries
        """
        return self._read_history()

    def clear(self) -> bool:
        """
        Clear all history.

        Returns:
            True if successful, False otherwise
        """
        try:
            self._write_history([])
            return True
        except Exception:
            return False

    def display(self, limit: int = 10) -> None:
        """
        Display history in a formatted table.

        Args:
            limit: Maximum number of entries to display
        """
        history = self.get_recent(limit)

        if not history:
            show_info("No history found")
            return

        # Create table with columns
        columns = [
            ("Timestamp", "cyan"),
            ("Request", "white"),
            ("Issue", "green"),
            ("Project", "yellow"),
            ("Status", "magenta"),
        ]

        rows = []
        for entry in history:
            # Format timestamp
            try:
                dt = datetime.fromisoformat(entry["timestamp"])
                timestamp = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                timestamp = entry["timestamp"]

            # Truncate long requests
            request = entry["nl_input"]
            if len(request) > 50:
                request = request[:47] + "..."

            # Format issue number
            issue = f"#{entry['issue_number']}" if entry.get("issue_number") else "-"

            # Truncate project path
            project = entry.get("project") or "-"
            if len(project) > 30:
                project = "..." + project[-27:]

            # Format status with simple indicators
            status = entry.get("status", "unknown")
            if status == "success":
                status = "[+] success"
            elif status == "error":
                status = "[X] error"
            elif status == "pending":
                status = "[?] pending"

            rows.append([timestamp, request, issue, project, status])

        table = create_table(
            title=f"Request History (showing {len(rows)} of {len(self.get_all())})",
            columns=columns,
            rows=rows,
            show_lines=False,
        )

        print_table(table)

        # Show file location
        print(f"\nHistory file: {self.history_file}")

    def get_by_issue(self, issue_number: int) -> Optional[Dict[str, Any]]:
        """
        Get a history entry by issue number.

        Args:
            issue_number: GitHub issue number

        Returns:
            History entry or None if not found
        """
        history = self._read_history()
        for entry in history:
            if entry.get("issue_number") == issue_number:
                return entry
        return None

    def update_status(
        self,
        issue_number: int,
        status: str,
        error: Optional[str] = None,
    ) -> bool:
        """
        Update the status of a history entry.

        Args:
            issue_number: GitHub issue number
            status: New status
            error: Error message if status is error

        Returns:
            True if successful, False otherwise
        """
        history = self._read_history()

        for entry in history:
            if entry.get("issue_number") == issue_number:
                entry["status"] = status
                if error:
                    entry["error"] = error
                entry["updated_at"] = datetime.now().isoformat()
                self._write_history(history)
                return True

        return False


# Convenience function for getting the default history instance
_default_history: Optional[RequestHistory] = None


def get_history() -> RequestHistory:
    """
    Get the default history instance.

    Returns:
        RequestHistory instance
    """
    global _default_history
    if _default_history is None:
        _default_history = RequestHistory()
    return _default_history
