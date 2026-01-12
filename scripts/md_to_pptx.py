#!/usr/bin/env python3
"""
Markdown to PPTX converter
Converts Markdown text to PPTX format using md2pptx
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory, NamedTemporaryFile

# Import shared utility functions
from utils.utils import get_md_text


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

    # Process Markdown text
    try:
        md_text = get_md_text(md_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Check for disallowed macros
    if "``` run-python" in md_text:
        print("Error: The `run-python` macro of md2pptx is not allowed.", file=sys.stderr)
        sys.exit(1)

    # Get md2pptx directory path
    script_dir = Path(__file__).resolve().parent
    md2pptx_dir = script_dir / "md2pptx-6.1"
    
    if not md2pptx_dir.exists():
        print(f"Error: md2pptx directory not found: {md2pptx_dir}", file=sys.stderr)
        print("Please ensure md2pptx is properly installed.", file=sys.stderr)
        sys.exit(1)

    # Determine template file
    template_path = None
    if args.template:
        template_path = Path(args.template)
        if not template_path.exists():
            print(f"Error: Template file not found: {args.template}", file=sys.stderr)
            sys.exit(1)
    else:
        # Use default template
        default_template = script_dir / "template" / "Bowen Template.pptx"
        if default_template.exists():
            template_path = default_template

    # Convert to PPTX
    output_path = Path(args.output)
    try:
        with TemporaryDirectory() as temp_dir:
            # Prepare metadata
            metadata = f"tempDir: {temp_dir}\n"
            if template_path:
                metadata += f"template: {template_path}\n"
            metadata += "DeleteFirstSlide: yes\n"
            
            md_text = metadata + "\n" + md_text

            # Create temporary Markdown file
            with NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
                md_file.write(md_text)
                md_file_path = md_file.name

            # Run md2pptx
            md2pptx_script = md2pptx_dir / "md2pptx.py"
            cmd = [sys.executable, str(md2pptx_script), md_file_path, str(output_path)]

            try:
                result = subprocess.run(
                    cmd,
                    timeout=60,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"Error: md2pptx failed with return code {result.returncode}", file=sys.stderr)
                    print(f"stdout: {result.stdout}", file=sys.stderr)
                    print(f"stderr: {result.stderr}", file=sys.stderr)
                    sys.exit(1)
            finally:
                # Delete temporary file
                if os.path.exists(md_file_path):
                    os.unlink(md_file_path)

            print(f"Successfully converted to {output_path}")
    except subprocess.TimeoutExpired:
        print("Error: md2pptx execution timed out", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to convert to PPTX - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
