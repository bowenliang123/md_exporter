"""MCP Tool: md_to_pptx"""

from pathlib import Path

from mcp.types import TextContent, Tool

from scripts.services.svc_md_to_pptx import convert_md_to_pptx


class MdToPptxTool:
    """Convert Markdown to PPTX tool"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        return Tool(
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
        )

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        md_text = arguments.get("md_text", "")
        output_path_str = arguments.get("output_path", "")
        output_path = Path(output_path_str) if output_path_str else None
        template_path = arguments.get("template_path")
        template = Path(template_path) if template_path else None

        convert_md_to_pptx(md_text, output_path, template_path=template)
        return [TextContent(type="text", text=f"Successfully converted Markdown to PPTX: {output_path}")]
