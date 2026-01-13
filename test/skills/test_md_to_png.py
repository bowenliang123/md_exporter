import os

from test_base import TestBase


class TestMdToPng(TestBase):
    def test_md_to_png(self):
        # Define input and output paths
        input_file = "test/resources/example_md.md"
        output_file = "test_output/test.png"
        
        try:
            # Run the tool using the base class method
            self.run_script("md_to_png.py", input_file, output_file)
            
            # Verify the output file is not empty
            self.verify_output_file(output_file)
            
        finally:
            # Clean up the output file
            if os.path.exists(output_file):
                os.remove(output_file)
            # Also clean up any numbered PNG files that might be generated
            for file in os.listdir("test_output"):
                if file.startswith("test_") and file.endswith(".png"):
                    os.remove(os.path.join("test_output", file))
