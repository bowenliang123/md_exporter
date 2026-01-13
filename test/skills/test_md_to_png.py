
from test_base import TestBase


class TestMdToPng(TestBase):
    def test_md_to_png(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.png"
        
        # Run the tool using the base class method
        self.run_script("md_to_png.py", input_file, output_file)
        
        # Verify the output file is not empty
        self.verify_output_file(output_file)
