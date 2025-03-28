#!/usr/bin/env python3
"""
Documentation Generator for Python Components

This script generates API documentation for all Python components in the Cognitive Workspace
monorepo using Sphinx and aggregates them with the TypeScript documentation.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent.parent
PYTHON_PACKAGES = [
    "backend",
]
OUTPUT_DIR = REPO_ROOT / "docs-dist" / "python"

def generate_python_docs():
    """Generate documentation for all Python packages."""
    print("Generating Python API documentation...")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for package in PYTHON_PACKAGES:
        package_path = REPO_ROOT / package
        if not package_path.exists():
            print(f"Package {package} not found, skipping...")
            continue

        print(f"Generating documentation for {package}...")

        # Generate documentation using Sphinx
        doc_output = OUTPUT_DIR / package
        os.makedirs(doc_output, exist_ok=True)

        try:
            # Initialize sphinx in the package directory if not already present
            sphinx_conf_path = package_path / "docs" / "conf.py"
            if not sphinx_conf_path.parent.exists():
                os.makedirs(sphinx_conf_path.parent, exist_ok=True)
                subprocess.run(
                    ["sphinx-quickstart", "--quiet", "--sep",
                     f"--project={package.capitalize()}",
                     "--author=Cognitive Workspace Team",
                     sphinx_conf_path.parent],
                    check=True
                )

                # Update conf.py to include autodoc and napoleon extensions
                with open(sphinx_conf_path, "r") as f:
                    conf_content = f.read()

                if "autodoc" not in conf_content:
                    with open(sphinx_conf_path, "w") as f:
                        extensions_line = "extensions = [\n    'sphinx.ext.autodoc',\n    'sphinx.ext.napoleon',\n    'sphinx.ext.viewcode',\n]"
                        conf_content = conf_content.replace("extensions = []", extensions_line)
                        f.write(conf_content)

            # Generate API documentation
            subprocess.run(
                ["sphinx-apidoc", "-o", str(package_path / "docs"),
                 str(package_path), "--force", "--separate"],
                check=True
            )

            # Build HTML documentation
            subprocess.run(
                ["sphinx-build", "-b", "html",
                 str(package_path / "docs"),
                 str(doc_output)],
                check=True
            )

            print(f"Documentation for {package} generated successfully in {doc_output}")

        except subprocess.CalledProcessError as e:
            print(f"Error generating documentation for {package}: {e}")

    print("Python API documentation generation complete!")

def create_index():
    """Create an index page that links to all documentation sets."""
    index_path = REPO_ROOT / "docs-dist" / "index.html"

    with open(index_path, "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cognitive Workspace Documentation</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #0366d6;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 10px;
        }
        h2 {
            margin-top: 30px;
            color: #24292e;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .doc-section {
            margin-bottom: 30px;
            padding: 15px;
            background-color: #f6f8fa;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Cognitive Workspace Documentation</h1>
    <p>Welcome to the unified documentation for the Cognitive Workspace project.</p>

    <div class="doc-section">
        <h2>TypeScript API Documentation</h2>
        <p>Documentation for all TypeScript packages and components.</p>
        <a href="./index.html">View TypeScript Documentation</a>
    </div>

    <div class="doc-section">
        <h2>Python API Documentation</h2>
        <p>Documentation for all Python packages and components.</p>
        <a href="./python/backend/index.html">View Backend API Documentation</a>
    </div>

    <div class="doc-section">
        <h2>Project Documentation</h2>
        <p>General project documentation, guides, and tutorials.</p>
        <a href="./docs/index.html">View Project Documentation</a>
    </div>

    <footer>
        <p>&copy; ${new Date().getFullYear()} Cognitive Workspace Team</p>
    </footer>
</body>
</html>
""")
    print(f"Created main index page at {index_path}")

if __name__ == "__main__":
    generate_python_docs()
    create_index()
    print("Documentation generation complete!")
