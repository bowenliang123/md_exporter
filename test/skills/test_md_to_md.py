from test_base import TestBase


class TestMdToMd(TestBase):
    def test_md_to_md(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.md"
        
        # Run the tool using the base class method
        self.run_script("md_to_md.py", input_file, output_file)
        
        # Verify the output file is not empty
        self.verify_output_file(output_file)
