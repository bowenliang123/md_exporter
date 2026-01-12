import zipfile
from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_linked_image import convert_md_to_linked_image
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text, get_param_value


class MarkdownToLinkedImageTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        is_compress = get_param_value(tool_parameters, "is_compress", "true")
        compress = "true" == is_compress.lower()

        try:
            # create a temporary output file
            suffix = ".zip" if compress else ".png"
            with NamedTemporaryFile(suffix=suffix, delete=False) as temp_output_file:
                temp_output_path = Path(temp_output_file.name)

            # convert markdown to linked images using the shared function
            created_files = convert_md_to_linked_image(md_text, temp_output_path, compress=compress, is_strip_wrapper=True)

            # generate blob messages based on the created files
            if compress:
                # single ZIP file
                yield self.create_blob_message(
                    blob=created_files[0].read_bytes(),
                    meta=get_meta_data(
                        mime_type=MimeType.ZIP,
                        output_filename=tool_parameters.get("output_filename"),
                    ),
                )
            else:
                # multiple image files
                for file_path in created_files:
                    # determine MIME type based on file suffix
                    suffix = file_path.suffix.lower()
                    mime_type = MimeType.PNG  # default
                    if suffix == ".jpg" or suffix == ".jpeg":
                        mime_type = MimeType.JPEG
                    elif suffix == ".gif":
                        mime_type = MimeType.GIF
                    elif suffix == ".webp":
                        mime_type = MimeType.WEBP
                    elif suffix == ".svg":
                        mime_type = MimeType.SVG
                    elif suffix == ".bmp":
                        mime_type = MimeType.BMP

                    yield self.create_blob_message(
                        blob=file_path.read_bytes(),
                        meta={"mime_type": mime_type}
                    )

        except Exception as e:
            self.logger.exception("Failed to convert markdown to linked images")
            yield self.create_text_message(f"Failed to convert markdown to linked images, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_output_path' in locals():
                temp_output_path.unlink(missing_ok=True)
            if 'created_files' in locals():
                for file_path in created_files:
                    file_path.unlink(missing_ok=True)

        return