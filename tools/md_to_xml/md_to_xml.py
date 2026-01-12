from collections.abc import Generator

import markdown
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from lxml import etree, html

from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text


class MarkdownToXmlTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters, is_strip_wrapper=True)
        try:
            html_str = markdown.markdown(text=md_text, extensions=["extra", "toc"])
            xml_element = html.fromstring(html_str)
            result_file_bytes = etree.tostring(element_or_tree=xml_element,
                                               xml_declaration=True, pretty_print=True, encoding="UTF-8")
        except Exception as e:
            self.logger.exception("Failed to convert to XML file")
            yield self.create_text_message(f"Failed to convert markdown text to XML file, error: {str(e)}")
            return

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.XML,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return
