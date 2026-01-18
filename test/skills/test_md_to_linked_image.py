from test_base import TestBase


class TestMdToLinkedImage(TestBase):
    def test_md_to_linked_image(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_dir = "test_output/images"

        # Run the tool using the base class method
        self.run_script("parser/cli_md_to_linked_image.py", input_file, output_dir)

        # Verify the output directory is not empty
        self.verify_output_dir(output_dir)
