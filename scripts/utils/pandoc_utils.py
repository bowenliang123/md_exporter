#!/usr/bin/env python3
"""
Pandoc utility functions
"""

from pypandoc import convert_file

DEFAULT_ENABLED_INPUT_EXTENSIONS = []
DEFAULT_DISABLED_INPUT_EXTENSIONS = [
    "blank_before_header", # https://pandoc.org/MANUAL.html#extension-blank_before_header
    "space_in_atx_header", # https://pandoc.org/MANUAL.html#extension-space_in_atx_header
]


def pandoc_convert_file(
    source_file: str,
    input_format: str,
    dest_format: str,
    outputfile: str,
    extra_args: list[str] = None,
    enabled_input_extensions: list[str] = DEFAULT_ENABLED_INPUT_EXTENSIONS,
    disabled_input_extensions: list[str] = DEFAULT_DISABLED_INPUT_EXTENSIONS,
) -> None:
    """
    Convert file using pandoc
    """
    extra_args = extra_args or []
    enabled = enabled_input_extensions or []
    disabled = disabled_input_extensions or []
    
    # Build format string with extensions
    if not input_format:
        raise ValueError("input_format must be specified")
    format_w_extensions = input_format
    if enabled:
        format_w_extensions += "+" + "+".join(enabled)
    if disabled:
        format_w_extensions += "-" + "-".join(disabled)

    convert_file(
        source_file=source_file,
        format=format_w_extensions,
        to=dest_format,
        outputfile=outputfile,
        extra_args=extra_args,
    )
