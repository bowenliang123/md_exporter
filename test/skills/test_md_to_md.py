import os

# Add the project root to Python path to fix import issues
import sys
from pathlib import Path

from test_base import TestBase

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.services.svc_md_to_md import convert_md_to_md


class TestMdToMd(TestBase):
    def test_md_to_md(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.md"
        
        # Register output for cleanup
        self.register_output(output_file)
        
        # Read input file
        with open(input_file, encoding='utf-8') as f:
            md_text = f.read()
        
        # Call the conversion function directly
        output_path = Path(output_file)
        result_path = convert_md_to_md(md_text, output_path)
        
        # Verify the output file is not empty
        self.verify_output_file(result_path)
