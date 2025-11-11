"""Main CLI entry point using Typer."""

import typer
from typing import Optional
from rich.console import Console

from interfaces.cli import __version__
from interfaces.cli.commands import handle_request, handle_new_project, handle_integrate
from interfaces.cli.interactive import run_interactive_mode
from interfaces.cli.history import get_history
from interfaces.cli.config_manager import (
    get_config_value,
    set_config_value,
    display_config,
    reset_config,
    validate_config,
)
from interfaces.cli.output import show_error, show_success, show_info


# Create the Typer app
app = typer.Typer(
    name="webbuilder",
    help="Natural language interface for tac-7 AI Developer Workflows",
    add_completion=False,
)

# Create console for rich output
console = Console()


@app.command()
def request(
    nl_input: str = typer.Argument(
        ...,
        help="Natural language description of what to build or change",
    ),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        "-p",
        help="Target project path (default: current directory)",
    ),
    auto_post: bool = typer.Option(
        False,
        "--auto-post",
        "-y",
        help="Skip confirmation and post immediately",
    ),
) -> None:
    """
    Submit a natural language request to create a GitHub issue.

    Examples:
        webbuilder request "Add user authentication"
        webbuilder request "Fix login bug" --project /path/to/project
        webbuilder request "Add dark mode" --auto-post
    """
    success = handle_request(
        nl_input=nl_input,
        project_path=project,
        auto_post=auto_post,
    )

    if not success:
        raise typer.Exit(code=1)


@app.command()
def interactive() -> None:
    """
    Start interactive mode with guided prompts.

    Interactive mode provides a menu-driven interface for:
    - Submitting requests
    - Viewing history
    - Creating new projects (coming soon)
    - Integrating ADW into existing codebases (coming soon)
    """
    run_interactive_mode()


@app.command()
def history(
    limit: int = typer.Option(
        10,
        "--limit",
        "-n",
        help="Number of recent entries to show",
    ),
) -> None:
    """
    View past requests and their status.

    Examples:
        webbuilder history
        webbuilder history --limit 25
    """
    history_manager = get_history()
    history_manager.display(limit=limit)


@app.command()
def config(
    action: str = typer.Argument(
        ...,
        help="Action to perform: get, set, list, reset, validate",
    ),
    key: Optional[str] = typer.Argument(
        None,
        help="Configuration key (for get/set actions)",
    ),
    value: Optional[str] = typer.Argument(
        None,
        help="Configuration value (for set action)",
    ),
) -> None:
    """
    Manage configuration settings.

    Actions:
        list      - Show all configuration values
        get       - Get a specific configuration value
        set       - Set a configuration value
        reset     - Reset configuration to defaults
        validate  - Validate current configuration

    Examples:
        webbuilder config list
        webbuilder config get github.default_repo
        webbuilder config set github.default_repo owner/repo
        webbuilder config set github.auto_post true
        webbuilder config reset
        webbuilder config validate
    """
    action = action.lower()

    if action == "list":
        display_config()

    elif action == "get":
        if not key:
            show_error("Key required for 'get' action")
            raise typer.Exit(code=1)

        value = get_config_value(key)
        if value is not None:
            show_success(f"{key} = {value}")
        else:
            show_error(f"Configuration key not found: {key}")
            raise typer.Exit(code=1)

    elif action == "set":
        if not key or not value:
            show_error("Both key and value required for 'set' action")
            raise typer.Exit(code=1)

        success = set_config_value(key, value)
        if not success:
            raise typer.Exit(code=1)

    elif action == "reset":
        success = reset_config()
        if not success:
            raise typer.Exit(code=1)

    elif action == "validate":
        success = validate_config()
        if not success:
            raise typer.Exit(code=1)

    else:
        show_error(
            f"Unknown action: {action}\n"
            "Valid actions: list, get, set, reset, validate"
        )
        raise typer.Exit(code=1)


@app.command()
def integrate(
    path: str = typer.Argument(
        ...,
        help="Path to existing project",
    ),
) -> None:
    """
    Integrate ADW into an existing codebase (Coming Soon).

    This command will set up AI Developer Workflows in your
    existing project, including configuration files, workflow
    templates, and integration with your CI/CD pipeline.

    Example:
        webbuilder integrate /path/to/project
    """
    success = handle_integrate(path)
    if not success:
        raise typer.Exit(code=1)


@app.command()
def new(
    name: str = typer.Argument(
        ...,
        help="Project name",
    ),
    framework: str = typer.Option(
        "react-vite",
        "--framework",
        "-f",
        help="Framework to use (react-vite, vue, svelte, etc.)",
    ),
) -> None:
    """
    Create a new web app project (Coming Soon).

    This command will scaffold a new web application with your
    chosen framework, complete with ADW integration.

    Examples:
        webbuilder new myapp
        webbuilder new myapp --framework vue
    """
    success = handle_new_project(name, framework)
    if not success:
        raise typer.Exit(code=1)


@app.command()
def version() -> None:
    """Show the version of tac-webbuilder CLI."""
    show_info(f"tac-webbuilder CLI version {__version__}")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
