#!/usr/bin/env python3
"""
Codebase Indexer - Create lightweight index for codebase-expert subagent.

This creates a compact index of the codebase that can be loaded quickly
by a subagent to determine which files are relevant for a specific task.

Usage:
    # Index entire project
    python3 adws/index_codebase.py projects/tac-webbuilder

    # Output to file
    python3 adws/index_codebase.py projects/tac-webbuilder > .codebase_index.json
"""

import ast
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import argparse


def estimate_tokens(text: str) -> int:
    """Rough token estimation (1 token ≈ 4 characters)."""
    return len(text) // 4


def parse_python_file(file_path: Path) -> Dict[str, Any]:
    """Extract structure from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)

        imports = []
        classes = {}
        functions = {}

        for node in ast.walk(tree):
            # Collect imports
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

            # Collect classes
            elif isinstance(node, ast.ClassDef):
                methods = [
                    n.name for n in node.body
                    if isinstance(n, ast.FunctionDef)
                ]
                classes[node.name] = {
                    "line_start": node.lineno,
                    "line_end": node.end_lineno or node.lineno,
                    "methods": methods
                }

            # Collect top-level functions
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                functions[node.name] = {
                    "line_start": node.lineno,
                    "line_end": node.end_lineno or node.lineno
                }

        lines = content.split('\n')
        return {
            "imports": list(set(imports)),
            "classes": classes,
            "functions": functions,
            "lines": len(lines),
            "tokens": estimate_tokens(content)
        }

    except Exception as e:
        return {
            "error": str(e),
            "imports": [],
            "classes": {},
            "functions": {},
            "lines": 0,
            "tokens": 0
        }


def parse_typescript_file(file_path: Path) -> Dict[str, Any]:
    """Extract basic structure from TypeScript/JavaScript file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        imports = []
        exports = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import '):
                imports.append(stripped)
            elif stripped.startswith('export '):
                exports.append(stripped)

        return {
            "imports": imports[:10],  # First 10 imports
            "exports": exports[:10],  # First 10 exports
            "lines": len(lines),
            "tokens": estimate_tokens(content)
        }

    except Exception as e:
        return {
            "error": str(e),
            "imports": [],
            "exports": [],
            "lines": 0,
            "tokens": 0
        }


def should_skip_file(file_path: Path, project_root: Path) -> bool:
    """Determine if file should be skipped based on .claudeignore patterns."""
    rel_path = str(file_path.relative_to(project_root))

    # Common patterns to skip
    skip_patterns = [
        '__pycache__',
        'node_modules',
        '.git',
        'dist',
        'build',
        '.pytest_cache',
        '.venv',
        'venv',
        '.DS_Store',
        '.log',
        '.lock',
        'agents/',
        'trees/',
        'logs/'
    ]

    return any(pattern in rel_path for pattern in skip_patterns)


def index_codebase(project_path: str) -> Dict[str, Any]:
    """Create a lightweight index of the codebase."""
    project_root = Path(project_path).resolve()

    if not project_root.exists():
        raise ValueError(f"Project path does not exist: {project_path}")

    index = {
        "project_root": str(project_root),
        "files": {},
        "summary": {
            "total_files": 0,
            "total_lines": 0,
            "total_tokens": 0,
            "by_extension": {}
        }
    }

    # Walk the directory
    for file_path in project_root.rglob('*'):
        if not file_path.is_file():
            continue

        if should_skip_file(file_path, project_root):
            continue

        rel_path = str(file_path.relative_to(project_root))
        extension = file_path.suffix

        file_info = {
            "path": rel_path,
            "extension": extension,
            "size_bytes": file_path.stat().st_size
        }

        # Parse based on file type
        if extension == '.py':
            structure = parse_python_file(file_path)
            file_info.update(structure)
        elif extension in ['.ts', '.tsx', '.js', '.jsx']:
            structure = parse_typescript_file(file_path)
            file_info.update(structure)
        elif extension in ['.md', '.txt']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_info['lines'] = len(content.split('\n'))
                    file_info['tokens'] = estimate_tokens(content)
            except:
                file_info['lines'] = 0
                file_info['tokens'] = 0
        else:
            # For other files, just track existence
            file_info['lines'] = 0
            file_info['tokens'] = 0

        # Add to index
        index['files'][rel_path] = file_info

        # Update summary
        index['summary']['total_files'] += 1
        index['summary']['total_lines'] += file_info.get('lines', 0)
        index['summary']['total_tokens'] += file_info.get('tokens', 0)

        # Count by extension
        if extension not in index['summary']['by_extension']:
            index['summary']['by_extension'][extension] = {
                'count': 0,
                'total_lines': 0,
                'total_tokens': 0
            }

        index['summary']['by_extension'][extension]['count'] += 1
        index['summary']['by_extension'][extension]['total_lines'] += file_info.get('lines', 0)
        index['summary']['by_extension'][extension]['total_tokens'] += file_info.get('tokens', 0)

    return index


def main():
    parser = argparse.ArgumentParser(description='Index codebase for codebase-expert')
    parser.add_argument('project_path', help='Path to project to index')
    parser.add_argument('--compact', action='store_true', help='Compact JSON output')

    args = parser.parse_args()

    try:
        index = index_codebase(args.project_path)

        # Output JSON
        indent = None if args.compact else 2
        print(json.dumps(index, indent=indent))

        # Print summary to stderr so it doesn't interfere with JSON output
        print(f"\n✅ Indexed {index['summary']['total_files']} files", file=sys.stderr)
        print(f"   Total lines: {index['summary']['total_lines']:,}", file=sys.stderr)
        print(f"   Estimated tokens: {index['summary']['total_tokens']:,}", file=sys.stderr)
        print(f"\n   By extension:", file=sys.stderr)
        for ext, stats in sorted(index['summary']['by_extension'].items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"     {ext or 'none':8s}: {stats['count']:4d} files, {stats['total_tokens']:>8,} tokens", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
