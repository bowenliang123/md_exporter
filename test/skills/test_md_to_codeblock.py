
from test_base import TestBase


class TestMdToCodeblock(TestBase):
    def test_md_to_codeblock(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_dir = "test_output/codeblocks"
        
        # Run the tool using the base class method
        self.run_script("md_to_codeblock.py", input_file, output_dir)
        
        # Verify the output directory is not empty
        self.verify_output_dir(output_dir)
