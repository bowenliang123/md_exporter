import os

from test_base import TestBase


class TestMdToPptx(TestBase):
    def test_md_to_pptx(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.pptx"
        
        try:
            # Run the tool using the base class method
            self.run_script("md_to_pptx.py", input_file, output_file)
            
            # Verify the output file is not empty
            self.verify_output_file(output_file)
            
        finally:
            # Clean up the output file
            if os.path.exists(output_file):
                os.remove(output_file)
