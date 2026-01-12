#!/usr/bin/env python3
"""
Markdown to CSV converter
Converts Markdown tables to CSV format
"""

import argparse
import sys
from pathlib import Path

# Import shared utility functions
from lib.svc_md_to_csv import convert_md_to_csv


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown tables to CSV format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output CSV file path'
    )
    parser.add_argument(
        '--strip-wrapper',
        action='store_true',
        help='Remove code block wrapper if present'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if input_path.exists():
        md_text = input_path.read_text(encoding='utf-8')
    else:
        md_text = args.input

    # Convert to CSV
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_csv(md_text, output_path, args.strip_wrapper)
        for file_path in created_files:
            print(f"Successfully converted to {file_path}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
