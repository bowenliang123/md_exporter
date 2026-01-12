#!/usr/bin/env python3
"""
Markdown linked images extractor
Extracts image links from Markdown and downloads them as files
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import httpx
import markdown
from bs4 import BeautifulSoup


from utils.utils import get_md_text


# MIME type mapping
MIME_TYPE_MAP = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
    "application/zip": ".zip",
    "image/bmp": ".bmp",
}


def get_extension_by_mime_type(mime_type: str) -> str:
    """Get file extension by MIME type"""
    return MIME_TYPE_MAP.get(mime_type.lower(), ".png")


def extract_image_urls(md_text: str) -> list[str]:
    """Extract image URLs from Markdown text"""
    html = markdown.markdown(text=md_text, extensions=["extra", "toc"])

    image_urls: list[str] = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        image_urls = [img.get('src') for img in img_tags if img.get('src')]
    except Exception as e:
        print(f"Warning: Failed to extract image URLs by HTML parser, trying regex: {e}", file=sys.stderr)

        # Fallback: Use regex
        markdown_image_pattern = re.compile(r"!\[.*?]\(.*?\)")
        match_image_tags = re.findall(markdown_image_pattern, md_text)
        for img in match_image_tags:
            url_match = re.findall(r"\((.*?)\)", img)
            if url_match:
                image_urls.append(url_match[0])

    # Filter invalid URLs
    result_image_urls = []
    for url in image_urls:
        if not url or not url.lower().startswith("http"):
            continue
        elif url in result_image_urls:
            continue
        else:
            result_image_urls.append(url)

    return result_image_urls


def main():
    parser = argparse.ArgumentParser(
        description='Extract image links from Markdown and download as files',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input Markdown file path or Markdown text'
    )
    parser.add_argument(
        'output',
        help='Output file or directory path'
    )
    parser.add_argument(
        '--compress',
        action='store_true',
        help='Compress all images into a ZIP file'
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
        md_text = get_md_text(md_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract image URLs
    image_urls = extract_image_urls(md_text)

    if not image_urls:
        print("Warning: No image URLs found in the input text", file=sys.stderr)
        sys.exit(0)

    output_path = Path(args.output)

    # Prepare downloaded images
    downloaded_images = []
    for url in image_urls:
        try:
            response = httpx.get(url, timeout=120)
            if response.status_code != 200:
                print(f"Warning: Failed to download image from URL: {url}, HTTP status code: {response.status_code}", file=sys.stderr)
                continue

            content_type = response.headers.get('Content-Type', 'image/png')
            downloaded_images.append({
                "blob": response.content,
                "mime_type": content_type
            })
            print(f"Downloaded: {url}")

        except Exception as e:
            print(f"Warning: Failed to download image from URL: {url}, error: {e}", file=sys.stderr)
            continue

    if not downloaded_images:
        print("Error: No images were successfully downloaded", file=sys.stderr)
        sys.exit(1)

    # Output files
    if args.compress:
        # Compress to ZIP file
        try:
            with NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file, \
                    zipfile.ZipFile(temp_zip_file.name, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                for idx, image_data in enumerate(downloaded_images, 1):
                    suffix = get_extension_by_mime_type(image_data["mime_type"])
                    with NamedTemporaryFile(delete=True) as temp_file:
                        temp_file.write(image_data["blob"])
                        temp_file.flush()
                        zip_file.write(temp_file.name, arcname=f"image_{idx}{suffix}")
                zip_file.close()

                output_path.write_bytes(Path(zip_file.filename).read_bytes())
                print(f"Successfully created ZIP file with {len(downloaded_images)} images: {output_path}")

        except Exception as e:
            print(f"Error: Failed to create ZIP file - {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Save as separate files
        try:
            # If output path is a directory, create directory
            if output_path.suffix == '':
                output_path.mkdir(parents=True, exist_ok=True)
                base_path = output_path
            else:
                # If output path is a file, use parent directory as base path
                base_path = output_path.parent

            for index, image_data in enumerate(downloaded_images):
                suffix = get_extension_by_mime_type(image_data["mime_type"])
                if len(downloaded_images) > 1:
                    file_path = base_path / f"{output_path.stem}_{index + 1}{suffix}"
                else:
                    file_path = output_path if output_path.suffix else base_path / f"{output_path.name}{suffix}"

                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_bytes(image_data["blob"])
                print(f"Successfully saved image to {file_path}")

        except Exception as e:
            print(f"Error: Failed to save images - {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
