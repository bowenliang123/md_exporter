#!/usr/bin/env python3
"""
Markdown to PPTX converter
Converts Markdown text to PPTX format using md2pptx
"""

import argparse
import sys
from pathlib import Path

# Add the scripts directory to Python path to fix import issues
sys.path.insert(0, str(Path(__file__).resolve().parent))

from services.svc_md_to_pptx import convert_md_to_pptx


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to PPTX format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output PPTX file path'
    )
    parser.add_argument(
        '--template',
        help='Path to PPTX template file (optional)'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if input_path.exists():
        md_text = input_path.read_text(encoding='utf-8')
    else:
        md_text = args.input

    # Convert to PPTX
    output_path = Path(args.output)
    template_path = Path(args.template) if args.template else None
    try:
        output_file = convert_md_to_pptx(md_text, output_path, template_path)
        print(f"Successfully converted to {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
