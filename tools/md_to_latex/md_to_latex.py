from collections.abc import Generator
from pathlib import Path
from tempfile import NamedTemporaryFile

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from scripts.services.svc_md_to_latex import convert_md_to_latex
from scripts.utils.file_utils import get_meta_data
from scripts.utils.logger_utils import get_logger
from scripts.utils.mimetype_utils import MimeType
from scripts.utils.param_utils import get_md_text_from_tool_params


class MarkdownToLatexTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text_from_tool_params(tool_parameters)
        output_filename = tool_parameters.get("output_filename")

        try:
            # create a temporary output LaTeX file
            with NamedTemporaryFile(suffix=".tex", delete=False) as temp_latex_file:
                temp_latex_output_path = Path(temp_latex_file.name)

            # convert markdown to latex using the shared function
            created_files = convert_md_to_latex(md_text, temp_latex_output_path, is_strip_wrapper=True)

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
                        mime_type=MimeType.LATEX,
                        output_filename=result_filename,
                    ),
                )

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to LaTeX file")
            yield self.create_text_message(f"Failed to convert markdown text to LaTeX file, error: {str(e)}")
            return
        finally:
            # clean up temporary files
            if "temp_latex_output_path" in locals():
                temp_latex_output_path.unlink(missing_ok=True)
            if "created_files" in locals():
                for file_path in created_files:
                    file_path.unlink(missing_ok=True)

        return
