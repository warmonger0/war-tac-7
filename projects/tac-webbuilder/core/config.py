"""
Configuration management for tac-webbuilder.

This module provides Pydantic-based configuration management that supports
loading settings from both YAML files and environment variables, with
environment variables taking precedence.
"""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GitHubConfig(BaseSettings):
    """GitHub-related configuration."""

    model_config = SettingsConfigDict(env_prefix="TWB_GITHUB_")

    default_repo: str = Field(
        default="",
        description="Default GitHub repository in format 'owner/repo'",
    )
    repo_url: Optional[str] = Field(
        default=None,
        description="Full GitHub repository URL",
    )
    pat: Optional[str] = Field(
        default=None,
        description="GitHub Personal Access Token",
    )
    auto_post: bool = Field(
        default=False,
        description="Automatically post issues to GitHub",
    )

    @field_validator("default_repo")
    @classmethod
    def validate_repo_format(cls, v: str) -> str:
        """Validate repository format."""
        if v and "/" not in v:
            raise ValueError("Repository must be in format 'owner/repo'")
        return v


class ADWConfig(BaseSettings):
    """AI Developer Workflow configuration."""

    model_config = SettingsConfigDict(env_prefix="TWB_ADW_")

    default_workflow: str = Field(
        default="adw_sdlc_iso",
        description="Default ADW workflow to use",
    )
    default_model_set: str = Field(
        default="base",
        description="Default model set (base, advanced, etc.)",
    )


class CLIConfig(BaseSettings):
    """CLI interface configuration."""

    model_config = SettingsConfigDict(env_prefix="TWB_CLI_")

    enabled: bool = Field(
        default=True,
        description="Enable CLI interface",
    )


class WebConfig(BaseSettings):
    """Web interface configuration."""

    model_config = SettingsConfigDict(env_prefix="TWB_WEB_")

    enabled: bool = Field(
        default=True,
        description="Enable web interface",
    )
    port: int = Field(
        default=5174,
        description="Port for web interface",
    )
    host: str = Field(
        default="127.0.0.1",
        description="Host for web interface",
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port number."""
        if not (1 <= v <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v


class InterfacesConfig(BaseSettings):
    """All interface configurations."""

    model_config = SettingsConfigDict(env_prefix="TWB_INTERFACES_")

    cli: CLIConfig = Field(default_factory=CLIConfig)
    web: WebConfig = Field(default_factory=WebConfig)


class ClaudeConfig(BaseSettings):
    """Claude Code configuration."""

    model_config = SettingsConfigDict(env_prefix="TWB_CLAUDE_")

    code_path: str = Field(
        default="/usr/local/bin/claude",
        description="Path to Claude Code CLI executable",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Anthropic API key",
    )


class AppConfig(BaseSettings):
    """Main application configuration."""

    model_config = SettingsConfigDict(
        env_prefix="TWB_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    github: GitHubConfig = Field(default_factory=GitHubConfig)
    adw: ADWConfig = Field(default_factory=ADWConfig)
    interfaces: InterfacesConfig = Field(default_factory=InterfacesConfig)
    claude: ClaudeConfig = Field(default_factory=ClaudeConfig)

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> "AppConfig":
        """
        Load configuration from a YAML file.

        Args:
            yaml_path: Path to the YAML configuration file

        Returns:
            AppConfig instance with settings loaded from YAML and environment

        Note:
            Environment variables will override YAML settings.
        """
        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            raise FileNotFoundError(f"Config file not found: {yaml_path}")

        with open(yaml_path, "r") as f:
            yaml_data = yaml.safe_load(f) or {}

        # Convert nested YAML data into environment variables temporarily
        # This allows Pydantic to properly merge YAML and env vars with env taking precedence
        env_backup = {}

        # Flatten YAML data to environment variable format
        def set_env_from_yaml(prefix: str, data: dict):
            """Set environment variables from YAML data if not already set."""
            for key, value in data.items():
                if isinstance(value, dict):
                    # Nested dict - recurse
                    set_env_from_yaml(f"{prefix}{key.upper()}__", value)
                else:
                    # Leaf value - set env var only if not already set (preserving existing env vars)
                    env_key = f"{prefix}{key.upper()}"
                    if env_key not in os.environ:
                        # Save for cleanup (None means it didn't exist before)
                        if env_key not in env_backup:
                            env_backup[env_key] = None
                        os.environ[env_key] = str(value)

        try:
            set_env_from_yaml("TWB_", yaml_data)
            # Now create config - Pydantic will load from env vars, with real env vars taking precedence
            return cls()
        finally:
            # Restore original environment - remove env vars we added
            for key, original_value in env_backup.items():
                if original_value is None:
                    # We added this, remove it
                    os.environ.pop(key, None)

    @classmethod
    def load(cls, yaml_path: Optional[Path | str] = None) -> "AppConfig":
        """
        Load configuration with automatic fallback.

        Tries to load from:
        1. Provided yaml_path
        2. config.yaml in current directory
        3. Environment variables only

        Args:
            yaml_path: Optional path to YAML config file

        Returns:
            AppConfig instance
        """
        # Try provided path
        if yaml_path:
            return cls.from_yaml(yaml_path)

        # Try default config.yaml
        default_config = Path("config.yaml")
        if default_config.exists():
            return cls.from_yaml(default_config)

        # Fall back to environment variables only
        return cls()


# Convenience function for loading config
def load_config(yaml_path: Optional[Path | str] = None) -> AppConfig:
    """
    Load application configuration.

    Args:
        yaml_path: Optional path to YAML configuration file

    Returns:
        AppConfig instance with all settings loaded
    """
    return AppConfig.load(yaml_path)
