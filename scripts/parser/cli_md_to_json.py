#!/usr/bin/env python3
"""
Markdown to JSON converter
Converts Markdown tables to JSON or JSONL format
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

from scripts.services.svc_md_to_json import convert_md_to_json  # noqa: E402
from scripts.utils.logger_utils import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown tables to JSON or JSONL format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output JSON file path")
    parser.add_argument(
        "--style", choices=["jsonl", "json_array"], default="jsonl", help="JSON output style (default: jsonl)"
    )
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to JSON
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_json(md_text, output_path, args.style, args.strip_wrapper)
        for file_path in created_files:
            logger.info(f"Successfully converted to {file_path}")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
