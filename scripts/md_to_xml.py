#!/usr/bin/env python3
"""
Markdown to XML converter
Converts Markdown text to XML format
"""

import argparse
import sys
from pathlib import Path

from lib.svc_md_to_xml import convert_md_to_xml


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to XML format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output XML file path'
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

    # Convert to XML
    output_path = Path(args.output)
    try:
        output_file = convert_md_to_xml(md_text, output_path, args.strip_wrapper)
        print(f"Successfully converted to {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
