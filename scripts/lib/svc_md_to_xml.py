#!/usr/bin/env python3
"""
MdToXml service
"""

from typing import Optional, List
from pathlib import Path

import markdown
from lxml import html, etree


def convert_md_to_xml(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> Path:
    """
    Convert Markdown text to XML format
    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output XML file
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        Path to the created XML file
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    from utils.utils import get_md_text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)
    
    # Convert to XML
    try:
        html_str = markdown.markdown(text=processed_md, extensions=["extra", "toc"])
        xml_element = html.fromstring(html_str)
        result_file_bytes = etree.tostring(
            element_or_tree=xml_element,
            xml_declaration=True,
            pretty_print=True,
            encoding="UTF-8"
        )

        output_path.write_bytes(result_file_bytes)
        return output_path
    except Exception as e:
        raise Exception(f"Failed to convert Markdown to XML: {e}")


class MarkdownToXmlService:
    """
    Service class for converting Markdown to XML
    """
    
    @staticmethod
    def convert(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> Path:
        """
        Convert Markdown text to XML format
        Args:
            md_text: Markdown text to convert
            output_path: Path to save the output XML file
            is_strip_wrapper: Whether to remove code block wrapper if present
        Returns:
            Path to the created XML file
        """
        return convert_md_to_xml(md_text, output_path, is_strip_wrapper)
