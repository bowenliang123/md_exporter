"""
MCP Tools package
Contains individual tool definitions for the MCP server
"""

from mcp.types import TextContent, Tool


class MCPToolBase:
    """Base class for MCP tool definitions"""

    @staticmethod
    def get_tool_definition() -> Tool:
        """Return the MCP Tool definition with schema"""
        raise NotImplementedError("Subclass must implement get_tool_definition()")

    @staticmethod
    async def execute(arguments: dict) -> list[TextContent]:
        """Execute the tool with given arguments"""
        raise NotImplementedError("Subclass must implement execute()")
