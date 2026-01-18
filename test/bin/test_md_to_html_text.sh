#!/bin/bash

# Test script for md_to_html_text.sh

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/common_test_runner.sh"

# Set up test environment
setup_test_env

# Run test
run_stdout_test "md_to_html_text" "test/resources/example_md.md"