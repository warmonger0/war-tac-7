#!/usr/bin/env python3
"""
Codebase Index Generator

Generates a lightweight metadata index of the codebase including:
- File paths, sizes, and modification dates
- Function and class signatures (NOT implementations)
- Import statements
- Target size: 10-50KB (lightweight, not full code)

This enables testing of context reduction strategies using the codebase-expert concept.
"""

import os
import json
import ast
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class CodebaseIndexer:
    """Generates lightweight metadata index of codebase"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.index: Dict[str, Any] = {
            "generated_at": datetime.now().isoformat(),
            "root_directory": str(self.root_dir.absolute()),
            "files": [],
            "summary": {}
        }

    def should_index_file(self, file_path: Path) -> bool:
        """Determine if a file should be indexed"""
        # Only index source code files
        valid_extensions = {".py", ".ts", ".tsx", ".js", ".jsx"}
        if file_path.suffix not in valid_extensions:
            return False

        # Skip common ignore patterns
        ignore_patterns = [
            "node_modules",
            ".venv",
            "venv",
            "__pycache__",
            ".git",
            "dist",
            "build",
            ".next",
            "coverage",
            ".pytest_cache"
        ]

        for pattern in ignore_patterns:
            if pattern in str(file_path):
                return False

        return True

    def extract_python_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from Python files using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source)

            imports = []
            functions = []
            classes = []

            for node in tree.body:
                # Extract imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

                # Extract function signatures
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    params = [arg.arg for arg in node.args.args]
                    functions.append({
                        "name": node.name,
                        "parameters": params,
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })

                # Extract class signatures
                elif isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            params = [arg.arg for arg in item.args.args]
                            methods.append({
                                "name": item.name,
                                "parameters": params
                            })
                    classes.append({
                        "name": node.name,
                        "methods": methods
                    })

            return {
                "imports": imports,
                "functions": functions,
                "classes": classes
            }

        except Exception as e:
            return {"error": str(e)}

    def extract_typescript_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract basic metadata from TypeScript/JavaScript files"""
        # For TypeScript, we do basic text analysis since full AST parsing
        # would require additional dependencies
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            imports = []
            exports = []

            # Extract import statements (simple regex-like approach)
            for line in content.split('\n'):
                stripped = line.strip()
                if stripped.startswith('import '):
                    imports.append(stripped[:100])  # Truncate long imports
                elif stripped.startswith('export '):
                    exports.append(stripped[:100])

            return {
                "imports": imports[:20],  # Limit to first 20 imports
                "exports": exports[:20],
                "note": "Basic text analysis - not full AST parsing"
            }

        except Exception as e:
            return {"error": str(e)}

    def index_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Index a single file"""
        if not self.should_index_file(file_path):
            return None

        try:
            stats = file_path.stat()
            relative_path = file_path.relative_to(self.root_dir)

            file_info = {
                "path": str(relative_path),
                "size_bytes": stats.st_size,
                "modified_at": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                "extension": file_path.suffix
            }

            # Extract code metadata based on file type
            if file_path.suffix == ".py":
                file_info["metadata"] = self.extract_python_metadata(file_path)
            elif file_path.suffix in {".ts", ".tsx", ".js", ".jsx"}:
                file_info["metadata"] = self.extract_typescript_metadata(file_path)

            return file_info

        except Exception as e:
            print(f"Warning: Could not index {file_path}: {e}")
            return None

    def generate_index(self):
        """Generate the complete codebase index"""
        print(f"Indexing codebase in: {self.root_dir}")

        file_count = 0
        total_size = 0

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file():
                file_info = self.index_file(file_path)
                if file_info:
                    self.index["files"].append(file_info)
                    file_count += 1
                    total_size += file_info["size_bytes"]

        # Add summary
        self.index["summary"] = {
            "total_files_indexed": file_count,
            "total_source_bytes": total_size,
            "file_types": self._count_file_types()
        }

        print(f"✅ Indexed {file_count} files")

    def _count_file_types(self) -> Dict[str, int]:
        """Count files by extension"""
        counts: Dict[str, int] = {}
        for file_info in self.index["files"]:
            ext = file_info["extension"]
            counts[ext] = counts.get(ext, 0) + 1
        return counts

    def save_index(self, output_path: str = ".codebase_index.json"):
        """Save index to JSON file"""
        with open(output_path, "w") as f:
            json.dump(self.index, f, indent=2)

        # Check file size
        size_kb = Path(output_path).stat().st_size / 1024
        print(f"📝 Index saved to: {output_path}")
        print(f"📊 Index size: {size_kb:.1f} KB")

        if size_kb > 50:
            print("⚠️  Warning: Index size exceeds 50KB target")

        return size_kb


def main():
    """Main entry point"""
    print("Generating codebase index...")
    print()

    indexer = CodebaseIndexer()
    indexer.generate_index()
    size_kb = indexer.save_index(".codebase_index.json")

    print()
    print(f"Summary:")
    print(f"  - Files indexed: {indexer.index['summary']['total_files_indexed']}")
    print(f"  - File types: {', '.join(indexer.index['summary']['file_types'].keys())}")
    print(f"  - Index size: {size_kb:.1f} KB")

    if 10 <= size_kb <= 50:
        print("✅ Index size within target range (10-50KB)")
    elif size_kb < 10:
        print("ℹ️  Index size below 10KB (acceptable)")
    else:
        print("⚠️  Index size exceeds 50KB target")


if __name__ == "__main__":
    main()
