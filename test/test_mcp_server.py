#!/usr/bin/env python3
"""
Simple test to verify MCP server can be loaded and tools are registered
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.mcp_server import app


def test_mcp_server_initialization():
    """Test that the MCP server is properly initialized"""
    assert app is not None
    assert app.name == "md-exporter"
    print("✓ MCP server initialized correctly")


async def test_list_tools():
    """Test that list_tools returns expected tools"""
    # Get the list of registered tools
    try:
        # The Server object stores request handlers, let's check if we can get tools
        tools = []
        
        # Try to call list_tools through the server's protocol
        # For testing, we'll just verify the handlers are set up
        if hasattr(app, '_request_handlers'):
            print(f"✓ Request handlers registered: {len(app._request_handlers)}")
        
        # Since we decorated with @app.list_tools(), the function should be registered
        # Let's try to import and call it directly
        from scripts import mcp_server
        tools = await mcp_server.list_tools()
        
        assert len(tools) > 0, "No tools returned"
        print(f"✓ {len(tools)} tools available")

        # Verify some expected tools
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "md_to_docx",
            "md_to_html",
            "md_to_pptx",
            "md_to_xlsx",
            "md_to_csv",
            "md_to_json",
        ]

        for expected_tool in expected_tools:
            assert expected_tool in tool_names, f"Expected tool {expected_tool} not found"

        print(f"✓ All expected tools are registered: {', '.join(expected_tools)}")
        print(f"  Full tool list: {', '.join(tool_names)}")
        
    except Exception as e:
        print(f"Error in test: {e}")
        raise


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing MCP Server")
    print("=" * 60)

    try:
        test_mcp_server_initialization()
        await test_list_tools()
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
