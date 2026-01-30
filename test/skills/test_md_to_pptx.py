from test_base import TestBase


class TestMdToPptx(TestBase):
    def test_md_to_pptx(self):
        # Define input and output paths
        input_file = "test/resources/example_md_pptx.md"
        output_file = "test_output/test.pptx"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_pptx.py", input_file, output_file)

        # Verify the output file is not empty
        self.verify_output_file(output_file)
