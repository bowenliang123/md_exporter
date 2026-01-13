#!/usr/bin/env python3
"""
Markdown to HTML converter
Converts Markdown text to HTML format
"""

import argparse
import sys
from pathlib import Path

# Import shared utility functions
from services.svc_md_to_html import convert_md_to_html


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to HTML format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output HTML file path'
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

    # Convert to HTML
    output_path = Path(args.output)
    try:
        convert_md_to_html(md_text, output_path, args.strip_wrapper)
        print(f"Successfully converted to {output_path}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to convert to HTML - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
