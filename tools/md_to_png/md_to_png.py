from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_png import convert_md_to_png
from scripts.lib.utils.file_utils import get_meta_data
from scripts.lib.utils.logger_utils import get_logger
from scripts.lib.utils.mimetype_utils import MimeType
from scripts.lib.utils.param_utils import get_md_text, get_param_value


class MarkdownToPngTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text(tool_parameters, is_strip_wrapper=True)
        output_filename = tool_parameters.get("output_filename", "output")
        is_compress = "true" == get_param_value(tool_parameters, "is_compress", "true").lower()
        compress = is_compress

        try:
            # create a temporary output file
            suffix = ".zip" if compress else ".png"
            with NamedTemporaryFile(suffix=suffix, delete=False) as temp_output_file:
                temp_output_path = Path(temp_output_file.name)

            # convert markdown to png using the shared function
            created_files = convert_md_to_png(md_text, temp_output_path, compress=compress, is_strip_wrapper=True)

            # generate blob messages based on the created files
            if compress:
                # single ZIP file
                yield self.create_blob_message(
                    blob=created_files[0].read_bytes(),
                    meta=get_meta_data(
                        mime_type=MimeType.ZIP,
                        output_filename=output_filename,
                    ),
                )
            else:
                # multiple PNG files
                for file_path in created_files:
                    yield self.create_blob_message(
                        blob=file_path.read_bytes(),
                        meta=get_meta_data(
                            mime_type=MimeType.PNG,
                            output_filename=output_filename if len(created_files) == 1 else f"{output_filename}_{file_path.stem.split('_')[-1]}",
                        )
                    )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to PNG files")
            yield self.create_text_message(f"Failed to convert markdown text to PNG files, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_output_path' in locals():
                temp_output_path.unlink(missing_ok=True)
            if 'created_files' in locals():
                for file_path in created_files:
                    file_path.unlink(missing_ok=True)

        return