#!/usr/bin/env python3
"""
Markdown codeblocks extractor
Extracts code blocks from Markdown and saves them as files
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

from scripts.services.svc_md_to_codeblock import convert_md_to_codeblock  # noqa: E402
from scripts.utils.logger_utils import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Extract code blocks from Markdown and save as files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Input Markdown file path")
    parser.add_argument("output", help="Output file or directory path")
    parser.add_argument("--compress", action="store_true", help="Compress all code blocks into a ZIP file")

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)
    md_text = input_path.read_text(encoding="utf-8")

    # Convert to code blocks
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_codeblock(md_text, output_path, args.compress)
        logger.info(f"Successfully processed {len(created_files)} files")
    except ValueError as e:
        logger.warning(f"Warning: {e}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
