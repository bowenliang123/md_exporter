#!/usr/bin/env python3
"""
Markdown to PPTX converter
Converts Markdown text to PPTX format using md2pptx
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

from services.svc_md_to_pptx import convert_md_to_pptx  # noqa: E402


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to PPTX format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path'
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
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    md_text = input_path.read_text(encoding='utf-8')

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
