"""
Tests for /api/routes endpoint
"""

import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_get_routes_returns_valid_response():
    """Test that GET /api/routes returns valid JSON structure"""
    response = client.get("/api/routes")

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "routes" in data
    assert "total" in data
    assert isinstance(data["routes"], list)
    assert isinstance(data["total"], int)


def test_get_routes_contains_required_fields():
    """Test that each route contains required fields"""
    response = client.get("/api/routes")
    data = response.json()

    assert len(data["routes"]) > 0

    for route in data["routes"]:
        assert "path" in route
        assert "method" in route
        assert "handler" in route
        assert "description" in route

        assert isinstance(route["path"], str)
        assert isinstance(route["method"], str)
        assert isinstance(route["handler"], str)
        assert isinstance(route["description"], str)


def test_get_routes_includes_known_endpoints():
    """Test that response includes known API endpoints"""
    response = client.get("/api/routes")
    data = response.json()

    paths = [r["path"] for r in data["routes"]]

    # Check for known endpoints
    assert "/api/upload" in paths
    assert "/api/query" in paths
    assert "/api/health" in paths
    assert "/api/routes" in paths


def test_get_routes_total_matches_count():
    """Test that total field matches actual routes count"""
    response = client.get("/api/routes")
    data = response.json()

    assert data["total"] == len(data["routes"])


def test_get_routes_methods_are_uppercase():
    """Test that HTTP methods are uppercase"""
    response = client.get("/api/routes")
    data = response.json()

    valid_methods = {"GET", "POST", "PUT", "DELETE", "PATCH"}

    for route in data["routes"]:
        assert route["method"] in valid_methods


def test_get_routes_paths_start_with_slash():
    """Test that all route paths start with /"""
    response = client.get("/api/routes")
    data = response.json()

    for route in data["routes"]:
        assert route["path"].startswith("/")
