from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

from md_exporter.services.svc_md_to_pptx import convert_md_to_pptx
from md_exporter.utils.file_utils import get_meta_data
from md_exporter.utils.logger_utils import get_logger
from md_exporter.utils.mimetype_utils import MimeType
from md_exporter.utils.param_utils import get_md_text_from_tool_params


class MarkdownToPptxTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters)
        pptx_template_file: File | None = tool_parameters.get("pptx_template_file")

        # check parameters
        if pptx_template_file and not isinstance(pptx_template_file, File):
            raise ValueError("Not a valid file for pptx template file")

        temp_pptx_template_file: NamedTemporaryFile | None = None
        temp_pptx_template_file_path: Path | None = None
        try:
            if pptx_template_file:
                temp_pptx_template_file = NamedTemporaryFile(delete=False, suffix=".pptx")
                temp_pptx_template_file.write(pptx_template_file.blob)
                temp_pptx_template_file.close()
                temp_pptx_template_file_path = Path(temp_pptx_template_file.name)

            # create a temporary output PPTX file
            with NamedTemporaryFile(suffix=".pptx", delete=False) as temp_pptx_file:
                temp_pptx_output_path = Path(temp_pptx_file.name)

            # convert markdown to pptx using the shared function
            output_path = convert_md_to_pptx(md_text, temp_pptx_output_path, temp_pptx_template_file_path)

            # read the result bytes
            result_file_bytes = output_path.read_bytes()

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to PPTX file")
            raise e
        finally:
            # clean up temporary files
            if temp_pptx_template_file:
                Path(temp_pptx_template_file.name).unlink(missing_ok=True)
            if "temp_pptx_output_path" in locals():
                temp_pptx_output_path.unlink(missing_ok=True)

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.PPTX,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
