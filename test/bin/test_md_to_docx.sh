#!/bin/bash

# Test script for md_to_docx.sh

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/test_common.sh"

# Set up test environment
setup_test_env

# Run test
run_file_test "md_to_docx" "test/resources/example_md.md" "docx"