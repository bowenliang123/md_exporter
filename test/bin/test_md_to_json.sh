#!/bin/bash

# Test script for md_to_json.sh

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/common_test_runner.sh"

# Set up test environment
setup_test_env

# Run test
run_file_test "md_to_json" "test/resources/example_md_table.md" "json"