from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_xlsx import convert_md_to_xlsx
from scripts.lib.utils.file_utils import get_meta_data
from scripts.lib.utils.logger_utils import get_logger
from scripts.lib.utils.mimetype_utils import MimeType
from scripts.lib.utils.param_utils import get_md_text, get_param_value


class MarkdownToXlsxTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        force_text_value: bool = ("true" == get_param_value(tool_parameters, "force_text_value", "true").lower())

        # generate XLSX file using shared service
        try:
            # Create temporary output file
            with NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_xlsx_file:
                temp_output_path = Path(temp_xlsx_file.name)
            
            try:
                # Convert to XLSX using the public service
                convert_md_to_xlsx(md_text, temp_output_path, is_strip_wrapper=True, force_text=force_text_value)
                
                # Read the converted file content
                result_file_bytes = temp_output_path.read_bytes()
                
                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.XLSX,
                        output_filename=tool_parameters.get("output_filename"),
                    ),
                )
            finally:
                # Clean up temporary output file
                if temp_output_path.exists():
                    temp_output_path.unlink()
        except Exception as e:
            self.logger.exception("Failed to convert file")
            yield self.create_text_message(
                f"Failed to convert markdown text to XLSX file, error: {str(e)}")
            return
