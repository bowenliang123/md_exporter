import os.path
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Generator, Optional

import pptx  # type: ignore
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File

from tools.utils.file_utils import get_meta_data
from tools.utils.logger_utils import get_logger
from tools.utils.mimetype_utils import MimeType
from tools.utils.param_utils import get_md_text

DEFAULT_TEMPLATE_PPTX_FILE_PATH = str(Path(__file__).resolve().parent / "template" / "Bowen Template.pptx")
MD2PPTX_FOLDER = "md2pptx-6.0"


class MarkdownToPptxTool(Tool):
    logger = get_logger(__name__)

    def _invoke(self, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """
        invoke tools
        """

        # get parameters
        md_text = get_md_text(tool_parameters)
        pptx_template_file: Optional[File] = tool_parameters.get("pptx_template_file")

        # check parameters
        if "``` run-python" in md_text:
            raise ValueError("The `run-python` marco of md2pptx is not allowed.")
        if pptx_template_file and not isinstance(pptx_template_file, File):
            raise ValueError("Not a valid file for pptx template file")

        temp_pptx_template_file: Optional[NamedTemporaryFile] = None
        temp_pptx_template_file_path: Optional[str] = None
        try:
            if pptx_template_file:
                temp_pptx_template_file = NamedTemporaryFile(delete=False)
                temp_pptx_template_file.write(pptx_template_file.blob)
                temp_pptx_template_file.close()
                temp_pptx_template_file_path = temp_pptx_template_file.name

            # create a temp directory that md2pptx uses
            with TemporaryDirectory() as temp_dir_path:
                # prepend md2pptx metadata configs
                md_text = self._prepend_metadata(
                    md_text=md_text,
                    temp_dir_path=temp_dir_path,
                    custom_template_file_path=temp_pptx_template_file_path,
                )
                # write markdown text to a temp source file
                with NamedTemporaryFile(suffix=".md", delete=True) as temp_md_file:
                    Path(temp_md_file.name).write_text(md_text, encoding="utf-8")

                    # run md2pptx to convert md file to pptx file
                    with NamedTemporaryFile(suffix=".pptx", delete=True) as temp_pptx_file:
                        current_script_folder = os.path.split(os.path.realpath(__file__))[0]
                        python_exec = sys.executable or "python3"
                        cmd = [python_exec, f"{current_script_folder}/{MD2PPTX_FOLDER}/md2pptx.py",
                               temp_md_file.name,
                               temp_pptx_file.name]

                        result = subprocess.run(
                            cmd,
                            timeout=60,  # timeout in seconds
                            capture_output=True,
                            text=True
                        )
                        if result.returncode != 0:
                            print(cmd)
                            raise Exception(f"Failed to convert markdown text to PPTX file,"
                                            f" command: {" ".join(cmd)},"
                                            f" return code: {result.returncode},"
                                            f" stdout: {result.stdout},"
                                            f" error: {result.stderr}")
                        result_file_bytes = Path(temp_pptx_file.name).read_bytes()

        except Exception as e:
            self.logger.exception("Failed to convert markdown text to PPTX file")
            # yield self.create_text_message(f"Failed to convert markdown text to PPTX file, error: {str(e)}")
            raise e
        finally:
            if temp_pptx_template_file:
                Path(temp_pptx_template_file.name).unlink(missing_ok=True)

        yield self.create_blob_message(
            blob=result_file_bytes,
            meta=get_meta_data(
                mime_type=MimeType.PPTX,
                output_filename=tool_parameters.get("output_filename"),
            ),
        )
        return

    @staticmethod
    def _prepend_metadata(md_text: str, temp_dir_path: str, custom_template_file_path: Optional[str]) -> str:
        """
        Prepend metadata to Markdown text
        """
        # the default template name is "Martin Template.pptx" in "md2pptx-*" subfolder
        template_pptx_file_path = custom_template_file_path if custom_template_file_path \
            else DEFAULT_TEMPLATE_PPTX_FILE_PATH
        temp_dir = f'tempDir: {temp_dir_path}'
        ppt_template = f"template: {template_pptx_file_path}"

        # delete the first slide
        # doc: https://github.com/MartinPacker/md2pptx/blob/master/docs/user-guide.md#deleting-the-first-processing-summary-slide---with-deletefirstslide
        delete_first_slide = "DeleteFirstSlide: yes"

        metadata_str = "\n".join([temp_dir, ppt_template, delete_first_slide])
        text = metadata_str + "\n" + md_text
        return text
