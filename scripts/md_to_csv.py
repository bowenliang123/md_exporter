#!/usr/bin/env python3
"""
Markdown to CSV converter
Converts Markdown tables to CSV format
"""

import argparse
import sys
from pathlib import Path

# Import shared utility functions
from utils.utils import get_md_text, parse_md_to_tables


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

    # Process Markdown text
    try:
        md_text = get_md_text(md_text, is_strip_wrapper=args.strip_wrapper)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse Markdown tables
    try:
        tables = parse_md_to_tables(md_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to CSV
    output_path = Path(args.output)
    for i, table in enumerate(tables):
        csv_str = table.to_csv(index=False, encoding="utf-8")
        
        # Determine output filename
        if len(tables) > 1:
            output_file = output_path.parent / f"{output_path.stem}_{i + 1}.csv"
        else:
            output_file = output_path
        
        # Write to file
        output_file.write_text(csv_str, encoding='utf-8')
        print(f"Successfully converted to {output_file}")


if __name__ == '__main__':
    main()
