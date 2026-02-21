#!/usr/bin/env python3
"""
Markdown to PNG converter
Converts Markdown text to PNG images
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_png import convert_md_to_png
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to PNG images", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output PNG file path or directory path")
    parser.add_argument("--compress", action="store_true", help="Compress all PNG images into a ZIP file")
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to PNG
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_png(md_text, output_path, args.compress, args.strip_wrapper)
        logger.info(f"Successfully processed {len(created_files)} files")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
