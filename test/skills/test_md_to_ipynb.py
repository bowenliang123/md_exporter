from test_base import TestBase


class TestMdToIpynb(TestBase):
    def test_md_to_ipynb(self):
        # Define input and output paths
        input_file = "test/resources/example_md_ipynb.md"
        output_file = "test_output/test.ipynb"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_ipynb.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)
