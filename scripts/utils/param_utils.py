from typing import Any

from .markdown_utils import strip_markdown_wrapper
from .text_utils import normalize_line_breaks, remove_think_tags


def get_md_text_from_tool_params(
    tool_parameters: dict[str, Any],
    is_strip_wrapper: bool = False,
    is_remove_think_tag: bool = True,
    is_normalize_line_breaks: bool = True,
) -> str:
    md_text = tool_parameters.get("md_text")
    md_text = md_text.strip() if md_text else None
    if not md_text:
        raise ValueError("Empty input md_text")

    # remove think tag
    if is_remove_think_tag:
        md_text = remove_think_tags(md_text)

    if is_strip_wrapper:
        md_text = strip_markdown_wrapper(md_text)

    # line breaks normalization by auto conversion from `\n` to `\n`
    if is_normalize_line_breaks:
        md_text = normalize_line_breaks(md_text)

    return md_text


def get_param_value(tool_parameters: dict[str, Any], param_name: str, default_value: Any = None) -> Any:
    param_value = tool_parameters.get(param_name, default_value)
    if not param_value:
        raise ValueError(f"Empty input {param_name}")

    return param_value
