#!/usr/bin/env python3
"""
MdToPptx service
"""

import os
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from scripts.utils.markdown_utils import get_md_text


def convert_md_to_pptx(
    md_text: str, output_path: Path, template_path: Path | None = None, is_strip_wrapper: bool = False
) -> Path:
    """
    Convert Markdown text to PPTX format using md2pptx
    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output PPTX file
        template_path: Path to PPTX template file (optional)
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        Path to the created PPTX file
    Raises:
        ValueError: If input processing fails or disallowed macros are found
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Check for disallowed macros
    if "``` run-python" in processed_md:
        raise ValueError("The `run-python` macro of md2pptx is not allowed.")

    # Get md2pptx directory path
    script_dir = Path(__file__).resolve().parent.parent  # Go up two levels: scripts/lib -> scripts
    md2pptx_dir = script_dir / "md2pptx-6.1.1"

    if not md2pptx_dir.exists():
        raise Exception(f"md2pptx directory not found: {md2pptx_dir}. Please ensure md2pptx is properly installed.")

    # Determine template file
    final_template_path = template_path
    if not final_template_path:
        # Use default template
        default_template = script_dir.parent / "assets" / "template" / "pptx_template.pptx"
        if default_template.exists():
            final_template_path = default_template

    # Convert to PPTX
    try:
        with TemporaryDirectory() as temp_dir:
            # Prepare metadata
            metadata = f"tempDir: {temp_dir}\n"
            if final_template_path:
                metadata += f"template: {final_template_path}\n"
            metadata += "DeleteFirstSlide: yes\n"

            full_md_text = metadata + "\n" + processed_md

            # Create temporary Markdown file
            with NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as md_file:
                md_file.write(full_md_text)
                md_file_path = md_file.name

            # Run md2pptx
            md2pptx_script = md2pptx_dir / "md2pptx.py"
            cmd = [sys.executable, str(md2pptx_script), md_file_path, str(output_path)]

            try:
                result = subprocess.run(cmd, timeout=60, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(
                        f"md2pptx failed with return code {result.returncode}. stdout: {result.stdout}, stderr: {result.stderr}"
                    )
            finally:
                # Delete temporary file
                if os.path.exists(md_file_path):
                    os.unlink(md_file_path)

            return output_path
    except subprocess.TimeoutExpired:
        raise Exception("md2pptx execution timed out")
    except Exception as e:
        raise Exception(f"Failed to convert to PPTX: {e}")
