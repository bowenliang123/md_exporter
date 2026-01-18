#!/usr/bin/env python3
"""
Markdown to PNG converter
Converts Markdown text to PNG images
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

from services.svc_md_to_png import convert_md_to_png  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to PNG images',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path'
    )
    parser.add_argument(
        'output',
        help='Output PNG file path or directory path'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress all PNG images into a ZIP file'
    )
    parser.add_argument(
        '--strip-wrapper',
        action='store_true',
        help='Remove code block wrapper if present'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    md_text = input_path.read_text(encoding='utf-8')

    # Convert to PNG
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_png(md_text, output_path, args.compress, args.strip_wrapper)
        print(f"Successfully processed {len(created_files)} files")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
