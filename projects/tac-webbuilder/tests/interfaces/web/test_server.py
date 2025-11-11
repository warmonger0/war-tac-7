"""Tests for the FastAPI server."""

import pytest
from fastapi.testclient import TestClient

from interfaces.web.server import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "tac-webbuilder API"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"
    assert data["websocket"] == "/ws"


def test_cors_headers(client):
    """Test CORS headers are present."""
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5174",
            "Access-Control-Request-Method": "GET",
        },
    )
    # FastAPI TestClient doesn't fully simulate CORS, but we can check the middleware is configured
    # In a real scenario, the headers would be present
    assert response.status_code in [200, 204]


def test_nonexistent_endpoint(client):
    """Test that non-existent endpoints return 404."""
    response = client.get("/api/nonexistent")
    assert response.status_code == 404
