#!/usr/bin/env python3
"""
MdToMermaid service
"""

import re
import threading
import zipfile
from pathlib import Path
from subprocess import CalledProcessError
from tempfile import NamedTemporaryFile

from nodejs_wheel import npx

from scripts.utils.logger_utils import get_logger
from scripts.utils.markdown_utils import get_md_text

logger = get_logger(__name__)


# Function to pre-install mermaid-cli
def pre_install_mermaid():
    """
    Pre-install mermaid-cli using npx to avoid installation during first conversion
    """
    try:
        # Execute npx command to install mermaid-cli
        cmd_args = ["--yes", "--package", "@mermaid-js/mermaid-cli",
                    "mmdc", "-V"]
        logger.info("Pre-installing mermaid-cli...")
        result = npx(cmd_args, return_completed_process=True)
        logger.info("Mermaid-cli pre-installation completed successfully")
    except Exception as e:
        logger.warning(f"Warning: Mermaid-cli pre-installation failed: {e}")
        # Continue execution even if pre-installation fails


# Run pre-installation asynchronously when module is imported
def start_pre_installation():
    """
    Start pre-installation in a separate thread to avoid blocking module loading
    """
    thread = threading.Thread(target=pre_install_mermaid, daemon=True)
    thread.start()


def extract_mermaid_blocks(md_text: str) -> list[str]:
    """
    Extract mermaid code blocks from Markdown text
    Args:
        md_text: Markdown text to process
    Returns:
        List of mermaid code blocks
    """
    # Pattern to match mermaid code blocks
    mermaid_pattern = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
    mermaid_blocks = mermaid_pattern.findall(md_text)

    # Clean up code blocks
    cleaned_blocks = []
    for block in mermaid_blocks:
        # Remove leading/trailing whitespace
        cleaned_block = block.strip()
        if cleaned_block:
            cleaned_blocks.append(cleaned_block)

    return cleaned_blocks


def convert_mermaid_to_png(mermaid_code: str, output_path: Path) -> bool:
    """
    Convert mermaid code to PNG using mermaid-cli
    Args:
        mermaid_code: Mermaid code to convert
        output_path: Path to save the PNG output
    Returns:
        True if conversion succeeded, False otherwise
    """

    try:
        # Create a temporary file for mermaid code (without markdown wrapper)
        # Mermaid CLI can process plain mermaid code files with .mmd extension
        with NamedTemporaryFile(suffix=".mmd", delete=False) as temp_mermaid_file:
            temp_mermaid_path = Path(temp_mermaid_file.name)
            temp_mermaid_path.write_text(mermaid_code)

        logger.debug(f"Created temporary file with content:\n{mermaid_code}")

        # Execute mermaid-cli command using nodejs-wheel npx
        logger.info(f"Executing mermaid-cli command for file: {temp_mermaid_path}")
        
        success = False
        
        try:
            logger.debug("Using nodejs-wheel npx")
            
            # Command arguments for mermaid-cli
            cmd_args = ["--yes", "--package", "@mermaid-js/mermaid-cli",
                        "mmdc",
                        "-i", str(temp_mermaid_path),
                        "-o", str(output_path),
                        "--scale", "2",
                        ]
            logger.debug(f"Running command: npx {' '.join(cmd_args)}")
            
            # Execute the command using nodejs-wheel npx
            result = npx(cmd_args, return_completed_process=True)
            
            logger.debug(f"Command returned: {result}")
            
            # Check if output file exists and has content
            if output_path.exists() and output_path.stat().st_size > 0:
                logger.info("Success with nodejs-wheel npx")
                # logger.debug(f"Output file size: {output_path.stat().st_size} bytes")
                success = True
            else:
                logger.error("Output file not created or empty")
                # Clean up empty output file
                if output_path.exists():
                    output_path.unlink()
                    
        except Exception as e:
            logger.error(f"Error with nodejs-wheel npx: {e}")
            # Clean up empty output file
            if output_path.exists():
                output_path.unlink()
        
        if not success:
            logger.error("Error: Failed to convert mermaid code to PNG")
            return False

        # Output file should exist and have content since we checked it in the loop
        logger.info(f"Successfully converted mermaid code to PNG: {output_path}")
        logger.debug(f"Output file size: {output_path.stat().st_size} bytes")
        return True

    except CalledProcessError as e:
        logger.error(f"Error: mermaid-cli execution failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Error: Unexpected error during conversion: {e}")
        return False
    finally:
        # Clean up temporary files
        if 'temp_mermaid_path' in locals() and temp_mermaid_path.exists():
            try:
                temp_mermaid_path.unlink()
            except Exception:
                pass


