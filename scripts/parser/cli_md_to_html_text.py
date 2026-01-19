#!/usr/bin/env python3
"""
Markdown to HTML text converter
Converts Markdown text to HTML and outputs to stdout
"""

import argparse
import sys
from pathlib import Path

# Add the scripts directory and parent directory to Python path to fix import issues
script_dir = str(Path(__file__).resolve().parent)
parent_dir = str(Path(__file__).resolve().parent.parent)

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from scripts.services.svc_md_to_html_text import convert_md_to_html_text  # noqa: E402
from scripts.utils.logger_utils import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to HTML and output to stdout",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input Markdown file path")

    args = parser.parse_args()

    # Read input
    input_path = args.input
    try:
        with open(input_path, encoding="utf-8") as f:
            md_text = f.read()
    except FileNotFoundError:
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)

    # Convert to HTML
    try:
        html_str = convert_md_to_html_text(md_text)
        print(html_str)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
