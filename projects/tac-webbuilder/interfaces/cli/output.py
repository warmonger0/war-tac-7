"""Rich terminal output formatting utilities for CLI."""

from typing import Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.markdown import Markdown


# Initialize global console instance
console = Console()


def show_error(message: str, title: str = "Error") -> None:
    """Display an error message in a red panel."""
    console.print(Panel(
        message,
        title=f"[bold red]{title}[/bold red]",
        border_style="red",
        padding=(1, 2)
    ))


def show_success(message: str, title: str = "Success") -> None:
    """Display a success message in a green panel."""
    console.print(Panel(
        message,
        title=f"[bold green]{title}[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))


def show_info(message: str, title: str = "Info") -> None:
    """Display an informational message in a blue panel."""
    console.print(Panel(
        message,
        title=f"[bold blue]{title}[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))


def show_warning(message: str, title: str = "Warning") -> None:
    """Display a warning message in a yellow panel."""
    console.print(Panel(
        message,
        title=f"[bold yellow]{title}[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    ))


def show_panel(
    content: str,
    title: Optional[str] = None,
    border_style: str = "white",
    padding: tuple[int, int] = (1, 2)
) -> None:
    """Display content in a styled panel."""
    panel_title = f"[bold]{title}[/bold]" if title else None
    console.print(Panel(
        content,
        title=panel_title,
        border_style=border_style,
        padding=padding
    ))


def create_table(
    title: str,
    columns: list[tuple[str, str]],
    rows: list[list[str]],
    show_header: bool = True,
    show_lines: bool = False
) -> Table:
    """Create a rich table with specified columns and rows."""
    table = Table(
        title=title,
        show_header=show_header,
        show_lines=show_lines,
        header_style="bold cyan"
    )

    # Add columns
    for col_name, col_style in columns:
        table.add_column(col_name, style=col_style)

    # Add rows
    for row in rows:
        table.add_row(*row)

    return table


def print_table(table: Table) -> None:
    """Print a table to the console."""
    console.print(table)


def show_markdown(content: str) -> None:
    """Display markdown-formatted content."""
    md = Markdown(content)
    console.print(md)


def show_syntax(
    code: str,
    language: str = "python",
    theme: str = "monokai",
    line_numbers: bool = False
) -> None:
    """Display syntax-highlighted code."""
    syntax = Syntax(code, language, theme=theme, line_numbers=line_numbers)
    console.print(syntax)


def get_progress_spinner(text: str = "Processing...") -> Progress:
    """Create a progress spinner for long-running operations."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    )


def print_status(message: str, style: str = "bold cyan") -> None:
    """Print a status message with optional styling."""
    console.print(f"[{style}]{message}[/{style}]")


def print_divider(char: str = "-", style: str = "dim") -> None:
    """Print a horizontal divider line."""
    width = console.width
    console.print(f"[{style}]{char * width}[/{style}]")


def confirm_action(prompt: str) -> bool:
    """Ask user to confirm an action."""
    from rich.prompt import Confirm
    return Confirm.ask(prompt)


def prompt_input(prompt: str, default: Optional[str] = None) -> str:
    """Prompt user for text input."""
    from rich.prompt import Prompt
    return Prompt.ask(prompt, default=default)
