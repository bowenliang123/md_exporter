#!/usr/bin/env python3
"""
Markdown to PNG converter
Converts Markdown text to PNG images
"""

import argparse
import io
import sys
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import pymupdf
from PIL import Image
from xhtml2pdf import pisa


from utils.utils import get_md_text, convert_markdown_to_html, contains_chinese, contains_japanese


def convert_to_html_with_font_support(md_text: str) -> str:
    """Convert Markdown to HTML with Chinese font support"""
    html_str = convert_markdown_to_html(md_text)

    if not contains_chinese(md_text) and not contains_japanese(md_text):
        return html_str

    # Add Chinese font CSS
    font_families = ",".join([
        "Sans-serif",
        "STSong-Light",
        "MSung-Light",
        "HeiseiMin-W3",
    ])
    css_style = f"""
    <style>
        html {{
            -pdf-word-wrap: CJK;
            font-family: "{font_families}"; 
        }}
    </style>
    """

    result = f"""
    {css_style}
    {html_str}
    """
    return result


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown text to PNG images',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output PNG file path or directory path'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress all PNG images into a ZIP file'
    )
    parser.add_argument(
        '--strip-wrapper',
        action='store_true',
        help='Remove code block wrapper if present'
    )

    args = parser.parse_args()

    # Read input
    input_path = Path(args.input)
    if input_path.exists():
        md_text = input_path.read_text(encoding='utf-8')
    else:
        md_text = args.input

    # Process Markdown text
    try:
        md_text = get_md_text(md_text, is_strip_wrapper=args.strip_wrapper)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)
    output_filename = output_path.stem if output_path.suffix else "output"

    images_for_zip = []
    try:
        # Convert to HTML
        html_str = convert_to_html_with_font_support(md_text)

        # Convert to PDF
        result_file_bytes = pisa.CreatePDF(
            src=html_str,
            dest_bytes=True,
            encoding="utf-8",
            capacity=500 * 1024 * 1024,
        )

        # Open PDF and convert to PNG
        doc = pymupdf.open(stream=result_file_bytes)
        total_page_count = doc.page_count
        zoom = 2

        for page_num in range(total_page_count):
            page = doc.load_page(page_num)
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert to PIL Image
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

            # Save to memory
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Create file name
            if total_page_count > 1:
                image_filename = f"{output_filename}_page{page_num + 1}.png"
            else:
                image_filename = f"{output_filename}.png"

            image_bytes = img_buffer.getvalue()

            if not args.compress:
                # Save PNG file directly
                if output_path.suffix and total_page_count == 1:
                    output_file = output_path
                else:
                    output_file = output_path.parent / image_filename if output_path.suffix else output_path / image_filename
                
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_bytes(image_bytes)
                print(f"Successfully converted to {output_file}")
            else:
                # Add to ZIP list
                images_for_zip.append({
                    "blob": image_bytes,
                    "suffix": ".png"
                })

        # If compression to ZIP is needed
        if args.compress and images_for_zip:
            with NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file, \
                    zipfile.ZipFile(temp_zip_file.name, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                for idx, image_data in enumerate(images_for_zip, 1):
                    with NamedTemporaryFile(delete=True) as temp_file:
                        temp_file.write(image_data["blob"])
                        temp_file.flush()
                        zip_file.write(temp_file.name, arcname=f"image_{idx}{image_data['suffix']}")
                zip_file.close()

                output_path.write_bytes(Path(zip_file.filename).read_bytes())
                print(f"Successfully created ZIP file with {len(images_for_zip)} PNG images: {output_path}")

    except Exception as e:
        print(f"Error: Failed to convert to PNG - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
