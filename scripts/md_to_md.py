#!/usr/bin/env python3
"""
Markdown to MD file converter
Converts Markdown text to .md file
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

from services.svc_md_to_md import convert_md_to_md


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to .md file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output MD file path'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if input_path.exists():
        md_text = input_path.read_text(encoding='utf-8')
    else:
        md_text = args.input

    # Convert to MD file
    output_path = Path(args.output)
    try:
        output_file = convert_md_to_md(md_text, output_path)
        print(f"Successfully saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
