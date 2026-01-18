#!/bin/bash

# Test script for md_to_linked_image.sh

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/common_test_runner.sh"

# Set up test environment
setup_test_env

# Run test
run_dir_test "md_to_linked_image" "test/resources/example_md.md"