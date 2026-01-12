from collections.abc import Generator
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_json import convert_md_to_json
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text


class JsonOutputStyle(StrEnum):
    JSONL = "jsonl"
    JSON_ARRAY = "json"


class MarkdownToJsonTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        output_filename = tool_parameters.get("output_filename")
        output_style = tool_parameters.get("output_style", JsonOutputStyle.JSONL)

        try:
            # create a temporary output JSON file
            with NamedTemporaryFile(suffix=".json", delete=False) as temp_json_file:
                temp_json_output_path = Path(temp_json_file.name)

            # convert markdown to json using the shared function
            created_files = convert_md_to_json(md_text, temp_json_output_path, style=output_style, is_strip_wrapper=True)
            
            # read the result bytes for each created file
            for i, file_path in enumerate(created_files):
                result_file_bytes = file_path.read_bytes()
                
                result_filename: str | None = None
                if output_filename:
                    if len(created_files) > 1:
                        result_filename = f"{output_filename}_{i + 1}"
                    else:
                        result_filename = output_filename

                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.JSON,
                        output_filename=result_filename,
                    ),
                )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to JSON file")
            yield self.create_text_message(f"Failed to convert markdown text to JSON file, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if 'temp_json_output_path' in locals():
                temp_json_output_path.unlink(missing_ok=True)
            if 'created_files' in locals():
                for file_path in created_files:
                    file_path.unlink(missing_ok=True)

        return
