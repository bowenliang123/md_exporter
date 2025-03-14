import logging
from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.mimetype_utils import MimeType
from tools.utils.table_utils import TableParser


class MarkdownToCsvTool(Tool):
    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = tool_parameters.get("md_text")
        if not md_text:
            raise ValueError("Invalid input md_text")

        # parse markdown to tables
        tables = TableParser.parse_md_to_tables(md_text)

        try:
            table = tables[0]
            csv_str = table.to_csv(index=False, encoding="utf-8")
            result_file_bytes = csv_str.encode("utf-8")
        except Exception as e:
            logging.exception("Failed to convert to CSV file")
            yield self.create_text_message(f"Failed to convert markdown text to CSV file, error: {str(e)}")
            return

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta={"mime_type": MimeType.CSV},
        )
        return
