from typing import Generator, Optional

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.file_utils import get_meta_data
from tools.utils.logger_utils import get_logger
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_text
from tools.utils.table_utils import TableParser


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
                csv_output_encoding = "utf-8" if csv_str.isascii() else "utf-8-sig"
                result_file_bytes = csv_str.encode(csv_output_encoding)

                result_filename: Optional[str] = None
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
