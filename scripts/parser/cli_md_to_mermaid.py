#!/usr/bin/env python3
"""
Convert Markdown text to mermaid PNG files
"""

import sys
from pathlib import Path

# Add the scripts directory to Python path to fix import issues
script_dir = str(Path(__file__).resolve().parent)
parent_dir = str(Path(__file__).resolve().parent.parent)

if script_dir not in sys.path:
    sys.path.insert(0, script_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.svc_md_to_mermaid import convert_md_to_mermaid, start_pre_installation  # noqa: E402

from scripts.utils.logger_utils import get_logger  # noqa: E402

logger = get_logger(__name__)


def main():
    """
    Main function
    """
    if len(sys.argv) < 2:
        logger.info("Usage: python md_to_mermaid.py <markdown_file> [output_path] [--compress]")
        sys.exit(1)

    # Get input file path
    input_file = Path(sys.argv[1])
    if not input_file.exists():
        logger.error(f"Error: Input file not found: {input_file}")
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
        logger.info(f"Successfully created {len(created_files)} files:")
        for file_path in created_files:
            logger.info(f"  - {file_path}")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Start asynchronous pre-installation
    start_pre_installation()

    main()
