from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_csv import convert_md_to_csv
from scripts.lib.utils.file_utils import get_meta_data
from scripts.lib.utils.logger_utils import get_logger
from scripts.lib.utils.mimetype_utils import MimeType
from scripts.lib.utils.param_utils import get_md_text


class MarkdownToCsvTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        output_filename = tool_parameters.get("output_filename")

        try:
            # create a temporary output CSV file
            with NamedTemporaryFile(suffix=".csv", delete=False) as temp_csv_file:
                temp_csv_output_path = Path(temp_csv_file.name)

            # convert markdown to csv using the shared function
            created_files = convert_md_to_csv(md_text, temp_csv_output_path)
            
            # read the result bytes for each created file
            for i, file_path in enumerate(created_files):
                result_file_bytes = file_path.read_bytes()
                
                result_filename: str | None = None
                if output_filename:
                    if len(created_files) > 1:
                        result_filename = f"{output_filename}_{i + 1}.csv"
                    else:
                        result_filename = output_filename

                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.CSV,
                        output_filename=result_filename,
                    ),
                )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to CSV file")
            yield self.create_text_message(f"Failed to convert markdown text to CSV file, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_csv_output_path' in locals():
                temp_csv_output_path.unlink(missing_ok=True)
            if 'created_files' in locals():
                for file_path in created_files:
                    file_path.unlink(missing_ok=True)

        return
