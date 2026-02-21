#!/bin/bash

# Test script for md_to_ipynb

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/common_test_runner_pypi.sh"

# Set up test environment
setup_test_env

# Run test
run_file_test "md_to_ipynb" "test/resources/example_md_ipynb.md" "ipynb"
