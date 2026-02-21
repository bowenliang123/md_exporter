#!/usr/bin/env python3
"""
Markdown to IPYNB converter
Converts Markdown text to IPYNB format
"""

import argparse
import sys
from pathlib import Path

from ..services.svc_md_to_ipynb import convert_md_to_ipynb
from ..utils.logger_utils import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown text to IPYNB format", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output IPYNB file path")
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to IPYNB
    output_path = Path(args.output)
    try:
        convert_md_to_ipynb(md_text, output_path, args.strip_wrapper)
        logger.info(f"Successfully converted to {output_path}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to IPYNB - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