def convert_md_to_mermaid(md_text: str, output_path: Path, compress: bool = False,
                          is_strip_wrapper: bool = False) -> list[Path]:
    """
    Extract mermaid code blocks from Markdown and convert them to PNG files
    Args:
        md_text: Markdown text to process
        output_path: Path to save the output files
        compress: Whether to compress all PNGs into a ZIP file
        is_strip_wrapper: Whether to remove code block wrapper if present
    Returns:
        List of paths to the created files
    Raises:
        ValueError: If input processing fails
        Exception: If conversion fails
    """
    # Process Markdown text
    processed_md = get_md_text(md_text, is_strip_wrapper=False)
    if "```mermaid" not in processed_md:
        processed_md = f"```mermaid\n{processed_md}\n```"

    # Extract mermaid code blocks
    mermaid_blocks = extract_mermaid_blocks(processed_md)

    if not mermaid_blocks:
        raise ValueError("No mermaid code blocks found in the input text")

    # Convert each mermaid block to PNG
    png_files = []
    for i, mermaid_code in enumerate(mermaid_blocks):
        try:
            # Create temporary PNG file
            with NamedTemporaryFile(suffix=".png", delete=False) as temp_png_file:
                temp_png_path = Path(temp_png_file.name)

            # Convert mermaid to PNG
            success = convert_mermaid_to_png(mermaid_code, temp_png_path)
            if success:
                png_files.append(temp_png_path)
                logger.info(f"Converted mermaid diagram {i + 1}")
            else:
                logger.error(f"Failed to convert mermaid diagram {i + 1}")
                # Clean up failed conversion
                if temp_png_path.exists():
                    temp_png_path.unlink()

        except Exception as e:
            logger.error(f"Error converting mermaid diagram {i + 1}: {e}")
            # Clean up temporary files
            if 'temp_png_path' in locals() and temp_png_path.exists():
                try:
                    temp_png_path.unlink()
                except Exception:
                    pass

    if not png_files:
        raise Exception("No mermaid diagrams were successfully converted")

    # Output files
    created_files = []
    if compress:
        # Compress to ZIP file
        try:
            with NamedTemporaryFile(suffix=".zip", delete=False) as temp_zip_file:
                temp_zip_path = Path(temp_zip_file.name)

            with zipfile.ZipFile(temp_zip_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                for i, png_path in enumerate(png_files):
                    zip_file.write(png_path, arcname=f"mermaid_{i + 1}.png")

            # Copy to final output path
            output_path.write_bytes(temp_zip_path.read_bytes())
            created_files.append(output_path)
            logger.info(f"Successfully created ZIP file with {len(png_files)} PNG diagrams: {output_path}")

            # Clean up temporary files
            temp_zip_path.unlink()
            for png_path in png_files:
                png_path.unlink()

        except Exception as e:
            # Clean up temporary files
            if 'temp_zip_path' in locals() and temp_zip_path.exists():
                temp_zip_path.unlink()
            for png_path in png_files:
                if png_path.exists():
                    png_path.unlink()
            raise Exception(f"Failed to create ZIP file: {e}")
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

            for i, png_path in enumerate(png_files):
                if len(png_files) > 1:
                    file_path = base_path / f"{output_path.stem}_{i + 1}.png"
                else:
                    file_path = output_path if output_path.suffix == '.png' else base_path / f"{output_path.name}.png"

                file_path.parent.mkdir(parents=True, exist_ok=True)
                # Copy PNG content
                file_path.write_bytes(png_path.read_bytes())
                created_files.append(file_path)
                logger.info(f"Successfully saved PNG to {file_path}")

                # Clean up temporary file
                png_path.unlink()

        except Exception as e:
            # Clean up temporary files
            for png_path in png_files:
                if png_path.exists():
                    png_path.unlink()
            raise Exception(f"Failed to save PNG files: {e}")

    return created_files
