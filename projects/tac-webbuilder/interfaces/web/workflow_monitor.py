"""
ADW workflow monitoring and status tracking.

This module monitors the agents/ directory for active ADW workflows,
reads their state, and provides status information for the web API.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from interfaces.web.models import (
    ADWState,
    WorkflowPhase,
    WorkflowStatus,
    WorkflowSummary,
)

logger = logging.getLogger(__name__)


class WorkflowMonitor:
    """
    Monitors ADW workflow execution in the agents/ directory.

    Reads ADW state files and agent logs to provide status information
    for the web API.
    """

    def __init__(self, agents_dir: Optional[Path] = None):
        """
        Initialize workflow monitor.

        Args:
            agents_dir: Path to agents directory (defaults to ./agents)
        """
        self.agents_dir = agents_dir or Path("agents")
        self._cache: dict[str, tuple[datetime, ADWState]] = {}
        self._cache_ttl_seconds = 5  # Cache for 5 seconds

    def list_active_workflows(self) -> list[WorkflowSummary]:
        """
        List all active ADW workflows.

        Returns:
            List of workflow summaries

        Raises:
            FileNotFoundError: If agents directory doesn't exist
        """
        if not self.agents_dir.exists():
            logger.warning(f"Agents directory not found: {self.agents_dir}")
            return []

        workflows = []

        try:
            # Scan agents directory for workflow directories
            for workflow_dir in self.agents_dir.iterdir():
                if not workflow_dir.is_dir():
                    continue

                try:
                    # Try to read workflow state
                    state = self._read_workflow_state(workflow_dir)
                    if state:
                        summary = WorkflowSummary(
                            adw_id=state.adw_id,
                            issue_number=state.issue_number,
                            current_phase=state.current_phase,
                            status=state.status,
                            started_at=state.started_at,
                            updated_at=state.updated_at,
                            pr_url=state.pr_url,
                        )
                        workflows.append(summary)
                except Exception as e:
                    logger.warning(f"Failed to read workflow {workflow_dir.name}: {e}")
                    continue

            logger.info(f"Found {len(workflows)} active workflows")
            return workflows

        except Exception as e:
            logger.error(f"Failed to list workflows: {e}")
            return []

    def get_workflow_status(self, adw_id: str) -> Optional[ADWState]:
        """
        Get detailed status for a specific workflow.

        Args:
            adw_id: Unique ADW identifier

        Returns:
            ADWState with complete workflow information or None if not found
        """
        # Check cache first
        if adw_id in self._cache:
            cached_time, cached_state = self._cache[adw_id]
            if (datetime.now() - cached_time).total_seconds() < self._cache_ttl_seconds:
                logger.debug(f"Returning cached state for {adw_id}")
                return cached_state

        # Find workflow directory
        workflow_dir = self.agents_dir / adw_id
        if not workflow_dir.exists():
            logger.warning(f"Workflow not found: {adw_id}")
            return None

        try:
            state = self._read_workflow_state(workflow_dir)
            if state:
                # Update cache
                self._cache[adw_id] = (datetime.now(), state)
                logger.info(f"Retrieved status for workflow {adw_id}")
            return state

        except Exception as e:
            logger.error(f"Failed to get workflow status for {adw_id}: {e}")
            return None

    def get_workflow_logs(self, adw_id: str) -> dict[str, str]:
        """
        Get logs for a specific workflow.

        Args:
            adw_id: Unique ADW identifier

        Returns:
            Dictionary mapping phase names to log contents
        """
        workflow_dir = self.agents_dir / adw_id
        if not workflow_dir.exists():
            return {}

        logs = {}

        try:
            # Look for log files in workflow directory
            for log_file in workflow_dir.glob("*.log"):
                phase_name = log_file.stem
                try:
                    with open(log_file, "r", encoding="utf-8") as f:
                        logs[phase_name] = f.read()
                except Exception as e:
                    logger.warning(f"Failed to read log {log_file}: {e}")
                    logs[phase_name] = f"Error reading log: {e}"

            return logs

        except Exception as e:
            logger.error(f"Failed to get logs for {adw_id}: {e}")
            return {}

    def _read_workflow_state(self, workflow_dir: Path) -> Optional[ADWState]:
        """
        Read ADW state from workflow directory.

        Args:
            workflow_dir: Path to workflow directory

        Returns:
            ADWState or None if state file not found or invalid
        """
        # Look for state file (common naming patterns)
        state_file_names = [
            "adw_state.json",
            "state.json",
            "workflow_state.json",
            f"{workflow_dir.name}_state.json",
        ]

        state_file = None
        for name in state_file_names:
            potential_file = workflow_dir / name
            if potential_file.exists():
                state_file = potential_file
                break

        if not state_file:
            # Try to infer state from directory structure
            logger.debug(f"No state file found in {workflow_dir}, creating minimal state")
            return self._create_minimal_state(workflow_dir)

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Parse state data
            return ADWState(
                adw_id=data.get("adw_id", workflow_dir.name),
                issue_number=data.get("issue_number", 0),
                repo_url=data.get("repo_url", ""),
                current_phase=WorkflowPhase(data.get("current_phase", "plan")),
                status=WorkflowStatus(data.get("status", "running")),
                started_at=datetime.fromisoformat(data.get("started_at", datetime.now().isoformat())),
                updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
                completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                pr_number=data.get("pr_number"),
                pr_url=data.get("pr_url"),
                error_message=data.get("error_message"),
                phase_logs=data.get("phase_logs", {}),
            )

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in state file {state_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to parse state file {state_file}: {e}")
            return None

    def _create_minimal_state(self, workflow_dir: Path) -> ADWState:
        """
        Create minimal state from directory structure.

        Args:
            workflow_dir: Path to workflow directory

        Returns:
            ADWState with inferred information
        """
        # Infer state from directory name and modification time
        adw_id = workflow_dir.name
        stat = workflow_dir.stat()
        created_time = datetime.fromtimestamp(stat.st_ctime)
        modified_time = datetime.fromtimestamp(stat.st_mtime)

        # Check for phase markers
        current_phase = WorkflowPhase.PLAN
        if (workflow_dir / "build_complete").exists():
            current_phase = WorkflowPhase.TEST
        if (workflow_dir / "test_complete").exists():
            current_phase = WorkflowPhase.ISOLATE
        if (workflow_dir / "isolate_complete").exists():
            current_phase = WorkflowPhase.SHIP
        if (workflow_dir / "ship_complete").exists():
            current_phase = WorkflowPhase.COMPLETED

        # Determine status
        status = WorkflowStatus.RUNNING
        if (workflow_dir / "error").exists():
            status = WorkflowStatus.FAILED
        elif current_phase == WorkflowPhase.COMPLETED:
            status = WorkflowStatus.COMPLETED

        return ADWState(
            adw_id=adw_id,
            issue_number=0,  # Unknown
            repo_url="",  # Unknown
            current_phase=current_phase,
            status=status,
            started_at=created_time,
            updated_at=modified_time,
            completed_at=modified_time if status == WorkflowStatus.COMPLETED else None,
            pr_number=None,
            pr_url=None,
            error_message=None,
            phase_logs={},
        )


# Global monitor instance
_workflow_monitor: Optional[WorkflowMonitor] = None


def get_workflow_monitor() -> WorkflowMonitor:
    """
    Get or create the global workflow monitor instance.

    Returns:
        WorkflowMonitor singleton instance
    """
    global _workflow_monitor
    if _workflow_monitor is None:
        _workflow_monitor = WorkflowMonitor()
    return _workflow_monitor
