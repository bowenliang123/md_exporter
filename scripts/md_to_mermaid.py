#!/usr/bin/env python3
"""
Convert Markdown text to mermaid PNG files
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from pathlib import Path

from scripts.services.svc_md_to_mermaid import convert_md_to_mermaid, start_pre_installation


def main():
    """
    Main function
    """
    if len(sys.argv) < 2:
        print("Usage: python md_to_mermaid.py <markdown_file> [output_path] [--compress]")
        sys.exit(1)

    # Get input file path
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    # Read markdown text
    md_text = input_file.read_text()

    # Get output path
    output_path = Path("output")
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    # Check if compress flag is set
    compress = False
    if len(sys.argv) > 3 and sys.argv[3] == "--compress":
        compress = True

    try:
        # Convert markdown to mermaid PNG images
        created_files = convert_md_to_mermaid(md_text, output_path, compress=compress)
        print(f"Successfully created {len(created_files)} files:")
        for file_path in created_files:
            print(f"  - {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Start asynchronous pre-installation
    start_pre_installation()

    main()
