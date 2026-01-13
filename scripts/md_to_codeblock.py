#!/usr/bin/env python3
"""
Markdown codeblocks extractor
Extracts code blocks from Markdown and saves them as files
"""

import argparse
import sys
from pathlib import Path

from services.svc_md_to_codeblock import convert_md_to_codeblock


def main():
    parser = argparse.ArgumentParser(
        description='Extract code blocks from Markdown and save as files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output file or directory path'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress all code blocks into a ZIP file'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if input_path.exists():
        md_text = input_path.read_text(encoding='utf-8')
    else:
        md_text = args.input

    # Convert to code blocks
    output_path = Path(args.output)
    try:
        created_files = convert_md_to_codeblock(md_text, output_path, args.compress)
        print(f"Successfully processed {len(created_files)} files")
    except ValueError as e:
        print(f"Warning: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
