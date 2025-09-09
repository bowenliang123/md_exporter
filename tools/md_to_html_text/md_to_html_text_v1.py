from typing import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.utils.logger_utils import get_logger
from tools.utils.md_utils import MarkdownUtils
from tools.utils.param_utils import get_md_text


class MarkdownToHtmlTextTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text(tool_parameters)

        try:
            html_str = MarkdownUtils.convert_markdown_to_html(md_text)
        except Exception as e:
            self.logger.exception("Failed to convert markdown text to HTML text")
            yield self.create_text_message(f"Failed to convert markdown text to HTML text, error: {str(e)}")
            return

        yield self.create_text_message(html_str)
        return
