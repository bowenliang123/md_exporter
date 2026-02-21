#!/usr/bin/env python3

import sys

from scripts.parser.cli_md_to_codeblock import main as md_to_codeblock_main
from scripts.parser.cli_md_to_csv import main as md_to_csv_main
from scripts.parser.cli_md_to_docx import main as md_to_docx_main
from scripts.parser.cli_md_to_html import main as md_to_html_main
from scripts.parser.cli_md_to_html_text import main as md_to_html_text_main
from scripts.parser.cli_md_to_ipynb import main as md_to_ipynb_main
from scripts.parser.cli_md_to_json import main as md_to_json_main
from scripts.parser.cli_md_to_latex import main as md_to_latex_main
from scripts.parser.cli_md_to_md import main as md_to_md_main
from scripts.parser.cli_md_to_pdf import main as md_to_pdf_main
from scripts.parser.cli_md_to_png import main as md_to_png_main
from scripts.parser.cli_md_to_pptx import main as md_to_pptx_main
from scripts.parser.cli_md_to_xlsx import main as md_to_xlsx_main
from scripts.parser.cli_md_to_xml import main as md_to_xml_main

# Mapping of subcommands to their main functions
SUBCOMMANDS = {
    "md_to_codeblock": md_to_codeblock_main,
    "md_to_csv": md_to_csv_main,
    "md_to_docx": md_to_docx_main,
    "md_to_html": md_to_html_main,
    "md_to_html_text": md_to_html_text_main,
    "md_to_ipynb": md_to_ipynb_main,
    "md_to_json": md_to_json_main,
    "md_to_latex": md_to_latex_main,
    "md_to_md": md_to_md_main,
    "md_to_pdf": md_to_pdf_main,
    "md_to_png": md_to_png_main,
    "md_to_pptx": md_to_pptx_main,
    "md_to_xlsx": md_to_xlsx_main,
    "md_to_xml": md_to_xml_main,
}


def main():
    """Main entry point for the markdown-exporter command."""
    if len(sys.argv) < 2:
        print("Error: Subcommand is required")
        print("Usage: markdown-exporter <subcommand> [options]")
        print("Subcommands:")
        for cmd in sorted(SUBCOMMANDS.keys()):
            print(f"  {cmd}")
        sys.exit(1)

    subcommand = sys.argv[1]
    if subcommand not in SUBCOMMANDS:
        print(f"Error: Invalid subcommand '{subcommand}'")
        print("Usage: markdown-exporter <subcommand> [options]")
        print("Subcommands:")
        for cmd in sorted(SUBCOMMANDS.keys()):
            print(f"  {cmd}")
        sys.exit(1)

    # Call the corresponding main function with the remaining arguments
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    try:
        SUBCOMMANDS[subcommand]()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
