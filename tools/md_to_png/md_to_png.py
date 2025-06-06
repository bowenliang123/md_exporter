import io
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator

import pymupdf
from PIL import Image
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.file_utils import get_meta_data
from tools.utils.logger_utils import get_logger
from tools.utils.md_utils import MarkdownUtils
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_text, get_param_value


class MarkdownToPngTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        from xhtml2pdf import pisa

        # get parameters
        md_text = get_md_text(tool_parameters, is_strip_wrapper=True)
        output_filename = tool_parameters.get("output_filename", "output")
        is_compress = "true" == get_param_value(tool_parameters, "is_compress", "true").lower()

        images_for_zip = []
        try:
            html_str = self._convert_to_html(md_text)
            result_file_bytes = pisa.CreatePDF(
                src=html_str,
                dest_bytes=True,  # pass the generated bytes in return
                encoding="utf-8",
                capacity=100 * 1024 * 1024,  # 100 MB capacity
            )

            # Open PDF with PyMuPDF
            doc = pymupdf.open(stream=result_file_bytes)

            total_page_count = doc.page_count
            zoom = 2
            for page_num in range(total_page_count):
                page = doc.load_page(page_num)
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                # Convert PyMuPDF pixmap to PIL Image
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

                # Save PIL Image to an in-memory bytes buffer
                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                img_buffer.seek(0)

                # Create filename for this page
                if total_page_count > 1:
                    image_filename = f"{output_filename}_page{page_num + 1}.png"
                else:
                    image_filename = f"{output_filename}.png"

                image_bytes = img_buffer.getvalue()
                if not is_compress:
                    # Send the PNG image
                    yield self.create_blob_message(
                        blob=image_bytes,
                        meta=get_meta_data(
                            mime_type=MimeType.PNG,
                            output_filename=image_filename,
                        )
                    )
                else:
                    images_for_zip.append({
                        "blob": image_bytes,
                        "meta": {
                            "mime_type": MimeType.PNG,
                        }
                    })

            if is_compress:
                with NamedTemporaryFile(suffix=".zip", delete=True) as temp_zip_file, \
                        zipfile.ZipFile(temp_zip_file.name, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
                    for idx, code_block in enumerate(images_for_zip, 1):
                        blob = code_block["blob"]
                        meta = code_block["meta"]
                        mime_type = meta["mime_type"]
                        suffix = MimeType.get_extension(mime_type)
                        with NamedTemporaryFile(delete=True) as temp_file:
                            temp_file.write(blob)
                            temp_file.flush()
                            zip_file.write(temp_file.name, arcname=f"image_{idx}{suffix}")
                    zip_file.close()

                    yield self.create_blob_message(
                        blob=Path(zip_file.filename).read_bytes(),
                        meta=get_meta_data(
                            mime_type=MimeType.ZIP,
                            output_filename=output_filename,
                        ),
                    )


        except Exception as e:
            self.logger.exception("Failed to convert file")
            yield self.create_text_message(f"Failed to convert markdown text to PNG files, error: {str(e)}")
            return

        return

    @staticmethod
    def _convert_to_html(md_text: str) -> str:
        # convert markdown to html
        html_str = MarkdownUtils.convert_markdown_to_html(md_text)

        if not MarkdownUtils.contains_chinese(md_text) \
                and not MarkdownUtils.contains_japanese(md_text):
            return html_str

        # prepend additional CSS style

        # known available asian fonts in PDF by default (Acrobat Reader)
        # https://xhtml2pdf.readthedocs.io/en/latest/reference.html#asian-fonts-support
        # TODO: make font list configurable
        font_families = ",".join(
            [
                "Sans-serif",  # for English
                "STSong-Light",  # for Simplified Chinese
                "MSung-Light",  # for Traditional Chinese
                "HeiseiMin-W3",  # for Japanese
            ]
        )
        css_style = f"""
        <style>
            html {{
                -pdf-word-wrap: CJK;
                font-family:  "{font_families}"; 
            }}
        </style>
        """

        result = f"""
        {css_style}
        {html_str}
        """
        return result
