import logging
from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.md_utils import MarkdownUtils


class MarkdownToPdfFile(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        from xhtml2pdf import pisa

        # get parameters
        md_text = tool_parameters.get("md_text")
        if not md_text:
            raise ValueError("Invalid input md_text")

        try:
            md_text = MarkdownUtils.strip_markdown_wrapper(md_text)
            html_str = self._convert_to_html(md_text)
            result_file_bytes = pisa.CreatePDF(
                src=html_str,
                dest_bytes=True,  # pass the generated bytes in return
                encoding="utf-8",
            )
        except Exception as e:
            logging.exception("Failed to convert file")
            yield self.create_text_message(f"Failed to convert markdown text to PDF file, error: {str(e)}")
            return

        # yield self.create_text_message("The PDF file is saved.")
        yield self.create_blob_message(blob=result_file_bytes, meta={"mime_type": "application/pdf"})
        return

    @staticmethod
    def _convert_to_html(md_text: str) -> str:
        html_str = MarkdownUtils.convert_markdown_to_html(md_text)

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