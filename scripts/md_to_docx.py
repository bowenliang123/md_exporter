#!/usr/bin/env python3
"""
Markdown to DOCX converter
Converts Markdown text to DOCX format
"""

import argparse
import sys
from pathlib import Path

from pypandoc import convert_file, convert_text

# Import shared utility functions
from utils.utils import get_md_text


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to DOCX format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output DOCX file path'
    )
    parser.add_argument(
        '--template',
        help='Path to DOCX template file (optional)'
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

    # Determine template file
    script_dir = Path(__file__).resolve().parent
    template_path = None
    if args.template:
        template_path = Path(args.template)
        if not template_path.exists():
            print(f"Error: Template file not found: {args.template}", file=sys.stderr)
            sys.exit(1)
    else:
        # Use default template
        default_template = script_dir / "template" / "docx_template.docx"
        if default_template.exists():
            template_path = default_template

    # Prepare pandoc arguments
    extra_args = []
    if template_path:
        extra_args.append(f"--reference-doc={template_path}")

    # Convert to DOCX
    output_path = Path(args.output)
    try:
        if extra_args:
            # Use template
            result = convert_text(
                md_text,
                format="markdown",
                to="docx",
                extra_args=extra_args
            )
            output_path.write_bytes(result)
        else:
            # No template
            result = convert_text(
                md_text,
                format="markdown",
                to="docx"
            )
            output_path.write_bytes(result)
        
        print(f"Successfully converted to {output_path}")
    except Exception as e:
        print(f"Error: Failed to convert to DOCX - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
