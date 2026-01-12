from collections.abc import Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.lib.svc_md_to_html_text import convert_md_to_html_text
from scripts.lib.utils.logger_utils import get_logger
from scripts.lib.utils.param_utils import get_md_text


class MarkdownToHtmlTextTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """
        # get parameters
        md_text = get_md_text(tool_parameters)

        try:
            html_str = convert_md_to_html_text(md_text, is_strip_wrapper=True)
        except Exception as e:
            self.logger.exception("Failed to convert markdown text to HTML text")
            yield self.create_text_message(f"Failed to convert markdown text to HTML text, error: {str(e)}")
            return

        yield self.create_text_message(html_str)
        return
