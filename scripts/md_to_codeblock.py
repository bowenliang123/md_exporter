#!/usr/bin/env python3
"""
Markdown codeblocks extractor
Extracts code blocks from Markdown and saves them as files
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

# Import shared utility functions
from utils.utils import get_md_text


class CodeBlock:
    def __init__(self, lang_type: str, code: str):
        self.lang_type = lang_type
        self.code = code

    @property
    def code_bytes(self) -> bytes:
        return self.code.encode("utf-8")


MIME_TYPE_MAP = {
    "css": "text/css",
    "csv": "text/csv",
    "python": "text/x-python",
    "json": "application/json",
    "javascript": "text/javascript",
    "bash": "application/x-sh",
    "sh": "application/x-sh",
    "svg": "image/svg+xml",
    "xml": "text/xml",
    "html": "text/html",
    "ruby": "text/x-ruby",
    "markdown": "text/markdown",
    "yaml": "text/yaml",
    "php": "application/x-httpd-php",
    "java": "text/x-java-source",
}

SUFFIX_MAP = {
    "css": ".css",
    "csv": ".csv",
    "python": ".py",
    "json": ".json",
    "javascript": ".js",
    "bash": ".sh",
    "sh": ".sh",
    "svg": ".svg",
    "xml": ".xml",
    "html": ".html",
    "markdown": ".md",
    "yaml": ".yaml",
    "ruby": ".rb",
    "php": ".php",
    "java": ".java",
}


def extract_code_blocks(text: str) -> list[CodeBlock]:
    """Extract code blocks"""
    code_blocks: list[CodeBlock] = []
    pattern = re.compile(r'```([a-zA-Z0-9\+#\-_]*)\s*\n(.*?)\n```', re.DOTALL)

    for match in pattern.finditer(text):
        lang_type = match.group(1).strip() or 'text'
        code_content = match.group(2).strip()
        code_blocks.append(CodeBlock(lang_type, code_content))

    return code_blocks


def get_mime_type(lang_type: str) -> str:
    """Get MIME type"""
    return MIME_TYPE_MAP.get(lang_type.lower(), "text/plain")


def get_suffix_by_language(lang_type: str) -> str:
    """Get file suffix by language type"""
    return SUFFIX_MAP.get(lang_type.lower(), ".txt")


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

    # Process Markdown text
    try:
        md_text = get_md_text(md_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract code blocks
    code_blocks = extract_code_blocks(md_text)
    
    if not code_blocks:
        print("Warning: No code blocks found in the input text", file=sys.stderr)
        sys.exit(0)

    output_path = Path(args.output)

    if args.compress:
        # Compress into ZIP file
        try:
            with NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file, \
                    zipfile.ZipFile(temp_zip_file.name, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                for idx, code_block in enumerate(code_blocks, 1):
                    suffix = get_suffix_by_language(code_block.lang_type)
                    with NamedTemporaryFile(prefix=f"code_{idx}", suffix=suffix, delete=True) as temp_file:
                        temp_file.write(code_block.code_bytes)
                        temp_file.flush()
                        zip_file.write(temp_file.name, arcname=f"code_{idx}{suffix}")
                zip_file.close()

                output_path.write_bytes(Path(zip_file.filename).read_bytes())
            
            print(f"Successfully created ZIP file with {len(code_blocks)} code blocks: {output_path}")
        except Exception as e:
            print(f"Error: Failed to create ZIP file - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Save as separate files
        try:
            # If output path is directory, create directory
            if output_path.suffix == '':
                output_path.mkdir(parents=True, exist_ok=True)
                base_path = output_path
            else:
                # If output path is file, use parent directory as base path
                base_path = output_path.parent

            for index, code_block in enumerate(code_blocks):
                suffix = get_suffix_by_language(code_block.lang_type)
                if len(code_blocks) > 1:
                    file_path = base_path / f"{output_path.stem}_{index + 1}{suffix}"
                else:
                    file_path = output_path if output_path.suffix else base_path / f"{output_path.name}{suffix}"

                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(code_block.code_bytes)
                print(f"Successfully saved code block to {file_path}")

        except Exception as e:
            print(f"Error: Failed to save code blocks - {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
