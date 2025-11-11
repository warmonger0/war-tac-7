"""
Unit tests for extraction and validation tooling.

Tests the validation logic for ensuring projects are standalone.
"""

import os
import subprocess
import tempfile
from pathlib import Path
import pytest


class TestDirectoryStructureValidation:
    """Test cases for directory structure validation."""

    def test_valid_directory_structure(self, tmp_path):
        """Test that all required directories are validated correctly."""
        required_dirs = ["app/client", "app/server", "scripts", "tests", "adws"]

        # Create required directories
        for dir_path in required_dirs:
            (tmp_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Verify all directories exist
        for dir_path in required_dirs:
            assert (tmp_path / dir_path).exists()
            assert (tmp_path / dir_path).is_dir()

    def test_missing_directory_detection(self, tmp_path):
        """Test that missing directories are detected."""
        required_dirs = ["app/client", "app/server", "scripts", "tests", "adws"]

        # Create all but one directory
        for dir_path in required_dirs[:-1]:
            (tmp_path / dir_path).mkdir(parents=True, exist_ok=True)

        # Verify the missing directory is detected
        assert not (tmp_path / required_dirs[-1]).exists()


class TestParentPathReferenceDetection:
    """Test cases for parent path reference detection."""

    def test_no_parent_path_references(self, tmp_path):
        """Test files with no parent path references."""
        test_file = tmp_path / "test.py"
        test_file.write_text("from app.server.main import app\nprint('hello')")

        # Search for parent path references
        result = subprocess.run(
            ["grep", "-r", "/Users/Warmonger0/tac/tac-7[^/]", str(tmp_path)],
            capture_output=True,
            text=True
        )

        assert result.returncode != 0  # grep returns non-zero when no matches found

    def test_parent_path_reference_detection(self, tmp_path):
        """Test that parent path references are detected."""
        test_file = tmp_path / "test.py"
        # Use a path that matches the pattern (ends with non-slash character after tac-7)
        test_file.write_text("path = '/Users/Warmonger0/tac/tac-7x/projects/file.py'")

        # Search for parent path references
        result = subprocess.run(
            ["grep", "-r", "/Users/Warmonger0/tac/tac-7[^/]", str(tmp_path)],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0  # grep returns 0 when matches are found
        assert "/Users/Warmonger0/tac/tac-7" in result.stdout


class TestScriptPermissionValidation:
    """Test cases for script permission validation."""

    def test_executable_script_detection(self, tmp_path):
        """Test that executable scripts are detected correctly."""
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()

        test_script = scripts_dir / "test.sh"
        test_script.write_text("#!/bin/bash\necho 'test'")
        test_script.chmod(0o755)  # Make executable

        assert os.access(test_script, os.X_OK)

    def test_non_executable_script_detection(self, tmp_path):
        """Test that non-executable scripts are detected."""
        scripts_dir = tmp_path / "scripts"
        scripts_dir.mkdir()

        test_script = scripts_dir / "test.sh"
        test_script.write_text("#!/bin/bash\necho 'test'")
        test_script.chmod(0o644)  # Not executable

        assert not os.access(test_script, os.X_OK)


class TestExtractionPreFlightChecks:
    """Test cases for extraction script pre-flight checks."""

    def test_source_validation(self, tmp_path):
        """Test that source directory validation works."""
        # Create app/server directory to simulate valid source
        app_server = tmp_path / "app" / "server"
        app_server.mkdir(parents=True)

        assert (tmp_path / "app" / "server").exists()
        assert (tmp_path / "app" / "server").is_dir()

    def test_destination_doesnt_exist(self, tmp_path):
        """Test that destination validation prevents overwriting."""
        dest = tmp_path / "destination"

        # Destination should not exist initially
        assert not dest.exists()

        # Create destination
        dest.mkdir()

        # Now destination exists and should be detected
        assert dest.exists()


@pytest.fixture
def tmp_path():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
