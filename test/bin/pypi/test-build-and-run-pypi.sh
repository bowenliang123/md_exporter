#!/bin/bash

set -e

# Get the absolute path of the directory containing the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "Created temporary directory: $TEMP_DIR"

# Clean up temporary directory on exit
cleanup() {
    echo "Cleaning up temporary directory: $TEMP_DIR"
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Step 1: Clean dist folder and build the package using uv build
echo "Step 1: Cleaning dist folder and building the package using uv build"
cd "$PROJECT_ROOT"
rm -rf dist
uv build

# Step 2: Create virtual environment in temporary directory
echo "Step 2: Creating virtual environment in temporary directory"
cd "$TEMP_DIR"
python3 -m venv .venv

# Step 3: Activate virtual environment and install the package
echo "Step 3: Activating virtual environment and installing the package"
source ".venv/bin/activate"
pip install --upgrade pip
# Install the wheel file instead of the tar.gz
cd "$PROJECT_ROOT/dist"
WHEEL_FILE=$(ls md_exporter-*.whl | head -1)
pip install "$PROJECT_ROOT/dist/$WHEEL_FILE"
cd "$TEMP_DIR"

# Step 4: Test the markdown-exporter command
echo "Step 4: Testing the markdown-exporter command"
markdown-exporter --help || true

# Test each subcommand with --help
echo "Step 5: Testing each subcommand with --help"
subcommands=("md_to_codeblock" "md_to_csv" "md_to_docx" "md_to_html" "md_to_html_text" "md_to_ipynb" "md_to_json" "md_to_latex" "md_to_md" "md_to_pdf" "md_to_png" "md_to_pptx" "md_to_xlsx" "md_to_xml")

for subcommand in "${subcommands[@]}"; do
    echo "Testing $subcommand..."
    markdown-exporter "$subcommand" --help || true
    echo ""
done

# Step 6: Run all PyPI CLI tests
echo "Step 6: Running all PyPI CLI tests"
"$PROJECT_ROOT/test/bin/pypi/run_all_tests_pypi.sh"

echo "All tests completed successfully!"
