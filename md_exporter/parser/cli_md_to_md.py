#!/usr/bin/env python3
"""
Markdown to MD converter
Converts Markdown text to .md file
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_md import convert_md_to_md
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to .md file", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output MD file path")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to MD file
    output_path = Path(args.output)
    try:
        output_file = convert_md_to_md(md_text, output_path)
        logger.info(f"Successfully saved to {output_file}")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
