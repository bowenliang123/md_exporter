from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.md_to_csv.md_to_csv import MarkdownToCsvTool
from tools.md_to_docx.md_to_docx import MarkdownToDocxTool
from tools.md_to_html.md_to_html import MarkdownToHtmlTool
from tools.md_to_json.md_to_json import MarkdownToJsonTool
from tools.md_to_md.md_to_md import MarkdownToMarkdownTool
from tools.md_to_pdf.md_to_pdf import MarkdownToPdfTool
from tools.md_to_pptx.md_to_pptx import MarkdownToPptxTool
from tools.md_to_xlsx.md_to_xlsx import MarkdownToXlsxTool


class MdExporterProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            MarkdownToCsvTool.from_credentials({})
            MarkdownToDocxTool.from_credentials({})
            MarkdownToHtmlTool.from_credentials({})
            MarkdownToJsonTool.from_credentials({})
            MarkdownToMarkdownTool.from_credentials({})
            MarkdownToPdfTool.from_credentials({})
            MarkdownToPptxTool.from_credentials({})
            MarkdownToXlsxTool.from_credentials({})
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
