import os
import shutil
import subprocess


def test_md_to_linked_image():
    # Define input and output paths
    input_file = "test/skills/test_sample.md"
    output_dir = "test_output/images"
    
    # Ensure output directory exists
    os.makedirs("test_output", exist_ok=True)
    
    try:
        # Run the tool using uv command, setting PYTHONPATH to include the project root
        env = os.environ.copy()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        env["PYTHONPATH"] = f"{project_root}:{env.get('PYTHONPATH', '')}"
        subprocess.run([
            "uv", "run", "python", "scripts/md_to_linked_image.py",
            input_file, output_dir
        ], check=True, env=env)
        
        # Verify the output directory is not empty
        assert os.path.exists(output_dir), f"Output directory {output_dir} was not created"
        assert len(os.listdir(output_dir)) > 0, f"Output directory {output_dir} is empty"
        
    finally:
        # Clean up the output directory
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
