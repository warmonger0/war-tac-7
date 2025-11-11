"""
WebSocket connection management for real-time updates.

Manages WebSocket connections and broadcasts workflow updates to connected
clients in real-time.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Optional

from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from interfaces.web.models import WebSocketMessage, WebSocketMessageType

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections and message broadcasting.

    Handles client connections, disconnections, and broadcasting messages
    to all connected clients.
    """

    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: list[WebSocket] = []
        self._lock = asyncio.Lock()
        logger.info("ConnectionManager initialized")

    async def connect(self, websocket: WebSocket):
        """
        Accept and register a new WebSocket connection.

        Args:
            websocket: WebSocket connection to register
        """
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection (total: {len(self.active_connections)})")

    async def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.

        Args:
            websocket: WebSocket connection to remove
        """
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected (remaining: {len(self.active_connections)})")

    async def send_to_client(self, websocket: WebSocket, message: dict):
        """
        Send message to a specific client.

        Args:
            websocket: Target WebSocket connection
            message: Message dictionary to send
        """
        try:
            if websocket.client_state == WebSocketState.CONNECTED:
                await websocket.send_json(message)
                logger.debug(f"Sent message to client: {message.get('type')}")
        except Exception as e:
            logger.error(f"Failed to send message to client: {e}")
            await self.disconnect(websocket)

    async def broadcast(self, message: dict):
        """
        Broadcast message to all connected clients.

        Args:
            message: Message dictionary to broadcast
        """
        async with self._lock:
            connections = self.active_connections.copy()

        if not connections:
            logger.debug("No active connections to broadcast to")
            return

        logger.info(f"Broadcasting message to {len(connections)} clients: {message.get('type')}")

        disconnected = []
        for connection in connections:
            try:
                if connection.client_state == WebSocketState.CONNECTED:
                    await connection.send_json(message)
                else:
                    disconnected.append(connection)
            except Exception as e:
                logger.error(f"Failed to broadcast to client: {e}")
                disconnected.append(connection)

        # Clean up disconnected clients
        if disconnected:
            async with self._lock:
                for conn in disconnected:
                    if conn in self.active_connections:
                        self.active_connections.remove(conn)
            logger.info(f"Removed {len(disconnected)} disconnected clients")

    async def broadcast_workflow_started(
        self,
        adw_id: str,
        issue_number: int,
        repo_url: str,
    ):
        """
        Broadcast workflow started event.

        Args:
            adw_id: Workflow identifier
            issue_number: GitHub issue number
            repo_url: Repository URL
        """
        message = WebSocketMessage(
            type=WebSocketMessageType.WORKFLOW_STARTED,
            data={
                "adw_id": adw_id,
                "issue_number": issue_number,
                "repo_url": repo_url,
            },
            timestamp=datetime.now(),
        )
        await self.broadcast(message.model_dump(mode="json"))

    async def broadcast_workflow_progress(
        self,
        adw_id: str,
        phase: str,
        status: str,
        progress_percent: Optional[int] = None,
        message_text: Optional[str] = None,
    ):
        """
        Broadcast workflow progress event.

        Args:
            adw_id: Workflow identifier
            phase: Current phase name
            status: Phase status
            progress_percent: Optional progress percentage
            message_text: Optional progress message
        """
        message = WebSocketMessage(
            type=WebSocketMessageType.WORKFLOW_PROGRESS,
            data={
                "adw_id": adw_id,
                "phase": phase,
                "status": status,
                "progress_percent": progress_percent,
                "message": message_text,
            },
            timestamp=datetime.now(),
        )
        await self.broadcast(message.model_dump(mode="json"))

    async def broadcast_workflow_completed(
        self,
        adw_id: str,
        pr_number: int,
        pr_url: str,
    ):
        """
        Broadcast workflow completed event.

        Args:
            adw_id: Workflow identifier
            pr_number: Pull request number
            pr_url: Pull request URL
        """
        message = WebSocketMessage(
            type=WebSocketMessageType.WORKFLOW_COMPLETED,
            data={
                "adw_id": adw_id,
                "pr_number": pr_number,
                "pr_url": pr_url,
            },
            timestamp=datetime.now(),
        )
        await self.broadcast(message.model_dump(mode="json"))

    async def broadcast_workflow_failed(
        self,
        adw_id: str,
        error_message: str,
        phase: Optional[str] = None,
    ):
        """
        Broadcast workflow failed event.

        Args:
            adw_id: Workflow identifier
            error_message: Error description
            phase: Optional phase where failure occurred
        """
        message = WebSocketMessage(
            type=WebSocketMessageType.WORKFLOW_FAILED,
            data={
                "adw_id": adw_id,
                "error_message": error_message,
                "phase": phase,
            },
            timestamp=datetime.now(),
        )
        await self.broadcast(message.model_dump(mode="json"))

    async def broadcast_error(self, error_message: str, details: Optional[dict[str, Any]] = None):
        """
        Broadcast error message.

        Args:
            error_message: Error description
            details: Optional additional error details
        """
        message = WebSocketMessage(
            type=WebSocketMessageType.ERROR,
            data={
                "error_message": error_message,
                "details": details or {},
            },
            timestamp=datetime.now(),
        )
        await self.broadcast(message.model_dump(mode="json"))

    async def keep_alive(self, websocket: WebSocket):
        """
        Send periodic ping messages to keep connection alive.

        Args:
            websocket: WebSocket connection to keep alive
        """
        try:
            while websocket.client_state == WebSocketState.CONNECTED:
                await asyncio.sleep(30)  # Ping every 30 seconds
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_json({"type": "ping", "timestamp": datetime.now().isoformat()})
        except Exception as e:
            logger.debug(f"Keep-alive failed: {e}")


# Global connection manager instance
_connection_manager: Optional[ConnectionManager] = None


def get_connection_manager() -> ConnectionManager:
    """
    Get or create the global connection manager instance.

    Returns:
        ConnectionManager singleton instance
    """
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint handler.

    Accepts connections, manages client lifecycle, and handles disconnections.

    Args:
        websocket: WebSocket connection
    """
    manager = get_connection_manager()

    try:
        # Accept connection
        await manager.connect(websocket)

        # Send welcome message
        await manager.send_to_client(
            websocket,
            {
                "type": "connected",
                "message": "Connected to tac-webbuilder API",
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Start keep-alive task
        keep_alive_task = asyncio.create_task(manager.keep_alive(websocket))

        try:
            # Keep connection open and receive messages
            while True:
                data = await websocket.receive_text()
                logger.debug(f"Received from client: {data}")

                # Echo back for now (can add client-to-server message handling)
                await manager.send_to_client(
                    websocket,
                    {
                        "type": "echo",
                        "data": data,
                        "timestamp": datetime.now().isoformat(),
                    },
                )

        except WebSocketDisconnect:
            logger.info("Client disconnected normally")
        finally:
            keep_alive_task.cancel()
            try:
                await keep_alive_task
            except asyncio.CancelledError:
                pass

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await manager.disconnect(websocket)
