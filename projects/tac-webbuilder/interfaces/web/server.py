"""
Main FastAPI application for tac-webbuilder web backend.

This module sets up the FastAPI application with all routes, middleware,
and WebSocket support for the web interface.
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from interfaces.web.models import HealthResponse
from interfaces.web.routes import history, projects, requests, workflows
from interfaces.web.state import get_request_state
from interfaces.web.websocket import get_connection_manager, websocket_endpoint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting tac-webbuilder API server...")

    # Initialize singletons
    get_request_state()
    get_connection_manager()

    # Clean up old requests on startup
    try:
        state = get_request_state()
        state.cleanup_old_requests()
        logger.info("Cleaned up old pending requests")
    except Exception as e:
        logger.error(f"Failed to cleanup old requests: {e}")

    logger.info(" API server started successfully")

    yield

    # Shutdown
    logger.info("Shutting down tac-webbuilder API server...")
    logger.info(" API server shut down")


# Create FastAPI application
app = FastAPI(
    title="tac-webbuilder API",
    version="1.0.0",
    description="Web backend API for tac-webbuilder - Natural language interface for AI Developer Workflows",
    lifespan=lifespan,
)

# CORS middleware configuration
# Get frontend origin from environment or use default
frontend_origin = os.getenv("TWB_FRONTEND_ORIGIN", "http://localhost:5174")
allowed_origins = [frontend_origin]

# Add additional origins if specified
additional_origins = os.getenv("TWB_ADDITIONAL_ORIGINS", "")
if additional_origins:
    allowed_origins.extend([origin.strip() for origin in additional_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    start_time = datetime.now()
    logger.info(f"{request.method} {request.url.path}")

    try:
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"{request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)")
        return response
    except Exception as e:
        logger.error(f"{request.method} {request.url.path} - Error: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": {"code": "internal_error", "message": str(e)}},
        )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "internal_error",
                "message": "An internal server error occurred",
            }
        },
    )


# Register routers
app.include_router(requests.router)
app.include_router(workflows.router)
app.include_router(projects.router)
app.include_router(history.router)


# Health check endpoint
@app.get(
    "/api/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check",
    description="Check if the API server is running and healthy",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse with server status and version
    """
    return HealthResponse(
        status="ok",
        version="1.0.0",
        timestamp=datetime.now(),
    )


# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="API root",
    description="Root endpoint with API information",
)
async def root():
    """
    Root endpoint.

    Returns:
        API information and links
    """
    return {
        "name": "tac-webbuilder API",
        "version": "1.0.0",
        "description": "Web backend API for tac-webbuilder",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health",
        "websocket": "/ws",
    }


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_route(websocket):
    """
    WebSocket endpoint for real-time updates.

    Provides real-time workflow status updates to connected clients.
    """
    await websocket_endpoint(websocket)


if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment
    host = os.getenv("TWB_WEB_BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("TWB_WEB_BACKEND_PORT", "8002"))
    reload = os.getenv("TWB_WEB_BACKEND_RELOAD", "true").lower() == "true"

    logger.info(f"Starting server on {host}:{port} (reload={reload})")

    uvicorn.run(
        "interfaces.web.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
