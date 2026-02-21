import logging
import uuid
from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from md_exporter.services.svc_md_to_ipynb import convert_md_to_ipynb
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToIpynbTool(Tool):
    logger = logging.getLogger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters, is_strip_wrapper=True)

        try:
            # Create temporary output file
            with NamedTemporaryFile(suffix=".ipynb", delete=False) as temp_output_file:
                temp_output_path = Path(temp_output_file.name)

            try:
                # Convert to IPYNB using the public service
                convert_md_to_ipynb(md_text, temp_output_path, is_strip_wrapper=True)

                # Read the converted file content
                result_file_bytes = temp_output_path.read_bytes()

                output_filename = tool_parameters.get("output_filename") or str(uuid.uuid4()).replace("-", "")
                # Add .ipynb extension if not present
                if not output_filename.endswith(".ipynb"):
                    output_filename += ".ipynb"

                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.IPYNB,
                        output_filename=output_filename,
                    ),
                )
            finally:
                # Clean up temporary output file
                if temp_output_path.exists():
                    temp_output_path.unlink()
        except Exception as e:
            self.logger.exception("Failed to convert markdown text to IPYNB file")
            yield self.create_text_message(f"Failed to convert markdown text to IPYNB file, error: {str(e)}")
            raise e
