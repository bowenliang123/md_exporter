#!/usr/bin/env python3
"""
Markdown to HTML text converter
Converts Markdown text to HTML and outputs to stdout
"""

import argparse
import sys

from pypandoc import convert_text


from utils.utils import get_md_text


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to HTML and output to stdout',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )

    args = parser.parse_args()

    # Read input
    input_path = args.input
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        md_text = args.input

    # Process Markdown text
    try:
        md_text = get_md_text(md_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to HTML
    try:
        html_str = convert_text(md_text, format="markdown", to="html").decode("utf-8")
        print(html_str)
    except Exception as e:
        print(f"Error: Failed to convert to HTML - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
