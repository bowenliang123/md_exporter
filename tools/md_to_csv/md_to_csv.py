from collections.abc import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_csv import get_csv_output_encoding
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text
from scripts.utils.table_utils import TableParser


class MarkdownToCsvTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        output_filename = tool_parameters.get("output_filename")

        # parse markdown to tables
        tables = TableParser.parse_md_to_tables(self.logger, md_text)

        for i, table in enumerate(tables):
            try:
                csv_str = table.to_csv(index=False, encoding="utf-8")
                csv_output_encoding = get_csv_output_encoding(csv_str)
                result_file_bytes = csv_str.encode(csv_output_encoding)

                result_filename: str | None = None
                if output_filename:
                    if len(tables) > 1:
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
                self.logger.exception("Failed to convert to CSV file")
                yield self.create_text_message(f"Failed to convert markdown text to CSV file, error: {str(e)}")
                return
