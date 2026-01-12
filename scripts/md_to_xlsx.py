#!/usr/bin/env python3
"""
Markdown to XLSX converter
Converts Markdown tables to XLSX format
"""

import argparse
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd

# Import shared utility functions
from utils.utils import get_md_text, parse_md_to_tables, SUGGESTED_SHEET_NAME


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown tables to XLSX format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output XLSX file path'
    )
    parser.add_argument(
        '--force-text',
        action='store_true',
        default=True,
        help='Convert cell values to text type (default: True)'
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
        tables = parse_md_to_tables(md_text, force_value_to_str=args.force_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to XLSX
    output_path = Path(args.output)
    try:
        with NamedTemporaryFile(suffix=".xlsx", delete=True) as temp_xlsx_file:
            with pd.ExcelWriter(temp_xlsx_file, engine='openpyxl') as writer:
                for i, table in enumerate(tables):
                    sheet_name = table.attrs.get(SUGGESTED_SHEET_NAME, f"Sheet{i + 1}")
                    table.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='')
                    # Auto-fit column width
                    if hasattr(writer.sheets[sheet_name], 'autofit'):
                        writer.sheets[sheet_name].autofit(max_width=200)

            # Read temp file and write to target
            temp_path = Path(temp_xlsx_file.name)
            output_path.write_bytes(temp_path.read_bytes())
        
        print(f"Successfully converted to {output_path}")
    except Exception as e:
        print(f"Error: Failed to convert to XLSX - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
