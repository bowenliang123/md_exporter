#!/usr/bin/env python3
"""
MCP Server for Markdown Exporter
Exposes markdown conversion tools via Model Context Protocol
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_codeblock import convert_md_to_codeblock
from scripts.services.svc_md_to_csv import convert_md_to_csv
from scripts.services.svc_md_to_docx import convert_md_to_docx
from scripts.services.svc_md_to_html import convert_md_to_html
from scripts.services.svc_md_to_html_text import convert_md_to_html_text
from scripts.services.svc_md_to_json import convert_md_to_json
from scripts.services.svc_md_to_latex import convert_md_to_latex
from scripts.services.svc_md_to_linked_image import convert_md_to_linked_image
from scripts.services.svc_md_to_md import convert_md_to_md
from scripts.services.svc_md_to_pptx import convert_md_to_pptx
from scripts.services.svc_md_to_xlsx import convert_md_to_xlsx
from scripts.services.svc_md_to_xml import convert_md_to_xml
from scripts.utils.logger_utils import get_logger

logger = get_logger(__name__)

# Create MCP server instance
app = Server("md-exporter")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available markdown conversion tools"""
    return [
        Tool(
            name="md_to_docx",
            description="Convert Markdown text to DOCX (Word document) format. Supports custom templates for styling.",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text to convert"},
                    "output_path": {"type": "string", "description": "Output file path for the DOCX file"},
                    "template_path": {
                        "type": "string",
                        "description": "Optional path to DOCX template file for custom styling",
                    },
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper (```) if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_html",
            description="Convert Markdown text to HTML file format",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text to convert"},
                    "output_path": {"type": "string", "description": "Output file path for the HTML file"},
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_html_text",
            description="Convert Markdown text to HTML string (returns HTML content as text)",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text to convert"},
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text"],
            },
        ),
        Tool(
            name="md_to_md",
            description="Save Markdown text to a .md file",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text to save"},
                    "output_path": {"type": "string", "description": "Output file path for the MD file"},
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_pptx",
            description=(
                "Convert Markdown text to PPTX (PowerPoint) format. "
                "Input must follow Pandoc slide show syntax. Supports custom templates."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text in Pandoc slide show format"},
                    "output_path": {"type": "string", "description": "Output file path for the PPTX file"},
                    "template_path": {
                        "type": "string",
                        "description": "Optional path to PPTX template file for custom styling",
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_xlsx",
            description="Convert Markdown tables to XLSX (Excel) format. Supports multiple tables as separate sheets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing tables"},
                    "output_path": {"type": "string", "description": "Output file path for the XLSX file"},
                    "force_text": {
                        "type": "boolean",
                        "description": "Force convert all cell values to text type",
                        "default": True,
                    },
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_csv",
            description="Convert Markdown tables to CSV format. Supports multiple tables (creates numbered files).",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing tables"},
                    "output_path": {"type": "string", "description": "Output file path for the CSV file(s)"},
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_json",
            description="Convert Markdown tables to JSON or JSONL format",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing tables"},
                    "output_path": {"type": "string", "description": "Output file path for the JSON file(s)"},
                    "style": {
                        "type": "string",
                        "enum": ["jsonl", "json_array"],
                        "description": (
                            "JSON output style: 'jsonl' (one object per line) or 'json_array' (single array)"
                        ),
                        "default": "jsonl",
                    },
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_xml",
            description="Convert Markdown tables to XML format",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing tables"},
                    "output_path": {"type": "string", "description": "Output file path for the XML file(s)"},
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_latex",
            description="Convert Markdown tables to LaTeX format",
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing tables"},
                    "output_path": {"type": "string", "description": "Output file path for the LaTeX file(s)"},
                    "strip_wrapper": {
                        "type": "boolean",
                        "description": "Remove code block wrapper if present",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_codeblock",
            description=(
                "Extract code blocks from Markdown and save them as individual files by language. "
                "Can optionally compress all files into a ZIP."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing code blocks"},
                    "output_path": {
                        "type": "string",
                        "description": "Output directory path or ZIP file path if compressing",
                    },
                    "compress": {
                        "type": "boolean",
                        "description": "Compress all code files into a single ZIP file",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
        Tool(
            name="md_to_linked_image",
            description=(
                "Extract and download all images referenced in Markdown image links. "
                "Can optionally compress all images into a ZIP."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "md_text": {"type": "string", "description": "Markdown text containing image links"},
                    "output_path": {
                        "type": "string",
                        "description": "Output directory path or ZIP file path if compressing",
                    },
                    "compress": {
                        "type": "boolean",
                        "description": "Compress all images into a single ZIP file",
                        "default": False,
                    },
                },
                "required": ["md_text", "output_path"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested markdown conversion tool"""

    try:
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        strip_wrapper = arguments.get("strip_wrapper", False)

        if name == "md_to_docx":
            template_path = arguments.get("template_path")
            template = Path(template_path) if template_path else None
            convert_md_to_docx(md_text, output_path, template_path=template, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to DOCX: {output_path}")]

        elif name == "md_to_html":
            convert_md_to_html(md_text, output_path, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to HTML: {output_path}")]

        elif name == "md_to_html_text":
            html_text = convert_md_to_html_text(md_text, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=html_text)]

        elif name == "md_to_md":
            convert_md_to_md(md_text, output_path)
            return [TextContent(type="text", text=f"Successfully saved Markdown to: {output_path}")]

        elif name == "md_to_pptx":
            template_path = arguments.get("template_path")
            template = Path(template_path) if template_path else None
            convert_md_to_pptx(md_text, output_path, template_path=template)
            return [TextContent(type="text", text=f"Successfully converted Markdown to PPTX: {output_path}")]

        elif name == "md_to_xlsx":
            force_text = arguments.get("force_text", True)
            convert_md_to_xlsx(md_text, output_path, force_text_value=force_text, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to XLSX: {output_path}")]

        elif name == "md_to_csv":
            convert_md_to_csv(md_text, output_path, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to CSV: {output_path}")]

        elif name == "md_to_json":
            style = arguments.get("style", "jsonl")
            convert_md_to_json(md_text, output_path, style=style, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to JSON: {output_path}")]

        elif name == "md_to_xml":
            convert_md_to_xml(md_text, output_path, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to XML: {output_path}")]

        elif name == "md_to_latex":
            convert_md_to_latex(md_text, output_path, is_strip_wrapper=strip_wrapper)
            return [TextContent(type="text", text=f"Successfully converted Markdown to LaTeX: {output_path}")]

        elif name == "md_to_codeblock":
            compress = arguments.get("compress", False)
            convert_md_to_codeblock(md_text, output_path, is_compress=compress)
            return [TextContent(type="text", text=f"Successfully extracted code blocks to: {output_path}")]

        elif name == "md_to_linked_image":
            compress = arguments.get("compress", False)
            convert_md_to_linked_image(md_text, output_path, is_compress=compress)
            return [TextContent(type="text", text=f"Successfully downloaded images to: {output_path}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
