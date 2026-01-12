#!/usr/bin/env python3
"""
Markdown to XML converter
Converts Markdown text to XML format
"""

import argparse
import sys
from pathlib import Path

import markdown
from lxml import html, etree


from utils.utils import get_md_text


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

    # Process Markdown text
    try:
        md_text = get_md_text(md_text, is_strip_wrapper=args.strip_wrapper)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to XML
    output_path = Path(args.output)
    try:
        html_str = markdown.markdown(text=md_text, extensions=["extra", "toc"])
        xml_element = html.fromstring(html_str)
        result_file_bytes = etree.tostring(
            element_or_tree=xml_element,
            xml_declaration=True,
            pretty_print=True,
            encoding="UTF-8"
        )

        output_path.write_bytes(result_file_bytes)
        print(f"Successfully converted to {output_path}")

    except Exception as e:
        print(f"Error: Failed to convert to XML - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
