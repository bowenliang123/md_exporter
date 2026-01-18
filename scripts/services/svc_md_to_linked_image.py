#!/usr/bin/env python3
"""
MdToLinkedImage service
"""

import re
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import httpx
import markdown
from bs4 import BeautifulSoup

from scripts.utils.logger_utils import get_logger
from scripts.utils.markdown_utils import get_md_text

logger = get_logger(__name__)

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
        soup = BeautifulSoup(html, "html.parser")
        img_tags = soup.find_all("img")
        image_urls = [img.get("src") for img in img_tags if img.get("src")]
    except Exception as e:
        logger.warning(f"Warning: Failed to extract image URLs by HTML parser, trying regex: {e}")

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


def convert_md_to_linked_image(
    md_text: str, output_path: Path, compress: bool = False, is_strip_wrapper: bool = False
) -> list[Path]:
    """
    Extract image links from Markdown and download them as files
    Args:
        md_text: Markdown text to process
        output_path: Path to save the output files
        compress: Whether to compress all images into a ZIP file
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        List of paths to the created files
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=is_strip_wrapper)

    # Extract image URLs
    image_urls = extract_image_urls(processed_md)

    if not image_urls:
        raise ValueError("No image URLs found in the input text")

    # Prepare downloaded images
    downloaded_images = []
    for url in image_urls:
        try:
            response = httpx.get(url, timeout=120)
            if response.status_code != 200:
                logger.warning(
                    f"Warning: Failed to download image from URL: {url}, HTTP status code: {response.status_code}"
                )
                continue

            content_type = response.headers.get("Content-Type", "image/png")
            downloaded_images.append({"blob": response.content, "mime_type": content_type})
            logger.info(f"Downloaded: {url}")

        except Exception as e:
            logger.warning(f"Warning: Failed to download image from URL: {url}, error: {e}")
            continue

    if not downloaded_images:
        # raise Exception("No images were successfully downloaded")
        return []

    # Output files
    created_files = []
    if compress:
        # Compress to ZIP file
        try:
            with (
                NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file,
                zipfile.ZipFile(temp_zip_file.name, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file,
            ):
                for idx, image_data in enumerate(downloaded_images, 1):
                    suffix = get_extension_by_mime_type(image_data["mime_type"])
                    with NamedTemporaryFile(delete=True) as temp_file:
                        temp_file.write(image_data["blob"])
                        temp_file.flush()
                        zip_file.write(temp_file.name, arcname=f"image_{idx}{suffix}")
                zip_file.close()

                output_path.write_bytes(Path(zip_file.filename).read_bytes())
                created_files.append(output_path)
                logger.info(f"Successfully created ZIP file with {len(downloaded_images)} images: {output_path}")

        except Exception as e:
            raise Exception(f"Failed to create ZIP file: {e}")
    else:
        # Save as separate files
        try:
            # If output path is a directory, create directory
            if output_path.suffix == "":
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
                created_files.append(file_path)
                logger.info(f"Successfully saved image to {file_path}")

        except Exception as e:
            raise Exception(f"Failed to save images: {e}")

    return created_files
