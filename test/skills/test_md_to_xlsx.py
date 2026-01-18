
from test_base import TestBase


class TestMdToXlsx(TestBase):
    def test_md_to_xlsx(self):
        # Define input and output paths
        input_file = "test/resources/example_md_table.md"
        output_file = "test_output/test.xlsx"
        
        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_xlsx.py", input_file, output_file)
        
        # Verify the output file is not empty
        self.verify_output_file(output_file)
