#!/usr/bin/env python3
"""
Markdown to DOCX conversion service
Provides common functionality for converting Markdown to DOCX format
"""

from pathlib import Path

from scripts.utils.markdown_utils import get_md_text
from scripts.utils.pandoc_utils import pandoc_convert_file


def convert_md_to_docx(
    md_text: str, output_path: Path, template_path: Path | None = None, is_strip_wrapper: bool = False
) -> None:
    """
    Convert Markdown text to DOCX format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output DOCX file
        template_path: Optional path to DOCX template file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Prepare pandoc arguments
    extra_args = []
    if template_path and template_path.exists():
        extra_args.append(f"--reference-doc={template_path}")

    # Convert to DOCX - use pandoc_convert_file with temporary file since convert_text doesn't work for DOCX
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as temp_md_file:
        temp_md_file.write(processed_md)
        temp_md_file_path = temp_md_file.name

    try:
        # Convert using pandoc_convert_file
        pandoc_convert_file(
            source_file=temp_md_file_path,
            input_format="markdown",
            dest_format="docx",
            outputfile=str(output_path),
            extra_args=extra_args,
        )
    finally:
        # Clean up temporary file
        import os

        os.unlink(temp_md_file_path)


def get_default_template(script_dir: Path) -> Path | None:
    """
    Get the default DOCX template path

    Args:
        script_dir: Directory of the calling script

    Returns:
        Optional[Path]: Path to default template if it exists, None otherwise
    """
    default_template = script_dir.parent / "assets" / "template" / "docx_template.docx"
    return default_template if default_template.exists() else None
