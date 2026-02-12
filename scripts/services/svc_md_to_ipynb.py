#!/usr/bin/env python3
"""
Markdown to IPYNB conversion service
Provides common functionality for converting Markdown to IPYNB format
"""

from pathlib import Path

from scripts.utils.markdown_utils import get_md_text


def convert_md_to_ipynb(md_text: str, output_path: Path, is_strip_wrapper: bool = False) -> None:
    """
    Convert Markdown text to IPYNB format

    Args:
        md_text: Markdown text to convert
        output_path: Path to save the output IPYNB file
        is_strip_wrapper: Whether to remove code block wrapper if present

    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Convert to IPYNB - use convert_file with temporary file
    from tempfile import NamedTemporaryFile

    from pypandoc import convert_file

    with NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as temp_md_file:
        temp_md_file.write(processed_md)
        temp_md_file_path = temp_md_file.name

    try:
        # Convert using convert_file with outputfile parameter
        convert_file(
            source_file=temp_md_file_path,
            format="markdown",
            to="ipynb",
            outputfile=str(output_path),
            extra_args=[],
        )

        # Post-process the IPYNB file to split into multiple cells
        import json

        with open(output_path, encoding="utf-8") as f:
            notebook = json.load(f)

        # Get the first cell (which contains all the content)
        if notebook["cells"]:
            first_cell = notebook["cells"][0]
            if first_cell["cell_type"] == "markdown":
                source = "".join(first_cell["source"])

                # Split the source into cells
                new_cells = []
                current_content = []
                in_code_block = False
                code_content = []

                lines = source.split("\n")
                for line in lines:
                    # Check for code block start
                    if line.strip().startswith("```"):
                        if not in_code_block:
                            # End of markdown cell, start of code block
                            if current_content:
                                # Add the current markdown cell
                                new_cells.append({"cell_type": "markdown", "metadata": {}, "source": current_content})
                                current_content = []
                            # Start code block
                            in_code_block = True
                            code_content = []
                        else:
                            # End of code block
                            in_code_block = False
                            # Add the code cell
                            new_cells.append(
                                {
                                    "cell_type": "code",
                                    "metadata": {},
                                    "source": code_content,
                                    "execution_count": None,
                                    "outputs": [],
                                }
                            )
                            code_content = []
                    elif in_code_block:
                        # Add to code content
                        code_content.append(line + "\n")
                    else:
                        # Add to markdown content
                        current_content.append(line + "\n")

                # Add any remaining markdown content
                if current_content:
                    new_cells.append({"cell_type": "markdown", "metadata": {}, "source": current_content})

                # Replace the cells with the new ones
                notebook["cells"] = new_cells

                # Write the updated notebook back
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(notebook, f, indent=2, ensure_ascii=False)
    finally:
        # Clean up temporary file
        import os

        os.unlink(temp_md_file_path)
