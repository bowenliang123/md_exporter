from io import StringIO
from logging import Logger

import markdown
import pandas as pd
from bs4 import BeautifulSoup
from pandas import DataFrame

from scripts.lib.utils.md_utils import MarkdownUtils

SUGGESTED_SHEET_NAME = "suggested_sheet_name"


class TableParser:
    @staticmethod
    def parse_md_to_tables(logger: Logger, md_text: str,
                           force_value_to_str: bool = True,
                           extract_headings_for_sheet_names: bool = True,
                           ) -> list[pd.DataFrame]:
        """
        Parse markdown text to tables
        :param logger: Logger
        :param md_text: markdown text
        :param force_value_to_str: whether to force all columns to string type
        :param extract_headings_for_sheet_names: 
        :return: list of tables
        """
        try:
            md_text = MarkdownUtils.strip_markdown_wrapper(md_text)
            if not md_text.startswith('|') and '|' in md_text:
                md_text = md_text.replace('|', '\n|', 1)

            html_str = markdown.markdown(text=md_text, extensions=['tables'])
            tables: list[DataFrame] = pd.read_html(StringIO(html_str), encoding="utf-8")
            headings: list[str] = TableParser.extract_headings(html_str, extract_headings_for_sheet_names)

            def post_process_table(table: DataFrame) -> DataFrame:
                table = table.fillna("")
                if force_value_to_str:
                    for col in table.columns:
                        if table[col].dtype not in {'object', 'string'}:
                            table[col] = table[col].astype(str)
                return table

            result_tables = []
            for i, table in enumerate(tables):
                if not table.empty:
                    process_table = post_process_table(table)
                    if headings and i < len(headings):
                        process_table.attrs[SUGGESTED_SHEET_NAME] = headings[i]
                    result_tables.append(process_table)

            tables = result_tables

            if not tables or len(tables) <= 0:
                raise ValueError("No available tables parsed from markdown text")
            return tables
        except Exception as e:
            msg = f"Failed to parse markdown to tables, exception: {str(e)}"
            logger.exception(msg)
            raise ValueError(msg)

    @staticmethod
    def extract_headings(html_str: str, extract_headings_for_sheet_names: bool) -> list[str]:
        """
        Extract headings from HTML string.
        :param html_str: HTML string
        :return: list of headings
        """
        if not extract_headings_for_sheet_names:
            return []

        soup = BeautifulSoup(html_str, 'html.parser')
        headings = []
        for i in range(1, 6):
            for tag in soup.find_all(f'h{i}'):
                tag_text = tag.text.strip()
                if tag_text:
                    # The maximum length allowed for an Excel sheet name is 31 characters
                    tag_text = tag_text[0:30] if len(tag_text) > 30 else tag_text
                    headings.append(tag_text)
        return headings
