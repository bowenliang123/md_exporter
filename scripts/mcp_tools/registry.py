"""
Tool Registry
Aggregates all MCP tool definitions
"""

from mcp.types import Tool

from scripts.mcp_tools.tool_md_to_codeblock import MdToCodeblockTool
from scripts.mcp_tools.tool_md_to_csv import MdToCsvTool
from scripts.mcp_tools.tool_md_to_docx import MdToDocxTool
from scripts.mcp_tools.tool_md_to_html import MdToHtmlTool
from scripts.mcp_tools.tool_md_to_html_text import MdToHtmlTextTool
from scripts.mcp_tools.tool_md_to_json import MdToJsonTool
from scripts.mcp_tools.tool_md_to_latex import MdToLatexTool
from scripts.mcp_tools.tool_md_to_linked_image import MdToLinkedImageTool
from scripts.mcp_tools.tool_md_to_md import MdToMdTool
from scripts.mcp_tools.tool_md_to_pptx import MdToPptxTool
from scripts.mcp_tools.tool_md_to_xlsx import MdToXlsxTool
from scripts.mcp_tools.tool_md_to_xml import MdToXmlTool

# Registry of all available tools
TOOL_CLASSES = [
    MdToDocxTool,
    MdToHtmlTool,
    MdToHtmlTextTool,
    MdToMdTool,
    MdToPptxTool,
    MdToXlsxTool,
    MdToCsvTool,
    MdToJsonTool,
    MdToXmlTool,
    MdToLatexTool,
    MdToCodeblockTool,
    MdToLinkedImageTool,
]

# Create a mapping from tool name to tool class
TOOL_MAP = {tool_class.get_tool_definition().name: tool_class for tool_class in TOOL_CLASSES}


def get_all_tool_definitions() -> list[Tool]:
    """Get all tool definitions"""
    return [tool_class.get_tool_definition() for tool_class in TOOL_CLASSES]


def get_tool_class(tool_name: str):
    """Get tool class by name"""
    return TOOL_MAP.get(tool_name)
