import os
import subprocess


def test_md_to_html():
    # Define input and output paths
    input_file = "test/resources/example_md.md"
    output_file = "test_output/test.html"
    
    # Ensure output directory exists
    os.makedirs("test_output", exist_ok=True)
    
    try:
        # Run the tool using uv command, setting PYTHONPATH to include the project root
        env = os.environ.copy()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"
        subprocess.run([
            "uv", "run", "python", "scripts/md_to_html.py",
            input_file, output_file
        ], check=True, env=env)
        
        # Verify the output file is not empty
        assert os.path.exists(output_file), f"Output file {output_file} was not created"
        assert os.path.getsize(output_file) > 0, f"Output file {output_file} is empty"
        
    finally:
        # Clean up the output file
        if os.path.exists(output_file):
            os.remove(output_file)
