#!/usr/bin/env python3
"""
Markdown to PDF converter
Converts Markdown text to PDF format
"""

import argparse
import sys
from pathlib import Path

from xhtml2pdf import pisa

# Import shared utility functions
from utils.utils import get_md_text, convert_markdown_to_html, contains_chinese, contains_japanese


def convert_to_html_with_font_support(md_text: str) -> str:
    """Convert Markdown to HTML and add Chinese/Japanese font support"""
    html_str = convert_markdown_to_html(md_text)

    if not contains_chinese(md_text) and not contains_japanese(md_text):
        return html_str

    # Add Chinese/Japanese font CSS
    font_families = ",".join([
        "Sans-serif",
        "STSong-Light",
        "MSung-Light",
        "HeiseiMin-W3",
    ])
    css_style = f"""
    <style>
        html {{
            -pdf-word-wrap: CJK;
            font-family: "{font_families}"; 
        }}
    </style>
    """

    result = f"""
    {css_style}
    {html_str}
    """
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to PDF format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output PDF file path'
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

    # Convert to HTML
    try:
        html_str = convert_to_html_with_font_support(md_text)
    except Exception as e:
        print(f"Error: Failed to convert to HTML - {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to PDF
    output_path = Path(args.output)
    try:
        result_file_bytes = pisa.CreatePDF(
            src=html_str,
            dest_bytes=True,
            encoding="utf-8",
            capacity=400 * 1024 * 1024,
        )
        
        output_path.write_bytes(result_file_bytes)
        print(f"Successfully converted to {output_path}")
    except Exception as e:
        print(f"Error: Failed to convert to PDF - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
