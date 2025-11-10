"""
Unit tests for routes_analyzer module
"""

import pytest
import tempfile
import os
from pathlib import Path
from core.routes_analyzer import RoutesAnalyzer


class TestRoutesAnalyzer:
    """Test suite for RoutesAnalyzer class"""

    def test_analyze_existing_server_routes(self):
        """Test that analyzer correctly identifies routes from actual server.py"""
        analyzer = RoutesAnalyzer("server.py")
        routes = analyzer.analyze_routes()

        # Should find multiple routes
        assert len(routes) > 0

        # Check that routes have required fields
        for route in routes:
            assert 'path' in route
            assert 'method' in route
            assert 'handler' in route
            assert 'description' in route

        # Check for some known routes
        paths = [r['path'] for r in routes]
        assert '/api/upload' in paths
        assert '/api/query' in paths
        assert '/api/health' in paths

    def test_analyze_routes_with_different_methods(self):
        """Test that analyzer extracts different HTTP methods correctly"""
        analyzer = RoutesAnalyzer("server.py")
        routes = analyzer.analyze_routes()

        methods = {r['method'] for r in routes}
        # Server should have GET, POST, and DELETE methods
        assert 'GET' in methods
        assert 'POST' in methods
        assert 'DELETE' in methods

    def test_analyze_routes_extracts_docstrings(self):
        """Test that analyzer extracts function docstrings as descriptions"""
        analyzer = RoutesAnalyzer("server.py")
        routes = analyzer.analyze_routes()

        # Find the upload route
        upload_route = next((r for r in routes if r['path'] == '/api/upload'), None)
        assert upload_route is not None
        # Should have a description from docstring
        assert upload_route['description'] != "N/A"
        assert len(upload_route['description']) > 0

    def test_analyze_routes_handles_missing_docstrings(self):
        """Test that analyzer handles functions without docstrings"""
        # Create temporary file with route but no docstring
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write("""
from fastapi import FastAPI
app = FastAPI()

@app.get("/test")
async def test_route():
    return {"status": "ok"}
""")
        temp_file.close()

        try:
            analyzer = RoutesAnalyzer(temp_file.name)
            routes = analyzer.analyze_routes()

            assert len(routes) == 1
            assert routes[0]['description'] == "N/A"
        finally:
            os.unlink(temp_file.name)

    def test_analyze_routes_with_no_routes(self):
        """Test that analyzer handles files with no routes"""
        # Create temporary file with no routes
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write("""
def some_function():
    return "hello"
""")
        temp_file.close()

        try:
            analyzer = RoutesAnalyzer(temp_file.name)
            routes = analyzer.analyze_routes()

            assert len(routes) == 0
        finally:
            os.unlink(temp_file.name)

    def test_analyze_routes_with_malformed_file(self):
        """Test that analyzer handles syntax errors gracefully"""
        # Create temporary file with syntax error
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write("""
def broken syntax here
""")
        temp_file.close()

        try:
            analyzer = RoutesAnalyzer(temp_file.name)
            routes = analyzer.analyze_routes()

            # Should return empty list, not raise exception
            assert routes == []
        finally:
            os.unlink(temp_file.name)

    def test_analyze_nonexistent_file(self):
        """Test that analyzer handles nonexistent files gracefully"""
        analyzer = RoutesAnalyzer("nonexistent_file.py")
        routes = analyzer.analyze_routes()

        # Should return empty list, not raise exception
        assert routes == []

    def test_routes_sorted_by_path(self):
        """Test that routes are returned sorted by path"""
        analyzer = RoutesAnalyzer("server.py")
        routes = analyzer.analyze_routes()

        # Check that paths are in sorted order
        paths = [r['path'] for r in routes]
        assert paths == sorted(paths)

    def test_extract_route_with_post_method(self):
        """Test extraction of POST routes"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write("""
from fastapi import FastAPI
app = FastAPI()

@app.post("/api/create")
async def create_item():
    '''Create a new item'''
    return {"status": "created"}
""")
        temp_file.close()

        try:
            analyzer = RoutesAnalyzer(temp_file.name)
            routes = analyzer.analyze_routes()

            assert len(routes) == 1
            assert routes[0]['method'] == 'POST'
            assert routes[0]['path'] == '/api/create'
            assert routes[0]['handler'] == 'create_item'
        finally:
            os.unlink(temp_file.name)

    def test_extract_route_with_delete_method(self):
        """Test extraction of DELETE routes"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_file.write("""
from fastapi import FastAPI
app = FastAPI()

@app.delete("/api/remove/{id}")
async def remove_item():
    '''Remove an item'''
    return {"status": "deleted"}
""")
        temp_file.close()

        try:
            analyzer = RoutesAnalyzer(temp_file.name)
            routes = analyzer.analyze_routes()

            assert len(routes) == 1
            assert routes[0]['method'] == 'DELETE'
            assert routes[0]['path'] == '/api/remove/{id}'
        finally:
            os.unlink(temp_file.name)
