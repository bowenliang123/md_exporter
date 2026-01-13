from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.services.svc_md_to_pdf import convert_md_to_pdf
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text


class MarkdownToPdfTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text(tool_parameters, is_strip_wrapper=True)
        
        try:
            # create a temporary output PDF file
            with NamedTemporaryFile(suffix=".pdf", delete=False) as temp_pdf_file:
                temp_pdf_output_path = Path(temp_pdf_file.name)

            # convert markdown to pdf using the shared function
            convert_md_to_pdf(md_text, temp_pdf_output_path, is_strip_wrapper=True)
            
            # read the result bytes
            result_file_bytes = temp_pdf_output_path.read_bytes()

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to PDF file")
            yield self.create_text_message(f"Failed to convert markdown text to PDF file, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_pdf_output_path' in locals():
                temp_pdf_output_path.unlink(missing_ok=True)

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.PDF,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
