#!/bin/bash

# Test script for md_to_mermaid.sh

# Source common functions
. "$(dirname "${BASH_SOURCE[0]}")/test_common.sh"

# Set up test environment
setup_test_env

# Run test with test_mermaid.md which contains mermaid code blocks
run_dir_test "md_to_mermaid" "test/resources/example_md_mermaid.md"
