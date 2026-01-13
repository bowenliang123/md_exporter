
from test_base import TestBase


class TestMdToJson(TestBase):
    def test_md_to_json(self):
        # Define input and output paths
        input_file = "test/resources/example_md_table.md"
        output_file = "test_output/test.json"
        
        # Run the tool using the base class method
        self.run_script("md_to_json.py", input_file, output_file)
        
        # Verify the output file is not empty
        self.verify_output_file(output_file)
