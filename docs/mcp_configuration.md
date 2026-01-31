# MCP Server Configuration Examples

This directory contains example configurations for using the Markdown Exporter MCP server with different MCP clients.

## Claude Desktop Configuration

### macOS
File location: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
File location: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration

```json
{
  "mcpServers": {
    "md-exporter": {
      "command": "python",
      "args": ["/absolute/path/to/md_exporter/scripts/mcp_server.py"]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/md_exporter` with the actual absolute path to your md_exporter installation.

## Available Tools

Once configured, you'll have access to these tools:

- `md_to_docx` - Convert Markdown to Word documents
- `md_to_html` - Convert Markdown to HTML files  
- `md_to_html_text` - Convert Markdown to HTML text string
- `md_to_md` - Save Markdown to file
- `md_to_pptx` - Convert Markdown to PowerPoint presentations
- `md_to_xlsx` - Convert Markdown tables to Excel spreadsheets
- `md_to_csv` - Convert Markdown tables to CSV
- `md_to_json` - Convert Markdown tables to JSON/JSONL
- `md_to_xml` - Convert Markdown tables to XML
- `md_to_latex` - Convert Markdown tables to LaTeX
- `md_to_codeblock` - Extract code blocks to files
- `md_to_linked_image` - Download images from Markdown
