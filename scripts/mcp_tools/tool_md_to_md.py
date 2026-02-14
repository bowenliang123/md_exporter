"""MCP Tool: md_to_md"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_md import convert_md_to_md


class MdToMdTool:
    """Save Markdown to file tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None

        convert_md_to_md(md_text, output_path)
        return [TextContent(type="text", text=f"Successfully saved Markdown to: {output_path}")]
