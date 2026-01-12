#!/usr/bin/env python3
"""
Markdown to JSON converter
Converts Markdown tables to JSON or JSONL format
"""

import argparse
import sys
from pathlib import Path
from enum import StrEnum

# Import shared utility functions
from utils.utils import get_md_text, parse_md_to_tables


class JsonOutputStyle(StrEnum):
    JSONL = "jsonl"
    JSON_ARRAY = "json_array"


def get_json_styles(output_style: str) -> tuple[int, bool]:
    """
    Get JSON format parameters
    :return: indent, object_per_line
    """
    match output_style:
        case JsonOutputStyle.JSONL:
            return 0, True
        case _:
            return 0, True


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown tables to JSON or JSONL format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output JSON file path'
    )
    parser.add_argument(
        '--style',
        choices=['jsonl', 'json_array'],
        default='jsonl',
        help='JSON output style (default: jsonl)'
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

    # Convert to JSON
    output_path = Path(args.output)
    try:
        for i, table in enumerate(tables):
            indent, object_per_line = get_json_styles(args.style)
            json_str = table.to_json(
                index=False,
                orient='records',
                force_ascii=False,
                indent=indent,
                lines=object_per_line
            )

            # Determine output file name
            if len(tables) > 1:
                output_file = output_path.parent / f"{output_path.stem}_{i + 1}.json"
            else:
                output_file = output_path

            # Write to file
            output_file.write_text(json_str, encoding='utf-8')
            print(f"Successfully converted to {output_file}")

    except Exception as e:
        print(f"Error: Failed to convert to JSON - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
