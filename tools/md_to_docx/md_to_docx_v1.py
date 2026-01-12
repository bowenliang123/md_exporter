from typing import Generator

import markdown
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from html2docx import html2docx

from scripts.utils.file_utils import get_meta_data
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text


class MarkdownToDocxTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text(tool_parameters, is_strip_wrapper=True)
        try:
            # Legacy: using markdowntodocx lib
            # with NamedTemporaryFile(suffix=".docx", delete=True) as temp_docx_file:
            #     markdownconverter.markdownToWordFromString(string=md_text, outfile=temp_docx_file)
            #     result_file_bytes = Path(temp_docx_file.name).read_bytes()

            html = markdown.markdown(text=md_text, extensions=["extra", "toc"])
            output_buf = html2docx(html, title="My Document")
            result_file_bytes = output_buf.getvalue()
        except Exception as e:
            self.logger.exception("Failed to convert file")
            yield self.create_text_message(f"Failed to convert markdown text to DOCX file, error: {str(e)}")
            return

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.DOCX,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
