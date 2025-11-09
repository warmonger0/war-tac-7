#!/usr/bin/env python3
"""
ADW System Validation Script

This script validates that all ADW components are present and functional
in the tac-webbuilder project after copying from tac-7.
"""

import sys
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists and report result."""
    if path.exists():
        print(f"{Colors.GREEN}✓{Colors.NC} {description}: {path}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.NC} {description} missing: {path}")
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists and report result."""
    if path.is_dir():
        file_count = len(list(path.glob("*")))
        print(f"{Colors.GREEN}✓{Colors.NC} {description}: {path} ({file_count} items)")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.NC} {description} missing: {path}")
        return False


def check_module_import(module_path: str, description: str) -> bool:
    """Check if a module can be imported."""
    try:
        __import__(module_path)
        print(f"{Colors.GREEN}✓{Colors.NC} {description} imports successfully")
        return True
    except ImportError as e:
        print(f"{Colors.RED}✗{Colors.NC} {description} import failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("ADW System Validation")
    print("=" * 60)
    print()

    project_root = Path(__file__).parent.parent
    passed = []
    failed = []

    print("Checking ADW Modules...")
    print("-" * 60)

    adw_modules = [
        "agent.py",
        "data_types.py",
        "git_ops.py",
        "github.py",
        "r2_uploader.py",
        "state.py",
        "utils.py",
        "workflow_ops.py",
        "worktree_ops.py",
        "__init__.py",
    ]

    for module in adw_modules:
        path = project_root / "adws" / "adw_modules" / module
        if check_file_exists(path, f"ADW module {module}"):
            passed.append(module)
        else:
            failed.append(module)

    print()
    print("Checking ADW Workflow Scripts...")
    print("-" * 60)

    workflow_scripts = [
        "adw_build_iso.py",
        "adw_document_iso.py",
        "adw_patch_iso.py",
        "adw_plan_build_document_iso.py",
        "adw_plan_build_iso.py",
        "adw_plan_build_review_iso.py",
        "adw_plan_build_test_iso.py",
        "adw_plan_build_test_review_iso.py",
        "adw_plan_iso.py",
        "adw_review_iso.py",
        "adw_sdlc_iso.py",
        "adw_sdlc_zte_iso.py",
        "adw_ship_iso.py",
        "adw_test_iso.py",
    ]

    for script in workflow_scripts:
        path = project_root / "adws" / script
        if check_file_exists(path, f"Workflow script {script}"):
            passed.append(script)
        else:
            failed.append(script)

    print()
    print("Checking ADW Support Directories...")
    print("-" * 60)

    support_dirs = [
        ("adws/adw_triggers", "ADW triggers directory"),
        ("adws/adw_tests", "ADW tests directory"),
        (".claude/commands", "Claude commands directory"),
        (".claude/hooks", "Claude hooks directory"),
    ]

    for dir_path, description in support_dirs:
        path = project_root / dir_path
        if check_directory_exists(path, description):
            passed.append(dir_path)
        else:
            failed.append(dir_path)

    print()
    print("Checking Key Files...")
    print("-" * 60)

    key_files = [
        ("adws/README.md", "ADW documentation"),
        (".claude/settings.json", "Claude settings"),
        ("core/config.py", "Configuration module"),
        ("pyproject.toml", "Project configuration"),
    ]

    for file_path, description in key_files:
        path = project_root / file_path
        if check_file_exists(path, description):
            passed.append(file_path)
        else:
            failed.append(file_path)

    print()
    print("Testing Module Imports...")
    print("-" * 60)

    # Add project root to path for imports
    sys.path.insert(0, str(project_root))

    imports = [
        ("core.config", "Core configuration"),
        ("adws.adw_modules.agent", "ADW Agent module"),
        ("adws.adw_modules.data_types", "ADW Data types"),
        ("adws.adw_modules.github", "ADW GitHub module"),
    ]

    for module_path, description in imports:
        if check_module_import(module_path, description):
            passed.append(module_path)
        else:
            failed.append(module_path)

    print()
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"{Colors.GREEN}Passed:{Colors.NC} {len(passed)}")
    print(f"{Colors.RED}Failed:{Colors.NC} {len(failed)}")
    print()

    if failed:
        print(f"{Colors.RED}✗ Validation failed{Colors.NC}")
        print("Failed items:", failed)
        return 1
    else:
        print(f"{Colors.GREEN}✓ All validation checks passed!{Colors.NC}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
