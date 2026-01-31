#!/usr/bin/env python3
"""
Integration test to verify MCP server can start and handle basic operations
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


async def test_tool_execution():
    """Test that we can execute a simple tool"""
    from scripts import mcp_server

    # Test md_to_html_text since it doesn't require file I/O
    test_md = "# Hello World\n\nThis is a **test**."

    try:
        result = await mcp_server.call_tool("md_to_html_text", {"md_text": test_md})

        assert len(result) > 0, "No result returned"
        assert result[0].type == "text", "Result should be text content"
        assert "Hello World" in result[0].text, "Output should contain original markdown content"
        assert "<h1>" in result[0].text or "<strong>" in result[0].text, "Output should be HTML"

        print("✓ md_to_html_text tool executed successfully")
        print(f"  Sample output: {result[0].text[:100]}...")

    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        raise


async def test_file_based_tool():
    """Test a tool that writes to a file"""
    from scripts import mcp_server

    test_md = "# Test Document\n\nThis is a test."

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as tmp:
        tmp_path = tmp.name

    try:
        result = await mcp_server.call_tool("md_to_md", {"md_text": test_md, "output_path": tmp_path})

        assert len(result) > 0, "No result returned"
        assert result[0].type == "text", "Result should be text content"
        assert "Successfully" in result[0].text, "Should indicate success"

        # Verify file was created
        output_file = Path(tmp_path)
        assert output_file.exists(), "Output file should exist"
        content = output_file.read_text()
        assert "Test Document" in content, "File should contain markdown content"

        print("✓ md_to_md tool executed successfully")
        print(f"  Output file: {tmp_path}")

        # Cleanup
        output_file.unlink()

    except Exception as e:
        print(f"❌ File-based tool execution failed: {e}")
        # Cleanup on error
        Path(tmp_path).unlink(missing_ok=True)
        raise


async def main():
    """Run integration tests"""
    print("=" * 60)
    print("MCP Server Integration Tests")
    print("=" * 60)

    try:
        await test_tool_execution()
        await test_file_based_tool()

        print("\n" + "=" * 60)
        print("✅ All integration tests passed!")
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
