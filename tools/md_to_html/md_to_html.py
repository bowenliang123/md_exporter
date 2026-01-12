from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.file_utils import get_meta_data
from tools.utils.logger_utils import get_logger
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_text


from scripts.lib.svc_md_to_html import convert_md_to_html
from scripts.utils.utils import get_md_text as get_md_text_base


class MarkdownToHtmlTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        from tempfile import NamedTemporaryFile
        from pathlib import Path
        
        # get parameters
        md_text = get_md_text(tool_parameters)

        try:
            # Create temporary output file
            with NamedTemporaryFile(suffix=".html", delete=False) as temp_output_file:
                temp_output_path = Path(temp_output_file.name)
            
            try:
                # Convert to HTML using the public service
                convert_md_to_html(md_text, temp_output_path, is_strip_wrapper=True)
                
                # Read the converted file content
                result_file_bytes = temp_output_path.read_bytes()
                
                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.HTML,
                        output_filename=tool_parameters.get("output_filename"),
                    ),
                )
            finally:
                # Clean up temporary output file
                if temp_output_path.exists():
                    temp_output_path.unlink()
        except Exception as e:
            self.logger.exception("Failed to convert file")
            yield self.create_text_message(f"Failed to convert markdown text to HTML file, error: {str(e)}")
            raise e
