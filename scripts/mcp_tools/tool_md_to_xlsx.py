"""MCP Tool: md_to_xlsx"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_xlsx import convert_md_to_xlsx


class MdToXlsxTool:
    """Convert Markdown tables to XLSX tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        strip_wrapper = arguments.get("strip_wrapper", False)
        force_text = arguments.get("force_text", True)

        convert_md_to_xlsx(md_text, output_path, force_text_value=force_text, is_strip_wrapper=strip_wrapper)
        return [TextContent(type="text", text=f"Successfully converted Markdown to XLSX: {output_path}")]
