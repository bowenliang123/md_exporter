"""MCP Tool: md_to_codeblock"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_codeblock import convert_md_to_codeblock


class MdToCodeblockTool:
    """Extract code blocks from Markdown tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        compress = arguments.get("compress", False)

        convert_md_to_codeblock(md_text, output_path, is_compress=compress)
        return [TextContent(type="text", text=f"Successfully extracted code blocks to: {output_path}")]
