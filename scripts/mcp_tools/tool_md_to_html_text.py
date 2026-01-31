"""MCP Tool: md_to_html_text"""

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_html_text import convert_md_to_html_text


class MdToHtmlTextTool:
    """Convert Markdown to HTML text tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        strip_wrapper = arguments.get("strip_wrapper", False)

        html_text = convert_md_to_html_text(md_text, is_strip_wrapper=strip_wrapper)
        return [TextContent(type="text", text=html_text)]
