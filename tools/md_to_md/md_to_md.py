from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.services.svc_md_to_md import convert_md_to_md
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text


class MarkdownToMarkdownTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)

        try:
            # create a temporary output MD file
            with NamedTemporaryFile(suffix=".md", delete=False) as temp_md_file:
                temp_md_output_path = Path(temp_md_file.name)

            # convert markdown to md using the shared function
            created_file = convert_md_to_md(md_text, temp_md_output_path, is_strip_wrapper=True)
            
            # read the result bytes
            result_file_bytes = created_file.read_bytes()

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to MD file")
            yield self.create_text_message(f"Failed to convert markdown text to MD file, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_md_output_path' in locals():
                temp_md_output_path.unlink(missing_ok=True)

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.MD,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
