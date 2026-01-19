#!/usr/bin/env python3
"""
Markdown to XLSX converter
Converts Markdown tables to XLSX format
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

from scripts.services.svc_md_to_xlsx import convert_md_to_xlsx  # noqa: E402
from scripts.utils.logger_utils import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown tables to XLSX format", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output XLSX file path")
    parser.add_argument(
        "--force-text", action="store_true", default=True, help="Convert cell values to text type (default: True)"
    )
    parser.add_argument("--strip-wrapper", action="store_true", help="Remove code block wrapper if present")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to XLSX
    output_path = Path(args.output)
    try:
        convert_md_to_xlsx(md_text, output_path, args.strip_wrapper, args.force_text)
        logger.info(f"Successfully converted to {output_path}")
    except ValueError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to convert to XLSX - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
