#!/usr/bin/env python3
"""
MdToJson service
"""

from enum import StrEnum
from pathlib import Path

from scripts.utils.markdown_utils import get_md_text
from scripts.utils.table_utils import parse_md_to_tables


class JsonOutputStyle(StrEnum):
    JSONL = "jsonl"
    JSON_ARRAY = "json_array"


def get_json_styles(output_style: str) -> tuple[int, bool]:
    """
    Get JSON format parameters
    :return: indent, object_per_line
    """
    match output_style:
        case JsonOutputStyle.JSON_ARRAY:
            return 0, False
        case JsonOutputStyle.JSONL:
            return 0, True
        case _:
            return 0, True


def convert_md_to_json(
    md_text: str, output_path: Path, style: str = "jsonl", is_strip_wrapper: bool = False
) -> list[Path]:
    """
    Convert Markdown tables to JSON or JSONL format
    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output JSON file
        style: JSON output style (jsonl or json_array)
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        List of paths to the created JSON files
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    # from scripts.utils.utils import get_md_text, parse_md_to_tables

    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Parse Markdown tables
    tables = parse_md_to_tables(processed_md)

    # Convert to JSON
    created_files = []
    for i, table in enumerate(tables):
        indent, object_per_line = get_json_styles(style)
        json_str = table.to_json(index=False, orient="records", force_ascii=False, indent=indent, lines=object_per_line)

        # Determine output file name
        if len(tables) > 1:
            output_file = output_path.parent / f"{output_path.stem}_{i + 1}.json"
        else:
            output_file = output_path

        # Write to file
        output_file.write_text(json_str, encoding="utf-8")
        created_files.append(output_file)

    return created_files
