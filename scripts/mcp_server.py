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

from scripts.mcp_tools.registry import get_all_tool_definitions, get_tool_class
from scripts.utils.logger_utils import get_logger

logger = get_logger(__name__)

# Create MCP server instance
app = Server("md-exporter")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available markdown conversion tools"""
    return get_all_tool_definitions()


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested markdown conversion tool"""

    try:
        tool_class = get_tool_class(name)
        if tool_class:
            return await tool_class.execute(arguments)
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
