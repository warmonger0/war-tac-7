"""Tests for CLI output formatting utilities."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from interfaces.cli.output import (
    show_error,
    show_success,
    show_info,
    show_warning,
    show_panel,
    create_table,
    print_table,
    show_markdown,
    show_syntax,
    print_status,
    print_divider,
)


@pytest.fixture
def mock_console():
    """Mock the rich console."""
    with patch("interfaces.cli.output.console") as mock:
        yield mock


class TestErrorMessages:
    """Test error message display functions."""

    def test_show_error(self, mock_console):
        """Test error message display."""
        show_error("Test error message")
        mock_console.print.assert_called_once()
        # Just verify the function was called - actual rendering is Rich's responsibility

    def test_show_error_custom_title(self, mock_console):
        """Test error message with custom title."""
        show_error("Test error", title="Custom Error")
        mock_console.print.assert_called_once()


class TestSuccessMessages:
    """Test success message display functions."""

    def test_show_success(self, mock_console):
        """Test success message display."""
        show_success("Operation completed")
        mock_console.print.assert_called_once()

    def test_show_success_custom_title(self, mock_console):
        """Test success message with custom title."""
        show_success("Done!", title="Completed")
        mock_console.print.assert_called_once()


class TestInfoMessages:
    """Test info message display functions."""

    def test_show_info(self, mock_console):
        """Test info message display."""
        show_info("Information message")
        mock_console.print.assert_called_once()


class TestWarningMessages:
    """Test warning message display functions."""

    def test_show_warning(self, mock_console):
        """Test warning message display."""
        show_warning("Warning message")
        mock_console.print.assert_called_once()


class TestPanelDisplay:
    """Test panel display functions."""

    def test_show_panel_basic(self, mock_console):
        """Test basic panel display."""
        show_panel("Test content")
        mock_console.print.assert_called_once()

    def test_show_panel_with_title(self, mock_console):
        """Test panel with title."""
        show_panel("Content", title="My Panel")
        mock_console.print.assert_called_once()


class TestTableCreation:
    """Test table creation and display."""

    def test_create_table_basic(self):
        """Test basic table creation."""
        columns = [("Name", "cyan"), ("Value", "green")]
        rows = [["Row1", "Value1"], ["Row2", "Value2"]]
        table = create_table("Test Table", columns, rows)

        assert table.title == "Test Table"
        assert len(table.columns) == 2

    def test_create_table_empty_rows(self):
        """Test table with no rows."""
        columns = [("Name", "cyan"), ("Value", "green")]
        rows = []
        table = create_table("Empty Table", columns, rows)

        assert len(table.columns) == 2

    def test_print_table(self, mock_console):
        """Test table printing."""
        columns = [("Col1", "white")]
        rows = [["Data1"]]
        table = create_table("Test", columns, rows)
        print_table(table)

        mock_console.print.assert_called_once_with(table)


class TestMarkdownDisplay:
    """Test markdown display functions."""

    def test_show_markdown(self, mock_console):
        """Test markdown display."""
        markdown_content = "# Heading\n\nParagraph"
        show_markdown(markdown_content)
        mock_console.print.assert_called_once()


class TestSyntaxDisplay:
    """Test syntax highlighting functions."""

    def test_show_syntax_python(self, mock_console):
        """Test Python syntax highlighting."""
        code = "def hello():\n    print('world')"
        show_syntax(code)
        mock_console.print.assert_called_once()

    def test_show_syntax_custom_language(self, mock_console):
        """Test syntax highlighting with custom language."""
        code = "SELECT * FROM users;"
        show_syntax(code, language="sql")
        mock_console.print.assert_called_once()


class TestStatusDisplay:
    """Test status message display."""

    def test_print_status(self, mock_console):
        """Test status message printing."""
        print_status("Processing...")
        mock_console.print.assert_called_once()

    def test_print_status_custom_style(self, mock_console):
        """Test status with custom style."""
        print_status("Done", style="bold green")
        mock_console.print.assert_called_once()


class TestDivider:
    """Test divider display."""

    def test_print_divider_default(self, mock_console):
        """Test default divider."""
        mock_console.width = 80
        print_divider()
        mock_console.print.assert_called_once()

    def test_print_divider_custom_char(self, mock_console):
        """Test divider with custom character."""
        mock_console.width = 80
        print_divider(char="=")
        mock_console.print.assert_called_once()
