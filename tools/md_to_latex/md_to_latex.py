import logging
from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.file_utils import get_meta_data
from tools.utils.logger_utils import get_logger
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_text
from tools.utils.table_utils import TableParser


class MarkdownToLatexTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)

        # parse markdown to tables
        tables = TableParser.parse_md_to_tables(self.logger, md_text)

        try:
            table = tables[0]
            table_latex_str = table.to_latex(index=False, bold_rows=True)
            doc_latex_str = ("\\documentclass[]{{article}}\n"
                             + "\\usepackage{{booktabs}}\n"
                             + "\\begin{document}}\n"
                             + "\n"
                             + table_latex_str
                             + "\n"
                             + "\\end{document}\n")
            result_file_bytes = doc_latex_str.encode("utf-8")
        except Exception as e:
            self.logger.exception("Failed to convert to LaTeX file")
            yield self.create_text_message(f"Failed to convert markdown text to LaTeX file, error: {str(e)}")
            return

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.LATEX,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
