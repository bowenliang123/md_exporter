import re

import markdown

CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')
# 正则表达式组合：平假名 + 片假名 + 日文汉字
JAPANESE_CHAR_PATTERN = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')


class MarkdownUtils:
    CSS_FOR_TABLE = """
    <!-- CSS for table -->
    <style>
        table, th, td {
            border: 1px solid;
        }
        table {
            width: 100%;
        }
    </style>
    """

    @classmethod
    def convert_markdown_to_html(cls, md_text: str) -> str:
        # official supported Markdown extensions:
        # https://python-markdown.github.io/extensions/#officially-supported-extensions
        html = markdown.markdown(text=md_text, extensions=["extra", "toc"])
        return f"""
        {html}
        {cls.CSS_FOR_TABLE}
        """ if "<table>" in html else html

    @staticmethod
    def strip_markdown_wrapper(md_text: str) -> str:
        # removing leading and trailing whitespaces
        md_text = md_text.strip()

        # removing codeblock wrapper if existed
        wrapper = "```"
        if md_text.endswith(wrapper):
            if md_text.startswith(wrapper):
                md_text = md_text[len(wrapper): -len(wrapper)]
            elif md_text.startswith(f"{wrapper}markdown"):
                md_text = md_text[(len(f"{wrapper}markdown")): -len(wrapper)]

        return md_text

    @staticmethod
    def contains_chinese(md_text: str) -> bool:
        return bool(CHINESE_CHAR_PATTERN.search(md_text))

    @staticmethod
    def contains_japanese(md_text: str) -> bool:
        return bool(JAPANESE_CHAR_PATTERN.search(md_text))
