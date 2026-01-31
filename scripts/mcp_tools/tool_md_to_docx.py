"""MCP Tool: md_to_docx"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_docx import convert_md_to_docx


class MdToDocxTool:
    """Convert Markdown to DOCX tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        strip_wrapper = arguments.get("strip_wrapper", False)
        template_path = arguments.get("template_path")
        template = Path(template_path) if template_path else None

        convert_md_to_docx(md_text, output_path, template_path=template, is_strip_wrapper=strip_wrapper)
        return [TextContent(type="text", text=f"Successfully converted Markdown to DOCX: {output_path}")]
