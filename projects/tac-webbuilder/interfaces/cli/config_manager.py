"""Configuration management for CLI interface."""

import os
from pathlib import Path
from typing import Optional, Any, Dict
import yaml

from core.config import load_config, AppConfig
from interfaces.cli.output import show_error, show_success, create_table, print_table


# Default configuration file path
DEFAULT_CONFIG_PATH = Path.home() / ".webbuilder" / "config.yaml"


def ensure_config_dir() -> Path:
    """
    Ensure the configuration directory exists.

    Returns:
        Path to the config directory
    """
    config_dir = DEFAULT_CONFIG_PATH.parent
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_path() -> Path:
    """
    Get the path to the configuration file.

    Checks for custom config path in WEBBUILDER_CONFIG env var,
    otherwise uses default path.

    Returns:
        Path to the config file
    """
    custom_path = os.environ.get("WEBBUILDER_CONFIG")
    if custom_path:
        return Path(custom_path)
    return DEFAULT_CONFIG_PATH


def load_cli_config() -> AppConfig:
    """
    Load the application configuration for CLI use.

    Returns:
        AppConfig instance
    """
    config_path = get_config_path()
    if config_path.exists():
        return load_config(config_path)
    return load_config()


def get_config_value(key: str) -> Optional[str]:
    """
    Get a configuration value by dot-notation key.

    Supports keys like:
    - github.default_repo
    - github.auto_post
    - adw.default_workflow
    - interfaces.cli.enabled

    Args:
        key: Dot-notation key (e.g., "github.default_repo")

    Returns:
        Configuration value as string, or None if not found
    """
    try:
        config = load_cli_config()

        # Navigate through nested config using dot notation
        parts = key.split(".")
        value = config
        for part in parts:
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return None

        return str(value) if value is not None else None
    except Exception as e:
        show_error(f"Error reading config: {e}")
        return None


def set_config_value(key: str, value: str) -> bool:
    """
    Set a configuration value in the YAML config file.

    Args:
        key: Dot-notation key (e.g., "github.default_repo")
        value: Value to set

    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_config_dir()
        config_path = get_config_path()

        # Load existing config or create new one
        if config_path.exists():
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f) or {}
        else:
            config_data = {}

        # Navigate to the target location and set value
        parts = key.split(".")
        current = config_data

        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]

        # Convert boolean strings to actual booleans
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        # Try to convert to int if possible
        elif value.isdigit():
            value = int(value)

        # Set the final value
        current[parts[-1]] = value

        # Write back to file
        with open(config_path, "w") as f:
            yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

        show_success(f"Set {key} = {value}")
        return True

    except Exception as e:
        show_error(f"Error setting config: {e}")
        return False


def list_config() -> Dict[str, Any]:
    """
    List all configuration values.

    Returns:
        Dictionary of all config values
    """
    try:
        config = load_cli_config()

        # Build a flat dictionary of all config values
        config_dict = {}

        # GitHub config
        config_dict["github.default_repo"] = config.github.default_repo
        config_dict["github.repo_url"] = config.github.repo_url or ""
        config_dict["github.auto_post"] = str(config.github.auto_post)

        # ADW config
        config_dict["adw.default_workflow"] = config.adw.default_workflow
        config_dict["adw.default_model_set"] = config.adw.default_model_set

        # Interface config
        config_dict["interfaces.cli.enabled"] = str(config.interfaces.cli.enabled)
        config_dict["interfaces.web.enabled"] = str(config.interfaces.web.enabled)
        config_dict["interfaces.web.port"] = str(config.interfaces.web.port)
        config_dict["interfaces.web.host"] = config.interfaces.web.host

        # Claude config
        config_dict["claude.code_path"] = config.claude.code_path

        return config_dict

    except Exception as e:
        show_error(f"Error listing config: {e}")
        return {}


def display_config() -> None:
    """Display all configuration values in a formatted table."""
    config_dict = list_config()

    if not config_dict:
        show_error("No configuration found")
        return

    # Create table
    columns = [("Key", "cyan"), ("Value", "green")]
    rows = [[key, value] for key, value in config_dict.items()]

    table = create_table(
        title="Configuration",
        columns=columns,
        rows=rows,
        show_lines=False
    )

    print_table(table)

    # Show config file location
    config_path = get_config_path()
    if config_path.exists():
        print(f"\nConfig file: {config_path}")
    else:
        print(f"\nNo config file found. Using defaults and environment variables.")
        print(f"Config will be created at: {config_path}")


def reset_config() -> bool:
    """
    Reset configuration to defaults by removing the config file.

    Returns:
        True if successful, False otherwise
    """
    try:
        config_path = get_config_path()
        if config_path.exists():
            config_path.unlink()
            show_success(f"Configuration reset. Deleted {config_path}")
            return True
        else:
            show_error("No configuration file to reset")
            return False
    except Exception as e:
        show_error(f"Error resetting config: {e}")
        return False


def validate_config() -> bool:
    """
    Validate the current configuration.

    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        config = load_cli_config()

        # Check GitHub configuration
        if config.github.default_repo and "/" not in config.github.default_repo:
            show_error("Invalid GitHub repo format. Must be 'owner/repo'")
            return False

        # Check port range
        if not (1 <= config.interfaces.web.port <= 65535):
            show_error("Invalid web port. Must be between 1 and 65535")
            return False

        show_success("Configuration is valid")
        return True

    except Exception as e:
        show_error(f"Configuration validation failed: {e}")
        return False
