"""Interactive mode for CLI interface."""

from pathlib import Path
from typing import Optional
import questionary
from questionary import ValidationError, Validator

from interfaces.cli.output import show_info, show_error, show_success, print_divider
from interfaces.cli.commands import handle_request
from interfaces.cli.history import get_history


class PathValidator(Validator):
    """Validator for file paths."""

    def validate(self, document) -> None:
        """Validate that the path exists."""
        if document.text:
            path = Path(document.text)
            if not path.exists():
                raise ValidationError(
                    message="Path does not exist",
                    cursor_position=len(document.text),
                )
            if not path.is_dir():
                raise ValidationError(
                    message="Path must be a directory",
                    cursor_position=len(document.text),
                )


class NonEmptyValidator(Validator):
    """Validator for non-empty strings."""

    def validate(self, document) -> None:
        """Validate that the string is not empty."""
        if not document.text or not document.text.strip():
            raise ValidationError(
                message="This field cannot be empty",
                cursor_position=len(document.text),
            )


def prompt_project_path() -> Optional[str]:
    """
    Prompt user for project path.

    Returns:
        Project path or None if cancelled
    """
    try:
        current_dir = Path.cwd()
        use_current = questionary.confirm(
            f"Use current directory ({current_dir})?",
            default=True,
        ).ask()

        if use_current is None:  # User cancelled
            return None

        if use_current:
            return str(current_dir)

        # Prompt for custom path
        path = questionary.path(
            "Enter project path:",
            validate=PathValidator,
            only_directories=True,
        ).ask()

        return path

    except KeyboardInterrupt:
        return None


def prompt_nl_request() -> Optional[str]:
    """
    Prompt user for natural language request.

    Returns:
        Natural language request or None if cancelled
    """
    try:
        request = questionary.text(
            "What would you like to build or change?",
            multiline=False,
            validate=NonEmptyValidator,
        ).ask()

        return request

    except KeyboardInterrupt:
        return None


def handle_submit_request() -> bool:
    """
    Handle submitting a new request through interactive prompts.

    Returns:
        True if successful, False otherwise
    """
    show_info("Let's create a new request")
    print()

    # Get project path
    project_path = prompt_project_path()
    if project_path is None:
        show_error("Cancelled")
        return False

    print()

    # Get natural language request
    nl_request = prompt_nl_request()
    if nl_request is None:
        show_error("Cancelled")
        return False

    print()

    # Confirm before posting
    confirm = questionary.confirm(
        "Review and post this request to GitHub?",
        default=True,
    ).ask()

    if not confirm:
        show_error("Cancelled")
        return False

    # Handle the request (will show preview and confirm)
    return handle_request(
        nl_input=nl_request,
        project_path=project_path,
        auto_post=False,  # Still show preview
    )


def handle_view_history() -> bool:
    """
    Handle viewing request history.

    Returns:
        True if successful, False otherwise
    """
    try:
        history = get_history()

        # Ask for limit
        limit_choice = questionary.select(
            "How many entries to show?",
            choices=[
                "10 (default)",
                "25",
                "50",
                "All",
            ],
        ).ask()

        if limit_choice is None:
            return False

        # Parse limit
        if "All" in limit_choice:
            limit = len(history.get_all())
        else:
            limit = int(limit_choice.split()[0])

        history.display(limit=limit)
        return True

    except KeyboardInterrupt:
        return False


def handle_create_project() -> bool:
    """
    Handle creating a new project (STUB for future).

    Returns:
        True if successful, False otherwise
    """
    show_info("Project creation is coming soon!")
    print()
    show_info(
        "This feature will allow you to scaffold new web applications\n"
        "with frameworks like React, Vue, Svelte, etc."
    )
    return False


def handle_integrate_adw() -> bool:
    """
    Handle integrating ADW into existing project (STUB for future).

    Returns:
        True if successful, False otherwise
    """
    show_info("ADW integration is coming soon!")
    print()
    show_info(
        "This feature will allow you to integrate AI Developer Workflows\n"
        "into your existing codebase."
    )
    return False


def run_interactive_mode() -> None:
    """
    Run the interactive mode with questionary prompts.

    This provides a guided workflow for:
    1. Submitting requests
    2. Viewing history
    3. Creating new projects (stub)
    4. Integrating ADW (stub)
    """
    try:
        show_success("Welcome to tac-webbuilder Interactive Mode!")
        print()
        show_info("Use arrow keys to navigate, Enter to select, Ctrl+C to exit")
        print_divider()
        print()

        while True:
            # Main menu
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Submit a request for existing project",
                    "View history",
                    "Create new web app (coming soon)",
                    "Integrate ADW into existing codebase (coming soon)",
                    "Exit",
                ],
            ).ask()

            if action is None or action == "Exit":
                show_success("Goodbye!")
                break

            print()

            # Handle action
            if "Submit a request" in action:
                handle_submit_request()
            elif "View history" in action:
                handle_view_history()
            elif "Create new web app" in action:
                handle_create_project()
            elif "Integrate ADW" in action:
                handle_integrate_adw()

            # Add spacing between iterations
            print()
            print_divider()
            print()

    except KeyboardInterrupt:
        print()
        show_success("Goodbye!")
    except Exception as e:
        print()
        show_error(f"An error occurred: {e}")
