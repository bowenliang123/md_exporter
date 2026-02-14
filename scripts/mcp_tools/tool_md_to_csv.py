"""MCP Tool: md_to_csv"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_csv import convert_md_to_csv


class MdToCsvTool:
    """Convert Markdown tables to CSV tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        strip_wrapper = arguments.get("strip_wrapper", False)

        convert_md_to_csv(md_text, output_path, is_strip_wrapper=strip_wrapper)
        return [TextContent(type="text", text=f"Successfully converted Markdown to CSV: {output_path}")]
