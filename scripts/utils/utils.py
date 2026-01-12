import re
from io import StringIO

import markdown
import pandas as pd
from bs4 import BeautifulSoup

# Regex pattern for removing think tags
THINK_TAG_REGEX = re.compile(r'<think>.*?</think>', flags=re.DOTALL)

# Regex pattern for matching Chinese characters
CHINESE_CHAR_PATTERN = re.compile(r'[\u4e00-\u9fff]')

# Regex pattern for matching Japanese characters
JAPANESE_CHAR_PATTERN = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')


SUGGESTED_SHEET_NAME = "suggested_sheet_name"


def get_md_text(md_text: str, 
                is_strip_wrapper: bool = False,
                is_remove_think_tag: bool = True,
                is_normalize_line_breaks: bool = True) -> str:
    """Process Markdown text"""
    md_text = md_text.strip() if md_text else None
    if not md_text:
        raise ValueError("Empty input md_text")

    # Remove think tags
    if is_remove_think_tag:
        md_text = THINK_TAG_REGEX.sub('', md_text)

    if is_strip_wrapper:
        md_text = strip_markdown_wrapper(md_text)

    # Normalize line breaks
    if is_normalize_line_breaks and "\\n" in md_text:
        md_text = md_text.replace("\\n", "\n")

    return md_text


def strip_markdown_wrapper(md_text: str) -> str:
    """Remove Markdown code block wrapper"""
    md_text = md_text.strip()
    wrapper = "```"
    if md_text.endswith(wrapper):
        if md_text.startswith(wrapper):
            md_text = md_text[len(wrapper): -len(wrapper)]
        elif md_text.startswith(f"{wrapper}markdown"):
            md_text = md_text[(len(f"{wrapper}markdown")): -len(wrapper)]
    return md_text


def contains_chinese(md_text: str) -> bool:
    """Check if contains Chinese characters"""
    return bool(CHINESE_CHAR_PATTERN.search(md_text))


def contains_japanese(md_text: str) -> bool:
    """Check if contains Japanese characters"""
    return bool(JAPANESE_CHAR_PATTERN.search(md_text))


def convert_markdown_to_html(md_text: str) -> str:
    """Convert Markdown to HTML"""
    html = markdown.markdown(text=md_text, extensions=["extra", "toc"])
    CSS_FOR_TABLE = """
    <style>
        table, th, td {
            border: 1px solid;
        }
        table {
            width: 100%;
        }
    </style>
    """
    return f"""
    {html}
    {CSS_FOR_TABLE}
    """ if "<table>" in html else html


def parse_md_to_tables(md_text: str,
                       force_value_to_str: bool = True,
                       extract_headings_for_sheet_names: bool = True) -> list[pd.DataFrame]:
    """Parse Markdown text to tables"""
    try:
        md_text = strip_markdown_wrapper(md_text)
        if not md_text.startswith('|') and '|' in md_text:
            md_text = md_text.replace('|', '\n|', 1)

        html_str = markdown.markdown(text=md_text, extensions=['tables'])
        tables: list[pd.DataFrame] = pd.read_html(StringIO(html_str), encoding="utf-8")
        headings: list[str] = extract_headings(html_str, extract_headings_for_sheet_names)

        def post_process_table(table: pd.DataFrame) -> pd.DataFrame:
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
        raise ValueError(f"Failed to parse markdown to tables, exception: {str(e)}")


def extract_headings(html_str: str, extract_headings_for_sheet_names: bool) -> list[str]:
    """Extract headings from HTML"""
    if not extract_headings_for_sheet_names:
        return []

    soup = BeautifulSoup(html_str, 'html.parser')
    headings = []
    for i in range(1, 6):
        for tag in soup.find_all(f'h{i}'):
            tag_text = tag.text.strip()
            if tag_text:
                tag_text = tag_text[0:30] if len(tag_text) > 30 else tag_text
                headings.append(tag_text)
    return headings
