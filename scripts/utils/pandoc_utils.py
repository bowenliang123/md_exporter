from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from pypandoc import convert_file, convert_text


def pandoc_convert_file(md_text: str, dst_format: str, extra_args: Optional[list[str]]) -> bytes:
    with NamedTemporaryFile(suffix=".md", delete=True) as md_file:
        md_file.write(md_text.encode("utf-8"))
        md_file.flush()

        with NamedTemporaryFile(suffix=f".{dst_format}", delete=True) as target_file:
            convert_file(
                source_file=md_file.name,
                format="markdown",
                to=dst_format,
                outputfile=target_file.name,
                extra_args=extra_args,
            )
            target_file.flush()
            return Path(target_file.name).read_bytes()


def pandoc_convert_text(md_text: str, dst_format: str) -> bytes:
    txt = convert_text(md_text, format="markdown", to=dst_format)
    return txt.encode("utf-8")
