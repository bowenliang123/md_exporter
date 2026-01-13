from test_base import TestBase


class TestMdToHtmlText(TestBase):
    def test_md_to_html_text(self):
        # Define input path
        input_file = "test/resources/example_md.md"
        
        try:
            # Run the tool using the base class method and capture output
            result = self.run_script_with_output("md_to_html_text.py", input_file)
            
            # Verify the output is not empty
            self.assertNotEqual(result.stdout.strip(), "", "Output is empty")
            
        finally:
            # No output file to clean up for this tool
            pass
