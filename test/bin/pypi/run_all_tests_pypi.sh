#!/bin/bash

# Run all PyPI CLI tests

# Get the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set up test environment
echo "Setting up test environment..."
. "$SCRIPT_DIR/common_test_runner_pypi.sh"
setup_test_env

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Run all tests
test_scripts=(
    "test_cli_md_to_codeblock.sh"
    "test_cli_md_to_csv.sh"
    "test_cli_md_to_docx.sh"
    "test_cli_md_to_html.sh"
    "test_cli_md_to_html_text.sh"
    "test_cli_md_to_ipynb.sh"
    "test_cli_md_to_json.sh"
    "test_cli_md_to_latex.sh"
    "test_cli_md_to_md.sh"
    "test_cli_md_to_pdf.sh"
    "test_cli_md_to_png.sh"
    "test_cli_md_to_pptx.sh"
    "test_cli_md_to_xlsx.sh"
    "test_cli_md_to_xml.sh"
)

for test_script in "${test_scripts[@]}"; do
    test_script_path="$SCRIPT_DIR/$test_script"
    if [ -f "$test_script_path" ]; then
        echo "\nRunning $test_script..."
        "$test_script_path"
        if [ $? -eq 0 ]; then
            ((TESTS_PASSED++))
        else
            ((TESTS_FAILED++))
        fi
    else
        echo "\nSkipping $test_script: File not found"
        ((TESTS_FAILED++))
    fi
done

# Print summary
echo "\n======================================"
echo "Test Summary"
echo "======================================"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo "Total tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -eq 0 ]; then
    echo "\n✓ All tests passed!"
    exit 0
else
    echo "\n✗ Some tests failed!"
    exit 1
fi
