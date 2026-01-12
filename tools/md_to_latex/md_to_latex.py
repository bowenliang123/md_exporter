from typing import Generator, Optional

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text
from scripts.utils.table_utils import TableParser


class MarkdownToLatexTool(Tool):
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
                table_latex_str = table.to_latex(index=False, bold_rows=True)
                doc_latex_str = ("\\documentclass[]{{article}}\n"
                                 + "\\usepackage{{booktabs}}\n"
                                 + "\\begin{document}}\n"
                                 + "\n"
                                 + table_latex_str
                                 + "\n"
                                 + "\\end{document}\n")
                result_file_bytes = doc_latex_str.encode("utf-8")

                result_filename: Optional[str] = None
                if output_filename:
                    if len(tables) > 1:
                        result_filename = f"{output_filename}_{i + 1}.csv"
                    else:
                        result_filename = output_filename

                yield self.create_blob_message(
                    blob=result_file_bytes,
                    meta=get_meta_data(
                        mime_type=MimeType.LATEX,
                        output_filename=result_filename,
                    ),
                )

            except Exception as e:
                self.logger.exception("Failed to convert to LaTeX file")
                yield self.create_text_message(f"Failed to convert markdown text to LaTeX file, error: {str(e)}")
                return
