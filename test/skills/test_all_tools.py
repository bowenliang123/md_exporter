# import os
# import pytest
# from pathlib import Path
#
# # Add the project root to Python path to fix import issues
# import sys
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# sys.path.insert(0, project_root)
#
# # Import all conversion functions
# from scripts.lib.svc_md_to_csv import convert_md_to_csv
# from scripts.lib.svc_md_to_pdf import convert_md_to_pdf
# from scripts.lib.svc_md_to_docx import convert_md_to_docx
# from scripts.lib.svc_md_to_xlsx import convert_md_to_xlsx
# from scripts.lib.svc_md_to_pptx import convert_md_to_pptx
# from scripts.lib.svc_md_to_codeblock import convert_md_to_codeblock
# from scripts.lib.svc_md_to_json import convert_md_to_json
# from scripts.lib.svc_md_to_xml import convert_md_to_xml
# from scripts.lib.svc_md_to_latex import convert_md_to_latex
# from scripts.lib.svc_md_to_html import convert_md_to_html
# from scripts.lib.svc_md_to_html_text import convert_md_to_html_text
# from scripts.lib.svc_md_to_png import convert_md_to_png
# from scripts.lib.svc_md_to_md import convert_md_to_md
# from scripts.lib.svc_md_to_linked_image import convert_md_to_linked_image
#
#
# # Read test sample markdown text once
# with open("test/skills/test_sample.md", 'r', encoding='utf-8') as f:
#     TEST_MD_TEXT = f.read()
#
#
# class TestMarkdownExporter:
#     """Test all markdown conversion tools"""
#
#     def setup_class(self):
#         """Setup test environment"""
#         # Ensure output directory exists
#         os.makedirs("test_output", exist_ok=True)
#
#     def teardown_method(self, method):
#         """Clean up after each test"""
#         # Clean up test_output directory
#         for file in os.listdir("test_output"):
#             file_path = os.path.join("test_output", file)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#             elif os.path.isdir(file_path):
#                 import shutil
#                 shutil.rmtree(file_path)
#
#     def test_md_to_csv(self):
#         """Test Markdown to CSV conversion"""
#         output_path = Path("test_output/test.csv")
#         result = convert_md_to_csv(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_pdf(self):
#         """Test Markdown to PDF conversion"""
#         output_path = Path("test_output/test.pdf")
#         result = convert_md_to_pdf(TEST_MD_TEXT, output_path)
#         assert result.exists(), f"Output file {result} was not created"
#         assert result.stat().st_size > 0, f"Output file {result} is empty"
#
#     def test_md_to_docx(self):
#         """Test Markdown to DOCX conversion"""
#         output_path = Path("test_output/test.docx")
#         result = convert_md_to_docx(TEST_MD_TEXT, output_path)
#         assert result.exists(), f"Output file {result} was not created"
#         assert result.stat().st_size > 0, f"Output file {result} is empty"
#
#     def test_md_to_xlsx(self):
#         """Test Markdown to XLSX conversion"""
#         output_path = Path("test_output/test.xlsx")
#         result = convert_md_to_xlsx(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_pptx(self):
#         """Test Markdown to PPTX conversion"""
#         output_path = Path("test_output/test.pptx")
#         result = convert_md_to_pptx(TEST_MD_TEXT, output_path)
#         assert result.exists(), f"Output file {result} was not created"
#         assert result.stat().st_size > 0, f"Output file {result} is empty"
#
#     def test_md_to_codeblock(self):
#         """Test Markdown to Codeblock conversion"""
#         output_path = Path("test_output/codeblocks")
#         result = convert_md_to_codeblock(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_json(self):
#         """Test Markdown to JSON conversion"""
#         output_path = Path("test_output/test.json")
#         result = convert_md_to_json(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_xml(self):
#         """Test Markdown to XML conversion"""
#         output_path = Path("test_output/test.xml")
#         result = convert_md_to_xml(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_latex(self):
#         """Test Markdown to LaTeX conversion"""
#         output_path = Path("test_output/test.tex")
#         result = convert_md_to_latex(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_html(self):
#         """Test Markdown to HTML conversion"""
#         output_path = Path("test_output/test.html")
#         result = convert_md_to_html(TEST_MD_TEXT, output_path)
#         assert result.exists(), f"Output file {result} was not created"
#         assert result.stat().st_size > 0, f"Output file {result} is empty"
#
#     def test_md_to_html_text(self):
#         """Test Markdown to HTML Text conversion"""
#         result = convert_md_to_html_text(TEST_MD_TEXT)
#         assert result.strip() != "", "Output is empty"
#
#     def test_md_to_png(self):
#         """Test Markdown to PNG conversion"""
#         output_path = Path("test_output/test.png")
#         result = convert_md_to_png(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
#
#     def test_md_to_md(self):
#         """Test Markdown to MD conversion"""
#         output_path = Path("test_output/test.md")
#         result = convert_md_to_md(TEST_MD_TEXT, output_path)
#         assert result.exists(), f"Output file {result} was not created"
#         assert result.stat().st_size > 0, f"Output file {result} is empty"
#
#     def test_md_to_linked_image(self):
#         """Test Markdown to Linked Image conversion"""
#         output_path = Path("test_output/images")
#         result = convert_md_to_linked_image(TEST_MD_TEXT, output_path)
#         assert len(result) > 0, "No output files created"
#         for file_path in result:
#             assert file_path.exists(), f"Output file {file_path} was not created"
#             assert file_path.stat().st_size > 0, f"Output file {file_path} is empty"
