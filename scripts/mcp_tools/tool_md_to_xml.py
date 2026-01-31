"""MCP Tool: md_to_xml"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_xml import convert_md_to_xml


class MdToXmlTool:
    """Convert Markdown tables to XML tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        strip_wrapper = arguments.get("strip_wrapper", False)

        convert_md_to_xml(md_text, output_path, is_strip_wrapper=strip_wrapper)
        return [TextContent(type="text", text=f"Successfully converted Markdown to XML: {output_path}")]
