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

from services.svc_md_to_json import convert_md_to_json


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

    # Convert to JSON
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_json(md_text, output_path, args.style, args.strip_wrapper)
        for file_path in created_files:
            print(f"Successfully converted to {file_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
