import os

# Add the project root to Python path to fix import issues
import sys
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.lib.svc_md_to_md import convert_md_to_md


def test_md_to_md():
    # Define input and output paths
    input_file = "test/resources/example_md.md"
    output_file = "test_output/test.md"
    
    # Ensure output directory exists
    os.makedirs("test_output", exist_ok=True)
    
    try:
        # Read input file
        with open(input_file, encoding='utf-8') as f:
            md_text = f.read()
        
        # Call the conversion function directly
        output_path = Path(output_file)
        result_path = convert_md_to_md(md_text, output_path)
        
        # Verify the output file is not empty
        assert os.path.exists(result_path), f"Output file {result_path} was not created"
        assert os.path.getsize(result_path) > 0, f"Output file {result_path} is empty"
        
    finally:
        # Clean up the output file
        if os.path.exists(output_file):
            os.remove(output_file)
