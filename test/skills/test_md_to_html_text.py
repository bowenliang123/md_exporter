import os
import subprocess


def test_md_to_html_text():
    # Define input path
    input_file = "test/skills/test_sample.md"
    
    try:
        # Run the tool using uv command, setting PYTHONPATH to include the project root
        env = os.environ.copy()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"
        result = subprocess.run([
            "uv", "run", "python", "scripts/md_to_html_text.py",
            input_file
        ], check=True, capture_output=True, text=True, env=env)
        
        # Verify the output is not empty
        assert result.stdout.strip() != "", "Output is empty"
        
    finally:
        # No output file to clean up for this tool
        pass
